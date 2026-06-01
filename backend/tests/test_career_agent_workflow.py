import asyncio

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.agents.career_agent import CareerAgent
from app.database import Base
from app.models.document import Document, DocumentChunk
from app.models.job import Job


def test_career_agent_workflow_generates_report(tmp_path) -> None:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)

    db = SessionLocal()
    job = Job(
        title="AI Agent Intern",
        company="Demo",
        description="Requires Python, FastAPI, LLM API, RAG, agent workflow, and testing experience.",
    )
    db.add(job)
    db.flush()
    document = Document(
        filename="profile.md",
        file_type="md",
        content_text="I built a Python FastAPI SQLite project and wrote pytest tests.",
    )
    db.add(document)
    db.flush()
    db.add(
        DocumentChunk(
            document_id=document.id,
            chunk_index=0,
            content=document.content_text,
            embedding_id="test:0",
        )
    )
    db.commit()
    db.refresh(job)

    result = asyncio.run(CareerAgent(db, output_dir=tmp_path).run(job.id, "Apply for an AI Agent internship"))

    assert result.analysis_id == 1
    assert result.markdown_report.startswith("# AI Career Agent Analysis Report")
    assert (tmp_path / "analysis_1.md").exists()
    assert [log.step for log in result.step_logs] == [
        "load_job",
        "analyze_job",
        "search_profile_evidence",
        "analyze_gap",
        "generate_learning_plan",
        "generate_project_plan",
        "generate_resume_bullets",
        "generate_interview_qa",
        "save_markdown_report",
        "persist_analysis",
    ]

    db.close()

