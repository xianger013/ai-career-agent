from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.job import Job
from app.schemas.job import JobAnalysisResponse, JobCreate, JobRead
from app.services.job_analyzer import JobAnalyzer


router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate, db: Session = Depends(get_db)) -> Job:
    job = Job(title=payload.title, company=payload.company, description=payload.description)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.post("/{job_id}/analyze", response_model=JobAnalysisResponse)
async def analyze_job(job_id: int, db: Session = Depends(get_db)) -> dict:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found.")
    return await JobAnalyzer().analyze(job)

