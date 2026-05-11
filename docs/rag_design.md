# RAG Design

## 目标

Phase 4 将 AI Career Agent 的检索能力从纯 fallback keyword search 升级为可选的本地向量检索 RAG，同时保留默认 fallback 模式，确保没有 embedding key 的用户仍然可以完整演示。

## fallback keyword search 是什么

fallback keyword search 是当前默认检索模式。系统会把 query 和文档 chunk 切成 token，计算重叠度并返回 top-k 结果。

优点：

- 不依赖外部 embedding API。
- 不需要安装向量数据库。
- 本地演示稳定。

限制：

- 不能理解同义表达。
- 召回质量依赖关键词重合。
- 不适合作为生产级 RAG。

## vector RAG 是什么

vector RAG 会把文档 chunk 和 query 转成 embedding 向量，通过向量相似度检索最相关的资料证据。当前版本使用 OpenAI-compatible Embedding + 本地 JSON VectorStore，后续可替换为 ChromaDB/FAISS。

后续可以在不改 API 的情况下，把当前 `VectorStore` 替换为 ChromaDB 或 FAISS。

## 配置

默认模式：

```env
RAG_MODE=fallback
```

向量模式：

```env
RAG_MODE=vector
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_API_KEY=your_embedding_api_key_here
EMBEDDING_BASE_URL=https://api.openai.com/v1
EMBEDDING_MODEL=text-embedding-3-small
VECTOR_STORE_TYPE=json
VECTOR_STORE_DIR=./data/vector_store
CHUNK_SIZE=800
CHUNK_OVERLAP=120
```

说明：当前已实现的 `VECTOR_STORE_TYPE` 是 `json`。`chroma` / `faiss` 是未来可选值，当前版本尚未实现；如果用户配置 `VECTOR_STORE_TYPE=chroma` 或 `faiss`，系统会继续使用 JSON VectorStore 并输出 warning。

## 文档上传流程

`POST /api/documents/upload`：

1. 校验文件类型，仅支持 `.md` 和 `.txt`。
2. 保存原始文件到 `backend/data/uploads/`。
3. 写入 `Document`。
4. 使用 `split_text()` 按 `CHUNK_SIZE` 和 `CHUNK_OVERLAP` 切分。
5. 写入 `DocumentChunk`。
6. 如果 `RAG_MODE=fallback`，上传结束，返回 `retrieval_mode=fallback`。
7. 如果 `RAG_MODE=vector`，调用 `EmbeddingService` 生成 chunk embeddings。
8. 将 chunk、metadata 和 embedding 写入 `VectorStore`。
9. 返回 `retrieval_mode=vector`。
10. 如果 vector 写入失败，保留数据库文本 chunk，并返回 `retrieval_mode=fallback_due_to_vector_error`。

## 文本切分策略

默认：

```env
CHUNK_SIZE=800
CHUNK_OVERLAP=120
```

切分是字符级重叠切分，目标是让第一版 RAG 保持稳定和易理解。后续可以升级为基于标题、段落和 token 的结构化切分。

## Embedding 调用

`EmbeddingService` 使用 OpenAI-compatible embeddings API：

```http
POST {EMBEDDING_BASE_URL}/embeddings
```

请求字段：

- `model`
- `input`

工程处理：

- 使用 `httpx.AsyncClient`。
- 设置 timeout。
- 支持批量文本。
- 空文本返回清晰错误。
- HTTP、网络、超时、响应格式错误均转换为 `EmbeddingServiceError`。
- 错误信息会脱敏 API Key。

## Vector Store 存储

当前 JSON VectorStore 文件：

```text
backend/data/vector_store/career_agent_documents.json
```

每条记录包含：

- `id`
- `chunk_id`
- `document_id`
- `content`
- `source`
- `metadata`
- `embedding`

metadata 至少包含：

- `document_id`
- `filename`
- `chunk_index`
- `vector_id`

## Search 流程

`POST /api/documents/search`：

fallback 模式：

1. 使用 keyword search。
2. 返回 `retrieval_mode=fallback`。

vector 模式：

1. 对 query 调用 `EmbeddingService.embed_text()`。
2. 使用 `VectorStore.search(query_embedding)` 做 cosine similarity。
3. 返回 `retrieval_mode=vector`。

vector 失败：

1. 自动 fallback 到 keyword search。
2. 返回 `retrieval_mode=fallback_due_to_vector_error`。
3. 返回 `retrieval_error`，便于调试 key、网络或向量目录问题。

## Agent 如何使用证据

CareerAgent 的 `search_profile_evidence` 步骤会调用 `DocumentService.search()`。Markdown 报告中的“用户资料证据”会展示：

- 检索模式。
- filename。
- chunk_index。
- score。
- content 摘要。

如果没有检索到证据，报告明确写：

```text
未检索到足够个人资料证据
```

## 当前限制

- 当前向量存储是轻量 JSON 文件，不适合大规模数据。
- 没有多用户隔离。
- 没有 rerank。
- 没有 hybrid search。
- 没有 embedding cache 去重。
- 没有 token-aware chunking。

## 后续优化

- 将 JSON VectorStore 替换为 ChromaDB 或 FAISS。
- 增加 embedding cache。
- 增加 hybrid search：keyword + vector。
- 增加 reranker。
- 增加按用户隔离的 collection。
- 增加检索评测集，衡量 recall 和 answer groundedness。
