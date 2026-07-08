from __future__ import annotations

import re

WORD_RE = re.compile(r"[^\W\d_]+(?:['-][^\W\d_]+)?", re.UNICODE)
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def tokenize_words(text: str) -> list[str]:
    return [match.group(0).lower() for match in WORD_RE.finditer(text)]


def split_sentences(text: str) -> list[str]:
    candidates = SENTENCE_RE.split(normalize_whitespace(text))
    return [sentence.strip() for sentence in candidates if sentence.strip()]


def sentence_word_count(sentence: str) -> int:
    return len(tokenize_words(sentence))

