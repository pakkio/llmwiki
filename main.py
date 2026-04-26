#!/usr/bin/env python3
"""
llmwiki — LLM-powered personal knowledge base (Karpathy-style)

Commands:
  ingest <file>        Extract concepts from a file and write wiki pages
  ingest -             Read from stdin
  query  <question>    Answer a question using only the wiki as source
  lint                 Health-check the wiki (orphans, contradictions, gaps)
  index                List all pages (title, summary, links, size)
  show   <title>       Render a wiki page
  log                  Show the operation log
  graph                Show the [[WikiLink]] graph between pages
"""
import argparse
import sys
from ingest import ingest, ingest_file
from query import query
from lint import lint
from display import show_index, show_page, show_log, show_graph, show_help


def main():
    parser = argparse.ArgumentParser(
        prog="llmwiki",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=False)

    p = sub.add_parser("ingest", help="Ingest a file (or - for stdin) into the wiki")
    p.add_argument("file", nargs="?", default="-", help="File path, or - for stdin (default)")

    q = sub.add_parser("query", help="Ask a question grounded in the wiki")
    q.add_argument("question", nargs="+", help="Your question")
    q.add_argument("--no-cache", dest="no_cache", action="store_true", help="Bypass QA cache (force fresh answer)")

    sub.add_parser("lint", help="Health-check the wiki (orphans, contradictions, gaps)")
    sub.add_parser("index", help="List all wiki pages")

    s = sub.add_parser("show", help="Render a wiki page")
    s.add_argument("title", help="Page title (exact, no .md)")

    sub.add_parser("log", help="Show the operation log")
    sub.add_parser("graph", help="Show the WikiLink graph")
    sub.add_parser("help", help="Show usage help")

    args = parser.parse_args()

    if not args.cmd:
        show_help()
        return

    if args.cmd == "ingest":
        if args.file and args.file != "-":
            result = ingest_file(args.file)
        else:
            text = sys.stdin.read()
            result = ingest(text)
        print("\n" + result)

    elif args.cmd == "query":
        result = query(" ".join(args.question), use_cache=not args.no_cache)
        print("\n" + result)

    elif args.cmd == "lint":
        result = lint()
        print("\n" + result)

    elif args.cmd == "index":
        show_index()

    elif args.cmd == "show":
        show_page(args.title)

    elif args.cmd == "log":
        show_log()

    elif args.cmd == "graph":
        show_graph()

    elif args.cmd == "help":
        show_help()


if __name__ == "__main__":
    main()
