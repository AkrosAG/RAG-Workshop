# RAG evaluation

- Methods: **fixed-vector, semantic-vector**
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
| or-kaufvertrag-verjaehrung | fixed-vector | 100% | 100% | 100% | 1.00 | 100% | 1,198 | 1,284 |
| or-kaufvertrag-verjaehrung | semantic-vector | 100% | 0% | 0% | 0.00 | 33% | 726 | 810 |
| bgg-beschwerdefrist | fixed-vector | 100% | 100% | 100% | 0.33 | 100% | 1,200 | 1,296 |
| bgg-beschwerdefrist | semantic-vector | 100% | 100% | 100% | 0.50 | 100% | 742 | 842 |
| or-probezeit | fixed-vector | 100% | 0% | 0% | 0.00 | 67% | 1,200 | 1,288 |
| or-probezeit | semantic-vector | 100% | 100% | 100% | 1.00 | 67% | 813 | 901 |
| dsg-einwilligung-widerruf | fixed-vector | 100% | 100% | 25% | 0.25 | 75% | 1,198 | 1,292 |
| dsg-einwilligung-widerruf | semantic-vector | 100% | 0% | 0% | 0.00 | 75% | 941 | 1,032 |
| or-artikel-1 | fixed-vector | 100% | 100% | 100% | 1.00 | 80% | 1,198 | 1,291 |
| or-artikel-1 | semantic-vector | 100% | 0% | 0% | 0.00 | 0% | 745 | 834 |

## Answers

| Question | Method | Fact coverage | Expected-citation precision | Citation grounding | Citation completeness | Answer tokens |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| or-kuendigung-krankheit | fixed-vector | 0% | 0% | 0% | 0% | 459 |
| or-kuendigung-krankheit | semantic-vector | 0% | 0% | 100% | 0% | 400 |
| or-kaufvertrag-verjaehrung | fixed-vector | 50% | 33% | 100% | 100% | 332 |
| or-kaufvertrag-verjaehrung | semantic-vector | 50% | 0% | 100% | 0% | 337 |
| bgg-beschwerdefrist | fixed-vector | 67% | 50% | 100% | 100% | 352 |
| bgg-beschwerdefrist | semantic-vector | 67% | 50% | 100% | 100% | 349 |
| or-probezeit | fixed-vector | 100% | 100% | 0% | 100% | 224 |
| or-probezeit | semantic-vector | 67% | 33% | 100% | 100% | 436 |
| dsg-einwilligung-widerruf | fixed-vector | 0% | 0% | 100% | 0% | 54 |
| dsg-einwilligung-widerruf | semantic-vector | 0% | 0% | 0% | 0% | 408 |
| or-artikel-1 | fixed-vector | 100% | 100% | 100% | 100% | 64 |
| or-artikel-1 | semantic-vector | 0% | 0% | 0% | 0% | 134 |

## Summary

- **fixed-vector:** article recall@K 54.2%, MRR 0.43, fact coverage 52.8%, expected-citation precision 47.2%, citation grounding 66.7%, citation completeness 66.7%, average context 1,289 tokens, corpus-token savings 99.88%.
- **semantic-vector:** article recall@K 33.3%, MRR 0.25, fact coverage 30.6%, expected-citation precision 13.9%, citation grounding 66.7%, citation completeness 33.3%, average context 892 tokens, corpus-token savings 99.92%.

## Strategic token perspective

All selected methods receive the same final chunk budget. Their actual token counts can differ because the retrieved chunks have different lengths.

## Answer details

### or-kuendigung-krankheit — fixed-vector

**Reference:** Nach Ablauf der Probezeit darf der Arbeitgeber bei einer unverschuldeten krankheitsbedingten vollständigen oder teilweisen Arbeitsverhinderung während der gesetzlichen Sperrfrist nicht kündigen: 30 Tage im ersten Dienstjahr, 90 Tage vom zweiten bis und mit fünften Dienstjahr und 180 Tage ab dem sechsten Dienstjahr. Eine während der Sperrfrist ausgesprochene Kündigung ist nichtig. Wurde vorher gekündigt und läuft die Kündigungsfrist in die Sperrfrist hinein, wird ihr Ablauf unterbrochen und danach fortgesetzt. Während der Probezeit gilt dieser Schutz nicht [SR_220_OR_de.md Art. 336c].

**Generated:** Ja, der Arbeitgeber darf während der Krankheit des Arbeitnehmers grundsätzlich kündigen — **aber nur außerhalb einer gesetzlich geschützten Sperrfrist**.

Laut Artikel 335c Absatz 1 des Schweizerischen Obligationenrechts (SR 220 OR) besteht eine **Sperrfrist** für die Kündigung während bestimmter Verhinderungszeiten, darunter auch bei Krankheit:

> *„Die Kündigung ist ausgeschlossen während:*  
> *a. der Arbeitnehmer durch Krankheit, Unfall oder Schwangerschaft an der Arbeitsleistung verhindert ist, soweit er im Dienst ist und die Verhinderung nicht durch sein Verschulden verursacht ist;*  
> *...*  
> *c. der Arbeitnehmer an einer von der zuständigen Bundesbehörde angeordneten Dienstleistung für eine Hilfsaktion im Ausland teilnimmt.“*  
> [SR_220_OR_de.md Art. 335c Abs. 1]

Die Kündigung ist in dieser Sperrfrist **nichtig** (Art. 335c Abs. 2). Ist die Kündigung dagegen **vor Beginn der Sperrfrist** ausgesprochen, so wird die Kündigungsfrist **unterbrochen** und erst nach Beendigung der Sperrfrist fortgesetzt (Art. 335c Abs. 2) [SR_220_OR_de.md Art. 335c Abs. 2].

Zusätzlich gilt:  
- Die Sperrfrist beginnt mit dem ersten Tag der Verhinderung (z. B. Krankheit) und erstreckt sich über die **gesamte Dauer der Verhinderung**, sofern diese nicht durch Verschulden des Arbeitnehmers verursacht ist.  
- Für die Dauer des Arbeitsausfalls aufgrund von Krankheit (ohne Verschulden) besteht zudem ein **Lohnanspruch** (Art. 324a), aber kein Schutz vor Kündigung **außerhalb** der Sperrfrist.

**Zusammenfassung**:  
Der Arbeitgeber darf **nicht während einer Krankheitsphase kündigen**, wenn die Krankheit nicht auf dem Verschulden des Arbeitnehmers beruht — das ist ausdrücklich gesetzlich gesperrt [SR_220_OR_de.md Art. 335c Abs. 1 lit. a]. Kündigt er doch, ist die Kündigung **nichtig** [SR_220_OR_de.md Art. 335c Abs. 2].

### or-kuendigung-krankheit — semantic-vector

**Reference:** Nach Ablauf der Probezeit darf der Arbeitgeber bei einer unverschuldeten krankheitsbedingten vollständigen oder teilweisen Arbeitsverhinderung während der gesetzlichen Sperrfrist nicht kündigen: 30 Tage im ersten Dienstjahr, 90 Tage vom zweiten bis und mit fünften Dienstjahr und 180 Tage ab dem sechsten Dienstjahr. Eine während der Sperrfrist ausgesprochene Kündigung ist nichtig. Wurde vorher gekündigt und läuft die Kündigungsfrist in die Sperrfrist hinein, wird ihr Ablauf unterbrochen und danach fortgesetzt. Während der Probezeit gilt dieser Schutz nicht [SR_220_OR_de.md Art. 336c].

**Generated:** Ja, der Arbeitgeber darf während der Krankheit des Arbeitnehmers **grundsätzlich kündigen**, jedoch unter besonderen Schutzvorschriften.

Gemäss Art. 328a Abs. 2 SR 220 OR besteht ein Schutz nicht automatisch durch die Krankheit allein. Die Vorschrift regelt vielmehr die Pflicht des Arbeitgebers, bei verhinderter Arbeitsleistung infolge Krankheit oder Unfall **Pflege und ärztliche Behandlung** zu gewähren – nicht jedoch eine Kündigungsverbotsfrist.

Ein **gesonderer Kündigungsschutz besteht jedoch in bestimmten Fällen**, beispielsweise:

- Während der **Mutterschaft** (Art. 329f) sowie  
- Während eines **Elternschaftsurlaubs**, eines **Betreuungsurlaubs** oder bei Inanspruchnahme des **Urlaubs des andern Elternteils** (Art. 329b Abs. 3 lit. c und d).

Zudem ist zu beachten, dass gemäss Art. 335b Abs. 3 SR 220 OR bei **Verhinderung infolge Krankheit während der Probezeit** die Probezeit entsprechend verlängert wird – das heißt, die Kündigung während der Krankheit ist dann möglicherweise gar nicht mehr zulässig, solange die Probezeit noch nicht abgelaufen ist (da sich die Probezeit verlängert).

**Kein ausdrücklicher Kündigungsverbot** ergibt sich aus Art. 328a Abs. 2 allein. Ein allgemeiner Schutz vor Kündigung während Krankheit ist im Schweizer Obligationenrecht **nicht vorgesehen**, solange keine speziellen Schutzvorschriften greifen (z. B. Mutterschaft, Elternschaft, langer Krankheitsverlauf mit versicherungsrechtlichen Folgen gemäss KSchG – das aber außerhalb des SR 220 OR).

Quelle: [SR_220_OR_de.md Art. 328a], [SR_220_OR_de.md Art. 329b], [SR_220_OR_de.md Art. 335b].

### or-kaufvertrag-verjaehrung — fixed-vector

**Reference:** Für Forderungen aus einem Kaufvertrag gilt grundsätzlich die allgemeine Verjährungsfrist von zehn Jahren, sofern das Bundeszivilrecht für den konkreten Anspruch keine abweichende Frist vorsieht [SR_220_OR_de.md Art. 127].

**Generated:** Forderungen aus einem Kaufvertrag verjähren nach **zwei Jahren** nach der Ablieferung der Sache an den Käufer, unabhängig davon, wann der Käufer die Mängel entdeckt, sofern nicht eine längere Haftungsfrist vereinbart wurde. Dies gilt insbesondere für Gewährleistungsansprüche wegen Mängeln der Sache [SR_220_OR_de.md Art. 21075].

Für Forderungen, die sich nicht auf Gewährleistungsmängel beziehen (z. B. auf Zahlungsverpflichtungen des Käufers), ist die allgemeine Verjährungsfrist von **zehn Jahren** maßgeblich, sofern das Bundeszivilrecht nichts anderes vorsieht [SR_220_OR_de.md Art. 127].

Zusätzlich verjähren Forderungen aus periodischen Leistungen (z. B. Ratenzahlungen) nach **fünf Jahren** [SR_220_OR_de.md Art. 128 Ziff. 1]. Allerdings betrifft dies nicht die Hauptforderung selbst, sondern nur die einzelnen periodischen Zahlungen.

Zusammenfassend hängt die Verjährungsfrist von der Art der Forderung ab:

- **Gewährleistungsansprüche wegen Mängeln der Sache**: **2 Jahre** nach Ablieferung [SR_220_OR_de.md Art. 21075];
- **Sonstige Forderungen aus dem Kaufvertrag (z. B. Kaufpreisforderung)**: **10 Jahre**, sofern nicht besondere Vorschriften gelten [SR_220_OR_de.md Art. 127];
- **Periodisch fällige Leistungen (z. B. Raten)**: **5 Jahre** nach Fälligkeit jeder einzelnen Leistung [SR_220_OR_de.md Art. 128].

### or-kaufvertrag-verjaehrung — semantic-vector

**Reference:** Für Forderungen aus einem Kaufvertrag gilt grundsätzlich die allgemeine Verjährungsfrist von zehn Jahren, sofern das Bundeszivilrecht für den konkreten Anspruch keine abweichende Frist vorsieht [SR_220_OR_de.md Art. 127].

**Generated:** Forderungen aus einem Kaufvertrag verjähren grundsätzlich **mit Ablauf von zwei Jahren nach deren Ablieferung an den Käufer**, wie aus dem Obligationenrecht (OR) hervorgeht:

> **Art. 21075 OR**  
> *1 Die Klagen auf Gewährleistung wegen Mängel der Sache verjähren mit Ablauf von zwei Jahren nach deren Ablieferung an den Käufer, selbst wenn dieser die Mängel erst später entdeckt, es sei denn, dass der Verkäufer eine Haftung auf längere Zeit übernommen hat.* [SR_220_OR_de.md Art. 21075]

Hinzu kommt, dass **andere Forderungen aus dem Kaufvertrag** (z. B. Kaufpreisforderungen des Verkäufers oder Schadensersatzforderungen außerhalb der Gewährleistung) nicht explizit in diesem Artikel geregelt sind. In solchen Fällen gilt die **allgemeine Verjährungsfrist von 10 Jahren** gemäß **Art. 127 ZGB**, sofern nicht eine spezifisch kürzere Frist (z. B. für Mängelgewährleistung oder Arbeitsergebnisse) greift.

Beispiel:  
- Gewährleistungsklagen wegen Mängel der Sache → **2 Jahre** nach Ablieferung (OR Art. 21075)  
- Kaufpreisforderung des Verkäufers → **10 Jahre**, sofern nicht vereinbart (ZGB Art. 127)  
- Mängel bei beweglichen Werken, die in unbewegliche Werke integriert sind → **5 Jahre** (OR Art. 371260 Abs. 1 second sentence)

Der Gesamtverjährungszeitraum hängt somit von der **Art der Forderung** ab, die aus dem Kaufvertrag erwächst.

### bgg-beschwerdefrist — fixed-vector

**Reference:** Grundsätzlich ist die Beschwerde gegen einen Entscheid innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen. Artikel 100 BGG sieht für bestimmte Fälle kürzere Fristen von zehn, fünf oder drei Tagen vor; gegen das unrechtmässige Verweigern oder Verzögern eines Entscheids kann jederzeit Beschwerde geführt werden [SR_173.110_BGG_de.md Art. 100].

**Generated:** Für eine Beschwerde ans Bundesgericht gilt grundsätzlich eine Frist von **30 Tagen**.

Dies ergibt sich aus:

- **SR_173.110_BGG_de.md Art. 100 Abs. 1**: *„Die Beschwerde gegen einen Entscheid ist innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen.“* [SR_173.110_BGG_de.md Art. 100 Abs. 1]

Zusätzlich bestimmt **SR_272_ZPO_de.md Art. 389 Abs. 2**, dass für Beschwerden gegen Schiedssprüche an das Bundesgericht die Bestimmungen des Bundesgerichtsgesetzes (BGG) gelten, soweit nicht im ZPO-Kapitel selbst Abweichendes geregelt ist. Auch hier findet sich die allgemeine 30-Tage-Frist.

Es bestehen jedoch Ausnahmen mit kürzeren Fristen, z. B.:

- **10 Tage** bei Entscheiden kantonaler Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen ([SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. a]),
- **5 Tage** bei bestimmten Entscheiden (z. B. im Rahmen der Wechselbetreibung, über Beschwerden gegen eidgenössische Abstimmungen) ([SR_173.110_BGG_de.md Art. 100 Abs. 3]),
- **3 Tage** bei Entscheiden der Kantonsregierungen über Beschwerden gegen Nationalratswahlen ([SR_173.110_BGG_de.md Art. 100 Abs. 4]).

Für Beschwerden im Asylverfahren gelten zudem besondere Fristen, z. B. **sieben Arbeitstage** im beschleunigten Verfahren ([SR_142.31_AsylG_de.md Art. 108 Abs. 1]).  

Ohne spezifische Vorgaben im Einzelgesetz gilt jedoch die **allgemeine Frist von 30 Tagen**.

### bgg-beschwerdefrist — semantic-vector

**Reference:** Grundsätzlich ist die Beschwerde gegen einen Entscheid innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen. Artikel 100 BGG sieht für bestimmte Fälle kürzere Fristen von zehn, fünf oder drei Tagen vor; gegen das unrechtmässige Verweigern oder Verzögern eines Entscheids kann jederzeit Beschwerde geführt werden [SR_173.110_BGG_de.md Art. 100].

**Generated:** Die allgemeine Beschwerdefrist beim Bundesgericht beträgt **30 Tage**, und zwar nach der Eröffnung der vollständigen Ausfertigung des Entscheids [SR_173.110_BGG_de.md Art. 100 Abs. 1].

Zusätzlich gibt es Sonderfristen, z. B.:

- **10 Tage** bei Entscheiden der kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. a];
- **10 Tage** bei Entscheiden auf dem Gebiet der internationalen Rechtshilfe in Strafsachen und der internationalen Amtshilfe in Steuersachen [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. b];
- **10 Tage** bei Entscheiden über die Rückgabe eines Kindes nach dem Europäischen Übereinkommen vom 20. Mai 1980 [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. c];
- **5 Tage** bei Entscheiden der kantonalen Aufsichtsbehörden im Rahmen der Wechselbetreibung sowie bei Entscheiden der Kantonsregierungen über Beschwerden gegen eidgenössische Abstimmungen [SR_173.110_BGG_de.md Art. 101 Abs. 3 lit. a, b];
- **3 Tage** bei Entscheiden der Kantonsregierungen über Beschwerden gegen die Nationalratswahlen [SR_173.110_BGG_de.md Art. 101 Abs. 3 lit. c].

Für Erweise (nicht Entscheide) beträgt die Beschwerdefrist 30 Tage nach der nach kantonalem Recht massgebenden Veröffentlichung [SR_173.110_BGG_de.md Art. 101].

Somit gilt **grundsätzlich eine Frist von 30 Tagen**, es sei denn, gesetzlich ist etwas anderes geregelt (Sonderfristen).

### or-probezeit — fixed-vector

**Reference:** Als Probezeit gilt grundsätzlich der erste Monat des Arbeitsverhältnisses. Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann davon abgewichen werden; die Probezeit darf jedoch höchstens drei Monate dauern. Während der Probezeit gilt eine Kündigungsfrist von sieben Tagen [SR_220_OR_de.md Art. 335b].

**Generated:** Im Arbeitsverhältnis beträgt die Probezeit grundsätzlich **einen Monat**, wie festgelegt in Artikel 335b Absatz 1 des Schweizerischen Obligationenrechts (SR 220 OR):

> „d der Probezeit jederzeit mit einer Kündigungsfrist von sieben Tagen gekündigt werden; als Probezeit gilt der erste Monat eines Arbeitsverhältnisses“ [SR_220_OR_de.md Art. 335b].

Abweichend davon kann die Probezeit **auf höchstens drei Monate verlängert** werden, wobei eine solche Verlängerung durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag erfolgen muss, sofern nicht bereits ein längerer, aber max. dreimonatiger Probezeitabschnitt vereinbart wurde [SR_220_OR_de.md Art. 335b Abs. 2].

Zudem kann die Probezeit bei Verkürzung infolge Krankheit, Unfall oder Erfüllung einer nicht freiwillig übernommenen gesetzlichen Pflicht **entsprechend verlängert** werden [SR_220_OR_de.md Art. 335b Abs. 3].

### or-probezeit — semantic-vector

**Reference:** Als Probezeit gilt grundsätzlich der erste Monat des Arbeitsverhältnisses. Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann davon abgewichen werden; die Probezeit darf jedoch höchstens drei Monate dauern. Während der Probezeit gilt eine Kündigungsfrist von sieben Tagen [SR_220_OR_de.md Art. 335b].

**Generated:** Die Dauer der Probezeit im Arbeitsverhältnis richtet sich nach dem jeweiligen Vertragstyp und beträgt:

1. **Im regulären Arbeitsverhältnis** (gemäss Art. 335b SR_220_OR_de.md):  
   - Der **erste Monat** des Arbeitsverhältnisses gilt per Default als Probezeit ([SR_220_OR_de.md Art. 335b Abs. 1]).  
   - Durch schriftliche Vereinbarung (Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag) kann die Probezeit **auf höchstens drei Monate verlängert** werden ([SR_220_OR_de.md Art. 335b Abs. 2]).  
   - Bei vorübergehender Verhinderung (z. B. Krankheit, Unfall, gesetzliche Pflicht) erfolgt eine entsprechende **Verlängerung** der Probezeit ([SR_220_OR_de.md Art. 335b Abs. 3]).

2. **Im Lehrvertrag** (gemäss Art. 344a SR_220_OR_de.md):  
   - Die Probezeit beträgt **mindestens einen Monat, maximal drei Monate** ([SR_220_OR_de.md Art. 344a Abs. 3]).  
   - Fehlt die Vereinbarung, gilt automatisch eine Probezeit von **drei Monaten** ([SR_220_OR_de.md Art. 344a Abs. 3]).  
   - Vor Ablauf der Probezeit kann sie mit Zustimmung der kantonalen Behörde auf **maximal sechs Monate** verlängert werden ([SR_220_OR_de.md Art. 344a Abs. 4]).

3. **Beim Heimarbeitnehmer** (gemäss Art. 354 SR_220_OR_de.md):  
   - Bei Probearbeit gilt das Arbeitsverhältnis **zur Probe auf bestimmte Zeit**, sofern nicht anderes vereinbart ([SR_220_OR_de.md Art. 354 Abs. 1]).  
   - Die konkrete Dauer ist nicht definiert; sie richtet sich nach der konkreten Vereinbarung.

**Zusammenfassung**:  
Die gesetzliche Standarddauer der Probezeit im Arbeitsverhältnis beträgt **einen Monat**, kann aber **bis maximal drei Monate** verlängert werden — ausgenommen im Ausbildungsverhältnis, wo eine vorübergehende Verlängerung auf **bis zu sechs Monate** möglich ist.

### dsg-einwilligung-widerruf — fixed-vector

**Reference:** Das DSG formuliert in den vorliegenden Artikeln kein eigenständiges allgemeines Widerrufsrecht. Es verlangt aber eine freiwillige und informierte Einwilligung [SR_235.1_DSG_de.md Art. 6], behandelt eine Bearbeitung entgegen der ausdrücklichen Willenserklärung als Persönlichkeitsverletzung [SR_235.1_DSG_de.md Art. 30] und nennt die Einwilligung nur als einen möglichen Rechtfertigungsgrund [SR_235.1_DSG_de.md Art. 31]. Wird sie für die Zukunft widerrufen, kann die Bearbeitung daher nicht mehr auf diese Einwilligung gestützt werden; ein anderer Rechtfertigungsgrund kann sie dennoch erlauben. Betroffene können insbesondere das Verbot einer Bearbeitung sowie gegebenenfalls Löschung oder Vernichtung verlangen [SR_235.1_DSG_de.md Art. 32].

**Generated:** Ja, eine Einwilligung zur Datenbearbeitung kann widerrufen werden.  

Gemäss Art. 7 Abs. 5 DSG lautet:  
> „Die Einwilligung kann jederzeit mit Wirkung für die Zukunft widerrufen werden.“  
[SR_235.1_DSG_de.md Art. 7]

### dsg-einwilligung-widerruf — semantic-vector

**Reference:** Das DSG formuliert in den vorliegenden Artikeln kein eigenständiges allgemeines Widerrufsrecht. Es verlangt aber eine freiwillige und informierte Einwilligung [SR_235.1_DSG_de.md Art. 6], behandelt eine Bearbeitung entgegen der ausdrücklichen Willenserklärung als Persönlichkeitsverletzung [SR_235.1_DSG_de.md Art. 30] und nennt die Einwilligung nur als einen möglichen Rechtfertigungsgrund [SR_235.1_DSG_de.md Art. 31]. Wird sie für die Zukunft widerrufen, kann die Bearbeitung daher nicht mehr auf diese Einwilligung gestützt werden; ein anderer Rechtfertigungsgrund kann sie dennoch erlauben. Betroffene können insbesondere das Verbot einer Bearbeitung sowie gegebenenfalls Löschung oder Vernichtung verlangen [SR_235.1_DSG_de.md Art. 32].

**Generated:** Ja, Sie können eine Einwilligung zur Datenbearbeitung widerrufen. Dies ergibt sich aus Art. 41 Abs. 1 lit. a SR_235.1_DSG_de.md, wonach eine betroffene Person mit schutzwürdigem Interesse verlangen kann, dass das verantwortliche Bundesorgan **die widerrechtliche Bearbeitung der betreffenden Personendaten unterlässt** – was insbesondere auch einen Widerruf der Einwilligung beinhaltet.

Zudem wird in Art. 15 Abs. 7 SR_235.1_DSG_de.md klargestellt, dass die **Einwilligung nur gültig ist, wenn sie freiwillig erteilt wird**, was impliziert, dass sie auch widerrufen werden kann. Der Widerruf ist jedoch nicht wirksam, wenn eine gesetzliche Grundlage die Bearbeitung unabhängig von der Einwilligung erlaubt (z. B. bei öffentlichen Aufgaben nach Art. 6 DSGVO analog).

Zusätzlich ist zu beachten:  
- Nach Art. 15 Abs. 6 SR_235.1_DSG_de.md muss die Einwilligung **ausdrücklich** erfolgen, wenn es sich um besonders schützenswerte Personendaten, Profiling mit hohem Risiko (durch private Personen) oder Profiling (durch Bundesorgane) handelt. Solche ausdrücklichen Einwilligungen sind grundsätzlich widerrufbar, es sei denn, das Gesetz sieht Ausnahmen vor.  

Zur Einhaltung des Rechts auf Widerruf ist es sinnvoll, den Widerruf **schriftlich** vorzunehmen und gegebenenfalls die Gründe anzugeben. Weitere Ansprüche – etwa auf Berichtigung, Löschung oder Bestreitungsvermerk – ergeben sich aus Art. 41 Abs. 2 lit. a SR_235.1_DSG_de.md.

> **Hinweis**: Der Widerruf wirkt nur für die Zukunft (rückwirkungslos), sofern nicht bereits rechtswidrige Bearbeitung vorliegt, die beseitigt werden muss (Art. 41 Abs. 1 lit. b SR_235.1_DSG_de.md).

### or-artikel-1 — fixed-vector

**Reference:** Zum Abschluss eines Vertrags ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich. Diese Willensäusserung kann ausdrücklich oder stillschweigend erfolgen [SR_220_OR_de.md Art. 1].

**Generated:** In Artikel 1 des Obligationenrechts (OR) steht:

1. *Zum Abschlusse eines Vertrages ist die übereinstimmende gegen seitige Willensäusserung der Parteien erforderlich.*  
2. *Sie kann eine ausdrückliche oder stillschweigende sein.*  

[SR_220_OR_de.md Art. 1]

### or-artikel-1 — semantic-vector

**Reference:** Zum Abschluss eines Vertrags ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich. Diese Willensäusserung kann ausdrücklich oder stillschweigend erfolgen [SR_220_OR_de.md Art. 1].

**Generated:** Im vorliegenden Kontext ist **kein Ausschnitt zu Artikel 1 des Schweizerischen Obligationenrechts (OR)** enthalten. Es wird nur das Kapitel 534 („Begriff und Entstehung …“) sowie andere Stellen genannt, aber nicht der eigentliche Artikel 1 OR.

Folglich lässt sich auf Grundlage des bereitgestellten Kontextes **nicht feststellen**, was in **Artikel 1 des OR** steht.

Um die Antwort zu erhalten, müsste der vollständige Text von **Art. 1 OR** – typischerweise mit dem Titel „Anwendungsbereich des Obligationenrechts“ – vorgelegt werden.
