# Technical Review

## 为什么先做后端 MVP

AI Agent 项目的核心风险在于业务链路是否跑通，而不是界面是否好看。先做后端 MVP 可以优先验证岗位创建、LLM 调用、资料检索、Agent 编排、报告保存和测试覆盖，避免在前端细节上过早消耗时间。

## 为什么先用 fallback 检索

第一版目标是保证本地可复现。正式向量检索需要 embedding API、向量库依赖和更多调试成本。fallback 检索虽然语义能力有限，但足以验证文档上传、文本切分、证据召回和 Agent 使用证据的链路。代码通过 `VectorStore` 抽象保留了替换空间。

## 为什么使用阶段式 SSE

token 级流式依赖 LLM provider 的 streaming 能力，也会增加前后端处理复杂度。阶段式 SSE 更适合当前 MVP：它能展示 Agent 进度，解释系统正在做什么，同时保持实现简单、稳定、易测试。

## 为什么暂时不做登录、多用户、Docker、复杂 RAG

这些能力都重要，但不是当前作品集 MVP 的最短路径。登录和多用户会引入权限、数据隔离和会话模型；Docker 会引入部署维护；复杂 RAG 会引入向量库和评测问题。当前阶段更适合先证明端到端 AI Agent 工程能力，再逐步扩展。

## 覆盖的岗位能力

- LLM API 调用和错误处理。
- Prompt Engineering 和 Prompt 文件化管理。
- RAG 基础链路：上传、切分、召回、证据引用。
- Agent workflow 编排。
- Tool Calling 架构抽象。
- FastAPI 后端 API 设计。
- SQLAlchemy 数据持久化。
- SSE 单向流式进度推送。
- Next.js + React + TypeScript 前端集成。
- Tailwind CSS 基础工程化 UI。
- pytest 自动化测试。
- README、demo guide、resume packaging 等作品集文档。

## 下一阶段技术路线

- 接入 ChromaDB 或 FAISS 替换 fallback 检索。
- 增加真实 embedding 接口和向量库持久化。
- 增加 token 级 LLM streaming。
- 增加报告导出 PDF 或服务端下载 API。
- 增加前端端到端测试。
- 增加 Docker 和部署说明。
- 在引入登录前先设计清楚用户、资料、岗位和分析记录的数据隔离边界。

