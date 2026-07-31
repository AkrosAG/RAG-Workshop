
A. Der Reranker rettet die Antwort (Kern-Demo: richtiger Artikel in Top-10, aber nicht in Top-4)

1. "Darf der Arbeitgeber während der Krankheit kündigen?" — Das Schaustück. Die Antwort steht in OR Art. 336c (Sperrfrist). In 3b liegt der Chunk auf Vektor-Platz 7 und fehlt damit im Top-4-Kontext; die Antwort kommt aus Ferien-/Fürsorge-Artikeln (329b, 328a). 3c holt 336c mit Score 0.92 auf Platz 1 und zusätzlich 336d (Kündigung zur Unzeit) von Platz 8 auf Platz 3.
2. "Wann verjähren Forderungen aus einem Kaufvertrag?" — OR Art. 127 (10-Jahres-Frist) liegt in 3b auf Platz 8, in 3c auf Platz 1. Schöner Nebeneffekt für die Diskussion: 3b hat stattdessen Art. 128 (5 Jahre für periodische Leistungen) auf Platz 1 — die Antwort wird also nicht nur schlechter, sondern potenziell falsch.

B. Der Reranker wirft das falsche Gesetz raus (Präzision statt Recall)

3. "Welche Frist gilt für eine Beschwerde ans Bundesgericht?" — Beide finden BGG Art. 100. Aber 3b hat auf Platz 4 die Asyl-Beschwerdefristen (AsylG Art. 108) im Kontext; 3c wirft sie raus (Score 0.14 vs. 0.96) und zieht dafür BGG Art. 107 und 101 nach. Zeigt: Der Cross-Encoder erkennt den Gesetzeskontext der Frage, das Embedding nur die Wortähnlichkeit "Beschwerdefrist".

C. Kein Unterschied — Erwartungsmanagement

4. "Wie lange dauert die Probezeit im Arbeitsverhältnis?" — OR Art. 335b ist in beiden auf Platz 1 (Rerank-Score 0.97). Wichtig als Kontrast: Reranking ist kein Zaubertrick, sondern greift nur, wenn die Vektorsuche gut genug war, den Treffer in die Top-10 zu bringen, aber zu schlecht für die Top-4.

D. Die Grenzen von 3c (Überleitung zu Stufe 4)

5. "Kann ich eine Einwilligung zur Datenbearbeitung widerrufen?" — Alle 10 Kandidaten scoren beim Reranker fast null (≈ 0.04). Der Reranker kann nur umsortieren, was die Vektorsuche liefert — und mangels Threshold wandern die vier "am wenigsten schlechten" Chunks trotzdem ins LLM. Perfekt, um die Threshold-Frage von vorhin zu diskutieren.
6. "Was steht in Artikel 1 des OR?" — Scheitert in 3b und 3c (der richtige Chunk ist nicht mal in den Top-50 der Vektorsuche). Damit begründet sich Stufe 4: Zitierstellen brauchen exakte Auflösung statt Semantik.
