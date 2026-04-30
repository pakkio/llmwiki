# DeepSeek Sparse Attention

**DeepSeek Sparse Attention (DSA)** is a novel attention mechanism introduced in [[DeepSeek-V4]]. It combines token-wise compression with sparsity to achieve world-leading long-context efficiency, drastically reducing both compute and memory costs compared to standard [[Attention Mechanism|attention]].

---

## Overview

DSA is the core architectural innovation enabling [[DeepSeek-V4]]'s 1M-token [[Context Window]] as a default standard. It addresses the quadratic complexity problem of standard [[Transformer]] self-attention, where computational cost scales as O(n²) with sequence length n.

---

## Key Components

### Token-wise Compression
Input tokens are compressed before attention computation, reducing the effective sequence length that needs to be processed. This compression preserves essential semantic information while lowering the token count.

### Sparse Attention Patterns
DSA applies sparsity to the attention matrix, meaning each token only attends to a selected subset of other tokens rather than the full sequence. This is conceptually related to [[Sliding Window Attention]] and other sparse attention techniques, but with custom patterns optimized for the DeepSeek-V4 architecture.

---

## Benefits

| Aspect | Benefit |
|---|---|
| **Compute efficiency** | Drastically reduced FLOPs for long sequences |
| **Memory efficiency** | Lower KV-cache memory requirements |
| **Context length** | Makes 1M-token contexts practical and economical |
| **Quality** | Maintains strong reasoning and knowledge capabilities |

---

## Impact

DSA enables [[DeepSeek-V4-Pro]] (1.6T total parameters) and [[DeepSeek-V4-Flash]] (284B total parameters) to support 1M context windows as the default across all official DeepSeek services — a significant leap from the previous generation's 128K-token limit.

---

## See Also

- [[DeepSeek-V4]]
- [[DeepSeek-V4-Pro]]
- [[DeepSeek-V4-Flash]]
- [[Attention Mechanism]]
- [[Transformer]]
- [[Context Window]]
- [[Sliding Window Attention]]
- [[Context Compression]]
