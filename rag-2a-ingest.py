"""Stage 2a — Ingest: fixed-size chunking into a local vector store.

Builds on rag-1-chat.py: same client and configuration; new is the ingest
pipeline — read documents, cut them into fixed-size chunks, embed each chunk
via the endpoint, and store everything in a local file-based Chroma collection.

Idempotent (desired-state): only chunks missing from the store get embedded;
re-running with an unchanged corpus does nothing.

Run:  poetry run python rag-2a-ingest.py
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

# --- Configuration (as in rag-1-chat.py, plus embedding/store settings) ---
EMBED_MODEL = os.getenv("EMBED_MODEL", "bge-m3")
client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("LLM_API_KEY", "ollama"),
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
COLLECTION = "rag_fixed"
CHUNK_SIZE = 800  # characters per chunk
OVERLAP = 0       # characters shared between neighbouring chunks


# --- NEW in 2a: chunking + embedding + storing ---
def chunk(text: str) -> list[str]:
    """Primitive fixed-size chunking: cut every CHUNK_SIZE characters."""
    step = CHUNK_SIZE - OVERLAP
    return [text[i : i + CHUNK_SIZE] for i in range(0, len(text), step)]


def embed(texts: list[str]) -> list[list[float]]:
    """Embed texts via the OpenAI-compatible /v1/embeddings endpoint."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


collection = chromadb.PersistentClient(path=str(ROOT / ".chroma")).get_or_create_collection(
    COLLECTION, embedding_function=None, metadata={"hnsw:space": "cosine"}
)

# Collect all chunks with deterministic ids, then embed only what is missing.
ids, texts, metas = [], [], []
for path in sorted(DATA.glob("*.md")):
    for n, piece in enumerate(chunk(path.read_text(encoding="utf-8"))):
        ids.append(f"{path.name}::{n}")
        texts.append(piece)
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
    print(f"[ingest] added {len(missing)} chunk(s); '{COLLECTION}' now holds {collection.count()}")
else:
    print(f"[ingest] up to date ('{COLLECTION}': {collection.count()} chunks)")
