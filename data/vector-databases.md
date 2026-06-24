# Vector Databases

A vector database stores embeddings and makes it fast to find the vectors most
similar to a given query vector. This operation is called nearest-neighbor
search. A naive implementation compares the query against every stored vector,
which becomes slow as the collection grows.

To stay fast, vector databases use an Approximate Nearest Neighbor (ANN) index.
A popular ANN algorithm is HNSW (Hierarchical Navigable Small World), which
builds a layered graph of vectors so that a search only has to visit a small
fraction of the data. ANN trades a tiny amount of accuracy for a large gain in
speed.

Chroma is a lightweight, open-source vector database designed to be easy to
embed directly into an application. It can run fully in-process and persist its
index to a local directory on disk, with no separate server to operate. This
makes it a good choice for prototypes, workshops, and small applications.

Qdrant is another open-source vector database. Unlike Chroma's file-based mode,
Qdrant typically runs as a separate service, which makes it a better fit for
larger, multi-user deployments.

Besides the vectors themselves, a vector database also stores metadata
alongside each entry — for example the source document, a chunk index, or a
timestamp. Metadata can be used to filter results before or after the
similarity search.
