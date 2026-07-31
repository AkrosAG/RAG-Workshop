"""Stage 4a - Build a small retrieval graph over the semantic Chroma index.

Edges connect neighbouring chunks and explicit legal references such as
"Art. 25". Run rag-3a-ingest.py before this script.

Run:  poetry run python rag-4a-graph.py
"""

import os
import sys
from pathlib import Path

import chromadb

from graph_retrieval import build_graph, save_graph


sys.excepthook = lambda exc_type, exc, _: sys.exit(f"{exc_type.__name__}: {exc}")

# Redirected stdout on Windows defaults to cp1252; model output needs UTF-8.
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
COLLECTION = os.getenv("RAG_COLLECTION", "rag_semantic")
GRAPH_PATH = ROOT / ".chroma-3" / f"{COLLECTION}_graph.json"

collection = chromadb.PersistentClient(path=str(ROOT / ".chroma-3")).get_collection(
    COLLECTION, embedding_function=None
)
graph = build_graph(collection)
save_graph(graph, GRAPH_PATH)

print(
    f"[graph] {graph['nodes']} nodes, {graph['edges']} directed edges "
    f"({graph['reference_edges']} article references)"
)
print(f"[graph] wrote {GRAPH_PATH}")
