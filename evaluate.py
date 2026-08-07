"""Evaluate the cumulative RAG variants used throughout the workshop.

Examples:
    poetry run python evaluate.py --stage fixed
    poetry run python evaluate.py --stage semantic
    poetry run python evaluate.py --stage rerank
    poetry run python evaluate.py --stage graph
    poetry run python evaluate.py --methods semantic-vector rerank
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from statistics import mean
from typing import Any

from graph_retrieval import (
    GRAPH_VERSION,
    build_article_index,
    build_graph,
    estimate_tokens,
    graph_retrieve,
    load_graph,
    vector_retrieve,
)

METHOD_ORDER = ("fixed-vector", "semantic-vector", "rerank", "graph")
STAGE_METHODS = {
    "fixed": ("fixed-vector",),
    "semantic": ("fixed-vector", "semantic-vector"),
    "rerank": ("fixed-vector", "semantic-vector", "rerank"),
    "graph": METHOD_ORDER,
}

sys.excepthook = lambda exc_type, exc, _: sys.exit(f"{exc_type.__name__}: {exc}")

# Redirected stdout on Windows defaults to cp1252; model output needs UTF-8.
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
CITATION_RE = re.compile(
    r"\[(?P<source>SR_[^\]\s]+\.md)\s+Art\.\s*"
    r"(?P<article>\d+(?:(?:bis|ter|quater)|[a-z])?\d*)"
    r"(?P<range>\s*[-–—]\s*\d+(?:(?:bis|ter|quater)|[a-z])?\d*)?"
    r"(?:\s+[^\]]*)?\]",
    re.IGNORECASE,
)


def normalized(text: str) -> str:
    return " ".join(text.casefold().split())


def resolve_methods(stage: str, methods: list[str] | None) -> tuple[str, ...]:
    """Resolve an accumulating workshop stage or an explicit method list."""
    selected = methods if methods else list(STAGE_METHODS[stage])
    return tuple(method for method in METHOD_ORDER if method in selected)


class Reranker:
    """Cache one local cross-encoder or call a compatible remote endpoint."""

    def __init__(self, model: str, url: str, api_key: str) -> None:
        self.model_name = model
        self.url = url
        self.api_key = api_key
        self._model: Any | None = None

    def score(self, question: str, documents: list[str]) -> list[float]:
        if self.url:
            import httpx

            response = httpx.post(
                self.url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model_name,
                    "query": question,
                    "documents": documents,
                },
                timeout=60,
            )
            if response.status_code != 200:
                raise RuntimeError(
                    f"Remote reranker '{self.model_name}' at {self.url} "
                    f"answered {response.status_code}: {response.text[:200]}"
                )
            scores = [0.0] * len(documents)
            for item in response.json()["results"]:
                score = item.get("relevance_score", item.get("score", 0.0))
                scores[item["index"]] = float(score)
            return scores

        if self._model is None:
            try:
                from sentence_transformers import CrossEncoder

                self._model = CrossEncoder(self.model_name)
            except (ImportError, OSError, ValueError) as exc:
                raise RuntimeError(
                    f"Could not load re-ranker '{self.model_name}'. Install the "
                    "project dependencies; the first local run may also need "
                    "internet access. Alternatively configure RERANK_URL."
                ) from exc
        pairs = [(question, document) for document in documents]
        return [
            float(score)
            for score in self._model.predict(pairs, show_progress_bar=False)
        ]


def rerank_hits(
    question: str,
    candidates: list[dict[str, Any]],
    keep: int,
    scorer: Reranker,
) -> list[dict[str, Any]]:
    """Order over-fetched vector candidates with the cross-encoder."""
    scores = scorer.score(question, [hit["document"] for hit in candidates])
    ranked = sorted(
        zip(candidates, scores), key=lambda item: item[1], reverse=True
    )
    return [
        {**hit, "rerank_score": score, "via": "rerank"}
        for hit, score in ranked[:keep]
    ]


def expected_article_pairs(case: dict[str, Any]) -> set[tuple[str, str]]:
    return {
        (item["source"].casefold(), item["article"].casefold())
        for item in case["expected_articles"]
    }


def article_rank(
    hits: list[dict[str, Any]],
    expected_source: str,
    expected_article: str,
    article_definitions: dict[str, list[str]],
) -> int | None:
    """Return the one-based rank of an expected article definition."""
    for rank, hit in enumerate(hits, start=1):
        source = hit["metadata"].get("source", "")
        definitions = article_definitions.get(hit["id"], [])
        if source.casefold() == expected_source and expected_article in definitions:
            return rank
    return None


def score_retrieval(
    case: dict[str, Any],
    hits: list[dict[str, Any]],
    article_definitions: dict[str, list[str]],
) -> dict[str, float]:
    sources = {hit["metadata"].get("source", "") for hit in hits}
    expected_sources = set(case["expected_sources"])
    expected_articles = expected_article_pairs(case)
    ranks = [
        article_rank(hits, source, article, article_definitions)
        for source, article in sorted(expected_articles)
    ]
    document_context = normalized("\n".join(hit["document"] for hit in hits))
    prompt_context = render_context(hits)
    expected_terms = [normalized(term) for term in case["expected_terms"]]

    return {
        "source_recall": (
            len(sources & expected_sources) / len(expected_sources)
            if expected_sources
            else 1.0
        ),
        "article_hit_at_k": float(any(rank is not None for rank in ranks)),
        "article_recall_at_k": (
            sum(rank is not None for rank in ranks) / len(ranks) if ranks else 1.0
        ),
        "article_mrr": (
            mean(1 / rank if rank is not None else 0.0 for rank in ranks)
            if ranks
            else 1.0
        ),
        # Diagnostic only: this describes retrieved vocabulary, not answer quality.
        "term_coverage": (
            sum(term in document_context for term in expected_terms)
            / len(expected_terms)
            if expected_terms
            else 1.0
        ),
        "document_context_tokens": estimate_tokens(document_context),
        "prompt_context_tokens": estimate_tokens(prompt_context),
    }


def render_context(hits: list[dict[str, Any]]) -> str:
    parts = []
    for hit in hits:
        source = hit["metadata"].get("source", "unknown")
        parts.append(
            f"[Quelle: {source}; Chunk: {hit['id']}]\n{hit['document']}"
        )
    return "\n\n".join(parts)


def answer_question(
    client: Any,
    model: str,
    question: str,
    hits: list[dict[str, Any]],
) -> str:
    context = render_context(hits)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Beantworte die Frage ausschliesslich anhand des Kontexts. "
                    "Belege jede wesentliche Aussage direkt mit einer Quellenangabe "
                    "im exakten Format [DATEINAME Art. ARTIKEL], zum Beispiel "
                    "[SR_220_OR_de.md Art. 335b]. Erfinde keine Quellen oder Artikel. "
                    "Wenn der Kontext nicht reicht, sage das ausdrücklich. "
                    "Dies ist keine individuelle Rechtsberatung."
                ),
            },
            {"role": "user", "content": f"Kontext:\n{context}\n\nFrage: {question}"},
        ],
    )
    return response.choices[0].message.content or ""


def cited_article_pairs(answer: str) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for match in CITATION_RE.finditer(answer):
        source = match.group("source").casefold()
        start = normalized_cited_article(match.group("article"))
        range_text = match.group("range")
        if not range_text:
            pairs.add((source, start))
            continue

        end_raw = re.sub(r"^\s*[-–—]\s*", "", range_text)
        end = normalized_cited_article(end_raw)
        start_match = re.fullmatch(r"(\d+)([a-z]+)?", start)
        end_match = re.fullmatch(r"(\d+)([a-z]+)?", end)
        if (
            start_match
            and end_match
            and not start_match.group(2)
            and not end_match.group(2)
        ):
            first, last = int(start), int(end)
            if first <= last <= first + 50:
                pairs.update((source, str(article)) for article in range(first, last + 1))
                continue
        pairs.update({(source, start), (source, end)})
    return pairs


def normalized_cited_article(raw: str) -> str:
    """Remove footnote digits glued to a cited Fedlex article number."""
    value = raw.casefold()
    letter_match = re.fullmatch(
        r"(\d{1,4})((?:bis|ter|quater)|[a-z])\d*", value
    )
    if letter_match:
        return "".join(letter_match.groups())
    # Four digits can be a genuine article number (the OR reaches Art. 1186).
    # Five or more digits are a PDF footnote glued to a one- to four-digit
    # article; the corpus' observed form uses a three-digit base here.
    if value.isdigit() and len(value) > 4:
        return value[:3]
    return value


def contains_non_negated(text: str, phrase: str) -> bool:
    """Return true when a phrase occurs without negation in its clause."""
    phrase = normalized(phrase)
    negations = {
        "falsch",
        "kein",
        "keine",
        "keinen",
        "keinem",
        "keiner",
        "keinesfalls",
        "nicht",
        "nie",
        "unwahr",
        "weder",
    }
    start = 0
    while (index := text.find(phrase, start)) >= 0:
        clause_start = max(
            text.rfind(separator, 0, index) for separator in ".!?;"
        )
        comma = text.rfind(",", clause_start + 1, index)
        after_comma = text[comma + 1 : index].strip() if comma >= 0 else ""
        if comma >= 0 and not after_comma.startswith(
            ("dass ", "ob ", "weil ", "wenn ")
        ):
            clause_start = comma
        clause_prefix = text[clause_start + 1 : index]
        prefix_words = set(
            re.findall(r"[0-9a-zäöüàâéèêëîïôûüç]+", clause_prefix)
        )
        if not (prefix_words & negations):
            return True
        start = index + len(phrase)
    return False


def retrieved_article_pairs(
    hits: list[dict[str, Any]], article_definitions: dict[str, list[str]]
) -> set[tuple[str, str]]:
    return {
        (hit["metadata"].get("source", "").casefold(), article.casefold())
        for hit in hits
        for article in article_definitions.get(hit["id"], [])
    }


def score_answer(
    case: dict[str, Any],
    answer: str,
    hits: list[dict[str, Any]],
    article_definitions: dict[str, list[str]],
) -> dict[str, float]:
    answer_text = normalized(answer)
    required_facts = case["required_facts"]
    covered_facts = [
        all(
            any(contains_non_negated(answer_text, alternative) for alternative in group)
            for group in fact["all_of"]
        )
        for fact in required_facts
    ]
    expected_citations = expected_article_pairs(case)
    actual_citations = cited_article_pairs(answer)
    correct_citations = actual_citations & expected_citations
    grounded_citations = actual_citations & retrieved_article_pairs(
        hits, article_definitions
    )

    return {
        "fact_coverage": (
            sum(covered_facts) / len(covered_facts) if covered_facts else 1.0
        ),
        "expected_citation_precision": (
            len(correct_citations) / len(actual_citations)
            if actual_citations
            else 0.0
        ),
        "citation_grounding": (
            len(grounded_citations) / len(actual_citations)
            if actual_citations
            else 0.0
        ),
        "citation_completeness": (
            len(correct_citations) / len(expected_citations)
            if expected_citations
            else 1.0
        ),
        "answer_tokens": estimate_tokens(answer),
    }


def render_report(
    rows: list[dict[str, Any]],
    cases: list[dict[str, Any]],
    full_corpus_tokens: int,
    collection_names: dict[str, str],
    context_k: int,
) -> str:
    method_order = list(dict.fromkeys(row["method"] for row in rows))
    lines = [
        "# RAG evaluation",
        "",
        f"- Methods: **{', '.join(method_order)}**",
        f"- Collections: {', '.join(f'`{key}={value}`' for key, value in collection_names.items())}",
        f"- Shared context budget: **{context_k} chunks**",
        f"- Full corpus: approximately **{full_corpus_tokens:,} tokens**",
        "- Token counts are estimated as characters / 4.",
        "- Term coverage is shown only as a retrieval diagnostic; it is not an "
        "answer-quality score.",
        "",
        "## Retrieval",
        "",
        "| Question | Method | Source recall | Article Hit@K | Article Recall@K | Article MRR | Term coverage (diagnostic) | Document tokens | Prompt-context tokens |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['id']} | {row['method']} | "
            f"{row['source_recall']:.0%} | {row['article_hit_at_k']:.0%} | "
            f"{row['article_recall_at_k']:.0%} | {row['article_mrr']:.2f} | "
            f"{row['term_coverage']:.0%} | "
            f"{row['document_context_tokens']:,} | "
            f"{row['prompt_context_tokens']:,} |"
        )

    lines.extend(
        [
            "",
            "## Answers",
            "",
            "| Question | Method | Fact coverage | Expected-citation precision | Citation grounding | Citation completeness | Answer tokens |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['id']} | {row['method']} | "
            f"{row['fact_coverage']:.0%} | "
            f"{row['expected_citation_precision']:.0%} | "
            f"{row['citation_grounding']:.0%} | "
            f"{row['citation_completeness']:.0%} | {row['answer_tokens']:,} |"
        )

    lines.extend(["", "## Summary", ""])
    for method in method_order:
        method_rows = [row for row in rows if row["method"] == method]
        avg_context_tokens = mean(
            row["prompt_context_tokens"] for row in method_rows
        )
        savings = 1 - avg_context_tokens / full_corpus_tokens
        lines.append(
            f"- **{method}:** article recall@K "
            f"{mean(row['article_recall_at_k'] for row in method_rows):.1%}, "
            f"MRR {mean(row['article_mrr'] for row in method_rows):.2f}, "
            f"fact coverage {mean(row['fact_coverage'] for row in method_rows):.1%}, "
            f"expected-citation precision "
            f"{mean(row['expected_citation_precision'] for row in method_rows):.1%}, "
            f"citation grounding "
            f"{mean(row['citation_grounding'] for row in method_rows):.1%}, "
            f"citation completeness "
            f"{mean(row['citation_completeness'] for row in method_rows):.1%}, "
            f"average context {avg_context_tokens:,.0f} tokens, "
            f"corpus-token savings {savings:.2%}."
        )

    lines.extend(["", "## Strategic token perspective", ""])
    if "semantic-vector" in method_order and "graph" in method_order:
        vector_tokens = mean(
            row["prompt_context_tokens"]
            for row in rows
            if row["method"] == "semantic-vector"
        )
        graph_tokens = mean(
            row["prompt_context_tokens"]
            for row in rows
            if row["method"] == "graph"
        )
        delta = (graph_tokens - vector_tokens) / vector_tokens
        lines.extend(
            [
                "All methods receive the same final chunk budget. Because chunking "
                "and retrieval differ, their actual token counts can still differ.",
                "",
                f"In this run GraphRAG used **{delta:+.1%}** context tokens compared "
                "with semantic Vector-RAG. Interpret this together with retrieval, "
                "fact coverage and citation quality.",
            ]
        )
    else:
        lines.append(
            "All selected methods receive the same final chunk budget. Their actual "
            "token counts can differ because the retrieved chunks have different lengths."
        )
    lines.extend(["", "## Answer details", ""])
    cases_by_id = {case["id"]: case for case in cases}
    for row in rows:
        case = cases_by_id[row["id"]]
        lines.extend(
            [
                f"### {row['id']} — {row['method']}",
                "",
                f"**Reference:** {case['reference_answer']}",
                "",
                f"**Generated:** {row['answer']}",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    import chromadb
    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Evaluate cumulative workshop RAG stages or selected methods."
    )
    parser.add_argument(
        "--questions", type=Path, default=ROOT / "evaluation" / "questions.json"
    )
    parser.add_argument(
        "--output", type=Path, default=ROOT / "evaluation" / "report.md"
    )
    parser.add_argument(
        "--stage",
        choices=tuple(STAGE_METHODS),
        default="graph",
        help=(
            "Cumulative workshop stage: fixed; semantic adds semantic-vector; "
            "rerank adds the cross-encoder; graph adds GraphRAG (default: graph)."
        ),
    )
    parser.add_argument(
        "--methods",
        nargs="+",
        choices=METHOD_ORDER,
        help="Explicit methods to run; overrides --stage.",
    )
    parser.add_argument(
        "--fixed-collection", default=os.getenv("RAG_FIXED_COLLECTION", "rag_fixed")
    )
    parser.add_argument(
        "--collection",
        "--semantic-collection",
        dest="semantic_collection",
        default=os.getenv("RAG_COLLECTION", "rag_semantic"),
        help="Stage-3 semantic collection (default: rag_semantic).",
    )
    parser.add_argument(
        "--context-k",
        type=int,
        default=6,
        help="Shared final chunk budget for every selected RAG (default: 6).",
    )
    parser.add_argument("--graph-seed-k", type=int, default=3)
    parser.add_argument(
        "--rerank-candidates",
        type=int,
        default=10,
        help="Vector candidates scored by the reranker (default: 10).",
    )
    parser.add_argument(
        "--article-k",
        type=int,
        default=2,
        help="Lexical article candidates merged into GraphRAG (default: 2).",
    )
    args = parser.parse_args()
    selected_methods = resolve_methods(args.stage, args.methods)
    if args.context_k < 1:
        parser.error("--context-k must be at least 1")
    if not 1 <= args.graph_seed_k <= args.context_k:
        parser.error("--graph-seed-k must be between 1 and --context-k")
    if not 0 <= args.article_k <= args.context_k:
        parser.error("--article-k must be between 0 and --context-k")
    if args.rerank_candidates < args.context_k:
        parser.error("--rerank-candidates must be at least --context-k")

    client = OpenAI(
        base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
        api_key=os.getenv("LLM_API_KEY", "ollama"),
    )
    embed_model = os.getenv("EMBED_MODEL", "bge-m3")
    chat_model = os.getenv("LLM_MODEL", "llama3.2")
    collections: dict[str, Any] = {}
    definitions: dict[str, dict[str, list[str]]] = {}
    if "fixed-vector" in selected_methods:
        fixed = chromadb.PersistentClient(path=str(ROOT / ".chroma-2")).get_collection(
            args.fixed_collection, embedding_function=None
        )
        collections["fixed"] = fixed
        definitions["fixed"] = build_graph(fixed)["article_definitions"]

    needs_semantic = any(
        method in selected_methods for method in ("semantic-vector", "rerank", "graph")
    )
    graph: dict[str, Any] | None = None
    article_index: list[dict[str, Any]] = []
    if needs_semantic:
        semantic = chromadb.PersistentClient(
            path=str(ROOT / ".chroma-3")
        ).get_collection(args.semantic_collection, embedding_function=None)
        collections["semantic"] = semantic
        if "graph" in selected_methods:
            graph = load_graph(
                ROOT / ".chroma-3" / f"{args.semantic_collection}_graph.json"
            )
            if graph.get("version") != GRAPH_VERSION:
                sys.exit(
                    "Graph format is outdated. Rebuild it with: "
                    "poetry run python rag-4a-graph.py"
                )
        else:
            graph = build_graph(semantic)
        article_definitions = graph.get("article_definitions")
        if not isinstance(article_definitions, dict):
            sys.exit("Could not determine normalized article definitions.")
        definitions["semantic"] = article_definitions
        if "graph" in selected_methods:
            article_index = build_article_index(semantic, graph)

    reranker = None
    if "rerank" in selected_methods:
        reranker = Reranker(
            os.getenv("RERANK_MODEL", "BAAI/bge-reranker-v2-m3"),
            os.getenv("RERANK_URL", ""),
            os.getenv("LLM_API_KEY", ""),
        )
    cases = json.loads(args.questions.read_text(encoding="utf-8"))

    corpus_collection = collections.get("semantic", collections.get("fixed"))
    corpus = corpus_collection.get(include=["documents"])
    full_corpus_text = normalized("\n".join(corpus["documents"]))
    full_corpus_tokens = estimate_tokens(full_corpus_text)
    rows: list[dict[str, Any]] = []

    for number, case in enumerate(cases, start=1):
        embedding = client.embeddings.create(
            model=embed_model, input=[case["question"]]
        ).data[0].embedding
        methods: dict[str, list[dict[str, Any]]] = {}
        if "fixed-vector" in selected_methods:
            methods["fixed-vector"] = vector_retrieve(
                collections["fixed"], embedding, args.context_k
            )
        if "semantic-vector" in selected_methods:
            methods["semantic-vector"] = vector_retrieve(
                collections["semantic"], embedding, args.context_k
            )
        if "rerank" in selected_methods:
            candidates = vector_retrieve(
                collections["semantic"], embedding, args.rerank_candidates
            )
            methods["rerank"] = rerank_hits(
                case["question"], candidates, args.context_k, reranker
            )
        if "graph" in selected_methods:
            methods["graph"] = graph_retrieve(
                collection=collections["semantic"],
                query_embedding=embedding,
                graph=graph,
                question=case["question"],
                article_index=article_index,
                seed_limit=args.graph_seed_k,
                article_limit=args.article_k,
                context_limit=args.context_k,
            )
        for method, hits in methods.items():
            answer = answer_question(
                client, chat_model, case["question"], hits
            )
            row: dict[str, Any] = {
                "id": case["id"],
                "method": method,
                "answer": answer,
            }
            method_definitions = definitions[
                "fixed" if method == "fixed-vector" else "semantic"
            ]
            row.update(score_retrieval(case, hits, method_definitions))
            row.update(score_answer(case, answer, hits, method_definitions))
            rows.append(row)
        print(f"[evaluate] {number}/{len(cases)} {case['id']}")

    report = render_report(
        rows,
        cases,
        full_corpus_tokens,
        {
            key: value.name
            for key, value in collections.items()
        },
        args.context_k,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print()
    print(report)
    print(f"[evaluate] wrote {args.output}")


if __name__ == "__main__":
    main()
