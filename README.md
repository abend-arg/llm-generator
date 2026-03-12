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
- npm for the frontend

## Run Local

From the repo root:

```bash
make run-local
```

This starts:
- API (`apps/api`) with local CORS
- Web (`apps/web`) in dev mode

## Test URLs

Sample URLs to validate each extraction strategy and compare results:

LLMS (existing `llms.txt` files):
- https://listdefender.com
- https://tagit.video
- https://mailchimp.com
- https://www.tryprofound.com/

HTML (single-page extraction should be sufficient):
- https://buenbit.com/
- https://www.ryomacorp.com/
- https://www.canals.ai/
- https://www.luxerone.com/

CRAWLER (multi-page crawl for richer context):
- https://www.monks.com/
- https://www.hostinger.com

## More Info

- API details (architecture, parsing): `apps/api/README.md`
- Web details: `apps/web/README.md`

Both READMEs include a **Future Work** section for follow‑ups and production hardening ideas.
