.PHONY: format type test all run run-local

all: format type test

run:
	@echo "Starting API with uvicorn..."
	uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

run-local:
	@echo "Starting API with uvicorn (CORS for local web)..."
	CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000" uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

format:
	@echo "Running ruff (imports + lint) and ruff format..."
	uv run ruff check --select I --fix .
	uv run ruff format .

type:
	@echo "Running mypy type check..."
	uv run mypy .

test:
	@echo "Running pytest..."
	uv run pytest
