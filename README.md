# llm-generator

Minimal project to generate `llms.txt` files from a URL.

## Overview

- `apps/api`: FastAPI backend that generates the file.
- `apps/web`: Next.js frontend to submit a URL and download the result.

## Run Local

From the repo root:

```bash
make run-local
```

This starts:
- API (`apps/api`) with CORS for local web.
- Web (`apps/web`) in dev mode.

See each app README for more details:
- `apps/api/README.md`
- `apps/web/README.md`
