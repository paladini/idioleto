from __future__ import annotations

import re

from idioleto.contracts import DisallowedNgram, Stylometrics
from idioleto.utils.text import split_sentences, tokenize_words

PUNCTUATION_RE = re.compile(r"[.,;:!?()\[\]{}\"']")
PASSIVE_EN_RE = re.compile(
    r"\b(am|is|are|was|were|be|been|being)\s+\w+(ed|en)\b",
    re.IGNORECASE,
)
PASSIVE_PT_RE = re.compile(
    r"\b(foi|foram|era|eram|será|serao|serão|sendo)\s+\w+(ado|ada|ados|adas|ido|ida|idos|idas)\b",
    re.IGNORECASE,
)


def compute_stylometrics(
    text: str, disallowed_ngrams: list[DisallowedNgram] | None = None
) -> Stylometrics:
    words = tokenize_words(text)
    sentences = split_sentences(text)
    sentence_count = max(1, len(sentences))
    word_count = len(words)
    unique_words = len(set(words))
    punctuation_count = len(PUNCTUATION_RE.findall(text))
    passive_count = sum(1 for sentence in sentences if _looks_passive(sentence))

    return Stylometrics(
        average_sentence_length=round(word_count / sentence_count, 2)
        if word_count
        else 0,
        type_token_ratio=round(unique_words / word_count, 4) if word_count else 0,
        punctuation_density=round((punctuation_count / word_count) * 100, 2)
        if word_count
        else 0,
        passive_voice_ratio=round(passive_count / sentence_count, 4)
        if sentences
        else 0,
        disallowed_ngrams=disallowed_ngrams or [],
    )


def _looks_passive(sentence: str) -> bool:
    return bool(PASSIVE_EN_RE.search(sentence) or PASSIVE_PT_RE.search(sentence))

