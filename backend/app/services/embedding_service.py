from __future__ import annotations

import hashlib
import math

import httpx

from app.config import settings


class EmbeddingService:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else settings.embedding_api_key
        self.base_url = base_url if base_url is not None else settings.embedding_base_url
        self.model = model or settings.embedding_model
        self.timeout = timeout or settings.request_timeout_seconds

    @property
    def is_configured(self) -> bool:
        return bool(
            self.api_key
            and self.base_url
            and self.api_key != "your_embedding_api_key_here"
            and "your_embedding_api_key" not in self.api_key
        )

    async def embed_text(self, text: str) -> list[float]:
        return (await self.embed_documents([text]))[0]

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not self.is_configured:
            return [self._fallback_embedding(text) for text in texts]

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
                data = response.json()
                return [item["embedding"] for item in data["data"]]
        except Exception:
            return [self._fallback_embedding(text) for text in texts]

    def _fallback_embedding(self, text: str, dimensions: int = 64) -> list[float]:
        vector = [0.0] * dimensions
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = digest[0] % dimensions
            vector[index] += 1.0
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]

