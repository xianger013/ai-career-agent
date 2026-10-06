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


def test_job_analyzer_fallback_keeps_chinese_keyword_support() -> None:
    job = Job(
        id=2,
        title="AI Agent Intern",
        company="Demo",
        description=(
            "\u9700\u8981 \u5927\u6a21\u578b\u3001\u63d0\u793a\u8bcd\u3001RAG\u3001"
            "\u5411\u91cf\u68c0\u7d22\u3001Agent \u5de5\u4f5c\u6d41\u3001"
            "\u6d4b\u8bd5\u548c\u540e\u7aef API \u7ecf\u9a8c\u3002"
        ),
    )

    result = asyncio.run(JobAnalyzer().analyze(job))

    assert result["llm_status"] == "fallback_no_llm_config"
    assert {"LLM API", "Prompt Engineering", "RAG", "Agent Workflow", "Testing"} <= set(result["required_skills"])
    assert "Implement document retrieval and evidence citation" in result["core_responsibilities"]
    assert "Provide stable backend API services" in result["core_responsibilities"]


class FailingConfiguredLLM:
    is_configured = True

    async def chat(self, messages: list[dict], temperature: float = 0.2) -> str:
        raise LLMServiceError("LLM provider returned HTTP 401: invalid key")


def test_job_analyzer_returns_llm_error_metadata_on_provider_failure() -> None:
    job = Job(
        id=3,
        title="AI Agent Intern",
        company="Demo",
        description="Requires Python and LLM API experience.",
    )

    result = asyncio.run(JobAnalyzer(llm_service=FailingConfiguredLLM()).analyze(job))

    assert result["llm_status"] == "fallback_after_llm_error"
    assert "HTTP 401" in result["llm_error"]
    assert "Python" in result["required_skills"]
