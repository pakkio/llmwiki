from llm import agent
from wiki import TOOLS, DISPATCH, read_page, read_cache, write_cache, append_log

# Query agent gets read-only tools (no write_page)
_QUERY_TOOLS = [t for t in TOOLS if t["function"]["name"] != "write_page"]


def _restricted_read(args: dict) -> str:
    return read_page(args.get("title", ""))


_QUERY_DISPATCH = {
    "read_page":    _restricted_read,
    "list_pages":   DISPATCH["list_pages"],
    "search_pages": DISPATCH["search_pages"],
}

SYSTEM = """You are a wiki query agent. Answer questions using only the wiki as your knowledge source.

Rules:
- Never answer from your own training knowledge — only from what you read in the wiki.
- If the wiki lacks the information, say so clearly rather than guessing.
- Always cite which pages you drew from at the end of your answer.

MANDATORY first step — no exceptions:
- Call read_page("index") before anything else. Do not search or read any page until you have done this.
- If the index alone is sufficient to answer (listing, coverage, discovery questions), answer immediately without searching or reading further.

Then (only if more detail is needed):
1. search_pages with 1–2 keyword variants to locate relevant pages.
2. list_pages if search returns nothing.
3. read_page for each relevant page.
4. Follow [[WikiLinks]] — if a linked concept is relevant, read that page too.
5. Answer concisely, grounded in what you read. End with: *Sources: [[Page1]], [[Page2]]*"""


def query(question: str, on_tool=None, use_cache: bool = True) -> str:
    q_snippet = question[:60] + ("…" if len(question) > 60 else "")

    # Exact cache hit — return instantly at zero cost
    if use_cache:
        cached = read_cache(question)
        if cached is not None:
            append_log("query", f'"{q_snippet}" · cached · $0.0000 · 0 in / 0 out tok')
            return cached

    # Cache miss (or cache bypassed) — run the agent
    content, stats = agent(
        question, _QUERY_TOOLS, _QUERY_DISPATCH,
        system=SYSTEM, label="Querying", on_tool=on_tool,
    )

    # Write (or refresh) cache entry for next time
    write_cache(question, content)

    q_snippet = question[:60] + ("…" if len(question) > 60 else "")
    detail = (
        f'"{q_snippet}"'
        f" · {stats['turns']} turns"
        f" · {stats['elapsed']:.1f}s"
        f" · ${stats['cost_usd']:.4f}"
        f" · {stats['prompt_tokens']:,} in / {stats['completion_tokens']:,} out tok"
    )
    append_log("query", detail)
    return content
