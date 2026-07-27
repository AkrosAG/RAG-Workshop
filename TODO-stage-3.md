# To-do: Workshop-Stufe 3

## Zielbild

- [ ] Stufe 2 unverändert lassen:
  - `rag-2a-ingest.py`: Fixed-Size-Chunking und Ingest
  - `rag-2b-chat.py`: klassische Vektorsuche mit Top-K
- [ ] Stufe 3 auf genau drei aufeinander aufbauende Skripte begrenzen:
  - `rag-3a-ingest.py`: verbessertes, strukturorientiertes Chunking
  - `rag-3b-chat-classical.py`: klassische Vektorsuche auf den verbesserten Chunks
  - `rag-3c-chat-rerank.py`: dynamisches Re-Ranking der Vektorkandidaten
- [ ] Hybrid Retrieval, Artikelindex, Reciprocal Rank Fusion und Graph-Erweiterung
  vollständig in Stufe 4 behandeln.

## 3a – Verbessertes Chunking

- [ ] Bestehendes `rag-3a-ingest.py` als Ausgangspunkt beibehalten.
- [ ] Sicherstellen, dass Überschriften und Absätze als Strukturgrenzen dienen.
- [ ] Weiterhin in die eigene Collection `rag_semantic` schreiben.
- [ ] Im Skript und im README deutlich machen, was sich gegenüber 2a ändert:
  Chunking-Strategie ja, Retrieval und Ranking nein.

## 3b – Klassische Abfrage

- [ ] `rag-3b-chat-classical.py` aus der einfachen Retrieval-Logik von
  `rag-2b-chat.py` ableiten.
- [ ] Standardmässig die Collection `rag_semantic` verwenden.
- [ ] Die Frage embedden und direkt die besten `TOP_K = 4` Vektortreffer als
  Kontext verwenden.
- [ ] In dieser Stufe weder Over-Fetching noch Re-Ranking einsetzen.
- [ ] Quellen in der ursprünglichen Reihenfolge der Vektorsuche ausgeben.
- [ ] Im Kommentar den isolierten Lerneffekt festhalten:
  gleiche Suche wie 2b, aber bessere Chunks.

## 3c – Dynamisches BGE-Re-Ranking

- [ ] `rag-3c-chat-rerank.py` auf 3b aufbauen lassen.
- [ ] Zunächst `TOP_N = 10` Kandidaten über die Vektorsuche abrufen.
- [ ] `BAAI/bge-reranker-v2-m3` als multilingualen Cross-Encoder einsetzen.
- [ ] Für jeden Kandidaten ein Paar aus `(question, chunk)` bewerten.
- [ ] Nach dem BGE-Score sortieren und die besten `TOP_K = 4` Chunks behalten.
- [ ] Re-Ranking-Scores, ursprünglichen Vektorrang und Quelle nachvollziehbar
  ausgeben.
- [ ] Den bisherigen Chatmodell-Prompt für das Re-Ranking entfernen; das
  Chatmodell soll in 3c nur noch die abschliessende Antwort generieren.
- [ ] Einen verständlichen Fehler ausgeben, wenn das Re-Ranker-Modell noch
  nicht lokal verfügbar ist oder nicht geladen werden kann.
- [ ] Optional `RERANK_MODEL` als Umgebungsvariable vorsehen; Default:
  `BAAI/bge-reranker-v2-m3`.

## Abhängigkeiten und Konfiguration

- [ ] `sentence-transformers` in `pyproject.toml` ergänzen.
- [ ] `sentence-transformers` in `requirements.txt` ergänzen.
- [ ] Lockdatei aktualisieren.
- [ ] Downloadgrösse, erstmalige Modellinitialisierung und CPU-/GPU-Verhalten
  im README erwähnen.
- [ ] Prüfen, ob für die Workshopumgebung ein vorab gefüllter Modell-Cache
  benötigt wird.

## Dokumentation

- [ ] Stufenübersicht und Ablaufdiagramm im README aktualisieren.
- [ ] Für jede Stufe einen direkt ausführbaren Beispielbefehl dokumentieren.
- [ ] Den Vergleich explizit zeigen:

  ```text
  2b: Fixed-Size-Chunks  → Vector Top-4
  3b: Semantic Chunks    → Vector Top-4
  3c: Semantic Chunks    → Vector Top-10 → BGE-Re-Ranking → Top-4
  ```

- [ ] Erklären, dass BGE Frage und Chunk gemeinsam verarbeitet und der
  Re-Rank-Score deshalb nicht beim Ingest vorberechnet werden kann.
- [ ] Stufe 4 klar als nächsten, unabhängigen Ausbau zu Hybrid-/GraphRAG
  abgrenzen.

## Tests und Validierung

- [ ] Syntaxprüfung für alle Skripte ausführen.
- [ ] Testen, dass 3b ohne Re-Ranker exakt `TOP_K` Chunks verwendet.
- [ ] Testen, dass 3c höchstens `TOP_N` Kandidaten bewertet und genau `TOP_K`
  übernimmt.
- [ ] Testen, dass Kandidaten anhand der BGE-Scores absteigend sortiert werden.
- [ ] Prüfen, dass Dokumente und Quellen nach dem Sortieren zusammenbleiben.
- [ ] Mindestens eine deutsche beziehungsweise schweizerrechtliche Testfrage
  zwischen 3b und 3c vergleichen.
- [ ] Vorhandene Unit-Tests und Git-Whitespace-Prüfung ausführen.
