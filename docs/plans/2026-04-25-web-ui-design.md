# Web UI Design — llmwiki

Date: 2026-04-25

## Overview

Add a modern web UI to llmwiki so users can ingest documents, query the wiki, browse pages, and view the operation log — without touching the CLI.

## Constraints

- Local deployment only (localhost)
- Existing CLI (`main.py`) must remain unchanged
- No new Python dependencies beyond FastAPI

## Architecture

Single-process: FastAPI serves the React SPA from `frontend/dist/` as static files, and exposes a JSON/SSE API at `/api/*`. The existing Python modules (`ingest`, `query`, `wiki`, `llm`) are imported directly into `api.py` — no duplication.

```
llmwiki/
├── api.py              ← FastAPI app (new)
├── frontend/           ← Vite + React + Tailwind (new)
│   ├── src/
│   │   ├── App.tsx
│   │   ├── pages/
│   │   │   ├── Index.tsx
│   │   │   ├── Page.tsx
│   │   │   ├── Ingest.tsx
│   │   │   ├── Query.tsx
│   │   │   └── Log.tsx
│   │   └── components/
│   │       └── WikiLink.tsx
│   └── dist/           ← built output (gitignored)
├── main.py             ← unchanged
└── ... (existing files unchanged)
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/pages` | List all pages with title + summary |
| GET | `/api/pages/{title}` | Get a single page (raw markdown) |
| POST | `/api/ingest` | Ingest text — streams SSE progress |
| POST | `/api/query` | Ask a question — streams SSE answer |
| GET | `/api/log` | Return log.md contents |
| GET | `/api/graph` | Return `{ nodes, edges }` for link graph |

Ingest and query use **Server-Sent Events** so the UI can show live tool-call progress (which pages the agent is reading/writing) before the final result.

## Frontend

**Stack:** React 18 + Vite + Tailwind CSS

**Layout:** Fixed sidebar nav + main content area.

**Pages:**
- **Index** — card grid of all pages (title + one-line summary), clickable to navigate
- **Page** — renders markdown; `[[WikiLinks]]` become clickable links
- **Query** — text input; streams agent tool calls as a live log, then renders final answer in markdown
- **Ingest** — textarea (paste) or drag-and-drop file; streams progress; shows pages written on completion
- **Log** — reverse-chronological list of operations from log.md

**Style:** Dark sidebar, light main content area, monospace wiki content, Tailwind `prose` for markdown.

## Running

```bash
# Build frontend once
cd frontend && npm install && npm run build

# Start server
uv run python api.py
# → http://localhost:8000
```

## Out of Scope

- Authentication
- Multi-user support
- Cloud deployment
- Graph visualization (beyond raw data endpoint)
