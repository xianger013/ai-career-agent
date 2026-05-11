# Interview Q&A

## 1. 为什么选择 FastAPI？

FastAPI 适合这个项目，因为它开发效率高、类型提示友好、自动生成 OpenAPI 文档，并且和 Pydantic、异步 httpx 调用配合比较自然。这个项目重点是快速验证 AI Agent 后端链路，FastAPI 的工程成本比较合适。

## 2. 为什么选择 Next.js？

Next.js 能快速搭建 React + TypeScript 前端，并且适合作品集展示。当前项目只需要一个单页工作台，Next.js App Router 足够使用，后续如果要做服务端渲染或部署也有扩展空间。

## 3. CareerAgent 如何工作？

CareerAgent 是一个轻量编排器。它按固定步骤读取岗位、分析 JD、检索资料、分析差距、生成学习计划、项目方案、简历 bullet、面试问答，并保存 Markdown 报告。它不直接堆业务逻辑，而是调用 Tool 和 Service。

## 4. 你怎么设计 Prompt？

Prompt 没有硬编码在 Python 里，而是放在 `backend/app/prompts/`。这样便于版本管理和后续迭代。Prompt 的输出结构尽量固定，方便后续解析和报告组装。

## 5. RAG 在项目里起什么作用？

RAG 用来从用户上传的个人资料中检索证据。这样报告不是只根据岗位 JD 泛泛生成，而是能引用用户已有经历，降低编造个人经历的风险。

## 6. fallback search 和 vector search 区别是什么？

fallback search 基于关键词重合，不需要 embedding API，适合本地演示。vector search 会把文本转成 embedding，通过向量相似度做语义检索，对同义表达更友好，但需要 embedding 服务和向量存储。

## 7. 为什么当前使用 JSON VectorStore？

这是一个作品集 MVP，目标是先保证本地可复现。JSON VectorStore 依赖少、容易测试、方便解释，也保留了 VectorStore 接口，后续可以替换成 ChromaDB 或 FAISS。

## 8. 为什么没有直接上 ChromaDB？

ChromaDB 会增加安装和环境差异问题。当前阶段更重要的是证明 embedding、向量检索、证据引用和 Agent 报告链路。文档中也明确说明 ChromaDB/FAISS 只是后续替换方向。

## 9. SSE 是什么？为什么用 SSE？

SSE 是 Server-Sent Events，适合后端向前端单向推送事件。Agent 执行有多个阶段，用 SSE 可以让用户实时看到进度，比一直等待同步响应体验更好。

## 10. 当前 SSE 为什么不是 token 级？

当前 LLM 调用主要是阶段式结果，不依赖 token streaming。为了降低复杂度，先推送阶段开始、完成和内容片段。后续可以在 LLMService 支持 stream_chat 后转发 token。

## 11. 如果 LLM API 失败怎么办？

LLMService 会返回清晰错误信息，并对 API key 做脱敏。岗位分析在没有 key 或失败时会使用 fallback 分析，保证项目本地演示不被外部服务阻断。

## 12. 如果 embedding API 失败怎么办？

`RAG_MODE=vector` 下 embedding 失败会返回 `retrieval_mode=fallback_due_to_vector_error` 和 `retrieval_error`，并自动回退到 keyword search。

## 13. 如何避免 LLM 编造用户经历？

报告里的用户资料证据来自文档检索结果，展示 source、chunk_index、score 和摘要。Agent 生成时基于检索证据组织内容；如果没有检索到证据，报告明确写“未检索到足够个人资料证据”。

## 14. 如何保证报告里的证据来自上传资料？

上传文件会保存为 Document，切分后写入 DocumentChunk。检索结果会带上 document_id、filename、chunk_index 和 content，报告直接展示这些字段。

## 15. 这个项目如何扩展成多用户？

需要增加 User 表、认证、资料和岗位的 user_id 外键，并在所有查询中按用户过滤。向量库也要按用户隔离 collection 或 metadata filter。

## 16. 如何做权限和数据隔离？

后端 API 需要鉴权依赖，数据库表增加 owner 字段，上传文件按用户目录隔离，向量记录带 user_id metadata，检索时强制过滤 user_id。

## 17. 如何把 SQLite 换成 PostgreSQL？

SQLAlchemy 已经通过 `DATABASE_URL` 配置数据库连接。要切换 PostgreSQL，需要安装驱动、修改 `DATABASE_URL`，并引入 Alembic 管理迁移。

## 18. 如何把 JSON VectorStore 换成 ChromaDB/FAISS？

保留 VectorStore 的 `add_documents` 和 `search` 接口，新增 Chroma 或 FAISS 实现，上传时写入对应向量库，搜索时调用对应 index，再保持 API 响应结构不变。

## 19. 如何评估 RAG 效果？

需要构建 query、期望证据 chunk、期望答案的评测集。先评估 recall@k，再评估最终报告是否引用正确证据，必要时引入 reranker。

## 20. 这个项目和普通 ChatGPT 对话有什么区别？

普通对话主要依赖用户临时输入。这个项目有结构化岗位、上传资料、检索证据、Agent 流程、数据库持久化、SSE 进度和可下载报告，更接近一个可复用应用。

## 21. 你在这个项目里最大的工程收获是什么？

最大的收获是把 AI 能力拆成可维护工程模块，而不是只调用模型：API、Service、Tool、Agent、Prompt、RAG、SSE、测试和文档都需要边界清晰。

## 22. 这个项目当前最需要改进的地方是什么？

最需要改进的是检索质量和生产化能力。当前 JSON VectorStore 适合演示，但还需要 ChromaDB/FAISS、hybrid search、rerank、多用户隔离和端到端测试。

