"""Evaluate Vector-RAG and GraphRAG retrieval, answers, citations and tokens.

Run after rag-3a-ingest.py and rag-4a-graph.py:
    poetry run python evaluate.py
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
    article_definition_candidates,
    estimate_tokens,
    graph_retrieve,
    load_graph,
    vector_retrieve,
)

sys.excepthook = lambda exc_type, exc, _: sys.exit(f"{exc_type.__name__}: {exc}")

ROOT = Path(__file__).resolve().parent
CITATION_RE = re.compile(
    r"\[(?P<source>SR_[^\]\s]+\.md)\s+Art\.\s*"
    r"(?P<article>\d{1,4}(?:(?:bis|ter|quater)|[a-z])?)\]",
    re.IGNORECASE,
)


def normalized(text: str) -> str:
    return " ".join(text.casefold().split())


def expected_article_pairs(case: dict[str, Any]) -> set[tuple[str, str]]:
    return {
        (item["source"].casefold(), item["article"].casefold())
        for item in case["expected_articles"]
    }


def article_rank(
    hits: list[dict[str, Any]], expected_source: str, expected_article: str
) -> int | None:
    """Return the one-based rank of an expected article definition."""
    for rank, hit in enumerate(hits, start=1):
        source = hit["metadata"].get("source", "")
        definitions = article_definition_candidates(hit["document"])
        if source.casefold() == expected_source and expected_article in definitions:
            return rank
    return None


def score_retrieval(
    case: dict[str, Any], hits: list[dict[str, Any]]
) -> dict[str, float]:
    sources = {hit["metadata"].get("source", "") for hit in hits}
    expected_sources = set(case["expected_sources"])
    expected_articles = expected_article_pairs(case)
    ranks = [
        article_rank(hits, source, article)
        for source, article in sorted(expected_articles)
    ]
    context = normalized("\n".join(hit["document"] for hit in hits))
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
            sum(term in context for term in expected_terms) / len(expected_terms)
            if expected_terms
            else 1.0
        ),
        "context_tokens": estimate_tokens(context),
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
    return {
        (match.group("source").casefold(), match.group("article").casefold())
        for match in CITATION_RE.finditer(answer)
    }


def score_answer(case: dict[str, Any], answer: str) -> dict[str, float]:
    answer_text = normalized(answer)
    required_facts = case["required_facts"]
    covered_facts = [
        any(normalized(alternative) in answer_text for alternative in fact["alternatives"])
        for fact in required_facts
    ]
    expected_citations = expected_article_pairs(case)
    actual_citations = cited_article_pairs(answer)
    correct_citations = actual_citations & expected_citations

    return {
        "fact_coverage": (
            sum(covered_facts) / len(covered_facts) if covered_facts else 1.0
        ),
        "citation_accuracy": (
            len(correct_citations) / len(actual_citations)
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
    collection_name: str,
    context_k: int,
) -> str:
    lines = [
        "# RAG evaluation",
        "",
        f"- Collection: `{collection_name}`",
        f"- Shared context budget: **{context_k} chunks**",
        f"- Full corpus: approximately **{full_corpus_tokens:,} tokens**",
        "- Token counts are estimated as characters / 4.",
        "- Term coverage is shown only as a retrieval diagnostic; it is not an "
        "answer-quality score.",
        "",
        "## Retrieval",
        "",
        "| Question | Method | Source recall | Article Hit@K | Article Recall@K | Article MRR | Term coverage (diagnostic) | Context tokens |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['id']} | {row['method']} | "
            f"{row['source_recall']:.0%} | {row['article_hit_at_k']:.0%} | "
            f"{row['article_recall_at_k']:.0%} | {row['article_mrr']:.2f} | "
            f"{row['term_coverage']:.0%} | {row['context_tokens']:,} |"
        )

    lines.extend(
        [
            "",
            "## Answers",
            "",
            "| Question | Method | Fact coverage | Citation accuracy | Citation completeness | Answer tokens |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['id']} | {row['method']} | "
            f"{row['fact_coverage']:.0%} | {row['citation_accuracy']:.0%} | "
            f"{row['citation_completeness']:.0%} | {row['answer_tokens']:,} |"
        )

    lines.extend(["", "## Summary", ""])
    for method in ("vector", "graph"):
        method_rows = [row for row in rows if row["method"] == method]
        avg_context_tokens = mean(row["context_tokens"] for row in method_rows)
        savings = 1 - avg_context_tokens / full_corpus_tokens
        lines.append(
            f"- **{method}:** article recall@K "
            f"{mean(row['article_recall_at_k'] for row in method_rows):.1%}, "
            f"MRR {mean(row['article_mrr'] for row in method_rows):.2f}, "
            f"fact coverage {mean(row['fact_coverage'] for row in method_rows):.1%}, "
            f"citation accuracy "
            f"{mean(row['citation_accuracy'] for row in method_rows):.1%}, "
            f"citation completeness "
            f"{mean(row['citation_completeness'] for row in method_rows):.1%}, "
            f"average context {avg_context_tokens:,.0f} tokens, "
            f"corpus-token savings {savings:.2%}."
        )

    vector_tokens = mean(
        row["context_tokens"] for row in rows if row["method"] == "vector"
    )
    graph_tokens = mean(
        row["context_tokens"] for row in rows if row["method"] == "graph"
    )
    delta = (graph_tokens - vector_tokens) / vector_tokens
    lines.extend(
        [
            "",
            "## Strategic token perspective",
            "",
            "Both methods receive the same chunk budget. Because chunks have different "
            "lengths, their actual token counts can still differ.",
            "",
            f"In this run GraphRAG used **{delta:+.1%}** context tokens compared "
            "with Vector-RAG. Interpret this together with article retrieval, "
            "fact coverage and citation quality.",
            "",
            "## Answer details",
            "",
        ]
    )
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
        description="Evaluate Vector-RAG vs GraphRAG retrieval and answers."
    )
    parser.add_argument(
        "--questions", type=Path, default=ROOT / "evaluation" / "questions.json"
    )
    parser.add_argument(
        "--output", type=Path, default=ROOT / "evaluation" / "report.md"
    )
    parser.add_argument(
        "--collection", default=os.getenv("RAG_COLLECTION", "rag_semantic")
    )
    parser.add_argument(
        "--context-k",
        type=int,
        default=4,
        help="Shared chunk budget for Vector-RAG and GraphRAG (default: 4).",
    )
    parser.add_argument("--graph-seed-k", type=int, default=3)
    args = parser.parse_args()
    if args.context_k < 1:
        parser.error("--context-k must be at least 1")
    if not 1 <= args.graph_seed_k <= args.context_k:
        parser.error("--graph-seed-k must be between 1 and --context-k")

    client = OpenAI(
        base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
        api_key=os.getenv("LLM_API_KEY", "ollama"),
    )
    embed_model = os.getenv("EMBED_MODEL", "bge-m3")
    chat_model = os.getenv("LLM_MODEL", "llama3.2")
    collection = chromadb.PersistentClient(
        path=str(ROOT / ".chroma")
    ).get_collection(args.collection, embedding_function=None)
    graph = load_graph(ROOT / ".chroma" / f"{args.collection}_graph.json")
    cases = json.loads(args.questions.read_text(encoding="utf-8"))

    corpus = collection.get(include=["documents"])
    full_corpus_text = normalized("\n".join(corpus["documents"]))
    full_corpus_tokens = estimate_tokens(full_corpus_text)
    rows: list[dict[str, Any]] = []

    for number, case in enumerate(cases, start=1):
        embedding = client.embeddings.create(
            model=embed_model, input=[case["question"]]
        ).data[0].embedding
        methods = {
            "vector": vector_retrieve(collection, embedding, args.context_k),
            "graph": graph_retrieve(
                collection,
                embedding,
                graph,
                args.graph_seed_k,
                args.context_k,
            ),
        }
        for method, hits in methods.items():
            answer = answer_question(
                client, chat_model, case["question"], hits
            )
            row: dict[str, Any] = {
                "id": case["id"],
                "method": method,
                "answer": answer,
            }
            row.update(score_retrieval(case, hits))
            row.update(score_answer(case, answer))
            rows.append(row)
        print(f"[evaluate] {number}/{len(cases)} {case['id']}")

    report = render_report(
        rows, cases, full_corpus_tokens, args.collection, args.context_k
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print()
    print(report)
    print(f"[evaluate] wrote {args.output}")


if __name__ == "__main__":
    main()
