# Interview Script

## 1. 30 秒项目介绍

AI Career Agent 是一个面向大学生求职的 AI Agent 工作台。用户输入岗位 JD 并上传个人资料后，系统会分析岗位能力要求，检索用户资料证据，生成能力差距、学习路线、项目建议、简历描述和面试问答。技术上使用 FastAPI、Next.js、LLM API、RAG、SSE 和 Agent 工作流，重点展示端到端 AI 应用工程能力。

## 2. 2 分钟项目介绍

我做这个项目是因为很多学生看到岗位 JD 后，不知道自己和岗位要求之间差什么，也不知道怎么把学习内容转化成简历项目。

项目的核心流程是：先创建岗位 JD，再上传个人资料或项目笔记。后端通过岗位分析服务提取能力要求，再通过文档检索找到用户资料中的证据。CareerAgent 会按步骤完成差距分析、学习路线、项目方案、简历 bullet 和面试问答，最后生成 Markdown 报告。前端是一个 Next.js 工作台，可以创建岗位、上传资料、查看检索结果、通过 SSE 查看 Agent 运行过程，并渲染和下载报告。

技术架构上，后端使用 FastAPI、Pydantic、SQLAlchemy 和 SQLite；LLMService 和 EmbeddingService 兼容 OpenAI 风格接口；检索层支持 fallback keyword search 和 Embedding + JSON VectorStore；Agent 层负责流程编排；前端使用 React、TypeScript、Tailwind CSS 和 react-markdown。当前项目可以本地完整演示，也诚实保留了一些限制，比如没有正式向量数据库、多用户和 Docker。

## 3. 技术架构讲解

- 前端：Next.js 单页工作台，负责岗位输入、资料上传、检索测试、Agent 运行、步骤日志和报告展示。
- 后端：FastAPI 提供 REST API 和 SSE 接口，API 层只处理请求响应。
- LLMService：封装 OpenAI-compatible Chat Completions API，处理超时、HTTP 错误和网络错误。
- EmbeddingService：封装 OpenAI-compatible Embeddings API，支持批量 embedding 和错误脱敏。
- Document Search：根据 `RAG_MODE` 选择 fallback keyword search 或 vector search。
- CareerAgent：编排岗位分析、资料检索、差距分析、计划生成、报告保存等步骤。
- SSE：通过 `EventSource` 将 Agent 阶段状态推送给前端。
- Markdown Report：后端生成报告，前端渲染并支持复制、下载。

## 4. Agent 工作流讲解

- `load_job`：从数据库读取岗位信息。
- `analyze_job`：分析岗位 JD，提取能力要求。
- `search_profile_evidence`：检索用户上传资料中的相关证据。
- `analyze_gap`：比较岗位要求和用户证据，判断已具备、部分具备和缺失能力。
- `generate_learning_plan`：生成阶段化学习路线。
- `generate_project_plan`：生成补齐差距的项目方案。
- `generate_resume_bullets`：生成可写入简历的项目描述。
- `generate_interview_qa`：生成面试问答准备材料。
- `save_markdown_report`：组装 Markdown 报告。
- `persist_analysis`：保存分析记录并写入报告文件。

## 5. RAG 讲解

fallback keyword search 是默认模式，不需要 embedding key，通过关键词重叠做本地检索。vector mode 会调用 EmbeddingService，把文档 chunk 和 query 转成向量，再用 JSON VectorStore 做 cosine similarity。

我保留 fallback 是为了保证没有外部 API key 的情况下也能完整演示。当前 JSON VectorStore 适合小规模本地作品集，不适合生产环境。后续可以把 VectorStore 替换成 ChromaDB 或 FAISS，并加入 hybrid search 和 reranker。

## 6. SSE 讲解

如果使用普通同步等待，用户只能在最后看到结果，不知道 Agent 运行到了哪一步。SSE 更适合这种后端向前端单向推送进度的场景，比 WebSocket 更轻量。

当前 SSE 是阶段式流式：每个阶段开始、完成和部分内容会推送事件。未来如果接入 LLM token streaming，可以把 LLMService 的 token 输出也转发给前端，实现 token 级流式。

## 7. 项目不足

- 没有正式向量数据库。
- 没有 hybrid search。
- 没有 reranker。
- 没有多用户系统。
- 没有权限系统。
- 没有 Docker。
- 缺少端到端测试。

## 8. 下一步优化

- 接入 ChromaDB/FAISS。
- 增加 hybrid search。
- 增加 rerank。
- 增加 Docker 部署。
- 增加 Playwright 端到端测试。
- 增加多用户数据隔离。
- 部署到云端并补充线上演示地址。

