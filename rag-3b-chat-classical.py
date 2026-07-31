"""Stage 3b — Classical vector retrieval over the semantic chunks from 3a.

Builds on rag-2b-chat.py. The retrieval algorithm deliberately stays the same:
embed the question, retrieve the TOP_K nearest chunks from Chroma, and use them
as context. The only difference from 2b is the default collection:
'rag_semantic', created by rag-3a-ingest.py.

This isolates the effect of improved chunking before stage 3c adds re-ranking.

Run:  poetry run python rag-3b-chat-classical.py "What is a vector database?"
"""

import os
import sys
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Minimal error handling: print one line instead of a stack trace.
sys.excepthook = lambda exc_type, exc, _: sys.exit(f"{exc_type.__name__}: {exc}")

# Redirected stdout on Windows defaults to cp1252; model output needs UTF-8.
sys.stdout.reconfigure(encoding="utf-8")

# --- Configuration (as in rag-2b, but using the semantic collection) ---
CHAT_MODEL = os.getenv("LLM_MODEL", "llama3.2")
EMBED_MODEL = os.getenv("EMBED_MODEL", "bge-m3")
client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("LLM_API_KEY", "ollama"),
)

ROOT = Path(__file__).resolve().parent
COLLECTION = os.getenv("RAG_COLLECTION", "rag_semantic")
TOP_K = 4

def embed(texts: list[str]) -> list[list[float]]:
    """Embed the question with the same model used for the stored chunks."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


def retrieve_top_k(
    collection: object, query_embedding: list[float], top_k: int = TOP_K
) -> list[dict[str, object]]:
    """Return exactly the available top-k vector hits in their original order."""
    hits = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas"],
    )
    return [
        {"document": document, "metadata": metadata}
        for document, metadata in zip(
            hits["documents"][0][:top_k],
            hits["metadatas"][0][:top_k],
        )
    ]


def main() -> None:
    question = " ".join(sys.argv[1:]) or "What is a vector database?"

    # --- Retrieve: unchanged classical vector Top-K from rag-2b ---
    collection = chromadb.PersistentClient(
        path=str(ROOT / ".chroma-3")
    ).get_collection(COLLECTION, embedding_function=None)
    hits = retrieve_top_k(collection, embed([question])[0])
    context = "\n\n".join(str(hit["document"]) for hit in hits)

    # --- Ask: answer only from the retrieved context ---
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

    print(answer.choices[0].message.content)
    print("\nSources:", [hit["metadata"]["source"] for hit in hits])


if __name__ == "__main__":
    main()
