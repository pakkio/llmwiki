# Attention Mechanism

The **attention mechanism** is a core component of the [[Transformer]] architecture and many modern [[Deep Learning]] models. It allows the model to dynamically weigh the importance of different tokens or features when generating each output, enabling it to focus on the most relevant parts of the input.

---

## Definition

The attention mechanism computes a weighted sum of **values** (V), where the weights are determined by the compatibility between **queries** (Q) and **keys** (K). The general formulation is:

\[
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
\]

This is known as **scaled dot-product attention**, where:

- **Q** = Queries — representations of what the model is looking for
- **K** = Keys — representations of what each token "offers"
- **V** = Values — the actual information to aggregate
- **dₖ** = dimension of the keys, used as a scaling factor to prevent vanishing gradients in the softmax

The scaling factor √dₖ is critical: without it, the dot products grow large in magnitude, pushing the softmax into regions with extremely small gradients.

---

## Variants

### Self-Attention (Intra-Attention)

In **self-attention**, the queries, keys, and values all come from the same source sequence. This allows every token to attend to every other token in the sequence, capturing long-range dependencies in a single layer. Self-attention is used in both the encoder and decoder of the [[Transformer]].

### Cross-Attention (Encoder-Decoder Attention)

In **cross-attention**, the queries come from one sequence (typically the decoder) while the keys and values come from another sequence (typically the encoder). This enables the decoder to attend to relevant information from the encoded input. Cross-attention is a key component in sequence-to-sequence models like the original [[Transformer]].

### Multi-Head Attention

Rather than performing a single attention function, **multi-head attention** runs *h* parallel attention heads, each with learned linear projections of Q, K, and V. Each head learns different relationships (e.g., syntactic vs. semantic, local vs. global). The outputs are concatenated and projected again:

\[
\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O
\]

where each head = Attention(QWᵢ^Q, KWᵢ^K, VWᵢ^V).

### Masked (Causal) Self-Attention

Used in autoregressive decoders (e.g., [[GPT]] models), this variant applies a mask to prevent tokens from attending to future positions during generation. The mask sets the attention scores for future tokens to −∞ before the softmax, ensuring each position can only depend on itself and preceding tokens.

---

## Historical Context

The attention mechanism was introduced **before Transformers** by Bahdanau et al. (2015) in the context of sequence-to-sequence models with [[Recurrent Neural Networks]] (RNNs). Bahdanau attention allowed the decoder to dynamically align with relevant encoder hidden states at each decoding step, addressing the bottleneck of fixed-length context vectors that earlier encoder-decoder [[RNN]] models suffered from.

The key innovation of the [[Transformer]] (Vaswani et al., 2017) was to **replace recurrence entirely with attention**, demonstrating that scaled dot-product attention alone — without any sequential processing — could achieve state-of-the-art results in machine translation and other tasks.

---

## Advantages

- **Long-range dependencies**: Direct connections between any two positions, regardless of distance
- **Parallelization**: Unlike [[RNN]]s, all positions can be computed simultaneously
- **Interpretability**: Attention weights can be visualized to show what the model is "looking at"

---

## Limitations

- **Quadratic complexity**: Self-attention scales as O(n²) with sequence length n
- **No positional awareness**: Attention is permutation-invariant, so [[Positional Encoding]] must be added separately
- **Memory usage**: Attention matrices grow quadratically, limiting long-context processing

---

## See Also

- [[Transformer]]
- [[Large Language Model]]
- [[Positional Encoding]]
- [[Embedding Model]]
- [[Natural Language Processing]]

---

## References

- Bahdanau, D., Cho, K., & Bengio, Y. (2015). *Neural Machine Translation by Jointly Learning to Align and Translate*. ICLR.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS.
