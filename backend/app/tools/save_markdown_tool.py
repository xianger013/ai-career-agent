from __future__ import annotations

from pathlib import Path


class SaveMarkdownTool:
    name = "save_markdown"
    description = "Save a Markdown report to the output directory."
    input_schema = {"type": "object", "required": ["content", "filename"]}

    async def run(self, content: str, output_dir: Path, filename: str) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / filename
        path.write_text(content, encoding="utf-8")
        return path

