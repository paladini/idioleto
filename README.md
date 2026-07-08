# idioleto

[![CI](https://github.com/paladini/idioleto/actions/workflows/ci.yml/badge.svg)](https://github.com/paladini/idioleto/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)

`idioleto` is a local-first CLI tool and engine for extracting a person's
authorial style from a raw text corpus and storing it as a portable `.idiolect`
profile.

The goal is simple: help local language models write in a user's own style
without sending private writing to a hosted service.

## Why idioleto?

`idioleto` is the Brazilian Portuguese word for "idiolect": the unique way a
person uses language.

The project uses the Brazilian Portuguese name to honor its roots while keeping
a distinct identity in the open-source landscape. The file format remains
`.idiolect`, because the standard must be immediately understandable across
languages, but the tool itself is named `idioleto`.

## What it does

`idioleto` turns a folder of writing into a structured authorial profile.

It extracts two layers:

- `stylometrics`: quantitative writing markers such as average sentence length,
  lexical diversity, punctuation density, passive voice ratio, and disallowed
  n-grams.
- `semantic_anchors`: short, high-signal snippets that represent the author's
  philosophy, memories, worldview, preferences, and recurring argument
  patterns.

The generated `.idiolect` file can then build a dynamic system prompt for a
local language model runner such as Ollama.

## Install for development

Clone the repository, create a virtual environment, and install the package:

```bash
git clone https://github.com/your-name/idioleto.git
cd idioleto
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
git clone https://github.com/your-name/idioleto.git
cd idioleto
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Compile a profile

Run `compile` against a folder containing Markdown, plain text, or PDF files:

```bash
idioleto compile --input ./examples/corpus --output ./examples/sample.idiolect
```

The compiler reads supported files, filters low-signal text, computes
stylometric markers, selects semantic anchors, and writes a validated
`.idiolect` JSON profile.

Supported input formats:

- Markdown: `.md`
- Plain text: `.txt`
- PDF: `.pdf`

## Generate text

Run `generate` with a profile, instruction, and local Ollama model:

```bash
idioleto generate \
  --profile ./examples/sample.idiolect \
  --prompt "Write a short note about local-first software." \
  --model llama3
```

By default, the generated text is printed to stdout. To write it to a file, use
`--output`:

```bash
idioleto generate \
  --profile ./examples/sample.idiolect \
  --prompt "Write a short note about local-first software." \
  --model llama3 \
  --output ./draft.txt
```

## The `.idiolect` format

A `.idiolect` file is a UTF-8 JSON document with this top-level shape:

```json
{
  "schema_version": "0.1.0",
  "profile_id": "sample",
  "created_at": "2026-07-07T12:00:00Z",
  "language": "en",
  "source_summary": {
    "file_count": 1,
    "total_characters": 2000,
    "total_words": 350,
    "included_extensions": [".md"]
  },
  "stylometrics": {
    "average_sentence_length": 22.4,
    "type_token_ratio": 0.48,
    "punctuation_density": 14.2,
    "passive_voice_ratio": 0.08,
    "disallowed_ngrams": []
  },
  "semantic_anchors": []
}
```

The complete JSON Schema lives at
`src/idioleto/schema/idiolect.schema.json`.

Read the schema guide in `docs/schema.md`.

## Local-first by design

`idioleto` is intended to run locally.

Your corpus can contain personal notes, drafts, essays, comments, journals, or
other sensitive writing. The core compile workflow does not require uploading
this material to a hosted API.

The v1 generation workflow uses Ollama over its local HTTP API. Future adapters
can add support for other local runners without changing the `.idiolect` file
format.

## Development

Run the test suite:

```bash
python -m pytest
```

Run lint checks:

```bash
python -m ruff check .
```

Run the CLI help:

```bash
python -m idioleto --help
```

## Community

`idioleto` is designed to grow as an open standard and a practical local-first
tool. The project welcomes issues, design discussion, tests, adapters, language
heuristics, and documentation improvements.

Before contributing, read:

- `CONTRIBUTING.md` for setup, workflow, and pull request expectations
- `CODE_OF_CONDUCT.md` for community standards
- `SECURITY.md` for responsible vulnerability reporting
- `SUPPORT.md` for where to ask questions

## Project status

This project is in early development. The current focus is a small, reliable
local-first vertical slice:

- A documented `.idiolect` schema
- Typed Python data contracts
- A working corpus compiler
- A prompt compiler
- Ollama-backed local generation

## License

MIT
