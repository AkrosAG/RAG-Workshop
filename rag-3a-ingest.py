"""Stage 3a — Refinement of the ingest: semantic chunking.

Builds on rag-2a-ingest.py; the ONLY change is the chunk() function.
Instead of cutting blindly every N characters, we split along the document's
own structure (markdown headings and paragraphs) and pack whole paragraphs
into chunks up to a size budget. Chunks never cut through a sentence or word,
so each chunk is a coherent unit of meaning.

(The same idea applies to source code, where an AST/LSP would provide the
structural boundaries instead of headings and paragraphs.)

Writes into its own collection 'rag_semantic', so the fixed-size store from
rag-2a stays untouched and both can be compared:
    RAG_COLLECTION=rag_semantic poetry run python rag-2b-chat.py "..."

Run:  poetry run python rag-3a-ingest.py
"""

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

# --- Configuration (as in rag-2a, but its own collection) ---
EMBED_MODEL = os.getenv("EMBED_MODEL", "bge-m3")
client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("LLM_API_KEY", "ollama"),
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
COLLECTION = "rag_semantic"
MAX_CHUNK_SIZE = 800  # budget per chunk — a paragraph is never split
EMBED_BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", "64"))


# --- CHANGED vs. rag-2a: structure-aware chunking ---
def chunk(text: str) -> list[str]:
    """Semantic chunking: split at headings/paragraphs, pack up to the budget.

    1. Split the document into blocks at blank lines (= paragraphs).
    2. A markdown heading always starts a new chunk (topic boundary).
    3. Consecutive blocks are packed together until MAX_CHUNK_SIZE is reached.
    """
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]

    chunks: list[str] = []
    current = ""
    for block in blocks:
        is_heading = block.lstrip().startswith("#")
        over_budget = len(current) + len(block) > MAX_CHUNK_SIZE
        if current and (is_heading or over_budget):
            chunks.append(current)
            current = block
        else:
            current = f"{current}\n\n{block}" if current else block
    if current:
        chunks.append(current)
    return chunks


def embed(texts: list[str]) -> list[list[float]]:
    """As in rag-2a-ingest.py: embed in endpoint-friendly batches."""
    embeddings: list[list[float]] = []
    for start in range(0, len(texts), EMBED_BATCH_SIZE):
        batch = texts[start : start + EMBED_BATCH_SIZE]
        resp = client.embeddings.create(model=EMBED_MODEL, input=batch)
        embeddings.extend(d.embedding for d in resp.data)
    return embeddings


# --- Ingest (identical to rag-2a, only chunk() changed) ---
collection = chromadb.PersistentClient(path=str(ROOT / ".chroma")).get_or_create_collection(
    COLLECTION, embedding_function=None, metadata={"hnsw:space": "cosine"}
)

ids, texts, metas = [], [], []
for path in sorted(DATA.glob("*.md")):
    for n, piece in enumerate(chunk(path.read_text(encoding="utf-8"))):
        ids.append(f"{path.name}::{n}")
        texts.append(piece)
        metas.append({"source": path.name})

existing = set(collection.get(include=[])["ids"])
missing = [j for j, _id in enumerate(ids) if _id not in existing]

if missing:
    for start in range(0, len(missing), EMBED_BATCH_SIZE):
        batch = missing[start : start + EMBED_BATCH_SIZE]
        batch_texts = [texts[j] for j in batch]
        collection.upsert(
            ids=[ids[j] for j in batch],
            embeddings=embed(batch_texts),
            documents=batch_texts,
            metadatas=[metas[j] for j in batch],
        )
        print(f"[ingest] embedded {min(start + len(batch), len(missing))}/{len(missing)}")
    print(f"[ingest] added {len(missing)} chunk(s); '{COLLECTION}' now holds {collection.count()}")
else:
    print(f"[ingest] up to date ('{COLLECTION}': {collection.count()} chunks)")
