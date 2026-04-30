# Markdown

**Summary**: A lightweight markup language using plain text formatting, serving as the foundational format for [[Karpathy's LLM Wiki]] because of its portability, LLM-native readability, and zero lock-in.

**Tags**: #markdown #format #writing #knowledge-management

---

## Overview

Markdown (`.md` files) is a lightweight markup language that uses plain text formatting conventions. It is the recommended format for [[Karpathy's LLM Wiki]] because it is the ideal medium for [[Large Language Model|LLM]]-readable knowledge bases.

## Why Markdown for LLM Wikis

### Portable and Future-Proof
A `.md` file is a text file. It opens in any editor, on any operating system, forever. No dependency on a company staying in business or an app maintaining backward compatibility.

### LLMs Read Markdown Natively
Models like [[Claude Code|Claude]] are trained on enormous amounts of markdown content — GitHub READMEs, documentation sites, forums. The syntax is part of their understanding. Headers, bullet points, code blocks, and bold text are interpreted as structure, not noise.

### It Forces Clarity
Writing in markdown discourages half-finished, poorly organized notes. Headers require naming sections. Lists require separating items. The format nudges toward clarity.

### Plain Text Means No Lock-In
Markdown files can be synced with [[git]], opened in [[VS Code]], viewed in [[Obsidian]], pushed to a private GitHub repo, or read in a terminal. The knowledge is owned in the most literal sense.

## Structure for Queryability

In [[Karpathy's LLM Wiki]], a consistent markdown structure is key. A recommended template includes:

- A title (`# Title`)
- A summary line
- Tags
- Creation and update dates
- Content sections separated by `---`
- [[WikiLinks]] to related notes

## Related

- [[Karpathy's LLM Wiki]]
- [[Claude Code]]
- [[Obsidian]]
- [[Personal Knowledge Base]]
- [[MindStudio]]
