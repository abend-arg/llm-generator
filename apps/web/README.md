# Web

## Intro

Minimal Next.js frontend to generate and download `llms.txt` from a URL using the API.

## Requirements

- Node.js (18+ recommended)
- npm/pnpm/yarn/bun

## Local Environment Setup

```bash
cd /home/abend/Dev/llm-generator/apps/web
npm install
```

## Environment

Set the backend URL via `BE_API_URL` (frontend env var):

```env
BE_API_URL=http://localhost:8000
```

> If not set, the app falls back to `http://localhost:8000`.

## Run Dev Server

```bash
npm run dev
```

Then open the app at:

```text
http://localhost:3000
```

## Notes

- The API should be running (see `apps/api/README.md`).
- In local dev, start the API with CORS enabled (`make run-local`).
