"""Small, transparent graph-retrieval helpers used by stage 4 and evaluation."""

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ARTICLE_RE = re.compile(
    r"\bArt\.\s*(\d{1,4}(?:(?:bis|ter|quater)|[a-z])?\d*)",
    re.IGNORECASE,
)
ARTICLE_DEFINITION_RE = re.compile(
    r"(?m)^\s*Art\.\s*(\d{1,4}(?:(?:bis|ter|quater)|[a-z])?\d*)",
    re.IGNORECASE,
)
ARTICLE_PARTS_RE = re.compile(
    r"^(\d{1,4})((?:bis|ter|quater)|[a-z])?(\d*)$", re.IGNORECASE
)


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
    match = ARTICLE_PARTS_RE.fullmatch(raw.casefold())
    if not match:
        return []
    number, suffix, footnote = match.groups()
    if suffix:
        return [f"{number}{suffix}"]
    if footnote:
        return [number]
    return [number[:end] for end in range(len(number), 0, -1)]


def _definition_article(raw: str, previous_number: int | None) -> str:
    """Choose the most plausible definition using the document's article order."""
    candidates = _article_candidates(raw)
    if not candidates or previous_number is None:
        return candidates[0] if candidates else raw.casefold()

    def score(candidate: str) -> tuple[int, int]:
        number = int(re.match(r"\d+", candidate).group())
        # Articles normally stay at the same number for letter suffixes or
        # advance by one. Prefer that over a glued footnote interpretation.
        delta = number - previous_number
        return (0 if delta >= 0 else 1, abs(delta))

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
    for source, source_ids in by_source.items():
        previous_number: int | None = None
        for chunk_id in sorted(source_ids, key=_chunk_number):
            for raw_article in ARTICLE_DEFINITION_RE.findall(
                documents_by_id[chunk_id]
            ):
                key = _definition_article(raw_article, previous_number)
                previous_number = int(re.match(r"\d+", key).group())
                definitions.setdefault((source, key), chunk_id)
                if chunk_id not in global_definitions[key]:
                    global_definitions[key].append(chunk_id)

    reference_edges = 0
    for chunk_id, text in documents_by_id.items():
        source = metadata_by_id[chunk_id].get("source", "unknown")
        raw_articles = ARTICLE_RE.findall(text)
        article_candidates = {
            candidate
            for raw_article in raw_articles
            for candidate in _article_candidates(raw_article)
        }
        for article in article_candidates:
            targets = []
            local_target = definitions.get((source, article))
            if local_target:
                targets.append(local_target)
            elif len(global_definitions[article]) == 1:
                targets.extend(global_definitions[article])
            for target in targets:
                if target != chunk_id and not edges[chunk_id].get(
                    target, ""
                ).startswith("references"):
                    edges[chunk_id][target] = f"references Art. {article}"
                    reference_edges += 1

    return {
        "version": 1,
        "collection": collection.name,
        "nodes": len(ids),
        "edges": sum(len(v) for v in edges.values()),
        "reference_edges": reference_edges,
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


def graph_retrieve(
    collection: Any,
    query_embedding: list[float],
    graph: dict[str, Any],
    seed_limit: int = 3,
    context_limit: int = 6,
) -> list[dict[str, Any]]:
    """Retrieve vector seeds, then expand their strongest graph neighbours."""
    seeds = vector_retrieve(collection, query_embedding, seed_limit)
    selected = {hit["id"]: hit for hit in seeds}
    neighbour_candidates: list[tuple[int, int, str, str]] = []

    kind_priority = {"references": 0, "previous": 1, "next": 1}
    for seed_rank, seed in enumerate(seeds):
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
