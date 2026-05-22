from __future__ import annotations

import logging
import re

from bs4 import BeautifulSoup
from html2text import HTML2Text

logger = logging.getLogger(__name__)

_LANG_PATTERNS = [
    (r"pip |import \w|from \w+ import|def \w+\(|class \w+", "python"),
    (r"sudo |apt |npm |curl |export |chmod |mkdir ", "bash"),
    (r"^[a-z_]+:\s", "yaml"),
    (r"\"\w+\"\s*:", "json"),
    (r"SELECT |INSERT |CREATE TABLE|ALTER TABLE", "sql"),
]


def _build_html2text() -> HTML2Text:
    h = HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0
    h.protect_links = True
    h.unicode_snob = True
    h.images_to_alt = False
    return h


def _detect_lang(code: str) -> str:
    for pattern, lang in _LANG_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
            return lang
    return ""


def _clean_code_blocks(soup: BeautifulSoup) -> None:
    for pre in list(soup.find_all("pre")):
        code_tag = pre.find("code")
        code_text = code_tag.get_text() if code_tag else pre.get_text()
        lang = ""
        if code_tag:
            for cls in code_tag.get("class", []):
                if cls.startswith("language-") or cls.startswith("hljs-"):
                    lang = cls.split("-", 1)[1]
                    break
        if not lang:
            lang = _detect_lang(code_text)
        code_text = code_text.strip()
        code_text = re.sub(r"^```\w*\n?", "", code_text)
        code_text = re.sub(r"\n?```$", "", code_text)
        pre.replace_with(f"\n\n```{lang}\n{code_text}\n```\n\n")


def _process_figures(soup: BeautifulSoup) -> None:
    for figure in list(soup.find_all("figure")):
        img = figure.find("img")
        caption_tag = figure.find("figcaption")
        caption = caption_tag.get_text().strip() if caption_tag else ""
        if img:
            src = img.get("src", "")
            alt = img.get("alt", "") or caption or "image"
            if src:
                figure.replace_with(f"\n\n![{alt}]({src})\n\n")


def _find_body(soup: BeautifulSoup) -> BeautifulSoup:
    body = soup.find("div", class_="entry-content")
    if body:
        return body
    article = soup.find("article")
    if article:
        return article
    return soup.find("main") or soup


def _normalize_html(html: str) -> str:
    html = html.replace('\\"', '"')
    return html


def extract_medium_content(html: str) -> str | None:
    if not html:
        return None

    html = _normalize_html(html)
    soup = BeautifulSoup(html, "html.parser")

    title = None
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text().strip()

    body = _find_body(soup)

    for tag_name in ("nav", "header", "footer", "aside", "style", "script", "noscript"):
        for tag in list(body.find_all(tag_name)):
            tag.decompose()

    chrome_kw = (
        "follow",
        "subscribe",
        "clap",
        "share",
        "response",
        "meter",
        "paywall",
        "promo",
        "sidebar",
        "cookie",
        "consent",
        "tds-cta",
        "member-only",
        "members-only",
    )
    for tag in list(body.find_all(True, attrs={"class": True})):
        if not tag.attrs:
            continue
        cls_str = " ".join(tag.get("class", []))
        if any(kw in cls_str for kw in chrome_kw):
            tag.decompose()

    _process_figures(body)
    _clean_code_blocks(body)

    for img in list(body.find_all("img")):
        src = img.get("src", "")
        alt = img.get("alt", "image")
        if src:
            img.replace_with(f"\n\n![{alt}]({src})\n\n")

    h = _build_html2text()
    md = h.handle(str(body))

    md = re.sub(r"\\n", "\n", md)
    md = re.sub(r"\t", "", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    lines = [line.strip() for line in md.split("\n")]
    md = "\n".join(lines)
    md = re.sub(r"\n{3,}", "\n\n", md)

    md = re.sub(r"^Member-only story\s*\n*", "", md, flags=re.IGNORECASE)

    if title and not md.lstrip().startswith(f"# {title}"):
        md = f"# {title}\n\n{md}"

    return md.strip() or None
