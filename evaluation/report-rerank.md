# RAG evaluation

- Methods: **fixed-vector, semantic-vector, rerank**
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
| or-kaufvertrag-verjaehrung | fixed-vector | 100% | 100% | 100% | 1.00 | 100% | 1,198 | 1,284 |
| or-kaufvertrag-verjaehrung | semantic-vector | 100% | 0% | 0% | 0.00 | 33% | 726 | 810 |
| or-kaufvertrag-verjaehrung | rerank | 100% | 100% | 100% | 1.00 | 100% | 617 | 702 |
| bgg-beschwerdefrist | fixed-vector | 100% | 100% | 100% | 0.33 | 100% | 1,200 | 1,296 |
| bgg-beschwerdefrist | semantic-vector | 100% | 100% | 100% | 0.50 | 100% | 742 | 842 |
| bgg-beschwerdefrist | rerank | 100% | 100% | 100% | 1.00 | 100% | 774 | 872 |
| or-probezeit | fixed-vector | 100% | 0% | 0% | 0.00 | 67% | 1,200 | 1,288 |
| or-probezeit | semantic-vector | 100% | 100% | 100% | 1.00 | 67% | 813 | 901 |
| or-probezeit | rerank | 100% | 100% | 100% | 1.00 | 67% | 890 | 980 |
| dsg-einwilligung-widerruf | fixed-vector | 100% | 100% | 25% | 0.25 | 75% | 1,198 | 1,292 |
| dsg-einwilligung-widerruf | semantic-vector | 100% | 0% | 0% | 0.00 | 75% | 941 | 1,032 |
| dsg-einwilligung-widerruf | rerank | 100% | 100% | 25% | 0.05 | 75% | 925 | 1,015 |
| or-artikel-1 | fixed-vector | 100% | 100% | 100% | 1.00 | 80% | 1,198 | 1,291 |
| or-artikel-1 | semantic-vector | 100% | 0% | 0% | 0.00 | 0% | 745 | 834 |
| or-artikel-1 | rerank | 100% | 0% | 0% | 0.00 | 0% | 888 | 980 |

## Answers

| Question | Method | Fact coverage | Expected-citation precision | Citation grounding | Citation completeness | Answer tokens |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| or-kuendigung-krankheit | fixed-vector | 0% | 0% | 50% | 0% | 592 |
| or-kuendigung-krankheit | semantic-vector | 0% | 0% | 100% | 0% | 508 |
| or-kuendigung-krankheit | rerank | 67% | 50% | 100% | 100% | 338 |
| or-kaufvertrag-verjaehrung | fixed-vector | 100% | 50% | 100% | 100% | 293 |
| or-kaufvertrag-verjaehrung | semantic-vector | 0% | 0% | 100% | 0% | 85 |
| or-kaufvertrag-verjaehrung | rerank | 50% | 100% | 100% | 100% | 488 |
| bgg-beschwerdefrist | fixed-vector | 100% | 33% | 100% | 100% | 393 |
| bgg-beschwerdefrist | semantic-vector | 67% | 50% | 100% | 100% | 356 |
| bgg-beschwerdefrist | rerank | 100% | 25% | 100% | 100% | 552 |
| or-probezeit | fixed-vector | 67% | 50% | 50% | 100% | 204 |
| or-probezeit | semantic-vector | 67% | 33% | 100% | 100% | 406 |
| or-probezeit | rerank | 67% | 50% | 100% | 100% | 366 |
| dsg-einwilligung-widerruf | fixed-vector | 0% | 0% | 0% | 0% | 148 |
| dsg-einwilligung-widerruf | semantic-vector | 0% | 0% | 50% | 0% | 204 |
| dsg-einwilligung-widerruf | rerank | 50% | 33% | 67% | 25% | 472 |
| or-artikel-1 | fixed-vector | 100% | 100% | 100% | 100% | 66 |
| or-artikel-1 | semantic-vector | 0% | 0% | 0% | 0% | 99 |
| or-artikel-1 | rerank | 0% | 0% | 0% | 0% | 202 |

## Summary

- **fixed-vector:** article recall@K 54.2%, MRR 0.43, fact coverage 61.1%, expected-citation precision 38.9%, citation grounding 66.7%, citation completeness 66.7%, average context 1,289 tokens, corpus-token savings 99.88%.
- **semantic-vector:** article recall@K 33.3%, MRR 0.25, fact coverage 22.2%, expected-citation precision 13.9%, citation grounding 75.0%, citation completeness 33.3%, average context 892 tokens, corpus-token savings 99.92%.
- **rerank:** article recall@K 70.8%, MRR 0.68, fact coverage 55.6%, expected-citation precision 43.1%, citation grounding 77.8%, citation completeness 70.8%, average context 923 tokens, corpus-token savings 99.92%.

## Strategic token perspective

All selected methods receive the same final chunk budget. Their actual token counts can differ because the retrieved chunks have different lengths.

## Answer details

### or-kuendigung-krankheit — fixed-vector

**Reference:** Nach Ablauf der Probezeit darf der Arbeitgeber bei einer unverschuldeten krankheitsbedingten vollständigen oder teilweisen Arbeitsverhinderung während der gesetzlichen Sperrfrist nicht kündigen: 30 Tage im ersten Dienstjahr, 90 Tage vom zweiten bis und mit fünften Dienstjahr und 180 Tage ab dem sechsten Dienstjahr. Eine während der Sperrfrist ausgesprochene Kündigung ist nichtig. Wurde vorher gekündigt und läuft die Kündigungsfrist in die Sperrfrist hinein, wird ihr Ablauf unterbrochen und danach fortgesetzt. Während der Probezeit gilt dieser Schutz nicht [SR_220_OR_de.md Art. 336c].

**Generated:** Ja, der Arbeitgeber darf grundsätzlich während der Krankheit kündigen — **jedoch mit wichtigen Einschränkungen**:

1. **Sperrfristen für Kündigungen**  
   Gemäss Artikel 335d des Schweizerischen Obligationenrechts (OR) gelten **Sperrfristen**, während deren eine Kündigung **nichtig** ist. Dazu zählen nach Artikel 335c Abs. 1 lit. b OR:
   > „d. während der Arbeitnehmer mit Zustimmung des Arbeitgebers an einer von der zuständigen Bundesbehörde angeordneten Dienstleistung für eine Hilfsaktion im Ausland teilnimmt.“  
   *(Anm.: Der Kontext enthält hier lediglich eine Unvollständigkeit — es fehlt die Aufzählung der konkreten Sperrfristen, z. B. für Krankheit.)*

2. **Tatsächliche Sperrfrist bei Krankheit**  
   Gemäss **Artikel 335c Abs. 1 lit. a OR** (wenngleich nicht im angegebenen Chunk enthalten, aber gängiger Bestandteil des OR):  
   > „a. während des Verhinderungsfristendienstes gemäss Artikel 328a Abs. 2 und 3“  
   → Dies bezieht sich auf die Zeit, in der der Arbeitgeber nach Artikel 328a Abs. 2 OR Pflege und ärztliche Behandlung zu gewähren hat:  
   > „Wird der Arbeitnehmer ohne sein Verschulden durch Krankheit oder Unfall an der Arbeitsleistung verhindert, so hat der Arbeitgeber Pflege und ärztliche Behandlung für eine beschränkte Zeit zu gewähren, **im ersten Dienstjahr für drei Wochen und nachher für eine angemessene längere Zeit**, je nach der Dauer des Arbeitsverhältnisses und den besonderen Umständen.“  
   [SR_220_OR_de.md Art. 328a Abs. 2]

   **Während dieser Sperrfrist (z. B. 3 Wochen im ersten Jahr)** ist eine Kündigung des Arbeitgebers **nichtig** ([SR_220_OR_de.md Art. 335c Abs. 2]).  
   > „Die Kündigung, die während einer der in Absatz 1 festgesetzten Sperrfristen erklärt wird, ist nichtig...“

3. **Außerhalb der Sperrfrist**  
   Eine Kündigung ist **zulässig**, wenn:
   - die Sperrfrist abgelaufen ist,
   - und der Arbeitgeber einen **begründeten Kündigungsgrund** vorlegen kann (z. B. dringende betriebliche Gründe, Vertrauensbruch usw.),
   - und die **ordentliche oder außerordentliche Kündigungsfrist** eingehalten wird.

**Zusammenfassung**:  
Der Arbeitgeber **darf nicht während der Sperrfrist** kündigen, die bei Krankheit nach Artikel 328a OR gilt (z. B. 3 Wochen im ersten Jahr). **Außerhalb dieser Frist** ist eine Kündigung grundsätzlich möglich, sofern die gesetzlichen Voraussetzungen erfüllt sind.

### or-kuendigung-krankheit — semantic-vector

**Reference:** Nach Ablauf der Probezeit darf der Arbeitgeber bei einer unverschuldeten krankheitsbedingten vollständigen oder teilweisen Arbeitsverhinderung während der gesetzlichen Sperrfrist nicht kündigen: 30 Tage im ersten Dienstjahr, 90 Tage vom zweiten bis und mit fünften Dienstjahr und 180 Tage ab dem sechsten Dienstjahr. Eine während der Sperrfrist ausgesprochene Kündigung ist nichtig. Wurde vorher gekündigt und läuft die Kündigungsfrist in die Sperrfrist hinein, wird ihr Ablauf unterbrochen und danach fortgesetzt. Während der Probezeit gilt dieser Schutz nicht [SR_220_OR_de.md Art. 336c].

**Generated:** Ja, der Arbeitgeber darf während der Krankheit des Arbeitnehmers **grundsätzlich kündigen**, aber unter bestimmten Einschränkungen.

Die Swiss Obligationenrecht (OR) sieht zwar keinen generellen Kündigungsverbot während Krankheit vor. Allerdings gelten folgende Regeln:

- Nach **Art. 335b Abs. 1 OR** ist während der **Probezeit** eine Kündigung mit einer Frist von **sieben Tagen** jederzeit möglich – auch während einer Krankheit [SR_220_OR_de.md Art. 335b].

- Für die **Dauer der Kündigungsfrist** gelten besondere Schutzvorschriften:
  - **Art. 336c OR** (nicht im bereitgestellten Kontext enthalten) schreibt vor, dass eine Kündigung während einer **nicht durch Verschulden des Arbeitnehmers verursachten Verhinderung** (z. B. Krankheit oder Unfall nach Art. 328a Abs. 2 OR) **unwirksam ist**, wenn sie innerhalb des **ersten Tages der Verhinderung bis zum Ende des Arbeitsverhältnisses** ausgesprochen wird – **sofern die Verhinderung mindestens 30 Tage andauert** [vgl. OR Art. 336c lit. b, nicht im angegebenen Chunk, aber bekanntes Swiss-Recht].

- Zudem ist gemäß **Art. 328a Abs. 2 OR** eine Verhinderung durch Krankheit oder Unfall **ohne Verschulden des Arbeitnehmers** vorzusehen. Der Arbeitgeber muss in diesem Fall **Pflege und ärztliche Behandlung gewähren** – dies ist aber keine kündigungsschützende Maßnahme, sondern eine Leistungspflicht [SR_220_OR_de.md Art. 328a Abs. 2].

**Fazit**:  
Die Kündigung ist **zulässig**, **es gelten aber Schutzfristen**, die eine Kündigung während einer längeren (>=30-tägigen), verschuldensfreien Krankheit unwirksam machen können (Art. 336c OR). Da **Art. 336c OR** nicht im bereitgestellten Kontext enthalten ist, lässt sich die vollständige rechtliche Lage nur unter Berücksichtigung weiterer Quellen abschließend klären.  

Aber:  
Die Frage lautet: *„Darf der Arbeitgeber während der Krankheit kündigen?“*  
→ **Ja, grundsätzlich – jedoch nicht innerhalb der gesetzlichen Kündigungsschutzfristen bei längeren, nicht eigenverschuldeten Krankheitsfällen (Art. 336c OR).**

### or-kuendigung-krankheit — rerank

**Reference:** Nach Ablauf der Probezeit darf der Arbeitgeber bei einer unverschuldeten krankheitsbedingten vollständigen oder teilweisen Arbeitsverhinderung während der gesetzlichen Sperrfrist nicht kündigen: 30 Tage im ersten Dienstjahr, 90 Tage vom zweiten bis und mit fünften Dienstjahr und 180 Tage ab dem sechsten Dienstjahr. Eine während der Sperrfrist ausgesprochene Kündigung ist nichtig. Wurde vorher gekündigt und läuft die Kündigungsfrist in die Sperrfrist hinein, wird ihr Ablauf unterbrochen und danach fortgesetzt. Während der Probezeit gilt dieser Schutz nicht [SR_220_OR_de.md Art. 336c].

**Generated:** Ja, **der Arbeitgeber darf während der Krankheit des Arbeitnehmers kündigen**, **aber mit Einschränkungen**:

- **Während der Probezeit** (erster Monat) ist eine Kündigung jederzeit mit einer Frist von **sieben Tagen** möglich, auch während einer Krankheit ([SR_220_OR_de.md Art. 335b Abs. 1](SR_220_OR_de.md Art. 335b)).

- **Nach Ablauf der Probezeit** darf der Arbeitgeber das Arbeitsverhältnis **nicht kündigen**, solange der Arbeitnehmer **ohne eigenes Verschulden durch Krankheit oder Unfall an der Arbeitsleistung verhindert** ist — und zwar:
  - im **ersten Dienstjahr** für **30 Tage**,
  - im **zweiten bis fünften Dienstjahr** für **90 Tage**,
  - ab dem **sechsten Dienstjahr** für **180 Tage** ([SR_220_OR_de.md Art. 336c Abs. 1 Buchst. b](SR_220_OR_de.md Art. 336c)).

Folglich:  
→ **Während der Probezeit**: Kündigung auch bei Krankheit möglich (mit 7-Tages-Frist).  
→ **Nach der Probezeit**: Kündigungsschutz während der oben genannten Fristen, sofern die Verhinderung **ohne eigenes Verschulden** (z. B. Krankheit, Unfall) erfolgt.

Weitere Hinweise:  
- Bei einer effektiven Verkürzung der Probezeit infolge Krankheit oder Unfall wird die Probezeit entsprechend verlängert ([SR_220_OR_de.md Art. 335b Abs. 3](SR_220_OR_de.md Art. 335b)).  
- Während dieser Schutzfrist ist eine außerordentliche Kündigung grundsätzlich unzulässig.

### or-kaufvertrag-verjaehrung — fixed-vector

**Reference:** Für Forderungen aus einem Kaufvertrag gilt grundsätzlich die allgemeine Verjährungsfrist von zehn Jahren, sofern das Bundeszivilrecht für den konkreten Anspruch keine abweichende Frist vorsieht [SR_220_OR_de.md Art. 127].

**Generated:** Forderungen aus einem Kaufvertrag verjähren nach der allgemeinen Verjährungsfrist von **zehn Jahren**, sofern das Bundeszivilrecht nichts anderes bestimmt ([SR_220_OR_de.md Art. 127]).

Allerdings gibt es für bestimmte Ansprüche aus dem Kaufvertrag speziell verkürzte Fristen:

- **Gewährleistungsansprüche wegen Mängeln der Sache** verjähren bereits **nach zwei Jahren nach deren Ablieferung an den Käufer**, selbst wenn der Käufer die Mängel erst später entdeckt, es sei denn, der Verkäufer hat eine längere Haftung übernommen ([SR_220_OR_de.md Art. 21075 Abs. 1]).

- **Ansprüche des Käufers wegen Mängeln des Grundstücks** verjähren **nach fünf Jahren nach dem Erwerb des Eigentums** ([SR_220_OR_de.md Art. 21075 Abs. 3] – korrigiert von Art. 220 OR in der Fassung vor 2013; heute gem. SR_220_OR_de.md Art. 127 i.V.m. Art. 21075, vgl. Chunk „## PDF-Seite 54“).

Zusammengefasst:
- **Allgemeine Verjährungsfrist**: 10 Jahre ([SR_220_OR_de.md Art. 127]);
- **Gewährleistungsansprüche (Sache)**: 2 Jahre ab Lieferung ([SR_220_OR_de.md Art. 21075 Abs. 1]);
- **Gewährleistungsansprüche (Grundstück)**: 5 Jahre ab Erwerb des Eigentums ([SR_220_OR_de.md Art. 21075 Abs. 3]).

### or-kaufvertrag-verjaehrung — semantic-vector

**Reference:** Für Forderungen aus einem Kaufvertrag gilt grundsätzlich die allgemeine Verjährungsfrist von zehn Jahren, sofern das Bundeszivilrecht für den konkreten Anspruch keine abweichende Frist vorsieht [SR_220_OR_de.md Art. 127].

**Generated:** Forderungen aus einem Kaufvertrag verjähren gemäss Artikel 21075 Absatz 1 des Schweizerischen Obligationenrechts (OR) **mit Ablauf von zwei Jahren nach deren Ablieferung an den Käufer**, auch wenn der Käufer die Mängel erst später entdeckt — es sei denn, der Verkäufer hat eine längere Haftungsfrist übernommen [SR_220_OR_de.md Art. 21075].

### or-kaufvertrag-verjaehrung — rerank

**Reference:** Für Forderungen aus einem Kaufvertrag gilt grundsätzlich die allgemeine Verjährungsfrist von zehn Jahren, sofern das Bundeszivilrecht für den konkreten Anspruch keine abweichende Frist vorsieht [SR_220_OR_de.md Art. 127].

**Generated:** Die Frage, wann Forderungen aus einem Kaufvertrag verjähren, ist im gegebenen Kontext **nicht direkt beantwortbar**, da keine Vorschrift speziell zur Verjährung von Forderungen aus einem allgemeinen Kaufvertrag angeführt ist.

Der Kontext enthält unter anderem:

- Allgemeine Verjährungsfristen: 10 Jahre (Art. 127 OR) und 5 Jahre (Art. 128 OR) für bestimmte Forderungen wie Mietzins, Arbeitnehmerentgelt, Handwerksarbeit etc.  
- Speziellere Fristen, z. B. für Schadenersatz bei Körperverletzung (3–20 Jahre, Art. 128a OR),  
- Für Gesellschafterforderungen (5 Jahre, Art. 591 OR),  
- Für Mängelansprüche bei Werkverträgen (2–5 Jahre, Art. 371 OR).

Die Verjährung von Forderungen aus einem **Kaufvertrag** fällt jedoch weder unter Art. 127 (Allgemeine 10-Jahresfrist), noch unter die speziell aufgeführten Fälle in Art. 128 OR, da dort ausdrücklich keine Kaufverträge genannt sind.

Gemäß der gesetzlichen Ordnung des Schweizerischen Obligationenrechts ist die **allgemeine Verjährungsfrist für Kaufvertragsforderungen**—sofern nicht anders bestimmt—zehn Jahre nach Art. 127 OR [SR_220_OR_de.md Art. 127].  
Für Mängelansprüche des Käufers gilt jedoch eine spezielle, kürzere Frist von **zwei Jahren nach Abnahme** (Art. 128 OR Abs. 2 lit. c, i.V.m. Art. 197 I OR i.V.m. Art. 197 III OR – letzteres nicht im gegebenen Kontext enthalten, aber in der Gesetzesdurchführung bekannt).  
Zudem gibt es eine **Verlängerung auf fünf Jahre**, wenn der Käufer vorsätzlich getäuscht wurde (Art. 197 III OR – nicht im Kontext enthalten).

Da die spezifische Rechtslage zu Kaufverträgen nicht vollständig im bereitgestellten Kontext abgebildet ist, lässt sich die Frage **nicht abschließend** anhand des gegebenen Textes beantworten.  

**Antwort:**  
Der gegebene Kontext enthält keine explizite Regelung zur Verjährung von Forderungen aus einem Kaufvertrag. Es ist daher nicht möglich, den genauen Verjährungszeitraum allein anhand dieses Textes zu bestimmen.

### bgg-beschwerdefrist — fixed-vector

**Reference:** Grundsätzlich ist die Beschwerde gegen einen Entscheid innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen. Artikel 100 BGG sieht für bestimmte Fälle kürzere Fristen von zehn, fünf oder drei Tagen vor; gegen das unrechtmässige Verweigern oder Verzögern eines Entscheids kann jederzeit Beschwerde geführt werden [SR_173.110_BGG_de.md Art. 100].

**Generated:** Die Frist für eine Beschwerde ans Bundesgericht beträgt **30 Tage**, und zwar nach der Eröffnung der vollständigen Ausfertigung des Entscheids (sofern nicht gesonderte, kürzere Fristen gelten). Dies gilt insbesondere für Beschwerden gegen Entscheide der Vorinstanz, wie aus Artikel 100 des Bundesgerichtsgesetzes (BGG) hervorgeht:

> **Art. 100 Beschwerde gegen Entscheide**  
> 1 Die Beschwerde gegen einen Entscheid ist innert **30 Tagen** nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen [SR_173.110_BGG_de.md Art. 100].

Zusätzlich ist zu beachten:

- Bei bestimmten Entscheiden (z. B. Entscheiden der kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen) beträgt die Frist **10 Tage** (Art. 100 Abs. 2 BGG) [SR_173.110_BGG_de.md Art. 100 Abs. 2].
- Bei Entscheiden im Asylverfahren im beschleunigten Verfahren beträgt die Frist **sieben Arbeitstage** (Art. 108 Abs. 1 AsylG) [SR_142.31_AsylG_de.md Art. 108 Abs. 1].

Im Zivilrecht richtet sich die Frist nach der ZPO: Für die Beschwerde gegen erstinstanzliche Entscheide oder prozessleitende Verfügungen beträgt die Frist gemäss Art. 321 Abs. 2 ZPO grundsätzlich **10 Tage**, es sei denn, das Gesetz sieht etwas anderes vor [SR_272_ZPO_de.md Art. 321 Abs. 2].

Zusammengefasst gilt also:  
➡️ **Allgemeine Frist: 30 Tage** (BGG, ZPO bei entscheidsgemässen Entscheiden),  
➡️ **Besondere, kürzere Fristen** (10, 5, 3, oder 7 Tage) für spezifische Entscheide, wie gesetzlich vorgesehen.

Detaillierte Angaben zu den Ausnahmen finden sich in den genannten Gesetzesstellen.

### bgg-beschwerdefrist — semantic-vector

**Reference:** Grundsätzlich ist die Beschwerde gegen einen Entscheid innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen. Artikel 100 BGG sieht für bestimmte Fälle kürzere Fristen von zehn, fünf oder drei Tagen vor; gegen das unrechtmässige Verweigern oder Verzögern eines Entscheids kann jederzeit Beschwerde geführt werden [SR_173.110_BGG_de.md Art. 100].

**Generated:** Für eine Beschwerde ans Bundesgericht gilt allgemein eine Frist von **30 Tagen** nach der Eröffnung der vollständigen Ausfertigung des Entscheids, sofern nicht eine kürzere oder abweichende Frist gesetzlich vorgesehen ist.

Konkret regelt **Artikel 100 Absatz 1 BGG**:

> *„Die Beschwerde gegen einen Entscheid ist innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen.“*  
> [SR_173.110_BGG_de.md Art. 100 Abs. 1]

Es existieren jedoch diverse Ausnahmen mit kürzeren Fristen, etwa:

- **10 Tage** bei Entscheiden der kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen (Art. 100 Abs. 2 lit. a BGG) [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. a]  
- **5 Tage** bei Entscheiden der kantonalen Aufsichtsbehörden im Rahmen der Wechselbetreibung sowie bei Entscheiden der Kantonsregierungen über Beschwerden gegen eidgenössische Abstimmungen (Art. 100 Abs. 3 lit. a BGG) [SR_173.110_BGG_de.md Art. 100 Abs. 3 lit. a]  
- **3 Tage** bei Entscheiden der Kantonsregierungen über Beschwerden gegen die Nationalratswahlen (Art. 100 Abs. 4 BGG) [SR_173.110_BGG_de.md Art. 100 Abs. 4]

Außerdem gelten in bestimmten Verfahren (z. B. Asylverfahren) eigene Fristen (vgl. Art. 108 AsylG) [SR_142.31_AsylG_de.md Art. 108].

Zusammenfassend: **Die Standard-Beschwerdefrist beim Bundesgericht beträgt 30 Tage**, es sei denn, das Gesetz sieht eine abweichende Frist ausdrücklich vor.

### bgg-beschwerdefrist — rerank

**Reference:** Grundsätzlich ist die Beschwerde gegen einen Entscheid innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen. Artikel 100 BGG sieht für bestimmte Fälle kürzere Fristen von zehn, fünf oder drei Tagen vor; gegen das unrechtmässige Verweigern oder Verzögern eines Entscheids kann jederzeit Beschwerde geführt werden [SR_173.110_BGG_de.md Art. 100].

**Generated:** Die allgemeine Frist für eine Beschwerde ans Bundesgericht beträgt **30 Tage**, und zwar **nach der Eröffnung der vollständigen Ausfertigung des Entscheids** [SR_173.110_BGG_de.md Art. 100 Abs. 1].

Allerdings gelten für bestimmte Entscheide kürzere Fristen:

- **10 Tage** bei:
  - Entscheiden der kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. a];
  - Entscheiden in der internationalen Rechtshilfe in Strafsachen und der internationalen Amtshilfe in Steuersachen [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. b];
  - Entscheiden über die Rückgabe eines Kindes nach dem Europäischen Übereinkommen vom 20. Mai 1980 (Haager Kindesentführungsübereinkommen) [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. c];
  - Entscheiden des Bundespatentgerichts über die Erteilung einer Lizenz nach Art. 40d des Patentgesetzes [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. d].

- **5 Tage** bei:
  - Entscheiden der kantonalen Aufsichtsbehörden im Rahmen der Wechselbetreibung [SR_173.110_BGG_de.md Art. 100 Abs. 3 lit. a];
  - Entscheiden der Kantonsregierungen über Beschwerden gegen eidgenössische Abstimmungen [SR_173.110_BGG_de.md Art. 100 Abs. 3 lit. b].

- **3 Tage** bei Entscheiden der Kantonsregierungen über Beschwerden gegen die Nationalratswahlen [SR_173.110_BGG_de.md Art. 100 Abs. 4].

Zusätzlich gilt für Beschwerden gegen **Erlasse** eine Frist von **30 Tagen nach der nach kantonalem Recht massgebenden Veröffentlichung** [SR_173.110_BGG_de.md Art. 101].

Weiterhin gilt für **Revisionsgesuche** eine Frist von **30 Tagen** nach Eröffnung der vollständigen Ausfertigung des Entscheids (bei Verletzung von Verfahrensvorschriften) [SR_173.110_BGG_de.md Art. 124 Abs. 1 lit. b], sowie **90 Tage** bei anderen Gründen [SR_173.110_BGG_de.md Art. 124 Abs. 1 lit. c, d].

Im Rahmen des **Verwaltungsrechtsschutzes (ATSG)** beträgt die Beschwerdefrist ebenfalls **30 Tage nach der Eröffnung des Einspracheentscheids** [SR_830.1_ATSG_de.md Art. 60 Abs. 1].

**Zusammenfassend:** Die **allgemeine Frist** laut Bundesgerichtsgesetz beträgt **30 Tage**, es bestehen jedoch diverse ** Ausnahmen mit kürzeren Fristen** (10, 5 oder 3 Tage), je nach Entscheidungsart.

### or-probezeit — fixed-vector

**Reference:** Als Probezeit gilt grundsätzlich der erste Monat des Arbeitsverhältnisses. Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann davon abgewichen werden; die Probezeit darf jedoch höchstens drei Monate dauern. Während der Probezeit gilt eine Kündigungsfrist von sieben Tagen [SR_220_OR_de.md Art. 335b].

**Generated:** Die Probezeit im Arbeitsverhältnis beträgt gemäß § 335b Abs. 1 des Schweizerischen Obligationenrechts standardmäßig **einen Monat**, nämlich „der erste Monat eines Arbeitsverhältnisses“ [SR_220_OR_de.md Art. 335b].  

Gemäß Abs. 2 kann sie durch schriftliche Vereinbarung (z. B. Normalarbeitsvertrag oder Gesamtarbeitsvertrag) **höchstens auf drei Monate verlängert** werden [SR_220_OR_de.md Art. 335b Abs. 2].  

Im **Lehrvertrag** beträgt die Probezeit gemäß § 344a Abs. 3 mindestens einen Monat und höchstens drei Monate; fehlt eine Vereinbarung, gilt automatisch eine Probezeit von drei Monaten [SR_220_OR_de.md Art. 344a Abs. 3].  

Weiter ist festzuhalten, dass die Probezeit bei Unterbrechungen (z. B. Krankheit, Unfall, gesetzliche Pflichten) entsprechend verlängert wird [SR_220_OR_de.md Art. 335b Abs. 3].

### or-probezeit — semantic-vector

**Reference:** Als Probezeit gilt grundsätzlich der erste Monat des Arbeitsverhältnisses. Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann davon abgewichen werden; die Probezeit darf jedoch höchstens drei Monate dauern. Während der Probezeit gilt eine Kündigungsfrist von sieben Tagen [SR_220_OR_de.md Art. 335b].

**Generated:** Die Dauer der Probezeit im Arbeitsverhältnis hängt vom konkreten Vertragstyp und den getroffenen Vereinbarungen ab:

1. **Im normalem Arbeitsverhältnis** gilt laut Art. 335b Abs. 1 und 2 SR_220_OR_de.md:  
   - Der **erste Monat** des Arbeitsverhältnisses gilt als Probezeit.  
   - Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann die Probezeit **auf höchstens drei Monate verlängert** werden ([SR_220_OR_de.md Art. 335b Abs. 2](SR_220_OR_de.md::630)).

2. **Im Lehrvertrag** gilt laut Art. 344a Abs. 3 SR_220_OR_de.md:  
   - Die Probezeit darf **nicht weniger als einen Monat und nicht mehr als drei Monate** betragen.  
   - Ohne ausdrückliche Vereinbarung gilt eine Probezeit von **drei Monaten** ([SR_220_OR_de.md Art. 344a Abs. 3](SR_220_OR_de.md::691)).

3. **Im Heimarbeitnehmerverhältnis** gem. Art. 354 Abs. 1 SR_220_OR_de.md gilt:  
   - Wenn dem Heimarbeitnehmer eine Probearbeit übergeben wird, gilt das Arbeitsverhältnis **zur Probe auf bestimmte Zeit**, sofern nicht anders vereinbart ([SR_220_OR_de.md Art. 354 Abs. 1](SR_220_OR_de.md::731)).  
   - Die konkrete Dauer ist nicht gesetzlich festgelegt; sie richtet sich nach der jeweiligen Vereinbarung.

Zusätzlich kann die Probezeit bei Krankheit, Unfall oder Erfüllung einer gesetzlichen Pflicht infolge von Dienstverhinderung entsprechend verlängert werden (Art. 335b Abs. 3 SR_220_OR_de.md) ([SR_220_OR_de.md Art. 335b Abs. 3](SR_220_OR_de.md::630)).

**Zusammenfassung:**  
- Mindestens **einen Monat**,  
- maximal **drei Monate**,  
- bei Lehrverträgen standardmäßig **drei Monate**, sofern nichts anderes vereinbart wird.

### or-probezeit — rerank

**Reference:** Als Probezeit gilt grundsätzlich der erste Monat des Arbeitsverhältnisses. Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann davon abgewichen werden; die Probezeit darf jedoch höchstens drei Monate dauern. Während der Probezeit gilt eine Kündigungsfrist von sieben Tagen [SR_220_OR_de.md Art. 335b].

**Generated:** Die Dauer der Probezeit im Arbeitsverhältnis richtet sich nach dem Ordentlichen Recht des schweizerischen Obligationenrechts (SR 220 OR):

- **Standardprobezeit**: Der erste Monat eines Arbeitsverhältnisses gilt als Probezeit [SR_220_OR_de.md Art. 335b Abs. 1].  
- **Maximaldauer**: Die Probezeit darf per schriftlicher Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag **höchstens auf drei Monate** verlängert werden [SR_220_OR_de.md Art. 335b Abs. 2].  
- **Verkürzung und Verlängerung bei Unterbrüchen**: Bei Krankheit, Unfall oder Erfüllung einer nicht freiwillig übernommenen gesetzlichen Pflicht während der Probezeit wird die Probezeit entsprechend verlängert [SR_220_OR_de.md Art. 335b Abs. 3].

Zusätzlich gilt für **Lehrverhältnisse** (ausnahmsweise gesondert geregelt):
- Die Probezeit darf **nicht weniger als einen Monat und nicht mehr als drei Monate** betragen; fehlt eine Vereinbarung, gelten drei Monate [SR_220_OR_de.md Art. 344a Abs. 3].
- Eine Verlängerung bis zu **sechs Monaten** ist ausnahmsweise möglich – aber nur mit Zustimmung der kantonalen Behörde und vor Ablauf der ursprünglichen Probezeit [SR_220_OR_de.md Art. 344a Abs. 4].

**Zusammenfassung**:  
Im ordentlichen Arbeitsverhältnis beträgt die Probezeit standardmäßig **einen Monat**, kann aber vertraglich bis zu **drei Monaten** verlängert werden. Für Auszubildende gilt analog eine maximale Dauer von drei Monaten (bzw. bis zu sechs Monaten mit behördlicher Genehmigung).

### dsg-einwilligung-widerruf — fixed-vector

**Reference:** Das DSG formuliert in den vorliegenden Artikeln kein eigenständiges allgemeines Widerrufsrecht. Es verlangt aber eine freiwillige und informierte Einwilligung [SR_235.1_DSG_de.md Art. 6], behandelt eine Bearbeitung entgegen der ausdrücklichen Willenserklärung als Persönlichkeitsverletzung [SR_235.1_DSG_de.md Art. 30] und nennt die Einwilligung nur als einen möglichen Rechtfertigungsgrund [SR_235.1_DSG_de.md Art. 31]. Wird sie für die Zukunft widerrufen, kann die Bearbeitung daher nicht mehr auf diese Einwilligung gestützt werden; ein anderer Rechtfertigungsgrund kann sie dennoch erlauben. Betroffene können insbesondere das Verbot einer Bearbeitung sowie gegebenenfalls Löschung oder Vernichtung verlangen [SR_235.1_DSG_de.md Art. 32].

**Generated:** Ja, Sie können eine Einwilligung zur Datenbearbeitung widerrufen.  

Gemäss Art. 8 Abs. 4 des Datenschutzgesetzes (DSG) gilt:  
> *„Die Einwilligung kann jederzeit mit Wirkung für die Zukunft widerrufen werden.“*  
[SR_235.1_DSG_de.md Art. 8 Abs. 4]  

Der Widerruf ist wirksam, sobald er beim Verantwortlichen eingegangen ist, und beendet ab diesem Zeitpunkt die Rechtmässigkeit der weiteren Verarbeitung — soweit die Verarbeitung ausschliesslich auf dieser Einwilligung beruht (vgl. Art. 7 Abs. 1 DSG in Verbindung mit Art. 8 Abs. 1–2 DSG) [SR_235.1_DSG_de.md Art. 8 Abs. 1–4; Art. 7 Abs. 1].

### dsg-einwilligung-widerruf — semantic-vector

**Reference:** Das DSG formuliert in den vorliegenden Artikeln kein eigenständiges allgemeines Widerrufsrecht. Es verlangt aber eine freiwillige und informierte Einwilligung [SR_235.1_DSG_de.md Art. 6], behandelt eine Bearbeitung entgegen der ausdrücklichen Willenserklärung als Persönlichkeitsverletzung [SR_235.1_DSG_de.md Art. 30] und nennt die Einwilligung nur als einen möglichen Rechtfertigungsgrund [SR_235.1_DSG_de.md Art. 31]. Wird sie für die Zukunft widerrufen, kann die Bearbeitung daher nicht mehr auf diese Einwilligung gestützt werden; ein anderer Rechtfertigungsgrund kann sie dennoch erlauben. Betroffene können insbesondere das Verbot einer Bearbeitung sowie gegebenenfalls Löschung oder Vernichtung verlangen [SR_235.1_DSG_de.md Art. 32].

**Generated:** Ja, eine Einwilligung zur Datenbearbeitung kann widerrufen werden. Dies folgt aus dem Datenschutzgesetz (DSG), wonach die Einwilligung **„nur gültig ist, wenn sie … freiwillig erteilt wird“**, was impliziert, dass sie auch jederzeit widerrufbar ist [SR_235.1_DSG_de.md Art. 15 Abs. 6].

Zudem sieht das DSG ausdrücklich Rechte der betroffenen Person vor, darunter das Recht auf **Löschung oder Vernichtung** der Daten sowie auf **Unterlassung der Bearbeitung**, was sich auch aus dem Recht auf Widerruf ableiten lässt [SR_235.1_DSG_de.md Art. 41 Abs. 2 lit. a].

Zusätzlich ist zu beachten: Die Einwilligung darf **nur für bestimmte, konkret beschriebene Bearbeitungen** erteilt werden und bleibt damit begrenzt – eine pauschale oder unspezifische Einwilligung ist nicht wirksam [SR_235.1_DSG_de.md Art. 15 Abs. 6].

### dsg-einwilligung-widerruf — rerank

**Reference:** Das DSG formuliert in den vorliegenden Artikeln kein eigenständiges allgemeines Widerrufsrecht. Es verlangt aber eine freiwillige und informierte Einwilligung [SR_235.1_DSG_de.md Art. 6], behandelt eine Bearbeitung entgegen der ausdrücklichen Willenserklärung als Persönlichkeitsverletzung [SR_235.1_DSG_de.md Art. 30] und nennt die Einwilligung nur als einen möglichen Rechtfertigungsgrund [SR_235.1_DSG_de.md Art. 31]. Wird sie für die Zukunft widerrufen, kann die Bearbeitung daher nicht mehr auf diese Einwilligung gestützt werden; ein anderer Rechtfertigungsgrund kann sie dennoch erlauben. Betroffene können insbesondere das Verbot einer Bearbeitung sowie gegebenenfalls Löschung oder Vernichtung verlangen [SR_235.1_DSG_de.md Art. 32].

**Generated:** Ja, eine Einwilligung zur Datenbearbeitung kann widerrufen werden. Dies ergibt sich aus derallgemeinen Rechtslage, wonach Einwilligungen nach angemessener Information **freiwillig** erteilt werden müssen – und freiwillige Willenserklärungen können grundsätzlich zurückgenommen werden.

Konkretisiert wird dies im Datenschutzrecht:  

> [SR_235.1_DSG_de.md Art. 7 Abs. 6]  
> *„Ist die Einwilligung der betroffenen Person erforderlich, so ist diese Einwilligung nur gültig, wenn sie für eine oder mehrere bestimmte Bearbeitungen nach angemessener Information freiwillig erteilt wird.“*  

Zwar enthält der gesamte Kontext keine ausdrückliche Widerrufsklausel, doch folgt aus dem Grundsatz der **freiwilligen** Einwilligung sowie aus allgemeinen zivilrechtlichen Grundsätzen (vgl. [SR_220_OR_de.md Art. 40b] zur Widerrufsmöglichkeit bei unerwünschten Angeboten), dass eine Einwilligung jederzeit mit Wirkung für die Zukunft widerrufen werden kann — insbesondere da sie nicht rechtsmissbräuchlich sein darf.

Zudem bestimmt Art. 31 Abs. 1 DSG ([SR_235.1_DSG_de.md Art. 31 Abs. 1]), dass eine Persönlichkeitsverletzung **nicht** widerrechtlich ist, wenn sie durch *Einwilligung* gerechtfertigt ist. Ein Widerruf beseitigt diese Rechtfertigungslücke — folglich darf die Bearbeitung nach Widerruf der Einwilligung nicht fortgesetzt werden, sofern kein anderer Rechtfertigungsgrund (z. B. gesetzliche Verpflichtung, überwiegendes Interesse) vorliegt.

Zusammenfassend:  
✅ Einwilligungen sind widerrufbar.  
✅ Der Widerruf muss nicht in einer bestimmten Form erfolgen (es sei denn, die Einwilligung selbst verlangt eine bestimmte Form für den Widerruf).  
✅ Der Widerruf wirkt **rückwirkungslos**, also nur für die Zukunft.  

Hinweis: Ein Widerruf beeinträchtigt nicht etwa bereits getätigte Zahlungen oder bestehende vertragliche Ansprüche — er betrifft lediglich künftige Datenverarbeitung.

### or-artikel-1 — fixed-vector

**Reference:** Zum Abschluss eines Vertrags ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich. Diese Willensäusserung kann ausdrücklich oder stillschweigend erfolgen [SR_220_OR_de.md Art. 1].

**Generated:** In Artikel 1 des Obligationenrechts (OR) steht:

**Art. 1**  
1 Zum Abschlusse eines Vertrages ist die übereinstimmende gegen seitige Willensäusserung der Parteien erforderlich.  
2 Sie kann eine ausdrückliche oder stillschweigende sein.  

[SR_220_OR_de.md Art. 1]

### or-artikel-1 — semantic-vector

**Reference:** Zum Abschluss eines Vertrags ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich. Diese Willensäusserung kann ausdrücklich oder stillschweigend erfolgen [SR_220_OR_de.md Art. 1].

**Generated:** Im gegebenen Kontext ist **keine Information zu Artikel 1 des OR (Obligationenrechts)** enthalten. Die aufgeführten Ausschnitte beziehen sich unter anderem auf Art. 335b OR (nicht explizit genannt), Art. 600 OR, Art. 731b, 819, 908 OR sowie Art. 697c–697hbis OR, aber nicht auf Art. 1 OR.

Daher ist die Antwort:

**Im vorliegenden Kontext ist nicht ersichtlich, was in Artikel 1 des OR steht.**

### or-artikel-1 — rerank

**Reference:** Zum Abschluss eines Vertrags ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich. Diese Willensäusserung kann ausdrücklich oder stillschweigend erfolgen [SR_220_OR_de.md Art. 1].

**Generated:** Im bereitgestellten Kontext ist der Inhalt von **Artikel 1 des OR** nicht enthalten. Die genannten Ausschnitte beziehen sich auf Artikel zu folgenden Themen:

- Art. 58 und 59 OR ([SR_210_ZGB_de.md::1729](SR_210_ZGB_de.md::1729))  
- ZPO-Artikel zu mass rechtlichen Maßnahmen ([SR_272_ZPO_de.md::413](SR_272_ZPO_de.md::413))  
- OR-Artikel zu Arbeitnehmern und Arbeitspflichten ([SR_220_OR_de.md::534](SR_220_OR_de.md::534))  
- StGB-Artikel zu strafrechtlichen Vorschriften ([SR_311.0_StGB_de.md::755](SR_311.0_StGB_de.md::755), [SR_311.0_StGB_de.md::161](SR_311.0_StGB_de.md::161), [SR_311.0_StGB_de.md::162](SR_311.0_StGB_de.md::162))  

Keiner dieser Ausschnitte enthält den Inhalt von **Art. 1 OR**.

**Antwort:**  
Der Inhalt von **Artikel 1 des OR** ist im bereitgestellten Kontext **nicht enthalten**.
