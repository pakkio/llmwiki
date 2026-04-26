# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

**llmwiki** is a Karpathy-style LLM-powered personal knowledge base. It ingests text documents, uses a DeepSeek V4-Flash agentic loop to decompose them into interlinked Markdown wiki pages, and answers questions grounded exclusively in the wiki. Two interfaces: a CLI (`main.py`) and a React SPA backed by a FastAPI server (`api.py`), running on port 8080.

## Running the project

**API server (production):**
```bash
nohup .venv/bin/python api.py > server.log 2>&1 &   # port 8080
```

**Frontend dev mode** (backend must already be running on 8080):
```bash
cd frontend && npm run dev               # port 5173, proxies /api/* → 8080
```

**Frontend build:**
```bash
cd frontend && npm run build             # outputs to frontend/dist/
```
When `frontend/dist/` exists, `api.py` serves the SPA at `/`.

**CLI:**
```bash
.venv/bin/python main.py ingest <file>
.venv/bin/python main.py ingest -
.venv/bin/python main.py query '<question>'
.venv/bin/python main.py query --no-cache '<question>'
.venv/bin/python main.py lint
.venv/bin/python main.py index | show <title> | log | graph
```

**Lint / typecheck frontend:**
```bash
cd frontend && npm run lint
npx tsc --noEmit
```

## Environment

`.env` (gitignored) must contain:
```
DEEPSEEK_API_KEY=<key>
AUTH_USERNAME=pakkio
AUTH_PASSWORD=<password>
```

Loaded by `python-dotenv` in `llm.py`. The OpenAI client points at `https://api.deepseek.com`.

## Directory layout

```
wiki/    ← knowledge graph pages + index.md + log.md (system-managed)
cache/   ← QA answer cache (keyed by exact question, gitignored)
raw/     ← original ingested source documents, timestamped (gitignored)
frontend/← React 19 SPA
```

## Architecture

### Data layer — `wiki.py`

Single source of truth for all filesystem I/O. Manages three directories:
- `wiki/` — Markdown pages; exposes `read_page`, `write_page`, `list_pages`, `search_pages` as LLM tool functions (also exported as `TOOLS` schema + `DISPATCH` dict)
- `cache/` — `read_cache(question)` / `write_cache(question, content)`; files named by sanitized question text
- `raw/` — `save_raw(text, source)` appends timestamped source documents on every ingest

`_RESERVED = {"index", "log"}` — these wiki files are system-managed and excluded from `list_pages` / `search_pages` results, but both agents can read them directly via `read_page`.

### LLM layer — `llm.py`

- `agent(prompt, tools, dispatch, ..., on_tool=None)` — tool-calling loop; returns `(content, stats)` where `stats` has `elapsed`, `turns`, `prompt_tokens`, `completion_tokens`, `cost_usd`
- Pricing constants: DeepSeek V4-Flash — `$0.14/$0.028/$0.28` per 1M input/cached/output tokens
- `on_tool` callback used by `api.py` to stream tool events over SSE

### Business logic — `ingest.py` / `query.py`

**`ingest.py`**: saves raw doc → runs agent (full read/write tools) → rebuilds index → appends log

**`query.py`**: checks `cache/` for exact match first (free, instant); on miss runs agent (read-only tools — no `write_page`) → writes result to `cache/` → appends log. `use_cache=False` skips the read but still refreshes the cache.

Query agent always starts by reading `index.md` for a full wiki overview, then searches for relevant pages. It can also read `log.md` directly if useful.

### API layer — `api.py`

- Bearer token auth middleware: all `/api/*` routes except `/api/login` require `Authorization: Bearer <token>`
- Sessions are in-memory (cleared on restart)
- Ingest and query run in a background thread and stream SSE (`type: tool | done | error`)
- Serves `frontend/dist/` as SPA when the build exists

### Frontend — `frontend/src/`

- `auth.ts` — `apiFetch()` wrapper (injects Bearer token, fires `auth:logout` event on 401)
- `pages/Login.tsx` — login gate shown when no token in localStorage
- `pages/Graph.tsx` — D3 force-directed graph; blue nodes = existing pages (sized by degree), dashed = linked but not created; zoom/pan/drag; click navigates to page
- All API calls go through `apiFetch()`, never bare `fetch()`
- React Router: `/` Index, `/graph`, `/page/:title`, `/query`, `/ingest`, `/lint`, `/log`, `/stats`, `/raw`
