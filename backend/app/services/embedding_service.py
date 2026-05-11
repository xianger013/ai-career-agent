from __future__ import annotations

import json

import httpx

from app.config import settings


class EmbeddingServiceError(RuntimeError):
    pass


class EmbeddingService:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        provider: str | None = None,
        timeout: float | None = None,
        batch_size: int = 64,
    ) -> None:
        self.api_key = api_key if api_key is not None else settings.embedding_api_key
        self.base_url = base_url if base_url is not None else settings.embedding_base_url
        self.model = model or settings.embedding_model
        self.provider = provider or settings.embedding_provider
        self.timeout = timeout or settings.request_timeout_seconds
        self.batch_size = batch_size

    @property
    def is_configured(self) -> bool:
        return bool(
            self.api_key
            and self.base_url
            and self.api_key != "your_embedding_api_key_here"
            and "your_embedding_api_key" not in self.api_key
        )

    async def embed_text(self, text: str) -> list[float]:
        embeddings = await self.embed_documents([text])
        return embeddings[0]

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        clean_texts = [text.strip() for text in texts]
        if not clean_texts:
            return []
        if any(not text for text in clean_texts):
            raise EmbeddingServiceError("Embedding input text cannot be empty.")

        self._validate_config()
        embeddings: list[list[float]] = []
        for start in range(0, len(clean_texts), self.batch_size):
            batch = clean_texts[start : start + self.batch_size]
            embeddings.extend(await self._embed_batch(batch))
        return embeddings

    def _validate_config(self) -> None:
        if self.provider != "openai_compatible":
            raise EmbeddingServiceError(f"Unsupported EMBEDDING_PROVIDER: {self.provider}")
        if not self.api_key or self.api_key == "your_embedding_api_key_here":
            raise EmbeddingServiceError("EMBEDDING_API_KEY is missing or still uses the placeholder value.")
        if not self.base_url:
            raise EmbeddingServiceError("EMBEDDING_BASE_URL is missing.")
        if not self.model:
            raise EmbeddingServiceError("EMBEDDING_MODEL is missing.")

    async def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        payload = {"model": self.model, "input": texts}
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url.rstrip('/')}/embeddings",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise EmbeddingServiceError("Embedding request timed out.") from exc
        except httpx.HTTPStatusError as exc:
            body = self._sanitize_error_text(exc.response.text)
            raise EmbeddingServiceError(
                f"Embedding provider returned HTTP {exc.response.status_code}: {body}"
            ) from exc
        except httpx.RequestError as exc:
            raise EmbeddingServiceError(f"Embedding network error: {self._sanitize_error_text(str(exc))}") from exc

        try:
            data = response.json()
            embeddings = [item["embedding"] for item in data["data"]]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise EmbeddingServiceError("Embedding response format is invalid.") from exc

        if len(embeddings) != len(texts):
            raise EmbeddingServiceError("Embedding response count does not match input count.")
        return embeddings

    def _sanitize_error_text(self, text: str) -> str:
        sanitized = text
        if self.api_key:
            sanitized = sanitized.replace(self.api_key, "[REDACTED_EMBEDDING_API_KEY]")
        return sanitized[:500]
