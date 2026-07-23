"""Compare Vector-RAG and GraphRAG retrieval quality and token footprint.

The evaluation is retrieval-only: it does not ask the chat model to judge its
own answers. It measures source recall, expected-term coverage, context size,
and estimated token savings relative to sending the complete corpus.

Run after rag-3a-ingest.py and rag-4a-graph.py:
    poetry run python evaluate.py
"""

import argparse
import json
import os
import sys
from pathlib import Path
from statistics import mean
from typing import Any

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

from graph_retrieval import (
    estimate_tokens,
    graph_retrieve,
    load_graph,
    vector_retrieve,
)


load_dotenv()
sys.excepthook = lambda exc_type, exc, _: sys.exit(f"{exc_type.__name__}: {exc}")

ROOT = Path(__file__).resolve().parent


def normalized(text: str) -> str:
    return " ".join(text.casefold().split())


def score_case(case: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, float]:
    sources = {hit["metadata"].get("source", "") for hit in hits}
    expected_sources = set(case["expected_sources"])
    context = normalized("\n".join(hit["document"] for hit in hits))
    expected_terms = [normalized(term) for term in case["expected_terms"]]

    return {
        "source_recall": (
            len(sources & expected_sources) / len(expected_sources)
            if expected_sources
            else 1.0
        ),
        "term_coverage": (
            sum(term in context for term in expected_terms) / len(expected_terms)
            if expected_terms
            else 1.0
        ),
        "context_tokens": estimate_tokens(context),
    }


def render_report(
    rows: list[dict[str, Any]], full_corpus_tokens: int, collection_name: str
) -> str:
    lines = [
        "# RAG retrieval evaluation",
        "",
        f"- Collection: `{collection_name}`",
        f"- Full corpus: approximately **{full_corpus_tokens:,} tokens**",
        "- Token counts are estimated as characters / 4.",
        "- Source recall and term coverage are deterministic retrieval metrics.",
        "",
        "| Question | Method | Source recall | Term coverage | Context tokens | Savings vs full corpus |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        savings = 1 - row["context_tokens"] / full_corpus_tokens
        lines.append(
            f"| {row['id']} | {row['method']} | "
            f"{row['source_recall']:.0%} | {row['term_coverage']:.0%} | "
            f"{row['context_tokens']:,} | {savings:.2%} |"
        )

    lines.extend(["", "## Summary", ""])
    for method in ("vector", "graph"):
        method_rows = [row for row in rows if row["method"] == method]
        avg_tokens = mean(row["context_tokens"] for row in method_rows)
        savings = 1 - avg_tokens / full_corpus_tokens
        lines.append(
            f"- **{method}:** source recall "
            f"{mean(row['source_recall'] for row in method_rows):.1%}, "
            f"term coverage {mean(row['term_coverage'] for row in method_rows):.1%}, "
            f"average context {avg_tokens:,.0f} tokens, "
            f"estimated corpus-token savings {savings:.2%}."
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
            "RAG saves tokens by selecting a small context instead of sending the "
            "complete corpus. GraphRAG may use slightly more context than plain "
            "Vector-RAG because it follows relationships, but that overhead is "
            "useful only if source recall or term coverage improves.",
            "",
            f"In this run GraphRAG used **{delta:+.1%}** context tokens compared "
            "with Vector-RAG. Interpret this together with the quality metrics, "
            "not as an isolated optimization target.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate Vector-RAG vs GraphRAG retrieval."
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
    parser.add_argument("--vector-k", type=int, default=4)
    parser.add_argument("--graph-seed-k", type=int, default=3)
    parser.add_argument("--graph-context-k", type=int, default=6)
    args = parser.parse_args()

    client = OpenAI(
        base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
        api_key=os.getenv("LLM_API_KEY", "ollama"),
    )
    embed_model = os.getenv("EMBED_MODEL", "bge-m3")
    collection = chromadb.PersistentClient(
        path=str(ROOT / ".chroma")
    ).get_collection(args.collection, embedding_function=None)
    graph = load_graph(ROOT / ".chroma" / f"{args.collection}_graph.json")
    cases = json.loads(args.questions.read_text(encoding="utf-8"))

    corpus = collection.get(include=["documents"])
    full_corpus_text = "\n".join(corpus["documents"])
    full_corpus_tokens = estimate_tokens(full_corpus_text)
    rows: list[dict[str, Any]] = []

    for number, case in enumerate(cases, start=1):
        embedding = client.embeddings.create(
            model=embed_model, input=[case["question"]]
        ).data[0].embedding
        methods = {
            "vector": vector_retrieve(collection, embedding, args.vector_k),
            "graph": graph_retrieve(
                collection,
                embedding,
                graph,
                args.graph_seed_k,
                args.graph_context_k,
            ),
        }
        for method, hits in methods.items():
            row = {"id": case["id"], "method": method}
            row.update(score_case(case, hits))
            rows.append(row)
        print(f"[evaluate] {number}/{len(cases)} {case['id']}")

    report = render_report(rows, full_corpus_tokens, args.collection)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print()
    print(report)
    print(f"[evaluate] wrote {args.output}")


if __name__ == "__main__":
    main()
