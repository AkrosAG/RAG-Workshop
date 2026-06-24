# RAG-Demo — Knowledge-Worker in einem Skript

Minimales, vollständiges RAG: **`rag.py`** durchläuft drei Stages, jede idempotent —
laden/embedden, LLM verbinden, Frage beantworten. Kein Framework, kein lokaler
ML-Stack: Embeddings **und** Generierung laufen über **einen** OpenAI-kompatiblen
Endpoint (lokales Ollama oder ein interner LiteLLM-Proxy). ~40 Zeilen, die man ganz liest.

## Die drei Stages in `rag.py`

1. **Ingest** — Dokumente fix chunken, über den Endpoint embedden, in Chroma ablegen.
   *Idempotent:* nur fehlende Chunks werden embedded; ein zweiter Lauf macht nichts.
2. **Verbindung** — ein OpenAI-Client für Embeddings und Chat.
3. **RAG-Abfrage** — Frage embedden → ähnlichste Chunks holen → Prompt bauen → Antwort.

Der Vektor-Store (Chroma) ist lokal und file-based — der einzige „lokale" Teil.

## Projektstruktur

```
rag-demo/
├── data/                     # neutraler Beispiel-Datensatz (3 Markdown-Dokumente)
├── notebooks/
│   └── 01_rag-zu-fuss.ipynb  # dieselben Stages als Schritt-für-Schritt-Notebook (mit Lücke)
├── rag.py                    # das ganze RAG in einem idempotenten Skript
├── pyproject.toml            # Abhängigkeiten (Poetry): chromadb, openai, python-dotenv
└── poetry.lock
```

## Schnellstart

Voraussetzung: Python ≥ 3.10, [Poetry](https://python-poetry.org/) und ein laufendes [Ollama](https://ollama.com/).

```bash
ollama pull llama3.2 && ollama pull bge-m3
poetry install
cp .env.example .env          # Windows: copy .env.example .env
poetry run python rag.py "What is a vector database?"
```

Der erste Lauf baut den Index und antwortet; jeder weitere überspringt den
Ingest („up to date") und antwortet direkt.

## Endpoint wählen (`.env`)

Default ist ein **lokales Ollama** (kein Key). Für einen anderen OpenAI-kompatiblen
Endpoint — z. B. einen internen LiteLLM-Proxy — `LLM_BASE_URL` / `LLM_API_KEY` /
`LLM_MODEL` / `EMBED_MODEL` in `.env` setzen (siehe `.env.example`).

## Notebook

`notebooks/01_rag-zu-fuss.ipynb` zeigt dieselben drei Stages Schritt für Schritt,
mit einer Lücke beim Chunking zum Selbermachen:

```bash
poetry install --with notebook
poetry run jupyter lab
```

## Stellschrauben

- In `rag.py`: `CHUNK_SIZE` (fixe Chunk-Grösse), `TOP_K` (Anzahl abgerufener Chunks).
- In `.env`: `LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL` / `EMBED_MODEL`.

## Ausblick Block 2 (Wahlmodul)

- **Chunking** mit Overlap oder satz-/absatzbewusst statt fix.
- **Reranking** der abgerufenen Kandidaten.
- **Query Rewriting** der Frage vor dem Embedden.
- **Evaluation** der Antwortqualität gegen Referenzfragen.
