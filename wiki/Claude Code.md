# Claude Code

**Summary**: Anthropic's terminal-based coding agent that runs in the local environment with direct [[filesystem]] access, used as the primary query interface for [[Karpathy's LLM Wiki]].

**Tags**: #claude #coding-agent #terminal #anthropic

---

## Overview

Claude Code is [[Anthropic]]'s terminal-based agent. Unlike Claude accessed through a browser, Claude Code runs in the user's local environment and has direct access to the filesystem. This makes it genuinely useful as a [[Personal Knowledge Base]] interface — the model works directly with local files rather than requiring copy-pasting.

## Capabilities

- Read specific files or entire directories
- Search across files for relevant content
- Create new files or update existing ones
- Execute shell commands to search, filter, or organize notes
- Write and edit code

## Installation

Requires [[Node.js]]. Install via npm:

```bash
npm install -g @anthropic-ai/claude-code
```

Then authenticate with an Anthropic account.

## Usage in LLM Wiki Workflow

Navigate to the wiki folder and launch Claude:

```bash
cd ~/wiki
claude
```

Then ask natural-language questions. Claude will:
1. Read through [[Markdown]] files in the wiki
2. Identify what is relevant
3. Produce grounded answers citing source files
4. Optionally update notes or create new ones

## Context Window

Claude 3.5 Sonnet supports approximately 200,000 tokens, enough to read tens of thousands of words in a single session. For most personal wikis (up to a few hundred focused notes), this is more than sufficient.

## Other Models

The [[Karpathy's LLM Wiki|markdown wiki pattern]] works with any model that can read files. Claude Code is the most natural interface because it is built for local filesystem access, but GPT-4, [[Gemini]], or others can be pointed at markdown files through similar agent frameworks.

## Related

- [[Karpathy's LLM Wiki]]
- [[Obsidian]]
- [[Personal Knowledge Base]]
- [[Markdown]]
- [[MindStudio]]
