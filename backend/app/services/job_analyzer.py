from __future__ import annotations

from pathlib import Path

from app.config import settings
from app.models.job import Job
from app.services.llm_service import LLMService, LLMServiceError


class JobAnalyzer:
    def __init__(self, llm_service: LLMService | None = None) -> None:
        self.llm_service = llm_service or LLMService()
        self.prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "job_analysis.md"

    async def analyze(self, job: Job) -> dict:
        prompt = self.prompt_path.read_text(encoding="utf-8")
        messages = [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": f"岗位标题: {job.title}\n公司: {job.company}\n岗位 JD:\n{job.description}",
            },
        ]

        if self.llm_service.is_configured:
            try:
                raw_markdown = await self.llm_service.chat(messages, temperature=settings.llm_temperature)
                return self._heuristic_analysis(job, raw_markdown=raw_markdown, llm_status="success")
            except LLMServiceError as exc:
                return self._heuristic_analysis(
                    job,
                    llm_status="fallback_after_llm_error",
                    llm_error=str(exc),
                )

        return self._heuristic_analysis(job, llm_status="fallback_no_llm_config")

    def _heuristic_analysis(
        self,
        job: Job,
        raw_markdown: str | None = None,
        llm_status: str = "fallback",
        llm_error: str | None = None,
    ) -> dict:
        text = f"{job.title}\n{job.description}".lower()
        skill_catalog = {
            "Python": ["python"],
            "FastAPI": ["fastapi"],
            "SQLAlchemy": ["sqlalchemy"],
            "SQL/SQLite": ["sql", "sqlite", "postgres"],
            "LLM API": ["llm", "openai", "chat completions", "大模型"],
            "Prompt Engineering": ["prompt", "提示词"],
            "RAG": ["rag", "检索", "向量", "embedding"],
            "Agent Workflow": ["agent", "工作流", "tool calling", "function calling"],
            "Docker": ["docker"],
            "React/Next.js": ["react", "next.js", "nextjs"],
            "Testing": ["pytest", "test", "测试"],
        }
        found = [
            skill
            for skill, keywords in skill_catalog.items()
            if any(keyword in text for keyword in keywords)
        ]
        if not found:
            found = ["Python", "LLM API", "Prompt Engineering", "RAG", "FastAPI"]

        ai_skills = [skill for skill in found if skill in {"LLM API", "Prompt Engineering", "RAG", "Agent Workflow"}]
        engineering = [skill for skill in found if skill not in set(ai_skills)]
        responsibilities = [
            "拆解岗位 JD 中的能力要求",
            "构建可复用的 AI Agent 工作流",
            "结合用户资料生成可执行的学习和项目路线",
        ]
        if "rag" in text or "检索" in text:
            responsibilities.append("实现文档检索和证据引用能力")
        if "api" in text or "后端" in text:
            responsibilities.append("提供稳定的后端 API 服务")

        analysis = {
            "job_id": job.id,
            "llm_status": llm_status,
            "llm_error": llm_error,
            "role_type": job.title,
            "core_responsibilities": responsibilities,
            "required_skills": found,
            "bonus_skills": ["部署经验", "自动化测试", "产品化表达"],
            "engineering_skills": engineering,
            "ai_skills": ai_skills or ["LLM API", "Prompt Engineering"],
            "product_skills": ["需求拆解", "结果结构化展示", "用户目标对齐"],
            "suggested_projects": [
                "AI Career Agent 求职能力分析系统",
                "基于 RAG 的个人知识库问答助手",
            ],
        }
        analysis["raw_markdown"] = raw_markdown or self._build_markdown(analysis)
        return analysis

    def _build_markdown(self, analysis: dict) -> str:
        def lines(items: list[str]) -> str:
            return "\n".join(f"- {item}" for item in items)

        return "\n\n".join(
            [
                "# 岗位分析结果",
                f"## 1. 岗位类型判断\n{analysis['role_type']}",
                f"## 2. 核心工作内容\n{lines(analysis['core_responsibilities'])}",
                f"## 3. 必备技术能力\n{lines(analysis['required_skills'])}",
                f"## 4. 加分能力\n{lines(analysis['bonus_skills'])}",
                f"## 5. AI Agent 相关能力\n{lines(analysis['ai_skills'])}",
                f"## 6. 工程开发能力\n{lines(analysis['engineering_skills'])}",
                "## 7. 对初学者的优先级建议\n- 先完成后端闭环，再补齐检索质量和前端展示。",
                f"## 8. 可用于补齐能力的项目方向\n{lines(analysis['suggested_projects'])}",
            ]
        )
