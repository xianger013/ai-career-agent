import asyncio

import httpx

from app.services.embedding_service import EmbeddingService, EmbeddingServiceError


class FakeEmbeddingResponse:
    def __init__(self, payload: dict | None = None, status_error: bool = False) -> None:
        self.payload = payload or {"data": [{"embedding": [0.1, 0.2, 0.3]}]}
        self.status_error = status_error
        self.text = "provider error with test-key"
        self.status_code = 500

    def raise_for_status(self) -> None:
        if self.status_error:
            request = httpx.Request("POST", "https://example.test/v1/embeddings")
            response = httpx.Response(500, request=request, text=self.text)
            raise httpx.HTTPStatusError("bad response", request=request, response=response)

    def json(self) -> dict:
        return self.payload


class FakeAsyncClient:
    response = FakeEmbeddingResponse()

    def __init__(self, timeout: float) -> None:
        self.timeout = timeout

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return None

    async def post(self, url: str, headers: dict, json: dict):
        return self.response


def test_embedding_service_embed_text_with_mock_api(monkeypatch) -> None:
    FakeAsyncClient.response = FakeEmbeddingResponse()
    monkeypatch.setattr("app.services.embedding_service.httpx.AsyncClient", FakeAsyncClient)
    service = EmbeddingService(
        api_key="test-key",
        base_url="https://example.test/v1",
        model="text-embedding-test",
    )

    result = asyncio.run(service.embed_text("Python FastAPI"))

    assert result == [0.1, 0.2, 0.3]


def test_embedding_service_rejects_empty_text() -> None:
    service = EmbeddingService(
        api_key="test-key",
        base_url="https://example.test/v1",
        model="text-embedding-test",
    )

    try:
        asyncio.run(service.embed_text("  "))
    except EmbeddingServiceError as exc:
        assert "cannot be empty" in str(exc)
    else:
        raise AssertionError("Expected EmbeddingServiceError")


def test_embedding_service_provider_error_is_clear_and_redacted(monkeypatch) -> None:
    FakeAsyncClient.response = FakeEmbeddingResponse(status_error=True)
    monkeypatch.setattr("app.services.embedding_service.httpx.AsyncClient", FakeAsyncClient)
    service = EmbeddingService(
        api_key="test-key",
        base_url="https://example.test/v1",
        model="text-embedding-test",
    )

    try:
        asyncio.run(service.embed_text("Python FastAPI"))
    except EmbeddingServiceError as exc:
        message = str(exc)
        assert "Embedding provider returned HTTP 500" in message
        assert "test-key" not in message
        assert "[REDACTED_EMBEDDING_API_KEY]" in message
    else:
        raise AssertionError("Expected EmbeddingServiceError")
