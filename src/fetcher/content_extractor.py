from __future__ import annotations

import trafilatura


def extract_content(html: str, url: str) -> str | None:
    if not html:
        return None
    return trafilatura.extract(html, output_format="markdown", include_images=True)
