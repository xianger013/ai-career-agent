from __future__ import annotations

from app.models.job import Job
from app.services.job_analyzer import JobAnalyzer


class AnalyzeJobTool:
    name = "analyze_job"
    description = "Analyze a job description into structured capability requirements."
    input_schema = {"type": "object", "required": ["job_id"]}

    def __init__(self, analyzer: JobAnalyzer | None = None) -> None:
        self.analyzer = analyzer or JobAnalyzer()

    async def run(self, job: Job) -> dict:
        return await self.analyzer.analyze(job)

