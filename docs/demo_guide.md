# Demo Guide

This guide describes the reviewer-facing local demo for AI Career Agent.

## Prerequisites

- Python 3.10 or newer.
- Node.js with npm.
- No API key is required for the fallback demo.

## Start The Backend

```powershell
cd backend
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to inspect the API.

## Start The Frontend

```powershell
cd frontend
npm ci
Copy-Item .env.example .env.local
npm run dev
```

Open `http://localhost:3000`.

## End-To-End Flow

1. Click `Fill sample job`.
2. Click `Create job`.
3. Upload `backend/data/samples/sample_profile.md`.
4. Click `Search profile`.
5. Click `Fill sample goal`.
6. Click `Run Career Agent`.
7. Inspect the step log, content preview, and final report.
8. Copy or download the Markdown report.

## Expected Result

The demo should produce an English Markdown report with:

- structured job analysis
- profile evidence
- skill matches and gaps
- learning phases
- recommended project plan
- resume bullets
- interview Q&A

The demo should work in fallback mode without external network calls.
