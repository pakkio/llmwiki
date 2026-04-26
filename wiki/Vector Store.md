# Vector Store

A **vector store** (or vector database) is a system designed to index, store, and perform similarity search over dense vector embeddings. It is a core component of [[Retrieval-Augmented Generation]] (RAG) pipelines.

---

## Role in RAG

In a [[Retrieval-Augmented Generation]] system, the vector store:

1. **Indexes** embeddings produced by an [[Embedding Model]] for a corpus of documents.
2. **Retrieves** the most similar embeddings to a given query embedding using distance metrics such as cosine similarity or Euclidean distance.
3. Returns the document chunks (or references) associated with the nearest neighbor embeddings to provide context to a [[Large Language Model]].

---

## Examples

- **Pinecone** — a managed, cloud-native vector database
- **Chroma** — an open-source embedding database designed for AI applications
- **FAISS** — a library for efficient similarity search and clustering of dense vectors, developed by Facebook AI Research

---

## See Also

- [[Retrieval-Augmented Generation]]
- [[Embedding Model]]
- [[Chunking Strategy]]
- [[Large Language Model]]
