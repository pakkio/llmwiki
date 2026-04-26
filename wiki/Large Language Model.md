# Large Language Model (LLM)

A **Large Language Model (LLM)** is a type of neural network model, typically based on the [[Transformer]] architecture, trained on vast amounts of text data to generate human-like text. LLMs are the generative component in [[Retrieval-Augmented Generation]] (RAG) systems.

---

## Role in RAG

In a [[Retrieval-Augmented Generation]] pipeline, the LLM:

1. Receives retrieved document chunks from a [[Vector Store]] as context.
2. Receives the user's original query.
3. Generates a final answer **grounded in** the retrieved context, rather than relying solely on parametric knowledge.

This reduces hallucination and allows the system to incorporate up-to-date or domain-specific information without retraining.

---

## Examples

- **GPT-4** (OpenAI)
- **Claude** (Anthropic)
- Other models commonly used in RAG include GPT-3.5, LLaMA, and Mistral

---

## See Also

- [[Retrieval-Augmented Generation]]
- [[Transformer]]
- [[Embedding Model]]
- [[Vector Store]]
- [[Chunking Strategy]]
- [[Next-Token Prediction]]
