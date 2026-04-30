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



---

## Context Windows

Every LLM has a [[Context Window]] — the total number of [[Tokens]] it can process in a single request-response cycle. This includes both input (prompt, system instructions, conversation history) and output. Models in 2026 range from 128K tokens (DeepSeek V3, Mistral Large) to 1M tokens (GPT-5, Gemini 2.5 Pro, Llama 4 Maverick).

The [[Context Window]] size directly impacts architectural decisions in applications like [[Retrieval-Augmented Generation]], and strategies such as [[Chunking Strategy|chunking]], [[Context Compression]], and sliding windows are used to manage it.
