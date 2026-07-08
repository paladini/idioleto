# Project state

## Decisions

- Use Python 3.11+ for local NLP ergonomics and simple packaging.
- Keep the compile workflow offline and free of mandatory model downloads.
- Use Ollama as the only v1 generation adapter.
- Support optional embeddings in the `.idiolect` schema without requiring them.
- Start with lightweight multilingual heuristics for English and Brazilian
  Portuguese friendly corpora.

## Verification commands

- `rtk python -m pytest`
- `rtk python -m ruff check .`
- `rtk python -m idioleto --help`

## Deferred

- llama.cpp adapter
- Local embedding model integration
- More precise passive voice detection per language
