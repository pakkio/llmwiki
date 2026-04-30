# Lost in the Middle

The **"Lost in the Middle"** problem refers to the empirical finding that [[Large Language Model|Large Language Models]] perform best when relevant information is placed at the **beginning or end** of the [[Context Window]], and perform significantly worse when it is buried in the middle of the context.

This phenomenon was systematically documented in a landmark 2023 paper by Liu et al.

---

## The Problem

In a [[Context Window]], LLMs do not attend to all parts of the input equally due to the nature of their [[Attention Mechanism]]. When multiple pieces of information are provided (e.g., retrieved document chunks in a [[Retrieval-Augmented Generation|RAG]] pipeline), the model tends to:

- **Focus on content near the start** — tokens close to the beginning of the prompt receive more attention.
- **Focus on content near the end** — tokens immediately preceding the generation point also receive strong attention.
- **Neglect content in the middle** — information positioned in the middle of the context is more likely to be ignored or underweighted.

---

## Practical Implications

Imagine building a [[Retrieval-Augmented Generation]] pipeline that retrieves 20 document chunks and stuffs them into the prompt. If the most relevant chunk lands in positions 8–12 out of 20, the model might effectively ignore it — even though it is right there in the context.

This is particularly dangerous because:
- The most relevant chunks from retrieval may not be placed at the optimal positions.
- Naive concatenation of retrieved results often places medium-relevance chunks in the middle.
- Users may assume that because information is in the context, the model will use it.

---

## Mitigation Strategies

Newer models (e.g., [[Claude Opus 4]], GPT-5) have partially mitigated this problem, but it has not disappeared. Best practices include:

1. **Put the most important information first** — right after the system prompt.
2. **Put instructions at the end** — closest to where the model generates its response.
3. **Avoid padding** with marginally relevant content just because context space is available.
4. **Use explicit markers** — headers, XML tags, or numbered sections to help the model locate information.
5. **Re-rank retrieved chunks** so the most relevant ones are placed first and last in the context.

---

## Relationship to Context Window Size

The "Lost in the Middle" effect contributes to the principle that **more context is not always better**. Even with a million-token [[Context Window]], model accuracy can degrade as context length increases — the model has more "hay" to search through for the "needle."

In benchmark tests, most models achieve near-perfect "needle in a haystack" scores at short contexts but show degradation at the extremes of their context windows.

---

## See Also

- [[Context Window]]
- [[Retrieval-Augmented Generation]]
- [[Attention Mechanism]]
- [[Large Language Model]]
- [[Chunking Strategy]]
