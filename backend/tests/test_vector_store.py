from app.services.vector_store import VectorStore


def test_vector_store_keyword_search_returns_ranked_results() -> None:
    store = VectorStore()
    store.add_documents(
        [
            {
                "document_id": 1,
                "chunk_id": "1",
                "content": "Python FastAPI SQLite project with pytest",
                "source": "profile.md",
                "metadata": {},
            },
            {
                "document_id": 2,
                "chunk_id": "2",
                "content": "Marketing writing notes",
                "source": "notes.md",
                "metadata": {},
            },
        ]
    )

    results = store.search("Python FastAPI project", top_k=5)

    assert len(results) == 1
    assert results[0]["source"] == "profile.md"
    assert results[0]["score"] > 0

