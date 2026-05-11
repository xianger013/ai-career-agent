from __future__ import annotations


class LearningPlanService:
    def generate(self, gap_analysis: dict) -> dict:
        priorities = gap_analysis.get("priority_order", [])
        focus = "、".join(priorities[:3]) if priorities else "岗位核心能力"
        return {
            "focus": focus,
            "phases": [
                {
                    "name": "第 1 阶段: 工程基础",
                    "goal": "建立可维护的后端项目结构",
                    "tasks": "FastAPI、SQLAlchemy、pytest、README",
                    "acceptance": "接口可启动，基础测试通过",
                    "duration": "3-5 天",
                },
                {
                    "name": "第 2 阶段: LLM API 调用",
                    "goal": "完成 OpenAI-compatible Chat Completions 调用",
                    "tasks": "封装 LLMService、错误处理、Prompt 文件化",
                    "acceptance": "岗位分析接口可在 mock 或真实模型下运行",
                    "duration": "2-3 天",
                },
                {
                    "name": "第 3 阶段: RAG 文档检索",
                    "goal": f"围绕 {focus} 建立证据检索能力",
                    "tasks": "上传资料、文本切分、fallback 检索",
                    "acceptance": "能返回与查询相关的资料片段",
                    "duration": "3-4 天",
                },
                {
                    "name": "第 4 阶段: Tool Calling",
                    "goal": "把核心能力封装成可复用工具",
                    "tasks": "AnalyzeJobTool、SearchProfileTool、SaveMarkdownTool",
                    "acceptance": "Agent 可按工具顺序执行",
                    "duration": "2 天",
                },
                {
                    "name": "第 5 阶段: Agent 工作流",
                    "goal": "完成从 JD 到报告的端到端编排",
                    "tasks": "差距分析、学习计划、项目方案、简历 bullet、面试 QA",
                    "acceptance": "输出完整 Markdown 报告",
                    "duration": "4-5 天",
                },
                {
                    "name": "第 6 阶段: 全栈展示与部署",
                    "goal": "补齐前端和部署材料",
                    "tasks": "Next.js 工作台、SSE、Docker",
                    "acceptance": "本地和容器均可演示",
                    "duration": "5-7 天",
                },
            ],
        }

