# Interview Script

Use this short script to present the project.

## Opening

AI Career Agent is a full-stack AI agent workspace for students and job seekers. It accepts a job description and profile notes, retrieves relevant evidence, analyzes skill gaps, and generates a practical learning and project plan.

## Technical Walkthrough

The backend is FastAPI with SQLAlchemy and SQLite. The AI layer uses prompt files, an OpenAI-compatible LLM service, fallback retrieval, optional embeddings, and a lightweight tool-based agent workflow. The frontend is a Next.js workspace that shows job input, profile search, SSE step logs, content previews, and the final Markdown report.

## Why It Matters

Many AI demos stop at a chat response. This project demonstrates an inspectable workflow: inputs are persisted, evidence is retrieved, steps are streamed, outputs are structured, and tests cover the core paths.

## Close

The project is young, but it has a clear roadmap and maintainer workflow. Next steps are CI hardening, Docker, hybrid retrieval, user isolation, and better evaluation fixtures.
