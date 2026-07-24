"""Small, transparent graph-retrieval helpers used by stage 4 and evaluation."""

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ARTICLE_RE = re.compile(
    r"\bArt\.\s*(\d+(?:(?:bis|ter|quater)|[a-z])?\d*)",
    re.IGNORECASE,
)
ARTICLE_DEFINITION_RE = re.compile(
    r"(?m)^\s*Art\.\s*(\d+(?:(?:bis|ter|quater)|[a-z])?\d*)",
    re.IGNORECASE,
)
ARTICLE_PARTS_RE = re.compile(
    r"^(\d+?)((?:bis|ter|quater)|[a-z])?(\d*)$", re.IGNORECASE
)
GRAPH_VERSION = 3
MAX_ARTICLE_DIGITS = 4
WORD_RE = re.compile(r"[0-9a-zäöüàâéèêëîïôûüç]+", re.IGNORECASE)
STOPWORDS = {
    "aber",
    "als",
    "auch",
    "auf",
    "aus",
    "bei",
    "das",
    "dem",
    "den",
    "der",
    "des",
    "die",
    "ein",
    "eine",
    "einer",
    "eines",
    "für",
    "gelten",
    "gilt",
    "hoch",
    "ist",
    "kann",
    "können",
    "lange",
    "mit",
    "nach",
    "oder",
    "sich",
    "und",
    "von",
    "was",
    "welche",
    "welchem",
    "welchen",
    "welcher",
    "welches",
    "wie",
    "wird",
    "voraussetzung",
    "voraussetzungen",
    "zu",
}
SOURCE_ALIASES = {
    "aig": {"aig", "ausländergesetz", "ausländerrecht"},
    "asylg": {"asylgesetz", "asylg"},
    "bv": {"bundesverfassung", "bv", "verfassung"},
    "dsg": {"datenschutzgesetz", "dsg"},
    "mwstg": {"mehrwertsteuer", "mehrwertsteuergesetz", "mwst", "mwstg"},
    "or": {"obligationenrecht", "or"},
    "stgb": {"stgb", "strafgesetzbuch"},
    "stpo": {"stpo", "strafprozessordnung"},
    "zgb": {"schweizerischeszivilgesetzbuch", "zgb", "zivilgesetzbuch"},
}
MIN_ARTICLE_SCORE = 2.0
RRF_CONSTANT = 60


def _chunk_number(chunk_id: str) -> int:
    try:
        return int(chunk_id.rsplit("::", 1)[1])
    except (IndexError, ValueError):
        return 0


def _article_candidates(raw: str) -> list[str]:
    """Return plausible article IDs, stripping glued PDF footnote numbers.

    Fedlex extraction can turn ``Art. 5a²`` into ``Art. 5a2`` and
    ``Art. 7²²`` into ``Art. 722``. Letter suffixes are unambiguous; for
    digits-only tokens all numeric prefixes remain candidates.
    """
    value = raw.casefold()
    letter_match = re.fullmatch(
        rf"(\d{{1,{MAX_ARTICLE_DIGITS}}})"
        r"((?:bis|ter|quater)|[a-z])(\d*)",
        value,
    )
    if letter_match:
        number, suffix, _footnote = letter_match.groups()
        return [f"{number}{suffix}"]
    if not value.isdigit():
        return []
    # Legal article numbers in this corpus have at most three digits. PDF
    # superscript footnote markers lose their formatting during extraction and
    # are glued to that number (``130`` + footnote ``82`` -> ``13082``).
    return [
        value[:end]
        for end in range(min(MAX_ARTICLE_DIGITS, len(value)), 0, -1)
    ]


def _definition_article(raw: str, previous_number: int | None) -> str:
    """Choose the most plausible definition using the document's article order."""
    candidates = _article_candidates(raw)
    if not candidates:
        return ""
    if previous_number is None:
        return candidates[0]

    def score(candidate: str) -> tuple[int, int, int]:
        number = int(re.match(r"\d+", candidate).group())
        # Articles normally stay at the same number for letter suffixes or
        # advance by one. Prefer that over a glued footnote interpretation.
        delta = number - previous_number
        return (
            0 if 0 <= delta <= 20 else 1,
            abs(delta),
            -len(candidate),
        )

    return min(candidates, key=score)


def build_graph(collection: Any) -> dict[str, Any]:
    """Build adjacency from document order and explicit legal article references."""
    result = collection.get(include=["documents", "metadatas"])
    ids = result["ids"]
    documents = result["documents"]
    metadatas = result["metadatas"]

    documents_by_id = dict(zip(ids, documents))
    metadata_by_id = dict(zip(ids, metadatas))
    edges: dict[str, dict[str, str]] = {chunk_id: {} for chunk_id in ids}

    # Structural edges: neighbouring chunks in the same source document.
    by_source: dict[str, list[str]] = defaultdict(list)
    for chunk_id, metadata in metadata_by_id.items():
        by_source[metadata.get("source", "unknown")].append(chunk_id)
    for source_ids in by_source.values():
        ordered = sorted(source_ids, key=_chunk_number)
        for left, right in zip(ordered, ordered[1:]):
            edges[left][right] = "next"
            edges[right][left] = "previous"

    # Semantic edges: a chunk mentioning "Art. X" points to the chunk where
    # that article is defined. Keep definitions scoped to a source where
    # possible, because article numbers repeat across different laws.
    definitions: dict[tuple[str, str], str] = {}
    global_definitions: dict[str, list[str]] = defaultdict(list)
    definitions_by_chunk: dict[str, list[str]] = defaultdict(list)
    definition_aliases: dict[tuple[str, str], set[str]] = defaultdict(set)
    for source, source_ids in by_source.items():
        previous_number: int | None = None
        for chunk_id in sorted(source_ids, key=_chunk_number):
            for raw_article in ARTICLE_DEFINITION_RE.findall(
                documents_by_id[chunk_id]
            ):
                key = _definition_article(raw_article, previous_number)
                if not key:
                    continue
                previous_number = int(re.match(r"\d+", key).group())
                definition_aliases[(source, raw_article.casefold())].add(key)
                canonical = definitions.setdefault((source, key), chunk_id)
                # Only the first definition is canonical. Later occurrences
                # are commonly tables of contents, appendices or transitional
                # material and must not produce false-positive article hits.
                if canonical == chunk_id:
                    if key not in definitions_by_chunk[chunk_id]:
                        definitions_by_chunk[chunk_id].append(key)
                    if chunk_id not in global_definitions[key]:
                        global_definitions[key].append(chunk_id)

    reference_edges = 0
    for chunk_id, text in documents_by_id.items():
        source = metadata_by_id[chunk_id].get("source", "unknown")
        for raw_article in set(ARTICLE_RE.findall(text)):
            raw_key = raw_article.casefold()
            aliases = definition_aliases.get((source, raw_key), set())
            local_candidates = {
                candidate
                for candidate in _article_candidates(raw_article)
                if (source, candidate) in definitions
            }
            if len(aliases) == 1:
                resolved = aliases
            elif raw_key in local_candidates:
                resolved = {raw_key}
            elif len(local_candidates) == 1:
                resolved = local_candidates
            else:
                # An ambiguous numeric token must not create several edges.
                resolved = set()

            for article in resolved:
                target = definitions[(source, article)]
                if target != chunk_id and not edges[chunk_id].get(
                    target, ""
                ).startswith("references"):
                    edges[chunk_id][target] = f"references Art. {article}"
                    reference_edges += 1

            if resolved:
                continue

            # Cross-law fallback is deliberately exact and only allowed when
            # the article number has one unique definition in the corpus.
            article = raw_key
            targets = []
            if len(global_definitions[article]) == 1:
                targets.extend(global_definitions[article])
            for target in targets:
                if target != chunk_id and not edges[chunk_id].get(
                    target, ""
                ).startswith("references"):
                    edges[chunk_id][target] = f"references Art. {article}"
                    reference_edges += 1

    return {
        "version": GRAPH_VERSION,
        "collection": collection.name,
        "nodes": len(ids),
        "edges": sum(len(v) for v in edges.values()),
        "reference_edges": reference_edges,
        "article_definitions": {
            chunk_id: sorted(articles)
            for chunk_id, articles in definitions_by_chunk.items()
        },
        "adjacency": {
            chunk_id: [
                {"id": neighbour, "kind": kind}
                for neighbour, kind in sorted(neighbours.items())
            ]
            for chunk_id, neighbours in edges.items()
        },
    }


def save_graph(graph: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def load_graph(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def vector_retrieve(
    collection: Any, query_embedding: list[float], limit: int
) -> list[dict[str, Any]]:
    hits = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {
            "id": chunk_id,
            "document": document,
            "metadata": metadata,
            "distance": distance,
            "via": "vector",
        }
        for chunk_id, document, metadata, distance in zip(
            hits["ids"][0],
            hits["documents"][0],
            hits["metadatas"][0],
            hits["distances"][0],
        )
    ]


def _search_tokens(text: str) -> list[str]:
    tokens = []
    for token in WORD_RE.findall(text.casefold()):
        if len(token) < 2 or token in STOPWORDS:
            continue
        tokens.append(token)
        # Small, transparent German normalization: nouns ending in "-keit"
        # often correspond to an adjective used in the same legal definition.
        if token.endswith("keit") and len(token) > 6:
            tokens.append(token[:-4])
    return tokens


def _source_terms(source: str) -> set[str]:
    """Extract searchable law abbreviations and SR numbers from a source name."""
    stem = Path(source).stem.casefold()
    parts = stem.split("_")
    return {
        token
        for token in parts[1:-1]
        if token and token not in {"de", "fr", "it"}
    }


def _source_matches_query(
    source_terms: set[str], query_tokens: set[str]
) -> bool:
    if source_terms & query_tokens:
        return True
    return any(
        any(
            query_token.startswith(alias) or alias.startswith(query_token)
            for query_token in query_tokens
            for alias in SOURCE_ALIASES.get(term, set())
        )
        for term in source_terms
    )


def build_article_index(
    collection: Any, graph: dict[str, Any]
) -> list[dict[str, Any]]:
    """Load normalized article-definition chunks into a small lexical index."""
    definitions = graph.get("article_definitions", {})
    ids = list(definitions)
    if not ids:
        return []
    index = []
    for start in range(0, len(ids), 500):
        result = collection.get(
            ids=ids[start : start + 500],
            include=["documents", "metadatas"],
        )
        index.extend(
            {
                "id": chunk_id,
                "document": document,
                "metadata": metadata,
                "articles": definitions.get(chunk_id, []),
                "tokens": _search_tokens(document),
                "source_terms": _source_terms(metadata.get("source", "")),
            }
            for chunk_id, document, metadata in zip(
                result["ids"], result["documents"], result["metadatas"]
            )
        )
    return index


def lexical_article_retrieve(
    article_index: list[dict[str, Any]], question: str, limit: int = 2
) -> list[dict[str, Any]]:
    """Rank article chunks with BM25-style lexical and law-name matching."""
    query_tokens = set(_search_tokens(question))
    if not query_tokens or not article_index or limit <= 0:
        return []

    document_frequency = Counter(
        token
        for entry in article_index
        for token in query_tokens & set(entry["tokens"])
    )
    average_length = (
        sum(len(entry["tokens"]) for entry in article_index) / len(article_index)
    )
    scored: list[tuple[float, str, dict[str, Any]]] = []
    for entry in article_index:
        frequencies = Counter(entry["tokens"])
        length = max(1, len(entry["tokens"]))
        score = 0.0
        for token in query_tokens:
            frequency = frequencies[token]
            if not frequency:
                continue
            count = document_frequency[token]
            inverse_frequency = math.log(
                1 + (len(article_index) - count + 0.5) / (count + 0.5)
            )
            denominator = frequency + 1.2 * (
                0.25 + 0.75 * length / max(1, average_length)
            )
            score += inverse_frequency * frequency * 2.2 / denominator

        content_score = score

        # A source hint only boosts a genuine topical match. It must never
        # turn every article of a named law into a candidate by itself.
        if content_score > 0 and _source_matches_query(
            entry["source_terms"], query_tokens
        ):
            score += 6.0

        # Prefer definitional clauses ("wer ... ist/besitzt/gilt") over later
        # provisions that merely mention the same legal concept repeatedly.
        text = entry["document"].casefold()
        for token in query_tokens:
            position = text.find(token)
            if position < 0:
                continue
            window = text[max(0, position - 100) : position + len(token) + 100]
            if re.search(r"\bwer\b", window) and re.search(
                r"\b(?:ist|besitzt|gilt|hat)\b", window
            ):
                score += 8.0
                break
        if content_score > 0 and score >= MIN_ARTICLE_SCORE:
            scored.append((score, entry["id"], entry))

    hits = []
    for score, _, entry in sorted(scored, key=lambda item: (-item[0], item[1]))[
        :limit
    ]:
        hits.append(
            {
                "id": entry["id"],
                "document": entry["document"],
                "metadata": entry["metadata"],
                "distance": None,
                "lexical_score": score,
                "via": "lexical-article",
            }
        )
    return hits


def _merge_hybrid_hits(
    vector_hits: list[dict[str, Any]],
    article_hits: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Merge rankings with classic reciprocal rank fusion and deduplicate."""
    merged: dict[str, dict[str, Any]] = {}
    scores: dict[str, float] = defaultdict(float)
    for rank, hit in enumerate(vector_hits, start=1):
        merged.setdefault(hit["id"], dict(hit))
        scores[hit["id"]] += 1.0 / (RRF_CONSTANT + rank)
    for rank, hit in enumerate(article_hits, start=1):
        if hit["id"] in merged:
            merged[hit["id"]]["via"] = "vector+lexical-article"
        else:
            merged[hit["id"]] = dict(hit)
        scores[hit["id"]] += 1.0 / (RRF_CONSTANT + rank)
    vector_ids = {hit["id"] for hit in vector_hits}
    return [
        merged[chunk_id]
        for chunk_id in sorted(
            scores,
            key=lambda item: (
                -scores[item],
                0 if item in vector_ids else 1,
                item,
            ),
        )
    ]


def graph_retrieve(
    collection: Any,
    query_embedding: list[float],
    graph: dict[str, Any],
    question: str = "",
    article_index: list[dict[str, Any]] | None = None,
    seed_limit: int = 3,
    article_limit: int = 2,
    context_limit: int = 6,
) -> list[dict[str, Any]]:
    """Merge vector and lexical article hits, then expand graph neighbours."""
    seeds = vector_retrieve(collection, query_embedding, seed_limit)
    article_hits = lexical_article_retrieve(
        article_index or [], question, article_limit
    )
    hybrid_hits = _merge_hybrid_hits(seeds, article_hits)
    selected = {
        hit["id"]: hit for hit in hybrid_hits[:context_limit]
    }
    neighbour_candidates: list[tuple[int, int, str, str]] = []

    kind_priority = {"references": 0, "previous": 1, "next": 1}
    for seed_rank, seed in enumerate(selected.values()):
        for edge in graph["adjacency"].get(seed["id"], []):
            kind = edge["kind"]
            priority = next(
                (value for prefix, value in kind_priority.items() if kind.startswith(prefix)),
                2,
            )
            neighbour_candidates.append((priority, seed_rank, edge["id"], kind))

    for _, _, neighbour_id, kind in sorted(neighbour_candidates):
        if len(selected) >= context_limit:
            break
        if neighbour_id in selected:
            continue
        result = collection.get(
            ids=[neighbour_id], include=["documents", "metadatas"]
        )
        if not result["ids"]:
            continue
        selected[neighbour_id] = {
            "id": neighbour_id,
            "document": result["documents"][0],
            "metadata": result["metadatas"][0],
            "distance": None,
            "via": kind,
        }

    return list(selected.values())


def estimate_tokens(text: str) -> int:
    """Cheap tokenizer-independent estimate suitable for relative comparisons."""
    return max(1, round(len(text) / 4))
