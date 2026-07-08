# Contributing to idioleto

Thank you for helping improve `idioleto`.

This project is early, local-first, and format-driven. Contributions are most
valuable when they keep the `.idiolect` standard portable, understandable, and
safe for private writing workflows.

## Development setup

1. Fork and clone the repository.
2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment.
4. Install the package with development dependencies:

   ```bash
   python -m pip install -e ".[dev]"
   ```

5. Run the checks:

   ```bash
   python -m pytest
   python -m ruff check .
   python -m idioleto --help
   ```

## Contribution guidelines

- Keep code and documentation in English.
- Keep corpus compilation local-first and offline by default.
- Do not add mandatory model downloads to the core compile workflow.
- Add or update tests for behavior changes.
- Update `README.md`, `docs/`, or examples when user-facing behavior changes.
- Keep `.idiolect` schema changes backward-aware and document them clearly.

## Pull request checklist

Before opening a pull request, make sure:

- Tests pass with `python -m pytest`.
- Linting passes with `python -m ruff check .`.
- The CLI loads with `python -m idioleto --help`.
- New public behavior is documented.
- The pull request explains why the change matters.

## Good first areas

- More language-specific heuristics that do not require heavyweight models.
- Better low-signal corpus filtering.
- More example corpora and `.idiolect` fixtures.
- Additional local runner adapters.
- Documentation improvements for the file format.
