# Web UI Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a FastAPI backend + React/Tailwind SPA that exposes all llmwiki functionality in a modern web UI, served from a single process at localhost:8000.

**Architecture:** FastAPI serves `frontend/dist/` as static files and exposes `/api/*` endpoints. The existing Python modules (`ingest`, `query`, `wiki`, `llm`) are imported directly — no duplication. Slow LLM operations (ingest, query) stream progress via Server-Sent Events.

**Tech Stack:** Python — FastAPI, uvicorn. Frontend — React 18, Vite, Tailwind CSS, react-router-dom, react-markdown, remark-gfm, @tailwindcss/typography.

---

### Task 1: Add FastAPI dependencies to pyproject.toml

**Files:**
- Modify: `pyproject.toml`

**Step 1: Add fastapi and uvicorn to dependencies**

Edit `pyproject.toml` so the dependencies list becomes:

```toml
[project]
name = "llmwiki"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "openai>=1.0",
    "python-dotenv>=1.0",
    "rich>=15.0.0",
    "fastapi>=0.111",
    "uvicorn[standard]>=0.29",
]
```

**Step 2: Sync the venv**

```bash
uv sync
```

Expected: resolves and installs fastapi + uvicorn into `.venv`.

---

### Task 2: Add SSE callback to `llm.py`

The `agent()` function must optionally call a hook after every tool dispatch so the FastAPI layer can stream progress to the browser. Add an `on_tool` parameter — existing callers pass nothing, so backward-compatible.

**Files:**
- Modify: `llm.py`

**Step 1: Update the `agent()` signature**

Change the function signature from:

```python
def agent(
    prompt: str,
    tools: list,
    dispatch: dict,
    model: str = DEFAULT_MODEL,
    system: str = DEFAULT_SYSTEM,
    label: str = "Thinking",
) -> str:
```

to:

```python
def agent(
    prompt: str,
    tools: list,
    dispatch: dict,
    model: str = DEFAULT_MODEL,
    system: str = DEFAULT_SYSTEM,
    label: str = "Thinking",
    on_tool=None,          # callable(name, args, result) | None
) -> str:
```

**Step 2: Call `on_tool` after each tool dispatch**

Inside the `for tc in msg.tool_calls:` loop, after the `_log_tool(...)` call, add:

```python
            if on_tool:
                on_tool(tc.function.name, args, str(result))
```

The full loop body becomes:

```python
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            result = dispatch[tc.function.name](args)
            _log_tool(tc.function.name, args, str(result))
            if on_tool:
                on_tool(tc.function.name, args, str(result))
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result,
            })
```

**Step 3: Verify CLI still works**

```bash
echo "Test the agent" | uv run python main.py ingest -
```

Expected: ingest runs normally (on_tool=None is a no-op).

---

### Task 3: Update `ingest.py` and `query.py` to accept and forward `on_tool`

**Files:**
- Modify: `ingest.py`
- Modify: `query.py`

**Step 1: Update `ingest.py`**

Change:

```python
def ingest(text: str) -> str:
    prompt = f"Ingest this document into the wiki:\n\n---\n{text}\n---"
    result = agent(prompt, TOOLS, DISPATCH, system=SYSTEM, label="Ingesting")
    rebuild_index()
    append_log("ingest", f"{len(text):,} chars → {result[:120].replace(chr(10), ' ')}")
    return result


def ingest_file(path: str) -> str:
    with open(path) as f:
        return ingest(f.read())
```

to:

```python
def ingest(text: str, on_tool=None) -> str:
    prompt = f"Ingest this document into the wiki:\n\n---\n{text}\n---"
    result = agent(prompt, TOOLS, DISPATCH, system=SYSTEM, label="Ingesting", on_tool=on_tool)
    rebuild_index()
    append_log("ingest", f"{len(text):,} chars → {result[:120].replace(chr(10), ' ')}")
    return result


def ingest_file(path: str, on_tool=None) -> str:
    with open(path) as f:
        return ingest(f.read(), on_tool=on_tool)
```

**Step 2: Update `query.py`**

Change:

```python
def query(question: str) -> str:
    result = agent(question, TOOLS, DISPATCH, system=SYSTEM, label="Querying")
    append_log("query", f"{question[:80]} → {result[:80].replace(chr(10), ' ')}")
    return result
```

to:

```python
def query(question: str, on_tool=None) -> str:
    result = agent(question, TOOLS, DISPATCH, system=SYSTEM, label="Querying", on_tool=on_tool)
    append_log("query", f"{question[:80]} → {result[:80].replace(chr(10), ' ')}")
    return result
```

**Step 3: Verify CLI still works**

```bash
uv run python main.py query "What is a transformer?"
```

Expected: answers as before.

---

### Task 4: Create `api.py` — FastAPI app

**Files:**
- Create: `api.py`

**Step 1: Create the file**

```python
#!/usr/bin/env python3
import json
import re
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from wiki import WIKI_DIR, _RESERVED, _path, list_pages, read_page, rebuild_index
from ingest import ingest
from query import query

app = FastAPI(title="llmwiki")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── helpers ──────────────────────────────────────────────────────────────────

def _page_summary(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return re.sub(r"\*\*([^*]+)\*\*", r"\1", line)[:120]
    return ""


def _sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


# ── API routes ────────────────────────────────────────────────────────────────

@app.get("/api/pages")
def api_list_pages():
    pages = []
    for p in sorted(WIKI_DIR.glob("*.md")):
        if p.stem in _RESERVED:
            continue
        text = p.read_text()
        links = sorted(set(re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', text)))
        pages.append({
            "title": p.stem,
            "summary": _page_summary(text),
            "links": links,
            "size": len(text),
        })
    return pages


@app.get("/api/pages/{title:path}")
def api_get_page(title: str):
    p = _path(title)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"Page '{title}' not found")
    return {"title": title, "content": p.read_text()}


@app.get("/api/log")
def api_log():
    log_path = _path("log")
    if not log_path.exists():
        return {"content": ""}
    return {"content": log_path.read_text()}


@app.get("/api/graph")
def api_graph():
    nodes, edges = [], []
    for p in sorted(WIKI_DIR.glob("*.md")):
        if p.stem in _RESERVED:
            continue
        nodes.append({"id": p.stem})
        text = p.read_text()
        for target in set(re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', text)):
            edges.append({"source": p.stem, "target": target})
    return {"nodes": nodes, "edges": edges}


class IngestRequest(BaseModel):
    text: str


@app.post("/api/ingest")
def api_ingest(req: IngestRequest):
    def stream():
        events = []

        def on_tool(name, args, result):
            events.append(_sse({"type": "tool", "name": name, "args": args, "result": result[:200]}))

        # Run ingest in same thread; yield events buffered per tool call
        # We use a generator trick: collect events during agent run, then flush
        # Since agent() is synchronous, we yield after it finishes per-tool
        import threading

        final = {}
        exc_holder = {}

        def run():
            try:
                final["result"] = ingest(req.text, on_tool=on_tool)
            except Exception as e:
                exc_holder["error"] = str(e)

        t = threading.Thread(target=run)
        t.start()

        import time
        while t.is_alive():
            while events:
                yield events.pop(0)
            time.sleep(0.05)

        t.join()
        while events:
            yield events.pop(0)

        if "error" in exc_holder:
            yield _sse({"type": "error", "message": exc_holder["error"]})
        else:
            yield _sse({"type": "done", "result": final["result"]})

    return StreamingResponse(stream(), media_type="text/event-stream")


class QueryRequest(BaseModel):
    question: str


@app.post("/api/query")
def api_query(req: QueryRequest):
    def stream():
        events = []

        def on_tool(name, args, result):
            events.append(_sse({"type": "tool", "name": name, "args": args, "result": result[:200]}))

        final = {}
        exc_holder = {}

        def run():
            try:
                final["result"] = query(req.question, on_tool=on_tool)
            except Exception as e:
                exc_holder["error"] = str(e)

        import threading, time
        t = threading.Thread(target=run)
        t.start()

        while t.is_alive():
            while events:
                yield events.pop(0)
            time.sleep(0.05)

        t.join()
        while events:
            yield events.pop(0)

        if "error" in exc_holder:
            yield _sse({"type": "error", "message": exc_holder["error"]})
        else:
            yield _sse({"type": "done", "result": final["result"]})

    return StreamingResponse(stream(), media_type="text/event-stream")


# ── Static SPA (must be last) ─────────────────────────────────────────────────

DIST = Path(__file__).parent / "frontend" / "dist"
if DIST.exists():
    app.mount("/", StaticFiles(directory=str(DIST), html=True), name="spa")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)
```

**Step 2: Smoke-test the API (without frontend)**

```bash
uv run python api.py &
curl http://localhost:8000/api/pages | python -m json.tool
```

Expected: JSON array of page objects. Kill background process after.

---

### Task 5: Scaffold the React + Vite + Tailwind frontend

**Files:**
- Create: `frontend/` (entire directory via npm commands)

**Step 1: Scaffold Vite React TypeScript project**

```bash
cd /home/pakkio/w/llmwiki
npm create vite@latest frontend -- --template react-ts
```

**Step 2: Install dependencies**

```bash
cd frontend
npm install
npm install react-router-dom react-markdown remark-gfm
npm install -D tailwindcss @tailwindcss/typography autoprefixer postcss
```

**Step 3: Init Tailwind**

```bash
npx tailwindcss init -p
```

**Step 4: Configure `tailwind.config.js`**

Replace the file content with:

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: { extend: {} },
  plugins: [require("@tailwindcss/typography")],
}
```

**Step 5: Replace `src/index.css`** with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Step 6: Replace `vite.config.ts`** with:

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
```

**Step 7: Verify build works**

```bash
npm run build
```

Expected: `frontend/dist/` created, no errors.

---

### Task 6: Create `App.tsx` with layout and routing

**Files:**
- Create: `frontend/src/App.tsx`

**Step 1: Write App.tsx**

```tsx
import { BrowserRouter, NavLink, Routes, Route } from 'react-router-dom'
import IndexPage from './pages/Index'
import PageView from './pages/Page'
import QueryPage from './pages/Query'
import IngestPage from './pages/Ingest'
import LogPage from './pages/Log'

const nav = [
  { to: '/',        label: 'Index'  },
  { to: '/query',   label: 'Query'  },
  { to: '/ingest',  label: 'Ingest' },
  { to: '/log',     label: 'Log'    },
]

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-gray-50 text-gray-900">
        {/* Sidebar */}
        <aside className="w-48 bg-gray-900 text-gray-100 flex flex-col shrink-0">
          <div className="px-4 py-5 text-lg font-bold tracking-tight border-b border-gray-700">
            🧠 llmwiki
          </div>
          <nav className="flex flex-col gap-1 p-3 flex-1">
            {nav.map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                end={to === '/'}
                className={({ isActive }) =>
                  `px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-gray-700 text-white'
                      : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                  }`
                }
              >
                {label}
              </NavLink>
            ))}
          </nav>
        </aside>

        {/* Main */}
        <main className="flex-1 overflow-auto p-8">
          <Routes>
            <Route path="/"            element={<IndexPage />} />
            <Route path="/page/:title" element={<PageView />} />
            <Route path="/query"       element={<QueryPage />} />
            <Route path="/ingest"      element={<IngestPage />} />
            <Route path="/log"         element={<LogPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
```

**Step 2: Replace `frontend/src/main.tsx`** with:

```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

---

### Task 7: Create `WikiLink` component

**Files:**
- Create: `frontend/src/components/WikiLink.tsx`

This component replaces `[[Title]]` and `[[Title|Label]]` patterns in markdown with clickable links.

```tsx
import { useNavigate } from 'react-router-dom'

interface Props {
  title: string
  label?: string
}

export default function WikiLink({ title, label }: Props) {
  const navigate = useNavigate()
  return (
    <button
      onClick={() => navigate(`/page/${encodeURIComponent(title)}`)}
      className="text-blue-600 hover:underline font-medium"
    >
      {label ?? title}
    </button>
  )
}
```

---

### Task 8: Create `Index` page

**Files:**
- Create: `frontend/src/pages/Index.tsx`

```tsx
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

interface PageMeta {
  title: string
  summary: string
  links: string[]
  size: number
}

export default function IndexPage() {
  const [pages, setPages] = useState<PageMeta[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    fetch('/api/pages')
      .then(r => r.json())
      .then(data => { setPages(data); setLoading(false) })
  }, [])

  if (loading) return <p className="text-gray-400">Loading…</p>
  if (!pages.length) return <p className="text-gray-400">No pages yet. Use Ingest to add content.</p>

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Wiki Index</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {pages.map(p => (
          <button
            key={p.title}
            onClick={() => navigate(`/page/${encodeURIComponent(p.title)}`)}
            className="text-left border border-gray-200 rounded-xl p-4 hover:border-blue-400 hover:shadow-sm transition-all bg-white"
          >
            <h2 className="font-semibold text-gray-900 mb-1">{p.title}</h2>
            <p className="text-sm text-gray-500 line-clamp-2">{p.summary}</p>
            {p.links.length > 0 && (
              <p className="text-xs text-blue-400 mt-2 truncate">
                → {p.links.slice(0, 3).join(', ')}{p.links.length > 3 ? '…' : ''}
              </p>
            )}
          </button>
        ))}
      </div>
    </div>
  )
}
```

---

### Task 9: Create `Page` view with WikiLink rendering

**Files:**
- Create: `frontend/src/pages/Page.tsx`

```tsx
import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export default function PageView() {
  const { title } = useParams<{ title: string }>()
  const navigate = useNavigate()
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!title) return
    setLoading(true)
    fetch(`/api/pages/${encodeURIComponent(title)}`)
      .then(r => {
        if (!r.ok) throw new Error('Page not found')
        return r.json()
      })
      .then(d => { setContent(d.content); setLoading(false) })
      .catch(e => { setError(e.message); setLoading(false) })
  }, [title])

  // Replace [[Title]] and [[Title|Label]] with links before rendering
  const processed = content
    .replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, (_, t, l) =>
      `[${l}](/page/${encodeURIComponent(t)})`)
    .replace(/\[\[([^\]]+)\]\]/g, (_, t) =>
      `[${t}](/page/${encodeURIComponent(t)})`)

  if (loading) return <p className="text-gray-400">Loading…</p>
  if (error)   return <p className="text-red-500">{error}</p>

  return (
    <div>
      <button onClick={() => navigate(-1)} className="text-sm text-gray-400 hover:text-gray-600 mb-4">
        ← Back
      </button>
      <article className="prose prose-slate max-w-3xl font-mono">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            a: ({ href, children }) => {
              if (href?.startsWith('/page/')) {
                const t = decodeURIComponent(href.replace('/page/', ''))
                return (
                  <button
                    onClick={() => navigate(href!)}
                    className="text-blue-600 hover:underline"
                  >
                    {children}
                  </button>
                )
              }
              return <a href={href} target="_blank" rel="noreferrer">{children}</a>
            }
          }}
        >
          {processed}
        </ReactMarkdown>
      </article>
    </div>
  )
}
```

---

### Task 10: Create `Query` page with SSE streaming

**Files:**
- Create: `frontend/src/pages/Query.tsx`

```tsx
import { useState, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface ToolEvent {
  name: string
  args: Record<string, string>
  result: string
}

const TOOL_COLORS: Record<string, string> = {
  read_page:    'text-cyan-600',
  write_page:   'text-green-600',
  list_pages:   'text-blue-600',
  search_pages: 'text-yellow-600',
}

export default function QueryPage() {
  const [question, setQuestion] = useState('')
  const [running, setRunning] = useState(false)
  const [events, setEvents] = useState<ToolEvent[]>([])
  const [answer, setAnswer] = useState('')
  const [error, setError] = useState('')
  const abortRef = useRef<AbortController | null>(null)

  async function submit() {
    if (!question.trim() || running) return
    setRunning(true)
    setEvents([])
    setAnswer('')
    setError('')
    abortRef.current = new AbortController()

    try {
      const res = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
        signal: abortRef.current.signal,
      })
      const reader = res.body!.getReader()
      const decoder = new TextDecoder()
      let buf = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buf += decoder.decode(value, { stream: true })
        const parts = buf.split('\n\n')
        buf = parts.pop()!
        for (const part of parts) {
          if (!part.startsWith('data: ')) continue
          const evt = JSON.parse(part.slice(6))
          if (evt.type === 'tool')  setEvents(e => [...e, evt])
          if (evt.type === 'done')  setAnswer(evt.result)
          if (evt.type === 'error') setError(evt.message)
        }
      }
    } catch (e: any) {
      if (e.name !== 'AbortError') setError(String(e))
    } finally {
      setRunning(false)
    }
  }

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold mb-6">Query</h1>

      <div className="flex gap-2 mb-6">
        <input
          value={question}
          onChange={e => setQuestion(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && submit()}
          placeholder="Ask a question grounded in the wiki…"
          className="flex-1 border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          onClick={submit}
          disabled={running || !question.trim()}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          {running ? 'Thinking…' : 'Ask'}
        </button>
      </div>

      {events.length > 0 && (
        <div className="mb-4 bg-gray-900 text-gray-100 rounded-lg p-4 font-mono text-xs space-y-1">
          {events.map((e, i) => (
            <div key={i}>
              <span className={TOOL_COLORS[e.name] ?? 'text-white'}>{e.name}</span>
              <span className="text-gray-400">
                ({Object.entries(e.args).map(([k,v]) => `${k}=${JSON.stringify(v)}`).join(', ')})
              </span>
              <span className="text-gray-500"> → {e.result.slice(0, 80)}</span>
            </div>
          ))}
          {running && <div className="text-gray-400 animate-pulse">…</div>}
        </div>
      )}

      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

      {answer && (
        <div className="prose prose-slate max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{answer}</ReactMarkdown>
        </div>
      )}
    </div>
  )
}
```

---

### Task 11: Create `Ingest` page with SSE streaming

**Files:**
- Create: `frontend/src/pages/Ingest.tsx`

```tsx
import { useState, useRef } from 'react'

interface ToolEvent {
  name: string
  args: Record<string, string>
}

export default function IngestPage() {
  const [text, setText] = useState('')
  const [running, setRunning] = useState(false)
  const [events, setEvents] = useState<ToolEvent[]>([])
  const [result, setResult] = useState('')
  const [error, setError] = useState('')

  function handleDrop(e: React.DragEvent) {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = ev => setText(ev.target?.result as string)
    reader.readAsText(file)
  }

  async function submit() {
    if (!text.trim() || running) return
    setRunning(true)
    setEvents([])
    setResult('')
    setError('')

    try {
      const res = await fetch('/api/ingest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      })
      const reader = res.body!.getReader()
      const decoder = new TextDecoder()
      let buf = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buf += decoder.decode(value, { stream: true })
        const parts = buf.split('\n\n')
        buf = parts.pop()!
        for (const part of parts) {
          if (!part.startsWith('data: ')) continue
          const evt = JSON.parse(part.slice(6))
          if (evt.type === 'tool')  setEvents(e => [...e, evt])
          if (evt.type === 'done')  setResult(evt.result)
          if (evt.type === 'error') setError(evt.message)
        }
      }
    } catch (e: any) {
      setError(String(e))
    } finally {
      setRunning(false)
    }
  }

  const writtenPages = events.filter(e => e.name === 'write_page').map(e => e.args.title)

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold mb-6">Ingest</h1>

      <div
        onDrop={handleDrop}
        onDragOver={e => e.preventDefault()}
        className="mb-4 border-2 border-dashed border-gray-300 rounded-xl p-3 text-center text-sm text-gray-400 hover:border-blue-300 transition-colors"
      >
        Drop a text file here, or paste below
      </div>

      <textarea
        value={text}
        onChange={e => setText(e.target.value)}
        rows={10}
        placeholder="Paste document text here…"
        className="w-full border border-gray-300 rounded-lg px-4 py-3 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-400 resize-y mb-4"
      />

      <button
        onClick={submit}
        disabled={running || !text.trim()}
        className="px-5 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50"
      >
        {running ? 'Ingesting…' : 'Ingest'}
      </button>

      {events.length > 0 && (
        <div className="mt-4 bg-gray-900 text-gray-100 rounded-lg p-4 font-mono text-xs space-y-1">
          {events.map((e, i) => (
            <div key={i}>
              <span className={e.name === 'write_page' ? 'text-green-400' : 'text-cyan-400'}>
                {e.name}
              </span>
              {e.args.title && <span className="text-gray-300"> "{e.args.title}"</span>}
            </div>
          ))}
          {running && <div className="text-gray-400 animate-pulse">…</div>}
        </div>
      )}

      {writtenPages.length > 0 && !running && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-sm font-semibold text-green-800 mb-1">Pages written:</p>
          <ul className="text-sm text-green-700 list-disc list-inside">
            {[...new Set(writtenPages)].map(t => <li key={t}>{t}</li>)}
          </ul>
        </div>
      )}

      {error && <p className="text-red-500 text-sm mt-4">{error}</p>}
      {result && !running && (
        <p className="text-sm text-gray-600 mt-4 italic">{result}</p>
      )}
    </div>
  )
}
```

---

### Task 12: Create `Log` page

**Files:**
- Create: `frontend/src/pages/Log.tsx`

```tsx
import { useEffect, useState } from 'react'

export default function LogPage() {
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/log')
      .then(r => r.json())
      .then(d => { setContent(d.content); setLoading(false) })
  }, [])

  if (loading) return <p className="text-gray-400">Loading…</p>

  const entries = content
    .split('\n')
    .filter(l => l.startsWith('- `'))
    .reverse()

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold mb-6">Log</h1>
      {!entries.length
        ? <p className="text-gray-400">No operations logged yet.</p>
        : (
          <ul className="space-y-2">
            {entries.map((e, i) => {
              const m = e.match(/^- `([^`]+)` \*\*([^*]+)\*\* — (.+)$/)
              if (!m) return <li key={i} className="text-sm text-gray-500 font-mono">{e}</li>
              const [, ts, op, detail] = m
              return (
                <li key={i} className="flex gap-3 items-start text-sm">
                  <span className="text-gray-400 font-mono shrink-0">{ts}</span>
                  <span className={`font-semibold shrink-0 ${op === 'ingest' ? 'text-green-600' : 'text-blue-600'}`}>{op}</span>
                  <span className="text-gray-600 truncate">{detail}</span>
                </li>
              )
            })}
          </ul>
        )
      }
    </div>
  )
}
```

---

### Task 13: Build frontend and run end-to-end

**Step 1: Build the React app**

```bash
cd /home/pakkio/w/llmwiki/frontend
npm run build
```

Expected: `frontend/dist/` populated, no TypeScript errors.

**Step 2: Start the FastAPI server**

```bash
cd /home/pakkio/w/llmwiki
uv run python api.py
```

Expected: `Uvicorn running on http://0.0.0.0:8000`

**Step 3: Open in browser**

Navigate to `http://localhost:8000`

Expected:
- Sidebar with Index / Query / Ingest / Log
- Index page shows existing wiki pages as cards
- Clicking a card shows the page with rendered markdown and clickable WikiLinks
- Query page: type a question, see tool calls stream, answer appears
- Ingest page: paste text, see pages being written in real time
- Log page: shows past operations

**Step 4: Add `.gitignore` entries**

Add to a root `.gitignore`:

```
frontend/dist/
frontend/node_modules/
__pycache__/
.env
.venv/
```

---

## Running the app

```bash
# One-time: build frontend
cd frontend && npm install && npm run build && cd ..

# Start server
uv run python api.py
# Open http://localhost:8000
```
