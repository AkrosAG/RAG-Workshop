#!/usr/bin/env python3
"""Convert downloaded Fedlex PDFs into Markdown files for RAG ingestion.

The original PDFs remain the source of truth. Each generated Markdown file
contains a metadata header and one section per PDF page so retrieved text can
be traced back to the source page.

Usage:
    python scripts/fedlex_pdf_to_md.py
    python scripts/fedlex_pdf_to_md.py --input-dir path/to/pdfs --output-dir data
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "scripts" / "fedlex_pdfs"
DEFAULT_OUTPUT = ROOT / "data"


def document_metadata(path: Path) -> tuple[str, str, str]:
    """Return SR number, short law name, and language from a Fedlex filename."""
    match = re.fullmatch(r"SR_(.+?)_([^_]+)_([a-z]{2})", path.stem)
    if not match:
        return "unknown", path.stem, "unknown"
    return match.group(1), match.group(2), match.group(3)


def clean_page(text: str) -> str:
    """Apply conservative cleanup without changing the legal wording."""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u00ad", "").replace("\x00", "")

    # Join words that the PDF split with a hyphen at a line boundary.
    text = re.sub(
        r"(?<=[a-zäöü])[-‐‑]\s*\n\s*(?=[a-zäöü])",
        "",
        text,
        flags=re.IGNORECASE,
    )

    lines: list[str] = []
    for raw_line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", raw_line).strip()
        # Standalone page counters add noise but no legal information.
        if re.fullmatch(r"\d+\s*/\s*\d+", line):
            continue
        lines.append(line)

    cleaned = "\n".join(lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def convert_pdf(path: Path) -> str:
    """Extract a PDF into Markdown with stable page-level source markers."""
    sr, law, language = document_metadata(path)
    reader = PdfReader(path)

    parts = [
        f"# {law} (SR {sr})",
        "",
        f"- Quelle: `{path.name}`",
        f"- Sprache: `{language}`",
        f"- PDF-Seiten: {len(reader.pages)}",
        "- Hinweis: Automatisch aus der offiziellen Fedlex-PDF extrahiert.",
    ]

    for page_number, page in enumerate(reader.pages, start=1):
        text = clean_page(page.extract_text() or "")
        if not text:
            continue
        parts.extend(["", f"## PDF-Seite {page_number}", "", text])

    return "\n".join(parts).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Fedlex PDFs into Markdown files for Chroma ingestion."
    )
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    input_dir = args.input_dir.resolve()
    output_dir = args.output_dir.resolve()
    pdfs = sorted(input_dir.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"No PDF files found in {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    for pdf in pdfs:
        target = output_dir / f"{pdf.stem}.md"
        target.write_text(convert_pdf(pdf), encoding="utf-8")
        print(f"[convert] {pdf.name} -> {target.relative_to(ROOT)}")

    print(f"[convert] wrote {len(pdfs)} Markdown file(s) to {output_dir}")


if __name__ == "__main__":
    main()
