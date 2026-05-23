from __future__ import annotations

from src.fetcher.types import QualityResult

PAYWALL_MARKERS = (
    "don't settle for shallow",
    "join premium members",
    "this article is for subscribers",
    "subscribe to continue reading",
    "already a subscriber? sign in",
    "subscribe to get full access",
    "become a subscriber",
    "to continue reading this article",
)


def _strip_md(text: str) -> str:
    return text.replace("*", "").replace("_", "").replace("#", "")


def check_quality(text: str | None) -> QualityResult:
    if not text:
        return QualityResult(passed=False, reason="too_short")

    stripped = text.strip()
    lower = stripped.lower()

    if len(stripped) < 500:
        for pattern in ("403 forbidden", "access denied", "404 not found", "cloudflare"):
            if pattern in lower:
                return QualityResult(passed=False, reason="error_page")

    if len(stripped) < 100:
        words = lower.split()
        if len(words) <= 2:
            for pattern in ("nginx", "error", "forbidden"):
                if pattern in words:
                    return QualityResult(passed=False, reason="error_page")

    if len(stripped) < 200:
        return QualityResult(passed=False, reason="too_short")

    cleaned = _strip_md(lower)
    for marker in PAYWALL_MARKERS:
        if marker in cleaned:
            return QualityResult(passed=False, reason="paywalled")

    return QualityResult(passed=True)
