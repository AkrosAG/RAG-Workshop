import unittest

from evaluate import score_answer, score_retrieval


CASE = {
    "expected_sources": ["SR_220_OR_de.md"],
    "expected_articles": [
        {"source": "SR_220_OR_de.md", "article": "335b"},
    ],
    "expected_terms": ["probezeit", "erster monat", "drei monate"],
    "required_facts": [
        {
            "description": "Die Probezeit beträgt einen Monat.",
            "alternatives": ["erster monat", "erste monat", "einen monat"],
        },
        {
            "description": "Die Probezeit dauert höchstens drei Monate.",
            "alternatives": ["höchstens drei monate", "maximal drei monate"],
        },
    ],
}


class EvaluationScoringTest(unittest.TestCase):
    def test_article_metrics_handle_glued_fedlex_footnote(self) -> None:
        hits = [
            {
                "document": (
                    "Art. 335b186\n"
                    "Als Probezeit gilt der erste Monat; höchstens drei Monate."
                ),
                "metadata": {"source": "SR_220_OR_de.md"},
            }
        ]

        score = score_retrieval(CASE, hits)

        self.assertEqual(score["article_hit_at_k"], 1.0)
        self.assertEqual(score["article_recall_at_k"], 1.0)
        self.assertEqual(score["article_mrr"], 1.0)

    def test_answer_scores_facts_and_citations_separately(self) -> None:
        answer = (
            "Der erste Monat, maximal drei Monate. "
            "[SR_220_OR_de.md Art. 335b] [SR_999_FAKE_de.md Art. 1]"
        )

        score = score_answer(CASE, answer)

        self.assertEqual(score["fact_coverage"], 1.0)
        self.assertEqual(score["citation_accuracy"], 0.5)
        self.assertEqual(score["citation_completeness"], 1.0)

    def test_missing_citation_does_not_count_as_correct(self) -> None:
        score = score_answer(CASE, "Der erste Monat, maximal drei Monate.")

        self.assertEqual(score["citation_accuracy"], 0.0)
        self.assertEqual(score["citation_completeness"], 0.0)


if __name__ == "__main__":
    unittest.main()
