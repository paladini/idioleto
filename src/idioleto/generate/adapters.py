from __future__ import annotations

from typing import Protocol


class GenerationAdapter(Protocol):
    def generate(self, *, model: str, system_prompt: str, user_prompt: str) -> str:
        """Generate text using a local model runner."""

