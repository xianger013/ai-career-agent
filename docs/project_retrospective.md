# Project Retrospective

AI Career Agent started as a portfolio-grade full-stack AI agent project. The core decision was to make the system useful even without paid model access, then leave clean extension points for production-grade AI infrastructure.

## What Worked

- The route/service/tool/agent split keeps responsibilities readable.
- Fallback retrieval makes local demos reliable.
- Prompt files make the LLM layer easier to review.
- SSE step events make the workflow visible to users.
- Markdown reports create a concrete artifact that can be inspected, copied, and downloaded.

## What Needs More Work

- Retrieval quality needs evaluation fixtures.
- Vector storage needs a production adapter.
- The app needs authentication before any hosted multi-user use.
- Docker would reduce setup friction.
- More contributor documentation will help future maintainers.

## Maintainer Notes

This repository is young and transparent about its current adoption. The near-term goal is to turn it into a strong open-source reference for job-search agents and career-planning workflows.
