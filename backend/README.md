# AI Career Agent Backend MVP

## Project Overview

AI Career Agent is a backend MVP for students and job seekers. It can create job records, analyze a job description, upload profile notes, retrieve profile evidence with a simple fallback search, run a lightweight CareerAgent workflow, and save a Markdown analysis report.

This MVP intentionally does not include frontend, SSE, Docker, authentication, or a production vector database.

## Features

- FastAPI backend with `/health`.
- SQLite persistence through SQLAlchemy.
- OpenAI-compatible `LLMService` with explicit timeout and provider error handling.
- Prompt files stored under `app/prompts/`.
- `.md` and `.txt` profile upload.
- Text splitting and keyword fallback retrieval.
- Tool layer for controlled, extensible tool calling.
- Non-streaming CareerAgent workflow.
- Markdown report saved to `outputs/analysis_{analysis_id}.md`.
- pytest coverage for core MVP paths.

## Tech Stack

Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy, SQLite, python-dotenv, httpx, pytest.

## Project Structure

```text
app/api          API route layer
app/models       SQLAlchemy models
app/schemas      Pydantic request/response schemas
app/services     LLM, retrieval, analysis, and generation logic
app/tools        Tool-calling abstractions
app/agents       CareerAgent workflow orchestration
app/prompts      Prompt files
app/utils        Text splitting and Markdown report helpers
data/samples     Sample input files
data/uploads     Uploaded local files
outputs          Generated Markdown reports
tests            pytest tests
```

## Quick Start

On Windows, prefer `python -m ...` commands so the active interpreter is used consistently.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```

If PowerShell blocks script activation, use:

```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```

Health check:

```powershell
curl.exe http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## Environment Variables

`.env.example` contains every setting read by `app/config.py`.

```env
APP_ENV=development
DATABASE_URL=sqlite:///./career_agent.db

LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.2

EMBEDDING_API_KEY=your_embedding_api_key_here
EMBEDDING_BASE_URL=https://api.openai.com/v1
EMBEDDING_MODEL=text-embedding-3-small

VECTOR_STORE_TYPE=fallback
OUTPUT_DIR=./outputs
UPLOAD_DIR=./data/uploads
REQUEST_TIMEOUT_SECONDS=30
```

Do not put real API keys in `.env.example`, README, docs, tests, or committed sample files. Use a local untracked `.env` file for secrets.

## Path Behavior On Windows

- Relative `OUTPUT_DIR` and `UPLOAD_DIR` are resolved under the `backend/` directory.
- Relative SQLite paths such as `sqlite:///./career_agent.db` are also resolved under `backend/`, even if the app is launched from another working directory.
- Generated reports are written to `backend/outputs/`.
- Uploaded files are written to `backend/data/uploads/`.

## LLM And Fallback Behavior

If `LLM_API_KEY` is missing or still set to `your_api_key_here`, the MVP uses deterministic local heuristic analysis so the workflow can run without paid external services.

If an LLM key is configured but the provider request fails, the job analysis response includes:

```json
{
  "llm_status": "fallback_after_llm_error",
  "llm_error": "LLM provider returned HTTP 401: ..."
}
```

Error messages are truncated and the configured API key is redacted if it appears in provider output.

## Retrieval Behavior

Current retrieval is not a production vector search. `VectorStore` keeps the same `add_documents()` and `search()` interface expected from a vector database, but the implementation uses keyword token overlap for the MVP. This makes the backend easy to run locally and leaves a clean seam for replacing it with ChromaDB or FAISS later.

## API Examples

### GET `/health`

```powershell
curl.exe http://localhost:8000/health
```

Response:

```json
{"status":"ok"}
```

### POST `/api/jobs`

```powershell
curl.exe -X POST http://localhost:8000/api/jobs `
  -H "Content-Type: application/json" `
  -d "{\"title\":\"AI Agent 实习生\",\"company\":\"Demo\",\"description\":\"需要 Python、FastAPI、LLM API、RAG 和 Agent 工作流经验。\"}"
```

Response shape:

```json
{
  "id": 1,
  "title": "AI Agent 实习生",
  "company": "Demo",
  "description": "需要 Python、FastAPI、LLM API、RAG 和 Agent 工作流经验。",
  "created_at": "2026-05-11T21:30:00",
  "updated_at": "2026-05-11T21:30:00"
}
```

### POST `/api/jobs/{job_id}/analyze`

```powershell
curl.exe -X POST http://localhost:8000/api/jobs/1/analyze
```

Response shape:

```json
{
  "job_id": 1,
  "llm_status": "fallback_no_llm_config",
  "llm_error": null,
  "role_type": "AI Agent 实习生",
  "core_responsibilities": ["拆解岗位 JD 中的能力要求"],
  "required_skills": ["Python", "FastAPI", "LLM API", "RAG", "Agent Workflow"],
  "bonus_skills": ["部署经验", "自动化测试", "产品化表达"],
  "engineering_skills": ["Python", "FastAPI"],
  "ai_skills": ["LLM API", "RAG", "Agent Workflow"],
  "product_skills": ["需求拆解", "结果结构化展示", "用户目标对齐"],
  "suggested_projects": ["AI Career Agent 求职能力分析系统"],
  "raw_markdown": "# 岗位分析结果..."
}
```

### POST `/api/documents/upload`

```powershell
curl.exe -X POST http://localhost:8000/api/documents/upload `
  -F "file=@data/samples/sample_profile.md"
```

Response shape:

```json
{
  "id": 1,
  "filename": "sample_profile.md",
  "file_type": "md",
  "created_at": "2026-05-11T21:31:00",
  "chunk_count": 1
}
```

### POST `/api/documents/search`

```powershell
curl.exe -X POST http://localhost:8000/api/documents/search `
  -H "Content-Type: application/json" `
  -d "{\"query\":\"Python FastAPI RAG 项目经验\",\"top_k\":5}"
```

Response shape:

```json
{
  "results": [
    {
      "document_id": 1,
      "chunk_id": "1",
      "content": "我使用 Python 和 FastAPI 做过一个课程项目...",
      "score": 0.42,
      "source": "sample_profile.md",
      "metadata": {"chunk_index": 0, "embedding_id": "1:0:64"}
    }
  ]
}
```

### POST `/api/agents/career/analyze`

```powershell
curl.exe -X POST http://localhost:8000/api/agents/career/analyze `
  -H "Content-Type: application/json" `
  -d "{\"job_id\":1,\"user_goal\":\"我想申请 AI Agent 实习岗位\"}"
```

Response shape:

```json
{
  "analysis_id": 1,
  "job_analysis": {},
  "profile_evidence": [],
  "gap_analysis": {},
  "learning_plan": {},
  "project_plan": {},
  "resume_bullets": [],
  "interview_qa": [],
  "markdown_report": "# AI Career Agent 分析报告...",
  "report_path": "D:\\xianger\\Codex\\backend\\outputs\\analysis_1.md",
  "step_logs": [
    {"step": "load_job", "status": "done", "summary": "已加载岗位 AI Agent 实习生"}
  ]
}
```

### GET `/api/agents/career/analyze/stream`

Stage-level SSE version of the CareerAgent workflow.

```powershell
curl.exe -N "http://localhost:8000/api/agents/career/analyze/stream?job_id=1&user_goal=我想申请 AI Agent 实习岗位"
```

Event examples:

```text
event: step
data: {"name":"load_job","status":"running","message":"正在读取岗位信息"}

event: content
data: {"section":"job_analysis","content":"# 岗位分析结果..."}

event: final
data: {"analysis_id":1,"markdown_report":"# AI Career Agent 分析报告..."}
```

## Tests

```powershell
cd backend
python -m pytest
```

Current coverage includes health check, text splitting, job analyzer fallback, fallback retrieval, and full CareerAgent workflow.

## Known Limits

- No frontend.
- No Docker packaging.
- No authentication or multi-user isolation.
- `.pdf` and `.docx` parsing are not implemented.
- Retrieval is keyword fallback, not ChromaDB or FAISS.
- Alembic migrations are not added yet; schema is created via SQLAlchemy metadata during startup.

## Next Steps

- Add SSE step streaming.
- Add Next.js workbench.
- Replace fallback retrieval with ChromaDB or FAISS behind the existing `VectorStore` interface.
- Add Docker and deployment docs.
- Add more integration tests and fixture data.
