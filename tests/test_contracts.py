from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from idioleto.contracts import IdiolectProfile

FIXTURE = Path(__file__).parent / "fixtures" / "sample.idiolect"


def test_valid_profile_loads() -> None:
    profile = IdiolectProfile.model_validate_json(FIXTURE.read_text(encoding="utf-8"))

    assert profile.schema_version == "0.1.0"
    assert profile.stylometrics.type_token_ratio == 0.72
    assert profile.semantic_anchors[0].kind == "philosophy"


def test_missing_required_field_fails() -> None:
    data = IdiolectProfile.model_validate_json(FIXTURE.read_text(encoding="utf-8"))
    payload = data.model_dump(mode="json")
    del payload["source_summary"]

    with pytest.raises(ValidationError):
        IdiolectProfile.model_validate(payload)


def test_type_token_ratio_must_be_between_zero_and_one() -> None:
    data = IdiolectProfile.model_validate_json(FIXTURE.read_text(encoding="utf-8"))
    payload = data.model_dump(mode="json")
    payload["stylometrics"]["type_token_ratio"] = 1.5

    with pytest.raises(ValidationError):
        IdiolectProfile.model_validate(payload)


def test_embedding_requires_embedding_model() -> None:
    data = IdiolectProfile.model_validate_json(FIXTURE.read_text(encoding="utf-8"))
    payload = data.model_dump(mode="json")
    payload["semantic_anchors"][0]["embedding"] = [0.1, 0.2]

    with pytest.raises(ValidationError):
        IdiolectProfile.model_validate(payload)

