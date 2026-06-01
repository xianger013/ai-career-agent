from __future__ import annotations


class ResumeService:
    def generate(self, project_plan: dict, job_analysis: dict) -> list[str]:
        skills = ", ".join(job_analysis.get("required_skills", [])[:5])
        return [
            "Designed and implemented the AI Career Agent backend MVP with job creation, profile upload, evidence retrieval, and full analysis-report generation.",
            f"Wrapped an OpenAI-compatible LLMService and file-based prompt workflow to turn role requirements into structured outputs covering {skills}.",
            "Built a lightweight agent workflow and tool-calling abstraction that orchestrates load_job, analyze_job, search_profile_evidence, and save_report steps.",
            "Completed the first RAG loop with SQLite, SQLAlchemy, and fallback keyword retrieval, with pytest coverage for health checks, splitting, retrieval, and agent flow.",
            f"Project plan: {project_plan.get('Project name', 'AI Career Agent')}; ready to extend with SSE, vector databases, and the frontend workspace.",
        ]

