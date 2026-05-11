from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.document import (
    DocumentSearchRequest,
    DocumentSearchResponse,
    DocumentUploadResponse,
)
from app.services.document_service import DocumentService


router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a filename.")
    try:
        result = await DocumentService(db).save_document(file.filename, await file.read())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    document = result.document
    return {
        "id": document.id,
        "document_id": document.id,
        "filename": document.filename,
        "file_type": document.file_type,
        "created_at": document.created_at,
        "chunk_count": result.chunk_count,
        "retrieval_mode": result.retrieval_mode,
        "retrieval_error": result.retrieval_error,
    }


@router.post("/search", response_model=DocumentSearchResponse)
async def search_documents(payload: DocumentSearchRequest, db: Session = Depends(get_db)) -> dict:
    result_set = await DocumentService(db).search(payload.query, top_k=payload.top_k)
    return {
        "retrieval_mode": result_set.retrieval_mode,
        "retrieval_error": result_set.retrieval_error,
        "results": result_set.results,
    }
