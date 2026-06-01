from __future__ import annotations

from app.models.job import Job


def _section_list(items: list[str] | list[dict]) -> str:
    if not items:
        return "- No clear evidence yet"
    lines: list[str] = []
    for item in items:
        if isinstance(item, dict):
            content = item.get("content") or item.get("question") or str(item)
            source = item.get("source")
            lines.append(f"- {content}" + (f" Source: {source}" if source else ""))
        else:
            lines.append(f"- {item}")
    return "\n".join(lines)


def _evidence_list(items: list[dict]) -> str:
    if not items:
        return "- Not enough profile evidence was retrieved"

    lines: list[str] = []
    for item in items:
        metadata = item.get("metadata", {})
        filename = metadata.get("filename") or item.get("source") or "unknown"
        chunk_index = metadata.get("chunk_index", "unknown")
        score = item.get("score", 0)
        mode = item.get("retrieval_mode", "unknown")
        content = (item.get("content") or "").replace("\n", " ").strip()
        summary = content[:240] + ("..." if len(content) > 240 else "")
        lines.append(
            f"- Retrieval mode: {mode} | Source: {filename} | chunk_index: {chunk_index} | score: {score}\n"
            f"  - Evidence summary: {summary}"
        )
    return "\n".join(lines)


def _retrieval_modes(items: list[dict]) -> str:
    modes = sorted({item.get("retrieval_mode", "unknown") for item in items}) if items else []
    if not modes:
        return "not enough profile evidence retrieved"
    labels = {
        "fallback": "fallback keyword search",
        "vector": "vector RAG",
        "fallback_due_to_vector_error": "fallback_due_to_vector_error",
    }
    return ", ".join(labels.get(mode, mode) for mode in modes)


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
                    f"### {phase.get('name', 'Phase')}",
                    f"- Goal: {phase.get('goal', '')}",
                    f"- Tasks: {phase.get('tasks', '')}",
                    f"- Acceptance criteria: {phase.get('acceptance', '')}",
                    f"- Estimated time: {phase.get('duration', '')}",
                ]
            )
        )

    qa_lines = []
    for item in interview_qa:
        qa_lines.append(
            "\n".join(
                [
                    f"### {item.get('question', 'Question')}",
                    item.get("answer", ""),
                ]
            )
        )

    return "\n\n".join(
        [
            "# AI Career Agent Analysis Report",
            "## 1. Job Overview",
            f"- Job: {job.title}",
            f"- Company: {job.company}",
            "## 2. Structured Job Analysis",
            job_analysis.get("raw_markdown", ""),
            "## 3. Profile Evidence",
            f"Retrieval modes: {_retrieval_modes(profile_evidence)}\n\n{_evidence_list(profile_evidence)}",
            "## 4. Skill Matches",
            _section_list(gap_analysis.get("matched_skills", [])),
            "## 5. Skill Gap Analysis",
            f"### Partially covered and needs strengthening\n{_section_list(partial_skills)}\n\n### Missing skills\n{_section_list(missing_skills)}",
            "## 6. Recommended Learning Path",
            "\n\n".join(phase_lines) if phase_lines else "- Not available yet",
            "## 7. Recommended Project Plan",
            "\n".join(f"- {key}: {value}" for key, value in project_plan.items()),
            "## 8. Resume Project Bullets",
            _section_list(resume_bullets),
            "## 9. Interview Q&A Preparation",
            "\n\n".join(qa_lines) if qa_lines else "- Not available yet",
            "## 10. Next Action Checklist",
            _section_list(
                [
                    "Close the top 2 missing skills first",
                    "Use the recommended project to build a demonstrable end-to-end loop",
                    "Turn the README, tests, and setup flow into interview-ready evidence",
                ]
                + [f"Priority skill to strengthen: {skill}" for skill in required_skills[:3]]
            ),
        ]
    )
