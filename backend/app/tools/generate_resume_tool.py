from __future__ import annotations

from app.services.resume_service import ResumeService


class GenerateResumeTool:
    name = "generate_resume_bullets"
    description = "Generate resume-ready bullet points from the project plan."
    input_schema = {"type": "object", "required": ["project_plan", "job_analysis"]}

    def __init__(self, service: ResumeService | None = None) -> None:
        self.service = service or ResumeService()

    async def run(self, project_plan: dict, job_analysis: dict) -> list[str]:
        return self.service.generate(project_plan, job_analysis)

