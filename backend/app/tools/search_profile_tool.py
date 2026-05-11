from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.document_service import DocumentService


class SearchProfileTool:
    name = "search_profile"
    description = "Search uploaded profile documents for evidence related to a query."
    input_schema = {"type": "object", "required": ["query"]}

    def __init__(self, db: Session) -> None:
        self.document_service = DocumentService(db)

    async def run(self, query: str, top_k: int = 5) -> list[dict]:
        return (await self.document_service.search(query, top_k=top_k)).results
