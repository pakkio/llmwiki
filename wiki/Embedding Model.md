# Embedding Model

An **embedding model** is a neural network that converts text (or other data modalities) into dense vector representations, also called *embeddings*. These vectors capture semantic meaning such that similar texts are positioned close together in the vector space.

In a [[Retrieval-Augmented Generation]] (RAG) pipeline, the embedding model is used to encode both documents and user queries into a shared vector space, enabling similarity search via a [[Vector Store]].

---

## Role in RAG

The embedding model plays a crucial role in the retrieval stage of [[Retrieval-Augmented Generation]]:

1. During indexing: all documents in the corpus are embedded and stored in a [[Vector Store]].
2. At query time: the user's query is embedded using the same model.
3. The [[Vector Store]] retrieves document embeddings most similar to the query embedding.

Retrieval quality depends heavily on the performance of the embedding model.

---

## Examples

- **text-embedding-ada-002** — OpenAI's embedding model, commonly used in RAG systems
- Other popular embedding models include Sentence-BERT, Instructor, and E5

---

## See Also

- [[Retrieval-Augmented Generation]]
- [[Vector Store]]
- [[Chunking Strategy]]
- [[Large Language Model]]
- [[Transformer]]
