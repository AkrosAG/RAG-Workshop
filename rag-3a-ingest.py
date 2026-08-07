"""Alternative legal-structure ingest for the Fedlex Markdown corpus.

Unlike ``rag-3a-ingest.py``, this variant treats legal articles as the primary
boundary, removes obvious table-of-contents/reference noise, splits oversized
article text at sentence or word boundaries, and packs small related blocks.

It deliberately writes to a separate store and collection:

    Chroma path:  .chroma-semantic
    Collection:   rag_semantic

Dry-run without embeddings:
    poetry run python rag-3a-ingest.py --dry-run

Build/update the separate Chroma database:
    poetry run python rag-3a-ingest.py
"""

import argparse
import os
import re
import sys
from collections import Counter
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "fedlex_mds"
CHROMA_PATH = ROOT / ".chroma-3"
COLLECTION = "rag_semantic"
MAX_CHUNK_SIZE = 800
EMBED_BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", "64"))

ARTICLE_HEADING_RE = re.compile(r"(?m)^(?=Art\.\s*\d)")
ARTICLE_LABEL_RE = re.compile(
    r"^Art\.\s*\d{1,4}(?:(?:bis|ter|quater)|[a-z])?\d*",
    re.IGNORECASE,
)
PAGE_MARKER_RE = re.compile(r"^##\s+PDF-Seite\s+\d+\s*$", re.IGNORECASE)
REFERENCE_ONLY_RE = re.compile(
    r"^\d+[a-z]?\s+(?:SR|AS|BBl)\s+[0-9IVX.\s–-]+$",
    re.IGNORECASE,
)
TOC_LINE_RE = re.compile(
    r"(?:\.{3,}\s*Art\.\s*\d|(?:^|\s)Art\.\s*\d[\w–-]*\s*$)",
    re.IGNORECASE,
)
SENTENCE_BOUNDARY_RE = re.compile(
    r"(?<!Art\.)(?<=[.!?])\s+(?=(?:\d+[a-z]?\s+)?[A-ZÄÖÜ])"
)
PARAGRAPH_NUMBER_RE = re.compile(r"\n(?=\d+(?:bis|ter|quater|[a-z])?\s+)")


def is_table_of_contents(block: str) -> bool:
    """Recognize headings and dense article listings from PDF contents pages."""
    if re.fullmatch(r"(?i)(?:#+\s*)?Inhaltsverzeichnis", block.strip()):
        return True
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if len(lines) < 5:
        return False
    toc_lines = sum(bool(TOC_LINE_RE.search(line)) for line in lines)
    dot_leaders = sum("..." in line for line in lines)
    return toc_lines >= 3 and (toc_lines + dot_leaders) / len(lines) >= 0.35


def is_reference_noise(block: str) -> bool:
    """Drop compact, standalone Fedlex footnote/source references."""
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    return bool(lines) and len(block) <= 200 and all(
        REFERENCE_ONLY_RE.fullmatch(line) for line in lines
    )


def split_at_articles(block: str) -> list[tuple[str, str]]:
    """Split a Markdown block before every line-starting legal article."""
    starts = [match.start() for match in ARTICLE_HEADING_RE.finditer(block)]
    if not starts:
        return [("text", block.strip())]

    parts: list[tuple[str, str]] = []
    if starts[0] > 0 and block[: starts[0]].strip():
        parts.append(("text", block[: starts[0]].strip()))
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(block)
        article = block[start:end].strip()
        if article:
            parts.append(("article", article))
    return parts


def split_long_text(
    text: str,
    max_size: int,
    continuation_prefix: str = "",
) -> list[str]:
    """Split oversized text at paragraphs, numbered clauses, sentences or words."""
    if len(text) <= max_size:
        return [text]

    normalized = PARAGRAPH_NUMBER_RE.sub("\n\n", text.strip())
    units: list[str] = []
    for paragraph in re.split(r"\n\s*\n", normalized):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        units.extend(
            part.strip()
            for part in SENTENCE_BOUNDARY_RE.split(paragraph)
            if part.strip()
        )

    chunks: list[str] = []
    current = ""

    def flush() -> None:
        nonlocal current
        if current:
            chunks.append(current)
            current = ""

    for unit in units:
        prefix = continuation_prefix if chunks and not current else ""
        separator = "\n" if current else ""
        candidate = f"{current}{separator}{unit}" if current else f"{prefix}{unit}"
        if len(candidate) <= max_size:
            current = candidate
            continue

        flush()
        prefix = continuation_prefix if chunks else ""
        available = max_size - len(prefix)
        remaining = unit
        while len(remaining) > available:
            split_at = remaining.rfind(" ", 0, available + 1)
            if split_at <= 0:
                split_at = available
            chunks.append(f"{prefix}{remaining[:split_at].rstrip()}")
            remaining = remaining[split_at:].lstrip()
            prefix = continuation_prefix
            available = max_size - len(prefix)
        current = f"{prefix}{remaining}" if remaining else ""

    flush()
    return chunks


def split_article(article: str, max_size: int) -> list[str]:
    """Keep an article together when possible and label continuation chunks."""
    label_match = ARTICLE_LABEL_RE.match(article)
    label = label_match.group(0) if label_match else "Artikel"
    continuation = f"{label} (Fortsetzung)\n"
    return split_long_text(article, max_size, continuation)


def legal_chunk(text: str, max_size: int = MAX_CHUNK_SIZE) -> list[str]:
    """Create focused legal chunks with article-first structural boundaries."""
    raw_blocks = [
        block.strip()
        for block in re.split(r"\n\s*\n", text)
        if block.strip()
    ]
    units: list[tuple[str, str]] = []
    for block in raw_blocks:
        if PAGE_MARKER_RE.fullmatch(block):
            continue
        if is_table_of_contents(block) or is_reference_noise(block):
            continue
        if block.lstrip().startswith("#"):
            units.append(("heading", block))
        else:
            units.extend(split_at_articles(block))

    chunks: list[str] = []
    current = ""

    def flush() -> None:
        nonlocal current
        if current:
            chunks.append(current)
            current = ""

    for kind, unit in units:
        if kind == "heading":
            flush()
            current = unit
            continue

        if kind == "article":
            flush()
            article_chunks = split_article(unit, max_size)
            chunks.extend(article_chunks)
            continue

        # Non-article material such as document metadata, title context or an
        # article continuation is packed while it fits. Oversized material is
        # split safely without cutting a normal word.
        separator = "\n\n" if current else ""
        if len(current) + len(separator) + len(unit) <= max_size:
            current = f"{current}{separator}{unit}" if current else unit
            continue
        flush()
        text_chunks = split_long_text(unit, max_size)
        chunks.extend(text_chunks[:-1])
        current = text_chunks[-1]

    flush()
    return [
        item
        for item in chunks
        if item.strip()
        and item.strip() != "Art."
        and not ARTICLE_LABEL_RE.fullmatch(item.strip())
    ]


def collect_chunks() -> tuple[list[str], list[str], list[dict[str, str]]]:
    """Read all Markdown files and return deterministic Chroma records."""
    ids: list[str] = []
    texts: list[str] = []
    metadatas: list[dict[str, str]] = []
    embed_model = os.getenv("EMBED_MODEL", "bge-m3")
    for path in sorted(DATA.glob("*.md")):
        for number, piece in enumerate(legal_chunk(path.read_text(encoding="utf-8"))):
            ids.append(f"{path.name}::{number}")
            texts.append(piece)
            metadatas.append(
                {
                    "source": path.name,
                    "embed_model": embed_model,
                    "chunk_strategy": "legal-article-v1",
                }
            )
    return ids, texts, metadatas


def print_audit(ids: list[str], texts: list[str]) -> None:
    """Print deterministic quality statistics without calling an API."""
    lengths = [len(text) for text in texts]
    article_counts = [
        len(ARTICLE_HEADING_RE.findall(text))
        for text in texts
    ]
    by_source = Counter(chunk_id.rsplit("::", 1)[0] for chunk_id in ids)
    print(f"[audit] {len(texts)} chunks from {len(by_source)} source files")
    if not texts:
        return
    print(
        f"[audit] length min/avg/max: {min(lengths)}/"
        f"{sum(lengths) / len(lengths):.1f}/{max(lengths)}"
    )
    print(
        f"[audit] over budget: {sum(length > MAX_CHUNK_SIZE for length in lengths)}; "
        f"empty: {sum(not text.strip() for text in texts)}; "
        f"multiple articles: {sum(count > 1 for count in article_counts)}"
    )


def embed(
    client: OpenAI, model: str, texts: list[str]
) -> list[list[float]]:
    """Create embeddings in endpoint-friendly batches."""
    embeddings: list[list[float]] = []
    for start in range(0, len(texts), EMBED_BATCH_SIZE):
        batch = texts[start : start + EMBED_BATCH_SIZE]
        response = client.embeddings.create(model=model, input=batch)
        embeddings.extend(item.embedding for item in response.data)
    return embeddings


def synchronize() -> None:
    """Synchronize the alternative desired state into its own Chroma store."""
    ids, texts, metadatas = collect_chunks()
    print_audit(ids, texts)

    embed_model = os.getenv("EMBED_MODEL", "bge-m3")
    client = OpenAI(
        base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
        api_key=os.getenv("LLM_API_KEY", "ollama"),
    )
    collection = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    ).get_or_create_collection(
        COLLECTION,
        embedding_function=None,
        metadata={"hnsw:space": "cosine"},
    )

    stored = collection.get(include=["documents", "metadatas"])
    existing_documents = dict(zip(stored["ids"], stored["documents"]))
    existing_metadatas = dict(zip(stored["ids"], stored["metadatas"]))
    changed = [
        index
        for index, chunk_id in enumerate(ids)
        if (
            existing_documents.get(chunk_id) != texts[index]
            or existing_metadatas.get(chunk_id, {}).get("embed_model")
            != embed_model
            or existing_metadatas.get(chunk_id, {}).get("chunk_strategy")
            != "legal-article-v1"
        )
    ]
    obsolete = sorted(set(existing_documents) - set(ids))

    for start in range(0, len(changed), EMBED_BATCH_SIZE):
        batch = changed[start : start + EMBED_BATCH_SIZE]
        batch_texts = [texts[index] for index in batch]
        collection.upsert(
            ids=[ids[index] for index in batch],
            embeddings=embed(client, embed_model, batch_texts),
            documents=batch_texts,
            metadatas=[metadatas[index] for index in batch],
        )
        print(
            f"[ingest] embedded "
            f"{min(start + len(batch), len(changed))}/{len(changed)}"
        )

    for start in range(0, len(obsolete), 500):
        collection.delete(ids=obsolete[start : start + 500])

    print(
        f"[ingest] synchronized {len(changed)} changed/new and "
        f"removed {len(obsolete)} obsolete chunk(s); "
        f"'{COLLECTION}' now holds {collection.count()}"
    )


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Build an article-oriented Fedlex Chroma collection."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only create and audit chunks; do not call the API or write Chroma.",
    )
    args = parser.parse_args()

    if args.dry_run:
        ids, texts, _ = collect_chunks()
        print_audit(ids, texts)
        return
    synchronize()


if __name__ == "__main__":
    sys.excepthook = lambda exc_type, exc, _: sys.exit(
        f"{exc_type.__name__}: {exc}"
    )
    # Redirected stdout on Windows defaults to cp1252; output needs UTF-8.
    sys.stdout.reconfigure(encoding="utf-8")
    main()
