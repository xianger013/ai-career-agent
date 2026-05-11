# Demo Guide

## 项目演示目标

这次演示的目标不是展示复杂 UI，而是证明 AI Career Agent 已经具备完整作品集闭环：

- 输入岗位 JD。
- 上传个人资料。
- 检索资料证据。
- 通过阶段式 SSE 展示 Agent 执行链路。
- 生成可复制、可下载的 Markdown 报告。
- 展示后端工程、Prompt、Agent workflow、fallback RAG、SSE 和 Next.js 前端能力。

## 后端启动

Windows PowerShell 推荐使用 `python -m uvicorn`，避免命令指向错误解释器。

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

检查方式：

```powershell
curl.exe http://127.0.0.1:8000/health
```

或打开：

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

前端地址：

```text
http://localhost:3000
```

`.env.local` 必须包含：

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

## 一次完整演示流程

1. 启动后端和前端。
2. 打开 `http://localhost:3000`。
3. 点击“填充示例岗位”。
4. 点击“创建岗位”，确认页面显示 `job_id`。
5. 上传 `backend/data/samples/sample_profile.md` 或自定义 `.md` / `.txt` 资料。
6. 在检索区输入 `Python FastAPI RAG 项目经验`，点击“检索资料”。
7. 点击“填充示例目标”。
8. 点击“运行 Career Agent”。
9. 观察步骤日志从 `load_job` 到 `final`。
10. 查看 Markdown 渲染后的报告。
11. 点击“复制 Markdown”或“下载 Markdown 报告”。

## 推荐截图清单

- 首页完整工作台截图。
- 填充示例岗位后的岗位输入区截图。
- 上传资料和检索结果截图。
- Agent 运行中步骤日志截图。
- Markdown 报告渲染结果截图。
- 下载报告按钮和生成的 `.md` 文件截图。

## 常见问题

### 访问 `http://127.0.0.1:8000` 返回 Not Found 是否正常？

正常。后端没有定义根路径 `/`。请访问：

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

### Windows 下为什么推荐 `python -m uvicorn`？

它能确保使用当前 Python 环境中的 uvicorn，避免全局命令、PATH 或虚拟环境未激活导致启动失败。

### 前端无法连接后端怎么办？

检查 `frontend/.env.local`：

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

修改后需要重启 `npm run dev`。

### SSE 是 token 级流式吗？

不是。当前 SSE 是阶段式流式：每个 Agent 阶段开始、结束，以及阶段内容会推送事件。后续可以在 LLMService 支持 token stream 后升级。

### 检索是不是正式 RAG？

当前是 fallback 关键词检索，不是生产级向量检索。代码保留了 `VectorStore` 抽象，后续可以替换为 ChromaDB 或 FAISS。

