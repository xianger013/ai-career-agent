# AI Career Agent Backend

The backend is a FastAPI service for creating job records, uploading profile notes, retrieving profile evidence, running the CareerAgent workflow, and saving Markdown reports.

## Capabilities

- `GET /health` health check.
- Job creation and retrieval with SQLite and SQLAlchemy.
- `.md` and `.txt` profile upload.
- Text splitting and fallback keyword retrieval.
- Optional OpenAI-compatible embedding retrieval through JSON VectorStore.
- OpenAI-compatible LLM calls with deterministic fallback behavior.
- CareerAgent workflow with stage-level SSE streaming.
- Markdown report generation and persisted analysis records.
- pytest coverage for health, text splitting, vector store, embedding service, job analysis, and agent workflow.

## Quick Start

```powershell
cd backend
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```

Health check:

```powershell
curl.exe http://127.0.0.1:8000/health
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Environment

`.env.example` contains every setting read by `app/config.py`. Do not commit real API keys.

Important modes:

- `RAG_MODE=fallback`: deterministic keyword retrieval, no embedding key required.
- `RAG_MODE=vector`: OpenAI-compatible embeddings plus local JSON VectorStore.

Generated reports are written to `backend/outputs/`. Uploaded files are written to `backend/data/uploads/`.

## Example Requests

Create a job:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/jobs `
  -H "Content-Type: application/json" `
  -d "{\"title\":\"AI Agent Intern\",\"company\":\"Demo\",\"description\":\"Requires Python, FastAPI, LLM API, RAG, and agent workflow experience.\"}"
```

Run the agent:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/agents/career/analyze `
  -H "Content-Type: application/json" `
  -d "{\"job_id\":1,\"user_goal\":\"I want to apply for an AI Agent internship.\"}"
```

Stream the agent:

```powershell
curl.exe "http://127.0.0.1:8000/api/agents/career/analyze/stream?job_id=1&user_goal=I%20want%20to%20apply%20for%20an%20AI%20Agent%20internship"
```

## Tests

```powershell
cd backend
python -m pytest
```

Baseline: 14 tests passing.
