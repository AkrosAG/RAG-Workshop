## SQL query for semantic chunking integrity

WITH chunks AS (
    SELECT
        e.embedding_id AS chunk_id,
        MAX(
            CASE
                WHEN m.key = 'source'
                THEN m.string_value
            END
        ) AS source,
        MAX(
            CASE
                WHEN m.key = 'chroma:document'
                THEN m.string_value
            END
        ) AS document,
        CAST(
            substr(
                e.embedding_id,
                instr(e.embedding_id, '::') + 2
            ) AS INTEGER
        ) AS chunk_no
    FROM embeddings e
    JOIN segments s
        ON s.id = e.segment_id
    JOIN collections c
        ON c.id = s.collection
    JOIN embedding_metadata m
        ON m.id = e.id
    WHERE c.name = 'rag_semantic'
    GROUP BY e.id, e.embedding_id
),
boundaries AS (
    SELECT
        *,
        lead(document) OVER (
            PARTITION BY source
            ORDER BY chunk_no
        ) AS next_document
    FROM chunks
)
SELECT
    chunk_id,
    source,
    chunk_no,
    length(document) AS chunk_length,
    document,
    next_document
FROM boundaries
WHERE source = 'SR_101_BV_de.md'
  AND next_document IS NOT NULL
ORDER BY chunk_no;



## Verbesserungsvorschlag AI-basiert:
Die Chunks sind im Sinne des aktuellen Algorithmus korrekt gespeichert:
keine verlorenen Daten
keine veralteten Chunks
keine leeren Chunks
keine durch Stage 3 erzeugten Worttrennungen
Überschriften beginnen jeweils einen neuen Chunk
Für gutes semantisches Retrieval sind sie aber nur teilweise optimal:
40,7 % überschreiten das Größenbudget
1.694 Chunks enthalten mehrere Artikel
Inhaltsverzeichnisse erzeugen Chunks mit mehr als 3.000 Zeichen
viele Fussnoten und Quellenhinweise bilden eigene Mini-Chunks
Die sinnvollste Verbesserung wäre:
Markdown-Blöcke
  → Inhaltsverzeichnisse und isolierte Fussnoten erkennen
  → primär an Art.-Überschriften trennen
  → übergroße Artikelblöcke zusätzlich an Satzgrenzen trennen
  → kleine zusammengehörige Blöcke bis zum Budget zusammenführen
Damit würden Artikel möglichst vollständig bleiben, ohne dass ein Chunk gleichzeitig acht verschiedene Artikel oder ganze Inhaltsverzeichnisse enthält. Ich habe bei dieser Prüfung noch nichts verändert.