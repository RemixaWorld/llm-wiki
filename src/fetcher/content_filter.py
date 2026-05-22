from __future__ import annotations

from src.fetcher.types import QualityResult


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

    return QualityResult(passed=True)
