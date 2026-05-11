from __future__ import annotations

import json
from collections.abc import AsyncGenerator

import httpx

from app.config import settings


class LLMServiceError(RuntimeError):
    pass


class LLMService:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else settings.llm_api_key
        self.base_url = base_url if base_url is not None else settings.llm_base_url
        self.model = model or settings.llm_model
        self.timeout = timeout or settings.request_timeout_seconds

    @property
    def is_configured(self) -> bool:
        return bool(
            self.api_key
            and self.base_url
            and self.api_key != "your_api_key_here"
            and "your_api_key" not in self.api_key
        )

    def _validate_config(self) -> None:
        if not self.api_key or self.api_key == "your_api_key_here":
            raise LLMServiceError("LLM_API_KEY is missing or still uses the placeholder value.")
        if not self.base_url:
            raise LLMServiceError("LLM_BASE_URL is missing.")

    def _sanitize_error_text(self, text: str) -> str:
        sanitized = text
        if self.api_key:
            sanitized = sanitized.replace(self.api_key, "[REDACTED_API_KEY]")
        return sanitized[:500]

    def _chat_url(self) -> str:
        assert self.base_url is not None
        return f"{self.base_url.rstrip('/')}/chat/completions"

    async def chat(self, messages: list[dict], temperature: float = 0.2) -> str:
        self._validate_config()
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self._chat_url(), headers=headers, json=payload)
                response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise LLMServiceError("LLM request timed out.") from exc
        except httpx.HTTPStatusError as exc:
            body = self._sanitize_error_text(exc.response.text)
            raise LLMServiceError(f"LLM provider returned HTTP {exc.response.status_code}: {body}") from exc
        except httpx.RequestError as exc:
            raise LLMServiceError(f"LLM network error: {self._sanitize_error_text(str(exc))}") from exc

        try:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise LLMServiceError("LLM response format is invalid.") from exc

    async def stream_chat(
        self,
        messages: list[dict],
        temperature: float = 0.2,
    ) -> AsyncGenerator[str, None]:
        self._validate_config()
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream("POST", self._chat_url(), headers=headers, json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        payload_text = line.removeprefix("data: ").strip()
                        if payload_text == "[DONE]":
                            break
                        data = json.loads(payload_text)
                        token = data.get("choices", [{}])[0].get("delta", {}).get("content")
                        if token:
                            yield token
        except httpx.TimeoutException as exc:
            raise LLMServiceError("LLM streaming request timed out.") from exc
        except httpx.HTTPStatusError as exc:
            raise LLMServiceError(f"LLM provider returned HTTP {exc.response.status_code}.") from exc
        except httpx.RequestError as exc:
            raise LLMServiceError(f"LLM network error: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise LLMServiceError("LLM streaming response contains invalid JSON.") from exc
