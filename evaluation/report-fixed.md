# RAG evaluation

- Methods: **fixed-vector**
- Collections: `fixed=rag_fixed`
- Shared context budget: **6 chunks**
- Full corpus: approximately **1,202,768 tokens**
- Token counts are estimated as characters / 4.
- Term coverage is shown only as a retrieval diagnostic; it is not an answer-quality score.

## Retrieval

| Question | Method | Source recall | Article Hit@K | Article Recall@K | Article MRR | Term coverage (diagnostic) | Document tokens | Prompt-context tokens |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| or-kuendigung-krankheit | fixed-vector | 100% | 0% | 0% | 0.00 | 67% | 1,199 | 1,285 |
| or-kaufvertrag-verjaehrung | fixed-vector | 100% | 100% | 100% | 1.00 | 100% | 1,198 | 1,284 |
| bgg-beschwerdefrist | fixed-vector | 100% | 100% | 100% | 0.33 | 100% | 1,200 | 1,296 |
| or-probezeit | fixed-vector | 100% | 0% | 0% | 0.00 | 67% | 1,200 | 1,288 |
| dsg-einwilligung-widerruf | fixed-vector | 100% | 100% | 25% | 0.25 | 75% | 1,198 | 1,292 |
| or-artikel-1 | fixed-vector | 100% | 100% | 100% | 1.00 | 80% | 1,198 | 1,291 |

## Answers

| Question | Method | Fact coverage | Expected-citation precision | Citation grounding | Citation completeness | Answer tokens |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| or-kuendigung-krankheit | fixed-vector | 0% | 0% | 67% | 0% | 411 |
| or-kaufvertrag-verjaehrung | fixed-vector | 100% | 33% | 67% | 100% | 198 |
| bgg-beschwerdefrist | fixed-vector | 67% | 50% | 100% | 100% | 280 |
| or-probezeit | fixed-vector | 67% | 0% | 100% | 0% | 237 |
| dsg-einwilligung-widerruf | fixed-vector | 0% | 0% | 100% | 0% | 344 |
| or-artikel-1 | fixed-vector | 100% | 100% | 100% | 100% | 66 |

## Summary

- **fixed-vector:** article recall@K 54.2%, MRR 0.43, fact coverage 55.6%, expected-citation precision 30.6%, citation grounding 88.9%, citation completeness 50.0%, average context 1,289 tokens, corpus-token savings 99.89%.

## Strategic token perspective

All selected methods receive the same final chunk budget. Their actual token counts can differ because the retrieved chunks have different lengths.

## Answer details

### or-kuendigung-krankheit — fixed-vector

**Reference:** Nach Ablauf der Probezeit darf der Arbeitgeber bei einer unverschuldeten krankheitsbedingten vollständigen oder teilweisen Arbeitsverhinderung während der gesetzlichen Sperrfrist nicht kündigen: 30 Tage im ersten Dienstjahr, 90 Tage vom zweiten bis und mit fünften Dienstjahr und 180 Tage ab dem sechsten Dienstjahr. Eine während der Sperrfrist ausgesprochene Kündigung ist nichtig. Wurde vorher gekündigt und läuft die Kündigungsfrist in die Sperrfrist hinein, wird ihr Ablauf unterbrochen und danach fortgesetzt. Während der Probezeit gilt dieser Schutz nicht [SR_220_OR_de.md Art. 336c].

**Generated:** Nein, der Arbeitgeber darf **während der Krankheit** des Arbeitnehmers **nicht kündigen**, wenn die Verhinderung **ohne Verschulden des Arbeitnehmers** erfolgt und innerhalb einer gesetzlich vorgesehenen Sperrfrist liegt.

Gemäss [SR_220_OR_de.md Art. 335b Abs. 1 lit. a] ist die Kündigung während des **Urlaubs**, während des **Krankheitsfalls** sowie bei **Schwangerschaft und Niederkunft** ausdrücklich ausgeschlossen:

> *„Die Kündigung des Arbeitsverhältnisses ist unzulässig, wenn…*  
> *a. der Arbeitnehmer durch Krankheit oder Unfall an der Arbeitsleistung verhindert ist, solange die Verhinderung bis zu einem Monat dauert und nicht durch ein Verschulden des Arbeitnehmers verursacht ist;*”

Darüber hinaus enthält [SR_220_OR_de.md Art. 335d Abs. 1 lit. a] eine allgemeine Sperrfristregelung, wonach die Kündigung **während der Verhinderung an der Arbeitsleistung** – einschliesslich Krankheit – nicht zulässig ist, soweit sie durch Umstände verursacht wird, für die der Arbeitnehmer nicht verantwortlich ist, und zwar **bis zu drei Wochen im ersten Dienstjahr** sowie **für eine angemessene, längere Zeit danach** ([SR_220_OR_de.md Art. 328a Abs. 2]).

Zusammenfassend:  
- Der Arbeitgeber **darf während der Krankheit nicht kündigen**, solange der Arbeitnehmer arbeitsunfähig ist und die Verhinderung **nicht jego Verschulden** zuzurechnen ist ([SR_220_OR_de.md Art. 335b Abs. 1 lit. a], [Art. 335d Abs. 1 lit. a]).  
- Die konkrete Dauer dieser Schutzfrist ergibt sich aus Art. 328a Abs. 2: **3 Wochen im ersten Dienstjahr**, danach **eine angemessene, längere Zeit**, abhängig von Dauer des Arbeitsverhältnisses und den Umständen.

### or-kaufvertrag-verjaehrung — fixed-vector

**Reference:** Für Forderungen aus einem Kaufvertrag gilt grundsätzlich die allgemeine Verjährungsfrist von zehn Jahren, sofern das Bundeszivilrecht für den konkreten Anspruch keine abweichende Frist vorsieht [SR_220_OR_de.md Art. 127].

**Generated:** Forderungen aus einem Kaufvertrag verjähren nach der allgemeinen Verjährungsfrist von **zehn Jahren**, sofern das Bundeszivilrecht nichts anderes bestimmt ([SR_220_OR_de.md Art. 127]).  

Für **Gewährleistungsansprüche wegen Mängeln der Sache** gilt eine spezielle Verjährungsfrist von **zwei Jahren** nach Ablieferung an den Käufer, selbst wenn dieser die Mängel erst später entdeckt — es sei denn, der Verkäufer hat eine längere Haftung übernommen ([SR_220_OR_de.md Art. 21075] Abs. 1).  

Für **Ansprüche des Käufers wegen Mängeln des Grundstücks** beträgt die Verjährungsfrist **fünf Jahre** nach dem Erwerb des Eigentums ([SR_220_OR_de.md Art. 149]).  

Die allgemeine Zehn-Jahres-Frist nach Art. 127 OR gilt somit nur, soweit keine speziellere Regelung (wie die oben genannten) greift.

### bgg-beschwerdefrist — fixed-vector

**Reference:** Grundsätzlich ist die Beschwerde gegen einen Entscheid innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen. Artikel 100 BGG sieht für bestimmte Fälle kürzere Fristen von zehn, fünf oder drei Tagen vor; gegen das unrechtmässige Verweigern oder Verzögern eines Entscheids kann jederzeit Beschwerde geführt werden [SR_173.110_BGG_de.md Art. 100].

**Generated:** Für eine Beschwerde ans Bundesgericht gilt allgemein eine **30-tägige Frist**, soweit das Bundesgerichtsgesetz (BGG) nichts anderes vorsieht.

Konkret ergibt sich dies aus:

- **Art. 100 Abs. 1 BGG**:  
  *„Die Beschwerde gegen einen Entscheid ist innert 30 Tagen nach der Eröffnung der vollständigen Ausfertigung beim Bundesgericht einzureichen.“* [SR_173.110_BGG_de.md Art. 100 Abs. 1]

Zusätzlich lässt sich aus **Art. 389 Abs. 2 ZPO** schließen, dass für das Verfahren vor dem Bundesgericht die Bestimmungen des Bundesgerichtsgesetzes gelten, soweit nicht im ZPO-Kapitel über die Schiedsgerichtsbarkeit etwas anderes bestimmt ist [SR_272_ZPO_de.md Art. 389 Abs. 2].

Weitere, verkürzte Fristen (10, 5, 3 Tage) gelten nur für spezifische Entscheide (z. B. bei Schuldbetreibung, Konkurs, internationaler Rechtshilfe im Strafrecht, usw.), wie in **Art. 100 Abs. 2–5 BGG** geregelt [SR_173.110_BGG_de.md Art. 100 Abs. 2–5].

Daher gilt:  
🔹 **Allgemeine Beschwerdefrist ans Bundesgericht: 30 Tage** nach Eröffnung der vollständigen Ausfertigung.  
🔹 Für bestimmte Entscheide: verkürzte Fristen gem. Art. 100 Abs. 2–5 BGG.

### or-probezeit — fixed-vector

**Reference:** Als Probezeit gilt grundsätzlich der erste Monat des Arbeitsverhältnisses. Durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag kann davon abgewichen werden; die Probezeit darf jedoch höchstens drei Monate dauern. Während der Probezeit gilt eine Kündigungsfrist von sieben Tagen [SR_220_OR_de.md Art. 335b].

**Generated:** Die Probezeit im Arbeitsverhältnis beträgt nach dem Schweizerischen Obligationenrecht (OR) grundsätzlich **einen Monat**, nämlich der erste Monat eines Arbeitsverhältnisses [SR_220_OR_de.md Art. 335c Abs. 1].  

Gemäß Absatz 2 des gleichen Artikels kann die Probezeit **durch schriftliche Abrede, Normalarbeitsvertrag oder Gesamtarbeitsvertrag** auf **höchstens drei Monate** verlängert werden.  

Zusätzlich ist in Absatz 3 geregelt, dass bei einer effektiven Verkürzung der Probezeit infolge Krankheit, Unfall oder Erfüllung einer nicht freiwillig übernommenen gesetzlichen Pflicht die Probezeit entsprechend verlängert wird.

Zusammengefasst:  
- **Standarddauer**: 1 Monat [SR_220_OR_de.md Art. 335c Abs. 1]  
- **Maximale vertraglich vereinbare Dauer**: 3 Monate [SR_220_OR_de.md Art. 335c Abs. 2]  
- **Verlängerung bei Verhinderung** (Krankheit, Unfall, gesetzliche Pflicht): um den jeweiligen Ausfallbetrag [SR_220_OR_de.md Art. 335c Abs. 3]

### dsg-einwilligung-widerruf — fixed-vector

**Reference:** Das DSG formuliert in den vorliegenden Artikeln kein eigenständiges allgemeines Widerrufsrecht. Es verlangt aber eine freiwillige und informierte Einwilligung [SR_235.1_DSG_de.md Art. 6], behandelt eine Bearbeitung entgegen der ausdrücklichen Willenserklärung als Persönlichkeitsverletzung [SR_235.1_DSG_de.md Art. 30] und nennt die Einwilligung nur als einen möglichen Rechtfertigungsgrund [SR_235.1_DSG_de.md Art. 31]. Wird sie für die Zukunft widerrufen, kann die Bearbeitung daher nicht mehr auf diese Einwilligung gestützt werden; ein anderer Rechtfertigungsgrund kann sie dennoch erlauben. Betroffene können insbesondere das Verbot einer Bearbeitung sowie gegebenenfalls Löschung oder Vernichtung verlangen [SR_235.1_DSG_de.md Art. 32].

**Generated:** Ja, Sie können eine Einwilligung zur Datenbearbeitung widerrufen.  

Laut Art. 7 Abs. 2 DSG muss die Einwilligung **freiwillig** erteilt werden, und aus der freiwilligen Natur folgt grundsätzlich das Recht, die Einwilligung jederzeit zuwiderrufen [SR_235.1_DSG_de.md Art. 7 Abs. 2].  

Zusätzlich enthält Art. 32 Abs. 1 DSG ein allgemeines Recht auf Berichtigung unrichtiger Daten — und ein Widerruf der Einwilligung kann insbesondere dann notwendig sein, wenn die weitere Verarbeitung ohne diese rechtsgrundlegend ist.  

Allerdings gilt:  
- Ein Widerruf wirkt **rückwirkungslos**, d. h. er beeinträchtigt nicht bereits erfolgte Verarbeitungen, soweit diese rechtmässig waren (z. B. aufgrund einer anderen Rechtsgrundlage wie eines gesetzlichen Auftrags).  
- Der Widerruf ist dem Verantwortlichen **ausdrücklich** mitzuteilen (vgl. Art. 7 Abs. 6 DSG).  

Zusätzlich ist zu beachten, dass Art. 36 DSG vorsieht, dass bei Vorliegen eines überwiegenden schutzwürdigen Interesses der betroffenen Person (z. B. Widerruf der Einwilligung) die Daten nicht weiterverarbeitet werden dürfen, sofern keine überwiegenden, rechtfertigenden Gründe (z. B. gesetzliche Pflichten) entgegenstehen.

**Zusammenfassung:**  
Ja, eine Einwilligung kann widerrufen werden, sofern sie freiwillig erteilt wurde, und der Widerruf ist dem Verantwortlichen mitzuteilen [SR_235.1_DSG_de.md Art. 7 Abs. 2].

### or-artikel-1 — fixed-vector

**Reference:** Zum Abschluss eines Vertrags ist die übereinstimmende gegenseitige Willensäusserung der Parteien erforderlich. Diese Willensäusserung kann ausdrücklich oder stillschweigend erfolgen [SR_220_OR_de.md Art. 1].

**Generated:** Artikel 1 des Obligationenrechts (OR) lautet:

**Art. 1**  
1 Zum Abschlusse eines Vertrages ist die übereinstimmende gegen seitige Willensäusserung der Parteien erforderlich.  
2 Sie kann eine ausdrückliche oder stillschweigende sein.  

[SR_220_OR_de.md Art. 1]
