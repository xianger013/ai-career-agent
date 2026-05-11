from __future__ import annotations

import json
import logging
import math
import re
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.config import settings
from app.models.document import DocumentChunk


TOKEN_RE = re.compile(r"[a-zA-Z0-9_+#.-]+|[\u4e00-\u9fff]")
logger = logging.getLogger(__name__)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


@dataclass
class VectorSearchResult:
    content: str
    source: str
    score: float
    metadata: dict[str, Any]
    document_id: int | None = None
    chunk_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class VectorStore:
    """Fallback keyword store plus lightweight persisted vector store.

    The vector implementation intentionally avoids mandatory ChromaDB/FAISS
    runtime dependencies in this MVP. It persists embeddings as JSON and keeps
    the same surface needed to swap in ChromaDB later.
    """

    _warned_vector_store_type = False

    def __init__(self, db: Session | None = None, persist_dir: Path | None = None) -> None:
        self.db = db
        self.persist_dir = persist_dir or settings.resolved_vector_store_dir
        self.persist_file = self.persist_dir / "career_agent_documents.json"
        self._documents: list[dict[str, Any]] = []
        if settings.vector_store_type != "json" and not VectorStore._warned_vector_store_type:
            logger.warning(
                "VECTOR_STORE_TYPE=%s is not implemented in this version; using JSON VectorStore.",
                settings.vector_store_type,
            )
            VectorStore._warned_vector_store_type = True

    def add_documents(self, chunks: list[dict[str, Any]]) -> None:
        if any("embedding" in chunk for chunk in chunks):
            self._add_vector_documents(chunks)
            return
        self._documents.extend(chunks)

    def search(self, query: str | list[float], top_k: int = 5) -> list[dict[str, Any]]:
        if isinstance(query, list):
            return self._search_vectors(query, top_k=top_k)
        return self._search_keywords(query, top_k=top_k)

    def _add_vector_documents(self, chunks: list[dict[str, Any]]) -> None:
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        records = {record["id"]: record for record in self._load_vector_records()}
        for chunk in chunks:
            embedding = chunk.get("embedding")
            if not isinstance(embedding, list) or not embedding:
                raise ValueError("Vector document requires a non-empty embedding list.")

            metadata = dict(chunk.get("metadata", {}))
            chunk_id = str(chunk.get("chunk_id") or metadata.get("chunk_id") or "")
            record_id = str(chunk.get("id") or chunk_id)
            records[record_id] = {
                "id": record_id,
                "chunk_id": chunk_id,
                "document_id": chunk.get("document_id") or metadata.get("document_id"),
                "content": chunk["content"],
                "source": chunk.get("source") or metadata.get("filename") or "unknown",
                "metadata": metadata,
                "embedding": [float(value) for value in embedding],
            }

        ordered_records = [records[key] for key in sorted(records)]
        self.persist_file.write_text(json.dumps(ordered_records, ensure_ascii=False, indent=2), encoding="utf-8")

    def _search_vectors(self, query_embedding: list[float], top_k: int = 5) -> list[dict[str, Any]]:
        if not query_embedding:
            return []

        scored: list[VectorSearchResult] = []
        for record in self._load_vector_records():
            score = self._cosine_similarity(query_embedding, record["embedding"])
            if score <= 0:
                continue
            scored.append(
                VectorSearchResult(
                    document_id=record.get("document_id"),
                    chunk_id=str(record.get("chunk_id", record.get("id", ""))),
                    content=record["content"],
                    source=record.get("source", "unknown"),
                    score=round(score, 4),
                    metadata=record.get("metadata", {}),
                )
            )

        scored.sort(key=lambda item: item.score, reverse=True)
        return [item.to_dict() for item in scored[:top_k]]

    def _search_keywords(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        query_tokens = Counter(tokenize(query))
        if not query_tokens:
            return []

        scored: list[dict[str, Any]] = []
        for item in self._iter_keyword_documents():
            content_tokens = Counter(tokenize(item["content"]))
            score = self._keyword_score(query_tokens, content_tokens)
            if score <= 0:
                continue
            result = dict(item)
            result["score"] = round(score, 4)
            scored.append(result)

        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]

    def _iter_keyword_documents(self) -> Iterable[dict[str, Any]]:
        yield from self._documents
        if self.db is None:
            return

        rows = self.db.query(DocumentChunk).all()
        for chunk in rows:
            yield {
                "document_id": chunk.document_id,
                "chunk_id": str(chunk.id),
                "content": chunk.content,
                "source": chunk.document.filename if chunk.document else "unknown",
                "metadata": {
                    "document_id": chunk.document_id,
                    "filename": chunk.document.filename if chunk.document else "unknown",
                    "chunk_index": chunk.chunk_index,
                    "embedding_id": chunk.embedding_id,
                },
            }

    def _load_vector_records(self) -> list[dict[str, Any]]:
        if not self.persist_file.exists():
            return []
        try:
            data = json.loads(self.persist_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Vector store file is invalid JSON: {self.persist_file}") from exc
        if not isinstance(data, list):
            raise ValueError(f"Vector store file must contain a JSON list: {self.persist_file}")
        return data

    def _keyword_score(self, query_tokens: Counter, content_tokens: Counter) -> float:
        overlap = sum(min(weight, content_tokens[token]) for token, weight in query_tokens.items())
        if overlap == 0:
            return 0.0
        return overlap / math.sqrt(sum(query_tokens.values()) * max(sum(content_tokens.values()), 1))

    def _cosine_similarity(self, left: list[float], right: list[float]) -> float:
        if len(left) != len(right):
            return 0.0
        dot = sum(a * b for a, b in zip(left, right))
        left_norm = math.sqrt(sum(value * value for value in left))
        right_norm = math.sqrt(sum(value * value for value in right))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return dot / (left_norm * right_norm)
