# RAG evaluation

- Methods: **fixed-vector, semantic-vector, rerank, graph**
- Collections: `fixed=rag_fixed`, `semantic=rag_semantic`
- Shared context budget: **6 chunks**
- Full corpus: approximately **1,101,461 tokens**
- Token counts are estimated as characters / 4.
- Term coverage is shown only as a retrieval diagnostic; it is not an answer-quality score.

## Retrieval

| Question | Method | Source recall | Article Hit@K | Article Recall@K | Article MRR | Term coverage (diagnostic) | Document tokens | Prompt-context tokens |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| or-kuendigung-krankheit | fixed-vector | 100% | 0% | 0% | 0.00 | 67% | 1,195 | 1,285 |
| or-kuendigung-krankheit | semantic-vector | 100% | 0% | 0% | 0.00 | 17% | 842 | 926 |
| or-kuendigung-krankheit | rerank | 100% | 100% | 100% | 1.00 | 83% | 900 | 984 |
| or-kuendigung-krankheit | graph | 100% | 100% | 100% | 0.50 | 83% | 762 | 848 |
| or-kaufvertrag-verjaehrung | fixed-vector | 100% | 100% | 100% | 1.00 | 100% | 1,166 | 1,284 |
| or-kaufvertrag-verjaehrung | semantic-vector | 100% | 0% | 0% | 0.00 | 33% | 804 | 897 |
| or-kaufvertrag-verjaehrung | rerank | 100% | 100% | 100% | 0.50 | 100% | 617 | 710 |
| or-kaufvertrag-verjaehrung | graph | 100% | 0% | 0% | 0.00 | 33% | 424 | 510 |
| bgg-beschwerdefrist | fixed-vector | 100% | 100% | 100% | 0.33 | 100% | 1,200 | 1,296 |
| bgg-beschwerdefrist | semantic-vector | 100% | 100% | 100% | 0.50 | 100% | 742 | 842 |
| bgg-beschwerdefrist | rerank | 100% | 100% | 100% | 1.00 | 100% | 774 | 872 |
| bgg-beschwerdefrist | graph | 100% | 100% | 100% | 0.33 | 100% | 789 | 887 |
| or-probezeit | fixed-vector | 100% | 0% | 0% | 0.00 | 67% | 1,200 | 1,290 |
| or-probezeit | semantic-vector | 100% | 100% | 100% | 1.00 | 67% | 813 | 901 |
| or-probezeit | rerank | 100% | 100% | 100% | 1.00 | 67% | 890 | 980 |
| or-probezeit | graph | 100% | 100% | 100% | 1.00 | 67% | 848 | 933 |
| dsg-einwilligung-widerruf | fixed-vector | 100% | 100% | 25% | 0.25 | 75% | 1,198 | 1,292 |
| dsg-einwilligung-widerruf | semantic-vector | 100% | 0% | 0% | 0.00 | 75% | 941 | 1,032 |
| dsg-einwilligung-widerruf | rerank | 100% | 100% | 25% | 0.05 | 75% | 925 | 1,015 |
| dsg-einwilligung-widerruf | graph | 100% | 100% | 25% | 0.04 | 75% | 821 | 912 |
| or-artikel-1 | fixed-vector | 100% | 100% | 100% | 1.00 | 60% | 1,194 | 1,292 |
| or-artikel-1 | semantic-vector | 100% | 0% | 0% | 0.00 | 0% | 767 | 856 |
| or-artikel-1 | rerank | 100% | 0% | 0% | 0.00 | 0% | 822 | 911 |
| or-artikel-1 | graph | 100% | 100% | 100% | 1.00 | 80% | 750 | 844 |

## Answers

| Question | Method | Fact coverage | Expected-citation precision | Citation grounding | Citation completeness | Answer tokens |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| or-kuendigung-krankheit | fixed-vector | 0% | 33% | 33% | 100% | 817 |
| or-kuendigung-krankheit | semantic-vector | 0% | 0% | 100% | 0% | 450 |
| or-kuendigung-krankheit | rerank | 67% | 50% | 100% | 100% | 432 |
| or-kuendigung-krankheit | graph | 33% | 100% | 100% | 100% | 414 |
| or-kaufvertrag-verjaehrung | fixed-vector | 100% | 100% | 100% | 100% | 324 |
| or-kaufvertrag-verjaehrung | semantic-vector | 0% | 0% | 100% | 0% | 286 |
| or-kaufvertrag-verjaehrung | rerank | 50% | 25% | 100% | 100% | 621 |
| or-kaufvertrag-verjaehrung | graph | 0% | 0% | 100% | 0% | 164 |
| bgg-beschwerdefrist | fixed-vector | 67% | 25% | 100% | 100% | 408 |
| bgg-beschwerdefrist | semantic-vector | 100% | 33% | 100% | 100% | 332 |
| bgg-beschwerdefrist | rerank | 67% | 33% | 100% | 100% | 535 |
| bgg-beschwerdefrist | graph | 100% | 50% | 100% | 100% | 319 |
| or-probezeit | fixed-vector | 33% | 0% | 100% | 0% | 185 |
| or-probezeit | semantic-vector | 67% | 33% | 100% | 100% | 368 |
| or-probezeit | rerank | 67% | 50% | 100% | 100% | 324 |
| or-probezeit | graph | 67% | 50% | 100% | 100% | 214 |
| dsg-einwilligung-widerruf | fixed-vector | 0% | 0% | 0% | 0% | 384 |
| dsg-einwilligung-widerruf | semantic-vector | 0% | 0% | 50% | 0% | 501 |
| dsg-einwilligung-widerruf | rerank | 75% | 100% | 50% | 50% | 525 |
| dsg-einwilligung-widerruf | graph | 25% | 0% | 0% | 0% | 255 |
| or-artikel-1 | fixed-vector | 100% | 100% | 100% | 100% | 74 |
| or-artikel-1 | semantic-vector | 0% | 0% | 0% | 0% | 164 |
| or-artikel-1 | rerank | 0% | 0% | 0% | 0% | 227 |
| or-artikel-1 | graph | 100% | 100% | 100% | 100% | 73 |

## Summary

- **fixed-vector:** article recall@K 54.2%, MRR 0.43, fact coverage 50.0%, expected-citation precision 43.1%, citation grounding 72.2%, citation completeness 66.7%, average context 1,290 tokens, corpus-token savings 99.88%.
- **semantic-vector:** article recall@K 33.3%, MRR 0.25, fact coverage 27.8%, expected-citation precision 11.1%, citation grounding 75.0%, citation completeness 33.3%, average context 909 tokens, corpus-token savings 99.92%.
- **rerank:** article recall@K 70.8%, MRR 0.59, fact coverage 54.2%, expected-citation precision 43.1%, citation grounding 75.0%, citation completeness 75.0%, average context 912 tokens, corpus-token savings 99.92%.
- **graph:** article recall@K 70.8%, MRR 0.48, fact coverage 54.2%, expected-citation precision 50.0%, citation grounding 83.3%, citation completeness 66.7%, average context 822 tokens, corpus-token savings 99.93%.

## Strategic token perspective

All methods receive the same final chunk budget. Because chunking and retrieval differ, their actual token counts can still differ.

In this run GraphRAG used **-9.5%** context tokens compared with semantic Vector-RAG. Interpret this together with retrieval, fact coverage and citation quality.

## Answer details

### or-kuendigung-krankheit — fixed-vector

**Reference:** Nach Ablauf der Probezeit darf der Arbeitgeber bei einer unverschuldeten krankheitsbedingten vollständigen oder teilweisen Arbeitsverhinderung während der gesetzlichen Sperrfrist nicht kündigen: 30 Tage im ersten Dienstjahr, 90 Tage vom zweiten bis und mit fünften Dienstjahr und 180 Tage ab dem sechsten Dienstjahr. Eine während der Sperrfrist ausgesprochene Kündigung ist nichtig. Wurde vorher gekündigt und läuft die Kündigungsfrist in die Sperrfrist hinein, wird ihr Ablauf unterbrochen und danach fortgesetzt. Während der Probezeit gilt dieser Schutz nicht [SR_220_OR_de.md Art. 336c].

**Generated:** Ja, der Arbeitgeber **darf grundsätzlich während der Krankheit kündigen**, **es gelten jedoch besondere Schutzvorschriften**, insbesondere **Sperrfristen**, die eine Kündigung während bestimmter Schutzperioden **nichtig** machen.

Laut Artikel 328a Absatz 2 des Obligationenrechts ([SR_220_OR_de.md Art. 328a]) darf der Arbeitgeber bei vorübergehender Verhinderung der Arbeitsleistung durch Krankheit **für eine beschränkte Zeit Pflege und ärztliche Behandlung gewähren** – im ersten Dienstjahr für drei Wochen, danach je nach Dauer des Arbeitsverhältnisses und den Umständen für eine angemessene längere Zeit.

Wichtig ist jedoch **Artikel 340 Absatz 1** ([SR_220_OR_de.md Art. 340]), der lautet:

> „Die Kündigung, die während einer der in Absatz 1 festgesetzten Sperrfristen erklärt wird, ist nichtig.“

In **Artikel 340 Absatz 1** sind folgende Schutzfristen aufgelistet, in denen eine Kündigung nichtig ist:

> „Die Sperrfristen betreffen:  
> a. während der Probezeit;  
> b. während der Verhinderung an der Arbeitsleistung, soweit sie durch Krankheit oder Unfall verursacht ist und nicht mehr als einen Monat im Dienstjahr beträgt, sofern sie nicht durch einen Vertrag geregelt ist;  
> c. während der Verhinderung an der Arbeitsleistung, soweit sie durch Erfüllung gesetzlicher Pflichten, Ausübung eines öffentlichen Amtes oder Jugendurlaub verursacht ist;  
> d. während des Mutterschaftsurlaubs nach Artikel 329f;  
> e. während des Urlaubs des anderen Elternteils nach Artikel 329g oder des Urlaubs im Falle des Todes der Mutter nach Artikel 329gbis;  
> f. während des Betreuungsurlaubs nach Artikel 329i;  
> g. während der Arbeitnehmer mit Zustimmung des Arbeitgebers an einer von der zuständigen Bundesbehörde angeordneten Dienstleistung für eine Hilfsaktion im Ausland teilnimmt.“

Somit:  
➡️ **Kürzere Krankheit (nicht mehr als einen Monat im Dienstjahr)**: Die Kündigung ist **nichtig**, wenn sie während dieser Zeit erfolgt ([SR_220_OR_de.md Art. 340 Abs. 1 lit. b]).  
➡️ **Längere Krankheit (> 1 Monat im Dienstjahr)**: Kein genereller Kündigungsschutz durch die Sperrfristen – **Kündigung ist möglich**, vorausgesetzt, es liegt **kein anderes Recht** (z. B. Persönlicher Kündigungsschutz gem. Art. 336c) entgegen.

Zusätzlich gilt:  
➡️ Die **Kündigung wegen Krankheit allein** wäre **unzulässig**, wenn sie gegen den **allgemeinen Kündigungsschutz nach Art. 336c** verstösst, der eine personenbedingte Kündigung verbietet, wenn der Arbeitnehmer aufgrund von Krankheit für mindestens 30 Tage im Jahr (im ersten Dienstjahr) bzw. 90 Tage (später) arbeitsunfähig ist – **sofern nicht schwerwiegende betriebliche oder wirtschaftliche Gründe vorliegen**, die eine Kündigung rechtfertigen ([SR_220_OR_de.md Art. 336c]).

**Zusammenfassung:**  
- Kündigung während einer **kurzen Krankheit (≤ 1 Monat/Jahr)** ist **nichtig** ([SR_220_OR_de.md Art. 340 Abs. 1 lit. b]).  
- Kündigung während einer **langen Krankheit (> 1 Monat/Jahr)** ist **grundsätzlich möglich**, unterliegt aber dem **personenbedingten Kündigungsschutz (Art. 336c)** und dem Verbot der Diskriminierung ([SR_220_OR_de.md Art. 336c]).  
- Die **Kündigung darf nicht gegen öffentliche Ordnung** oder **unzulässige Beweggründe** erfolgen (z. B. Schwangerschaft: Art. 336c Abs. 2 lit. a).

### or-kuendigung-krankheit — semantic-vector

**Reference:** Nach Ablauf der Probezeit darf der Arbeitgeber bei einer unverschuldeten krankheitsbedingten vollständigen oder teilweisen Arbeitsverhinderung während der gesetzlichen Sperrfrist nicht kündigen: 30 Tage im ersten Dienstjahr, 90 Tage vom zweiten bis und mit fünften Dienstjahr und 180 Tage ab dem sechsten Dienstjahr. Eine während der Sperrfrist ausgesprochene Kündigung ist nichtig. Wurde vorher gekündigt und läuft die Kündigungsfrist in die Sperrfrist hinein, wird ihr Ablauf unterbrochen und danach fortgesetzt. Während der Probezeit gilt dieser Schutz nicht [SR_220_OR_de.md Art. 336c].

**Generated:** Ja, der Arbeitgeber darf während der Krankheit des Arbeitnehmers grundsätzlich kündigen – **aber mit Einschränkungen**, die sich aus dem Obligationenrecht ergeben.

Laut **Artikel 335b Absatz 1 SR_220_OR_de.md** darf das Arbeitsverhältnis während der Probezeit **jederzeit** mit einer Frist von sieben Tagen gekündigt werden, unabhängig davon, ob der Arbeitnehmer krank ist. Allerdings folgt aus **Artikel 335b Absatz 3** eine zwingende Verlängerung der Probezeit, wenn sie infolge von Krankheit effektiv verkürzt wird – dies zeigt, dass Krankheit den Kündigungsschutz nicht grundsätzlich ausschließt, sondern die probezeitbezogenen Regelungen beeinflusst.

Für das laufende Arbeitsverhältnis nach der Probezeit gilt hingegen allgemeiner Kündigungsschutz. **Krankheit allein begründet keinen besonderen Kündigungsschutz** im Sinne eines generellen Verbots, während Krankheit zu kündigen. Allerdings dürfen bei Krankheit gemäß **Artikel 328a Absatz 2** Leistungen wie Pflege und ärztliche Behandlung gewährt werden, ohne dass dies die Kündigungsfreiheit impliziert.

Ein echter **Kündigungsschutz bei Krankheit** ergibt sich erst aus **absoluten Schutzfristen**, wie etwa der Schwangerschaft (Art. 329b Abs. 3 lit. a SR_220_OR_de.md) oder dem Mutterschaftsurlaub (Art. 329b Abs. 3 lit. b SR_220_OR_de.md). Eine einfache Krankheit ist **nicht** Gegenstand eines solchen absoluten Schutzes.

Zusammenfassend:  
**Der Arbeitgeber darf während einer Krankheit kündigen, sofern keine spezifischen Schutzfristen (z. B. Schwangerschaft, Mutterschaft, Elternurlaub) greifen.** Die Kündigung muss jedoch weiterhin ordentlich und rechtlich zulässig erfolgen (z. B. keine missbräuchliche Kündigung gem. Art. 336c OR).

Quelle: [SR_220_OR_de.md Art. 335b], [SR_220_OR_de.md Art. 328a], [SR_220_OR_de.md Art. 329b].

### or-kuendigung-krankheit — rerank

**Reference:** Nach Ablauf der Probezeit darf der Arbeitgeber bei einer unverschuldeten krankheitsbedingten vollständigen oder teilweisen Arbeitsverhinderung während der gesetzlichen Sperrfrist nicht kündigen: 30 Tage im ersten Dienstjahr, 90 Tage vom zweiten bis und mit fünften Dienstjahr und 180 Tage ab dem sechsten Dienstjahr. Eine während der Sperrfrist ausgesprochene Kündigung ist nichtig. Wurde vorher gekündigt und läuft die Kündigungsfrist in die Sperrfrist hinein, wird ihr Ablauf unterbrochen und danach fortgesetzt. Während der Probezeit gilt dieser Schutz nicht [SR_220_OR_de.md Art. 336c].

**Generated:** Ja, **der Arbeitgeber darf während der Krankheit kündigen**, **aber nur unter strikten Voraussetzungen und zeitlich begrenzt**:

- **Während der Probezeit** (erster Monat) kann das Arbeitsverhältnis jederzeit mit einer Kündigungsfrist von sieben Tagen gekündigt werden – also **auch während Krankheit**, sofern keine abweichenden Vereinbarungen bestehen ([SR_220_OR_de.md Art. 335b Abs. 1]`.

- **Nach Ablauf der Probezeit** darf der Arbeitgeber das Arbeitsverhältnis **nicht kündigen**, **während** der Arbeitnehmer **ohne eigenes Verschulden durch Krankheit** oder Unfall **an der Arbeitsleistung verhindert ist**, und zwar:
  - **im ersten Dienstjahr während 30 Tagen**,
  - **ab zweitem bis und mit fünftem Dienstjahr während 90 Tagen**,
  - **ab sechstem Dienstjahr während 180 Tagen** ([SR_220_OR_de.md Art. 336c Abs. 1 Buchst. b]).

- Die Kündigung **während dieser Schutzfrist ist daher untersagt**. Sie ist rechtswidrig, wenn sie innerhalb dieser Fristen erfolgt, es sei denn, der Arbeitnehmer hat selbst versichert, dass er die Probezeit verlängern will oder künftig nicht mehr einsatzfähig ist – aber das ändert nichts an dem Schutz im Sinne von Art. 336c Abs. 1 lit. b.

Zusätzlich gilt: Ist die Verhinderung durch eigenes Verschulden (z. B. Selbstverschulden durch Alkoholkonsum), entsteht **kein Kündigungsschutz** nach Art. 336c Abs. 1 lit. b.

**Fazit:**  
Der Arbeitgeber darf während der Krankheit **nur innerhalb der Schutzfristen von Art. 336c Abs. 1 lit. b** **nicht kündigen**. Vor Ablauf der Probezeit ist eine Kündigung auch während Krankheit möglich (mit 7-Tages-Frist), nach Ablauf der Probezeit hängt die Zulässigkeit von der Dauer des Arbeitsverhältnisses und der Dauer der Krankheitsverhinderung ab.

### or-kuendigung-krankheit — graph

**Reference:** Nach Ablauf der Probezeit darf der Arbeitgeber bei einer unverschuldeten krankheitsbedingten vollständigen oder teilweisen Arbeitsverhinderung während der gesetzlichen Sperrfrist nicht kündigen: 30 Tage im ersten Dienstjahr, 90 Tage vom zweiten bis und mit fünften Dienstjahr und 180 Tage ab dem sechsten Dienstjahr. Eine während der Sperrfrist ausgesprochene Kündigung ist nichtig. Wurde vorher gekündigt und läuft die Kündigungsfrist in die Sperrfrist hinein, wird ihr Ablauf unterbrochen und danach fortgesetzt. Während der Probezeit gilt dieser Schutz nicht [SR_220_OR_de.md Art. 336c].

**Generated:** Ja, der Arbeitgeber darf während der Krankheit des Arbeitnehmers **unter bestimmten Voraussetzungen** kündigen, jedoch nicht uneingeschränkt.

Gemäss **Art. 336c Abs. 1 lit. b SR_220_OR_de.md** ist eine Kündigung während einer Krankheit **nicht zulässig**, soweit der Arbeitnehmer **ohne eigenes Verschulden** durch Krankheit an der Arbeitsleistung verhindert ist – und zwar:

- **im ersten Dienstjahr** während **30 Tagen**,  
- **ab dem zweiten bis zum fünften Dienstjahr** während **90 Tagen**,  
- **ab dem sechsten Dienstjahr** während **180 Tagen**.

Das heisst: Solange die Krankheit innerhalb dieser Fristen liegt und nicht durch eigenes Verschulden des Arbeitnehmers verursacht ist (z. B. Selbstverletzung, Alkoholmissbrauch), darf der Arbeitgeber **nicht kündigen**.

Außerhalb dieser Schutzfristen (z. B. nach Ablauf der 30/90/180-Tages-Frist) oder bei Vorliegen eines Verschuldens des Arbeitnehmers ist eine Kündigung grundsätzlich möglich, sofern keine weiteren Schutzvorschriften (z. B. nach dem Asylgesetz oder beim militärischen Dienst nach Art. 336c Abs. 1 lit. a) greifen.

Zusätzlich gilt: Sollte die Krankheit **länger als ein Monat** im Dienstjahr andauern und **durch Verschulden des Arbeitnehmers** verursacht sein, darf der Arbeitgeber gemäss **Art. 329b Abs. 1** die Ferien kürzen — dies betrifft aber nicht direkt das Kündigungsverbot.

👉 **Zusammenfassung:**  
Der Arbeitgeber darf während der Krankheit **nicht kündigen**, solange der Arbeitnehmer innerhalb der gesetzlichen Schutzfristen (30/90/180 Tage je nach Dienstjahreszahl) und **ohne eigenes Verschulden** arbeitsunfähig ist ([SR_220_OR_de.md Art. 336c Abs. 1 lit. b]).

### or-kaufvertrag-verjaehrung — fixed-vector

**Reference:** Für Forderungen aus einem Kaufvertrag gilt grundsätzlich die allgemeine Verjährungsfrist von zehn Jahren, sofern das Bundeszivilrecht für den konkreten Anspruch keine abweichende Frist vorsieht [SR_220_OR_de.md Art. 127].

**Generated:** Forderungen aus einem Kaufvertrag verjähren nach dem Schweizerischen Obligationenrecht grundsätzlich mit Ablauf von **zehn Jahren**, sofern das Bundeszivilrecht nichts anderes bestimmt ([SR_220_OR_de.md Art. 127]).

Zusätzlich ist zu beachten:  
- Für Mängel einer Sache, die bestimmungsgemäss in ein unbewegliches Werk integriert worden ist und diese Mangelhaftigkeit das Werk verursacht hat, beträgt die Verjährungsfrist **fünf Jahre** ([SR_220_OR_de.md Art. 127 Abs. 2]).  
- Für Kulturgüter (gemäss Kulturgütertransfergesetz) verjährt die Klage **ein Jahr** nach Entdeckung des Mangels, **jedoch spätestens 30 Jahre** nach Vertragsabschluss ([SR_220_OR_de.md Art. 127 Abs. 3]).  

Hinweis: Die allgemeine Verjährungsfrist für die Hauptforderung (z. B. Zahlungsanspruch des Verkäufers) bleibt zehn Jahre, während die Gewährleistungs- oder Mangelbeseitigungsansprüche (insbesondere bei beweglichen Sachen) gemäss § 2 des Kaufrechts (Art. 197 ff. OR) normalerweise **12 Monate** nach Übergabe der Sache verjähren – dies ist jedoch nicht im gegebenen Kontext enthalten und müsste aus anderen Teilen des OR ergänzt werden. Da die Frage jedoch ausschliesslich anhand des bereitgestellten Kontextes beantwortet werden soll, gilt gemäss [SR_220_OR_de.md Art. 127] die allgemeine Frist von zehn Jahren.

### or-kaufvertrag-verjaehrung — semantic-vector

**Reference:** Für Forderungen aus einem Kaufvertrag gilt grundsätzlich die allgemeine Verjährungsfrist von zehn Jahren, sofern das Bundeszivilrecht für den konkreten Anspruch keine abweichende Frist vorsieht [SR_220_OR_de.md Art. 127].

**Generated:** Forderungen aus einem Kaufvertrag verjähren **mit Ablauf von zwei Jahren nach deren Ablieferung an den Käufer**, sofern nicht der Verkäufer eine Haftung auf längere Zeit übernommen hat. Dies gilt insbesondere für **Klagen auf Gewährleistung wegen Mängel der Sache** [SR_220_OR_de.md Art. 21075].  

Zusätzlich gelten bei **Bauleistungen** unterschiedliche Verjährungsfristen:  
- Bei **beweglichen Werken**, die in unbewegliches Werk integriert sind, beträgt die Verjährungsfrist für Mängelansprüche des Bestellers **fünf Jahre** [SR_220_OR_de.md Art. 371260 Abs. 1].  
- Bei **unbeweglichen Werken** verjähren Mängelansprüche des Bestellers gegen den Unternehmer sowie gegen Architekten oder Ingenieure **mit Ablauf von fünf Jahren seit der Abnahme des Werkes** [SR_220_OR_de.md Art. 371260 Abs. 2].  

Zu anderen Forderungen aus dem Kaufvertrag (z. B. Schadenersatz, nicht gewährleistungsrechtlich) können weitere Verjährungsfristen gelten, etwa die allgemeine Verjährungsfrist von drei Jahren bei Schadenersatzansprüchen aus vertragswidriger Körperverletzung (Art. 128a), jedoch nicht für den regulären Kaufpreis oder Gewährleistungsanspruch.

### or-kaufvertrag-verjaehrung — rerank

**Reference:** Für Forderungen aus einem Kaufvertrag gilt grundsätzlich die allgemeine Verjährungsfrist von zehn Jahren, sofern das Bundeszivilrecht für den konkreten Anspruch keine abweichende Frist vorsieht [SR_220_OR_de.md Art. 127].

**Generated:** Die Verjährungsfrist für Forderungen aus einem Kaufvertrag richtet sich nach dem Vertragsgegenstand (bewegliche Sache, unbewegliche Sache) sowie nach der Art der Forderung (z. B. Kaufpreis, Mangelbeseitigung, Schadenersatz).

Folgende Rechtsvorschriften finden Anwendung:

- Für Forderungen aus einem **Kaufvertrag über bewegliche Sachen** (z. B. Kaufpreisforderung, Rückgewähranspruch bei Mangel) gilt die **allgemeine Verjährungsfrist von zehn Jahren**, sofern nicht eine spezielle Vorschrift kürzere Fristen vorsieht [SR_220_OR_de.md Art. 127].

- Für **Ansprüche wegen Mängel des Werkes** (etwa bei Werkverträgen, die Kaufverträgen nahestehen) gelten spezielle Fristen:
  - Bei einem **beweglichen Werk**, das bestimmungsgemäss in ein unbewegliches Werk integriert worden ist, beträgt die Verjährungsfrist **fünf Jahre**, soweit dessen Mangelhaftigkeit die Mangelhaftigkeit des unbeweglichen Werkes verursacht [SR_220_OR_de.md Art. 371 Abs. 1 Satz 2].
  - Bei einem **unbeweglichen Werk** verjähren die Ansprüche des Bestellers **nach fünf Jahren seit der Abnahme des Werkes** [SR_220_OR_de.md Art. 371 Abs. 2].
  - Diese Fristen können nicht zu Lasten des Bestellers verkürzt werden [SR_220_OR_de.md Art. 371 Abs. 3].

- Forderungen aus **Kaufverträgen über bewegliche Sachen**, soweit sie nicht unter spezielle Verjährungsregelungen fallen, unterliegen nach der Rechtsprechung und Literatur üblicherweise der **allgemeinen Verjährungsfrist von drei Jahren** nach dem Schadenseintritt bei mangelfreiem Lieferungsanspruch – **sofern sie aus einer vertragswidrigen Leistung (z. B. Lieferung einer mangelfhaften Sache) resultieren** [SR_220_OR_de.md Art. 128a].

- **Periodische Leistungen** wie etwa Ratenzahlungen aus einem Kaufvertrag verjähren **nach fünf Jahren** [SR_220_OR_de.md Art. 128 Abs. 1 Ziff. 1].

Zusammenfassend hängt die Verjährungsfrist von der **Natur der Forderung** ab:

- Kaufpreisforderung (einfache Forderung, nicht periodisch): **10 Jahre** (allgemeine Verjährung, Art. 127 OR), es sei denn, sie fällt unter eine speziell kürzere Frist.
- Mängelansprüche (Werkverträge): **2–5 Jahre**, je nach Art des Werkes [Art. 371 OR].
- Periodische Zahlungen (z. B. Raten): **5 Jahre** [Art. 128 Abs. 1 Ziff. 1].
- Schadenersatz infolge mangelfhafter Lieferung: **3 Jahre ab Kenntnis vom Schaden, spätestens 20 Jahre ab Vertragsverletzung** [Art. 128a].

Ohne weitere Angaben zum konkreten Forderungstyp aus dem Kaufvertrag lässt sich keine einheitliche Frist nennen.

### or-kaufvertrag-verjaehrung — graph

**Reference:** Für Forderungen aus einem Kaufvertrag gilt grundsätzlich die allgemeine Verjährungsfrist von zehn Jahren, sofern das Bundeszivilrecht für den konkreten Anspruch keine abweichende Frist vorsieht [SR_220_OR_de.md Art. 127].

**Generated:** Forderungen aus einem Kaufvertrag verjähren grundsätzlich nach zwei Jahren seit Ablieferung der Sache an den Käufer, unabhängig davon, ob der Käufer die Mängel später entdeckt hat – es sei denn, der Verkäufer hat eine längere Haftung übernommen [SR_220_OR_de.md Art. 21075].

Zusätzlich gilt:  
- Allgemeine Forderungen (z. B. Zahlungsansprüche) verjähren nach fünf Jahren [SR_220_OR_de.md Art. 128].  
- Ansprüche des Eigentümers wegen Veränderung oder Wertverminderung sowie Ansprüche des Nutzniessers auf Ersatz von Verwendungen oder Wegnahme von Vorrichtungen verjähren mit Ablauf eines Jahres seit der Rückleistung der Sache [SR_210_ZGB_de.md Art. 754].

### bgg-beschwerdefrist — fixed-vector

**Reference:** Grundsätzlich ist die Beschwerde gegen einen Entscheid innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen. Artikel 100 BGG sieht für bestimmte Fälle kürzere Fristen von zehn, fünf oder drei Tagen vor; gegen das unrechtmässige Verweigern oder Verzögern eines Entscheids kann jederzeit Beschwerde geführt werden [SR_173.110_BGG_de.md Art. 100].

**Generated:** Für eine Beschwerde ans Bundesgericht gilt grundsätzlich eine Frist von **30 Tagen** nach Eröffnung der vollständigen Ausfertigung des Entscheids oder nach Zustellung des begründeten Entscheids.

Konkret ergibt sich dies aus folgenden Quellen:

- Nach **[SR_173.110_BGG_de.md Art. 100 Abs. 1]**:  
  *„Die Beschwerde gegen einen Entscheid ist innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen.“*

- Nach **[SR_272_ZPO_de.md Art. 321 Abs. 1]**:  
  *„Die Beschwerde ist bei der Rechtsmittelinstanz innert 30 Tagen seit der Zustellung des begründeten Entscheides oder seit der nachträglichen Zustellung der Entscheidbegründung (Art. 239) schriftlich und begründet einzureichen.“*

Zusätzlich gibt es jedoch Ausnahmen mit verkürzten Fristen, z. B.:

- **10 Tage** bei Entscheiden kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen ([SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. a], [SR_272_ZPO_de.md Art. 321 Abs. 2])  
- **5 Tage** bei bestimmten Entscheiden im Wechselbetreibungsverfahren oder bei Beschwerden gegen eidgenössische Abstimmungen ([SR_173.110_BGG_de.md Art. 100 Abs. 3])  
- **3 Tage** bei Beschwerden gegen Nationalratswahlen ([SR_173.110_BGG_de.md Art. 100 Abs. 4])

Weiterhin gelten bei Beschwerden gegen **Erlasse** 30 Tage seit Veröffentlichung ([SR_173.110_BGG_de.md Art. 101]).

Für beschleunigte Verfahren im Asylwesen gelten z. B. 7 Arbeitstage oder 30 Tage, je nach Verfahrensart ([SR_142.31_AsylG_de.md Art. 108 Abs. 1]).

Zusammengefasst lautet die allgemeine Regel: **30 Tage**, es sei denn, das Gesetz sieht eine speziell verkürzte Frist vor.

### bgg-beschwerdefrist — semantic-vector

**Reference:** Grundsätzlich ist die Beschwerde gegen einen Entscheid innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen. Artikel 100 BGG sieht für bestimmte Fälle kürzere Fristen von zehn, fünf oder drei Tagen vor; gegen das unrechtmässige Verweigern oder Verzögern eines Entscheids kann jederzeit Beschwerde geführt werden [SR_173.110_BGG_de.md Art. 100].

**Generated:** Die allgemeine Frist für eine Beschwerde ans Bundesgericht beträgt **30 Tage**, und zwar nach der Eröffnung der vollständigen Ausfertigung des Entscheids [SR_173.110_BGG_de.md Art. 100 Abs. 1].

Zusätzlich gibt es spezielle, kürzere Fristen für bestimmte Entscheide:

- **10 Tage** bei Entscheiden der kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen sowie bei Entscheiden in den Bereichen internationale Rechtshilfe in Strafsachen, internationale Amtshilfe in Steuersachen und Rückgabe eines Kindes nach dem Europäischen Übereinkommen vom 20. Mai 1980 [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. a–c].

- **5 Tage** bei Entscheiden der kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen *im Rahmen der Wechselbetreibung* sowie bei Entscheiden der Kantonsregierungen über Beschwerden gegen eidgenössische Abstimmungen [SR_173.110_BGG_de.md Art. 101 Abs. 3 lit. a–b].

- **3 Tage** bei Entscheiden der Kantonsregierungen über Beschwerden gegen die Nationalratswahlen [SR_173.110_BGG_de.md Art. 101 Abs. 4].

Zudem gilt für Beschwerden gegen Erlass: **30 Tage** nach der massgebenden Veröffentlichung [SR_173.110_BGG_de.md Art. 101].

In Asylsachen gelten abweichende Fristen (z. B. 7 Arbeitstage im beschleunigten Verfahren, 30 Tage im erweiterten Verfahren) [SR_142.31_AsylG_de.md Art. 108].

### bgg-beschwerdefrist — rerank

**Reference:** Grundsätzlich ist die Beschwerde gegen einen Entscheid innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen. Artikel 100 BGG sieht für bestimmte Fälle kürzere Fristen von zehn, fünf oder drei Tagen vor; gegen das unrechtmässige Verweigern oder Verzögern eines Entscheids kann jederzeit Beschwerde geführt werden [SR_173.110_BGG_de.md Art. 100].

**Generated:** Die allgemeine Beschwerdefrist beim Bundesgericht beträgt **30 Tage** nach der Eröffnung der vollständigen Ausfertigung des Entscheids [SR_173.110_BGG_de.md Art. 100 Abs. 1].

Zusätzlich gibt es verkürzte Fristen für bestimmte Entscheide:

- **10 Tage** bei:
  - Entscheiden der kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. a];
  - Entscheiden im Bereich der internationalen Rechtshilfe in Strafsachen und der internationalen Amtshilfe in Steuersachen [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. b];
  - Entscheiden über die Rückgabe eines Kindes nach dem Europäischen Übereinkommen vom 20. Mai 1980 (Hague Child Abduction Convention) sowie über die Anerkennung und Vollstreckung von Entscheidungen über das Sorgerecht für Kinder [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. c];
  - Entscheiden des Bundespatentgerichts über die Erteilung einer Lizenz nach Artikel 40d des Patentgesetzes [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. d].

- **5 Tage** bei:
  - Entscheiden der kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen im Rahmen der Wechselbetreibung [SR_173.110_BGG_de.md Art. 100 Abs. 3 lit. a];
  - Entscheiden der Kantonsregierungen über Beschwerden gegen eidgenössische Abstimmungen [SR_173.110_BGG_de.md Art. 100 Abs. 3 lit. b].

- **3 Tage** bei Entscheiden der Kantonsregierungen über Beschwerden gegen die Nationalratswahlen [SR_173.110_BGG_de.md Art. 100 Abs. 4].

Ferner beträgt die Frist für eine **Beschwerde gegen einen Erlass** 30 Tage nach der nach kantonalem Recht massgebenden Veröffentlichung des Erlasses [SR_173.110_BGG_de.md Art. 101].

Hinzu kommen spezielle Fristen für **Revisionsgesuche**, z. B. 30 Tage nach Eröffnung des Entscheids bei Verletzung von Verfahrensvorschriften oder 90 Tage nach der endgültigen Entscheidung des Europäischen Gerichtshofs für Menschenrechte bei EMRK-Verletzung [SR_173.110_BGG_de.md Art. 124].

In Fällen, in denen die Einsprache ausgeschlossen ist, gilt gemäss SR_830.1_ATSG_de.md Art. 60 Abs. 1 eine Beschwerdefrist von 30 Tagen nach der Eröffnung des Einspracheentscheides oder der Verfügung.

### bgg-beschwerdefrist — graph

**Reference:** Grundsätzlich ist die Beschwerde gegen einen Entscheid innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen. Artikel 100 BGG sieht für bestimmte Fälle kürzere Fristen von zehn, fünf oder drei Tagen vor; gegen das unrechtmässige Verweigern oder Verzögern eines Entscheids kann jederzeit Beschwerde geführt werden [SR_173.110_BGG_de.md Art. 100].

**Generated:** Die allgemeine Beschwerdefrist beim Bundesgericht beträgt **30 Tage**, und zwar nach der Eröffnung der vollständigen Ausfertigung des Entscheids [SR_173.110_BGG_de.md Art. 100 Abs. 1].

Es bestehen jedoch besondere, kürzere Fristen für bestimmte Entscheide:

- **10 Tage** bei Entscheiden der kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen sowie bei Entscheiden auf den Gebieten der internationalen Rechtshilfe in Strafsachen und der internationalen Amtshilfe in Steuersachen und bei Entscheiden über die Rückgabe eines Kindes nach dem Europäischen Übereinkommen vom 20. Mai 1980 über die Anerkennung und Vollstreckung von Entscheidungen über das Sorgerecht für Kinder [SR_173.110_BGG_de.md Art. 100 Abs. 2 lit. a–c].

- **5 Tage** bei Entscheiden der kantonalen Aufsichtsbehörden in Schuldbetreibungs- und Konkurssachen im Rahmen der Wechselbetreibung sowie bei Entscheiden der Kantonsregierungen über Beschwerden gegen eidgenössische Abstimmungen [SR_173.110_BGG_de.md Art. 100 Abs. 3 lit. a–b].

- **3 Tage** bei Entscheiden der Kantonsregierungen über Beschwerden gegen die Nationalratswahlen [SR_173.110_BGG_de.md Art. 100 Abs. 4].

Weitere Fristen gelten für Revisionsgesuche (z. B. 30 oder 90 Tage, je nach Grund) [SR_173.110_BGG_de.md Art. 124].

### or-probezeit — fixed-vector

**Reference:** Als Probezeit gilt grundsätzlich der erste Monat des Arbeitsverhältnisses. Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann davon abgewichen werden; die Probezeit darf jedoch höchstens drei Monate dauern. Während der Probezeit gilt eine Kündigungsfrist von sieben Tagen [SR_220_OR_de.md Art. 335b].

**Generated:** Im Arbeitsverhältnis beträgt die Probezeit gemäss Art. 335c Abs. 2 SR_220_OR_de.md **höchstens drei Monate**.  

Zusätzlich ergibt sich aus Art. 335c Abs. 1 SR_220_OR_de.md, dass der **erste Monat eines Arbeitsverhältnisses als Probezeit gilt**, es sei denn, es werden durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag abweichende Vereinbarungen getroffen – wobei die Probezeit **nicht länger als drei Monate** sein darf [SR_220_OR_de.md Art. 335c].  

Für **Lehrverhältnisse** gilt nach Art. 344a Abs. 3 SR_220_OR_de.md: Die Probezeit darf **nicht weniger als einen Monat und nicht mehr als drei Monate** betragen; fehlt eine Festlegung, gilt automatisch eine Probezeit von drei Monaten [SR_220_OR_de.md Art. 344a].

### or-probezeit — semantic-vector

**Reference:** Als Probezeit gilt grundsätzlich der erste Monat des Arbeitsverhältnisses. Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann davon abgewichen werden; die Probezeit darf jedoch höchstens drei Monate dauern. Während der Probezeit gilt eine Kündigungsfrist von sieben Tagen [SR_220_OR_de.md Art. 335b].

**Generated:** Die Dauer der Probezeit im Arbeitsverhältnis richtet sich nach dem Allgemeinen Teil des Schweizerischen Obligationenrechts (SR 220 OR):

- **Grundregel**: Der erste Monat eines Arbeitsverhältnisses gilt als Probezeit [SR_220_OR_de.md Art. 335b Abs. 1].

- **Verlängerung möglich**: Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann die Probezeit **auf höchstens drei Monate** verlängert werden [SR_220_OR_de.md Art. 335b Abs. 2].

- **Verkürzung im Einzelfall**: Wird die Probezeit durch Krankheit, Unfall oder Erfüllung einer nicht freiwillig übernommenen gesetzlichen Pflicht effektiv verkürzt, so erfolgt eine entsprechende Verlängerung [SR_220_OR_de.md Art. 335b Abs. 3].

Zusätzlich gilt für **Lehrverhältnisse** (Berufsbildung):
- Die Probezeit darf **nicht weniger als einen Monat und nicht mehr als drei Monate** betragen; fehlt eine Vereinbarung, gelten drei Monate als vereinbart [SR_220_OR_de.md Art. 344a Abs. 3].
- Eine Verlängerung bis zu sechs Monaten ist ausnahmsweise nur mit Zustimmung der kantonalen Behörde möglich [SR_220_OR_de.md Art. 344a Abs. 4].

Für **Heimarbeitnehmer**:
- Wird einer Probearbeit übergeben, gilt das Arbeitsverhältnis zur Probe, sofern nichts anderes vereinbart ist [SR_220_OR_de.md Art. 354 Abs. 1].

**Zusammenfassung**: Die gesetzliche Mindestprobezeit beträgt **einen Monat**, die maximal zulässige Dauer beträgt **drei Monate** (bzw. sechs Monate im Lehrverhältnis mit behördlicher Genehmigung).

### or-probezeit — rerank

**Reference:** Als Probezeit gilt grundsätzlich der erste Monat des Arbeitsverhältnisses. Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann davon abgewichen werden; die Probezeit darf jedoch höchstens drei Monate dauern. Während der Probezeit gilt eine Kündigungsfrist von sieben Tagen [SR_220_OR_de.md Art. 335b].

**Generated:** Die Dauer der Probezeit im Arbeitsverhältnis richtet sich nach dem allgemeinen Arbeitsverhältnis gemäss dem Schweizerischen Obligationenrecht (OR):

- Nach **Art. 335b Abs. 1 OR** gilt **der erste Monat eines Arbeitsverhältnisses** als Probezeit [SR_220_OR_de.md Art. 335b].

- Laut **Art. 335b Abs. 2 OR** kann die Probezeit **durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag auf höchstens drei Monate verlängert** werden; eine Verlängerung über drei Monate hinaus ist nicht zulässig [SR_220_OR_de.md Art. 335b].

- Bei einer **effektiven Verkürzung der Probezeit** infolge Krankheit, Unfall oder Erfüllung einer nicht freiwillig übernommenen gesetzlichen Pflicht erfolgt eine **entprechende Verlängerung** [SR_220_OR_de.md Art. 335b Abs. 3].

Zusätzlich gilt für **Lehrverhältnisse** gesondert nach **Art. 344a Abs. 3 OR**, dass die Probezeit **nicht weniger als einen Monat und nicht mehr als drei Monate** betragen darf; fehlt eine Festlegung im Vertrag, gilt automatisch eine Probezeit von **drei Monaten** [SR_220_OR_de.md Art. 344a].

**Zusammenfassung**:  
Die reguläre Probezeit im Arbeitsverhältnis beträgt **mindestens einen Monat**, höchstens **drei Monate**, sofern nicht eine kürzere, vereinbarte oder gesetzlich bedingte Verlängerung/Verkürzung eintritt.

### or-probezeit — graph

**Reference:** Als Probezeit gilt grundsätzlich der erste Monat des Arbeitsverhältnisses. Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann davon abgewichen werden; die Probezeit darf jedoch höchstens drei Monate dauern. Während der Probezeit gilt eine Kündigungsfrist von sieben Tagen [SR_220_OR_de.md Art. 335b].

**Generated:** Die Probezeit im Arbeitsverhältnis beträgt **grundsätzlich den ersten Monat** des Arbeitsverhältnisses ([SR_220_OR_de.md Art. 335b Abs. 1](SR_220_OR_de.md Art. 335b)).  

Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann sie **höchstens auf drei Monate verlängert** werden ([SR_220_OR_de.md Art. 335b Abs. 2](SR_220_OR_de.md Art. 335b)).  

Bei einer effektiven Verkürzung der Probezeit infolge Krankheit, Unfall oder Erfüllung einer nicht freiwillig übernommenen gesetzlichen Pflicht erfolgt eine entsprechende Verlängerung ([SR_220_OR_de.md Art. 335b Abs. 3](SR_220_OR_de.md Art. 335b)).  

Im **Lehrverhältnis** gilt analog: Die Probezeit beträgt mindestens einen Monat und höchstens drei Monate; fehlt eine Vereinbarung, so gilt eine Probezeit von drei Monaten ([SR_220_OR_de.md Art. 344a Abs. 3](SR_220_OR_de.md Art. 344a)).

### dsg-einwilligung-widerruf — fixed-vector

**Reference:** Das DSG formuliert in den vorliegenden Artikeln kein eigenständiges allgemeines Widerrufsrecht. Es verlangt aber eine freiwillige und informierte Einwilligung [SR_235.1_DSG_de.md Art. 6], behandelt eine Bearbeitung entgegen der ausdrücklichen Willenserklärung als Persönlichkeitsverletzung [SR_235.1_DSG_de.md Art. 30] und nennt die Einwilligung nur als einen möglichen Rechtfertigungsgrund [SR_235.1_DSG_de.md Art. 31]. Wird sie für die Zukunft widerrufen, kann die Bearbeitung daher nicht mehr auf diese Einwilligung gestützt werden; ein anderer Rechtfertigungsgrund kann sie dennoch erlauben. Betroffene können insbesondere das Verbot einer Bearbeitung sowie gegebenenfalls Löschung oder Vernichtung verlangen [SR_235.1_DSG_de.md Art. 32].

**Generated:** Ja, eine Einwilligung zur Datenbearbeitung kann widerrufen werden.  

Die Datenverarbeitungsverordnung (DSG) sieht ausdrücklich vor, dass die Einwilligung widerrufbar ist. Dies folgt implizit aus Art. 8 Abs. 2 DSG, wonach die Einwilligung „nur gültig ist, wenn sie … freiwillig erteilt wird“ – ein Widerruf ist somit möglich, solange keine gesetzliche Verpflichtung zur Datenverarbeitung besteht (vgl. Art. 4 DSG).  

Zudem ergibt sich aus dem allgemeinen Datenschutzgrundsatz der **Rückabwicklungsmöglichkeit bei widerruflicher Einwilligung**, wie sie in ähnlichen Rechtsordnungen (z. B. EU-DSGVO) ausdrücklich geregelt ist. In der Schweizer DSG ist dies zwar nicht ausdrücklich benannt, aber die Rechtsprechung und Lehre anerkennt den Widerruf als Folge der **freiwilligen** Natur der Einwilligung gem. Art. 8 Abs. 2 lit. c DSG [SR_235.1_DSG_de.md Art. 8].

Falls die Einwilligung aber **nicht** die einzige Rechtsgrundlage für die Datenverarbeitung ist (z. B. wenn eine gesetzliche Verpflichtung oder ein überwiegendes legitimes Interesse besteht), ist ein Widerruf möglicherweise nicht wirksam.

> **Zusammenfassung**:  
> - Eine Einwilligung gem. Art. 8 Abs. 2 DSG ist **widerrufbar**, da sie freiwillig erteilt werden muss.  
> - Ein Widerruf hat aber keine retroaktive Wirkung; bereits erfolgte Bearbeitungen bleiben rechtslich wirksam.  
> - Die Verarbeitung muss nach Widerruf eingestellt werden, es sei denn, eine andere Rechtsgrundlage (z. B. gesetzliche Verpflichtung) gilt.

Quelle: [SR_235.1_DSG_de.md Art. 8 Abs. 2 lit. c]

### dsg-einwilligung-widerruf — semantic-vector

**Reference:** Das DSG formuliert in den vorliegenden Artikeln kein eigenständiges allgemeines Widerrufsrecht. Es verlangt aber eine freiwillige und informierte Einwilligung [SR_235.1_DSG_de.md Art. 6], behandelt eine Bearbeitung entgegen der ausdrücklichen Willenserklärung als Persönlichkeitsverletzung [SR_235.1_DSG_de.md Art. 30] und nennt die Einwilligung nur als einen möglichen Rechtfertigungsgrund [SR_235.1_DSG_de.md Art. 31]. Wird sie für die Zukunft widerrufen, kann die Bearbeitung daher nicht mehr auf diese Einwilligung gestützt werden; ein anderer Rechtfertigungsgrund kann sie dennoch erlauben. Betroffene können insbesondere das Verbot einer Bearbeitung sowie gegebenenfalls Löschung oder Vernichtung verlangen [SR_235.1_DSG_de.md Art. 32].

**Generated:** Ja, eine Einwilligung zur Datenbearbeitung kann widerrufen werden. Die Datenschutzgesetzgebung sieht ausdrücklich vor, dass die Einwilligung widerrufbar ist – dies folgt aus dem allgemeinen Grundsatz der freiwilligen und jederzeit widerrufbaren Einwilligung nach Art. 4 Abs. 1 DSG (Datenschutzgesetz), wenn auch der konkrete Widerruf im vorliegenden Kontext nicht direkt zitiert wird.

Allerdings ist in den vorliegenden Auszügen keine direkte Regelung zum Widerruf der Einwilligung enthalten. Es heisst lediglich:

> „Die Einwilligung muss ausdrücklich erfolgen für: a. die Bearbeitung von besonders schützenswerten Personendaten; b. ein Profiling mit hohem Risiko durch eine private Person; oder c. ein Profiling durch ein Bundesorgan.“  
[SR_235.1_DSG_de.md Art. 15 Abs. 7]

Und:

> „Die Einwilligung ist nur gültig, wenn sie … **freiwillig** erteilt wird.“  
[SR_235.1_DSG_de.md Art. 15 Abs. 6]

Ein freiwillig erteiltes Rechtsgeschäft – wie die Einwilligung – ist nach allgemeinem Rechtsgrundsatz (und im schweizerischen Datenschutzrecht ausdrücklich) widerrufbar, solange die Datenbearbeitung noch nicht rechtskräftig abgeschlossen ist. Zudem sehen die Vorschriften über die Rechte der betroffenen Person (z. B. Berichtigung, Löschung, Einschränkung der Bearbeitung) implizit einen Widerruf vor – etwa wenn die Bearbeitung widerrechtlich ist und beseitigt werden muss [SR_235.1_DSG_de.md Art. 41 Abs. 1 lit. a–c].

Zusätzlich ermöglicht das Gesetz, dass bei Unrichtigkeit der Daten eine Berichtigung oder Löschung verlangt werden kann, was wiederum eine Wirkung auf die Einwilligung haben kann [SR_235.1_DSG_de.md Art. 41 Abs. 2 lit. a].

**Fazit:** Ja, eine Einwilligung zur Datenbearbeitung kann widerrufen werden, da sie nach dem Datenschutzgesetz freiwillig erteilt werden muss (Art. 15 Abs. 6 DSG), und freiwillige Willenserklärungen sind nach Schweizer Recht grundsätzlich widerruflich. Konkrete Verfahrensdetails ergeben sich aus den allgemeinen Rechten der betroffenen Person (Art. 41 DSG).

### dsg-einwilligung-widerruf — rerank

**Reference:** Das DSG formuliert in den vorliegenden Artikeln kein eigenständiges allgemeines Widerrufsrecht. Es verlangt aber eine freiwillige und informierte Einwilligung [SR_235.1_DSG_de.md Art. 6], behandelt eine Bearbeitung entgegen der ausdrücklichen Willenserklärung als Persönlichkeitsverletzung [SR_235.1_DSG_de.md Art. 30] und nennt die Einwilligung nur als einen möglichen Rechtfertigungsgrund [SR_235.1_DSG_de.md Art. 31]. Wird sie für die Zukunft widerrufen, kann die Bearbeitung daher nicht mehr auf diese Einwilligung gestützt werden; ein anderer Rechtfertigungsgrund kann sie dennoch erlauben. Betroffene können insbesondere das Verbot einer Bearbeitung sowie gegebenenfalls Löschung oder Vernichtung verlangen [SR_235.1_DSG_de.md Art. 32].

**Generated:** Ja, eine Einwilligung zur Datenbearbeitung kann widerrufen werden.  

Laut der Rechtsprechung und dem Schweizer Datenschutzrecht ist die Einwilligung grundsätzlich freiwillig und kann daher jederzeit widerrufen werden. Dies ergibt sich aus dem Grundsatz der Freiwilligkeit der Einwilligung (vgl. Art. 4 DSGVO i.V.m. Art. 7 Abs. 3 DSGVO), der auch in der Schweizer Rechtsordnung anerkannt ist, soweit nicht spezifisch abweichende Vorschriften bestehen.

Im vorliegenden Kontext wird die Gültigkeit der Einwilligung in Art. 6 lit. a SR_235.1_DSG_de.md (Datenschutzgesetz, DSG) geregelt:

> **[SR_235.1_DSG_de.md Art. 6]**  
> Die Einwilligung der betroffenen Person ist nur gültig, wenn sie für eine oder mehrere bestimmte Bearbeitungen nach angemessener Information **freiwillig** erteilt wird.

Da die Einwilligung freiwillig sein muss, folgt logisch, dass sie auch jederzeit widerrufen werden kann — ein widerrufsberechtigter Widerruf ist ein wesentlicher Bestandteil der Freiwilligkeit.

Zusätzlich wird in **Art. 31 DSG** formuliert:

> **[SR_235.1_DSG_de.md Art. 31]**  
> Eine Persönlichkeitsverletzung ist widerrechtlich, wenn sie nicht durch **Einwilligung der betroffenen Person**, durch ein überwiegendes privates oder öffentliches Interesse oder durch Gesetz gerechtfertigt ist.

Daraus folgt: Wenn die Einwilligung widerrufen wird, entfällt eine mögliche Rechtfertigungslücke für die weitere Datenverarbeitung — es sei denn, ein anderer Rechtfertigungsgrund (z. B. Vertragsdurchführung gem. Art. 31 Abs. 2 lit. a DSG, oder gesetzliche Verpflichtung) tritt stattdessen in Kraft.

**Zusammenfassung:**  
Ja, Sie können eine Einwilligung zur Datenbearbeitung widerrufen. Der Widerruf ist wirksam, sobald er beim Verantwortlichen eingegangen ist ([SR_235.1_DSG_de.md Art. 6], Art. 31). Nach dem Widerruf ist die weitere Verarbeitung unless ein anderer Rechtfertigungsgrund vorliegt.

Hinweis: Im vorliegenden Kontext ist kein widerrufsspezifischer Text wiedergegeben. Die Angabe bezieht sich auf allgemeine rechtliche Prinzipien, die in der Rechtsprechung und Auslegung des DSG anerkannt sind.

### dsg-einwilligung-widerruf — graph

**Reference:** Das DSG formuliert in den vorliegenden Artikeln kein eigenständiges allgemeines Widerrufsrecht. Es verlangt aber eine freiwillige und informierte Einwilligung [SR_235.1_DSG_de.md Art. 6], behandelt eine Bearbeitung entgegen der ausdrücklichen Willenserklärung als Persönlichkeitsverletzung [SR_235.1_DSG_de.md Art. 30] und nennt die Einwilligung nur als einen möglichen Rechtfertigungsgrund [SR_235.1_DSG_de.md Art. 31]. Wird sie für die Zukunft widerrufen, kann die Bearbeitung daher nicht mehr auf diese Einwilligung gestützt werden; ein anderer Rechtfertigungsgrund kann sie dennoch erlauben. Betroffene können insbesondere das Verbot einer Bearbeitung sowie gegebenenfalls Löschung oder Vernichtung verlangen [SR_235.1_DSG_de.md Art. 32].

**Generated:** Ja, eine Einwilligung zur Datenbearbeitung kann widerrufen werden. Die Datenschutzverordnung (DSG) sieht hierfür ausdrücklich vor:  

> „Die Einwilligung kann jederzeit mit Wirkung für die Zukunft widerrufen werden.“  

Diese Regelung ist in der **DSG** verankert, konkret in **[SR_235.1_DSG_de.md Art. 15 Abs. 2]**, wonach:

> „Die betroffene Person kann ihre Einwilligung jederzeit mit Wirkung für die Zukunft widerrufen. Der Widerruf berührt nicht die Rechtmäßigkeit der bis zum Widerruf erfolgten Bearbeitung.“  

Zudem ergibt sich aus **[SR_235.1_DSG_de.md Art. 15 Abs. 1]**, dass die Einwilligung freiwillig, für spezifische Bearbeitungszwecke und nach angemessener Information erteilt werden muss – was impliziert, dass sie auch wieder freiwillig und jederzeit rückabwickelbar sein muss.  

**Kurz zusammengefasst:**  
✅ Einwilligungen können jederzeit widerrufen werden.  
✅ Der Widerruf wirkt nur *für die Zukunft* (rückwirkungslos).  
✅ Bereits rechtmäßig durchgeführte Bearbeitungen bleiben dadurch unberührt.

### or-artikel-1 — fixed-vector

**Reference:** Zum Abschluss eines Vertrags ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich. Diese Willensäusserung kann ausdrücklich oder stillschweigend erfolgen [SR_220_OR_de.md Art. 1].

**Generated:** In Artikel 1 des Schweizerischen Obligationenrechts (OR) steht:

> **Art. 1**  
> **1** Zum Abschlusse eines Vertrages ist die übereinstimmende gegen seitige Willensäusserung der Parteien erforderlich.  
> **2** Sie kann eine ausdrückliche oder stillschweigende sein.  

[SR_220_OR_de.md Art. 1]

### or-artikel-1 — semantic-vector

**Reference:** Zum Abschluss eines Vertrags ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich. Diese Willensäusserung kann ausdrücklich oder stillschweigend erfolgen [SR_220_OR_de.md Art. 1].

**Generated:** Im gegebenen Kontext ist **kein Inhalt von Artikel 1 des OR** (Schweizerisches Obligationenrecht) enthalten.

Die bereitgestellten Ausschnitte enthalten lediglich:

- eine allgemeine Einleitung zum OR mit Hinweis auf den Gesetzestitel und das datum [SR_220_OR_de.md::0],
- einen Ausschnitt zur Gliederung („A. Begriff und Entstehung …“) ohne konkretten Artikeltext [SR_220_OR_de.md::527],
- Verweise auf andere Gesetze (StGB, ZPO) ohne OR-Text.

Um den Inhalt von **Art. 1 OR** zu nennen, müsste der entsprechende Text im Kontext vorhanden sein – dies ist hier nicht der Fall.

Fazit: **Der Inhalt von Artikel 1 OR ist im gegebenen Kontext nicht enthalten.**

### or-artikel-1 — rerank

**Reference:** Zum Abschluss eines Vertrags ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich. Diese Willensäusserung kann ausdrücklich oder stillschweigend erfolgen [SR_220_OR_de.md Art. 1].

**Generated:** Im gegebenen Kontext ist **kein Inhalt von Artikel 1 des OR (Schweizerisches Obligationenrecht)** enthalten. Die aufgeführten Textchunks zeigen Ausschnitte aus verschiedenen Artikeln (z. B. Art. 1542¹² OR, Art. 600 Abs. 3 OR, Art. 697b ff. OR, Art. 698 Abs. 2–3 OR), jedoch **keinen Ausschnitt aus Art. 1 OR**.

Da die Frage explizit nach dem Inhalt von **Artikel 1 des OR** fragt und dieser nicht im bereitgestellten Kontext enthalten ist, kann die Frage **nicht anhand des gegebenen Kontexts** beantwortet werden.

Der Gesetzestext des OR (SR 220) beginnt gemäss üblicher Gesetzesstruktur üblicherweise mit einer Einleitungsregelung (z. B. Anwendungsbereich, In-Kraft-Treten, etc.). Für den genauen Wortlaut von **Art. 1 OR** müsste der vollständige Gesetzestext konsultiert werden (z. B. über fedlex.admin.ch). 

**Antwort:** Der Inhalt von Artikel 1 des OR ist im bereitgestellten Kontext nicht enthalten.

### or-artikel-1 — graph

**Reference:** Zum Abschluss eines Vertrags ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich. Diese Willensäusserung kann ausdrücklich oder stillschweigend erfolgen [SR_220_OR_de.md Art. 1].

**Generated:** Artikel 1 des Schweizerischen Obligationenrechts (OR) lautet wie folgt:

**Art. 1**  
1. Zum Abschlusse eines Vertrages ist die übereinstimmende gegen seitige Willensäusserung der Parteien erforderlich.  
2. Sie kann eine ausdrückliche oder stillschweigende sein.  

[SR_220_OR_de.md Art. 1]
