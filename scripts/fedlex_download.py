#!/usr/bin/env python3
"""
Lädt die konsolidierten, aktuell anwendbaren Fassungen der Kern-Bundeserlasse
als PDF von Fedlex herunter.

Vorgehen:
  1. Eine SPARQL-Abfrage an https://fedlex.data.admin.ch/sparqlendpoint löst
     pro SR-Nummer die URL der PDF-Manifestation der neuesten anwendbaren
     Konsolidierung auf (JOLux-Modell: ConsolidationAbstract -> Consolidation
     -> Expression -> Manifestation).
  2. Die PDFs werden in das Zielverzeichnis geladen.

Nur Python-Standardbibliothek, keine Abhängigkeiten.

Nutzung:
    python3 fedlex_download.py                 # Deutsch, ./fedlex_pdfs
    python3 fedlex_download.py --lang fr       # Französisch
    python3 fedlex_download.py --outdir /pfad  # anderes Zielverzeichnis

Rechtlicher Hinweis: Die Wiederverwendung der Fedlex-Texte ist gemäss
https://www.fedlex.admin.ch/de/broadcasters ausdrücklich erlaubt.
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

SPARQL_ENDPOINT = "https://fedlex.data.admin.ch/sparqlendpoint"
USER_AGENT = "fedlex-pdf-downloader/1.0 (persoenliche Nutzung)"

# SR-Nummer -> Kurzbezeichnung (für Dateinamen)
LAWS = {
    "101":     "BV",
    "210":     "ZGB",
    "220":     "OR",
    "272":     "ZPO",
    "311.0":   "StGB",
    "312.0":   "StPO",
    "173.110": "BGG",
    "235.1":   "DSG",
    "142.20":  "AIG",
    "142.31":  "AsylG",
    "641.20":  "MWSTG",
    "642.11":  "DBG",
    "830.1":   "ATSG",
    "831.10":  "AHVG",
}

LANG_URI = {
    "de": "http://publications.europa.eu/resource/authority/language/DEU",
    "fr": "http://publications.europa.eu/resource/authority/language/FRA",
    "it": "http://publications.europa.eu/resource/authority/language/ITA",
    "rm": "http://publications.europa.eu/resource/authority/language/ROH",
    "en": "http://publications.europa.eu/resource/authority/language/ENG",
}


def build_query(sr_numbers, lang_uri):
    values = " ".join(f'"{sr}"' for sr in sr_numbers)
    # Kern der Abfrage entspricht dem offiziellen JOLux-Beispiel
    # (swiss.github.io/fedlex-jolux, "Classified Compilation").
    # Ergänzt: Auflösung SR-Nummer -> ConsolidationAbstract über die
    # Taxonomie-Notation sowie Filter auf heute anwendbare Fassungen
    # (sonst könnte eine bereits publizierte, aber erst künftig geltende
    # Fassung zurückkommen).
    return f"""
PREFIX jolux: <http://data.legilux.public.lu/resource/ontology/jolux#>
PREFIX skos:  <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>

SELECT ?sr ?date ?url WHERE {{
  VALUES ?sr {{ {values} }}
  ?abstract a jolux:ConsolidationAbstract ;
            jolux:classifiedByTaxonomyEntry ?tax .
  ?tax skos:notation ?notation .
  FILTER(str(?notation) = ?sr)
  ?work jolux:isMemberOf ?abstract ;
        jolux:dateApplicability ?date ;
        jolux:isRealizedBy ?expression .
  FILTER(xsd:date(?date) <= xsd:date(NOW()))
  ?expression jolux:language <{lang_uri}> ;
              jolux:isEmbodiedBy ?manifestation .
  ?manifestation jolux:format <http://publications.europa.eu/resource/authority/file-type/PDF> ;
                 jolux:isExemplifiedBy ?url .
}}
ORDER BY ?sr DESC(?date)
"""


def run_sparql(query):
    data = urllib.parse.urlencode({"query": query}).encode("utf-8")
    req = urllib.request.Request(
        SPARQL_ENDPOINT,
        data=data,
        headers={
            "Accept": "application/sparql-results+json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def resolve_pdf_urls(sr_numbers, lang_uri):
    """Gibt {sr: (datum, url)} der jeweils neuesten anwendbaren Fassung zurück."""
    result = {}
    bindings = run_sparql(build_query(sr_numbers, lang_uri))["results"]["bindings"]
    for b in bindings:
        sr = b["sr"]["value"]
        date = b["date"]["value"]
        url = b["url"]["value"]
        # Ergebnisse sind pro SR absteigend nach Datum sortiert:
        # erster Treffer = neueste anwendbare Fassung.
        if sr not in result:
            result[sr] = (date, url)
    return result


def download(url, target: Path):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp, open(target, "wb") as f:
        while chunk := resp.read(65536):
            f.write(chunk)


def main():
    parser = argparse.ArgumentParser(description="Fedlex-Kernerlasse als PDF laden")
    parser.add_argument("--lang", default="de", choices=sorted(LANG_URI),
                        help="Sprache der Erlasse (Standard: de)")
    parser.add_argument("--outdir", default="fedlex_pdfs",
                        help="Zielverzeichnis (Standard: ./fedlex_pdfs)")
    parser.add_argument("--delay", type=float, default=1.0,
                        help="Pause in Sekunden zwischen Downloads (Standard: 1.0)")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"Löse PDF-URLs für {len(LAWS)} Erlasse auf (Sprache: {args.lang}) ...")
    try:
        urls = resolve_pdf_urls(list(LAWS), LANG_URI[args.lang])
    except Exception as e:
        sys.exit(f"SPARQL-Abfrage fehlgeschlagen: {e}")

    missing = [sr for sr in LAWS if sr not in urls]
    ok, failed = 0, []

    for sr, abbr in LAWS.items():
        if sr not in urls:
            continue
        date, url = urls[sr]
        target = outdir / f"SR_{sr}_{abbr}_{args.lang}.pdf"
        print(f"  SR {sr:>8} ({abbr:6}) Stand {date}: {url}")
        try:
            download(url, target)
            ok += 1
        except Exception as e:
            failed.append((sr, str(e)))
            print(f"    FEHLER: {e}")
        time.sleep(args.delay)

    print(f"\nFertig: {ok} von {len(LAWS)} PDFs in {outdir.resolve()}")
    if missing:
        print(f"Keine PDF-URL gefunden für SR: {', '.join(missing)}")
        print("(Mögliche Ursachen: Sprache nicht verfügbar – z. B. Englisch nur "
              "für einzelne Erlasse – oder abweichende Taxonomie-Notation.)")
    if failed:
        print("Download fehlgeschlagen für:")
        for sr, err in failed:
            print(f"  SR {sr}: {err}")


if __name__ == "__main__":
    main()