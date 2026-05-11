from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10)


class JobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    company: str
    description: str
    created_at: datetime
    updated_at: datetime


class JobAnalysisResponse(BaseModel):
    job_id: int
    llm_status: str
    llm_error: str | None = None
    role_type: str
    core_responsibilities: list[str]
    required_skills: list[str]
    bonus_skills: list[str]
    engineering_skills: list[str]
    ai_skills: list[str]
    product_skills: list[str]
    suggested_projects: list[str]
    raw_markdown: str
