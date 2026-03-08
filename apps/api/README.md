# API

## Intro

FastAPI service with a hexagonal-architecture base. The presentation layer lives in `presentation/` and exposes `/ping` and `/export-content`.

## Requirements

- Python 3.12+
- `uv` (install: https://docs.astral.sh/uv/)

## Run API

```bash
make run
```

## Local Environment Setup

```bash
cd /home/abend/Dev/llm-generator/apps/api
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
```

## Postman

The Postman collection lives in `postman/api.postman_collection.json` and uses a `{{base_url}}` variable with a default of `http://localhost:8000`. You can override `base_url` via a Postman Environment if needed.

## Dependency Management with uv

Add runtime dependencies:

```bash
uv add fastapi
```

Add development dependencies by group:

```bash
uv add --group lint ruff
uv add --group test pytest
uv add --group type mypy
uv add --group hooks pre-commit
```

Install a single group:

```bash
uv sync --group test
```

Install all dev groups:

```bash
uv sync --group dev
```

> Note: the `dev` group includes `lint`, `test`, `type`, and `hooks` via `include-group`.
