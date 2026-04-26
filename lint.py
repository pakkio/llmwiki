import json
import re
from wiki import WIKI_DIR, TOOLS, DISPATCH, list_pages, read_page, append_log

_READ_ONLY = {"read_page", "list_pages", "search_pages"}
_LINT_TOOLS = [t for t in TOOLS if t["function"]["name"] in _READ_ONLY]
_LINT_DISPATCH = {k: v for k, v in DISPATCH.items() if k in _READ_ONLY}

SYSTEM = """You are a wiki health-check agent. Audit the wiki and produce a structured lint report.

Look for:
1. Contradictions — claims on different pages that conflict with each other.
2. Missing cross-references — concepts mentioned in text but not WikiLinked.
3. Data gaps — important topics hinted at but lacking their own page.
4. Suggested questions — queries worth asking to deepen the knowledge base.
5. Suggested sources — types of documents worth ingesting next.

Note: orphan pages, missing pages, and isolated pages are already identified in the structural
analysis provided in your prompt — include them in the report but do not re-derive them.

Steps:
1. Review the pre-computed structural analysis.
2. Use read_page on pages that may contradict each other or have missing cross-references.
   Focus on pages that share topics — use search_pages to find related ones.
3. Produce the markdown report below. Be specific: cite page titles, quote snippets.
   If the wiki is healthy, say so — do not fabricate issues.

Output format:

# Wiki Lint Report

## Summary
One-paragraph overview of wiki health.

## Structural Issues
### Orphan pages (no inbound links)
### Missing pages (WikiLinked but not created)
### Isolated pages (no outbound links)

## Semantic Issues
### Contradictions
### Missing cross-references

## Gaps & Suggestions
### Questions worth investigating
### Sources worth ingesting

## Health score
X/10 with one-line justification."""


def _graph_analysis() -> dict:
    pages = set(json.loads(list_pages()))
    if not pages:
        return {"page_count": 0, "pages": [], "orphans": [], "missing_pages": [], "isolated": []}

    inbound: dict[str, list] = {p: [] for p in pages}
    outbound: dict[str, list] = {p: [] for p in pages}
    missing_targets: set[str] = set()

    for title in pages:
        text = (WIKI_DIR / f"{title}.md").read_text()
        links = set(re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', text))
        for link in links:
            if link in pages:
                inbound[link].append(title)
                outbound[title].append(link)
            else:
                missing_targets.add(link)

    return {
        "page_count": len(pages),
        "pages": sorted(pages),
        "orphans": sorted(p for p in pages if not inbound[p]),
        "missing_pages": sorted(missing_targets),
        "isolated": sorted(p for p in pages if not outbound[p]),
    }


def lint(on_tool=None) -> str:
    from llm import agent

    analysis = _graph_analysis()
    if not analysis["page_count"]:
        return "Wiki is empty — nothing to lint."

    prompt = (
        "Health-check this wiki. Pre-computed structural analysis:\n\n"
        f"```json\n{json.dumps(analysis, indent=2)}\n```\n\n"
        "Now read pages to find semantic issues and produce the lint report."
    )

    content, stats = agent(
        prompt, _LINT_TOOLS, _LINT_DISPATCH,
        system=SYSTEM, label="Linting", on_tool=on_tool,
    )

    detail = (
        f"{analysis['page_count']} pages"
        f" · {stats['turns']} turns"
        f" · {stats['elapsed']:.1f}s"
        f" · ${stats['cost_usd']:.4f}"
        f" · {stats['prompt_tokens']:,} in / {stats['completion_tokens']:,} out tok"
    )
    append_log("lint", detail)
    return content
