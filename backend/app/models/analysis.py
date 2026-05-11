from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False, index=True)
    job_analysis_json: Mapped[str] = mapped_column(Text, nullable=False)
    profile_evidence_json: Mapped[str] = mapped_column(Text, nullable=False)
    gap_analysis_json: Mapped[str] = mapped_column(Text, nullable=False)
    learning_plan_json: Mapped[str] = mapped_column(Text, nullable=False)
    project_plan_json: Mapped[str] = mapped_column(Text, nullable=False)
    resume_bullets_json: Mapped[str] = mapped_column(Text, nullable=False)
    interview_qa_json: Mapped[str] = mapped_column(Text, nullable=False)
    markdown_report: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    job = relationship("Job", back_populates="analyses")

