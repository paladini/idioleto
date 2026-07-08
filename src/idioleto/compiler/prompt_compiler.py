from __future__ import annotations

from collections import defaultdict

from idioleto.contracts import IdiolectProfile


def compile_system_prompt(
    profile: IdiolectProfile, *, max_anchor_chars: int = 2400
) -> str:
    """Map an idiolect profile into a concise local LLM system prompt."""
    metrics = profile.stylometrics
    sections = [
        "You are a local writing assistant that imitates an author's style.",
        "Preserve the user's requested topic and intent while matching the profile.",
        "",
        "Style profile:",
        f"- Sentence rhythm: {_sentence_length_label(metrics.average_sentence_length)}",
        f"- Vocabulary range: {_ttr_label(metrics.type_token_ratio)}",
        f"- Punctuation habits: {_punctuation_label(metrics.punctuation_density)}",
        f"- Passive voice tendency: {_passive_label(metrics.passive_voice_ratio)}",
    ]

    if metrics.disallowed_ngrams:
        sections.extend(["", "Avoid these corpus artifacts and boilerplate phrases:"])
        for item in metrics.disallowed_ngrams[:20]:
            sections.append(f"- {item.ngram!r} ({item.reason})")

    anchors = _format_anchors(profile, max_anchor_chars=max_anchor_chars)
    if anchors:
        sections.extend(["", "Semantic anchors to preserve:", anchors])

    sections.extend(
        [
            "",
            "Generation rules:",
            "- Do not mention that you are imitating a style.",
            "- Do not quote the profile unless the user explicitly asks for quotes.",
            "- Prefer the profile's cadence, epistemic stance, and recurring concerns.",
            "- Avoid unsupported personal claims not grounded in the profile.",
        ]
    )
    return "\n".join(sections)


def _sentence_length_label(value: float) -> str:
    if value >= 25:
        return "writes long, layered sentences with room for qualification"
    if value <= 12:
        return "writes short, direct sentences with compact transitions"
    return "mixes concise and moderately developed sentences"


def _ttr_label(value: float) -> str:
    if value >= 0.6:
        return "uses a varied vocabulary and avoids repetitive phrasing"
    if value <= 0.35:
        return "uses a stable, recurring vocabulary with familiar terms"
    return "uses moderate lexical variation"


def _punctuation_label(value: float) -> str:
    if value >= 18:
        return "uses punctuation frequently for rhythm, emphasis, and structure"
    if value <= 7:
        return "uses sparse punctuation and simple sentence boundaries"
    return "uses balanced punctuation"


def _passive_label(value: float) -> str:
    if value >= 0.25:
        return "often uses passive constructions and process-focused phrasing"
    if value <= 0.08:
        return "strongly favors active voice"
    return "uses passive voice occasionally"


def _format_anchors(profile: IdiolectProfile, *, max_anchor_chars: int) -> str:
    grouped: dict[str, list[str]] = defaultdict(list)
    for anchor in profile.semantic_anchors:
        grouped[anchor.kind].append(anchor.snippet.strip())

    lines: list[str] = []
    used_chars = 0
    for kind in sorted(grouped):
        header = f"{kind.replace('_', ' ').title()}:"
        if used_chars + len(header) > max_anchor_chars:
            break
        lines.append(header)
        used_chars += len(header)
        for snippet in grouped[kind]:
            normalized = " ".join(snippet.split())
            line = f"- {normalized}"
            if used_chars + len(line) > max_anchor_chars:
                return "\n".join(lines)
            lines.append(line)
            used_chars += len(line)
    return "\n".join(lines)
