from __future__ import annotations

from pathlib import Path

from app.config import settings
from app.models.job import Job
from app.services.llm_service import LLMService, LLMServiceError


class JobAnalyzer:
    def __init__(self, llm_service: LLMService | None = None) -> None:
        self.llm_service = llm_service or LLMService()
        self.prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "job_analysis.md"

    async def analyze(self, job: Job) -> dict:
        prompt = self.prompt_path.read_text(encoding="utf-8")
        messages = [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": f"Job title: {job.title}\nCompany: {job.company}\nJob description:\n{job.description}",
            },
        ]

        if self.llm_service.is_configured:
            try:
                raw_markdown = await self.llm_service.chat(messages, temperature=settings.llm_temperature)
                return self._heuristic_analysis(job, raw_markdown=raw_markdown, llm_status="success")
            except LLMServiceError as exc:
                return self._heuristic_analysis(
                    job,
                    llm_status="fallback_after_llm_error",
                    llm_error=str(exc),
                )

        return self._heuristic_analysis(job, llm_status="fallback_no_llm_config")

    def _heuristic_analysis(
        self,
        job: Job,
        raw_markdown: str | None = None,
        llm_status: str = "fallback",
        llm_error: str | None = None,
    ) -> dict:
        text = f"{job.title}\n{job.description}".lower()
        skill_catalog = {
            "Python": ["python"],
            "FastAPI": ["fastapi"],
            "SQLAlchemy": ["sqlalchemy"],
            "SQL/SQLite": ["sql", "sqlite", "postgres"],
            "LLM API": ["llm", "openai", "chat completions", "large language model", "\\u5927\\u6a21\\u578b"],
            "Prompt Engineering": ["prompt", "prompt engineering", "\\u63d0\\u793a\\u8bcd"],
            "RAG": ["rag", "retrieval", "vector", "embedding", "\\u68c0\\u7d22", "\\u5411\\u91cf"],
            "Agent Workflow": ["agent", "workflow", "tool calling", "function calling", "\\u5de5\\u4f5c\\u6d41"],
            "Docker": ["docker"],
            "React/Next.js": ["react", "next.js", "nextjs"],
            "Testing": ["pytest", "test", "testing", "\\u6d4b\\u8bd5"],
        }
        found = [
            skill
            for skill, keywords in skill_catalog.items()
            if any(keyword in text for keyword in keywords)
        ]
        if not found:
            found = ["Python", "LLM API", "Prompt Engineering", "RAG", "FastAPI"]

        ai_skills = [skill for skill in found if skill in {"LLM API", "Prompt Engineering", "RAG", "Agent Workflow"}]
        engineering = [skill for skill in found if skill not in set(ai_skills)]
        responsibilities = [
            "Break down job-description requirements into reusable skill signals",
            "Build a reusable AI agent workflow",
            "Generate an actionable learning and project roadmap from profile evidence",
        ]
        if "rag" in text or "retrieval" in text or "\\u68c0\\u7d22" in text:
            responsibilities.append("Implement document retrieval and evidence citation")
        if "api" in text or "backend" in text or "\\u540e\\u7aef" in text:
            responsibilities.append("Provide stable backend API services")

        analysis = {
            "job_id": job.id,
            "llm_status": llm_status,
            "llm_error": llm_error,
            "role_type": job.title,
            "core_responsibilities": responsibilities,
            "required_skills": found,
            "bonus_skills": ["Deployment experience", "Automated testing", "Product-oriented communication"],
            "engineering_skills": engineering,
            "ai_skills": ai_skills or ["LLM API", "Prompt Engineering"],
            "product_skills": ["Requirement breakdown", "Structured result presentation", "User-goal alignment"],
            "suggested_projects": [
                "AI Career Agent skill-gap analysis workspace",
                "RAG-based personal knowledge-base assistant",
            ],
        }
        analysis["raw_markdown"] = raw_markdown or self._build_markdown(analysis)
        return analysis

    def _build_markdown(self, analysis: dict) -> str:
        def lines(items: list[str]) -> str:
            return "\n".join(f"- {item}" for item in items)

        return "\n\n".join(
            [
                "# Job Analysis Result",
                f"## 1. Role Type\n{analysis['role_type']}",
                f"## 2. Core Responsibilities\n{lines(analysis['core_responsibilities'])}",
                f"## 3. Required Technical Skills\n{lines(analysis['required_skills'])}",
                f"## 4. Bonus Skills\n{lines(analysis['bonus_skills'])}",
                f"## 5. AI Agent Skills\n{lines(analysis['ai_skills'])}",
                f"## 6. Engineering Skills\n{lines(analysis['engineering_skills'])}",
                "## 7. Priority Advice For Beginners\n- Complete the backend loop first, then improve retrieval quality and frontend presentation.",
                f"## 8. Project Directions To Close Skill Gaps\n{lines(analysis['suggested_projects'])}",
            ]
        )
