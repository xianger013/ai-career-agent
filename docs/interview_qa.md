# Interview Q&A

## How would you describe AI Career Agent?

AI Career Agent is a full-stack AI workflow that turns a job description and profile notes into skill-gap analysis, learning phases, project recommendations, resume bullets, and interview Q&A.

## Why does the project include fallback retrieval?

Fallback retrieval lets reviewers run the demo without paid API keys. It also creates deterministic behavior for tests. Vector retrieval remains available through an OpenAI-compatible embedding service.

## How is the backend organized?

Routes handle HTTP boundaries, services contain LLM and retrieval logic, tools wrap reusable agent capabilities, and the CareerAgent orchestrates the full workflow.

## How are prompts managed?

Prompts live in `backend/app/prompts`. The code reads prompt files and injects runtime inputs instead of hard-coding long prompt text inside service logic.

## What are the main production gaps?

The main gaps are authentication, multi-user data isolation, production vector storage, retrieval evaluation, hybrid search, Docker, and stronger observability.
