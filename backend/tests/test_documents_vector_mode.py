import asyncio

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.services.document_service import DocumentService
from app.services.vector_store import VectorStore


class MockEmbeddingService:
    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[1.0, 0.0, 0.0] if "Python" in text else [0.0, 1.0, 0.0] for text in texts]

    async def embed_text(self, text: str) -> list[float]:
        return [1.0, 0.0, 0.0]


def test_document_service_vector_mode_upload_and_search(tmp_path) -> None:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    vector_store = VectorStore(db, persist_dir=tmp_path)
    service = DocumentService(
        db,
        embedding_service=MockEmbeddingService(),
        vector_store=vector_store,
        rag_mode="vector",
    )

    upload = asyncio.run(service.save_document("profile.md", b"Python FastAPI RAG project notes"))
    search = asyncio.run(service.search("Python FastAPI", top_k=3))

    assert upload.retrieval_mode == "vector"
    assert upload.chunk_count == 1
    assert search.retrieval_mode == "vector"
    assert search.results[0]["retrieval_mode"] == "vector"
    assert search.results[0]["source"] == "profile.md"

    db.close()
