# Governance

`idioleto` is maintained as a small, open-source project with a bias toward
clear standards and local-first user control.

## Maintainer responsibilities

Maintainers are responsible for:

- Reviewing pull requests.
- Protecting the local-first compile workflow.
- Keeping the `.idiolect` schema understandable and versioned.
- Triaging issues and security reports.
- Setting release direction.

## Decision principles

Changes are favored when they:

- Preserve user privacy.
- Improve portability of `.idiolect` files.
- Keep local execution practical.
- Add tests or documentation for public behavior.
- Avoid provider lock-in.

Changes are rejected or deferred when they:

- Require uploading private corpora by default.
- Add heavyweight dependencies without a clear local benefit.
- Make the schema harder to read or validate.
- Break existing profiles without a migration path.
