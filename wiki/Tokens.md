# Tokens

**Tokens** are the fundamental units that [[Large Language Model|Large Language Models]] read and produce. They are the atomic pieces of text that a model processes — roughly ¾ of a word in English, though the exact mapping depends on the tokenizer used by the model.

---

## Token Count Approximations

For English text:

| Unit | Approximate Tokens |
|---|---|
| 1 word | ~1.33 tokens |
| 1 character | ~0.25 tokens |
| 1,000 tokens | ~750 words |
| 100K tokens | ~75,000 words (~150 pages) |

For CJK languages (Chinese, Japanese, Korean), a single character often maps to 1–2 tokens, meaning the same [[Context Window]] holds significantly fewer characters than English words.

---

## Role in Context Windows

The [[Context Window]] of an LLM is measured in tokens, not words or characters. When you send a prompt to an LLM API, both the input and the model's output count against the context window limit. A model with a 128K context window can handle 128,000 tokens total — if your input uses 100K tokens, the model only has 28K tokens left for its response.

---

## Tokenization

The process of converting text into tokens is called **tokenization**, performed by a **tokenizer** (e.g., Byte-Pair Encoding, WordPiece, SentencePiece). Different models may use different tokenizers, so the same text can produce different token counts across models.

---

## See Also

- [[Context Window]]
- [[Large Language Model]]
- [[Transformer]]
- [[Retrieval-Augmented Generation]]
