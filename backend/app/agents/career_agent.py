from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncGenerator, Awaitable, Callable
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.agents.agent_state import CareerAgentResult, StepLog
from app.config import settings
from app.models.analysis import Analysis
from app.models.job import Job
from app.services.gap_analyzer import GapAnalyzer
from app.tools.analyze_job_tool import AnalyzeJobTool
from app.tools.generate_interview_qa_tool import GenerateInterviewQATool
from app.tools.generate_learning_plan_tool import GenerateLearningPlanTool
from app.tools.generate_resume_tool import GenerateResumeTool
from app.tools.save_markdown_tool import SaveMarkdownTool
from app.tools.search_profile_tool import SearchProfileTool
from app.utils.markdown import build_analysis_report


class CareerAgent:
    def __init__(self, db: Session, output_dir: Path | None = None) -> None:
        self.db = db
        self.output_dir = output_dir or settings.resolved_output_dir
        self.analyze_job_tool = AnalyzeJobTool()
        self.search_profile_tool = SearchProfileTool(db)
        self.gap_analyzer = GapAnalyzer()
        self.learning_plan_tool = GenerateLearningPlanTool()
        self.resume_tool = GenerateResumeTool()
        self.interview_tool = GenerateInterviewQATool()
        self.save_markdown_tool = SaveMarkdownTool()
        self.step_logs: list[StepLog] = []

    async def run(self, job_id: int, user_goal: str) -> CareerAgentResult:
        return await self._execute(job_id, user_goal)

    async def run_stream(self, job_id: int, user_goal: str) -> AsyncGenerator[dict[str, Any], None]:
        """Run the agent and stream stage-level events through an async queue."""
        queue: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue()

        async def emit(event: str, data: dict[str, Any]) -> None:
            await queue.put({"event": event, "data": data})

        async def runner() -> None:
            try:
                result = await self._execute(job_id, user_goal, emit=emit)
                await emit(
                    "final",
                    {
                        "analysis_id": result.analysis_id,
                        "markdown_report": result.markdown_report,
                        "report_path": result.report_path,
                    },
                )
            except Exception as exc:
                await emit("error", {"message": str(exc)})
            finally:
                await queue.put(None)

        task = asyncio.create_task(runner())
        try:
            while True:
                item = await queue.get()
                if item is None:
                    break
                yield item
        finally:
            await task

    async def _execute(
        self,
        job_id: int,
        user_goal: str,
        emit: Callable[[str, dict[str, Any]], Awaitable[None]] | None = None,
    ) -> CareerAgentResult:
        self.step_logs = []
        await self._emit_step(emit, "load_job", "running", "Loading job details")
        job = self._load_job(job_id)
        await self._emit_step(emit, "load_job", "done", f"Loaded job {job.title}")

        await self._emit_step(emit, "analyze_job", "running", "Analyzing job requirements")
        job_analysis = await self.analyze_job_tool.run(job)
        analyze_summary = f"Extracted {len(job_analysis.get('required_skills', []))} core skills"
        self._log("analyze_job", "done", analyze_summary)
        await self._emit_step(emit, "analyze_job", "done", analyze_summary)
        await self._emit_content(emit, "job_analysis", job_analysis.get("raw_markdown", ""))

        await self._emit_step(emit, "search_profile_evidence", "running", "Retrieving profile evidence")
        query = self._build_profile_query(job_analysis, user_goal)
        profile_evidence = await self.search_profile_tool.run(query, top_k=6)
        evidence_summary = f"Retrieved {len(profile_evidence)} evidence chunks"
        self._log("search_profile_evidence", "done", evidence_summary)
        await self._emit_step(emit, "search_profile_evidence", "done", evidence_summary)
        await self._emit_content(emit, "profile_evidence", self._to_json(profile_evidence))

        await self._emit_step(emit, "analyze_gap", "running", "Analyzing skill gaps")
        gap_analysis = self.gap_analyzer.analyze(job_analysis, profile_evidence)
        gap_summary = f"Found {len(gap_analysis.get('missing_skills', []))} missing skills"
        self._log("analyze_gap", "done", gap_summary)
        await self._emit_step(emit, "analyze_gap", "done", gap_summary)
        await self._emit_content(emit, "gap_analysis", self._to_json(gap_analysis))

        await self._emit_step(emit, "generate_learning_plan", "running", "Generating learning plan and project plan")
        learning_plan, project_plan = await self.learning_plan_tool.run(job_analysis, gap_analysis, user_goal)
        learning_summary = f"Generated {len(learning_plan.get('phases', []))} learning phases"
        self._log("generate_learning_plan", "done", learning_summary)
        await self._emit_step(emit, "generate_learning_plan", "done", learning_summary)
        await self._emit_content(emit, "learning_plan", self._to_json(learning_plan))
        await self._emit_step(emit, "generate_project_plan", "running", "Generating recommended project plan")
        self._log("generate_project_plan", "done", "Generated recommended project plan")
        await self._emit_step(emit, "generate_project_plan", "done", "Generated recommended project plan")
        await self._emit_content(emit, "project_plan", self._to_json(project_plan))

        await self._emit_step(emit, "generate_resume_bullets", "running", "Generating resume bullets")
        resume_bullets = await self.resume_tool.run(project_plan, job_analysis)
        resume_summary = f"Generated {len(resume_bullets)} resume bullets"
        self._log("generate_resume_bullets", "done", resume_summary)
        await self._emit_step(emit, "generate_resume_bullets", "done", resume_summary)
        await self._emit_content(emit, "resume_bullets", self._to_json(resume_bullets))

        await self._emit_step(emit, "generate_interview_qa", "running", "Generating interview Q&A")
        interview_qa = await self.interview_tool.run(job_analysis, gap_analysis, project_plan)
        interview_summary = f"Generated {len(interview_qa)} interview Q&A items"
        self._log("generate_interview_qa", "done", interview_summary)
        await self._emit_step(emit, "generate_interview_qa", "done", interview_summary)
        await self._emit_content(emit, "interview_qa", self._to_json(interview_qa))

        await self._emit_step(emit, "save_markdown_report", "running", "Assembling Markdown report")
        markdown_report = build_analysis_report(
            job,
            job_analysis,
            profile_evidence,
            gap_analysis,
            learning_plan,
            project_plan,
            resume_bullets,
            interview_qa,
        )
        self._log("save_markdown_report", "done", "Generated Markdown report content")
        await self._emit_step(emit, "save_markdown_report", "done", "Generated Markdown report content")

        await self._emit_step(emit, "persist_analysis", "running", "Saving analysis record and report file")
        record = self._persist_analysis(
            job.id,
            job_analysis,
            profile_evidence,
            gap_analysis,
            learning_plan,
            project_plan,
            resume_bullets,
            interview_qa,
            markdown_report,
        )
        report_path = await self.save_markdown_tool.run(
            markdown_report,
            self.output_dir,
            f"analysis_{record.id}.md",
        )
        self._log("persist_analysis", "done", f"Saved analysis record and report file {report_path.name}")
        await self._emit_step(emit, "persist_analysis", "done", f"Saved analysis record and report file {report_path.name}")

        return CareerAgentResult(
            analysis_id=record.id,
            job_analysis=job_analysis,
            profile_evidence=profile_evidence,
            gap_analysis=gap_analysis,
            learning_plan=learning_plan,
            project_plan=project_plan,
            resume_bullets=resume_bullets,
            interview_qa=interview_qa,
            markdown_report=markdown_report,
            report_path=str(report_path),
            step_logs=self.step_logs,
        )

    def _load_job(self, job_id: int) -> Job:
        job = self.db.get(Job, job_id)
        if job is None:
            raise ValueError(f"Job {job_id} not found.")
        self._log("load_job", "done", f"Loaded job {job.title}")
        return job

    def _build_profile_query(self, job_analysis: dict, user_goal: str) -> str:
        skills = " ".join(job_analysis.get("required_skills", []))
        responsibilities = " ".join(job_analysis.get("core_responsibilities", []))
        return f"{user_goal} {skills} {responsibilities}"

    def _persist_analysis(
        self,
        job_id: int,
        job_analysis: dict,
        profile_evidence: list[dict],
        gap_analysis: dict,
        learning_plan: dict,
        project_plan: dict,
        resume_bullets: list[str],
        interview_qa: list[dict],
        markdown_report: str,
    ) -> Analysis:
        record = Analysis(
            job_id=job_id,
            job_analysis_json=self._to_json(job_analysis),
            profile_evidence_json=self._to_json(profile_evidence),
            gap_analysis_json=self._to_json(gap_analysis),
            learning_plan_json=self._to_json(learning_plan),
            project_plan_json=self._to_json(project_plan),
            resume_bullets_json=self._to_json(resume_bullets),
            interview_qa_json=self._to_json(interview_qa),
            markdown_report=markdown_report,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def _log(self, step: str, status: str, summary: str) -> None:
        self.step_logs.append(StepLog(step=step, status=status, summary=summary))

    async def _emit_step(
        self,
        emit: Callable[[str, dict[str, Any]], Awaitable[None]] | None,
        name: str,
        status: str,
        message: str,
    ) -> None:
        if emit is not None:
            await emit("step", {"name": name, "status": status, "message": message})

    async def _emit_content(
        self,
        emit: Callable[[str, dict[str, Any]], Awaitable[None]] | None,
        section: str,
        content: str,
    ) -> None:
        if emit is not None:
            await emit("content", {"section": section, "content": content})

    def _to_json(self, value: object) -> str:
        return json.dumps(value, ensure_ascii=False)
