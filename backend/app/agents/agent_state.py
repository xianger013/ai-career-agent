from __future__ import annotations

from pydantic import BaseModel


class StepLog(BaseModel):
    step: str
    status: str
    summary: str


class CareerAgentResult(BaseModel):
    analysis_id: int
    job_analysis: dict
    profile_evidence: list[dict]
    gap_analysis: dict
    learning_plan: dict
    project_plan: dict
    resume_bullets: list[str]
    interview_qa: list[dict]
    markdown_report: str
    report_path: str
    step_logs: list[StepLog]

