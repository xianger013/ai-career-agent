from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    file_type: str
    created_at: datetime


class DocumentUploadResponse(DocumentRead):
    document_id: int
    chunk_count: int
    retrieval_mode: str
    retrieval_error: str | None = None


class DocumentSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class DocumentSearchResult(BaseModel):
    document_id: int | None = None
    chunk_id: str
    content: str
    score: float
    source: str
    metadata: dict = Field(default_factory=dict)
    retrieval_mode: str = "fallback"


class DocumentSearchResponse(BaseModel):
    retrieval_mode: str
    retrieval_error: str | None = None
    results: list[DocumentSearchResult]
