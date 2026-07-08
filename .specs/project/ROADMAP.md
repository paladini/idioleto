# Roadmap

**Current milestone:** v1 local-first vertical slice
**Status:** In Progress

## v1 local-first vertical slice

**Goal:** Ship a usable CLI that compiles a corpus into `.idiolect` and uses it
with Ollama for local text generation.

### Features

**Project foundation** - COMPLETE

- Python package structure
- README, license, and packaging metadata
- Spec-driven project notes

**Data contracts and schema** - COMPLETE

- Pydantic models
- JSON Schema
- Sample fixture

**Prompt compiler** - COMPLETE

- Map quantitative metrics to style instructions
- Include semantic anchors
- Include disallowed n-gram constraints

**Corpus compiler** - COMPLETE

- Markdown, text, and PDF loading
- Low-signal filtering
- Lightweight stylometrics
- Semantic anchor selection

**Ollama generation** - COMPLETE

- Local Ollama HTTP adapter
- CLI generation command
- stdout and file output modes

## Future considerations

- llama.cpp adapter
- Optional local embedding generation
- Stronger language-specific NLP modules
- Public schema documentation site
- Golden-corpus benchmark suite
