# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`error-manager` is a Python library for managing error codes, descriptions, and data in a unified way throughout a project. Published on PyPI as `error-manager`. No runtime dependencies.

## Tooling

- **Package manager:** `uv`
- **Configuration:** `pyproject.toml` (metadata + tool config), `tox.ini` (tox envs + coverage)
- **Task runner:** `just` (imports shared Justfile from `dg_justfile/`)

## Commands

### Testing
```bash
just test                    # Run tests via justfile (uv sync + uv run pytest)
uv run pytest                # Run tests directly
uv run pytest tests/test_errors.py  # Run a single test file
uv run pytest -k "test_name"        # Run a specific test
uv run tox                   # Run all tox environments (py310-py314)
uv run tox -e py312          # Run tests on specific Python version
just tox                     # Run tox via justfile
```

### Type Checking
```bash
uv run tox -e typecheck      # mypy with --ignore-missing-imports
```

### Documentation
```bash
uv run tox -e docs           # Build Sphinx docs to docs/_build/
```

### Dependency Management
```bash
uv sync --extra dev          # Install project + dev dependencies
uv lock                      # Update lock file
```

## Architecture

Source layout: `src/errors/`, tests in `tests/`.

### Core Components

- **`ErrorCode`** (`base.py`): Frozen dataclass (`code`, `description`, `error_data`). The fundamental error object.
- **`FunctionalErrorsBaseClass`** (`base.py`): Enum subclass for grouping related errors by domain. Each member's value is an `ErrorCode`.
- **`ListErrors`** (`error.py`): Singleton registry. Error enumerators register themselves here on import. Provides global `error_description()` and `error_object()` lookups by code string.
- **`ErrorListByMixin`** (`mixin.py`): Alternative to `ListErrors` using mixin inheritance for better type checking and IDE autocompletion.
- **`ReturnValueWithStatus[T]`** (`data_classes.py`): Generic dataclass for returning a result with validity status and accumulated errors. `ReturnValueWithErrorStatus` is a factory for creating pre-errored instances.
- **`is_error()`, `add_error_data()`** (`base.py`): Utility functions for checking error types and attaching context data to immutable error codes.

### Key Pattern

Error enumerators subclass `FunctionalErrorsBaseClass`, define members as `ErrorCode` instances, and auto-register with the `ListErrors` singleton on class creation. This enables global error lookup by code string across the project.

## Git Conventions

- Branch naming: `DGEM-<story nr>-<short-description>` (e.g. `DGEM-1-new-package-setup-with-claude-and-uv`)

## CI/CD

GitHub Actions workflow (`.github/workflows/main.yml`) runs on every push:
- **Format** — `ruff format --check` (direct, no tox)
- **Lint** — `ruff check` (direct, no tox)
- **Type check** — `tox -e typecheck` (mypy)
- **Test** — tox matrix for Python 3.12, 3.13, 3.14
- **Build** — source distribution + wheel
- **Publish** — PyPI via Trusted Publishing (on version tags `v*`), environment: `pypi_releasing`

## Code Style

- Ruff for linting and formatting (line length 88)
- Lint rules: C (mccabe), F (pyflakes), E/W (pycodestyle), B (bugbear), I (isort)
- mypy with `check_untyped_defs = True`
