from __future__ import annotations


class GapAnalyzer:
    def analyze(self, job_analysis: dict, profile_evidence: list[dict]) -> dict:
        evidence_text = "\n".join(item.get("content", "") for item in profile_evidence).lower()
        required_skills = job_analysis.get("required_skills", [])

        matched: list[str] = []
        partial: list[str] = []
        missing: list[str] = []

        for skill in required_skills:
            skill_lower = skill.lower()
            if skill_lower and skill_lower in evidence_text:
                matched.append(skill)
            elif any(part in evidence_text for part in skill_lower.replace("/", " ").split()):
                partial.append(skill)
            else:
                missing.append(skill)

        return {
            "matched_skills": matched,
            "partial_skills": partial,
            "missing_skills": missing,
            "priority_order": missing[:3] + partial[:2],
            "next_30_days": [
                "Use a small project to connect the core technical chain required by the role",
                "Add verifiable project evidence for each missing skill",
                "Organize the README, API examples, test results, and deployment notes",
            ],
        }

