from __future__ import annotations

import re

from idioleto.contracts import DisallowedNgram
from idioleto.utils.text import normalize_whitespace

FUTURE_INTENT_PATTERNS = [
    re.compile(r"\bbooks?\s+to\s+read\b", re.IGNORECASE),
    re.compile(r"\bto\s+read\b", re.IGNORECASE),
    re.compile(r"\btodo\b", re.IGNORECASE),
    re.compile(r"\bto\s+do\b", re.IGNORECASE),
    re.compile(r"\bideas?\s+for\s+later\b", re.IGNORECASE),
    re.compile(r"\breading\s+list\b", re.IGNORECASE),
]

METADATA_PATTERNS = [
    re.compile(r"^---$"),
    re.compile(r"^\s*(title|date|tags|author|draft|slug):\s*.+$", re.IGNORECASE),
    re.compile(r"^\s*#+\s*$"),
]

BOILERPLATE_PATTERNS = [
    re.compile(r"^\s*table\s+of\s+contents\s*$", re.IGNORECASE),
    re.compile(r"^\s*copyright\b", re.IGNORECASE),
]


def clean_document_text(text: str) -> tuple[str, list[DisallowedNgram]]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    cleaned: list[str] = []
    disallowed: list[DisallowedNgram] = []
    in_front_matter = False

    for index, line in enumerate(lines):
        stripped = line.strip()
        if index == 0 and stripped == "---":
            in_front_matter = True
            disallowed.append(
                DisallowedNgram(ngram="front matter", n=2, reason="metadata")
            )
            continue
        if in_front_matter:
            if stripped == "---":
                in_front_matter = False
            continue

        lowered_line = stripped.lower()
        future_match = _first_match(FUTURE_INTENT_PATTERNS, stripped)
        if future_match:
            disallowed.append(
                DisallowedNgram(
                    ngram=normalize_whitespace(future_match.group(0).lower()),
                    n=len(future_match.group(0).split()),
                    reason="future_intent",
                )
            )
            continue
        if lowered_line.startswith(("- [ ]", "* [ ]", "- todo", "* todo")):
            disallowed.append(
                DisallowedNgram(ngram="todo", n=1, reason="future_intent")
            )
            continue
        if _matches_any(METADATA_PATTERNS, stripped):
            disallowed.append(
                DisallowedNgram(
                    ngram=stripped[:80] or "metadata",
                    n=1,
                    reason="metadata",
                )
            )
            continue
        if _matches_any(BOILERPLATE_PATTERNS, stripped):
            disallowed.append(
                DisallowedNgram(
                    ngram=stripped[:80],
                    n=max(1, len(stripped.split())),
                    reason="boilerplate",
                )
            )
            continue
        cleaned.append(line)

    return normalize_whitespace("\n".join(cleaned)), _dedupe_disallowed(disallowed)


def _first_match(patterns: list[re.Pattern[str]], text: str) -> re.Match[str] | None:
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            return match
    return None


def _matches_any(patterns: list[re.Pattern[str]], text: str) -> bool:
    return any(pattern.search(text) for pattern in patterns)


def _dedupe_disallowed(items: list[DisallowedNgram]) -> list[DisallowedNgram]:
    seen: set[tuple[str, str]] = set()
    deduped: list[DisallowedNgram] = []
    for item in items:
        key = (item.ngram.lower(), item.reason)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped[:50]
