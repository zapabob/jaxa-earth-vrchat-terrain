# 2026-05-27 Dependabot lock refresh - Codex

## Goal

Resolve open Dependabot alerts in `uv.lock` while keeping the JAXA terrain pipeline source unchanged.

## Changes

- Refreshed vulnerable locked Python packages including `black`, `cryptography`, `GitPython`, `idna`, `pillow`, `protobuf`, `pygments`, `PyJWT`, `pytest`, `python-dotenv`, `python-multipart`, `requests`, `streamlit`, and `urllib3`.
- Accepted resolver changes that remove `tornado` and add current `streamlit` runtime dependencies.

## Verification

- `uv lock --check`: passed.
- `uv lock --dry-run`: no lockfile changes detected.
- Python AST parse of repository Python files: passed.
- `uv run --with pytest pytest -q --version`: resolved `pytest 9.0.3`.
- `uv tree` confirmed patched locked versions for `pillow`, `cryptography`, `streamlit`, `urllib3`, `PyJWT`, and `Pygments`.
