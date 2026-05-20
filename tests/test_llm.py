"""Tests for LLM wrapper with mocked litellm."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from pydantic import BaseModel

from src.llm import _get_providers, complete_structured


class SimpleOutput(BaseModel):
    answer: str
    confidence: float


class TestGetProviders:
    def test_ollama_always_present(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("WIKI_MINIMAX_API_KEY", "")
        monkeypatch.setenv("WIKI_DEEPSEEK_API_KEY", "")
        monkeypatch.setenv("WIKI_GROQ_API_KEY", "")
        monkeypatch.setenv("WIKI_GEMINI_API_KEY", "")

        # Reset singleton
        import src.config

        src.config._settings = None

        providers = _get_providers()
        assert len(providers) >= 1
        names = [p[1] for p in providers]
        assert "ollama" in names

        src.config._settings = None

    def test_groq_added_when_key_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("WIKI_MINIMAX_API_KEY", "")
        monkeypatch.setenv("WIKI_DEEPSEEK_API_KEY", "")
        monkeypatch.setenv("WIKI_GROQ_API_KEY", "test-key-123")
        monkeypatch.setenv("WIKI_GEMINI_API_KEY", "")

        import src.config

        src.config._settings = None

        providers = _get_providers()
        names = [p[1] for p in providers]
        assert names[0] == "groq"

        src.config._settings = None

    def test_provider_order(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("WIKI_MINIMAX_API_KEY", "mm-key")
        monkeypatch.setenv("WIKI_DEEPSEEK_API_KEY", "ds-key")
        monkeypatch.setenv("WIKI_GROQ_API_KEY", "groq-key")
        monkeypatch.setenv("WIKI_GEMINI_API_KEY", "gemini-key")

        import src.config

        src.config._settings = None

        providers = _get_providers()
        names = [p[1] for p in providers]
        assert names == ["minimax", "deepseek", "groq", "gemini", "ollama"]

        src.config._settings = None

    def test_deepseek_between_minimax_and_groq(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("WIKI_MINIMAX_API_KEY", "")
        monkeypatch.setenv("WIKI_DEEPSEEK_API_KEY", "ds-key")
        monkeypatch.setenv("WIKI_GROQ_API_KEY", "groq-key")
        monkeypatch.setenv("WIKI_GEMINI_API_KEY", "gemini-key")

        import src.config

        src.config._settings = None

        providers = _get_providers()
        names = [p[1] for p in providers]
        assert names == ["deepseek", "groq", "gemini", "ollama"]

        src.config._settings = None


class TestCompleteStructured:
    @pytest.mark.asyncio
    async def test_returns_structured_output(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Mock instructor client to return structured output."""
        monkeypatch.setenv("WIKI_GROQ_API_KEY", "")
        monkeypatch.setenv("WIKI_GEMINI_API_KEY", "")

        import src.config

        src.config._settings = None

        expected = SimpleOutput(answer="42", confidence=0.95)

        mock_create = AsyncMock(return_value=expected)
        mock_client = AsyncMock()
        mock_client.chat.completions.create = mock_create

        with patch("src.llm.instructor.from_litellm", return_value=mock_client):
            result = await complete_structured(
                messages=[{"role": "user", "content": "What is 6*7?"}],
                response_model=SimpleOutput,
                temperature=0.1,
            )

        assert result.answer == "42"
        assert result.confidence == 0.95
        mock_create.assert_called_once()

        src.config._settings = None

    @pytest.mark.asyncio
    async def test_fallback_on_failure(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """First provider fails, second succeeds."""
        monkeypatch.setenv("WIKI_MINIMAX_API_KEY", "")
        monkeypatch.setenv("WIKI_GROQ_API_KEY", "groq-key")
        monkeypatch.setenv("WIKI_GEMINI_API_KEY", "")

        import src.config

        src.config._settings = None

        expected = SimpleOutput(answer="fallback", confidence=0.8)
        call_count = 0

        async def mock_create(**kwargs: object) -> SimpleOutput:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ConnectionError("groq down")
            return expected

        mock_client = AsyncMock()
        mock_client.chat.completions.create = mock_create

        with patch("src.llm.instructor.from_litellm", return_value=mock_client):
            result = await complete_structured(
                messages=[{"role": "user", "content": "test"}],
                response_model=SimpleOutput,
            )

        assert result.answer == "fallback"
        assert call_count == 2  # groq failed, ollama succeeded

        src.config._settings = None

    @pytest.mark.asyncio
    async def test_all_providers_fail(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """All providers fail — raises RuntimeError."""
        monkeypatch.setenv("WIKI_MINIMAX_API_KEY", "")
        monkeypatch.setenv("WIKI_GROQ_API_KEY", "")
        monkeypatch.setenv("WIKI_GEMINI_API_KEY", "")

        import src.config

        src.config._settings = None

        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(side_effect=ConnectionError("down"))

        with (
            patch("src.llm.instructor.from_litellm", return_value=mock_client),
            pytest.raises(RuntimeError, match="all LLM providers failed"),
        ):
            await complete_structured(
                messages=[{"role": "user", "content": "test"}],
                response_model=SimpleOutput,
            )

        src.config._settings = None


class TestLLMSemaphore:
    @pytest.mark.asyncio
    async def test_semaphore_limits_concurrency(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Global semaphore caps concurrent LLM API calls."""
        monkeypatch.setenv("WIKI_MINIMAX_API_KEY", "")
        monkeypatch.setenv("WIKI_GROQ_API_KEY", "")
        monkeypatch.setenv("WIKI_GEMINI_API_KEY", "")
        monkeypatch.setenv("WIKI_MAX_CONCURRENT_LLM", "2")

        import src.config
        import src.llm

        src.config._settings = None
        src.llm._semaphore = None

        import asyncio

        peak = 0
        current = 0

        async def mock_create(**kwargs: object) -> SimpleOutput:
            nonlocal peak, current
            current += 1
            peak = max(peak, current)
            await asyncio.sleep(0.05)
            current -= 1
            return SimpleOutput(answer="ok", confidence=0.9)

        mock_client = AsyncMock()
        mock_client.chat.completions.create = mock_create

        with patch("src.llm.instructor.from_litellm", return_value=mock_client):
            results = await asyncio.gather(
                *[
                    complete_structured(
                        messages=[{"role": "user", "content": f"test {i}"}],
                        response_model=SimpleOutput,
                    )
                    for i in range(5)
                ],
            )

        assert len(results) == 5
        assert peak <= 2  # never exceeded max_concurrent_llm

        src.config._settings = None
        src.llm._semaphore = None
