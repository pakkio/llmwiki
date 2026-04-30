# Sliding Window Attention

**Sliding Window Attention** is an architectural optimization used in some [[Transformer]]-based [[Large Language Model|Large Language Models]] where each token only attends to the **N most recent tokens** rather than the entire sequence. This reduces the quadratic computational cost of full [[Attention Mechanism|self-attention]] to a linear cost with respect to sequence length.

---

## How It Works

In standard full attention, every token attends to every other token in the sequence, resulting in O(n²) complexity. In sliding window attention:

- A **window size** W is defined (e.g., 4,096 tokens).
- Each token attends only to the previous W tokens (and itself).
- Tokens beyond the window boundary are not directly connected.
- The attention matrix becomes banded rather than dense.

This means the model can accept theoretically unlimited input length while keeping computation bounded.

---

## Trade-offs

| Aspect | Sliding Window | Full Attention |
|---|---|---|
| Computational cost | O(n × W) — linear | O(n²) — quadratic |
| Long-range dependencies | Weak (indirect, via stacked layers) | Direct (any token to any token) |
| Memory usage | Lower (banded attention matrix) | Higher (dense attention matrix) |
| Context window limit | Larger possible contexts | Harder to scale |

**Key trade-off**: Tokens far apart in the context have weaker connections. Information must propagate through multiple layers to travel across the window, which can dilute long-range reasoning.

---

## Usage in Models

- **Mistral's earlier models** used sliding window attention with a window of 4,096 tokens, even though they could accept longer inputs.
- Most frontier models in 2026 use **full attention** across the entire [[Context Window]], sometimes combined with other optimizations like grouped-query attention (GQA) to manage memory usage.

---

## Relationship to Context Window Strategies

Sliding window attention is an architectural technique implemented **inside the model**. This is distinct from the [[Context Window|context management strategy]] of using a **sliding window with overlap** at the application layer, where a developer processes tokens 0–100K, then slides to 80K–180K, and merges results. The application-layer approach works with any model regardless of its internal attention mechanism.

---

## See Also

- [[Attention Mechanism]]
- [[Context Window]]
- [[Transformer]]
- [[Large Language Model]]
