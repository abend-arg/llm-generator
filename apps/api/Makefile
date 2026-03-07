.PHONY: format type test all run

all: format type test

run:
	@echo "Starting API with uvicorn..."
	uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

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
