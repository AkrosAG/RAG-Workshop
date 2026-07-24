"""Stage 2a — Ingest: fixed-size chunking into a local vector store.

Builds on rag-1-chat.py: same client and configuration; new is the ingest
pipeline — read documents, cut them into fixed-size chunks, embed each chunk
via the endpoint, and store everything in a local file-based Chroma collection.

Idempotent (desired-state): new and changed chunks are embedded, obsolete
chunks are removed, and re-running with an unchanged corpus does nothing.

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
EMBED_BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", "64"))


# --- NEW in 2a: chunking + embedding + storing ---
def chunk(text: str) -> list[str]:
    """Primitive fixed-size chunking: cut every CHUNK_SIZE characters."""
    step = CHUNK_SIZE - OVERLAP
    return [text[i : i + CHUNK_SIZE] for i in range(0, len(text), step)]


def embed(texts: list[str]) -> list[list[float]]:
    """Embed texts in endpoint-friendly batches."""
    embeddings: list[list[float]] = []
    for start in range(0, len(texts), EMBED_BATCH_SIZE):
        batch = texts[start : start + EMBED_BATCH_SIZE]
        resp = client.embeddings.create(model=EMBED_MODEL, input=batch)
        embeddings.extend(d.embedding for d in resp.data)
    return embeddings


collection = chromadb.PersistentClient(path=str(ROOT / ".chroma")).get_or_create_collection(
    COLLECTION, embedding_function=None, metadata={"hnsw:space": "cosine"}
)

# Collect all chunks with deterministic IDs, then synchronize changed,
# missing and obsolete chunks with the desired corpus state.
ids, texts, metas = [], [], []
for path in sorted(DATA.glob("*.md")):
    for n, piece in enumerate(chunk(path.read_text(encoding="utf-8"))):
        ids.append(f"{path.name}::{n}")
        texts.append(piece)
        metas.append({"source": path.name, "embed_model": EMBED_MODEL})

stored = collection.get(include=["documents", "metadatas"])
existing_documents = dict(zip(stored["ids"], stored["documents"]))
existing_metadatas = dict(zip(stored["ids"], stored["metadatas"]))
changed = [
    j for j, chunk_id in enumerate(ids)
    if (
        existing_documents.get(chunk_id) != texts[j]
        or existing_metadatas.get(chunk_id, {}).get("embed_model") != EMBED_MODEL
    )
]
obsolete = sorted(set(existing_documents) - set(ids))

if changed:
    for start in range(0, len(changed), EMBED_BATCH_SIZE):
        batch = changed[start : start + EMBED_BATCH_SIZE]
        batch_texts = [texts[j] for j in batch]
        collection.upsert(
            ids=[ids[j] for j in batch],
            embeddings=embed(batch_texts),
            documents=batch_texts,
            metadatas=[metas[j] for j in batch],
        )
        print(f"[ingest] embedded {min(start + len(batch), len(changed))}/{len(changed)}")
if obsolete:
    for start in range(0, len(obsolete), 500):
        collection.delete(ids=obsolete[start : start + 500])

if changed or obsolete:
    print(
        f"[ingest] synchronized {len(changed)} changed/new and "
        f"removed {len(obsolete)} obsolete chunk(s); "
        f"'{COLLECTION}' now holds {collection.count()}"
    )
else:
    print(f"[ingest] up to date ('{COLLECTION}': {collection.count()} chunks)")
