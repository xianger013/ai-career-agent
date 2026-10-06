# Backend Acceptance Notes

The backend MVP is accepted when the following checks pass.

## Functional Checks

- `GET /health` returns `{"status":"ok"}`.
- A job can be created through `/api/jobs`.
- A `.md` or `.txt` profile can be uploaded.
- Profile chunks can be retrieved in fallback mode.
- CareerAgent can run end to end and persist a Markdown report.
- SSE streaming returns `step`, `content`, `final`, and `error` events where appropriate.

## Quality Checks

- Backend tests pass with `python -m pytest`.
- Provider failures are reported without leaking API keys.
- Fallback mode works without external credentials.
- Generated reports use English headings and content.

## Current Baseline

The current backend baseline is 15 passing pytest tests.
