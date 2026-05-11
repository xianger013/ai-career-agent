# Resume Packaging

## 项目名称

AI Career Agent：面向大学生求职的能力差距分析与学习规划 Agent

## 项目简介

基于 FastAPI、Next.js、LLM API、RAG fallback 检索和 SSE 实现的 AI Agent 工作台。用户可以创建岗位 JD、上传个人资料，系统会分析岗位能力要求、检索资料证据、生成能力差距、学习路线、推荐项目、简历描述和面试问答，并输出 Markdown 报告。

## 技术栈

FastAPI、SQLAlchemy、SQLite、Next.js、React、TypeScript、Tailwind CSS、SSE、OpenAI-compatible API、Prompt Engineering。

## 简历 Bullet Points

- 设计并实现 AI Career Agent 全栈 MVP，支持岗位 JD 创建、资料上传、能力差距分析、学习路线生成和 Markdown 报告输出。
- 基于 FastAPI、Pydantic v2 和 SQLAlchemy 搭建后端分层架构，将 API、Service、Tool、Agent、Prompt 模块解耦。
- 封装 OpenAI-compatible `LLMService`，支持超时、网络错误、模型错误处理，并在无 API Key 时使用本地 fallback 逻辑保障演示可运行。
- 设计轻量级 Agent workflow，将 `load_job`、`analyze_job`、`search_profile_evidence`、`analyze_gap`、`generate_learning_plan` 等步骤串联为可追踪执行链路。
- 实现 `.md` / `.txt` 资料上传、文本切分和 fallback 关键词检索，为后续替换 ChromaDB/FAISS 保留 `VectorStore` 抽象接口。
- 使用 SSE 和 EventSource 实现阶段式流式反馈，让前端可以实时展示 Agent 执行进度和阶段内容。
- 使用 Next.js、React、TypeScript 和 Tailwind CSS 搭建单页工作台，支持岗位输入、资料上传、检索测试、Agent 运行、Markdown 渲染、复制和下载报告。
- 编写 pytest 覆盖健康检查、文本切分、岗位分析、检索、SSE 和完整 Agent 工作流，降低迭代时破坏核心链路的风险。

## 面试讲解

### 项目背景

很多大学生或求职者面对岗位 JD 时不知道应该补齐哪些能力，也不知道如何把学习内容包装成项目经历。这个项目把岗位分析、个人资料检索、差距分析、学习规划和简历表达串成一个 Agent 工作台。

### 核心流程

用户先创建岗位 JD，再上传个人资料或项目笔记。后端分析岗位能力结构，检索用户资料中的相关证据，判断已具备能力和缺失能力，然后生成学习计划、项目方案、简历 bullet 和面试问答，最后保存并展示 Markdown 报告。

### Agent 如何拆分任务

Agent 不直接把所有逻辑写在一个函数里，而是拆成可复用工具：岗位分析工具、资料检索工具、学习计划生成工具、简历生成工具、面试问答工具和 Markdown 保存工具。Agent 层只负责编排顺序和保存 step log。

### SSE 为什么有用

Agent 工作流可能包含多个阶段，用户如果只等待最终结果会缺少反馈。SSE 可以在不引入 WebSocket 复杂度的情况下，让前端实时看到每个阶段的 running/done 状态，适合这种单向进度推送场景。

### 当前 fallback 检索和正式 RAG 的区别

当前 fallback 检索主要基于关键词 token overlap，优点是本地可运行、依赖少、方便演示。正式 RAG 会使用 embedding 模型把文本向量化，并通过 ChromaDB、FAISS 等向量库做语义召回，能处理同义表达和更复杂的问题。

### 下一步如何扩展 ChromaDB/FAISS

后端已经保留 `EmbeddingService` 和 `VectorStore` 抽象。下一步可以在上传资料时生成真实 embedding，把 chunk 写入 ChromaDB 或 FAISS；检索时对 query 生成 embedding 并做 top-k 召回，再把召回证据交给 Agent 生成报告。

### 当前项目的不足

- 目前是单用户本地项目，没有登录和权限隔离。
- SSE 是阶段式流式，不是 token 级模型输出。
- fallback 检索不是生产级 RAG。
- 没有 Docker 部署和云端运行环境。
- 前端主要用于演示，还没有端到端自动化测试。

