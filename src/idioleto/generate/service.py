from __future__ import annotations

from idioleto.compiler import compile_system_prompt
from idioleto.contracts import IdiolectProfile
from idioleto.generate.adapters import GenerationAdapter


def generate_text(
    profile: IdiolectProfile,
    *,
    prompt: str,
    model: str,
    adapter: GenerationAdapter,
) -> str:
    system_prompt = compile_system_prompt(profile)
    return adapter.generate(
        model=model,
        system_prompt=system_prompt,
        user_prompt=prompt,
    )
