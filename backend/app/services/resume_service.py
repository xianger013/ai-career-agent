from __future__ import annotations


class ResumeService:
    def generate(self, project_plan: dict, job_analysis: dict) -> list[str]:
        skills = "、".join(job_analysis.get("required_skills", [])[:5])
        return [
            "设计并实现 AI Career Agent 后端 MVP，支持岗位 JD 创建、资料上传、检索证据召回和完整分析报告生成。",
            f"封装 OpenAI-compatible LLMService 与 Prompt 文件化流程，将岗位能力拆解为结构化结果，覆盖 {skills} 等能力。",
            "实现轻量级 Agent 工作流和 Tool Calling 抽象，按 load_job、analyze_job、search_profile_evidence、save_report 等步骤编排任务。",
            "基于 SQLite、SQLAlchemy 和 fallback 关键词检索完成第一版 RAG 闭环，并用 pytest 覆盖健康检查、文本切分、检索和 Agent 流程。",
            f"项目方案: {project_plan.get('项目名称', 'AI Career Agent')}，可继续扩展 SSE、向量库和前端工作台。",
        ]

