# Context Window (LLM)

A **context window** is the total number of [[Tokens]] that a [[Large Language Model]] can process in a single request-response cycle. It covers both input (prompt, system instructions, retrieved documents, conversation history) and output (the model's response) tokens combined.

Think of it as a fixed-size whiteboard — everything the model knows about the current conversation must fit on that whiteboard. Once full, the oldest content is silently dropped or the request is refused.

---

## Tokens vs. Characters vs. Words

| Unit | Approximate Ratio (English) |
|---|---|
| 1 token | ~4 characters |
| 1 token | ~0.75 words |
| 1,000 tokens | ~750 words |
| 100K tokens | ~75,000 words (~150 pages) |

For CJK languages (Chinese, Japanese, Korean), a single character often maps to 1–2 tokens, meaning the same context window holds significantly fewer characters than English words.

---

## Current Token Limits by Model (2026)

| Model | Provider | Context Window | Max Output |
|---|---|---|---|
| GPT-5 | OpenAI | 1,000,000 tokens | 32,768 tokens |
| GPT-4.1 | OpenAI | 1,000,000 tokens | 32,768 tokens |
| Claude Opus 4 | Anthropic | 200,000 tokens | 32,000 tokens |
| Claude Sonnet 4 | Anthropic | 200,000 tokens | 16,000 tokens |
| Gemini 2.5 Pro | Google | 1,000,000 tokens | 65,536 tokens |
| Gemini 2.5 Flash | Google | 1,000,000 tokens | 65,536 tokens |
| DeepSeek V3 | DeepSeek | 128,000 tokens | 8,192 tokens |
| Llama 4 Maverick | Meta | 1,000,000 tokens | 16,384 tokens |
| Mistral Large | Mistral | 128,000 tokens | 8,192 tokens |

Key observations:
- **The 1M club is growing**: GPT-5, GPT-4.1, Gemini 2.5 Pro, Gemini 2.5 Flash, and Llama 4 Maverick all support 1M tokens.
- **Output limits are much smaller**: Even 1M-input models cap output at 8K–65K tokens. The window is asymmetric.
- **Open-source models lag**: DeepSeek V3 and Mistral Large offer 128K, roughly 8× smaller than frontier closed models.

---

## How Context Windows Work

The context window is tied to the model's [[Attention Mechanism]]. [[Transformer]]-based LLMs use self-attention where every token can attend to every other token. The computational cost scales **quadratically** with sequence length — doubling the context window roughly quadruples computation for the attention layers.

Model providers use architectural optimizations such as [[Sliding Window Attention]], sparse attention, ring attention, and efficient KV-cache management to make million-token contexts feasible.

---

## The "Lost in the Middle" Problem

LLMs do not attend to all parts of the context equally. A landmark 2023 paper (Liu et al.) showed that models perform best when relevant information is at the **beginning or end** of the context, and perform significantly worse when it is buried in the middle. This is known as the [[Lost in the Middle]] problem.

---

## Cost Implications

Context window size directly impacts API costs. LLM APIs charge per token for both input and output.

### Cost to Fill Full Context (Input Only, 2026)

| Model | Context Size | Input Price (per 1M tokens) | Cost to Fill Context |
|---|---|---|---|
| GPT-5 | 1M tokens | $2.00 | $2.00 |
| Claude Opus 4 | 200K tokens | $15.00 | $3.00 |
| Claude Sonnet 4 | 200K tokens | $3.00 | $0.60 |
| Gemini 2.5 Pro | 1M tokens | $1.25 / $2.50* | ~$2.25 |
| DeepSeek V3 | 128K tokens | $0.27 | $0.035 |

*Gemini 2.5 Pro: $1.25/1M under 200K tokens, $2.50/1M over 200K tokens.

[[Prompt Caching]] can significantly reduce costs — cached tokens can be 50–90% cheaper.

---

## Practical Strategies

When data exceeds the context window, or when filling it is too expensive or degrades quality, use these strategies:

1. **[[Chunking Strategy|Chunking]] and Selective Retrieval ([[Retrieval-Augmented Generation|RAG]])** — Split documents into chunks (256–1024 tokens), embed them, and retrieve only the top-K most relevant at query time.
2. **Summarization Chains** — Split document into context-fitting chunks, summarize each (map step), then combine summaries into a final summary (reduce step).
3. **Sliding Window with Overlap** — Process overlapping windows (e.g., tokens 0–100K, then 80K–180K) and merge results.
4. **[[Context Compression]]** — Strip boilerplate, pre-summarize verbose sections, remove non-essential markup before sending to the LLM.
5. **Hierarchical Context Management** — Keep critical context (system prompt, instructions) always present, session context loaded per-turn, and on-demand content retrieved as needed.

---

## Choosing the Right Context Size

- **Small (4K–16K tokens)**: Simple chatbots, classification, short-form generation, single-turn Q&A. Cheaper and faster.
- **Medium (32K–128K tokens)**: Document Q&A over single documents, code review of individual files, multi-turn conversations.
- **Large (200K–1M tokens)**: Entire codebase analysis, multi-document reasoning, long research papers, legal contracts, book-length content.

**Decision rule**: Ask "Does the model need to reason across all this data simultaneously, or can the task be decomposed?" If decomposable, use [[Retrieval-Augmented Generation|RAG]] or chunking with a smaller context.

---

## Context Windows and Local Inference

When running models locally (via llama.cpp, vLLM, [[Ollama]]), the KV-cache grows linearly with sequence length. A 70B parameter model at full 128K context may require 80+ GB of VRAM. Most local deployments limit context to 4K–16K tokens to fit hardware constraints.

---

## Future Trends

- **Infinite context via memory systems**: External memory the model reads/writes across turns.
- **Cheaper long contexts**: Prompt caching, speculative decoding, more efficient attention mechanisms.
- **Better mid-context retrieval**: Architectures trained to handle retrieval across the full window, reducing [[Lost in the Middle]].
- **Hybrid retrieval-context approaches**: Long context as "working memory" supplemented by retrieval from larger knowledge bases.

---

## See Also

- [[Tokens]]
- [[Large Language Model]]
- [[Transformer]]
- [[Attention Mechanism]]
- [[Sliding Window Attention]]
- [[Lost in the Middle]]
- [[Retrieval-Augmented Generation]]
- [[Chunking Strategy]]
- [[Context Compression]]
- [[Prompt Caching]]
- [[Embedding Model]]



---

## DeepSeek-V4 Update (April 2026)

With the release of [[DeepSeek-V4]], the table above is now outdated. [[DeepSeek-V4-Pro]] and [[DeepSeek-V4-Flash]] both support **1M-token context windows** as the default (matching GPT-5, Gemini 2.5 Pro, and other frontier models). The previous DeepSeek V3's 128K limit has been superseded.

The 1M context is enabled by a novel [[DeepSeek Sparse Attention]] (DSA) mechanism with token-wise compression, delivering drastically reduced compute and memory costs for long sequences.
