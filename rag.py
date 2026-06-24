"""A complete RAG in one idempotent script: ingest -> retrieve -> generate.

Embeddings AND generation both run on a single OpenAI-compatible endpoint
(Marvin via LiteLLM, or Ollama as a local fallback). The vector store is a
local, file-based Chroma collection — no ML stack installed locally.

The ingest stage is idempotent (desired-state): only chunks that are not
already stored get embedded, so re-running with an unchanged corpus does no
work and yields the same answer.

Usage:
    uv run python rag.py "What is a vector database?"
"""

import os
import sys
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CHUNK_SIZE = 800
TOP_K = 4
CHAT_MODEL = os.getenv("LLM_MODEL", "llama3.2")
EMBED_MODEL = os.getenv("EMBED_MODEL", "bge-m3")
question = " ".join(sys.argv[1:]) or "What is a vector database?"

# One OpenAI-compatible client for BOTH embeddings and chat. Defaults to a local
# Ollama; point LLM_BASE_URL at any OpenAI-compatible endpoint (e.g. an internal
# LiteLLM proxy) via .env.
client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("LLM_API_KEY", "ollama"),
)


def embed(texts: list[str]) -> list[list[float]]:
    """Embed texts via the OpenAI-compatible /v1/embeddings endpoint."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


# Local, file-based vector store — no server.
collection = chromadb.PersistentClient(path=str(ROOT / ".chroma")).get_or_create_collection(
    "rag_demo", embedding_function=None, metadata={"hnsw:space": "cosine"}
)

# --- Stage 1: ingest (idempotent — embed only what's missing) ---
ids, texts, metas = [], [], []
for path in sorted(DATA.glob("*.md")):
    text = path.read_text(encoding="utf-8")
    for i in range(0, len(text), CHUNK_SIZE):
        ids.append(f"{path.name}::{i // CHUNK_SIZE}")
        texts.append(text[i : i + CHUNK_SIZE])
        metas.append({"source": path.name})

existing = set(collection.get(ids=ids)["ids"])
missing = [j for j, _id in enumerate(ids) if _id not in existing]
if missing:
    collection.upsert(
        ids=[ids[j] for j in missing],
        embeddings=embed([texts[j] for j in missing]),
        documents=[texts[j] for j in missing],
        metadatas=[metas[j] for j in missing],
    )
    print(f"[ingest] added {len(missing)} chunk(s); collection now holds {collection.count()}")
else:
    print(f"[ingest] up to date ({collection.count()} chunks)")

# --- Stage 2: retrieve -> augment -> generate ---
hits = collection.query(query_embeddings=embed([question]), n_results=TOP_K)
context = "\n\n".join(hits["documents"][0])

answer = client.chat.completions.create(
    model=CHAT_MODEL,
    messages=[
        {"role": "system", "content": "Answer the question using ONLY the context. If it is not in the context, say so."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ],
)

print(f"\nQ: {question}\n")
print(answer.choices[0].message.content)
print("\nSources:", [m["source"] for m in hits["metadatas"][0]])
