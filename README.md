# RAG-Workshop — vom Chat-Backbone zum verfeinerten RAG

Didaktische Progression in sieben kleinen Skripten: Jedes baut sichtbar auf dem
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
   │
rag-4a-graph.py        Graph: Nachbar-Chunks + explizite Gesetzesverweise
rag-4b-chat.py         Hybrid GraphRAG: Vektor + Artikelsuche → Graph → Antwort
```

## Die Stufen

| Skript | Baut auf | Neu |
|---|---|---|
| `rag-1-chat.py` | — | OpenAI-kompatibler Client, eine Chat-Anfrage |
| `rag-2a-ingest.py` | rag-1 | `chunk()` (fix), `embed()`, idempotentes Befüllen von Chroma (`rag_fixed`) |
| `rag-2b-chat.py` | rag-1 + 2a | Frage embedden → Top-K-Chunks holen → als Kontext in den Prompt |
| `rag-3a-ingest.py` | rag-2a | nur `chunk()` geändert: struktur-/absatzbewusst (Collection `rag_semantic`) |
| `rag-3b-chat.py` | rag-2b | Over-Fetch (Top-10) + Re-Ranking durch das Chat-Modell → beste 4 |
| `rag-4a-graph.py` | rag-3a | baut einen transparenten Retrieval-Graph aus Nachbarschaft und `Art.`-Verweisen |
| `rag-4b-chat.py` | rag-4a | kombiniert Vektor- und lexikalische Artikeltreffer und erweitert sie über Graph-Kanten |

Alle Ingests sind **idempotent**: neue oder inhaltlich beziehungsweise durch
einen Modellwechsel veränderte Chunks werden embedded, obsolete Chunks werden
entfernt und ein unveränderter zweiter Lauf tut nichts.

## Schnellstart

Voraussetzung: Python ≥ 3.10, [Poetry](https://python-poetry.org/), eine
Verbindung zum AKROS-VPN und ein Marvin-API-Key mit Zugriff auf die
konfigurierten Chat- und Embedding-Modelle.

```bash
poetry install
cp .env.example .env          # Windows: copy .env.example .env
# danach den Key für die aktuelle Shell setzen:
# PowerShell: .\set-key.ps1
# Bash: source ./set-key.sh
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
poetry run python rag-4a-graph.py                              # 4a: Graph bauen
poetry run python rag-4b-chat.py "Wie lange dauert die Probezeit?" # 4b: GraphRAG
```

## Schweizer Gesetze aus Fedlex vorbereiten

Die Schweizer Gesetzestexte werden reproduzierbar aus Fedlex aufgebaut:

1. `fedlex_download.py` lädt die aktuell anwendbaren Fassungen als PDF nach
   `scripts/fedlex_pdfs/`.
2. `fedlex_pdf_to_md.py` extrahiert und bereinigt den Text und erzeugt
   `data/SR_*.md`.
3. Die Ingest-Skripte chunken diese Markdown-Dateien und schreiben die
   Embeddings nach ChromaDB.

Die heruntergeladenen PDFs, die daraus erzeugten Markdown-Dateien und die
lokale ChromaDB werden bewusst **nicht in Git versioniert**. Sie bleiben lokal
erhalten und können mit den folgenden Befehlen jederzeit neu erzeugt werden.

Kompletter Ablauf mit Poetry für die Demonstration von Fixed-Size-Chunking:

```bash
poetry install
poetry run python scripts/fedlex_download.py --outdir scripts/fedlex_pdfs
poetry run python scripts/fedlex_pdf_to_md.py
poetry run python rag-2a-ingest.py
```

Mit einem klassischen `.venv` für dieselbe Fixed-Size-Demonstration:

```bash
python -m pip install -r requirements.txt
python scripts/fedlex_download.py --outdir scripts/fedlex_pdfs
python scripts/fedlex_pdf_to_md.py
python rag-2a-ingest.py
```

Der Konverter lässt die Original-PDFs unverändert, bereinigt typische
PDF-Zeilentrennungen und ergänzt Seitenmarker. Danach finden `rag-2a-ingest.py`
und `rag-3a-ingest.py` die erzeugten `data/SR_*.md` automatisch.

Die Ingestion verarbeitet den großen Rechtskorpus in Batches von 64 Chunks.
Bei Bedarf lässt sich die Größe über `EMBED_BATCH_SIZE` reduzieren.

## GraphRAG

Die GraphRAG-Stufe verwendet bewusst kein Graph-Framework. Dadurch bleibt die
Mechanik im Workshop sichtbar:

1. `rag-3a-ingest.py` erzeugt den semantisch gechunkten Chroma-Index.
2. `rag-4a-graph.py` verbindet aufeinanderfolgende Chunks derselben Quelle und
   erkannte Gesetzesverweise wie `Art. 25`.
3. `rag-4b-chat.py` sucht semantische Vektor-Seeds.
4. Ein kleiner BM25-ähnlicher Index sucht parallel in den normalisierten
   Artikel-Chunks. Erlassnamen und Abkürzungen wie `ZGB`, `StGB` oder `MWSTG`
   verstärken nur Artikel, die zugleich einen inhaltlichen Texttreffer haben.
5. Beide Rankings werden mit klassischer Reciprocal Rank Fusion dedupliziert
   zusammengeführt und anschließend um relevante Nachbar- und
   Referenz-Chunks aus dem Graph ergänzt.

```bash
poetry run python rag-3a-ingest.py
poetry run python rag-4a-graph.py
poetry run python rag-4b-chat.py \
  "Wie wird die Unschuldsvermutung in BV und StPO geregelt?"
```

`rag-2a-ingest.py` und `rag-2b-chat.py` sind eine eigenständige didaktische
Stufe für Fixed-Size-Chunking. Sie sind weder Voraussetzung für GraphRAG noch
Teil der Vector-RAG-vs.-GraphRAG-Evaluation.

Der Graph wird lokal unter `.chroma/rag_semantic_graph.json` gespeichert und
nicht versioniert. Mit `GRAPH_SEED_K` und `GRAPH_CONTEXT_K` lässt sich steuern,
wie viele Vektor-Treffer und Chunks insgesamt in den Kontext gelangen.
`GRAPH_ARTICLE_K` steuert die Zahl lexikalischer Artikelkandidaten
(Standard: 2). In der Evaluation entspricht dies `--article-k`.
Nach Änderungen an der Artikelerkennung muss `rag-4a-graph.py` erneut
ausgeführt werden; Chat und Evaluation lehnen veraltete Graphformate ab.

## Evaluation: Vector-RAG vs. GraphRAG

`evaluation/questions.json` enthält Referenzfragen mit erwarteten Quellen,
Artikeln, Referenzantworten und atomaren Pflichtfakten. `evaluate.py` lässt
beide Retrieval-Varianten mit demselben Chat-Modell antworten und vergleicht:

- Quellen-Recall, Article Hit@K, Article Recall@K und Article MRR,
- Faktenabdeckung der generierten Antwort; zusammengesetzte Fakten können
  mehrere gleichzeitig erforderliche `all_of`-Bedingungen enthalten,
- Präzision erwarteter Quellen-/Artikelbezeichner, Grounding gegen die
  tatsächlich abgerufenen Artikel und Vollständigkeit der Zitate,
- Abdeckung erwarteter Begriffe als reine Retrieval-Diagnose,
- geschätzten Tokens des reinen Dokumentkontexts und des vollständigen
  Prompt-Kontexts inklusive Quellen- und Chunkbezeichnern,
- geschätzten Antwort-Tokens,
- Tokenersparnis gegenüber dem vollständigen Korpus.

```bash
poetry run python evaluate.py
```

Der generierte Bericht landet unter `evaluation/report.md` und wird nicht
versioniert. Die Tokenzahl wird näherungsweise als `Zeichen / 4` berechnet.
Das ist keine Abrechnungsmetrik, eignet sich aber für den relativen Vergleich.
Pro Referenzfrage werden zwei Chat-Anfragen ausgeführt: eine für Vector-RAG
und eine für GraphRAG. Die Bewertung selbst ist deterministisch und verwendet
keinen zusätzlichen LLM-Judge. `Term Coverage` wird ausdrücklich nicht als
Antwortqualität interpretiert.

`Expected-citation precision` prüft, ob die genannten Quellen-/Artikelpaare
zur Referenzfrage gehören. `Citation grounding` prüft zusätzlich, ob diese
Artikel tatsächlich im abgerufenen Kontext vorhanden waren. Beide Metriken
prüfen bewusst keine freie semantische Schlussfolgerung zwischen Aussage und
Gesetzestext.
Zusätze wie `Abs. 1`, `lit. a`, `Ziff. 2` oder Fussnoten dürfen im Zitat stehen;
für die Metriken wird der jeweilige Basisartikel ausgewertet.

Die strategische Perspektive ist Teil des Reports: RAG spart Tokens gegenüber
dem vollständigen Kontext. Vector-RAG und GraphRAG verwenden standardmässig
dasselbe Budget von sechs Chunks (`--context-k`), damit der Vergleich fair
bleibt. `--graph-seed-k` bestimmt, wie viele davon zunächst über die
Vektorsuche gewählt werden.

Beide Chat-Skripte können auf beide Indizes zeigen — so lassen sich die
Chunking-Strategien direkt vergleichen:

```bash
RAG_COLLECTION=rag_semantic poetry run python rag-2b-chat.py "..."
RAG_COLLECTION=rag_semantic poetry run python rag-3b-chat.py "..."
```

## Endpoint wählen (`.env`) — Key bleibt ausserhalb

`.env` enthält nur **Nicht-Geheimes**: `LLM_BASE_URL`, `LLM_MODEL`, `EMBED_MODEL`
(siehe `.env.example`). Konfiguriert ist Marvin; der Endpoint ist nur über das
AKROS-VPN erreichbar und benötigt einen passenden API-Key.

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
