from __future__ import annotations

from pathlib import Path

from sqlalchemy.orm import Session

from app.config import settings
from app.models.document import Document, DocumentChunk
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.utils.text_splitter import split_text


class DocumentService:
    def __init__(self, db: Session, embedding_service: EmbeddingService | None = None) -> None:
        self.db = db
        self.embedding_service = embedding_service or EmbeddingService()

    async def save_document(self, filename: str, content: bytes) -> tuple[Document, int]:
        safe_name = Path(filename).name
        suffix = Path(safe_name).suffix.lower()
        if suffix not in {".md", ".txt"}:
            raise ValueError("Only .md and .txt files are supported in the MVP.")

        text = content.decode("utf-8", errors="replace")
        settings.resolved_upload_dir.mkdir(parents=True, exist_ok=True)
        upload_path = settings.resolved_upload_dir / safe_name
        upload_path.write_bytes(content)

        document = Document(filename=safe_name, file_type=suffix.removeprefix("."), content_text=text)
        self.db.add(document)
        self.db.flush()

        chunks = split_text(text)
        embeddings = await self.embedding_service.embed_documents(chunks) if chunks else []
        for index, chunk in enumerate(chunks):
            embedding_id = f"{document.id}:{index}:{len(embeddings[index]) if embeddings else 0}"
            self.db.add(
                DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=chunk,
                    embedding_id=embedding_id,
                )
            )

        self.db.commit()
        self.db.refresh(document)
        return document, len(chunks)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        return VectorStore(self.db).search(query, top_k=top_k)

