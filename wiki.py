import json
import re
from datetime import datetime, timezone
from pathlib import Path

WIKI_DIR  = Path(__file__).parent / "wiki"
CACHE_DIR = Path(__file__).parent / "cache"
RAW_DIR   = Path(__file__).parent / "raw"

for _d in (WIKI_DIR, CACHE_DIR, RAW_DIR):
    _d.mkdir(exist_ok=True)

_RESERVED = {"index", "log"}


# --- Wiki pages ---

def _path(title: str) -> Path:
    return WIKI_DIR / f"{title.replace('/', '_')}.md"


def read_page(title: str) -> str:
    p = _path(title)
    if not p.exists():
        return f"Page '{title}' does not exist."
    return p.read_text()


def write_page(title: str, content: str) -> str:
    _path(title).write_text(content)
    return f"Page '{title}' written ({len(content)} chars)."


def append_page(title: str, content: str) -> str:
    p = _path(title)
    if not p.exists():
        return f"Page '{title}' does not exist. Use write_page to create it first."
    with open(p, "a") as f:
        f.write("\n" + content)
    return f"Appended {len(content)} chars to '{title}'."


def delete_page(title: str) -> str:
    p = _path(title)
    if title in _RESERVED:
        return f"Page '{title}' is system-managed and cannot be deleted."
    if not p.exists():
        return f"Page '{title}' does not exist."
    p.unlink()
    return f"Page '{title}' deleted."


def list_pages() -> str:
    pages = [p.stem for p in sorted(WIKI_DIR.glob("*.md")) if p.stem not in _RESERVED]
    return json.dumps(pages) if pages else "[]"


def search_pages(query: str) -> str:
    query_lower = query.lower()
    matches = []
    for p in sorted(WIKI_DIR.glob("*.md")):
        if p.stem in _RESERVED:
            continue
        text = p.read_text()
        if query_lower in p.stem.lower() or query_lower in text.lower():
            snippet = next((l.strip() for l in text.splitlines() if l.strip()), "")
            matches.append({"title": p.stem, "snippet": snippet[:120]})
    return json.dumps(matches) if matches else "[]"


# --- Cache (QA answers) ---

def _cache_path(question: str) -> Path:
    safe = re.sub(r'[/:*?"<>|\\]', '_', question.strip())[:120]
    return CACHE_DIR / f"{safe}.md"


def read_cache(question: str) -> str | None:
    p = _cache_path(question)
    return p.read_text() if p.exists() else None


def write_cache(question: str, content: str) -> None:
    _cache_path(question).write_text(content)


# --- Raw ingested documents ---

def save_raw(text: str, source: str = "") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    safe_src = re.sub(r'[/:*?"<>|\\]', '_', source)[:40]
    name = f"{ts}_{safe_src}.txt" if safe_src else f"{ts}.txt"
    (RAW_DIR / name).write_text(text)
    return name


# --- System-managed wiki files ---

def rebuild_index() -> None:
    pages = [p for p in sorted(WIKI_DIR.glob("*.md")) if p.stem not in _RESERVED]
    if not pages:
        _path("index").write_text("# Wiki Index\n\n_Empty._\n")
        return

    lines = ["# Wiki Index\n", f"_{len(pages)} pages — last updated {_now()}_\n"]
    for p in pages:
        text = p.read_text()
        summary = next(
            (l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")),
            ""
        )
        summary = re.sub(r"\*\*([^*]+)\*\*", r"\1", summary)[:300]
        links = sorted(set(re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', text)))
        link_str = ", ".join(f"[[{l}]]" for l in links[:5]) + ("…" if len(links) > 5 else "")
        lines.append(f"## [[{p.stem}]]\n{summary}\n\n_Links: {link_str}_\n")

    _path("index").write_text("\n".join(lines))


def append_log(operation: str, detail: str) -> None:
    log_path = _path("log")
    header = "# Wiki Log\n\n" if not log_path.exists() else ""
    entry = f"- `{_now()}` **{operation}** — {detail}\n"
    with open(log_path, "a") as f:
        f.write(header + entry)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


# --- Tool definitions for the LLM agent ---

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_page",
            "description": "Read an existing wiki page by title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Page title (filename without .md)"},
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_page",
            "description": "Create or overwrite a wiki page. Use markdown with [[WikiLinks]] for related pages.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Page title"},
                    "content": {"type": "string", "description": "Full markdown content of the page"},
                },
                "required": ["title", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "append_page",
            "description": "Append markdown content to the end of an existing wiki page. Use instead of write_page when only adding new information to avoid overwriting existing content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Page title"},
                    "content": {"type": "string", "description": "Markdown content to append"},
                },
                "required": ["title", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_page",
            "description": "Delete a wiki page. Use only to remove duplicates or stale pages superseded by a better one.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Page title to delete"},
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_pages",
            "description": "List all existing wiki page titles.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_pages",
            "description": "Search wiki pages by keyword (checks titles and content).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search keyword or phrase"},
                },
                "required": ["query"],
            },
        },
    },
]

DISPATCH = {
    "read_page":    lambda args: read_page(**args),
    "write_page":   lambda args: write_page(**args),
    "append_page":  lambda args: append_page(**args),
    "delete_page":  lambda args: delete_page(**args),
    "list_pages":   lambda _: list_pages(),
    "search_pages": lambda args: search_pages(**args),
}
