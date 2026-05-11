from __future__ import annotations

from app.services.learning_plan_service import LearningPlanService
from app.services.project_plan_service import ProjectPlanService


class GenerateLearningPlanTool:
    name = "generate_learning_plan"
    description = "Generate a phased learning plan and project plan from the gap analysis."
    input_schema = {"type": "object", "required": ["gap_analysis"]}

    def __init__(
        self,
        learning_service: LearningPlanService | None = None,
        project_service: ProjectPlanService | None = None,
    ) -> None:
        self.learning_service = learning_service or LearningPlanService()
        self.project_service = project_service or ProjectPlanService()

    async def run(self, job_analysis: dict, gap_analysis: dict, user_goal: str) -> tuple[dict, dict]:
        learning_plan = self.learning_service.generate(gap_analysis)
        project_plan = self.project_service.generate(job_analysis, gap_analysis, user_goal)
        return learning_plan, project_plan

