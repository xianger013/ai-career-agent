from __future__ import annotations


class LearningPlanService:
    def generate(self, gap_analysis: dict) -> dict:
        priorities = gap_analysis.get("priority_order", [])
        focus = ", ".join(priorities[:3]) if priorities else "core job skills"
        return {
            "focus": focus,
            "phases": [
                {
                    "name": "Phase 1: Engineering foundation",
                    "goal": "Build a maintainable backend project structure",
                    "tasks": "FastAPI, SQLAlchemy, pytest, README",
                    "acceptance": "The API starts successfully and baseline tests pass",
                    "duration": "3-5 days",
                },
                {
                    "name": "Phase 2: LLM API integration",
                    "goal": "Implement OpenAI-compatible Chat Completions calls",
                    "tasks": "Wrap LLMService, handle provider errors, and store prompts as files",
                    "acceptance": "The job-analysis endpoint runs with either mocks or a real model",
                    "duration": "2-3 days",
                },
                {
                    "name": "Phase 3: RAG document retrieval",
                    "goal": f"Build evidence retrieval around {focus}",
                    "tasks": "Profile upload, text splitting, and fallback retrieval",
                    "acceptance": "Relevant profile chunks are returned for a query",
                    "duration": "3-4 days",
                },
                {
                    "name": "Phase 4: Tool calling",
                    "goal": "Wrap core capabilities as reusable tools",
                    "tasks": "AnalyzeJobTool, SearchProfileTool, SaveMarkdownTool",
                    "acceptance": "The agent executes tools in the intended order",
                    "duration": "2 days",
                },
                {
                    "name": "Phase 5: Agent workflow",
                    "goal": "Orchestrate the end-to-end flow from job description to report",
                    "tasks": "Gap analysis, learning plan, project plan, resume bullets, interview Q&A",
                    "acceptance": "A complete Markdown report is generated",
                    "duration": "4-5 days",
                },
                {
                    "name": "Phase 6: Full-stack demo and deployment",
                    "goal": "Complete frontend and deployment materials",
                    "tasks": "Next.js workspace, SSE, Docker",
                    "acceptance": "The project can be demonstrated locally and in a container",
                    "duration": "5-7 days",
                },
            ],
        }

