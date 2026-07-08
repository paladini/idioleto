from __future__ import annotations

from pathlib import Path

from idioleto.compiler import compile_system_prompt
from idioleto.contracts import IdiolectProfile

FIXTURE = Path(__file__).parent / "fixtures" / "sample.idiolect"


def test_prompt_maps_long_sentences_to_style_instruction() -> None:
    profile = IdiolectProfile.model_validate_json(FIXTURE.read_text(encoding="utf-8"))

    prompt = compile_system_prompt(profile)

    assert "writes long, layered sentences" in prompt
    assert "uses a varied vocabulary" in prompt
    assert "'books to read' (future_intent)" in prompt


def test_prompt_includes_semantic_anchors_with_limit() -> None:
    profile = IdiolectProfile.model_validate_json(FIXTURE.read_text(encoding="utf-8"))

    prompt = compile_system_prompt(profile, max_anchor_chars=220)

    assert "Semantic anchors to preserve:" in prompt
    assert "I believe useful software" in prompt
    assert len(prompt) < 1600

