# Security policy

`idioleto` handles private writing corpora, so privacy and local execution are
core security concerns.

## Supported versions

The project is pre-release. Security fixes target the current `main` branch
until versioned releases begin.

## Reporting a vulnerability

Report security issues privately through GitHub's security advisory workflow
when available. If advisories are not available, contact the repository owner
through GitHub.

Do not open a public issue for vulnerabilities involving:

- Accidental corpus disclosure
- Unsafe file handling
- Prompt injection risks in generated profiles
- Unexpected network access
- Dependency vulnerabilities with practical exploit paths

## Security principles

- Corpus compilation must work without network access.
- Generated `.idiolect` files must avoid storing full private corpora.
- Optional integrations must be explicit and documented.
- Dependencies must stay minimal and justified.
