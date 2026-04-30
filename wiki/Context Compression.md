# Context Compression

**Context compression** is a strategy for managing [[Context Window]] usage by reducing the size of input text before sending it to a [[Large Language Model]]. The goal is to retain essential information while minimizing token count, saving both cost and model attention capacity.

---

## Techniques

Common compression methods include:

1. **Remove redundancy** — Strip boilerplate, headers, footers, and repeated sections from documents.
2. **Pre-summarization** — Use a smaller, cheaper model to summarize verbose sections before injecting them into the main prompt.
3. **Selective extraction** — Extract only relevant sections using keyword matching or a lightweight [[Embedding Model|retriever]].
4. **Markup stripping** — Remove HTML tags, markdown formatting, and other non-essential markup.

A 100K-token document might compress to 20K tokens with minimal information loss.

---

## Benefits

- **Reduced cost** — Fewer input tokens means lower API bills.
- **Better model attention** — The model has less "hay" to search through, reducing the [[Lost in the Middle]] effect.
- **Lower latency** — Shorter inputs process faster.
- **Larger effective capacity** — Compressed content can fit into a smaller [[Context Window]].

---

## Relationship to Other Strategies

Context compression is often combined with:

- **[[Chunking Strategy|Chunking]] and [[Retrieval-Augmented Generation|RAG]]** — Compress individual chunks before embedding or before passing them to the LLM.
- **Summarization Chains** — The map step in a map-reduce summarization pattern is a form of compression.
- **Hierarchical Context Management** — Compressed summaries can serve as the persistent top-level context.

---

## See Also

- [[Context Window]]
- [[Large Language Model]]
- [[Retrieval-Augmented Generation]]
- [[Chunking Strategy]]
- [[Lost in the Middle]]
- [[Tokens]]
