"""LiteLLM wrapper with instructor structured output and provider fallback chain."""

from __future__ import annotations

import asyncio
import logging
from typing import TypeVar

import instructor
import litellm
from pydantic import BaseModel

from src.config import get_settings

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

# Suppress litellm's verbose logging
litellm.suppress_debug_info = True

_semaphore: asyncio.Semaphore | None = None


def get_llm_semaphore() -> asyncio.Semaphore:
    """Return cached semaphore capped at max_concurrent_llm."""
    global _semaphore
    if _semaphore is None:
        _semaphore = asyncio.Semaphore(get_settings().max_concurrent_llm)
    return _semaphore


def _get_providers() -> list[tuple[str, str, dict[str, str]]]:
    """Build ordered list of (model, name, extra_kwargs) from settings.

    When llm_provider is set (e.g. "deepseek" or "minimax"), only that
    cloud provider + ollama are returned. Otherwise all configured providers
    are included in priority order.
    """
    settings = get_settings()
    providers: list[tuple[str, str, dict[str, str]]] = []
    chosen = settings.llm_provider.lower().strip() if settings.llm_provider else ""

    # MiniMax
    if settings.minimax_api_key.get_secret_value() and chosen in ("", "minimax"):
        providers.append(
            (
                settings.minimax_model,
                "minimax",
                {
                    "api_key": settings.minimax_api_key.get_secret_value(),
                    "api_base": settings.minimax_api_base,
                },
            )
        )

    # DeepSeek V4 Flash
    if settings.deepseek_api_key.get_secret_value() and chosen in ("", "deepseek"):
        providers.append(
            (
                settings.deepseek_model,
                "deepseek",
                {"api_key": settings.deepseek_api_key.get_secret_value()},
            )
        )

    # Groq
    if settings.groq_api_key.get_secret_value() and chosen in ("", "groq"):
        providers.append(
            (
                settings.groq_model,
                "groq",
                {"api_key": settings.groq_api_key.get_secret_value()},
            )
        )

    # Gemini
    if settings.gemini_api_key.get_secret_value() and chosen in ("", "gemini"):
        providers.append(
            (
                settings.gemini_model,
                "gemini",
                {"api_key": settings.gemini_api_key.get_secret_value()},
            )
        )

    # Ollama (local fallback — always available)
    providers.append(
        (
            settings.ollama_model,
            "ollama",
            {"api_base": settings.ollama_host},
        )
    )

    return providers


async def complete_structured(  # noqa: UP047
    messages: list[dict[str, str]],
    response_model: type[T],
    temperature: float | None = None,
) -> T:
    """Call LLM with fallback chain and return structured Pydantic output.

    When llm_provider is set, only that cloud provider + ollama are tried.
    Otherwise all configured providers are tried in priority order.
    Uses instructor for structured output extraction.
    """
    providers = _get_providers()
    if not providers:
        msg = "no LLM providers configured"
        raise RuntimeError(msg)

    last_error: Exception | None = None

    for model, name, kwargs in providers:
        try:
            # JSON mode for providers where tool calling is incompatible
            mode = instructor.Mode.JSON if name in {"ollama", "minimax", "deepseek"} else instructor.Mode.TOOLS
            client = instructor.from_litellm(litellm.acompletion, mode=mode)

            sem = get_llm_semaphore()
            async with sem:
                result = await client.chat.completions.create(
                    model=model,
                    messages=messages,
                    response_model=response_model,
                    temperature=temperature,
                    **kwargs,
                )
            logger.info("llm complete provider=%s model=%s", name, model)
            return result
        except Exception as exc:
            logger.warning(
                "llm provider failed provider=%s model=%s error=%s",
                name,
                model,
                str(exc),
            )
            last_error = exc
            continue

    msg = f"all LLM providers failed, last error: {last_error}"
    raise RuntimeError(msg)
