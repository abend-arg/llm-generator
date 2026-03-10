# API

## Intro

FastAPI service that generates `llms.txt` from a URL. It exposes `/ping` and `/export-content`.

## Architecture

Hexagonal layers:
- `presentation` (router + controllers)
- `application` (services, extractors, renderers)
- `domain` (models and policies)

## Parsing Strategy

- The pipeline tries extractors in order and stops on the first successful one.
- Each extractor decides when it “cannot extract” and raises `CouldNotExtract` to allow fallback.

Current order:
- `LlmsTxtExtractor` (prefers existing `/.well-known/llms.txt` or `/llms.txt`)
- `HtmlExtractor` (fallback)
- `DefaultTitleExtractor` (last resort)

### Flexible llms.txt parsing

The `llms.txt` parsing is intentionally tolerant to non‑standard files:
- Ignores `###` subheaders.
- Keeps non‑link content as `info` (preserving lists and blank lines).
- Drops empty sections.
- Allows mixed content within sections (non‑link lines go to `info`).

### HTML extraction notes

- Summary is selected from containers with headings, with reject keywords to avoid testimonials.
- Useful links are derived from internal anchors and filtered (privacy/login/etc.).
- Policies (thresholds and filters) live in `domain/html_policies.py`.

## Requirements

- Python 3.12+
- `uv` (install:)

```text
https://docs.astral.sh/uv/
```

## Run API

```bash
make run-local
```

OpenAPI docs are available at `/docs` once the API is running.

## Local Environment Setup

```bash
cd apps/api
uv sync --group dev
```

> The `dev` group is only for development tooling. It is not required to run the API.
>
> If you want a minimal environment, you can install specific groups with `--group lint|test|type|hooks`.

## Pre-commit

`pre-commit` runs a defined set of checks automatically before each git commit. This helps catch formatting/lint/type issues early and keeps the codebase consistent across the team.

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## Make Commands

```bash
make                # runs format + type + test
make format         # ruff (imports + lint) + ruff format
make type           # mypy
make test           # pytest
make run            # starts the API with uvicorn
make run-local      # starts the API with CORS for local web
```

## Postman

The Postman collection lives in `postman/api.postman_collection.json` and uses a `{{base_url}}` variable with a default of `http://localhost:8000`. You can override `base_url` via a Postman Environment if needed.

## Dependency Management with uv

Examples:

To add runtime dependencies:

```bash
uv add fastapi
```

Or development dependencies by group:

```bash
uv add --group lint ruff
uv add --group test pytest
uv add --group type mypy
uv add --group hooks pre-commit
```

To install a single group:

```bash
uv sync --group test
```

To install all dev groups:

```bash
uv sync --group dev
```

> Note: the `dev` group includes `lint`, `test`, `type`, and `hooks` via `include-group`.

## Future Work

- Tests (unit/integration) to validate extractors and renderers against real sites.
- Structured logging and metrics for production visibility.
- Extractor for JS-heavy pages (SPAs) using a headless browser (e.g., Playwright) as fallback.
- Alternative pipeline: extract human-readable text and use an LLM integration to draft `llms.txt`.
