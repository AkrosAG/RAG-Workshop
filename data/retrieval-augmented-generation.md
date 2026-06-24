# Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation is a technique that gives a large language model
access to external knowledge at query time. Instead of relying only on what the
model learned during training, a RAG system retrieves relevant passages from a
knowledge base and places them into the prompt, so the model can answer from
that fresh, specific context.

RAG addresses several weaknesses of a plain language model: a fixed knowledge
cutoff, no awareness of private or company-internal documents, a tendency to
hallucinate, and the inability to cite sources. By grounding answers in
retrieved text, RAG makes responses more accurate and verifiable.

A RAG system has two phases. The ingestion phase runs once per document set:
load the documents, split them into chunks, embed each chunk, and store the
vectors in a vector database. The query phase runs for every user question:
embed the question, retrieve the most similar chunks, build an augmented prompt
from those chunks, and generate an answer with the language model.

Chunking is the step of splitting documents into smaller pieces before
embedding. The simplest strategy is fixed-size chunking, which cuts the text
every N characters. More advanced strategies respect sentence or paragraph
boundaries, add overlap between neighboring chunks, or split by document
structure.

Retrieval quality can be improved with techniques such as reranking, where a
second model re-scores the retrieved candidates, and query rewriting, where the
user's question is reformulated before searching. RAG is not the only way to
extend a model's context: tool or function calling, the Model Context Protocol
(MCP), and simply using a larger context window all solve related problems.
