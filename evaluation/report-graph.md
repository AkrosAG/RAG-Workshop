# RAG evaluation

- Methods: **fixed-vector, semantic-vector, rerank, graph**
- Collections: `fixed=rag_fixed`, `semantic=rag_semantic`
- Shared context budget: **6 chunks**
- Full corpus: approximately **1,100,916 tokens**
- Token counts are estimated as characters / 4.
- Term coverage is shown only as a retrieval diagnostic; it is not an answer-quality score.

## Retrieval

| Question | Method | Source recall | Article Hit@K | Article Recall@K | Article MRR | Term coverage (diagnostic) | Document tokens | Prompt-context tokens |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| or-kuendigung-krankheit | fixed-vector | 100% | 0% | 0% | 0.00 | 67% | 1,199 | 1,285 |
| or-kuendigung-krankheit | semantic-vector | 100% | 0% | 0% | 0.00 | 17% | 848 | 931 |
| or-kuendigung-krankheit | rerank | 100% | 100% | 100% | 1.00 | 83% | 906 | 990 |
| or-kuendigung-krankheit | graph | 100% | 100% | 100% | 0.50 | 83% | 768 | 854 |
| or-kaufvertrag-verjaehrung | fixed-vector | 100% | 100% | 100% | 1.00 | 100% | 1,198 | 1,284 |
| or-kaufvertrag-verjaehrung | semantic-vector | 100% | 0% | 0% | 0.00 | 33% | 726 | 810 |
| or-kaufvertrag-verjaehrung | rerank | 100% | 100% | 100% | 1.00 | 100% | 617 | 702 |
| or-kaufvertrag-verjaehrung | graph | 100% | 100% | 100% | 0.25 | 100% | 400 | 484 |
| bgg-beschwerdefrist | fixed-vector | 100% | 100% | 100% | 0.33 | 100% | 1,200 | 1,296 |
| bgg-beschwerdefrist | semantic-vector | 100% | 100% | 100% | 0.50 | 100% | 742 | 842 |
| bgg-beschwerdefrist | rerank | 100% | 100% | 100% | 1.00 | 100% | 774 | 872 |
| bgg-beschwerdefrist | graph | 100% | 100% | 100% | 0.33 | 100% | 789 | 887 |
| or-probezeit | fixed-vector | 100% | 0% | 0% | 0.00 | 67% | 1,200 | 1,288 |
| or-probezeit | semantic-vector | 100% | 100% | 100% | 1.00 | 67% | 813 | 901 |
| or-probezeit | rerank | 100% | 100% | 100% | 1.00 | 67% | 890 | 980 |
| or-probezeit | graph | 100% | 100% | 100% | 1.00 | 67% | 848 | 933 |
| dsg-einwilligung-widerruf | fixed-vector | 100% | 100% | 25% | 0.25 | 75% | 1,198 | 1,292 |
| dsg-einwilligung-widerruf | semantic-vector | 100% | 0% | 0% | 0.00 | 75% | 941 | 1,032 |
| dsg-einwilligung-widerruf | rerank | 100% | 100% | 25% | 0.05 | 75% | 925 | 1,015 |
| dsg-einwilligung-widerruf | graph | 100% | 100% | 25% | 0.04 | 75% | 821 | 912 |
| or-artikel-1 | fixed-vector | 100% | 100% | 100% | 1.00 | 80% | 1,198 | 1,291 |
| or-artikel-1 | semantic-vector | 100% | 0% | 0% | 0.00 | 0% | 745 | 834 |
| or-artikel-1 | rerank | 100% | 0% | 0% | 0.00 | 0% | 888 | 980 |
| or-artikel-1 | graph | 100% | 100% | 100% | 1.00 | 80% | 652 | 740 |

## Answers

| Question | Method | Fact coverage | Expected-citation precision | Citation grounding | Citation completeness | Answer tokens |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| or-kuendigung-krankheit | fixed-vector | 0% | 0% | 50% | 0% | 576 |
| or-kuendigung-krankheit | semantic-vector | 0% | 33% | 67% | 100% | 570 |
| or-kuendigung-krankheit | rerank | 67% | 50% | 100% | 100% | 542 |
| or-kuendigung-krankheit | graph | 33% | 0% | 0% | 0% | 404 |
| or-kaufvertrag-verjaehrung | fixed-vector | 100% | 33% | 67% | 100% | 243 |
| or-kaufvertrag-verjaehrung | semantic-vector | 50% | 0% | 100% | 0% | 310 |
| or-kaufvertrag-verjaehrung | rerank | 50% | 50% | 100% | 100% | 432 |
| or-kaufvertrag-verjaehrung | graph | 100% | 50% | 100% | 100% | 176 |
| bgg-beschwerdefrist | fixed-vector | 100% | 33% | 100% | 100% | 362 |
| bgg-beschwerdefrist | semantic-vector | 67% | 33% | 100% | 100% | 361 |
| bgg-beschwerdefrist | rerank | 67% | 20% | 80% | 100% | 498 |
| bgg-beschwerdefrist | graph | 67% | 50% | 100% | 100% | 304 |
| or-probezeit | fixed-vector | 67% | 0% | 100% | 0% | 227 |
| or-probezeit | semantic-vector | 67% | 50% | 100% | 100% | 437 |
| or-probezeit | rerank | 67% | 100% | 100% | 100% | 234 |
| or-probezeit | graph | 33% | 50% | 100% | 100% | 172 |
| dsg-einwilligung-widerruf | fixed-vector | 0% | 0% | 100% | 0% | 353 |
| dsg-einwilligung-widerruf | semantic-vector | 0% | 0% | 50% | 0% | 295 |
| dsg-einwilligung-widerruf | rerank | 25% | 0% | 0% | 0% | 405 |
| dsg-einwilligung-widerruf | graph | 0% | 0% | 0% | 0% | 186 |
| or-artikel-1 | fixed-vector | 100% | 100% | 100% | 100% | 66 |
| or-artikel-1 | semantic-vector | 0% | 0% | 0% | 0% | 76 |
| or-artikel-1 | rerank | 0% | 0% | 0% | 0% | 216 |
| or-artikel-1 | graph | 100% | 100% | 100% | 100% | 70 |

## Summary

- **fixed-vector:** article recall@K 54.2%, MRR 0.43, fact coverage 61.1%, expected-citation precision 27.8%, citation grounding 86.1%, citation completeness 50.0%, average context 1,289 tokens, corpus-token savings 99.88%.
- **semantic-vector:** article recall@K 33.3%, MRR 0.25, fact coverage 30.6%, expected-citation precision 19.4%, citation grounding 69.4%, citation completeness 50.0%, average context 892 tokens, corpus-token savings 99.92%.
- **rerank:** article recall@K 70.8%, MRR 0.68, fact coverage 45.8%, expected-citation precision 36.7%, citation grounding 63.3%, citation completeness 66.7%, average context 923 tokens, corpus-token savings 99.92%.
- **graph:** article recall@K 87.5%, MRR 0.52, fact coverage 55.6%, expected-citation precision 41.7%, citation grounding 66.7%, citation completeness 66.7%, average context 802 tokens, corpus-token savings 99.93%.

## Strategic token perspective

All methods receive the same final chunk budget. Because chunking and retrieval differ, their actual token counts can still differ.

In this run GraphRAG used **-10.1%** context tokens compared with semantic Vector-RAG. Interpret this together with retrieval, fact coverage and citation quality.

## Answer details

### or-kuendigung-krankheit — fixed-vector

**Reference:** Nach Ablauf der Probezeit darf der Arbeitgeber bei einer unverschuldeten krankheitsbedingten vollständigen oder teilweisen Arbeitsverhinderung während der gesetzlichen Sperrfrist nicht kündigen: 30 Tage im ersten Dienstjahr, 90 Tage vom zweiten bis und mit fünften Dienstjahr und 180 Tage ab dem sechsten Dienstjahr. Eine während der Sperrfrist ausgesprochene Kündigung ist nichtig. Wurde vorher gekündigt und läuft die Kündigungsfrist in die Sperrfrist hinein, wird ihr Ablauf unterbrochen und danach fortgesetzt. Während der Probezeit gilt dieser Schutz nicht [SR_220_OR_de.md Art. 336c].

**Generated:** Ja, der Arbeitgeber **darf grundsätzlich während der Krankheit kündigen**, jedoch **unterliegt dies bestimmten Sperrfristen und Schutzvorschriften**.

Laut Artikel 335d Absatz 1 des Obligationenrechts (SR 220 OR) gelten sogenannte **Sperrfristen für Kündigungen während bestimmter Verhinderungszeiten**. Dort ist in Artikel 335 Absatz 1 festgehalten:

> „Die Kündigung ist während folgender Fristen nichtig:  
> a. während des Urlaubs nach Artikel 329c;  
> b. während der Verhinderung des Arbeitnehmers an der Arbeitsleistung infolge von Krankheit oder Unfall, wenn sie **länger als 30 Tage** dauert, **sofern** der Arbeitnehmer dem Arbeitgeber **innerhalb von drei Tagen** nach dem ersten Tag der Verhinderung einen ärztlichen Attest vorgelegt hat;  
> c. während der Schwangerschaft und bis acht Wochen nach der Niederkunft; …“  

[SR_220_OR_de.md Art. 335]

Zudem bestimmt Artikel 328a Absatz 2 OR:

> „Wird der Arbeitnehmer **ohne sein Verschulden** durch Krankheit oder Unfall an der Arbeitsleistung verhindert, so hat der Arbeitgeber **Pflege und ärztliche Behandlung für eine beschränkte Zeit zu gewähren**, im ersten Dienstjahr für **drei Wochen** und nachher für eine **angemessene längere Zeit**, je nach der Dauer des Arbeitsverhältnisses und den besonderen Umständen.“  

[SR_220_OR_de.md Art. 328a]

Daraus folgt:  
- Während der **ersten 30 Tage der Krankheit** (sofern ärztliches Attest binnen 3 Tagen vorgelegt wurde) **darf der Arbeitgeber kündigen**, es besteht **kein Kündigungsschutz**.  
- **Ab dem 31. Tag der Verhinderung** (mit ärztlichem Attest) **darf der Arbeitgeber nicht mehr kündigen** – die Kündigung ist **nichtig**.

Zusätzlich ist zu beachten, dass bei **Kündigungen durch den Arbeitgeber** der Schutz nach Artikel 335 Absatz 1 lit. c **auch bei Schwangerschaft und Mutterschaft** greift (vgl. Art. 328a Abs. 3 OR [SR_220_OR_de.md Art. 328a]).

➡️ **Zusammenfassung:**  
Der Arbeitgeber **darf während der Krankheit kündigen**, **wenn** die Krankheit **kürzer als 30 Tage** ist **und** der Arbeitnehmer **rechtzeitig ärztlich bescheinigt** hat. **Ab dem 31. Tag** (mit Attest) ist eine Kündigung **nichtig**.

Weitere Einschränkungen ergeben sich möglicherweise aus **Gesamtarbeitsverträgen** oder **Betriebsreglementen**, sofern diese strengere Schutzfristen vorsehen.

### or-kuendigung-krankheit — semantic-vector

**Reference:** Nach Ablauf der Probezeit darf der Arbeitgeber bei einer unverschuldeten krankheitsbedingten vollständigen oder teilweisen Arbeitsverhinderung während der gesetzlichen Sperrfrist nicht kündigen: 30 Tage im ersten Dienstjahr, 90 Tage vom zweiten bis und mit fünften Dienstjahr und 180 Tage ab dem sechsten Dienstjahr. Eine während der Sperrfrist ausgesprochene Kündigung ist nichtig. Wurde vorher gekündigt und läuft die Kündigungsfrist in die Sperrfrist hinein, wird ihr Ablauf unterbrochen und danach fortgesetzt. Während der Probezeit gilt dieser Schutz nicht [SR_220_OR_de.md Art. 336c].

**Generated:** Ja, der Arbeitgeber darf während der Krankheit des Arbeitnehmers grundsätzlich kündigen, **sofern nicht besondere Schutzvorschriften greifen**.

Die schweizerische Obligationenrechtsordnung (OR) enthält keine pauschale Kündigungssperre während Krankheit. Allerdings gibt es einige wichtige Einschränkungen und Schutzvorschriften:

1. **Kündigungsschutz während Mutterschaft**:  
   Während des Mutterschaftsurlaubs (s. Art. 329f OR) und in den zwei Monaten vor der voraussichtlichen Entbindung sowie acht Wochen nach der Niederkunft ist eine Kündigung aus gesetzlichen Gründen unzulässig (Art. 336c OR i.V.m. Art. 335c OR). Diese Vorschrift schützt jedoch nicht generell vor Kündigung während Krankheit im weiteren Sinne.

2. **Kürzung von Ferien bei Krankheit**:  
   Nach Art. 329b Abs. 2 OR dürfen die Ferien **nicht gekürzt** werden, wenn die Verhinderung an der Arbeitsleistung durch Krankheit (ohne Verschulden des Arbeitnehmers) verursacht wurde und insgesamt **nicht mehr als einen Monat** im Dienstjahr beträgt.  
   Bei längerer Verhinderung (mehr als einen Monat) kann der Arbeitgeber die Ferien entsprechend kürzen (Art. 329b Abs. 1 OR).

3. **Probezeit und Krankheit**:  
   In der Probezeit kann das Arbeitsverhältnis mit einer Frist von sieben Tagen gekündigt werden (Art. 335b Abs. 1 OR). Eine Krankheit führt nicht automatisch zu einer Kündigungssperre. Allerdings wird die Probezeit nach Art. 335b Abs. 3 OR bei Krankheit entsprechend verlängert.

4. **Kein allgemeiner Kündigungsschutz bei Krankheit**:  
   Es existiert **keine allgemeine gesetzliche Kündigungssperre** bei kurzfristiger oder mittelfristiger Krankheit (im Gegensatz zu bestimmten Schutzfristen z. B. beim Mutterschaftsurlaub oder Urlaub nach den Eltern-URLAUBS-Vorschriften).

**Zusammenfassung**:  
Der Arbeitgeber darf grundsätzlich während der Krankheit kündigen, **sofern keine besonderen Schutzfristen** (z. B. Mutterschaftsschutz nach Art. 336c OR) oder tarifvertragliche/vertragliche Schutzklauseln entgegenstehen. Eine bloße Krankheit allein begründet keinen Kündigungsschutz.

Quelle: [SR_220_OR_de.md Art. 329b], [SR_220_OR_de.md Art. 335b], [SR_220_OR_de.md Art. 336c] (letzteres nicht im bereitgestellten Kontext enthalten, aber im Gesetzestext enthalten – ggf. ergänzungsbedürftig).

### or-kuendigung-krankheit — rerank

**Reference:** Nach Ablauf der Probezeit darf der Arbeitgeber bei einer unverschuldeten krankheitsbedingten vollständigen oder teilweisen Arbeitsverhinderung während der gesetzlichen Sperrfrist nicht kündigen: 30 Tage im ersten Dienstjahr, 90 Tage vom zweiten bis und mit fünften Dienstjahr und 180 Tage ab dem sechsten Dienstjahr. Eine während der Sperrfrist ausgesprochene Kündigung ist nichtig. Wurde vorher gekündigt und läuft die Kündigungsfrist in die Sperrfrist hinein, wird ihr Ablauf unterbrochen und danach fortgesetzt. Während der Probezeit gilt dieser Schutz nicht [SR_220_OR_de.md Art. 336c].

**Generated:** Nein, der Arbeitgeber darf während der Krankheit des Arbeitnehmers **nach Ablauf der Probezeit** nicht kündigen, **wenn** der Arbeitnehmer ohne eigenes Verschulden durch Krankheit oder Unfall an der Arbeitsleistung verhindert ist – **und zwar innerhalb der gesetzlich festgelegten Schutzfristen**.

Gemäss **Art. 336c Abs. 1 lit. b SR_220_OR_de.md**:

> *„Art. 336c*  
> *1 Nach Ablauf der Probezeit darf der Arbeitgeber das Arbeitsverhältnis nicht kündigen:  
> …*  
> *b. während der Arbeitnehmer ohne eigenes Verschulden durch Krankheit oder durch Unfall ganz oder teilweise an der Arbeitsleistung verhindert ist, und zwar im ersten Dienstjahr während 30 Tagen, ab zweitem bis und mit fünftem Dienstjahr während 90 Tagen und ab sechstem Dienstjahr während 180 Tagen“* [SR_220_OR_de.md Art. 336c].

Das bedeutet:  
- Im **ersten Dienstjahr**: Schutz für bis zu **30 Tage** im Jahr,  
- Im **zweiten bis fünften Dienstjahr**: Schutz für bis zu **90 Tage** im Jahr,  
- **Ab dem sechsten Dienstjahr**: Schutz für bis zu **180 Tage** im Jahr.

Innerhalb dieser Fristen darf der Arbeitgeber nicht kündigen – **auch nicht, wenn der Arbeitnehmer bereits vorher gekündigt hat oder die Kündigung mit einer fristgerechten Mitteilung versehen ist**. Diese Schutzfristen gelten nur nach Ablauf der Probezeit (vgl. Art. 336c Abs. 1).

Während der **Probezeit** hingegen ist eine Kündigung grundsätzlich möglich – auch während Krankheit – jedoch nur mit **7-tägiger Kündigungsfrist** (Art. 335b Abs. 1). Allerdings kann die Probezeit bei Krankheit **entsprechend verlängert** werden (Art. 335b Abs. 3).

Zusätzlich schreibt Art. 328a Abs. 2 vor, dass der Arbeitgeber bei Krankheit des Arbeitnehmers **Pflege und ärztliche Behandlung** leisten muss – dies ist eine Pflicht des Arbeitgebers, keine Zulassung zur Kündigung.

**Zusammenfassung**:  
- **Während Probezeit**: Kündigung möglich, aber mit 7-Tages-Frist; bei Krankheit kann die Probezeit verlängert werden (Art. 335b Abs. 1, 3) [SR_220_OR_de.md Art. 335b].  
- **Nach Probezeit**: Kündigung während Krankheit nur **außerhalb der gesetzlichen Schutzfristen** erlaubt (Art. 336c Abs. 1 lit. b) [SR_220_OR_de.md Art. 336c].

### or-kuendigung-krankheit — graph

**Reference:** Nach Ablauf der Probezeit darf der Arbeitgeber bei einer unverschuldeten krankheitsbedingten vollständigen oder teilweisen Arbeitsverhinderung während der gesetzlichen Sperrfrist nicht kündigen: 30 Tage im ersten Dienstjahr, 90 Tage vom zweiten bis und mit fünften Dienstjahr und 180 Tage ab dem sechsten Dienstjahr. Eine während der Sperrfrist ausgesprochene Kündigung ist nichtig. Wurde vorher gekündigt und läuft die Kündigungsfrist in die Sperrfrist hinein, wird ihr Ablauf unterbrochen und danach fortgesetzt. Während der Probezeit gilt dieser Schutz nicht [SR_220_OR_de.md Art. 336c].

**Generated:** Ja, der Arbeitgeber darf während der Krankheit des Arbeitnehmers **unter bestimmten Voraussetzungen** kündigen.

Laut **Art. 336c Abs. 1 lit. b SR_220_OR_de.md** ist die Kündigung während der Krankheit **ausgeschlossen**, soweit die Verhinderung **ohne eigenes Verschulden** des Arbeitnehmers (z. B. durch Krankheit oder Unfall) erfolgt – **und zwar**:

- im **ersten Dienstjahr** während **30 Tagen**,  
- ab **zweitem bis und mit fünftem Dienstjahr** während **90 Tagen**,  
- ab **sechstem Dienstjahr** während **180 Tagen**.

Das bedeutet:  
→ Innerhalb dieser Fristen ist eine Kündigung wegen Krankheit **nicht zulässig**, sofern keine andere gesetzliche oder vertragliche Grundlage vorliegt (z. B. außerordentliche Kündigung bei schwerem Verschulden).  
→ Nach Ablauf dieser Schutzfristen **darf der Arbeitgeber kündigen**, auch wenn die Krankheit noch besteht – vorausgesetzt, die allgemeinen Kündigungsregeln (z. B. Fristen, schriftliche Form) werden eingehalten.

**Zusätzlich**: Art. 328a Abs. 2 SR_220_OR_de.md regelt, dass der Arbeitgeber bei Krankheit ohne Verschulden des Arbeitnehmers eine beschränkte Zeit für Pflege und ärztliche Behandlung zu gewähren hat (im ersten Dienstjahr drei Wochen), was die Dauer des Schutzes ergänzt, aber nicht ersetzt.

**Fazit:**  
Der Arbeitgeber darf während der Krankheit **nicht innerhalb der gesetzlichen Schutzfristen nach Art. 336c Abs. 1 lit. b SR_220_OR_de.md** kündigen. Danach ist eine ordentliche Kündigung grundsätzlich möglich, sofern weitere Rechtsvorschriften (z. B. Kündigungsschutzgesetze bei besonders schutzbedürftigen Personen) nicht entgegenstehen.

### or-kaufvertrag-verjaehrung — fixed-vector

**Reference:** Für Forderungen aus einem Kaufvertrag gilt grundsätzlich die allgemeine Verjährungsfrist von zehn Jahren, sofern das Bundeszivilrecht für den konkreten Anspruch keine abweichende Frist vorsieht [SR_220_OR_de.md Art. 127].

**Generated:** Forderungen aus einem Kaufvertrag verjähren grundsätzlich mit Ablauf von **zehn Jahren**, sofern das Bundeszivilrecht nichts anderes bestimmt (Art. 127 OR) [SR_220_OR_de.md Art. 127].

Allerdings gibt es für bestimmte Ansprüche aus dem Kaufvertrag kürzere Verjährungsfristen:

- **Gewährleistungsansprüche wegen Mängeln der Sache** verjähren mit Ablauf von **zwei Jahren** nach deren Ablieferung an den Käufer, selbst wenn dieser die Mängel erst später entdeckt (Art. 21075 Abs. 1 OR) [SR_220_OR_de.md Art. 21075].

- **Ansprüche des Käufers wegen Mängeln des Grundstücks** verjähren mit Ablauf von **fünf Jahren** nach dem Erwerb des Eigentums (Art. 149 OR) [SR_220_OR_de.md Art. 149].

Die allgemeine Verjährungsfrist von zehn Jahren (Art. 127 OR) bleibt unberührt für Forderungen, für die keine spezielle Verjährungsfrist bestimmt ist, z. B. für Zahlungsansprüche aus dem Kaufvertrag, sofern sie nicht bereits verfallen sind (z. B. aufgrund der Gewährleistungsfristen).

### or-kaufvertrag-verjaehrung — semantic-vector

**Reference:** Für Forderungen aus einem Kaufvertrag gilt grundsätzlich die allgemeine Verjährungsfrist von zehn Jahren, sofern das Bundeszivilrecht für den konkreten Anspruch keine abweichende Frist vorsieht [SR_220_OR_de.md Art. 127].

**Generated:** Forderungen aus einem Kaufvertrag verjähren **mit Ablauf von zwei Jahren nach deren Ablieferung an den Käufer**, sofern nicht eine längere Haftungsfrist vereinbart wurde. Dies gilt insbesondere für Gewährleistungsansprüche wegen Mängel der Sache [SR_220_OR_de.md Art. 21075].

Zusätzlich können andere Forderungen aus dem Kaufvertrag (z. B. Schadensersatz außerhalb der Gewährleistung, Zahlungsansprüche) einer gesetzlichen Verjährungsfrist unterliegen, je nach Art der Forderung. So verjähren beispielsweise allgemeine Ansprüche aus einem Vertrag, sofern nicht gesondert geregelt, nach der allgemeinen Verjährungsfrist von zehn Jahren gemäß § 127 I ZGB (nicht im gegebenen Kontext aufgeführt, aber gesetzlich festgelegt). Der vorliegende Kontext enthält jedoch nur die spezifische Regelung für Gewährleistungsansprüche aus dem Kaufvertrag.

Somit lautet die direkte Antwort auf die Frage anhand des gegebenen Kontexts:

**Forderungen aus einem Kaufvertrag im Sinne von Gewährleistungsansprüchen wegen Mängel der Sache verjähren mit Ablauf von zwei Jahren nach deren Ablieferung an den Käufer, selbst wenn diese Mängel erst später entdeckt werden, es sei denn, der Verkäufer hat eine längere Haftung übernommen [SR_220_OR_de.md Art. 21075].**

### or-kaufvertrag-verjaehrung — rerank

**Reference:** Für Forderungen aus einem Kaufvertrag gilt grundsätzlich die allgemeine Verjährungsfrist von zehn Jahren, sofern das Bundeszivilrecht für den konkreten Anspruch keine abweichende Frist vorsieht [SR_220_OR_de.md Art. 127].

**Generated:** Im Schweizerischen Obligationenrecht (OR) gibt es keine allgemeine spezifische Verjährungsfrist für **Forderungen aus einem Kaufvertrag** als solche. Die Verjährung richtet sich nach der Art der Forderung, die aus dem Kaufvertrag entsteht.

Zu unterscheiden sind beispielsweise:

- **Mängelansprüche des Bestellers** (Art. 371 OR):  
  – Bei beweglichen Sachen: **zwei Jahre** nach der Abnahme des Werkes (Art. 371 Abs. 1 OR) [SR_220_OR_de.md Art. 371].  
  – Bei Mängeln beweglicher Werke, die in unbewegliche Werke integriert sind: **fünf Jahre** (ebd.).  
  – Bei unbeweglichen Werken: **fünf Jahre** seit der Abnahme (Art. 371 Abs. 2 OR) [SR_220_OR_de.md Art. 371].

- **Preisforderungen des Verkäufers** oder **Kontereklageforderungen des Käufers** (z. B. auf Rückgewähr des Kaufpreises bei Rückspruch oder Mangel):  
  Diese fallen grundsätzlich unter die **Allgemeine Verjährungsfrist von zehn Jahren** nach Art. 127 OR, es sei denn, eine speziellere Vorschrift greift (ebd.) [SR_220_OR_de.md Art. 127].

- **Schadensersatzforderungen** infolge eines Mangels oder vertragswidrigen Verhaltens beim Kauf:  
  Hier ist eventuell Art. 128a OR anzuwenden (Verjährung von drei Jahren ab Kenntnis des Schadens, spätestens zwanzig Jahre nach dem schädigenden Verhalten), sofern es sich um eine Körperverletzung oder Tötung handelt – andernfalls grundsätzlich die 10-Jahres-Verjährung (Art. 127 OR) [SR_220_OR_de.md Art. 128a, Art. 127].

Fazit:  
**Forderungen aus einem Kaufvertrag verjähren je nach Art der Forderung unterschiedlich**, meistentends nach den spezifischen Vorschriften zu Werksverträgen (Art. 371 OR) oder nach der allgemeinen Frist von **zehn Jahren** (Art. 127 OR), sofern keine kürzere spezielle Frist gilt.

### or-kaufvertrag-verjaehrung — graph

**Reference:** Für Forderungen aus einem Kaufvertrag gilt grundsätzlich die allgemeine Verjährungsfrist von zehn Jahren, sofern das Bundeszivilrecht für den konkreten Anspruch keine abweichende Frist vorsieht [SR_220_OR_de.md Art. 127].

**Generated:** Forderungen aus einem Kaufvertrag verjähren grundsätzlich mit Ablauf von **zehn Jahren**, sofern das Bundeszivilrecht nicht etwas anderes bestimmt [SR_220_OR_de.md Art. 127].

Für **Gewährleistungsansprüche wegen Mängel der Sache** gilt eine spezielle Verjährungsfrist von **zwei Jahren** nach Ablieferung der Sache an den Käufer, selbst wenn der Mangel erst später entdeckt wird – es sei denn, der Verkäufer hat eine längere Haftung übernommen [SR_220_OR_de.md Art. 21075].

Für andere Forderungen aus einem Kaufvertrag, die nicht unter die Gewährleistung fallen (z. B. Schadensersatz außerhalb des Gewährleistungsrechts), greift die allgemeine Verjährungsfrist von zehn Jahren [SR_220_OR_de.md Art. 127].

### bgg-beschwerdefrist — fixed-vector

**Reference:** Grundsätzlich ist die Beschwerde gegen einen Entscheid innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen. Artikel 100 BGG sieht für bestimmte Fälle kürzere Fristen von zehn, fünf oder drei Tagen vor; gegen das unrechtmässige Verweigern oder Verzögern eines Entscheids kann jederzeit Beschwerde geführt werden [SR_173.110_BGG_de.md Art. 100].

**Generated:** Die allgemeine Beschwerdefrist beim Bundesgericht beträgt **30 Tage** nach der Eröffnung der vollständigen Ausfertigung des Entscheids [SR_173.110_BGG_de.md Art. 100 Abs. 1].

Es bestehen jedoch Ausnahmen mit kürzeren Fristen:

- **10 Tage** bei Entscheiden der kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen sowie bei Entscheiden in den Bereichen internationale Rechtshilfe im Strafrecht und internationaler Kindesentführung [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. a, c, d].

- **5 Tage** bei Entscheiden der kantonalen Aufsichtsbehörden im Rahmen der Wechselbetreibung sowie bei Entscheiden der Kantonsregierungen über Beschwerden gegen eidgenössische Abstimmungen [SR_173.110_BGG_de.md Art. 100 Abs. 3 lit. a, b].

- **3 Tage** bei Beschwerden gegen die Nationalratswahlen [SR_173.110_BGG_de.md Art. 100 Abs. 4].

Für Beschwerden gegen Beschlüsse im Asylverfahren gelten zudem abweichende Fristen, z. B. **7 Arbeitstage** im beschleunigten Verfahren und **30 Tage** im erweiterten Verfahren [SR_142.31_AsylG_de.md Art. 108 Abs. 1].

In Zivilsachen gemäss ZPO gilt für die Beschwerde bei erstinstanzlichen Entscheiden und prozessleitenden Verfügungen grundsätzlich **10 Tage**, es sei denn, das Gesetz sieht etwas anderes vor [SR_272_ZPO_de.md Art. 321 Abs. 2].

Zusammenfassend: Die **allgemeine Beschwerdefrist beim Bundesgericht beträgt 30 Tage**, es können aber – je nach Art des Entscheids – kürzere Fristen gelten.

### bgg-beschwerdefrist — semantic-vector

**Reference:** Grundsätzlich ist die Beschwerde gegen einen Entscheid innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen. Artikel 100 BGG sieht für bestimmte Fälle kürzere Fristen von zehn, fünf oder drei Tagen vor; gegen das unrechtmässige Verweigern oder Verzögern eines Entscheids kann jederzeit Beschwerde geführt werden [SR_173.110_BGG_de.md Art. 100].

**Generated:** Die allgemeine Frist für eine Beschwerde ans Bundesgericht beträgt **30 Tage** nach der Eröffnung der vollständigen Ausfertigung des Entscheids [SR_173.110_BGG_de.md Art. 100 Abs. 1].

Zusätzlich gibt es spezielle, verkürzte Fristen für bestimmte Entscheide:

- **10 Tage** für Entscheide der kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen (Art. 100 Abs. 2 lit. a) sowie für Entscheide auf den Gebieten der internationalen Rechtshilfe in Strafsachen und der internationalen Amtshilfe in Steuersachen (Art. 100 Abs. 2 lit. b) [SR_173.110_BGG_de.md Art. 100 Abs. 2].
- **5 Tage** für Entscheide der kantonalen Aufsichtsbehörden im Rahmen der Wechselbetreibung sowie für Entscheide der Kantonsregierungen über Beschwerden gegen eidgenössische Abstimmungen (Art. 100 Abs. 3 lit. a und b) [SR_173.110_BGG_de.md Art. 100 Abs. 3].
- **3 Tage** für Entscheide der Kantonsregierungen über Beschwerden gegen die Nationalratswahlen (Art. 100 Abs. 4) [SR_173.110_BGG_de.md Art. 100 Abs. 4].

Für Beschwerden gegen Erweise beträgt die Frist ebenfalls **30 Tage** nach der nach kantonalem Recht massgebenden Veröffentlichung (Art. 101) [SR_173.110_BGG_de.md Art. 101].

In Asylsachen gelten getrennte Fristen:  
- **7 Arbeitstage** im beschleunigten Verfahren,  
- **30 Tage** im erweiterten Verfahren,  
- **5 Arbeitstage** bei Nichteintretensentscheiden und bestimmten anderen Entscheiden (Art. 108) [SR_142.31_AsylG_de.md Art. 108].

### bgg-beschwerdefrist — rerank

**Reference:** Grundsätzlich ist die Beschwerde gegen einen Entscheid innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen. Artikel 100 BGG sieht für bestimmte Fälle kürzere Fristen von zehn, fünf oder drei Tagen vor; gegen das unrechtmässige Verweigern oder Verzögern eines Entscheids kann jederzeit Beschwerde geführt werden [SR_173.110_BGG_de.md Art. 100].

**Generated:** Die allgemeine Frist für eine Beschwerde ans Bundesgericht beträgt **30 Tage**, und zwar **nach der Eröffnung der vollständigen Ausfertigung des Entscheids** [SR_173.110_BGG_de.md Art. 100 Abs. 1].

Es bestehen jedoch Ausnahmen mit verkürzten Fristen:

- **10 Tage** bei:
  - Entscheiden der kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. a];
  - Entscheiden im Bereich der internationalen Rechtshilfe in Strafsachen und internationalen Amtshilfe in Steuersachen [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. b];
  - Entscheiden über die Rückgabe eines Kindes nach dem Europäischen Übereinkommen vom 20. Mai 1980 (Haager Kindesentführungsübereinkommen) oder nach dem Übereinkommen vom 25. Oktober 1980 (zivilrechtliche Aspekte internationaler Kindesentführung) [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. c];
  - Entscheiden des Bundespatentgerichts über die Erteilung einer Lizenz nach § 40d PatG [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. d].

- **5 Tage** bei:
  - Entscheiden der kantonalen Aufsichtsbehörden im Rahmen der Wechselbetreibung (Schuldbetreibung/Konkurs) [SR_173.110_BGG_de.md Art. 103 Abs. 2 lit. a];
  - Entscheiden der Kantonsregierungen über Beschwerden gegen eidgenössische Abstimmungen [SR_173.110_BGG_de.md Art. 103 Abs. 2 lit. b].

- **3 Tage** bei Entscheiden der Kantonsregierungen über Beschwerden gegen die Nationalratswahlen [SR_173.110_BGG_de.md Art. 103 Abs. 3].

Zudem gilt für die Beschwerde gegen einen Erlass eine Frist von **30 Tagen nach der nach dem kantonalen Recht massgebenden Veröffentlichung des Erlasses** [SR_173.110_BGG_de.md Art. 101].

Im Zusammenhang mit Revisionsgesuchen (nicht Beschwerden im engeren Sinne) gelten nach § 124 BGG ebenfalls 30 bzw. 90 Tage, je nach Revisionsgrund [SR_173.110_BGG_de.md Art. 124].

Zusätzlich gilt für das Amtshilferecht (ATSG) eine allgemeine Frist von **30 Tagen nach der Eröffnung des Einspracheentscheides** [SR_830.1_ATSG_de.md Art. 60 Abs. 1].

### bgg-beschwerdefrist — graph

**Reference:** Grundsätzlich ist die Beschwerde gegen einen Entscheid innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen. Artikel 100 BGG sieht für bestimmte Fälle kürzere Fristen von zehn, fünf oder drei Tagen vor; gegen das unrechtmässige Verweigern oder Verzögern eines Entscheids kann jederzeit Beschwerde geführt werden [SR_173.110_BGG_de.md Art. 100].

**Generated:** Die allgemeine Beschwerdefrist beim Bundesgericht beträgt **30 Tage**, gemäss Art. 100 Abs. 1 Bundesgerichtsgesetz (BGG):

> „Die Beschwerde gegen einen Entscheid ist innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen.“  
> [SR_173.110_BGG_de.md Art. 100 Abs. 1]

Es gibt jedoch Ausnahmen mit verkürzten Fristen, etwa:

- **10 Tage** bei Entscheiden der kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen, bei internationaler Rechtshilfe in Strafsachen sowie bei Rückgabeentscheiden nach dem Europäischen Übereinkommen über das Sorgerecht (Art. 100 Abs. 2 BGG) [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. a–c];

- **5 Tage** bei Entscheiden der kantonalen Aufsichtsbehörden im Wechselbetreibungsbereich sowie bei Entscheiden der Kantonsregierungen über Beschwerden gegen eidgenössische Abstimmungen (Art. 100 Abs. 3 BGG) [SR_173.110_BGG_de.md Art. 100 Abs. 3 lit. a–b];

- **3 Tage** bei Entscheiden der Kantonsregierungen über Beschwerden gegen Nationalratswahlen (Art. 100 Abs. 4 BGG) [SR_173.110_BGG_de.md Art. 100 Abs. 4].

Für Revisionsgesuche gilt eine generelle Frist von **90 Tagen**, je nach Grund (Art. 124 BGG) [SR_173.110_BGG_de.md Art. 124].

### or-probezeit — fixed-vector

**Reference:** Als Probezeit gilt grundsätzlich der erste Monat des Arbeitsverhältnisses. Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann davon abgewichen werden; die Probezeit darf jedoch höchstens drei Monate dauern. Während der Probezeit gilt eine Kündigungsfrist von sieben Tagen [SR_220_OR_de.md Art. 335b].

**Generated:** Die Probezeit im Arbeitsverhältnis beträgt gemäß **Art. 335c Abs. 1 OR** grundsätzlich **einen Monat**, nämlich der erste Monat eines Arbeitsverhältnisses [SR_220_OR_de.md Art. 335c al. 1].

Abweichende Vereinbarungen sind zulässig, sofern sie schriftlich getroffen werden (z. B. durch Normalarbeitsvertrag oder Gesamtarbeitsvertrag); die Probezeit darf jedoch **höchstens drei Monate** betragen [SR_220_OR_de.md Art. 335c al. 2].

Zudem gilt:  
- Bei einer Verkürzung der Probezeit infolge Krankheit, Unfall oder Erfüllung einer nicht freiwillig übernommenen gesetzlichen Pflicht erfolgt eine entsprechende Verlängerung [SR_220_OR_de.md Art. 335c al. 3].  

Für **Lehrverhältnisse** ist gemäß **Art. 344a Abs. 3 OR** die Probezeit mit **mindestens einem und höchstens drei Monaten** festzulegen; fehlt eine Vereinbarung, gilt automatisch eine Probezeit von **drei Monaten** [SR_220_OR_de.md Art. 344a al. 3].

### or-probezeit — semantic-vector

**Reference:** Als Probezeit gilt grundsätzlich der erste Monat des Arbeitsverhältnisses. Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann davon abgewichen werden; die Probezeit darf jedoch höchstens drei Monate dauern. Während der Probezeit gilt eine Kündigungsfrist von sieben Tagen [SR_220_OR_de.md Art. 335b].

**Generated:** Die Dauer der Probezeit im Arbeitsverhältnis richtet sich nach dem jeweiligen Vertrags Typ und kann wie folgt festgelegt werden:

1. **Im gewöhnlichen Arbeitsverhältnis** gilt gemäss Art. 335b Abs. 1 SR 220 OR:  
   > *„Der erste Monat eines Arbeitsverhältnisses“* gilt als Probezeit.  
   Die Probezeit beträgt also **grundsätzlich einen Monat**. Sie darf jedoch gemäss Abs. 2 durch schriftliche Vereinbarung (Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag) **auf höchstens drei Monate verlängert** werden [SR_220_OR_de.md Art. 335b].

2. **Im Lehrvertrag** gilt gemäss Art. 344a Abs. 3 SR 220 OR:  
   > *„Die Probezeit darf nicht weniger als einen Monat und nicht mehr als drei Monate betragen.“*  
   Fehlt eine Vereinbarung, gilt eine Probezeit von **drei Monaten** [SR_220_OR_de.md Art. 344a].

3. **Im Heimarbeitnehmerverhältnis** gemäss Art. 354 Abs. 1 SR 220 OR:  
   > *„Das Arbeitsverhältnis zur Probe auf bestimmte Zeit eingegangen, sofern nichts anderes verabredet ist.“*  
   Hier ist die Probezeit nicht pauschal bezeichnet, sondern richtet sich nach der konkreten Vereinbarung; bei Nichtfestlegung ergibt sich die Dauer aus dem Verwendungszusammenhang (z. B. Dauer der Probearbeit).

Zusätzlich ist zu beachten:  
- Bei vorübergehender Verhinderung des Arbeitnehmers (z. B. Krankheit, Unfall) wird die Probezeit gemäss Art. 335b Abs. 3 SR 220 OR entsprechend verlängert [SR_220_OR_de.md Art. 335b].

**Zusammenfassung:**  
Im regulären Arbeitsverhältnis beträgt die Probezeit **grundsätzlich einen Monat**, kann aber **auf bis zu drei Monate verlängert** werden. Im Lehrverhältnis beträgt sie mindestens einen und höchstens drei Monate (Standard: drei Monate). Bei Heimarbeitnehmern richtet sich die Dauer nach Vereinbarung.

### or-probezeit — rerank

**Reference:** Als Probezeit gilt grundsätzlich der erste Monat des Arbeitsverhältnisses. Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann davon abgewichen werden; die Probezeit darf jedoch höchstens drei Monate dauern. Während der Probezeit gilt eine Kündigungsfrist von sieben Tagen [SR_220_OR_de.md Art. 335b].

**Generated:** Die Dauer der Probezeit im Arbeitsverhältnis richtet sich nach Art. 335b des Schweizerischen Obligationenrechts (OR):

- **Standardprobezeit**: Der erste Monat eines Arbeitsverhältnisses gilt als Probezeit [SR_220_OR_de.md Art. 335b Abs. 1].  
- **Maximaldauer**: Durch schriftliche Vereinbarung (z. B. Normalarbeitsvertrag oder Gesamtarbeitsvertrag) kann die Probezeit auf **höchstens drei Monate** verlängert werden [SR_220_OR_de.md Art. 335b Abs. 2].  
- **Verlängerung infolge von Hindernissen**: Bei einer effektiven Verkürzung der Probezeit infolge Krankheit, Unfall oder Erfüllung einer nicht freiwillig übernommenen gesetzlichen Pflicht erfolgt eine entsprechende Verlängerung [SR_220_OR_de.md Art. 335b Abs. 3].

**Zusammenfassung**: Die normale Probezeit beträgt **einen Monat**, kann aber vertraglich auf **bis zu drei Monate** verlängert werden — und bei besonderen Umständen (z. B. Krankheit) entsprechend weiter verlängert.

### or-probezeit — graph

**Reference:** Als Probezeit gilt grundsätzlich der erste Monat des Arbeitsverhältnisses. Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann davon abgewichen werden; die Probezeit darf jedoch höchstens drei Monate dauern. Während der Probezeit gilt eine Kündigungsfrist von sieben Tagen [SR_220_OR_de.md Art. 335b].

**Generated:** Die Probezeit im Arbeitsverhältnis beträgt **grundsätzlich den ersten Monat** [SR_220_OR_de.md Art. 335b Abs. 1].  

Durch schriftliche Vereinbarung (Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag) kann sie **auf maximal drei Monate verlängert** werden; eine Verlängerung darüber hinaus ist nicht zulässig [SR_220_OR_de.md Art. 335b Abs. 2].  

Ist im Lehrvertrag keine Probezeit festgelegt, gilt eine Probezeit von **drei Monaten** [SR_220_OR_de.md Art. 344a Abs. 3].  

Bei Verkürzung der Probezeit infolge Krankheit, Unfall oder Erfüllung einer nicht freiwillig übernommenen gesetzlichen Pflicht erfolgt eine **entsprechende Verlängerung** [SR_220_OR_de.md Art. 335b Abs. 3].

### dsg-einwilligung-widerruf — fixed-vector

**Reference:** Das DSG formuliert in den vorliegenden Artikeln kein eigenständiges allgemeines Widerrufsrecht. Es verlangt aber eine freiwillige und informierte Einwilligung [SR_235.1_DSG_de.md Art. 6], behandelt eine Bearbeitung entgegen der ausdrücklichen Willenserklärung als Persönlichkeitsverletzung [SR_235.1_DSG_de.md Art. 30] und nennt die Einwilligung nur als einen möglichen Rechtfertigungsgrund [SR_235.1_DSG_de.md Art. 31]. Wird sie für die Zukunft widerrufen, kann die Bearbeitung daher nicht mehr auf diese Einwilligung gestützt werden; ein anderer Rechtfertigungsgrund kann sie dennoch erlauben. Betroffene können insbesondere das Verbot einer Bearbeitung sowie gegebenenfalls Löschung oder Vernichtung verlangen [SR_235.1_DSG_de.md Art. 32].

**Generated:** Ja, Sie können eine Einwilligung zur Datenbearbeitung widerrufen.

Das Datenschutzgesetz (DSG) sieht ausdrücklich die Möglichkeit des Widerrufs der Einwilligung vor. Obwohl der konkrete Widerruf nicht direkt in den gegebenen Fragmenten steht, folgt dies aus Art. 7 Abs. 6 DSG, wonach die Einwilligung „nur gültig ist, wenn sie … freiwillig erteilt wird“ [SR_235.1_DSG_de.md Art. 7 Abs. 6]. Eine widerrufliche Einwilligung ist zudem implizit in Art. 32 Abs. 1 DSG belegt, wonach die betroffene Person Anspruch auf Berichtigung, Löschung oder Vernichtung personenbezogener Daten hat, sofern keine gesetzlichen Hinderungsgründe vorliegen — ein Widerruf der Einwilligung stellt einen solchen Grund dar, wenn die Bearbeitung ausschliesslich auf dieser Einwilligung beruht.

Zusätzlich unterstreicht Art. 7 Abs. 7 DSG, dass die Einwilligung „ausdrücklich“ erfolgen muss für bestimmte sensible oder risikoreiche Bearbeitungen (z. B. besonders schützenswerte Daten oder Profiling), was impliziert, dass sie auch ausdrücklich widerrufen werden kann [SR_235.1_DSG_de.md Art. 7 Abs. 7].

Zusammenfassend: Eine Einwilligung ist grundsätzlich widerruflich (vgl. Art. 7 Abs. 6 DSG i.V.m. Art. 32 DSG), sofern nicht eine andere gesetzliche Grundlage für die Bearbeitung zugrunde liegt (z. B. gesetzliche Verpflichtung, vertragliche Notwendigkeit oder überwiegendes öffentliches oder privates Interesse gem. Art. 4 Abs. 2 DSG).

### dsg-einwilligung-widerruf — semantic-vector

**Reference:** Das DSG formuliert in den vorliegenden Artikeln kein eigenständiges allgemeines Widerrufsrecht. Es verlangt aber eine freiwillige und informierte Einwilligung [SR_235.1_DSG_de.md Art. 6], behandelt eine Bearbeitung entgegen der ausdrücklichen Willenserklärung als Persönlichkeitsverletzung [SR_235.1_DSG_de.md Art. 30] und nennt die Einwilligung nur als einen möglichen Rechtfertigungsgrund [SR_235.1_DSG_de.md Art. 31]. Wird sie für die Zukunft widerrufen, kann die Bearbeitung daher nicht mehr auf diese Einwilligung gestützt werden; ein anderer Rechtfertigungsgrund kann sie dennoch erlauben. Betroffene können insbesondere das Verbot einer Bearbeitung sowie gegebenenfalls Löschung oder Vernichtung verlangen [SR_235.1_DSG_de.md Art. 32].

**Generated:** Ja, eine Einwilligung zur Datenbearbeitung kann widerrufen werden.  

Laut [SR_235.1_DSG_de.md Art. 15 Abs. 6] ist die Einwilligung „nur gültig, wenn sie … freiwillig erteilt wird“, was impliziert, dass sie jederzeit widerrufbar ist – ein Widerruf steht im Einklang mit dem freiwilligen Charakter. Zudem bestimmt [SR_235.1_DSG_de.md Art. 41 Abs. 1 lit. b] ausdrücklich, dass die betroffene Person verlangen kann, dass das Bundesorgan „die Folgen einer widerrechtlichen Bearbeitung beseitigt“, was bei Widerruf der Einwilligung notwendig ist, sofern die Bearbeitung ohne diese unrechtmässig wird.

Zusätzlich regelt [SR_235.1_DSG_de.md Art. 41 Abs. 2 lit. a] die Möglichkeit, dass die betroffene Person verlangen kann, „die betreffenden Personendaten berichtigt, löscht oder vernichtet“ zu sehen – ein Widerruf der Einwilligung kann z. B. zur Pflicht zur Löschung führen, soweit keine weiteren rechtmässigen Verarbeitungsgrundlagen bestehen.

Hinweis: Der Widerruf wirkt nur für die Zukunft ([SR_235.1_DSG_de.md Art. 15 Abs. 7] impliziert dies ausdrücklich für die Gültigkeit der Einwilligung), und die Rechtmässigkeit der vor dem Widerruf erfolgten Verarbeitung bleibt unberührt.

### dsg-einwilligung-widerruf — rerank

**Reference:** Das DSG formuliert in den vorliegenden Artikeln kein eigenständiges allgemeines Widerrufsrecht. Es verlangt aber eine freiwillige und informierte Einwilligung [SR_235.1_DSG_de.md Art. 6], behandelt eine Bearbeitung entgegen der ausdrücklichen Willenserklärung als Persönlichkeitsverletzung [SR_235.1_DSG_de.md Art. 30] und nennt die Einwilligung nur als einen möglichen Rechtfertigungsgrund [SR_235.1_DSG_de.md Art. 31]. Wird sie für die Zukunft widerrufen, kann die Bearbeitung daher nicht mehr auf diese Einwilligung gestützt werden; ein anderer Rechtfertigungsgrund kann sie dennoch erlauben. Betroffene können insbesondere das Verbot einer Bearbeitung sowie gegebenenfalls Löschung oder Vernichtung verlangen [SR_235.1_DSG_de.md Art. 32].

**Generated:** Ja, eine Einwilligung zur Datenbearbeitung kann widerrufen werden.  

Gemäss § 6 des Kontextes (SR_235.1_DSG_de.md::15) ist die Einwilligung „nur gültig, wenn sie für eine oder mehrere bestimmte Bearbeitungen nach angemessener Information freiwillig erteilt wird.“ Dies impliziert, dass sie auch jederzeit widerrufbar ist – ein Prinzip, das sich auch aus der allgemeinen Rechtsprechung und der Rechtsdoktrin zur Einwilligung ergibt, obwohl hier nicht explizit der Widerruf genannt ist.

Darüber hinaus enthält der Kontext im Bereich des Vertragsrechts (SR_220_OR_de.md::54) eine vergleichbare Vorschrift: Der Kunde kann seinen Antrag zum Vertragsabschluss oder seine Annahmeerklärung widerrufen, wenn das Angebot unter bestimmten, genannten Bedingungen gemacht wurde. Obwohl dies direkt den Vertragsabschluss betrifft, unterstreicht es den allgemeinen Grundsatz der Widerrufbarkeit von Willenserklärungen unter bestimmten Voraussetzungen.

Zusätzlich wird im Datenschutzrecht (SR_235.1_DSG_de.md) deutlich, dass die Einwilligung ein Rechtfertigungsgrund für eine Datenbearbeitung ist (Art. 31 DSG, SR_235.1_DSG_de.md::69). Da Einwilligung ein willkürlicher Rechtfertigungsgrund ist, ist ihre Rücknahme grundsätzlich möglich – dies folgt aus dem Rechtsprinzip, dass ein Recht, das freiwillig eingeräumt wurde, auch freiwillig wieder entzogen werden kann, es sei denn, gesetzliche Beschränkungen bestehen (vgl. Art. 31 Abs. 1 DSG).

Somit lässt sich aus dem Kontext ableiten, dass die Einwilligung widerrufbar ist, vorausgesetzt, der Widerruf erfolgt wirksam (z. B. in geeigneter Form und bis zur vollzogenen Bearbeitung).

### dsg-einwilligung-widerruf — graph

**Reference:** Das DSG formuliert in den vorliegenden Artikeln kein eigenständiges allgemeines Widerrufsrecht. Es verlangt aber eine freiwillige und informierte Einwilligung [SR_235.1_DSG_de.md Art. 6], behandelt eine Bearbeitung entgegen der ausdrücklichen Willenserklärung als Persönlichkeitsverletzung [SR_235.1_DSG_de.md Art. 30] und nennt die Einwilligung nur als einen möglichen Rechtfertigungsgrund [SR_235.1_DSG_de.md Art. 31]. Wird sie für die Zukunft widerrufen, kann die Bearbeitung daher nicht mehr auf diese Einwilligung gestützt werden; ein anderer Rechtfertigungsgrund kann sie dennoch erlauben. Betroffene können insbesondere das Verbot einer Bearbeitung sowie gegebenenfalls Löschung oder Vernichtung verlangen [SR_235.1_DSG_de.md Art. 32].

**Generated:** Ja, eine Einwilligung zur Datenbearbeitung kann widerrufen werden.  

Gemäss Art. 13 DSG (Datenschutzgesetz) ist die Einwilligung freiwillig und kann daher grundsätzlich widerrufen werden – der Widerruf ist however nur wirksam für die Zukunft:  

**[SR_235.1_DSG_de.md Art. 13]**  
*„Die Einwilligung kann jederzeit mit Wirkung für die Zukunft widerrufen werden. Der Widerruf berührt nicht die Rechtsmässigkeit der Datenbearbeitung bis zum Zeitpunkt des Widerrufs.“*  

Der Widerruf wirkt also rückwirkungslos; bereits rechtswidrig erfolgte Bearbeitungen vor dem Widerruf bleiben unberührt, zukünftige Bearbeitungen müssen eingestellt werden, sofern keine andere Rechtsgrundlage (z. B. gesetzliche Verpflichtung, berechtigtes Interesse) vorliegt.

### or-artikel-1 — fixed-vector

**Reference:** Zum Abschluss eines Vertrags ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich. Diese Willensäusserung kann ausdrücklich oder stillschweigend erfolgen [SR_220_OR_de.md Art. 1].

**Generated:** Artikel 1 des Obligationenrechts (OR) lautet:

**Art. 1**  
1. Zum Abschlusse eines Vertrages ist die übereinstimmende gegen seitige Willensäusserung der Parteien erforderlich.  
2. Sie kann eine ausdrückliche oder stillschweigende sein.  

[SR_220_OR_de.md Art. 1]

### or-artikel-1 — semantic-vector

**Reference:** Zum Abschluss eines Vertrags ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich. Diese Willensäusserung kann ausdrücklich oder stillschweigend erfolgen [SR_220_OR_de.md Art. 1].

**Generated:** Im vorliegenden Kontext wird **Artikel 1 des OR (Obligationenrechts)** nicht zitiert oder genannt. Weder in den genannten Abschnitten noch in den anderen Quellen wird der Inhalt von Art. 1 OR wiedergegeben.

Da keine direkte Quellenangabe zu Art. 1 OR vorliegt, kann die Frage **nicht beantwortet** werden.

### or-artikel-1 — rerank

**Reference:** Zum Abschluss eines Vertrags ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich. Diese Willensäusserung kann ausdrücklich oder stillschweigend erfolgen [SR_220_OR_de.md Art. 1].

**Generated:** Im bereitgestellten Kontext ist **keine Information über Artikel 1 des OR (Organisationsgesetz)** enthalten. Weder der vollständige Wortlaut von Art. 1 OR noch eine Aussage dazu ist auffindbar.

Die genannten Quellen enthalten Auszüge zu folgenden Artikeln:
- Art. 58 und 59 OR (in Bezug auf die UeB OR),
- Art. 600 Abs. 3 OR (in Bezug auf die ZPO),
- Art. 731b, 819, 908 OR (in Bezug auf Massnahmen bei Gesellschaftsmängeln),
- Art. 697b ff., 699, 805, 881 OR (in Bezug auf Untersuchungs- und Einberufungsbefugnisse),
- Art. 229 ff., 230 ff. StGB (vorsätzliche Gefährdungshandlungen), sowie
- Art. 260 bis ff. StGB (Terrorismusbeziehungen).

Für die **Inhaltsangabe von Art. 1 OR** wäre die Ausfertigung des Gesetzeswerks selbst erforderlich – diese liegt nicht vor.

👉 **Antwort:** Aus dem vorliegenden Kontext ist nicht ersichtlich, was in Artikel 1 des OR steht.

### or-artikel-1 — graph

**Reference:** Zum Abschluss eines Vertrags ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich. Diese Willensäusserung kann ausdrücklich oder stillschweigend erfolgen [SR_220_OR_de.md Art. 1].

**Generated:** Artikel 1 des Schweizerischen Obligationenrechts (OR) lautet:

**Art. 1**  
1. Zum Abschlusse eines Vertrages ist die übereinstimmende gegen seitige Willensäusserung der Parteien erforderlich.  
2. Sie kann eine ausdrückliche oder stillschweigende sein.  

[SR_220_OR_de.md Art. 1]
