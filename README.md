# llmwiki

A Karpathy-style LLM-powered personal knowledge base. Paste or ingest any document and an agentic loop (DeepSeek V4-Flash) decomposes it into interlinked Markdown wiki pages. Query the wiki to get answers grounded strictly in what was ingested — no hallucination from model training data.

## Features

- **Ingest** — paste text or submit a file; the agent turns it into linked wiki pages
- **Query** — ask questions answered only from the wiki; repeat queries are cached
- **Graph** — interactive force-directed graph of wiki page relationships
- **Lint** — wiki health checks for gaps, orphan pages, and missing cross-references
- **Stats** — usage and cost totals for ingest/query/cache activity
- **Raw** — browse original ingested source documents, including deleted entries from the log
- **Log** — per-operation cost, time, and token counts
- **CLI + Web UI** — both interfaces share the same Python backend

## Quick start

```bash
# 1. Create .env
echo "DEEPSEEK_API_KEY=<your key>" > .env
echo "AUTH_USERNAME=pakkio"       >> .env
echo "AUTH_PASSWORD=<password>"   >> .env

# 2. Build frontend
cd frontend && npm install && npm run build && cd ..

# 3. Start server
.venv/bin/python api.py
# → http://0.0.0.0:8080
```

## Directory layout

```
wiki/    ← knowledge graph (Markdown pages + index.md + log.md)
cache/   ← cached QA answers (keyed by question)
raw/     ← original ingested source documents (saved on every ingest)
frontend/← React 19 + Vite + Tailwind SPA
```

## CLI usage

```bash
.venv/bin/python main.py ingest <file>       # ingest a file
.venv/bin/python main.py ingest -            # ingest from stdin
.venv/bin/python main.py query '<question>'  # query the wiki
.venv/bin/python main.py query --no-cache '<question>'  # bypass cache
.venv/bin/python main.py lint                # run wiki health checks
.venv/bin/python main.py index               # list all pages
.venv/bin/python main.py show <title>        # render a page
.venv/bin/python main.py log                 # operation log
.venv/bin/python main.py graph               # WikiLink graph (CLI)
```

## Environment variables

| Variable | Description |
|---|---|
| `DEEPSEEK_API_KEY` | DeepSeek API key |
| `AUTH_USERNAME` | Web UI login username |
| `AUTH_PASSWORD` | Web UI login password |

## Architecture

```
ingest.py / query.py   ← system prompts + agent orchestration
llm.py                 ← DeepSeek agent loop (tool calling, cost tracking)
wiki.py                ← all filesystem I/O (wiki/, cache/, raw/)
api.py                 ← FastAPI + Bearer token auth + SSE streaming
frontend/src/          ← React SPA (Index, Page, Query, Ingest, Lint, Log, Stats, Raw, Graph)
```

- **Ingest agent** has full read/write access to `wiki/`
- **Query agent** is read-only on `wiki/`; cache reads/writes are handled at the application level
- Both agents never see `cache/`, `raw/`, `index.md`, or `log.md`
- Token usage and cost are tracked per operation and written to `wiki/log.md`
