# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pyEnsemblRest is a Python client library for the Ensembl REST API. It provides a dynamic, Pythonic interface to all Ensembl REST endpoints without requiring explicit method definitions. The library handles rate limiting (15 requests/second), retry logic, and various response formats.

## Development Commands

### Setup
```bash
# Install dependencies
make install
# Or with Poetry directly
poetry install --sync
```

### Testing
```bash
# Run unit tests (excludes live API tests)
make unit-test
# Or
poetry run pytest -v -m "not live"

# Run all tests with coverage (used in CI)
make ci-test
# Or
poetry run pytest -v --cov=pyensemblrest --cov-report lcov:./tests/lcov.info tests/

# Upload coverage to Coveralls
make coverage
```

### Code Quality
```bash
# Type checking
make type-check
# Or
poetry run mypy . --no-incremental

# Linting
make lint
# Or
poetry run ruff check . --fix

# Formatting
make format
# Or
poetry run ruff format .

# Run all pre-commit hooks (except tests)
SKIP=unit-test poetry run pre-commit run --all-files
```

### Dependency Management
```bash
# Update lock file
make freeze
# Or
poetry lock
```

## Architecture

### Dynamic Method Registration

The library uses a dynamic method registration system rather than hard-coded methods. All REST API endpoints are defined in `pyensemblrest/ensembl_config.py` in the `ensembl_api_table` dictionary. Each entry specifies:
- `url`: URL template with `{{parameter}}` placeholders
- `method`: HTTP method (GET or POST)
- `content_type`: Default content type
- `post_parameters`: List of parameters passed in POST body (for POST methods)
- `doc`: Documentation string

When `EnsemblRest` is instantiated, `__add_methods()` dynamically adds methods to the instance based on `ensembl_api_table`. This allows the library to support all Ensembl REST endpoints without explicit method definitions.

### Request Flow

1. User calls a dynamic method (e.g., `ensRest.getSequenceById(id='ENSG00000157764')`)
2. `call_api_func()` validates mandatory parameters from URL template
3. URL is constructed by replacing `{{parameter}}` placeholders
4. `__get_response()` handles rate limiting and executes the request
5. `parseResponse()` processes the response and handles retries if needed

### Rate Limiting and Retry Logic

The library implements automatic rate limiting (15 requests/second) in `__get_response()`:
- Tracks request count and timing
- Sleeps if rate limit would be exceeded
- Reads rate limit headers from Ensembl API responses

Retry logic in `__retry_request()` handles:
- Ensembl known errors (defined in `ensembl_known_errors`)
- HTTP 500 errors (Ensembl sometimes returns 500 on valid requests)
- Timeouts
- Up to `max_attempts` (default 5) with exponential backoff

### Exception Hierarchy

- `EnsemblRestError`: Base exception for all REST API errors
- `EnsemblRestRateLimitError`: Raised on HTTP 429 (rate limit hit)
- `EnsemblRestServiceUnavailable`: Raised on connection errors

### Key Files

- `pyensemblrest/ensemblrest.py`: Main `EnsemblRest` class with dynamic method registration
- `pyensemblrest/ensembl_config.py`: API endpoint definitions, HTTP status codes, configuration
- `pyensemblrest/exceptions.py`: Custom exception classes
- `pyensemblrest/__init__.py`: Package exports and version metadata

## Testing Notes

The test suite uses pytest markers:
- `@pytest.mark.live`: Tests that call the live Ensembl REST API
- By default, `make unit-test` excludes live tests with `-m "not live"`
- CI runs all tests including live API calls

## Version Management

This project uses `poetry-dynamic-versioning` to automatically set the version from git tags. The version in `pyproject.toml` is set to `0.0.0` as a placeholder and is replaced at build time with the git tag version.

## Type Checking

mypy is configured with strict mode in `pyproject.toml`. The `tests/` directory and `examples.py` are excluded from type checking.

## Code Style

The project uses Ruff for both linting and formatting with:
- Line length: 88 characters
- Selected rules: E4, E7, E9, F, I (import sorting)
- Configured in `[tool.ruff]` section of `pyproject.toml`
