# Personal Knowledge Base

**Summary**: A system for collecting, organizing, and retrieving personal knowledge — notes, documents, research, and references — optimized for the owner's use, potentially queried by [[Large Language Model|LLMs]] in the [[Karpathy's LLM Wiki]] pattern.

**Tags**: #knowledge-management #note-taking #productivity #second-brain

---

## Overview

A personal knowledge base (PKM — Personal Knowledge Management) is a system for storing and retrieving information an individual finds valuable. Traditional systems ([[Notion]], [[Google Docs]], browser bookmarks, sticky notes) are optimized for human browsing — the user remembers where something is and navigates to it.

## LLM-Optimized Knowledge Bases

The [[Karpathy's LLM Wiki]] pattern introduces a shift: instead of designing for human navigation, design for [[Large Language Model|LLM]] reading. The user describes what they need in plain language, and the model finds and synthesizes information across the entire knowledge base.

### Comparison

| Aspect | Traditional Notes App | LLM Wiki |
|---|---|---|
| Access method | Browse, search, click | Natural language query |
| Format | Proprietary or semi-structured | Plain [[Markdown]] |
| Control | Vendor-dependent | Local files, fully owned |
| Query capability | Keyword search | Semantic synthesis across files |

## Key Practices

- **Write summaries**: A one-line summary at the top of each note helps models decide relevance quickly.
- **Use consistent terminology**: Pick one term for a concept and use it everywhere.
- **Link notes**: [[WikiLinks]] create a graph that models can traverse.
- **Keep notes focused**: Specific, single-topic files are easier to query than catch-all documents.
- **Use an inbox**: Dump rough notes into an inbox folder, then have [[Claude Code]] help organize them.

## Scaling

For small knowledge bases (hundreds of notes), direct file-reading by models like [[Claude Code]] works well. For larger scales, a [[Retrieval-Augmented Generation|RAG]] layer using [[Vector Store|vector embeddings]] can add semantic search.

## Related

- [[Karpathy's LLM Wiki]]
- [[Claude Code]]
- [[Obsidian]]
- [[Markdown]]
- [[MindStudio]]
