from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from idioleto.compile.corpus_loader import SUPPORTED_EXTENSIONS, load_corpus
from idioleto.compile.filters import clean_document_text
from idioleto.compile.semantic_anchors import select_semantic_anchors
from idioleto.compile.stylometrics import compute_stylometrics
from idioleto.contracts import DisallowedNgram, IdiolectProfile, SourceSummary
from idioleto.utils.text import tokenize_words


def compile_profile(input_dir: Path, *, language: str = "auto") -> IdiolectProfile:
    documents = load_corpus(input_dir)
    if not documents:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        msg = f"No supported non-empty files found in {input_dir} ({supported})."
        raise ValueError(msg)

    cleaned_docs: list[tuple[Path, str]] = []
    disallowed: list[DisallowedNgram] = []
    for document in documents:
        cleaned_text, document_disallowed = clean_document_text(document.text)
        if cleaned_text:
            cleaned_docs.append((document.path, cleaned_text))
        disallowed.extend(document_disallowed)

    combined_text = "\n\n".join(text for _, text in cleaned_docs)
    if not tokenize_words(combined_text):
        msg = "The corpus did not contain enough finalized prose after filtering."
        raise ValueError(msg)

    unique_disallowed = _dedupe_disallowed(disallowed)
    words = tokenize_words(combined_text)
    profile = IdiolectProfile(
        profile_id=_profile_id_from_output(input_dir),
        created_at=datetime.now(UTC),
        language=_resolve_language(language, combined_text),
        source_summary=SourceSummary(
            file_count=len(documents),
            total_characters=len(combined_text),
            total_words=len(words),
            included_extensions=sorted(
                {document.path.suffix.lower() for document in documents}
            ),
        ),
        stylometrics=compute_stylometrics(combined_text, unique_disallowed),
        semantic_anchors=select_semantic_anchors(cleaned_docs),
    )
    return profile


def _resolve_language(language: str, text: str) -> str:
    if language != "auto":
        return language
    lowered = text.lower()
    pt_markers = sum(
        lowered.count(marker)
        for marker in [" que ", " nao ", " não ", " uma ", " para ", " por "]
    )
    en_markers = sum(
        lowered.count(marker)
        for marker in [" the ", " and ", " that ", " with ", " for "]
    )
    return "pt-BR" if pt_markers > en_markers else "en"


def _profile_id_from_output(input_dir: Path) -> str:
    return input_dir.resolve().name or "idiolect-profile"


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
