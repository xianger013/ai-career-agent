from __future__ import annotations

from app.services.interview_service import InterviewService


class GenerateInterviewQATool:
    name = "generate_interview_qa"
    description = "Generate interview questions and answers for the recommended project."
    input_schema = {"type": "object", "required": ["job_analysis", "gap_analysis", "project_plan"]}

    def __init__(self, service: InterviewService | None = None) -> None:
        self.service = service or InterviewService()

    async def run(self, job_analysis: dict, gap_analysis: dict, project_plan: dict) -> list[dict]:
        return self.service.generate(job_analysis, gap_analysis, project_plan)

