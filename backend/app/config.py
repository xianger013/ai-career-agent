from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "development")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./career_agent.db")
    llm_api_key: str | None = os.getenv("LLM_API_KEY")
    llm_base_url: str | None = os.getenv("LLM_BASE_URL")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    embedding_api_key: str | None = os.getenv("EMBEDDING_API_KEY")
    embedding_base_url: str | None = os.getenv("EMBEDDING_BASE_URL")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    embedding_provider: str = os.getenv("EMBEDDING_PROVIDER", "openai_compatible")
    rag_mode: str = os.getenv("RAG_MODE", "fallback")
    vector_store_type: str = os.getenv("VECTOR_STORE_TYPE", "json")
    vector_store_dir: Path = Path(os.getenv("VECTOR_STORE_DIR", "./data/vector_store"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    output_dir: Path = Path(os.getenv("OUTPUT_DIR", "./outputs"))
    upload_dir: Path = Path(os.getenv("UPLOAD_DIR", "./data/uploads"))
    request_timeout_seconds: float = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))

    @property
    def resolved_database_url(self) -> str:
        if not self.database_url.startswith("sqlite:///") or self.database_url == "sqlite:///:memory:":
            return self.database_url

        raw_path = self.database_url.removeprefix("sqlite:///")
        db_path = Path(raw_path)
        if db_path.is_absolute():
            return self.database_url

        resolved = (BASE_DIR / db_path).resolve().as_posix()
        return f"sqlite:///{resolved}"

    @property
    def resolved_output_dir(self) -> Path:
        return self.output_dir if self.output_dir.is_absolute() else BASE_DIR / self.output_dir

    @property
    def resolved_upload_dir(self) -> Path:
        return self.upload_dir if self.upload_dir.is_absolute() else BASE_DIR / self.upload_dir

    @property
    def resolved_vector_store_dir(self) -> Path:
        return self.vector_store_dir if self.vector_store_dir.is_absolute() else BASE_DIR / self.vector_store_dir


settings = Settings()
