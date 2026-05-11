from __future__ import annotations

import math
import re
from collections import Counter
from collections.abc import Iterable

from sqlalchemy.orm import Session

from app.models.document import DocumentChunk


TOKEN_RE = re.compile(r"[a-zA-Z0-9_+#.-]+|[\u4e00-\u9fff]")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


class VectorStore:
    """Keyword fallback store with the same add/search surface as a vector DB."""

    def __init__(self, db: Session | None = None) -> None:
        self.db = db
        self._documents: list[dict] = []

    def add_documents(self, chunks: list[dict]) -> None:
        self._documents.extend(chunks)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        query_tokens = Counter(tokenize(query))
        if not query_tokens:
            return []

        scored: list[dict] = []
        for item in self._iter_documents():
            content_tokens = Counter(tokenize(item["content"]))
            score = self._score(query_tokens, content_tokens)
            if score <= 0:
                continue
            result = dict(item)
            result["score"] = round(score, 4)
            scored.append(result)

        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]

    def _iter_documents(self) -> Iterable[dict]:
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
                    "chunk_index": chunk.chunk_index,
                    "embedding_id": chunk.embedding_id,
                },
            }

    def _score(self, query_tokens: Counter, content_tokens: Counter) -> float:
        overlap = sum(min(weight, content_tokens[token]) for token, weight in query_tokens.items())
        if overlap == 0:
            return 0.0
        return overlap / math.sqrt(sum(query_tokens.values()) * max(sum(content_tokens.values()), 1))

