# AI Career Agent Frontend

Minimal Next.js + React + TypeScript + Tailwind workbench for the AI Career Agent backend.

## Start

```powershell
cd frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

Open:

```text
http://localhost:3000
```

## Environment

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

The backend must be running before using the workbench.

## Demo Flow

1. Create a job from the job input card.
2. Upload a `.md` or `.txt` profile document.
3. Run a retrieval test query.
4. Run Career Agent.
5. Watch the SSE step log.
6. Copy the final Markdown report.

## Known Limits

- Markdown is displayed as raw text in a `pre` block.
- SSE is stage-level streaming, not token-level streaming.
- Current retrieval is fallback keyword search, not a production vector database.
- There is no login or multi-user system.

