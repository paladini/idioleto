from __future__ import annotations

from pathlib import Path

import pytest

from idioleto.compile import corpus_loader
from idioleto.compile.service import compile_profile
from idioleto.contracts import IdiolectProfile


def test_compile_profile_reads_supported_files_and_filters_future_intents(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "note.md").write_text(
        """---
title: Draft
---

I believe writing tools should preserve the user voice.
I prefer calm software because it lets people think.

Books to read:
- [ ] Something later
""",
        encoding="utf-8",
    )
    (corpus / "essay.txt").write_text(
        "When I write, I want every sentence to earn its place. "
        "The world needs tools that respect private memory.",
        encoding="utf-8",
    )
    (corpus / "scan.pdf").write_text("not a real pdf", encoding="utf-8")
    (corpus / "ignore.csv").write_text("not supported", encoding="utf-8")

    monkeypatch.setattr(
        corpus_loader,
        "_read_pdf",
        lambda path: "I remember a moment when local software felt trustworthy.",
    )

    profile = compile_profile(corpus, language="auto")
    payload = profile.model_dump_json()
    reloaded = IdiolectProfile.model_validate_json(payload)

    assert reloaded.source_summary.file_count == 3
    assert sorted(reloaded.source_summary.included_extensions) == [
        ".md",
        ".pdf",
        ".txt",
    ]
    assert reloaded.language == "en"
    assert reloaded.stylometrics.average_sentence_length > 0
    assert any(
        item.ngram == "books to read" and item.reason == "future_intent"
        for item in reloaded.stylometrics.disallowed_ngrams
    )
    assert reloaded.semantic_anchors


def test_compile_profile_errors_on_empty_supported_corpus(tmp_path: Path) -> None:
    corpus = tmp_path / "empty"
    corpus.mkdir()
    (corpus / "empty.md").write_text("", encoding="utf-8")
    (corpus / "ignored.csv").write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError, match="No supported non-empty files"):
        compile_profile(corpus)
