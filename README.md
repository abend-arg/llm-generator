# llm-generator

Project to generate `llms.txt` files from a URL, with a backend API and a web frontend.

## Description

The system takes a URL, attempts to fetch an existing `llms.txt`, and if not available, extracts content from HTML to build a `llms.txt` with useful sections. It is designed to be extensible with multiple extractors and renderers.

## Tech Stack

- Backend: FastAPI (Python 3.12+)
- Frontend: Next.js (React)
- HTML parsing: BeautifulSoup + httpx
- Validation: Pydantic

## Requirements

- Python 3.12+
- Node.js 18+ (recommended)
- `uv` for the backend
- npm/pnpm/yarn/bun for the frontend

## Run Local

From the repo root:

```bash
make run-local
```

This starts:
- API (`apps/api`) with local CORS
- Web (`apps/web`) in dev mode

## More Info

- API details (architecture, parsing): `apps/api/README.md`
- Web details: `apps/web/README.md`

Both READMEs include a **Future Work** section for follow‑ups and production hardening ideas.
