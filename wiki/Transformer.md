# Transformer (Neural Network)

**Transformers** are a class of deep learning architectures introduced in the 2017 paper *"Attention Is All You Need"* by Vaswani et al. Unlike earlier sequence models such as [[Recurrent Neural Networks]] (RNNs) or [[Long Short-Term Memory]] (LSTM) networks, Transformers rely entirely on an [[Attention Mechanism]] and do not require sequential data processing, enabling massive parallelization during training.

Transformers have become the dominant architecture in [[Natural Language Processing]] (NLP) and have been extended to computer vision, reinforcement learning, and multimodal AI.

---

## Architecture

The Transformer follows an **encoder-decoder structure**, though many modern variants use only the encoder (e.g., [[BERT]]) or only the decoder (e.g., [[GPT]]).

### Core Components

1. **Input Embeddings** — Token sequences are mapped to dense vector representations.
2. **Positional Encoding** — Since Transformers have no inherent notion of sequence order, sinusoidal or learned positional encodings are added to input embeddings.
3. **Multi-Head Self-Attention** — The key innovation. It computes attention scores between every pair of positions in the sequence, allowing the model to capture long-range dependencies.
4. **Feed-Forward Networks (FFNs)** — Position-wise fully connected layers applied independently to each position.
5. **Add & Normalization** — Residual connections followed by layer normalization, applied after each sub-layer.
6. **Masked Self-Attention** — In the decoder, attention is masked to prevent attending to future tokens (causal/autoregressive masking).
7. **Cross-Attention** — In the decoder, attention over the encoder's output representations.

### Attention in the Transformer

The Transformer uses **scaled dot-product attention** and **multi-head attention** as described in the [[Attention Mechanism]] page.

---

## Training

Transformers are typically trained using:
- **Loss function**: [[Cross-Entropy Loss]] for language modeling tasks
- **Optimizer**: [[Adam]] or AdamW
- **Learning rate schedule**: A warmup stage followed by cosine or inverse-square decay
- **Regularization**: [[Dropout]], label smoothing, and weight decay

They are highly parallelizable and benefit from training on large corpora using [[Graphics Processing Unit]] (GPU) clusters.

---

## Key Advantages

| Feature | Benefit |
|---|---|
| **Parallelization** | Unlike RNNs, all positions can be processed simultaneously |
| **Long-range dependencies** | Direct connections between any two tokens regardless of distance |
| **Transfer learning** | Pre-trained Transformers (e.g., BERT, GPT) can be fine-tuned for many tasks |
| **Scalability** | Larger models and more data consistently improve performance |

---

## Limitations

- **Quadratic complexity** — Self-attention scales as O(n²) with sequence length n, making very long sequences expensive.
- **Fixed context window** — Models cannot attend beyond a predefined maximum sequence length.
- **No inherent positional understanding** — Positional encodings are an imperfect workaround.
- **Training cost** — Large Transformers require enormous compute resources.

---

## Major Variants

### Encoder-Only
- **[[BERT]]** (Bidirectional Encoder Representations from Transformers)
- **[[RoBERTa]]** (Robustly Optimized BERT Approach)
- **[[ALBERT]]**, **[[DistilBERT]]** (lighter variants)

### Decoder-Only (Autoregressive)
- **[[GPT]]** family (GPT-2, GPT-3, GPT-4, GPT-4o)
- **[[LLaMA]]**, **[[Mistral]]**
- **[[Chinchilla]]** (scaling law optimized)

### Encoder-Decoder
- **Original Transformer** (Vaswani et al.)
- **[[T5]]** (Text-to-Text Transfer Transformer)
- **[[BART]]**

### Vision Transformers
- **[[ViT]]** (Vision Transformer) — applies Transformers directly to image patches
- **[[Swin Transformer]]** — hierarchical, window-based attention

---

## Applications

- **Natural Language Processing**: Translation, summarization, question answering, text generation
- **Computer Vision**: Image classification, object detection, segmentation
- **Multimodal**: Image captioning, text-to-image generation (e.g., [[DALL-E]], [[Stable Diffusion]])
- **Audio/Speech**: Speech recognition, text-to-speech (e.g., [[Whisper]])
- **Reinforcement Learning**: Decision Transformers for sequential decision-making
- **Biology**: Protein folding ([[AlphaFold2]]), drug discovery

---

## Historical Context

| Year | Milestone |
|---|---|
| 2015 | Bahdanau et al. introduce attention for [[RNN]]-based sequence-to-sequence models |
| 2017 | *"Attention Is All You Need"* published (Vaswani et al., Google) — the Transformer is born |
| 2018 | GPT-1 and BERT introduced, sparking the "Transformer revolution" in NLP |
| 2020 | GPT-3 demonstrates few-shot learning at scale |
| 2020 | Vision Transformer (ViT) shows Transformers rival CNNs in vision |
| 2022 | ChatGPT (GPT-3.5) brings Transformers to mainstream public use |
| 2023 | GPT-4, LLaMA, and open-source model ecosystems emerge |
| 2024+ | Continued scaling, multimodal models, and efficiency improvements |

---

## See Also

- [[Attention Mechanism]]
- [[Natural Language Processing]]
- [[Deep Learning]]
- [[Large Language Model]]
- [[Tokenization]]
- [[Positional Encoding]]
- [[Self-Supervised Learning]]

---

## References

- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS.
- Devlin, J., et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL.
- Brown, T., et al. (2020). *Language Models are Few-Shot Learners*. NeurIPS.
- Dosovitskiy, A., et al. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. ICLR.
- Bahdanau, D., Cho, K., & Bengio, Y. (2015). *Neural Machine Translation by Jointly Learning to Align and Translate*. ICLR.
