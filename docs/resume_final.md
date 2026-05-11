# Resume Final

## 1. 项目名称

AI Career Agent：面向大学生求职的能力差距分析与学习规划 Agent

## 2. 一句话介绍

基于 FastAPI、Next.js、LLM API、RAG 和 SSE 实现的 AI Agent 工作台，支持岗位 JD 分析、个人资料检索、能力差距分析、学习路线生成、项目建议、简历描述和面试问答生成。

## 3. 技术栈

FastAPI / SQLAlchemy / SQLite / Next.js / React / TypeScript / Tailwind CSS / SSE / OpenAI-compatible API / Embedding / JSON VectorStore / Prompt Engineering / RAG / Agent Workflow

## 4. 简历 Bullet Points

- 基于 FastAPI 设计后端 API，支持岗位创建、资料上传、文档检索和 Agent 分析流程。
- 使用 Next.js + TypeScript 实现前端工作台，通过 SSE 展示 Agent 阶段式执行过程。
- 设计 CareerAgent 工作流，将岗位分析、资料检索、差距分析、学习路线、简历生成和面试问答拆分为可维护步骤。
- 实现 OpenAI-compatible LLMService 和 EmbeddingService，支持模型配置、超时控制和错误处理。
- 构建 RAG 检索模块，支持 fallback keyword search 与 Embedding + JSON VectorStore 向量检索。
- 生成 Markdown 分析报告，支持前端渲染、复制和下载，便于作品集展示。
- 编写 pytest 测试覆盖健康检查、文本切分、岗位分析、检索、SSE 和 Agent 工作流核心链路。
- 补充 README、RAG 设计、技术复盘、演示指南、面试问答等文档，提高项目可复现性和可展示性。

## 5. 简历短版

- 实现 AI Career Agent 全栈 MVP，支持岗位 JD 分析、资料上传、RAG 检索、Agent 工作流和 Markdown 报告生成。
- 基于 FastAPI + SQLAlchemy + SQLite 构建后端，封装 LLMService / EmbeddingService 并提供清晰错误处理。
- 使用 Next.js + TypeScript + Tailwind CSS 实现前端工作台，通过 SSE 展示 Agent 阶段式执行进度。
- 编写 pytest 和完整 README/docs，覆盖核心链路并说明项目限制、演示流程和后续扩展方向。

## 6. 简历长版

AI Career Agent 是一个面向大学生求职的 AI Agent 工作台。项目从岗位 JD 分析出发，结合用户上传的个人资料，通过 LLM、RAG 检索和 Agent 工作流生成能力差距、学习路线、项目建议、简历描述和面试问答。后端使用 FastAPI、SQLAlchemy 和 SQLite，前端使用 Next.js、React、TypeScript 和 Tailwind CSS。系统支持 fallback keyword search 和 OpenAI-compatible Embedding + JSON VectorStore 两种检索模式，并通过 SSE 向前端推送阶段式执行进度。项目补充了测试、README、演示指南、RAG 设计和面试材料，适合作为 AI 应用开发方向的作品集项目。

