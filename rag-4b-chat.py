"""Stage 4b - GraphRAG chat: vector seeds plus graph-neighbour expansion.

Run rag-3a-ingest.py and rag-4a-graph.py first.

Run:  poetry run python rag-4b-chat.py "Wie lange dauert die Probezeit?"
"""

import os
import sys
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

from graph_retrieval import estimate_tokens, graph_retrieve, load_graph


load_dotenv()
sys.excepthook = lambda exc_type, exc, _: sys.exit(f"{exc_type.__name__}: {exc}")

ROOT = Path(__file__).resolve().parent
COLLECTION = os.getenv("RAG_COLLECTION", "rag_semantic")
GRAPH_PATH = ROOT / ".chroma" / f"{COLLECTION}_graph.json"
CHAT_MODEL = os.getenv("LLM_MODEL", "llama3.2")
EMBED_MODEL = os.getenv("EMBED_MODEL", "bge-m3")
SEED_K = int(os.getenv("GRAPH_SEED_K", "3"))
CONTEXT_K = int(os.getenv("GRAPH_CONTEXT_K", "6"))

client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("LLM_API_KEY", "ollama"),
)
question = " ".join(sys.argv[1:]) or "Wie lange dauert die Probezeit?"

collection = chromadb.PersistentClient(path=str(ROOT / ".chroma")).get_collection(
    COLLECTION, embedding_function=None
)
graph = load_graph(GRAPH_PATH)
embedding = client.embeddings.create(model=EMBED_MODEL, input=[question]).data[0].embedding
hits = graph_retrieve(collection, embedding, graph, SEED_K, CONTEXT_K)

context_parts = []
for hit in hits:
    source = hit["metadata"].get("source", "unknown")
    context_parts.append(
        f"[Quelle: {source}; Chunk: {hit['id']}; gefunden via: {hit['via']}]\n"
        f"{hit['document']}"
    )
context = "\n\n".join(context_parts)

answer = client.chat.completions.create(
    model=CHAT_MODEL,
    messages=[
        {
            "role": "system",
            "content": (
                "Beantworte die Frage ausschliesslich mit dem bereitgestellten "
                "Kontext. Nenne Gesetz und Artikel, wenn sie im Kontext stehen. "
                "Wenn die Antwort nicht enthalten ist, sage das ausdrücklich. "
                "Dies ist keine individuelle Rechtsberatung."
            ),
        },
        {"role": "user", "content": f"Kontext:\n{context}\n\nFrage: {question}"},
    ],
)

print(answer.choices[0].message.content)
print(f"\n[graph-rag] {len(hits)} chunks, about {estimate_tokens(context)} context tokens")
for hit in hits:
    print(f"- {hit['id']} ({hit['via']})")
