from __future__ import annotations


class ProjectPlanService:
    def generate(self, job_analysis: dict, gap_analysis: dict, user_goal: str) -> dict:
        skills = job_analysis.get("required_skills", [])[:6]
        missing = gap_analysis.get("missing_skills", [])[:3]
        return {
            "项目名称": "AI Career Agent 求职能力分析系统",
            "项目目标": "输入岗位 JD 和个人资料，自动生成能力差距、学习路线、项目方案、简历描述和面试问答。",
            "为什么适合该岗位": f"该项目直接覆盖 {user_goal}，并能展示 LLM、RAG、Agent、后端工程能力。",
            "覆盖的岗位能力": "、".join(skills + missing) or "LLM API、RAG、Agent 工作流、FastAPI",
            "技术栈": "Python、FastAPI、SQLAlchemy、SQLite、httpx、pytest、OpenAI-compatible API",
            "功能模块": "岗位管理、资料上传、fallback 检索、Agent 编排、Markdown 报告保存",
            "开发阶段": "后端 MVP -> 检索增强 -> 前端工作台 -> SSE -> Docker 部署",
            "每阶段验收标准": "接口可用、测试通过、报告可生成、演示链路完整",
            "简历表达方式": "突出端到端 AI Agent 工程闭环，而不是只写模型调用。",
            "后续可扩展方向": "接入真实向量库、SSE 流式输出、多用户资料隔离、前端可视化。",
        }

