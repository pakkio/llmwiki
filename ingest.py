from pathlib import Path
from llm import agent
from wiki import TOOLS, DISPATCH, save_raw, rebuild_index, append_log

SYSTEM = """You are a wiki-building agent. Your job: decompose a document into structured, interlinked wiki pages.

Rules:
- Do NOT write index.md or log.md — those are system-managed.
- Do NOT hallucinate facts beyond the source document.
- Prefer updating an existing page over creating a near-duplicate. Use delete_page to remove a stale or duplicate page after merging its content into a better one.
- Every page must use [[WikiLinks]] to name related concepts, even if those pages don't exist yet.

Steps:
1. list_pages — see what already exists.
2. Identify 3–8 key concepts/entities in the document.
3. For each concept: search_pages to check for an existing page; if found, read_page to review it.
4. write_page for each concept with:
   - # Title as the first line
   - Concise sections covering definition, context, and details from the document
   - [[WikiLinks]] to related concepts throughout
5. Reply with a one-paragraph summary: pages written, pages updated, key links created."""


def ingest(text: str, on_tool=None, source: str = "") -> str:
    raw_name = save_raw(text, source)
    prompt = f"Ingest this document into the wiki:\n\n---\n{text}\n---"
    content, stats = agent(prompt, TOOLS, DISPATCH, system=SYSTEM, label="Ingesting", on_tool=on_tool)
    rebuild_index()
    detail = (
        f"{len(text):,} chars"
        f" · {stats['turns']} turns"
        f" · {stats['elapsed']:.1f}s"
        f" · ${stats['cost_usd']:.4f}"
        f" · {stats['prompt_tokens']:,} in / {stats['completion_tokens']:,} out tok"
        f" · raw:{raw_name}"
    )
    append_log("ingest", detail)
    return content


def ingest_file(path: str, on_tool=None) -> str:
    with open(path) as f:
        text = f.read()
    return ingest(text, on_tool=on_tool, source=Path(path).name)
