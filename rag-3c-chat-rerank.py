"""Stage 3c — Re-rank vector candidates with a dedicated cross-encoder.

Builds on rag-3b-chat-classical.py and changes only candidate ranking:

1. Over-fetch TOP_N candidates from the semantic vector store.
2. Score every (question, candidate) pair with a multilingual BGE re-ranker.
3. Keep the best TOP_K candidates as context for the chat model.

Unlike an embedding model, a cross-encoder reads the question and passage
together. Its relevance scores therefore have to be computed at query time.

The re-ranker model is downloaded on first use and then cached locally.

Run:  poetry run python rag-3c-chat-rerank.py "What is a vector database?"
"""

import os
import sys
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import CrossEncoder

load_dotenv()

# Minimal error handling: print one line instead of a stack trace.
sys.excepthook = lambda exc_type, exc, _: sys.exit(f"{exc_type.__name__}: {exc}")

# --- Configuration (as in 3b, plus the dedicated re-ranker) ---
CHAT_MODEL = os.getenv("LLM_MODEL", "llama3.2")
EMBED_MODEL = os.getenv("EMBED_MODEL", "bge-m3")
RERANK_MODEL = os.getenv("RERANK_MODEL", "BAAI/bge-reranker-v2-m3")
client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("LLM_API_KEY", "ollama"),
)

ROOT = Path(__file__).resolve().parent
COLLECTION = os.getenv("RAG_COLLECTION", "rag_semantic")
TOP_N = 10
TOP_K = 4

question = " ".join(sys.argv[1:]) or "What is a vector database?"


def embed(texts: list[str]) -> list[list[float]]:
    """Embed the question with the same model used for the stored chunks."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


def rerank(question: str, candidates: list[str], keep: int) -> list[tuple[int, float]]:
    """Return (candidate index, score), ordered by cross-encoder relevance."""
    try:
        model = CrossEncoder(RERANK_MODEL)
    except (OSError, ValueError) as exc:
        raise RuntimeError(
            f"Could not load re-ranker '{RERANK_MODEL}'. "
            "The first run needs internet access to download the model."
        ) from exc
    pairs = [(question, candidate) for candidate in candidates]
    scores = model.predict(pairs, show_progress_bar=False)
    ranked = sorted(
        ((index, float(score)) for index, score in enumerate(scores)),
        key=lambda item: item[1],
        reverse=True,
    )
    return ranked[: min(keep, len(ranked))]


# --- Retrieve: over-fetch candidates using the same vector search as 3b ---
collection = chromadb.PersistentClient(path=str(ROOT / ".chroma-3")).get_collection(
    COLLECTION, embedding_function=None
)
hits = collection.query(query_embeddings=embed([question]), n_results=TOP_N)
candidates = hits["documents"][0]
sources = [metadata["source"] for metadata in hits["metadatas"][0]]

# --- Re-rank: score question and chunk together, then keep the best TOP_K ---
ranking = rerank(question, candidates, TOP_K)
context = "\n\n".join(candidates[index] for index, _ in ranking)

print("[rerank] BGE cross-encoder ranking:")
for rerank_position, (vector_index, score) in enumerate(ranking, start=1):
    print(
        f"- rerank {rerank_position}: vector {vector_index + 1}, "
        f"score {score:.4f}, source {sources[vector_index]}"
    )

# --- Ask: identical answer generation to 3b ---
answer = client.chat.completions.create(
    model=CHAT_MODEL,
    messages=[
        {
            "role": "system",
            "content": (
                "Answer the question using ONLY the context. "
                "If it is not in the context, say so."
            ),
        },
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ],
)

print("\n" + (answer.choices[0].message.content or ""))
print("\nSources:", [sources[index] for index, _ in ranking])
