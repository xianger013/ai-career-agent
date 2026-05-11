# Project Log

## Phase 1 后端 MVP

完成内容：

- 搭建 FastAPI 后端项目结构。
- 实现 `/health`。
- 实现岗位创建、岗位分析、资料上传、资料检索、CareerAgent 非流式分析接口。
- 实现 SQLAlchemy + SQLite 持久化。
- 实现 LLMService 和 Prompt 文件化。
- 实现 fallback 检索、Tool 层和 Markdown 报告保存。
- 增加基础 pytest。

技术点：

- FastAPI 路由分层。
- SQLAlchemy ORM。
- Pydantic v2 schema。
- OpenAI-compatible Chat Completions 封装。
- Agent workflow 编排。
- fallback RAG 检索。

验收结果：

- 后端可启动。
- 核心接口可用。
- `outputs/analysis_{analysis_id}.md` 可生成。
- pytest 通过。

已知限制：

- 无前端。
- 无 SSE。
- 无 Docker。
- 检索不是正式向量数据库。

## Phase 1.5 后端质量审查

完成内容：

- 核对 README 启动命令。
- 核对 `.env.example`、`config.py`、`LLMService` 配置一致性。
- 改善 Windows 下相对路径解析。
- 增加 LLM 错误状态和错误信息返回。
- 增加 `docs/backend_mvp_acceptance.md`。

技术点：

- Windows 路径稳定性。
- 外部 API 错误处理和脱敏。
- 文档化 API 请求和响应。

验收结果：

- 后端测试通过。
- 未发现真实 API Key 泄露。

已知限制：

- 仍未加入 Alembic。
- API 集成测试还可以继续增加。

## Phase 2 SSE + 前端工作台

完成内容：

- 新增 `GET /api/agents/career/analyze/stream`。
- CareerAgent 增加 `run_stream()`。
- 新增 `app/utils/sse.py`。
- 新增 Next.js + React + TypeScript + Tailwind 单页工作台。
- 前端支持创建岗位、上传资料、检索资料、运行 Agent、查看步骤日志和 Markdown 原文。

技术点：

- Server-Sent Events。
- EventSource 客户端。
- Next.js App Router。
- Tailwind 卡片式布局。

验收结果：

- 后端 pytest 通过。
- 前端 `npm run build` 通过。

已知限制：

- SSE 是阶段式，不是 token 级。
- Markdown 仍是原文展示。
- 前端无复杂状态管理和自动化测试。

## Phase 3 演示体验强化

完成内容：

- 使用 `react-markdown` 渲染最终报告。
- 增加“复制 Markdown”和“下载 Markdown 报告”。
- 增加“填充示例岗位”和“填充示例目标”。
- 优化 Agent 步骤列表状态展示。
- 增加基础错误提示。
- 补充 demo、项目日志、简历包装、技术复盘文档。
- 增强根目录 README。

技术点：

- Markdown 渲染。
- 浏览器 Blob 下载。
- 演示流程文档化。
- 作品集表达和面试讲解整理。

验收结果：

- 后端测试继续通过。
- 前端 build 通过。

已知限制：

- Markdown 渲染未做复杂主题和目录。
- 下载只在浏览器端生成，不同步后端文件。
- 仍未做登录、多用户、Docker 和正式向量库。

