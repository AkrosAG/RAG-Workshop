"""Stage 2b — RAG chat: augment the prompt with retrieved chunks.

Builds on rag-1-chat.py (same chat backbone) and uses the vector store filled
by rag-2a-ingest.py. New is the retrieval step: embed the question, fetch the
most similar chunks from Chroma, and put them into the prompt as context.

Set RAG_COLLECTION=rag_semantic to chat over the store built by rag-3a-ingest.py.

Run:  poetry run python rag-2b-chat.py "What is a vector database?"
"""

import os
import sys
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# --- Configuration (as in rag-1/2a) ---
CHAT_MODEL = os.getenv("LLM_MODEL", "llama3.2")
EMBED_MODEL = os.getenv("EMBED_MODEL", "bge-m3")
client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("LLM_API_KEY", "ollama"),
)

ROOT = Path(__file__).resolve().parent
COLLECTION = os.getenv("RAG_COLLECTION", "rag_fixed")
TOP_K = 4

question = " ".join(sys.argv[1:]) or "What is a vector database?"


def embed(texts: list[str]) -> list[list[float]]:
    """As in rag-2a-ingest.py — the question must use the same model as the chunks."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


# --- NEW in 2b: retrieve context for the question ---
collection = chromadb.PersistentClient(path=str(ROOT / ".chroma")).get_collection(
    COLLECTION, embedding_function=None
)
hits = collection.query(query_embeddings=embed([question]), n_results=TOP_K)
context = "\n\n".join(hits["documents"][0])

# --- Ask (as in rag-1, but with the retrieved context in the prompt) ---
answer = client.chat.completions.create(
    model=CHAT_MODEL,
    messages=[
        {"role": "system", "content": "Answer the question using ONLY the context. If it is not in the context, say so."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ],
)

print(answer.choices[0].message.content)
print("\nSources:", [m["source"] for m in hits["metadatas"][0]])
