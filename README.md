# AI Career Agent

AI Career Agent 是一个面向大学生求职的全栈 AI Agent 作品集项目。它支持岗位 JD 创建、个人资料上传、fallback RAG 检索、Agent 工作流分析、SSE 阶段式流式反馈、Markdown 报告渲染、复制和下载。

## 当前能力覆盖

- LLM API：封装 OpenAI-compatible Chat Completions 调用，并提供清晰错误处理。
- Prompt Engineering：Prompt 放在后端 `app/prompts/`，避免硬编码在业务逻辑里。
- Agent workflow：CareerAgent 编排岗位分析、资料检索、差距分析、学习路线、项目建议、简历描述和面试问答。
- fallback RAG：支持资料上传、文本切分、关键词 fallback 检索和证据引用。
- FastAPI：后端 API、Pydantic schema、SQLAlchemy、SQLite。
- SSE：通过 EventSource 展示阶段式运行进度。
- Next.js：单页工作台完成完整演示链路。
- Markdown report：最终报告支持渲染、复制和下载。

## 项目截图占位

### 首页截图

> 放置 `AI Career Agent 工作台` 首屏截图。

### 创建岗位截图

> 放置填充示例岗位并创建成功后显示 `job_id` 的截图。

### Agent 运行截图

> 放置步骤日志显示 running / done 状态的截图。

### 报告结果截图

> 放置 Markdown 渲染报告和下载按钮的截图。

## 后端启动

Windows PowerShell 推荐使用 `python -m uvicorn`。

```powershell
cd backend
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```

后端地址：

```text
http://127.0.0.1:8000
```

健康检查：

```powershell
curl.exe http://127.0.0.1:8000/health
```

API 文档：

```text
http://127.0.0.1:8000/docs
```

## 前端启动

```powershell
cd frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

访问：

```text
http://localhost:3000
```

前端环境变量：

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

## 快速演示流程

1. 启动后端。
2. 启动前端。
3. 打开 `http://localhost:3000`。
4. 点击“填充示例岗位”。
5. 点击“创建岗位”，确认页面显示 `job_id`。
6. 上传 `backend/data/samples/sample_profile.md` 或自己的 `.md` / `.txt` 资料。
7. 输入 query 并点击“检索资料”。
8. 点击“填充示例目标”。
9. 点击“运行 Career Agent”。
10. 查看步骤日志和阶段内容。
11. 查看 Markdown 渲染报告。
12. 点击“下载 Markdown 报告”。

## 文档索引

- [后端 MVP 验收](docs/backend_mvp_acceptance.md)
- [演示指南](docs/demo_guide.md)
- [项目日志](docs/project_log.md)
- [简历包装](docs/resume_packaging.md)
- [技术复盘](docs/technical_review.md)

## 测试与构建

后端：

```powershell
cd backend
python -m pytest
```

前端：

```powershell
cd frontend
npm run build
```

## 已知限制

- 阶段式 SSE，不是 token 级模型流式输出。
- fallback 检索，不是生产级向量检索。
- 单用户本地项目，没有多用户数据隔离。
- 无登录权限系统。
- 暂无 Docker。
- `.pdf` / `.docx` 深度解析未实现。

