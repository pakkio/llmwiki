#!/usr/bin/env python3
import json
import os
import re
import secrets
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from wiki import WIKI_DIR, RAW_DIR, _RESERVED, _path, list_pages, read_page, rebuild_index
from ingest import ingest
from query import query
from lint import lint

_AUTH_USER = os.environ.get("AUTH_USERNAME", "pakkio")
_AUTH_PASS = os.environ.get("AUTH_PASSWORD", "")
_sessions: set[str] = set()

app = FastAPI(title="llmwiki")


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    path = request.url.path
    if path.startswith("/api/") and path != "/api/login":
        auth = request.headers.get("Authorization", "")
        token = auth.removeprefix("Bearer ").strip()
        if token not in _sessions:
            return JSONResponse({"detail": "Unauthorized"}, status_code=401)
    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/api/login")
def api_login(req: LoginRequest):
    if req.username == _AUTH_USER and req.password == _AUTH_PASS:
        token = secrets.token_hex(32)
        _sessions.add(token)
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


def _page_summary(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return re.sub(r"\*\*([^*]+)\*\*", r"\1", line)[:120]
    return ""


def _sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


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


@app.get("/api/stats")
def api_stats():
    log_path = _path("log")
    if not log_path.exists():
        return {}
    stats = {
        "ingest_count": 0, "ingest_cost": 0.0,
        "ingest_tokens_in": 0, "ingest_tokens_out": 0,
        "query_count": 0, "query_cost": 0.0,
        "query_tokens_in": 0, "query_tokens_out": 0,
        "cached_count": 0,
    }
    entry_re = re.compile(r'^- `[^`]+` \*\*(\w+)\*\* — (.+)$')
    cost_re  = re.compile(r'\$([0-9.]+)')
    tok_re   = re.compile(r'([\d,]+) in / ([\d,]+) out tok')
    for line in log_path.read_text().splitlines():
        m = entry_re.match(line)
        if not m:
            continue
        op, detail = m.group(1), m.group(2)
        cm = cost_re.search(detail)
        tm = tok_re.search(detail)
        cost = float(cm.group(1)) if cm else 0.0
        tok_in  = int(tm.group(1).replace(",", "")) if tm else 0
        tok_out = int(tm.group(2).replace(",", "")) if tm else 0
        if op == "ingest":
            stats["ingest_count"] += 1
            stats["ingest_cost"]      += cost
            stats["ingest_tokens_in"]  += tok_in
            stats["ingest_tokens_out"] += tok_out
        elif op == "query":
            if "· cached ·" in detail:
                stats["cached_count"] += 1
            else:
                stats["query_count"]      += 1
                stats["query_cost"]        += cost
                stats["query_tokens_in"]   += tok_in
                stats["query_tokens_out"]  += tok_out
    stats["total_cost"] = round(stats["ingest_cost"] + stats["query_cost"], 6)
    stats["ingest_cost"] = round(stats["ingest_cost"], 6)
    stats["query_cost"]  = round(stats["query_cost"],  6)
    return stats


@app.get("/api/raw")
def api_raw_list():
    # Start with files actually on disk
    on_disk: dict[str, dict] = {}
    for p in RAW_DIR.glob("*.txt"):
        on_disk[p.name] = {"name": p.name, "size": p.stat().st_size, "mtime": p.stat().st_mtime, "exists": True}

    # Augment with names referenced in the log (may have been deleted)
    log_path = _path("log")
    if log_path.exists():
        raw_re = re.compile(r'raw:(\S+\.txt)')
        for line in log_path.read_text().splitlines():
            m = raw_re.search(line)
            if m:
                name = m.group(1)
                if name not in on_disk:
                    on_disk[name] = {"name": name, "size": None, "mtime": None, "exists": False}

    return sorted(on_disk.values(), key=lambda f: f["name"], reverse=True)


@app.get("/api/raw/{filename}")
def api_raw_get(filename: str):
    p = RAW_DIR / filename
    if not p.exists() or not p.is_relative_to(RAW_DIR):
        raise HTTPException(status_code=404, detail="Not found")
    return {"name": filename, "content": p.read_text()}


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
        import threading, time
        events = []

        def on_tool(name, args, result):
            events.append(_sse({"type": "tool", "name": name, "args": args, "result": result[:200]}))

        final = {}
        exc_holder = {}

        def run():
            try:
                final["result"] = ingest(req.text, on_tool=on_tool)
            except Exception as e:
                exc_holder["error"] = str(e)

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


@app.get("/api/lint")
def api_lint():
    def stream():
        import threading, time
        events = []

        def on_tool(name, args, result):
            events.append(_sse({"type": "tool", "name": name, "args": args, "result": result[:200]}))

        final = {}
        exc_holder = {}

        def run():
            try:
                final["result"] = lint(on_tool=on_tool)
            except Exception as e:
                exc_holder["error"] = str(e)

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


class QueryRequest(BaseModel):
    question: str
    use_cache: bool = True


@app.post("/api/query")
def api_query(req: QueryRequest):
    def stream():
        import threading, time
        events = []

        def on_tool(name, args, result):
            events.append(_sse({"type": "tool", "name": name, "args": args, "result": result[:200]}))

        final = {}
        exc_holder = {}

        def run():
            try:
                final["result"] = query(req.question, on_tool=on_tool, use_cache=req.use_cache)
            except Exception as e:
                exc_holder["error"] = str(e)

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


DIST = Path(__file__).parent / "frontend" / "dist"
if DIST.exists():
    app.mount("/", StaticFiles(directory=str(DIST), html=True), name="spa")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=False)
