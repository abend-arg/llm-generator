# Web

## Intro

Minimal Next.js frontend to generate and download `llms.txt` from a URL using the API. The app is designed to be exported as a static site to take advantage of inexpensive static hosting in the cloud.

## Requirements

- Node.js (18+ recommended)
- npm/pnpm/yarn/bun

## Local Environment Setup

```bash
cd apps/web
make install
```

## Environment

Set the backend URL via `NEXT_PUBLIC_BE_API_URL` (frontend env var):

```env
NEXT_PUBLIC_BE_API_URL=http://example.com/api
```

> If not set, the app falls back to `http://localhost:8000`.

## Run Dev Server

Using Makefile:

```bash
make dev
```

Or directly:

```bash
npm run dev
```

Then open the app at:

```text
http://localhost:3000
```

## Notes

- The API should be running (see `apps/api/README.md`).

## Static Export

This app is configured for static export (ideal for any static host).

```bash
make build
# or
npm run build
```

The static files will be generated in the `out/` directory. 

## Deployment Notes

For a static hosting setup (e.g., DigitalOcean App Platform):

1. Build the static bundle:

```bash
npm run build
```

2. Set the backend URL:

```
NEXT_PUBLIC_BE_API_URL=https://your-api-domain.com
```

3. Deploy the `out/` directory as a static site.

## Future Work

- UI polish (layout/spacing, visual hierarchy, states).
- Optional stream of user interactions (analytics/usage events) if needed.
- Automated UI tests (Playwright, Cypress, or Selenium).
