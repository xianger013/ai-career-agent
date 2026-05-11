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
        document, chunk_count = await DocumentService(db).save_document(file.filename, await file.read())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "id": document.id,
        "filename": document.filename,
        "file_type": document.file_type,
        "created_at": document.created_at,
        "chunk_count": chunk_count,
    }


@router.post("/search", response_model=DocumentSearchResponse)
def search_documents(payload: DocumentSearchRequest, db: Session = Depends(get_db)) -> dict:
    results = DocumentService(db).search(payload.query, top_k=payload.top_k)
    return {"results": results}

