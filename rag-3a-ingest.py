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
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

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
    """As in rag-2a-ingest.py."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


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
