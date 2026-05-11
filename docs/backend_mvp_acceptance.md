# Backend MVP Acceptance

## Scope

This document records the accepted backend MVP for AI Career Agent. The scope is limited to FastAPI backend functionality and excludes frontend, SSE streaming, Docker, authentication, and production vector search.

## Implemented Capabilities

- FastAPI app starts from `backend/`.
- `GET /health` returns `{"status":"ok"}`.
- Job records can be created and persisted in SQLite.
- Job descriptions can be analyzed through `JobAnalyzer`.
- `LLMService` supports OpenAI-compatible Chat Completions APIs with timeout and clear provider/network error messages.
- Missing placeholder LLM configuration falls back to deterministic local analysis.
- `.md` and `.txt` profile documents can be uploaded.
- Uploaded documents are saved under `backend/data/uploads/`.
- Document text is split into overlapping chunks.
- Fallback keyword retrieval returns relevant document chunks.
- CareerAgent runs the non-streaming end-to-end workflow.
- Markdown reports are saved under `backend/outputs/analysis_{analysis_id}.md`.
- pytest covers the core MVP path.

## API List

### `GET /health`

Health check.

Response:

```json
{"status":"ok"}
```

### `POST /api/jobs`

Create a job record.

Request:

```json
{
  "title": "AI Agent 实习生",
  "company": "Demo",
  "description": "需要 Python、FastAPI、LLM API、RAG 和 Agent 工作流经验。"
}
```

Response includes `id`, `title`, `company`, `description`, `created_at`, and `updated_at`.

### `POST /api/jobs/{job_id}/analyze`

Analyze a job description.

Response includes structured capability fields, `raw_markdown`, `llm_status`, and optional `llm_error`.

### `POST /api/documents/upload`

Upload `.md` or `.txt` profile material.

Multipart field:

```text
file=@data/samples/sample_profile.md
```

Response includes document metadata and `chunk_count`.

### `POST /api/documents/search`

Search uploaded profile chunks through fallback retrieval.

Request:

```json
{
  "query": "Python FastAPI RAG 项目经验",
  "top_k": 5
}
```

Response includes `results` with `document_id`, `chunk_id`, `content`, `score`, `source`, and `metadata`.

### `POST /api/agents/career/analyze`

Run the full non-streaming CareerAgent workflow.

Request:

```json
{
  "job_id": 1,
  "user_goal": "我想申请 AI Agent 实习岗位"
}
```

Response includes job analysis, profile evidence, gap analysis, learning plan, project plan, resume bullets, interview QA, Markdown report, report path, and step logs.

## Run Commands

Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```

Tests:

```powershell
cd backend
python -m pytest
```

## Configuration Check

The following variables are present in `.env.example` and read by `app/config.py`:

- `APP_ENV`
- `DATABASE_URL`
- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL`
- `LLM_TEMPERATURE`
- `EMBEDDING_API_KEY`
- `EMBEDDING_BASE_URL`
- `EMBEDDING_MODEL`
- `EMBEDDING_PROVIDER`
- `RAG_MODE`
- `VECTOR_STORE_TYPE`
- `VECTOR_STORE_DIR`
- `CHUNK_SIZE`
- `CHUNK_OVERLAP`
- `OUTPUT_DIR`
- `UPLOAD_DIR`
- `REQUEST_TIMEOUT_SECONDS`

Relative `DATABASE_URL`, `OUTPUT_DIR`, and `UPLOAD_DIR` values are resolved under `backend/` for stable Windows behavior.

## Test Coverage

Current tests:

- `tests/test_health.py`: FastAPI health endpoint.
- `tests/test_text_splitter.py`: chunking and overlap validation.
- `tests/test_job_analyzer.py`: fallback analysis and LLM failure metadata.
- `tests/test_vector_store.py`: fallback keyword retrieval.
- `tests/test_career_agent_workflow.py`: complete workflow and report generation.

## Known Limits

- No frontend UI.
- No SSE streaming.
- No Docker packaging.
- No real ChromaDB or FAISS integration yet.
- No Alembic migrations yet.
- No login, permission model, or multi-user data isolation.
- `.pdf` and `.docx` upload parsing is not implemented.
- The fallback retriever is keyword overlap, so semantic recall is limited.

## Next Phase Plan

- Add SSE endpoint for step-by-step CareerAgent progress.
- Add a small Next.js workbench for job creation, profile upload, retrieval testing, and analysis display.
- Replace fallback retrieval with ChromaDB or FAISS through the existing `VectorStore` interface.
- Add Dockerfile and docker-compose after the backend/frontend integration stabilizes.
- Add integration tests for API upload/search/agent flows with isolated temporary databases.
