import unittest

from evaluate import cited_article_pairs, score_answer, score_retrieval
from graph_retrieval import (
    _merge_hybrid_hits,
    build_graph,
    lexical_article_retrieve,
)


CASE = {
    "expected_sources": ["SR_220_OR_de.md"],
    "expected_articles": [
        {"source": "SR_220_OR_de.md", "article": "335b"},
    ],
    "expected_terms": ["probezeit", "erster monat", "drei monate"],
    "required_facts": [
        {
            "description": "Die Probezeit beträgt einen Monat.",
            "all_of": [["erster monat", "erste monat", "einen monat"]],
        },
        {
            "description": "Die Probezeit dauert höchstens drei Monate.",
            "all_of": [["höchstens drei monate", "maximal drei monate"]],
        },
    ],
}


class EvaluationScoringTest(unittest.TestCase):
    def setUp(self) -> None:
        self.definitions = {"or::0": ["335b"]}

    def test_article_metrics_handle_glued_fedlex_footnote(self) -> None:
        hits = [
            {
                "id": "or::0",
                "document": (
                    "Art. 335b186\n"
                    "Als Probezeit gilt der erste Monat; höchstens drei Monate."
                ),
                "metadata": {"source": "SR_220_OR_de.md"},
            }
        ]

        score = score_retrieval(CASE, hits, self.definitions)

        self.assertEqual(score["article_hit_at_k"], 1.0)
        self.assertEqual(score["article_recall_at_k"], 1.0)
        self.assertEqual(score["article_mrr"], 1.0)
        self.assertGreater(
            score["prompt_context_tokens"], score["document_context_tokens"]
        )

    def test_article_138_does_not_match_expected_article_13(self) -> None:
        case = {
            **CASE,
            "expected_articles": [
                {"source": "SR_220_OR_de.md", "article": "13"},
            ],
        }
        hits = [
            {
                "id": "or::0",
                "document": "Art. 138\nEine andere Regel.",
                "metadata": {"source": "SR_220_OR_de.md"},
            }
        ]

        score = score_retrieval(case, hits, {"or::0": ["138"]})

        self.assertEqual(score["article_hit_at_k"], 0.0)
        self.assertEqual(score["article_mrr"], 0.0)

    def test_answer_scores_facts_and_citations_separately(self) -> None:
        answer = (
            "Der erste Monat, maximal drei Monate. "
            "[SR_220_OR_de.md Art. 335b] [SR_999_FAKE_de.md Art. 1]"
        )

        hits = [
            {
                "id": "or::0",
                "document": "Art. 335b186\nProbezeit.",
                "metadata": {"source": "SR_220_OR_de.md"},
            }
        ]
        score = score_answer(CASE, answer, hits, self.definitions)

        self.assertEqual(score["fact_coverage"], 1.0)
        self.assertEqual(score["expected_citation_precision"], 0.5)
        self.assertEqual(score["citation_grounding"], 0.5)
        self.assertEqual(score["citation_completeness"], 1.0)

    def test_missing_citation_does_not_count_as_correct(self) -> None:
        score = score_answer(
            CASE, "Der erste Monat, maximal drei Monate.", [], self.definitions
        )

        self.assertEqual(score["expected_citation_precision"], 0.0)
        self.assertEqual(score["citation_grounding"], 0.0)
        self.assertEqual(score["citation_completeness"], 0.0)

    def test_citation_parser_accepts_legal_qualifiers(self) -> None:
        answer = (
            "[SR_312.0_StPO_de.md Art. 10 Abs. 1] "
            "[SR_101_BV_de.md Art. 130 lit. a, Fn. 84]"
        )

        self.assertEqual(
            cited_article_pairs(answer),
            {
                ("sr_312.0_stpo_de.md", "10"),
                ("sr_101_bv_de.md", "130"),
            },
        )

    def test_citation_parser_expands_article_ranges(self) -> None:
        self.assertEqual(
            cited_article_pairs(
                "[SR_101_BV_de.md Art. 32–34] "
                "[SR_311.0_StGB_de.md Art. 130-132]"
            ),
            {
                ("sr_101_bv_de.md", "32"),
                ("sr_101_bv_de.md", "33"),
                ("sr_101_bv_de.md", "34"),
                ("sr_311.0_stgb_de.md", "130"),
                ("sr_311.0_stgb_de.md", "131"),
                ("sr_311.0_stgb_de.md", "132"),
            },
        )

    def test_citation_parser_strips_glued_footnote_digits(self) -> None:
        self.assertEqual(
            cited_article_pairs(
                "[SR_101_BV_de.md Art. 13084] "
                "[SR_220_OR_de.md Art. 335b186]"
            ),
            {
                ("sr_101_bv_de.md", "130"),
                ("sr_220_or_de.md", "335b"),
            },
        )

    def test_citation_parser_preserves_four_digit_or_articles(self) -> None:
        self.assertEqual(
            cited_article_pairs(
                "[SR_220_OR_de.md Art. 1000] "
                "[SR_220_OR_de.md Art. 1153] "
                "[SR_220_OR_de.md Art. 1153a862]"
            ),
            {
                ("sr_220_or_de.md", "1000"),
                ("sr_220_or_de.md", "1153"),
                ("sr_220_or_de.md", "1153a"),
            },
        )

    def test_negated_fact_is_not_covered(self) -> None:
        score = score_answer(
            CASE,
            "Die Probezeit beträgt nicht einen Monat, maximal drei Monate.",
            [],
            self.definitions,
        )

        self.assertEqual(score["fact_coverage"], 0.5)

    def test_incomplete_all_of_fact_is_not_covered(self) -> None:
        case = {
            **CASE,
            "required_facts": [
                {
                    "description": "Alle Bedingungen sind erforderlich.",
                    "all_of": [["notwendig"], ["leisten kann"], ["zumutbar"]],
                }
            ],
        }

        score = score_answer(case, "Die Arbeit ist notwendig.", [], {})

        self.assertEqual(score["fact_coverage"], 0.0)

    def test_sentence_level_negations_are_not_covered(self) -> None:
        for answer in (
            "Es ist nicht korrekt, dass die Probezeit einen Monat beträgt.",
            "Die Probezeit beträgt keinesfalls einen Monat.",
        ):
            with self.subTest(answer=answer):
                score = score_answer(CASE, answer, [], {})
                self.assertEqual(score["fact_coverage"], 0.0)


class FakeCollection:
    name = "test"

    def get(self, include=None, ids=None):
        documents = [f"Art. {article}\nDefinition" for article in range(1, 139)]
        documents.append("Die Regel steht in Art. 138.")
        return {
            "ids": [f"law::{index}" for index in range(len(documents))],
            "documents": documents,
            "metadatas": [{"source": "law.md"}] * len(documents),
        }


class GraphArticleResolutionTest(unittest.TestCase):
    def test_article_138_does_not_link_to_prefix_articles(self) -> None:
        graph = build_graph(FakeCollection())
        references = {
            edge["id"]
            for edge in graph["adjacency"]["law::138"]
            if edge["kind"].startswith("references")
        }

        self.assertEqual(references, {"law::137"})
        self.assertEqual(graph["article_definitions"]["law::137"], ["138"])

    def test_glued_multi_digit_footnotes_are_removed(self) -> None:
        class FootnoteCollection:
            name = "footnotes"

            def get(self, include=None, ids=None):
                return {
                    "ids": ["bv::0", "bv::1", "bv::2"],
                    "documents": [
                        "Art. 105\nAlkohol",
                        "Art. 10650\nGeldspiele",
                        "Art. 13082\nMehrwertsteuer",
                    ],
                    "metadatas": [{"source": "SR_101_BV_de.md"}] * 3,
                }

        graph = build_graph(FootnoteCollection())

        self.assertEqual(graph["article_definitions"]["bv::1"], ["106"])
        self.assertEqual(graph["article_definitions"]["bv::2"], ["130"])
        self.assertNotIn("1065", str(graph["article_definitions"]))
        self.assertNotIn("1308", str(graph["article_definitions"]))

    def test_only_first_duplicate_definition_is_canonical(self) -> None:
        class DuplicateCollection:
            name = "duplicates"

            def get(self, include=None, ids=None):
                return {
                    "ids": ["law::0", "law::1"],
                    "documents": [
                        "Art. 1\nSubstantive definition.",
                        "Art. 1\nRepeated appendix entry.",
                    ],
                    "metadatas": [{"source": "law.md"}] * 2,
                }

        graph = build_graph(DuplicateCollection())

        self.assertEqual(graph["article_definitions"], {"law::0": ["1"]})

    def test_four_digit_letter_article_with_footnote_is_normalized(self) -> None:
        class ArtifactCollection:
            name = "artifact"

            def get(self, include=None, ids=None):
                return {
                    "ids": ["or::0"],
                    "documents": ["Art. 1153a862\nCorrupted PDF heading."],
                    "metadatas": [{"source": "SR_220_OR_de.md"}],
                }

        graph = build_graph(ArtifactCollection())

        self.assertEqual(
            graph["article_definitions"], {"or::0": ["1153a"]}
        )

    def test_four_digit_articles_are_preserved(self) -> None:
        class FourDigitCollection:
            name = "four-digits"

            def get(self, include=None, ids=None):
                return {
                    "ids": ["or::0", "or::1", "or::2"],
                    "documents": [
                        "Art. 999\nFirst.",
                        "Art. 1000\nSecond.",
                        "Art. 1186870\nLast with footnote.",
                    ],
                    "metadatas": [{"source": "SR_220_OR_de.md"}] * 3,
                }

        graph = build_graph(FourDigitCollection())

        self.assertEqual(graph["article_definitions"]["or::1"], ["1000"])
        self.assertEqual(graph["article_definitions"]["or::2"], ["1186"])


class HybridArticleRetrievalTest(unittest.TestCase):
    def setUp(self) -> None:
        documents = [
            (
                "zgb::13",
                "Art. 13\nDie Handlungsfähigkeit besitzt, wer volljährig und "
                "urteilsfähig ist.",
                "SR_210_ZGB_de.md",
            ),
            (
                "stgb::15",
                "Art. 15\nWird jemand ohne Recht angegriffen oder unmittelbar "
                "mit einem Angriff bedroht, darf er angemessen abwehren. Notwehr.",
                "SR_311.0_StGB_de.md",
            ),
            (
                "mwstg::25",
                "Art. 25 Steuersätze\nNormalsatz 8,1 Prozent; reduzierter "
                "Steuersatz 2,6 Prozent.",
                "SR_641.20_MWSTG_de.md",
            ),
            (
                "other::55",
                "Art. 55\nAllgemeine Vorschriften über Verfahren und Behörden.",
                "SR_641.20_MWSTG_de.md",
            ),
        ]
        self.index = [
            {
                "id": chunk_id,
                "document": document,
                "metadata": {"source": source},
                "articles": [],
                "tokens": document.casefold().replace(".", "").split(),
                "source_terms": {source.split("_")[2].casefold()},
            }
            for chunk_id, document, source in documents
        ]

    def assert_top_article(self, question: str, expected_id: str) -> None:
        hits = lexical_article_retrieve(self.index, question, limit=2)
        self.assertTrue(hits)
        self.assertEqual(hits[0]["id"], expected_id)

    def test_finds_handlungsfaehigkeit_article(self) -> None:
        self.assert_top_article(
            "Welche Voraussetzungen gelten nach dem ZGB für die Handlungsfähigkeit?",
            "zgb::13",
        )

    def test_finds_notwehr_article(self) -> None:
        self.assert_top_article(
            "Wann darf ein unmittelbar drohender Angriff als Notwehr abgewehrt werden?",
            "stgb::15",
        )

    def test_finds_mwst_rate_article(self) -> None:
        self.assert_top_article(
            "Wie hoch sind Normalsatz und reduzierter Mehrwertsteuersatz?",
            "mwstg::25",
        )

    def test_source_name_without_topic_match_returns_no_article(self) -> None:
        hits = lexical_article_retrieve(
            self.index, "Was gilt für Satelliten nach dem ZGB?", limit=2
        )

        self.assertEqual(hits, [])

    def test_vector_wins_equal_rrf_rank(self) -> None:
        vector = [
            {
                "id": "vector::1",
                "document": "vector",
                "metadata": {},
                "via": "vector",
            }
        ]
        lexical = [
            {
                "id": "article::1",
                "document": "article",
                "metadata": {},
                "via": "lexical-article",
            }
        ]

        merged = _merge_hybrid_hits(vector, lexical)

        self.assertEqual([hit["id"] for hit in merged], ["vector::1", "article::1"])


if __name__ == "__main__":
    unittest.main()
