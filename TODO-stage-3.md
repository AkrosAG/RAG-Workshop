# To-do: Workshop-Stufe 3

## Zielbild

- [X] Stufe 2 unverändert lassen:
  - `rag-2a-ingest.py`: Fixed-Size-Chunking und Ingest
  - `rag-2b-chat.py`: klassische Vektorsuche mit Top-K
- [X] Stufe 3 auf genau drei aufeinander aufbauende Skripte begrenzen:
  - `rag-3a-ingest.py`: verbessertes, strukturorientiertes Chunking
  - `rag-3b-chat-classical.py`: klassische Vektorsuche auf den verbesserten Chunks
  - `rag-3c-chat-rerank.py`: dynamisches Re-Ranking der Vektorkandidaten
- [X] Hybrid Retrieval, Artikelindex, Reciprocal Rank Fusion und Graph-Erweiterung
  vollständig in Stufe 4 behandeln.

## 3a – Verbessertes Chunking

- [X] Bestehendes `rag-3a-ingest.py` als Ausgangspunkt beibehalten.
- [X] Sicherstellen, dass Überschriften und Absätze als Strukturgrenzen dienen.
- [X] Weiterhin in die eigene Collection `rag_semantic` schreiben.
- [X] Im Skript und im README deutlich machen, was sich gegenüber 2a ändert:
  Chunking-Strategie ja, Retrieval und Ranking nein.

## 3b – Klassische Abfrage

- [X] `rag-3b-chat-classical.py` aus der einfachen Retrieval-Logik von
  `rag-2b-chat.py` ableiten.
- [X] Standardmässig die Collection `rag_semantic` verwenden.
- [X] Die Frage embedden und direkt die besten `TOP_K = 4` Vektortreffer als
  Kontext verwenden.
- [X] In dieser Stufe weder Over-Fetching noch Re-Ranking einsetzen.
- [X] Quellen in der ursprünglichen Reihenfolge der Vektorsuche ausgeben.
- [X] Im Kommentar den isolierten Lerneffekt festhalten:
  gleiche Suche wie 2b, aber bessere Chunks.

## 3c – Dynamisches BGE-Re-Ranking

- [X] `rag-3c-chat-rerank.py` auf 3b aufbauen lassen.
- [X] Zunächst `TOP_N = 10` Kandidaten über die Vektorsuche abrufen.
- [X] `BAAI/bge-reranker-v2-m3` als multilingualen Cross-Encoder einsetzen.
- [X] Für jeden Kandidaten ein Paar aus `(question, chunk)` bewerten.
- [X] Nach dem BGE-Score sortieren und die besten `TOP_K = 4` Chunks behalten.
- [X] Re-Ranking-Scores, ursprünglichen Vektorrang und Quelle nachvollziehbar
  ausgeben.
- [X] Den bisherigen Chatmodell-Prompt für das Re-Ranking entfernen; das
  Chatmodell soll in 3c nur noch die abschliessende Antwort generieren.
- [X] Einen verständlichen Fehler ausgeben, wenn das Re-Ranker-Modell noch
  nicht lokal verfügbar ist oder nicht geladen werden kann.
- [X] Optional `RERANK_MODEL` als Umgebungsvariable vorsehen; Default:
  `BAAI/bge-reranker-v2-m3`.

## Abhängigkeiten und Konfiguration

- [X] `sentence-transformers` in `pyproject.toml` ergänzen.
- [X] `sentence-transformers` in `requirements.txt` ergänzen.
- [X] Lockdatei aktualisieren.
- [X] Downloadgrösse, erstmalige Modellinitialisierung und CPU-/GPU-Verhalten
  im README erwähnen.
- [X] Prüfen, ob für die Workshopumgebung ein vorab gefüllter Modell-Cache
  benötigt wird. Ergebnis: für einen zuverlässigen Workshop ohne garantierten
  Internetzugang vorab füllen; Befehl im README dokumentiert.

## Dokumentation

- [X] Stufenübersicht und Ablaufdiagramm im README aktualisieren.
- [X] Für jede Stufe einen direkt ausführbaren Beispielbefehl dokumentieren.
- [X] Den Vergleich explizit zeigen:

  ```text
  2b: Fixed-Size-Chunks  → Vector Top-4
  3b: Semantic Chunks    → Vector Top-4
  3c: Semantic Chunks    → Vector Top-10 → BGE-Re-Ranking → Top-4
  ```
- [X] Erklären, dass BGE Frage und Chunk gemeinsam verarbeitet und der
  Re-Rank-Score deshalb nicht beim Ingest vorberechnet werden kann.
- [X] Stufe 4 klar als nächsten, unabhängigen Ausbau zu Hybrid-/GraphRAG
  abgrenzen.

## Tests und Validierung

- [X] Syntaxprüfung für alle Skripte ausführen.
- [X] Testen, dass 3b ohne Re-Ranker exakt `TOP_K` Chunks verwendet.
- [X] Testen, dass 3c höchstens `TOP_N` Kandidaten bewertet und genau `TOP_K`
  übernimmt.
- [X] Testen, dass Kandidaten anhand der BGE-Scores absteigend sortiert werden.
- [X] Prüfen, dass Dokumente und Quellen nach dem Sortieren zusammenbleiben.
- [X] Mindestens eine deutsche beziehungsweise schweizerrechtliche Testfrage
  zwischen 3b und 3c vergleichen.
- [X] Vorhandene Unit-Tests und Git-Whitespace-Prüfung ausführen.
