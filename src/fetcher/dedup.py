from __future__ import annotations

import hashlib
from pathlib import Path


def _stable_hash(s: str) -> int:
    return int.from_bytes(hashlib.md5(s.encode("utf-8")).digest()[:8], "little")


def minhash(text: str, num_perm: int = 128) -> set[int]:
    if not text:
        return set()

    content = text.strip()[:8192]
    shingles = [content[i : i + 4] for i in range(max(len(content) - 3, 0))]
    if not shingles:
        return set()

    hashes = {_stable_hash(s) for s in shingles}
    return set(sorted(hashes)[:num_perm])


def jaccard_similarity(a: set[int], b: set[int]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


class DedupIndex:
    def __init__(self, output_path: Path, threshold: float = 0.85):
        import yaml

        self._threshold = threshold
        self._index: dict[str, dict[str, set[int]]] = {}

        if not output_path.exists():
            return

        for domain_dir in output_path.iterdir():
            if not domain_dir.is_dir():
                continue
            domain = domain_dir.name
            self._index[domain] = {}
            for fp in domain_dir.glob("*.md"):
                text = fp.read_text(encoding="utf-8")
                if not text.startswith("---"):
                    continue
                end = text.find("---", 3)
                if end == -1:
                    continue
                meta = yaml.safe_load(text[3:end])
                if meta.get("status") != "ok":
                    continue
                body = text[end + 3 :].strip()
                if body:
                    self._index[domain][fp.name] = minhash(body)

    def check(self, domain: str, content: str) -> str | None:
        domain_index = self._index.get(domain)
        if not domain_index or not content:
            return None

        sig = minhash(content)
        for filename, existing_sig in domain_index.items():
            if jaccard_similarity(sig, existing_sig) >= self._threshold:
                return filename
        return None

    def add(self, domain: str, filename: str, content: str) -> None:
        if not content:
            return
        self._index.setdefault(domain, {})[filename] = minhash(content)
