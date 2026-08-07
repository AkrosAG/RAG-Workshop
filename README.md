# RAG-Workshop — vom Chat-Backbone zum verfeinerten RAG

Didaktische Progression in acht kleinen Skripten: Jedes baut sichtbar auf dem
vorigen auf — gleiche Konfiguration, gleiche Struktur, pro Stufe kommt genau
ein Konzept dazu. Kein Framework, keine Blackbox.

```
rag-1-chat.py          Backbone: Modell anbinden, einen Prompt absetzen
   │
rag-2a-ingest.py       + Ingest: Fixed-Size-Chunking → Embedding-DB (Chroma, file-based)
rag-2b-chat.py         + Retrieval: Abfrage mit passenden Chunks anreichern (= RAG)
   │
rag-3a-ingest.py       Verfeinerung Ingest: artikelorientiertes Legal-Chunking
rag-3b-chat-classical.py
                       Klassische Vector-Top-K-Abfrage auf den Legal-Chunks
rag-3c-chat-rerank.py  Over-Fetch + Re-Ranking mit einem BGE-Cross-Encoder
   │
rag-4a-graph.py        Graph: Nachbar-Chunks + explizite Gesetzesverweise
rag-4b-chat.py         Hybrid GraphRAG: Vektor + Artikelsuche → Graph → Antwort
```

## Die Stufen

| Skript                       | Baut auf    | Neu                                                                                                                                             |
| ---------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `rag-1-chat.py`            | —          | OpenAI-kompatibler Client, eine Chat-Anfrage                                                                                                    |
| `rag-2a-ingest.py`         | rag-1       | `chunk()` (fix), `embed()`, idempotentes Befüllen von Chroma (`rag_fixed`)                                                               |
| `rag-2b-chat.py`           | rag-1 + 2a  | Frage embedden → Top-K-Chunks holen → als Kontext in den Prompt                                                                               |
| `rag-3a-ingest.py`         | rag-2a      | artikelorientiertes Chunking für Fedlex: Rauschen filtern, an`Art.` trennen, übergrosse Artikel sicher teilen (Collection `rag_semantic`) |
| `rag-3b-chat-classical.py` | rag-2b + 3a | unveränderte Vector-Top-K-Abfrage auf den artikelorientierten Chunks                                                                           |
| `rag-3c-chat-rerank.py`    | rag-3b      | Over-Fetch (Top-10) + dynamisches BGE-Re-Ranking von Frage und Chunk → beste 4                                                                 |
| `rag-4a-graph.py`          | rag-3a      | baut einen transparenten Retrieval-Graph aus Nachbarschaft und`Art.`-Verweisen                                                                |
| `rag-4b-chat.py`           | rag-4a      | kombiniert Vektor- und lexikalische Artikeltreffer und erweitert sie über Graph-Kanten                                                         |

Alle Ingests sind **idempotent**: neue oder inhaltlich beziehungsweise durch
einen Modellwechsel veränderte Chunks werden embedded, obsolete Chunks werden
entfernt und ein unveränderter zweiter Lauf tut nichts.

## Curriculum

### Schnellstart (Hands-on: Vom Setup zur ersten belegbaren Antwort)

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
```

**Funktioniert** — Allgemeinwissen aus dem Training, flüssig und korrekt beantwortet:

```bash
poetry run python rag-1-chat.py "Wie hoch ist der aktuelle Normalsatz der Mehrwertsteuer in der Schweiz?"
```

**Funktioniert nicht mehr** — präzise Quellenarbeit. Das Modell erfindet selbstbewusst einen Wortlaut aus dem Erbrecht samt offiziell aussehendem Fedlex-Link; tatsächlich regelt Art. 721 ZGB die Aufbewahrung gefundener Sachen:

```bash
poetry run python rag-1-chat.py "Was steht in Art. 721 ZGB? Zitiere den genauen Wortlaut."
```

Ohne Grounding gibt es keine Verifizierbarkeit — genau das motiviert RAG.

### Semantic Chunking

```bash
poetry run python rag-2a-ingest.py                            # 2a: Index bauen
poetry run python rag-2b-chat.py "What is a vector database?" # 2b: RAG
```

**Funktioniert** — Faktenfragen, deren Antwort kompakt in einem Chunk liegt: korrekt 2,6 Prozent, belegt mit wörtlichem Zitat aus MWSTG Art. 25:

```bash
poetry run python rag-2b-chat.py "Wie hoch ist der reduzierte Mehrwertsteuersatz?"
```

**Funktioniert nicht mehr** — verlässliche Artikelangaben. Die Dauer stimmt (ein Monat, verlängerbar auf drei), zitiert wird aber Art. 335c statt 335b: der Fixed-Size-Schnitt trennt die Artikelüberschrift vom Text, und das Modell greift zur Nummer des Nachbarartikels im selben Chunk:

```bash
poetry run python rag-2b-chat.py "Wie lange dauert die Probezeit im Arbeitsverhältnis?"
```

**Funktioniert nicht mehr, ohne dass man es sieht** — unsichtbar unvollständige Aufzählungen. Der Fixed-Size-Schnitt trennt die Ausnahmeliste von Art. 198 ZPO direkt nach der Einleitung "Das Schlichtungsverfahren entfällt:"; die Vektorsuche erwischt nur den Chunk mit dem Listen-Ende. Die Antwort nennt darum nur die Buchstaben f–i (einzige kantonale Instanz, Widerklage, Bundespatentgericht, …) und unterschlägt a–e (summarisches Verfahren, Personenstand, Scheidung, SchKG-Klagen, …) — sie klingt vollständig, zitiert korrekt Art. 198/199 und ist trotzdem nur die halbe Liste. Nur wer das Gesetz kennt, merkt es; 3b liefert auf dieselbe Frage die komplette Aufzählung, weil Art. 198 dort als zusammenhängender Chunk im Index liegt:

```bash
poetry run python rag-2b-chat.py "In welchen Fällen entfällt das Schlichtungsverfahren?"
```

### Reranking

```bash
poetry run python rag-3a-ingest.py --dry-run                  # 3a: Chunks ohne API-Aufruf prüfen
poetry run python rag-3a-ingest.py                            # 3a: artikelorientierten Index bauen
poetry run python rag-3b-chat-classical.py "What is a vector database?" # 3b: Vector Top-K
poetry run python rag-3c-chat-rerank.py "What is a vector database?" # 3c: BGE-Re-Ranking
```

**3b funktioniert** — dieselbe Probezeit-Frage zitiert jetzt korrekt Art. 335b Abs. 1–3 (plus Art. 344a für Lehrverträge), weil die Chunks Artikelgrenzen respektieren:

```bash
poetry run python rag-3b-chat-classical.py "Wie lange dauert die Probezeit im Arbeitsverhältnis?"
```

**3b funktioniert nicht mehr** — der einschlägige Art. 336c (Sperrfristen) liegt für diese Frage nur auf Vektor-Platz 7 und fehlt damit im Top-4-Kontext; die Antwort weicht auf Probezeit- und Ferienartikel aus:

```bash
poetry run python rag-3b-chat-classical.py "Darf der Arbeitgeber während der Krankheit kündigen?"
```

**3c funktioniert** — der Cross-Encoder holt Art. 336c von Vektor-Platz 7 auf Platz 1 (Score 0.92), und die Antwort nennt die Sperrfristen von 30/90/180 Tagen:

```bash
poetry run python rag-3c-chat-rerank.py "Darf der Arbeitgeber während der Krankheit kündigen?"
```

**3c funktioniert nicht mehr** — Zitierstellen-Fragen. Der Chunk zu Art. 1 OR ist nicht einmal unter den Top-50 der Vektorsuche (die Frage trägt keinen semantischen Inhalt, und der Chunk erwähnt sein eigenes Gesetz nicht); der Reranker kann nur umsortieren, was die Vektorsuche liefert:

```bash
poetry run python rag-3c-chat-rerank.py "Was steht in Artikel 1 des OR?"
```

### Hybrid GraphRAG

```bash
poetry run python rag-4a-graph.py                              # 4a: Graph bauen
poetry run python rag-4b-chat.py "Wie lange dauert die Probezeit?" # 4b: GraphRAG
```

**Funktioniert** — Zitierstellen werden über den Artikel-Definitions-Index des Graphen exakt aufgelöst (`via: cited-article`); auch der in Stufe 1 halluzinierte Art. 721 ZGB kommt jetzt wörtlich korrekt:

```bash
poetry run python rag-4b-chat.py "Was steht in Artikel 1 des OR?"
poetry run python rag-4b-chat.py "Was steht in Art. 721 ZGB?"
```

**Funktioniert nicht mehr** — Aggregation über den ganzen Korpus. Retrieval liefert einzelne Chunks, zählen kann es nicht; die Antwort stellt immerhin ehrlich fest, dass die Zahl nicht im Kontext steht:

```bash
poetry run python rag-4b-chat.py "Wie viele Artikel hat das ZGB?"
```

Solche Fragen brauchen andere Werkzeuge (Korpus-Statistik, agentische Ansätze) — die Grenze von Retrieval-Systemen insgesamt.

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
und `rag-3a-ingest.py` die erzeugten `data/SR_*.md` automatisch. Stage 3
entfernt die Seitenmarker beim Chunking wieder, damit sie nicht im
Retrieval-Kontext landen.

Die Ingestion verarbeitet den großen Rechtskorpus in Batches von 64 Chunks.
Bei Bedarf lässt sich die Größe über `EMBED_BATCH_SIZE` reduzieren.

## Klassisches Retrieval und Re-Ranking

Stufe 3 trennt zwei Verbesserungen bewusst voneinander. `rag-3a-ingest.py`
verbessert ausschliesslich das Chunking für Gesetzestexte:

- PDF-Seitenmarker, offensichtliche Inhaltsverzeichnisse und isolierte
  Fedlex-Quellenfragmente werden nicht indexiert.
- Eine Zeile mit `Art. <Nummer>` beginnt primär einen neuen Chunk.
- Ein Artikel bleibt bis zum Grössenbudget von 800 Zeichen zusammen.
- Übergrosse Artikel werden bevorzugt an Absätzen, nummerierten Bestimmungen
  und Satzgrenzen geteilt; Fortsetzungen behalten die Artikelbezeichnung.
- Kleine zusammengehörige Textblöcke werden bis zum Budget kombiniert.

Mit `--dry-run` lassen sich Anzahl und Längen der erzeugten Chunks sowie leere,
übergrosse oder mehrere Artikel enthaltende Chunks prüfen, ohne Embeddings zu
erzeugen oder Chroma zu verändern:

```bash
poetry run python rag-3a-ingest.py --dry-run
poetry run python rag-3a-ingest.py
```

Der Stage-3-Index liegt unter `.chroma-3`; die Collection heisst trotz der
neuen Chunking-Strategie weiterhin `rag_semantic`. Die Metadaten jedes Chunks
enthalten zusätzlich `chunk_strategy=legal-article-v1`.

`rag-3b-chat-classical.py` fragt diesen Index weiterhin nur mit klassischer
Vektorsuche ab und verwendet die vier ähnlichsten Chunks direkt als Kontext.
Das Legal-Chunking verbessert die Artikelgrenzen, garantiert bei kurzen,
mehrdeutigen Fragen wie `Was steht in Art. 1 OR?` aber noch keinen exakten
Artikeltreffer: 3b wertet Gesetzesabkürzung und Artikelnummer nicht als
strukturierte Filter aus.

`rag-3c-chat-rerank.py` holt zunächst zehn Vektorkandidaten. Anschliessend
bewertet `BAAI/bge-reranker-v2-m3` jedes Paar aus Frage und Chunk gemeinsam und
sortiert die Kandidaten nach diesem Relevanzscore neu. Nur die besten vier
Chunks gelangen in den Antwort-Prompt:

```text
2b: Fixed-Size-Chunks → Vector Top-4
3b: Legal Chunks      → Vector Top-4
3c: Legal Chunks      → Vector Top-10 → BGE-Re-Ranking → Top-4
```

Der Cross-Encoder wird beim ersten Start heruntergeladen und danach im lokalen
Hugging-Face-Cache wiederverwendet. Der Download ist deutlich grösser als die
Workshop-Skripte selbst; CPU-Inferenz funktioniert, eine unterstützte GPU
beschleunigt das Re-Ranking. Über `RERANK_MODEL` kann ein anderes kompatibles
Cross-Encoder-Modell gewählt werden.

Alternativ kann das Re-Ranking über einen Jina-kompatiblen Remote-Endpoint laufen: `RERANK_URL` auf den Endpoint setzen und `RERANK_MODEL` auf das dortige Modell (siehe `.env.example`, für Marvin: `NexaAI/jina-v2-rerank-mlx`). Damit entfallen Modell-Download und lokale Inferenz; dafür braucht der virtuelle Key Zugriff auf das Rerank-Modell.

Für eine Workshopumgebung ohne verlässlichen Internetzugang sollte der
Modell-Cache vorab gefüllt werden. Auf jedem Workshop-Rechner einmal ausführen:

```bash
poetry run python -c "from sentence_transformers import CrossEncoder; CrossEncoder('BAAI/bge-reranker-v2-m3')"
```

Anschliessend lässt sich der Re-Ranker aus dem lokalen Hugging-Face-Cache
starten. Ohne vorab gefüllten Cache benötigt der erste Lauf Internetzugang und
kann wegen des Modelldownloads deutlich länger dauern.

Ein Re-Rank-Score kann nicht beim Ingest vorberechnet werden: Anders als ein
Embedding verarbeitet der Cross-Encoder Frage und Chunk gemeinsam. Das
Re-Ranking findet deshalb bei jeder Abfrage statt. Der Reranker kann nur die
zehn zuvor von der Vektorsuche gelieferten Kandidaten neu sortieren; einen dort
fehlenden Artikel kann er nicht nachträglich aus der Collection holen.

## GraphRAG

Die GraphRAG-Stufe verwendet bewusst kein Graph-Framework. Dadurch bleibt die
Mechanik im Workshop sichtbar:

1. `rag-3a-ingest.py` erzeugt den semantisch gechunkten Chroma-Index.
2. `rag-4a-graph.py` verbindet aufeinanderfolgende Chunks derselben Quelle und
   erkannte Gesetzesverweise wie `Art. 25`.
3. `rag-4b-chat.py` sucht semantische Vektor-Seeds.
4. Explizit zitierte Artikel in der Frage („Was steht in Artikel 1 des OR?") werden über den Artikel-Definitions-Index des Graphen exakt aufgelöst und priorisiert in den Kontext übernommen. Embeddings können blosse Artikelnummern nicht zuverlässig matchen; ohne genannten Erlass wird nur eine korpusweit eindeutige Nummer aufgelöst.
5. Ein kleiner BM25-ähnlicher Index sucht parallel in den normalisierten
   Artikel-Chunks. Erlassnamen und Abkürzungen wie `ZGB`, `StGB` oder `MWSTG`
   verstärken nur Artikel, die zugleich einen inhaltlichen Texttreffer haben.
6. Beide Rankings werden mit klassischer Reciprocal Rank Fusion dedupliziert
   zusammengeführt und anschließend um relevante Nachbar- und
   Referenz-Chunks aus dem Graph ergänzt.

```bash
poetry run python rag-3a-ingest.py
poetry run python rag-4a-graph.py
poetry run python rag-4b-chat.py \
  "Wie wird die Unschuldsvermutung in BV und StPO geregelt?"
```

`rag-2a-ingest.py` und `rag-2b-chat.py` sind eine eigenständige didaktische
Stufe für Fixed-Size-Chunking. Sie sind keine Voraussetzung für GraphRAG, werden
in der kumulativen Workshop-Evaluation aber als Ausgangsbasis mitgeführt.

Der Graph wird lokal unter `.chroma-3/rag_semantic_graph.json` gespeichert und
nicht versioniert. Mit `GRAPH_SEED_K` und `GRAPH_CONTEXT_K` lässt sich steuern,
wie viele Vektor-Treffer und Chunks insgesamt in den Kontext gelangen.
`GRAPH_ARTICLE_K` steuert die Zahl lexikalischer Artikelkandidaten
(Standard: 2). In der Evaluation entspricht dies `--article-k`.
Nach Änderungen an der Artikelerkennung muss `rag-4a-graph.py` erneut
ausgeführt werden; Chat und Evaluation lehnen veraltete Graphformate ab.

## Kumulative Workshop-Evaluation

`evaluation/questions.json` enthält die Fragen aus `samples.md` mit erwarteten
Quellen, Artikeln, Referenzantworten und atomaren Pflichtfakten. `evaluate.py`
lässt die für eine Workshop-Stufe verfügbaren RAG-Varianten mit demselben
Chat-Modell antworten und vergleicht:

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
# Stufe 2: nur Fixed-Size-Vector-RAG
poetry run python evaluate.py --stage fixed

# Stufe 3a/3b: Fixed-Size plus strukturorientiertes Chunking
poetry run python evaluate.py --stage semantic

# Stufe 3c: zusätzlich Cross-Encoder-Reranking
poetry run python evaluate.py --stage rerank

# Stufe 4: zusätzlich hybrides GraphRAG (Standard)
poetry run python evaluate.py --stage graph
```

Die Stufen sind kumulativ: Jede neue Stufe führt auch alle bisherigen RAGs aus.
Für gezielte Versuche überschreibt `--methods` die Stufenauswahl:

```bash
poetry run python evaluate.py --methods semantic-vector rerank
```

Verfügbare Methoden sind `fixed-vector`, `semantic-vector`, `rerank` und
`graph`. Für `fixed-vector` muss `.chroma-2/rag_fixed`, für die übrigen Methoden
`.chroma-3/rag_semantic` vorhanden sein. Die Namen lassen sich mit
`--fixed-collection` und `--semantic-collection` beziehungsweise dem bisherigen
Alias `--collection` ändern. `--rerank-candidates` steuert, wie viele semantische
Treffer der Cross-Encoder bewertet; standardmässig sind es zehn.

Der generierte Bericht landet unter `evaluation/report.md` und wird nicht
versioniert. Die Tokenzahl wird näherungsweise als `Zeichen / 4` berechnet.
Das ist keine Abrechnungsmetrik, eignet sich aber für den relativen Vergleich.
Pro Referenzfrage wird je ausgewählter Methode eine Chat-Anfrage ausgeführt.
Die Bewertung selbst ist deterministisch und verwendet keinen zusätzlichen
LLM-Judge. `Term Coverage` wird ausdrücklich nicht als Antwortqualität
interpretiert.

`Expected-citation precision` prüft, ob die genannten Quellen-/Artikelpaare
zur Referenzfrage gehören. `Citation grounding` prüft zusätzlich, ob diese
Artikel tatsächlich im abgerufenen Kontext vorhanden waren. Beide Metriken
prüfen bewusst keine freie semantische Schlussfolgerung zwischen Aussage und
Gesetzestext.
Zusätze wie `Abs. 1`, `lit. a`, `Ziff. 2` oder Fussnoten dürfen im Zitat stehen;
für die Metriken wird der jeweilige Basisartikel ausgewertet.

Die strategische Perspektive ist Teil des Reports: RAG spart Tokens gegenüber
dem vollständigen Kontext. Alle Methoden verwenden standardmässig dasselbe
finale Budget von sechs Chunks (`--context-k`), damit der Vergleich fair bleibt.
`--graph-seed-k` bestimmt, wie viele GraphRAG-Kandidaten zunächst über die
Vektorsuche gewählt werden.

Die Stage-3-Chats verwenden standardmässig den von `rag-3a-ingest.py`
erzeugten Index:

```bash
RAG_COLLECTION=rag_semantic poetry run python rag-3b-chat-classical.py "..."
RAG_COLLECTION=rag_semantic poetry run python rag-3c-chat-rerank.py "..."
```

## Endpoint wählen (`.env`) — Key bleibt ausserhalb

`.env` enthält nur **Nicht-Geheimes**: `LLM_BASE_URL`, `LLM_MODEL`,
`EMBED_MODEL` und `RERANK_MODEL` (siehe `.env.example`). Konfiguriert ist
Marvin; der Endpoint ist nur über das AKROS-VPN erreichbar und benötigt einen
passenden API-Key. Der Re-Ranker läuft lokal.

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
├── rag-1-chat.py … rag-3c-chat-rerank.py
├── pyproject.toml            # Laufzeit- und optionale Notebook-Abhängigkeiten
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
- **Re-Ranking:** Kandidatenzahl, Modell und Laufzeit vergleichen.
- **Query Rewriting:** die Frage vor dem Embedden umformulieren/erweitern.
- **Evaluation:** beide Indizes und beide Retrieval-Varianten gegen Referenzfragen messen.
