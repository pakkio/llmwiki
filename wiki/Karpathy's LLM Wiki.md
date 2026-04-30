# Karpathy's LLM Wiki

**Summary**: A personal knowledge management workflow pattern that uses structured [[Markdown]] files, queried by an [[Large Language Model|LLM]] (typically through [[Claude Code]]), instead of traditional browsing or search.

**Tags**: #knowledge-management #workflow #llm #personal-knowledge-base

---

## Overview

Andrej Karpathy — co-founder of OpenAI and former Tesla AI director — has advocated for a simple idea: your personal notes and documents, organized in plain [[Markdown]], can become a knowledge base that an LLM can reason over directly. He calls this an **LLM wiki**.

Unlike traditional [[Personal Knowledge Base|note-taking apps]] optimized for human browsing (search, click, navigate), an LLM wiki is optimized for a model to read on your behalf. The user describes what they need in plain language, and the model finds and synthesizes information across the entire knowledge base.

## Architecture

The system has three minimal components:

1. **A folder of [[Markdown]] files** — the knowledge base, containing research notes, meeting summaries, project docs, book notes, code snippets, etc.
2. **A consistent structure within each file** — using a title, summary line, tagged topics, and structured content so the model can quickly locate relevant information.
3. **[[Claude Code]] as the query interface** — a terminal-based agent that reads files directly from the local filesystem, answers questions, and can update or add notes.

No database, vector embeddings, or servers are required for the basic setup.

## Why Markdown

Karpathy's approach centers on [[Markdown]] because it is:
- **Portable and future-proof** — `.md` files open in any editor, on any OS, forever.
- **Read natively by LLMs** — Models like Claude are trained on vast amounts of markdown content (GitHub READMEs, docs), so headers, lists, and code blocks are interpreted as structure.
- **Lock-in free** — Sync via git, open in [[Obsidian]], VS Code, or a terminal. The knowledge is fully owned by the user.

## Query Example

```bash
cd ~/wiki
claude
```

Then ask:
- *"What notes do I have about machine learning interpretability?"*
- *"Summarize everything in my research folder related to RAG systems."*
- *"Find any notes where I mentioned the vendor Acme Corp."*

Claude reads the files, identifies relevance, and cites which files it drew from.

## Best Practices

- Write a one-line summary at the top of each note — Claude uses this to decide relevance without reading the full file.
- Use consistent terminology (pick one term like "RAG" or "retrieval augmented generation" and stick with it).
- Link notes with [[WikiLinks]] — Claude can follow these connections to build a richer reasoning graph.
- Keep notes focused — ten 1,000-word notes are better than one 10,000-word catch-all.
- Use an `inbox/` folder for rough notes, then have Claude help triage them.

## Scaling Up

For wikis up to a few hundred notes, Claude's direct file-reading (context window of ~200,000 tokens) is sufficient. Beyond that, a [[Retrieval-Augmented Generation|RAG]] layer (e.g., [[Vector Store|vector embeddings]] via [[LlamaIndex]]) can be added for semantic search.

## Related

- [[Claude Code]]
- [[Obsidian]]
- [[Personal Knowledge Base]]
- [[Markdown]]
- [[MindStudio]]
