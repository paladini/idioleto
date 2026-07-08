from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCHEMA_VERSION = "0.1.0"

NgramReason = Literal[
    "future_intent",
    "boilerplate",
    "metadata",
    "citation_artifact",
    "low_signal",
]

AnchorKind = Literal[
    "philosophy",
    "memory",
    "worldview",
    "preference",
    "argument_pattern",
    "self_description",
]

SupportedExtension = Literal[".md", ".txt", ".pdf"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DisallowedNgram(StrictModel):
    ngram: str = Field(min_length=1)
    n: int = Field(ge=1)
    reason: NgramReason


class Stylometrics(StrictModel):
    average_sentence_length: float = Field(ge=0)
    type_token_ratio: float = Field(ge=0, le=1)
    punctuation_density: float = Field(ge=0)
    passive_voice_ratio: float = Field(ge=0, le=1)
    disallowed_ngrams: list[DisallowedNgram] = Field(default_factory=list)


class SourceLocation(StrictModel):
    file: str | None = None
    location: str | None = None


class SemanticAnchor(StrictModel):
    id: str = Field(min_length=1)
    kind: AnchorKind
    snippet: str = Field(min_length=1, max_length=1200)
    embedding: list[float] | None = None
    embedding_model: str | None = None
    source: SourceLocation | None = None

    @model_validator(mode="after")
    def require_model_for_embedding(self) -> SemanticAnchor:
        if self.embedding is not None and not self.embedding_model:
            msg = "embedding_model is required when embedding is present"
            raise ValueError(msg)
        return self


class SourceSummary(StrictModel):
    file_count: int = Field(ge=0)
    total_characters: int = Field(ge=0)
    total_words: int = Field(ge=0)
    included_extensions: list[SupportedExtension]


class IdiolectProfile(StrictModel):
    schema_version: Literal["0.1.0"] = SCHEMA_VERSION
    profile_id: str = Field(min_length=1)
    created_at: datetime
    language: str = Field(min_length=2)
    source_summary: SourceSummary
    stylometrics: Stylometrics
    semantic_anchors: list[SemanticAnchor] = Field(default_factory=list)

