import asyncio

from app.models.job import Job
from app.services.job_analyzer import JobAnalyzer
from app.services.llm_service import LLMServiceError


def test_job_analyzer_fallback_returns_structured_result() -> None:
    job = Job(
        id=1,
        title="AI Agent Intern",
        company="Demo",
        description="Requires Python, FastAPI, LLM API, RAG, agent workflow, and pytest experience.",
    )

    result = asyncio.run(JobAnalyzer().analyze(job))

    assert result["job_id"] == 1
    assert result["llm_status"] == "fallback_no_llm_config"
    assert "Python" in result["required_skills"]
    assert "raw_markdown" in result


class FailingConfiguredLLM:
    is_configured = True

    async def chat(self, messages: list[dict], temperature: float = 0.2) -> str:
        raise LLMServiceError("LLM provider returned HTTP 401: invalid key")


def test_job_analyzer_returns_llm_error_metadata_on_provider_failure() -> None:
    job = Job(
        id=2,
        title="AI Agent Intern",
        company="Demo",
        description="Requires Python and LLM API experience.",
    )

    result = asyncio.run(JobAnalyzer(llm_service=FailingConfiguredLLM()).analyze(job))

    assert result["llm_status"] == "fallback_after_llm_error"
    assert "HTTP 401" in result["llm_error"]
    assert "Python" in result["required_skills"]
