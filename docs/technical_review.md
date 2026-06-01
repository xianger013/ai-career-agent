# Technical Review

AI Career Agent is a compact reference implementation for an AI career-planning workflow. It is intentionally small enough to inspect but complete enough to demonstrate a real product loop.

## Strengths

- Clear FastAPI route, service, tool, and agent boundaries.
- Deterministic fallback behavior for demos without API keys.
- Prompt files live outside business logic.
- Agent workflow emits stage-level SSE events.
- Markdown reports preserve a durable output artifact.
- pytest covers the important backend paths.

## Engineering Tradeoffs

- SQLite and JSON VectorStore keep local setup simple, but they are not production-scale storage choices.
- Stage-level SSE is easier to reason about than token streaming, but it is less interactive.
- The frontend is a focused demo workspace rather than a full multi-user product.
- Fallback retrieval is transparent and deterministic, but it has weaker semantic recall than embeddings.

## Recommended Next Steps

- Add CI enforcement for backend tests and frontend build.
- Add Docker Compose for repeatable local demos.
- Add hybrid retrieval and a small retrieval-evaluation fixture.
- Add authentication and user data isolation before any hosted deployment.
- Add issue labels and release notes once external contributors appear.
