# Chunking Strategy

A **chunking strategy** defines how documents are split into smaller pieces (chunks) before being embedded and indexed in a [[Vector Store]]. It is a critical design decision in [[Retrieval-Augmented Generation]] (RAG) pipelines.

---

## Role in RAG

When building a [[Retrieval-Augmented Generation]] system, documents are too long to embed and use as a single piece of context. A chunking strategy determines:

- **Chunk size** — how many tokens or characters per chunk
- **Chunk overlap** — whether adjacent chunks share overlapping content to preserve context boundaries
- **Splitting method** — splitting by tokens, characters, sentences, paragraphs, or semantic boundaries

The choice of chunking strategy directly impacts retrieval quality: chunks that are too small may lose context, while chunks that are too large may dilute relevance or exceed the context window of the [[Large Language Model]].

---

## Common Approaches

- **Fixed-size token chunks** — simple but can cut through sentences mid-thought
- **Recursive character splitting** — split on natural boundaries (paragraphs, sentences) with preferred delimiters
- **Semantic chunking** — uses an [[Embedding Model]] to detect topic boundaries before splitting
- **Document-structure-aware splitting** — respects markdown headings, section breaks, or other structural markers

---

## See Also

- [[Retrieval-Augmented Generation]]
- [[Embedding Model]]
- [[Vector Store]]
- [[Large Language Model]]
