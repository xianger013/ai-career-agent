from __future__ import annotations


class InterviewService:
    def generate(self, job_analysis: dict, gap_analysis: dict, project_plan: dict) -> list[dict]:
        missing = "、".join(gap_analysis.get("missing_skills", [])[:3]) or "真实向量库和前端展示"
        return [
            {
                "question": "你如何介绍这个项目？",
                "answer": "这是一个面向求职者的 AI Agent 系统，可以根据岗位 JD 和个人资料生成能力差距、学习路线、项目方案、简历描述和面试问答。",
            },
            {
                "question": "后端架构如何拆分？",
                "answer": "API 层只处理请求响应，Service 层处理 LLM、检索和生成逻辑，Tool 层封装可复用能力，Agent 层负责编排完整工作流。",
            },
            {
                "question": "没有真实 embedding API 时怎么做？",
                "answer": "保留 EmbeddingService 和 VectorStore 抽象接口，开发模式使用关键词 fallback 检索，后续可平滑替换为 Chroma 或 FAISS。",
            },
            {
                "question": "Prompt 如何管理？",
                "answer": "Prompt 独立放在 app/prompts 下，代码只负责读取和注入输入，避免把长提示词硬编码在业务逻辑中。",
            },
            {
                "question": "当前项目还可以如何改进？",
                "answer": f"优先补齐 {missing}，并增加 SSE 流式输出、前端工作台、Docker 部署和更严格的评测集。",
            },
            {
                "question": "推荐项目方案的核心价值是什么？",
                "answer": project_plan.get("为什么适合该岗位", "展示端到端 AI Agent 工程能力。"),
            },
        ]

