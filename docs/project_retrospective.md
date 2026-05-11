# Project Retrospective

## 1. 项目起点

这个项目从 AI Agent / 大模型应用相关岗位要求出发。很多岗位会要求 LLM API、Prompt Engineering、RAG、Agent 工作流、后端 API、前端展示、测试和文档。AI Career Agent 的目标是把这些能力整合成一个可以本地演示、可以写进简历、也能在面试中讲清楚的作品集项目。

## 2. 阶段推进

Phase 1：后端 MVP。先实现 FastAPI、数据库模型、岗位创建、资料上传、fallback 检索、CareerAgent 和 Markdown 报告，保证核心链路能跑通。

Phase 1.5：后端质量审查。修复 README、配置一致性、Windows 路径、LLM 错误信息和验收文档。

Phase 2：SSE + 前端工作台。增加阶段式流式接口和 Next.js 单页工作台，让项目可以完整演示。

Phase 3：演示体验强化。增加 Markdown 渲染、复制、下载、示例填充、演示指南和作品集包装文档。

Phase 4：RAG 升级。保留 fallback，新增 OpenAI-compatible Embedding + JSON VectorStore 向量检索，并标注 retrieval_mode。

Phase 5：发布包装。整理 GitHub README、截图说明、简历最终表述、面试讲解稿、技术问答、项目复盘和发布清单。

## 3. 关键工程决策

- 先做后端 MVP：优先验证业务闭环，而不是先做 UI。
- 再做 SSE 和前端：核心 API 稳定后，再补演示体验。
- 再做展示体验：让项目从“能跑”变成“能讲、能截图、能写简历”。
- 再做 RAG：先有 fallback 作为安全网，再加入 vector mode。
- 选择 JSON VectorStore：减少本地安装复杂度，先证明向量检索链路。
- 保留 fallback：没有 embedding key 或外部 API 失败时，项目仍可完整演示。

## 4. 学到的工程能力

- API 设计：保持接口稳定，同时增量增加字段。
- 前后端联调：从 REST API 到 SSE 事件流。
- Agent 工作流：把复杂任务拆成可追踪步骤。
- Prompt 设计：Prompt 文件化，避免硬编码。
- RAG 检索：理解 fallback、embedding、vector search 的边界。
- SSE：用轻量单向事件流提升长任务体验。
- 测试：用 pytest 覆盖核心链路，降低迭代风险。
- 文档：把启动、演示、限制、简历和面试材料整理完整。
- 项目验收：每个阶段都有明确可验证结果。

## 5. 仍然不足

- 没有正式向量数据库。
- 没有 hybrid search 和 reranker。
- 没有登录、多用户和权限系统。
- 没有 Docker。
- 没有端到端自动化测试。
- 没有 PDF / DOCX 深度解析。
- 没有线上部署地址。

## 6. 下一步路线

1. 接入 ChromaDB 或 FAISS，替换 JSON VectorStore。
2. 增加 hybrid search 和 reranker。
3. 增加 Playwright 端到端演示测试。
4. 增加 Docker 和部署说明。
5. 设计多用户数据隔离。
6. 增加 PDF / DOCX 解析。
7. 增加 RAG 评测集。

