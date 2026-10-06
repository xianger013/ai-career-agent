from __future__ import annotations


class InterviewService:
    def generate(self, job_analysis: dict, gap_analysis: dict, project_plan: dict) -> list[dict]:
        missing = ", ".join(gap_analysis.get("missing_skills", [])[:3]) or "production vector storage and frontend presentation"
        return [
            {
                "question": "How would you introduce this project?",
                "answer": "It is an AI agent system for job seekers that turns a job description and profile notes into skill gaps, a learning path, project ideas, resume bullets, and interview Q&A.",
            },
            {
                "question": "How is the backend architecture split?",
                "answer": "The API layer handles requests and responses, services handle LLM, retrieval, and generation logic, tools wrap reusable capabilities, and the agent layer orchestrates the full workflow.",
            },
            {
                "question": "What happens without a real embedding API?",
                "answer": "The project keeps EmbeddingService and VectorStore abstractions, uses keyword fallback retrieval in development, and can later swap in Chroma or FAISS.",
            },
            {
                "question": "How are prompts managed?",
                "answer": "Prompts live under app/prompts, while code only reads them and injects inputs. This keeps long prompts out of business logic.",
            },
            {
                "question": "How can the project improve next?",
                "answer": f"Prioritize {missing}, then add SSE streaming, the frontend workspace, Docker deployment, and stricter evaluation cases.",
            },
            {
                "question": "What is the core value of the recommended project plan?",
                "answer": project_plan.get("Why it fits this role", "It demonstrates end-to-end AI agent engineering ability."),
            },
        ]

