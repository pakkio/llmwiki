# Obsidian

**Summary**: A local-first [[Markdown]] editor with a strong plugin ecosystem and clean interface, recommended as the front-end for managing [[Karpathy's LLM Wiki]].

**Tags**: #note-taking #markdown-editor #knowledge-management #obsidian

---

## Overview

Obsidian is the recommended front-end for the [[Karpathy's LLM Wiki]] workflow. It is a local-first markdown editor — files stay on the user's disk and Obsidian is simply how they are read and written. A "vault" in Obsidian is just a folder containing plain [[Markdown]] files.

## Why Obsidian for an LLM Wiki

- **Local-first**: Files remain on the user's machine, not in a proprietary system.
- **[[WikiLinks]] support**: Obsidian's `[[wiki links]]` format creates connections between notes that [[Claude Code]] can follow.
- **Graph view**: Visualizes relationships between notes.
- **Backlinks**: Shows which notes reference the current one.
- **Plugin ecosystem**: Extensible for additional functionality.
- **Not required**: Claude Code does not depend on Obsidian — any editor (VS Code, Typora, iA Writer, Zed, Vim) works. Obsidian is recommended for its management features.

## Setup for LLM Wiki

### Step 1: Create a Vault
Download Obsidian from the official site. Create a new vault in a folder (e.g., `~/wiki` or `~/Documents/llm-wiki`).

### Step 2: Define a Note Template
Create `_templates/note.md`:

```markdown
# undefined

**Summary**: One sentence describing this note.
**Tags**: #topic1 #topic2
**Created**: 2026-04-06T00:00:00+00:00
**Last Updated**: 2026-04-06T00:00:00+00:00

---

## Content

Write the main content here.

## Related Notes

- [[Note Title]]
```

### Step 3: Organize Into Folders
Start with 4–5 top-level folders:

```
wiki/
├── _templates/
├── projects/
├── research/
├── reference/
├── meetings/
└── inbox/
```

The `inbox/` folder is for rough notes not yet organized. [[Claude Code]] can help triage them.

## Related

- [[Karpathy's LLM Wiki]]
- [[Claude Code]]
- [[Personal Knowledge Base]]
- [[Markdown]]
- [[MindStudio]]
