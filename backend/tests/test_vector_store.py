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


def test_vector_store_persists_and_searches_embeddings(tmp_path) -> None:
    store = VectorStore(persist_dir=tmp_path)
    store.add_documents(
        [
            {
                "id": "document_1_chunk_0",
                "document_id": 1,
                "chunk_id": "10",
                "content": "Python FastAPI vector note",
                "source": "profile.md",
                "embedding": [1.0, 0.0, 0.0],
                "metadata": {"document_id": 1, "filename": "profile.md", "chunk_index": 0},
            },
            {
                "id": "document_2_chunk_0",
                "document_id": 2,
                "chunk_id": "20",
                "content": "Marketing note",
                "source": "notes.md",
                "embedding": [0.0, 1.0, 0.0],
                "metadata": {"document_id": 2, "filename": "notes.md", "chunk_index": 0},
            },
        ]
    )

    reloaded = VectorStore(persist_dir=tmp_path)
    results = reloaded.search([0.9, 0.1, 0.0], top_k=1)

    assert len(results) == 1
    assert results[0]["document_id"] == 1
    assert results[0]["metadata"]["chunk_index"] == 0
