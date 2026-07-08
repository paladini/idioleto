# idioleto

**Vision:** `idioleto` is a local-first CLI and engine that extracts an
author's idiolect from a private corpus and stores it as a portable `.idiolect`
profile for local LLM generation.

**For:** Writers, developers, researchers, and local-first AI users who want to
reuse their own writing style without uploading private text to hosted services.

**Solves:** Users can preserve and reuse their authorial voice through a
standardized, human-readable style profile.

## Goals

- Compile a valid `.idiolect` profile from Markdown, plain text, and PDF files.
- Generate text through Ollama using a prompt compiled from that profile.
- Keep the compile workflow fully local and independent from remote APIs.

## Tech stack

- Language: Python 3.11+
- CLI: Typer
- Contracts: Pydantic v2
- PDF parsing: pypdf
- Local LLM integration: Ollama HTTP API through httpx
- Tests and linting: pytest and ruff

## Scope

v1 includes:

- `.idiolect` JSON Schema and typed Python contracts
- `idioleto compile`
- `idioleto generate`
- Lightweight multilingual stylometrics
- Optional semantic embeddings field in the file format
- Ollama generation adapter

Explicitly out of scope:

- Hosted LLM providers
- Mandatory embedding model downloads
- Full linguistic parsing with heavyweight NLP models
- llama.cpp adapter implementation
- GUI or web app surfaces

## Constraints

- The codebase and documentation are written in English.
- The project name remains `idioleto`.
- Compilation must work offline with no model downloads.
