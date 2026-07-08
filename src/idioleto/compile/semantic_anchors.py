from __future__ import annotations

import hashlib
import re
from pathlib import Path

from idioleto.contracts import SemanticAnchor, SourceLocation
from idioleto.utils.text import (
    normalize_whitespace,
    sentence_word_count,
    split_sentences,
)

ANCHOR_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("self_description", re.compile(r"\b(i am|i'm|eu sou|me considero)\b", re.I)),
    ("philosophy", re.compile(r"\b(i believe|acredito|creio|penso que)\b", re.I)),
    ("preference", re.compile(r"\b(i prefer|prefiro|i like|gosto de)\b", re.I)),
    ("memory", re.compile(r"\b(i remember|lembro|quando eu|when i)\b", re.I)),
    ("worldview", re.compile(r"\b(the world|society|o mundo|a sociedade)\b", re.I)),
    ("argument_pattern", re.compile(r"\b(because|therefore|por isso|porque)\b", re.I)),
]


def select_semantic_anchors(
    documents: list[tuple[Path, str]], *, max_anchors: int = 12
) -> list[SemanticAnchor]:
    candidates: list[tuple[int, SemanticAnchor]] = []
    for path, text in documents:
        for index, sentence in enumerate(split_sentences(text)):
            normalized = normalize_whitespace(sentence)
            words = sentence_word_count(normalized)
            if words < 8 or words > 90:
                continue
            kind, pattern_score = _classify_anchor(normalized)
            if not kind:
                continue
            score = pattern_score + min(words, 40)
            anchor_id = _anchor_id(path, index, normalized)
            candidates.append(
                (
                    score,
                    SemanticAnchor(
                        id=anchor_id,
                        kind=kind,
                        snippet=normalized[:1200],
                        source=SourceLocation(
                            file=str(path),
                            location=f"sentence:{index + 1}",
                        ),
                    ),
                )
            )

    candidates.sort(key=lambda item: item[0], reverse=True)
    anchors: list[SemanticAnchor] = []
    seen_snippets: set[str] = set()
    for _, anchor in candidates:
        key = anchor.snippet.lower()
        if key in seen_snippets:
            continue
        seen_snippets.add(key)
        anchors.append(anchor)
        if len(anchors) >= max_anchors:
            break
    return anchors


def _classify_anchor(sentence: str) -> tuple[str | None, int]:
    for kind, pattern in ANCHOR_PATTERNS:
        if pattern.search(sentence):
            return kind, 40
    return None, 0


def _anchor_id(path: Path, index: int, snippet: str) -> str:
    digest = hashlib.sha1(f"{path}:{index}:{snippet}".encode()).hexdigest()
    return f"anchor-{digest[:12]}"
