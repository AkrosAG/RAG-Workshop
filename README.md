# RAG-Workshop — vom Chat-Backbone zum verfeinerten RAG

Didaktische Progression in fünf kleinen Skripten: Jedes baut sichtbar auf dem
vorigen auf — gleiche Konfiguration, gleiche Struktur, pro Stufe kommt genau
ein Konzept dazu. Kein Framework, keine Blackbox.

```
rag-1-chat.py          Backbone: Modell anbinden, einen Prompt absetzen
   │
rag-2a-ingest.py       + Ingest: Fixed-Size-Chunking → Embedding-DB (Chroma, file-based)
rag-2b-chat.py         + Retrieval: Abfrage mit passenden Chunks anreichern (= RAG)
   │
rag-3a-ingest.py       Verfeinerung Ingest: semantisches Chunking (Absätze/Überschriften)
rag-3b-chat.py         Verfeinerung Retrieval: Over-Fetch + LLM-Re-Ranking
```

## Die Stufen

| Skript | Baut auf | Neu |
|---|---|---|
| `rag-1-chat.py` | — | OpenAI-kompatibler Client, eine Chat-Anfrage |
| `rag-2a-ingest.py` | rag-1 | `chunk()` (fix), `embed()`, idempotentes Befüllen von Chroma (`rag_fixed`) |
| `rag-2b-chat.py` | rag-1 + 2a | Frage embedden → Top-K-Chunks holen → als Kontext in den Prompt |
| `rag-3a-ingest.py` | rag-2a | nur `chunk()` geändert: struktur-/absatzbewusst (Collection `rag_semantic`) |
| `rag-3b-chat.py` | rag-2b | Over-Fetch (Top-10) + Re-Ranking durch das Chat-Modell → beste 4 |

Alle Ingests sind **idempotent**: nur fehlende Chunks werden embedded, ein
zweiter Lauf tut nichts.

## Schnellstart

Voraussetzung: Python ≥ 3.10, [Poetry](https://python-poetry.org/) und ein laufendes [Ollama](https://ollama.com/).

```bash
ollama pull llama3.2 && ollama pull bge-m3
poetry install
cp .env.example .env          # Windows: copy .env.example .env
```

Ohne Poetry geht es auch mit einem klassischen venv + `requirements.txt`:

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Dann die Stufen der Reihe nach (mit venv statt Poetry: `python ...` direkt):

```bash
poetry run python rag-1-chat.py "Why is the sky blue?"      # 1: Backbone
poetry run python rag-2a-ingest.py                            # 2a: Index bauen
poetry run python rag-2b-chat.py "What is a vector database?" # 2b: RAG
poetry run python rag-3a-ingest.py                            # 3a: semantischer Index
poetry run python rag-3b-chat.py "What is a vector database?" # 3b: mit Re-Ranking
```

## Schweizer Gesetze aus Fedlex vorbereiten

Die heruntergeladenen Fedlex-PDFs werden nicht direkt von den Ingest-Skripten
gelesen. Konvertiere sie zuerst in nachvollziehbares Markdown unter `data/`:

```bash
poetry run python scripts/fedlex_pdf_to_md.py
```

Mit einem klassischen `.venv` funktioniert derselbe Schritt ohne Poetry:

```bash
python scripts/fedlex_pdf_to_md.py
```

Der Konverter lässt die Original-PDFs unverändert, bereinigt typische
PDF-Zeilentrennungen und ergänzt Seitenmarker. Danach finden `rag-2a-ingest.py`
und `rag-3a-ingest.py` die erzeugten `data/SR_*.md` automatisch.

Kompletter Ablauf für den Schweizer-Recht-Datensatz:

```bash
poetry run python scripts/fedlex_download.py --outdir scripts/fedlex_pdfs
poetry run python scripts/fedlex_pdf_to_md.py
poetry run python rag-2a-ingest.py
```

Die Ingestion verarbeitet den großen Rechtskorpus in Batches von 64 Chunks.
Bei Bedarf lässt sich die Größe über `EMBED_BATCH_SIZE` reduzieren.

Beide Chat-Skripte können auf beide Indizes zeigen — so lassen sich die
Chunking-Strategien direkt vergleichen:

```bash
RAG_COLLECTION=rag_semantic poetry run python rag-2b-chat.py "..."
RAG_COLLECTION=rag_semantic poetry run python rag-3b-chat.py "..."
```

## Endpoint wählen (`.env`) — Key bleibt ausserhalb

`.env` enthält nur **Nicht-Geheimes**: `LLM_BASE_URL`, `LLM_MODEL`, `EMBED_MODEL`
(siehe `.env.example`). Default ist ein lokales Ollama — dafür braucht es keinen Key.

Der **API-Key wird nie in eine Datei geschrieben**. Für einen Endpoint mit Key
(z. B. einen internen LiteLLM-Proxy) setzt du ihn einmal pro Shell-Session:

```powershell
.\set-key.ps1                 # PowerShell — fragt verdeckt ab, gilt für die Session
```

```bash
source set-key.sh             # bash/zsh — MUSS gesourced werden
```

Danach erben alle `python`/`poetry`-Aufrufe aus dieser Shell den Key; beim
Schliessen der Shell ist er weg. `python-dotenv` überschreibt gesetzte
Umgebungsvariablen nicht — der Session-Key gewinnt also immer.

## Projektstruktur

```
rag-demo/
├── data/                     # neutraler Beispiel-Datensatz (3 Markdown-Dokumente)
├── notebooks/
│   └── 01_rag-zu-fuss.ipynb  # die Stufen 1–2b als Schritt-für-Schritt-Notebook (mit Lücke)
├── rag-1-chat.py … rag-3b-chat.py
├── pyproject.toml            # Abhängigkeiten (Poetry): chromadb, openai, python-dotenv
└── poetry.lock
```

## Notebook

`notebooks/01_rag-zu-fuss.ipynb` zeigt die Stufen 1–2b Schritt für Schritt,
mit einer Lücke beim Chunking zum Selbermachen:

```bash
poetry install --with notebook
poetry run jupyter lab
```

## Weiterführende Ideen (Workshop Block 2)

- **Chunking:** Overlap in `rag-2a`, andere Budgets, AST-basiert für Quellcode.
- **Re-Ranking:** dedizierter Cross-Encoder statt LLM-Judge.
- **Query Rewriting:** die Frage vor dem Embedden umformulieren/erweitern.
- **Evaluation:** beide Indizes und beide Retrieval-Varianten gegen Referenzfragen messen.
