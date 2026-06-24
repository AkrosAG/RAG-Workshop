# Embeddings

An embedding is a numerical representation of a piece of data — most often a
piece of text — as a vector of floating-point numbers. A small embedding model
might produce vectors with 384 dimensions; larger models use 1024 or more.

The key property of a good embedding is that semantically similar texts end up
close together in vector space, while unrelated texts end up far apart.
"Closeness" is measured with a distance or similarity metric. Cosine similarity
is the most common choice: it compares the angle between two vectors and ignores
their length. When vectors are normalized to unit length, cosine similarity is
equivalent to a simple dot product.

Embedding models are trained on large amounts of text so that they learn to map
meaning to geometry. The classic early example is word2vec, which produced one
vector per word. Modern encoder models such as the sentence-transformers family
embed whole sentences or paragraphs at once, capturing context rather than
individual words.

In a retrieval system, every document chunk is embedded once and stored. At
query time, the user's question is embedded with the same model, and the system
looks for the stored vectors nearest to the question vector. Using the same
model for both indexing and querying is essential — vectors from different
models are not comparable.
