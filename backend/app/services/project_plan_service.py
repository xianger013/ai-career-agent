from __future__ import annotations


class ProjectPlanService:
    def generate(self, job_analysis: dict, gap_analysis: dict, user_goal: str) -> dict:
        skills = job_analysis.get("required_skills", [])[:6]
        missing = gap_analysis.get("missing_skills", [])[:3]
        return {
            "Project name": "AI Career Agent skill-gap analysis workspace",
            "Project goal": "Input a job description and profile notes, then generate skill gaps, a learning path, project plan, resume bullets, and interview Q&A.",
            "Why it fits this role": f"This project directly supports {user_goal} and demonstrates LLM, RAG, agent workflow, and backend engineering skills.",
            "Covered role skills": ", ".join(skills + missing) or "LLM API, RAG, Agent Workflow, FastAPI",
            "Tech stack": "Python, FastAPI, SQLAlchemy, SQLite, httpx, pytest, OpenAI-compatible API",
            "Feature modules": "Job management, profile upload, fallback retrieval, agent orchestration, Markdown report storage",
            "Development stages": "Backend MVP -> retrieval enhancement -> frontend workspace -> SSE -> Docker deployment",
            "Acceptance criteria per stage": "APIs work, tests pass, reports generate, and the demo flow is complete",
            "Resume positioning": "Emphasize an end-to-end AI agent engineering loop instead of only model calls.",
            "Future expansion": "Add a production vector database, SSE streaming, multi-user data isolation, and richer frontend visualization.",
        }

