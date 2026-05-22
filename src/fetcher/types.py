from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class FetchResult(BaseModel):
    url: str
    status: str  # ok | dead | failed | paywalled | unavailable | low_quality | duplicate
    title: str | None = None
    content: str | None = None
    domain: str
    fetch_date: datetime
    error: str | None = None


class QualityResult(BaseModel):
    passed: bool
    reason: str | None = None
