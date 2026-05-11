from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.orm import Session

from app.config import settings
from app.models.document import Document, DocumentChunk
from app.services.embedding_service import EmbeddingService, EmbeddingServiceError
from app.services.vector_store import VectorStore
from app.utils.text_splitter import split_text


@dataclass
class DocumentUploadResult:
    document: Document
    chunk_count: int
    retrieval_mode: str
    retrieval_error: str | None = None


@dataclass
class DocumentSearchResultSet:
    results: list[dict]
    retrieval_mode: str
    retrieval_error: str | None = None


class DocumentService:
    def __init__(
        self,
        db: Session,
        embedding_service: EmbeddingService | None = None,
        vector_store: VectorStore | None = None,
        rag_mode: str | None = None,
    ) -> None:
        self.db = db
        self.embedding_service = embedding_service or EmbeddingService()
        self.vector_store = vector_store or VectorStore(db)
        self.rag_mode = rag_mode or settings.rag_mode

    async def save_document(self, filename: str, content: bytes) -> DocumentUploadResult:
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

        raw_chunks = split_text(text, chunk_size=settings.chunk_size, overlap=settings.chunk_overlap)
        chunk_rows: list[DocumentChunk] = []
        for index, chunk in enumerate(raw_chunks):
            row = DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk,
                embedding_id=None,
            )
            self.db.add(row)
            chunk_rows.append(row)

        self.db.flush()
        retrieval_mode = "fallback"
        retrieval_error: str | None = None

        if self.rag_mode == "vector" and chunk_rows:
            try:
                embeddings = await self.embedding_service.embed_documents([chunk.content for chunk in chunk_rows])
                vector_documents = []
                for chunk, embedding in zip(chunk_rows, embeddings):
                    vector_id = f"document_{document.id}_chunk_{chunk.chunk_index}"
                    chunk.embedding_id = vector_id
                    vector_documents.append(
                        {
                            "id": vector_id,
                            "chunk_id": str(chunk.id),
                            "document_id": document.id,
                            "content": chunk.content,
                            "source": document.filename,
                            "embedding": embedding,
                            "metadata": {
                                "document_id": document.id,
                                "filename": document.filename,
                                "chunk_index": chunk.chunk_index,
                                "vector_id": vector_id,
                            },
                        }
                    )
                self.vector_store.add_documents(vector_documents)
                retrieval_mode = "vector"
            except (EmbeddingServiceError, ValueError) as exc:
                retrieval_mode = "fallback_due_to_vector_error"
                retrieval_error = str(exc)
        elif self.rag_mode != "fallback":
            retrieval_mode = "fallback_due_to_vector_error"
            retrieval_error = f"Unsupported RAG_MODE: {self.rag_mode}"

        self.db.commit()
        self.db.refresh(document)
        return DocumentUploadResult(
            document=document,
            chunk_count=len(chunk_rows),
            retrieval_mode=retrieval_mode,
            retrieval_error=retrieval_error,
        )

    async def search(self, query: str, top_k: int = 5) -> DocumentSearchResultSet:
        if self.rag_mode == "fallback":
            results = self._keyword_search(query, top_k, retrieval_mode="fallback")
            return DocumentSearchResultSet(results=results, retrieval_mode="fallback")

        if self.rag_mode != "vector":
            error = f"Unsupported RAG_MODE: {self.rag_mode}"
            results = self._keyword_search(query, top_k, retrieval_mode="fallback_due_to_vector_error")
            return DocumentSearchResultSet(
                results=results,
                retrieval_mode="fallback_due_to_vector_error",
                retrieval_error=error,
            )

        try:
            query_embedding = await self.embedding_service.embed_text(query)
            results = self.vector_store.search(query_embedding, top_k=top_k)
            for result in results:
                result["retrieval_mode"] = "vector"
            return DocumentSearchResultSet(results=results, retrieval_mode="vector")
        except (EmbeddingServiceError, ValueError) as exc:
            results = self._keyword_search(query, top_k, retrieval_mode="fallback_due_to_vector_error")
            return DocumentSearchResultSet(
                results=results,
                retrieval_mode="fallback_due_to_vector_error",
                retrieval_error=str(exc),
            )

    def _keyword_search(self, query: str, top_k: int, retrieval_mode: str) -> list[dict]:
        results = VectorStore(self.db).search(query, top_k=top_k)
        for result in results:
            result["retrieval_mode"] = retrieval_mode
        return results
