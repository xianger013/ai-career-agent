# Project Log

This log records the main implementation milestones.

## Milestones

- Created a FastAPI backend with health checks and SQLite persistence.
- Added job creation and structured job-analysis fallback logic.
- Added profile upload, text splitting, and fallback retrieval.
- Added OpenAI-compatible embedding support with JSON VectorStore.
- Added CareerAgent orchestration across job analysis, profile evidence, gap analysis, learning plan, project plan, resume bullets, interview Q&A, and report persistence.
- Added stage-level SSE streaming for frontend progress updates.
- Added a Next.js workspace for the end-to-end demo.
- Added English public documentation and OSS maintainer materials.

## Current Baseline

- Backend tests: 14 passing.
- Frontend build: passing.
- Public adoption metrics: 1 star, 0 forks, no package downloads.

## Next Milestones

- Docker Compose setup.
- Retrieval evaluation fixtures.
- Hybrid search and reranking.
- Auth and user data isolation.
- Contributor-friendly issue labels and release notes.
