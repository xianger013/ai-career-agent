from __future__ import annotations

from app.models.job import Job


def _section_list(items: list[str] | list[dict]) -> str:
    if not items:
        return "- 暂无明确证据"
    lines: list[str] = []
    for item in items:
        if isinstance(item, dict):
            content = item.get("content") or item.get("question") or str(item)
            source = item.get("source")
            lines.append(f"- {content}" + (f" 来源: {source}" if source else ""))
        else:
            lines.append(f"- {item}")
    return "\n".join(lines)


def build_analysis_report(
    job: Job,
    job_analysis: dict,
    profile_evidence: list[dict],
    gap_analysis: dict,
    learning_plan: dict,
    project_plan: dict,
    resume_bullets: list[str],
    interview_qa: list[dict],
) -> str:
    """Build the final Markdown report saved by the agent."""
    required_skills = job_analysis.get("required_skills", [])
    missing_skills = gap_analysis.get("missing_skills", [])
    partial_skills = gap_analysis.get("partial_skills", [])
    phases = learning_plan.get("phases", [])

    phase_lines = []
    for phase in phases:
        phase_lines.append(
            "\n".join(
                [
                    f"### {phase.get('name', '阶段')}",
                    f"- 目标: {phase.get('goal', '')}",
                    f"- 任务: {phase.get('tasks', '')}",
                    f"- 验收标准: {phase.get('acceptance', '')}",
                    f"- 预计时间: {phase.get('duration', '')}",
                ]
            )
        )

    qa_lines = []
    for item in interview_qa:
        qa_lines.append(
            "\n".join(
                [
                    f"### {item.get('question', '问题')}",
                    item.get("answer", ""),
                ]
            )
        )

    return "\n\n".join(
        [
            "# AI Career Agent 分析报告",
            "## 1. 岗位基本信息",
            f"- 岗位: {job.title}",
            f"- 公司: {job.company}",
            "## 2. 岗位能力结构化拆解",
            job_analysis.get("raw_markdown", ""),
            "## 3. 用户资料证据",
            _section_list(profile_evidence),
            "## 4. 能力匹配情况",
            _section_list(gap_analysis.get("matched_skills", [])),
            "## 5. 能力差距分析",
            f"### 部分具备但需强化\n{_section_list(partial_skills)}\n\n### 明显缺失\n{_section_list(missing_skills)}",
            "## 6. 推荐学习路线",
            "\n\n".join(phase_lines) if phase_lines else "- 暂无",
            "## 7. 推荐项目方案",
            "\n".join(f"- {key}: {value}" for key, value in project_plan.items()),
            "## 8. 简历项目描述",
            _section_list(resume_bullets),
            "## 9. 面试问答准备",
            "\n\n".join(qa_lines) if qa_lines else "- 暂无",
            "## 10. 下一步行动清单",
            _section_list(
                [
                    "补齐缺失技能中优先级最高的 2 项",
                    "用推荐项目完成可演示的端到端闭环",
                    "把项目 README、测试和部署方式整理成面试材料",
                ]
                + [f"重点补齐: {skill}" for skill in required_skills[:3]]
            ),
        ]
    )

