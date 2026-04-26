import json
import re
from wiki import WIKI_DIR, read_page, list_pages

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.table import Table
    from rich.panel import Panel
    from rich.rule import Rule
    _rich = True
except ImportError:
    _rich = False

_console = Console() if _rich else None


def show_help() -> None:
    if _rich:
        from rich.text import Text
        from rich.columns import Columns

        def cmd(name, args, desc):
            return f"  [bold cyan]{name}[/] [green]{args}[/]\n    [dim]{desc}[/dim]\n"

        body = (
            "[bold]llmwiki[/] — LLM-powered knowledge base (Karpathy-style)\n\n"
            "[bold underline]Commands[/]\n\n"
            + cmd("ingest", "<file>",    "Extract concepts from a file and write wiki pages")
            + cmd("ingest", "-",         "Same, reading from stdin")
            + cmd("query",  "<question>","Answer a question grounded in the wiki")
            + cmd("lint",   "",          "Health-check the wiki (orphans, contradictions, gaps)")
            + cmd("index",  "",          "Rich table: all pages, summaries, links, sizes")
            + cmd("show",   "<title>",   "Render a wiki page as markdown  (try: show index)")
            + cmd("log",    "",          "Show the operation log (ingests + queries)")
            + cmd("graph",  "",          "Print the [[WikiLink]] graph between pages")
            + cmd("help",   "",          "Show this message")
            + "\n[bold underline]Examples[/]\n\n"
            "  [dim]$ uv run python main.py ingest notes.txt[/dim]\n"
            "  [dim]$ echo 'BERT is ...' | uv run python main.py ingest -[/dim]\n"
            "  [dim]$ uv run python main.py query 'What is a vector store?'[/dim]\n"
            "  [dim]$ uv run python main.py show Transformer[/dim]\n"
            "  [dim]$ uv run python main.py show index[/dim]\n"
        )
        _console.print(Panel(body, title="[bold]llmwiki help[/]", border_style="cyan", padding=(1, 2)))
    else:
        print(__import__("__main__").__doc__)


def _header(text: str) -> None:
    if _rich:
        _console.print(Rule(f"[bold cyan]{text}[/bold cyan]", style="cyan"))
    else:
        print(f"\n{'─'*60}  {text}  {'─'*60}\n")


def show_page(title: str) -> None:
    _header(f"show  {title}")
    content = read_page(title)
    if _rich:
        _console.print(Panel(Markdown(content), title=f"[bold cyan]{title}[/]", border_style="cyan"))
    else:
        print(f"\n{'='*60}\n{title}\n{'='*60}\n{content}\n")


def show_index() -> None:
    _header("index")
    pages = json.loads(list_pages())
    if not pages:
        print("Wiki is empty.")
        return

    if _rich:
        table = Table(title=f"Wiki Index  ({len(pages)} pages)", show_lines=True, expand=False)
        table.add_column("#", style="dim", width=4)
        table.add_column("Page", style="bold cyan", min_width=24)
        table.add_column("Summary", style="white", max_width=48)
        table.add_column("Links", style="green", max_width=32)
        table.add_column("Size", style="dim", width=10)

        for i, title in enumerate(pages, 1):
            path = WIKI_DIR / f"{title}.md"
            content = path.read_text()
            summary = next(
                (l.strip() for l in content.splitlines() if l.strip() and not l.startswith("#")),
                ""
            )
            summary = re.sub(r"\*\*([^*]+)\*\*", r"\1", summary)[:80]
            links = sorted(set(re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', content)))
            link_str = ", ".join(links[:3]) + ("…" if len(links) > 3 else "")
            table.add_row(str(i), title, summary, link_str, f"{len(content):,}")

        _console.print(table)
    else:
        print(f"\nWiki Index ({len(pages)} pages)")
        print("-" * 40)
        for i, title in enumerate(pages, 1):
            size = len((WIKI_DIR / f"{title}.md").read_text())
            print(f"  {i:2}. {title} ({size:,} chars)")


def show_log() -> None:
    _header("log")
    log_path = WIKI_DIR / "log.md"
    if not log_path.exists():
        print("No log yet.")
        return
    content = log_path.read_text()
    if _rich:
        _console.print(Panel(Markdown(content), title="[bold yellow]Wiki Log[/]", border_style="yellow"))
    else:
        print(content)


def show_graph() -> None:
    _header("graph")
    pages = json.loads(list_pages())
    if not pages:
        print("Wiki is empty.")
        return

    page_set = set(pages)
    if _rich:
        _console.print("\n[bold]Wiki Link Graph[/]\n")
    else:
        print("\nWiki Link Graph\n")

    for title in pages:
        content = (WIKI_DIR / f"{title}.md").read_text()
        raw_links = sorted(set(re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', content)))
        internal = [l for l in raw_links if l in page_set]
        external = [l for l in raw_links if l not in page_set]

        if _rich:
            parts = [f"[bold cyan]{title}[/] →"]
            for l in internal:
                parts.append(f"[green]{l}[/]")
            for l in external:
                parts.append(f"[dim]{l}[/]")
            _console.print(" ".join(parts))
        else:
            targets = ", ".join(raw_links) if raw_links else "(no links)"
            print(f"  {title} → {targets}")
