from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.vector_store import VectorStore


class SearchProfileTool:
    name = "search_profile"
    description = "Search uploaded profile documents for evidence related to a query."
    input_schema = {"type": "object", "required": ["query"]}

    def __init__(self, db: Session) -> None:
        self.vector_store = VectorStore(db)

    async def run(self, query: str, top_k: int = 5) -> list[dict]:
        return self.vector_store.search(query, top_k=top_k)

