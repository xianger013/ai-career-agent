# RAG Design

AI Career Agent uses a small, local-first retrieval design so the project can be demonstrated without paid infrastructure.

## Retrieval Modes

### Fallback Keyword Search

`RAG_MODE=fallback` splits uploaded `.md` and `.txt` files into chunks, scores them with simple keyword overlap, and returns the highest-scoring evidence. This mode is deterministic and works without API keys.

### Vector Search

`RAG_MODE=vector` calls an OpenAI-compatible embeddings endpoint and stores vectors in a local JSON VectorStore. This keeps the interface close to a production RAG system while staying easy to inspect.

## Data Flow

1. User uploads profile notes.
2. Backend stores the raw document.
3. Text splitter creates chunks.
4. Retrieval indexes chunks through fallback or vector mode.
5. CareerAgent builds a query from job-analysis skills and user goal.
6. Retrieved evidence is included in the final Markdown report.

## Why JSON VectorStore

JSON storage is not production infrastructure, but it is valuable for this repository because reviewers can inspect behavior without a database service. The current abstraction leaves room for ChromaDB, FAISS, pgvector, or another vector store.

## Current Limitations

- No hybrid search yet.
- No reranker.
- No embedding cache.
- No retrieval evaluation dataset.
- No tenant isolation or permissions model.

## Roadmap

The next retrieval improvements are hybrid search, reranking, retrieval-quality tests, and a production vector-store adapter.
