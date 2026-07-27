"""Stage 3b — Refinement of the retrieval: re-ranking.

Builds on rag-2b-chat.py; the retrieval step is extended in two moves:

1. Over-fetch: pull MORE candidates than needed (TOP_N=10) from the vector
   store. Vector similarity is fast but coarse — it finds "roughly related".
2. Re-rank: let the chat model judge each candidate's relevance to the
   question, then keep only the best TOP_K=4 as context.

Works against either store: rag_fixed (from rag-2a) by default, or
    RAG_COLLECTION=rag_semantic poetry run python rag-3b-chat.py "..."

Run:  poetry run python rag-3b-chat.py "What is a vector database?"
"""

import json
import os
import re
import sys
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Minimal error handling: print one line instead of a stack trace.
sys.excepthook = lambda exc_type, exc, _: sys.exit(f"{exc_type.__name__}: {exc}")

# --- Configuration (as in rag-2b) ---
CHAT_MODEL = os.getenv("LLM_MODEL", "llama3.2")
EMBED_MODEL = os.getenv("EMBED_MODEL", "bge-m3")
client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("LLM_API_KEY", "ollama"),
)

ROOT = Path(__file__).resolve().parent
COLLECTION = os.getenv("RAG_COLLECTION", "rag_fixed")
TOP_N = 10  # NEW: candidates fetched from the store (over-fetch)
TOP_K = 4   # candidates that survive the re-ranking

question = " ".join(sys.argv[1:]) or "What is a vector database?"


def embed(texts: list[str]) -> list[list[float]]:
    """As in rag-2b-chat.py."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


# --- Retrieve (as in rag-2b, but over-fetching TOP_N candidates) ---
collection = chromadb.PersistentClient(path=str(ROOT / ".chroma")).get_collection(
    COLLECTION, embedding_function=None
)
hits = collection.query(query_embeddings=embed([question]), n_results=TOP_N)
candidates = hits["documents"][0]
sources = [m["source"] for m in hits["metadatas"][0]]


# --- NEW in 3b: re-rank the candidates with the chat model ---
def rerank(question: str, candidates: list[str], keep: int) -> list[int]:
    """Ask the model which passages actually answer the question.

    Returns the indices of the `keep` most relevant candidates, best first.
    Falls back to the original vector-similarity order if parsing fails.
    """
    numbered = "\n\n".join(f"[{i}] {c}" for i, c in enumerate(candidates))
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a re-ranker. Given a question and numbered passages, "
                    f"reply with ONLY a JSON array of the {keep} most relevant passage "
                    "numbers, most relevant first. Example: [3, 0, 7, 1]"
                ),
            },
            {"role": "user", "content": f"Question: {question}\n\nPassages:\n{numbered}"},
        ],
    )
    reply = resp.choices[0].message.content or ""
    match = re.search(r"\[[\d,\s]*\]", reply)  # tolerate chatter around the array
    order: list[int] = []
    if match:
        try:
            parsed = json.loads(match.group())
        except (json.JSONDecodeError, TypeError):
            parsed = []
        if isinstance(parsed, list):
            for item in parsed:
                if (
                    isinstance(item, int)
                    and not isinstance(item, bool)
                    and 0 <= item < len(candidates)
                    and item not in order
                ):
                    order.append(item)

    # Invalid, duplicate or incomplete model output is completed with the
    # original vector order. This also acts as the full parsing fallback.
    for index in range(len(candidates)):
        if len(order) >= min(keep, len(candidates)):
            break
        if index not in order:
            order.append(index)
    return order


best = rerank(question, candidates, TOP_K)
context = "\n\n".join(candidates[i] for i in best)
print(f"[rerank] kept {best} of 0..{len(candidates) - 1}")

# --- Ask (identical to rag-2b) ---
answer = client.chat.completions.create(
    model=CHAT_MODEL,
    messages=[
        {"role": "system", "content": "Answer the question using ONLY the context. If it is not in the context, say so."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ],
)

print(answer.choices[0].message.content)
print("\nSources:", [sources[i] for i in best])
