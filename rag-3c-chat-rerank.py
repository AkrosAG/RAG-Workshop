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
from typing import Callable

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

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

def embed(texts: list[str]) -> list[list[float]]:
    """Embed the question with the same model used for the stored chunks."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


def retrieve_candidates(
    collection: object, query_embedding: list[float], top_n: int = TOP_N
) -> list[dict[str, object]]:
    """Return at most top-n vector candidates in their original rank order."""
    hits = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_n,
        include=["documents", "metadatas"],
    )
    return [
        {
            "document": document,
            "metadata": metadata,
            "vector_rank": rank,
        }
        for rank, (document, metadata) in enumerate(
            zip(
                hits["documents"][0][:top_n],
                hits["metadatas"][0][:top_n],
            ),
            start=1,
        )
    ]


def rerank(
    question: str,
    candidates: list[str],
    keep: int,
    model_factory: Callable[[str], object] | None = None,
) -> list[tuple[int, float]]:
    """Return (candidate index, score), ordered by cross-encoder relevance."""
    if model_factory is None:
        def model_factory(model_name: str) -> object:
            from sentence_transformers import CrossEncoder

            return CrossEncoder(model_name)

    try:
        model = model_factory(RERANK_MODEL)
    except (ImportError, OSError, ValueError) as exc:
        raise RuntimeError(
            f"Could not load re-ranker '{RERANK_MODEL}'. "
            "Install the project dependencies first; the first model run also "
            "needs internet access unless the Hugging Face cache was pre-filled."
        ) from exc
    pairs = [(question, candidate) for candidate in candidates]
    scores = model.predict(pairs, show_progress_bar=False)
    ranked = sorted(
        ((index, float(score)) for index, score in enumerate(scores)),
        key=lambda item: item[1],
        reverse=True,
    )
    return ranked[: min(keep, len(ranked))]


def main() -> None:
    question = " ".join(sys.argv[1:]) or "Wann ist eine Person volljährig?"

    # --- Retrieve: over-fetch candidates using the same vector search as 3b ---
    collection = chromadb.PersistentClient(
        path=str(ROOT / ".chroma-3")
    ).get_collection(COLLECTION, embedding_function=None)
    vector_hits = retrieve_candidates(collection, embed([question])[0])
    candidates = [str(hit["document"]) for hit in vector_hits]

    # --- Re-rank: score question and chunk together, then keep the best TOP_K ---
    ranking = rerank(question, candidates, TOP_K)
    selected = [vector_hits[index] for index, _ in ranking]
    context = "\n\n".join(str(hit["document"]) for hit in selected)

    print("[rerank] BGE cross-encoder ranking:")
    for rerank_position, ((vector_index, score), hit) in enumerate(
        zip(ranking, selected), start=1
    ):
        print(
            f"- rerank {rerank_position}: vector {hit['vector_rank']}, "
            f"score {score:.4f}, source {hit['metadata']['source']}"
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
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ],
    )

    print("\n" + (answer.choices[0].message.content or ""))
    print("\nSources:", [hit["metadata"]["source"] for hit in selected])


if __name__ == "__main__":
    main()
