from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.agents.career_agent import CareerAgent
from app.dependencies import get_db
from app.schemas.analysis import CareerAnalyzeRequest, CareerAnalyzeResponse
from app.utils.sse import format_sse


router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.post("/career/analyze", response_model=CareerAnalyzeResponse)
async def run_career_agent(payload: CareerAnalyzeRequest, db: Session = Depends(get_db)):
    try:
        return await CareerAgent(db).run(payload.job_id, payload.user_goal)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/career/analyze/stream")
async def stream_career_agent(
    job_id: int = Query(..., ge=1),
    user_goal: str = Query(default="I want to analyze skill gaps and generate a learning plan."),
    db: Session = Depends(get_db),
) -> StreamingResponse:
    async def event_generator():
        async for item in CareerAgent(db).run_stream(job_id, user_goal):
            yield format_sse(item["event"], item["data"])

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
