from fastapi.testclient import TestClient

from app.main import app


def test_career_agent_stream_returns_sse_final_event() -> None:
    with TestClient(app) as client:
        job_response = client.post(
            "/api/jobs",
            json={
                "title": "AI Agent Intern",
                "company": "Demo",
                "description": "Requires Python, FastAPI, LLM API, RAG, and agent workflow experience.",
            },
        )
        job_id = job_response.json()["id"]

        with client.stream(
            "GET",
            "/api/agents/career/analyze/stream",
            params={"job_id": job_id, "user_goal": "Apply for an AI Agent internship"},
        ) as response:
            body = "".join(response.iter_text())

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert "event: step" in body
    assert "event: final" in body
    assert "markdown_report" in body


def test_career_agent_stream_returns_error_event_for_missing_job() -> None:
    with TestClient(app) as client:
        with client.stream(
            "GET",
            "/api/agents/career/analyze/stream",
            params={"job_id": 999999, "user_goal": "missing"},
        ) as response:
            body = "".join(response.iter_text())

    assert response.status_code == 200
    assert "event: error" in body
    assert "Job 999999 not found" in body
