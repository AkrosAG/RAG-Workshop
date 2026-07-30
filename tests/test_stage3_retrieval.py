import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


stage3b = load_script("stage3b", "rag-3b-chat-classical.py")
stage3c = load_script("stage3c", "rag-3c-chat-rerank.py")


class FakeCollection:
    def __init__(self, count: int = 12):
        self.count = count
        self.requested_results = None

    def query(self, query_embeddings, n_results, include):
        self.requested_results = n_results
        return {
            "documents": [[f"chunk-{index}" for index in range(self.count)]],
            "metadatas": [
                [
                    {"source": f"source-{index}.md"}
                    for index in range(self.count)
                ]
            ],
        }


class FakeReranker:
    pairs = []

    def __init__(self, model_name: str):
        self.model_name = model_name

    def predict(self, pairs, show_progress_bar=False):
        type(self).pairs = pairs
        return [0.1, 0.9, 0.4, 0.8, 0.2, 0.3, 0.7, 0.6, 0.5, 0.0]


class Stage3RetrievalTest(unittest.TestCase):
    def test_3b_uses_exactly_top_k_vector_hits_in_original_order(self):
        collection = FakeCollection()

        hits = stage3b.retrieve_top_k(collection, [0.1], stage3b.TOP_K)

        self.assertEqual(collection.requested_results, stage3b.TOP_K)
        self.assertEqual(len(hits), stage3b.TOP_K)
        self.assertEqual(
            [hit["document"] for hit in hits],
            ["chunk-0", "chunk-1", "chunk-2", "chunk-3"],
        )
        self.assertEqual(
            [hit["metadata"]["source"] for hit in hits],
            [
                "source-0.md",
                "source-1.md",
                "source-2.md",
                "source-3.md",
            ],
        )

    def test_3c_scores_at_most_top_n_and_keeps_top_k(self):
        collection = FakeCollection()
        vector_hits = stage3c.retrieve_candidates(
            collection, [0.1], stage3c.TOP_N
        )
        ranking = stage3c.rerank(
            "Wann liegt Notwehr nach Schweizer Recht vor?",
            [hit["document"] for hit in vector_hits],
            stage3c.TOP_K,
            model_factory=FakeReranker,
        )

        self.assertEqual(collection.requested_results, stage3c.TOP_N)
        self.assertEqual(len(vector_hits), stage3c.TOP_N)
        self.assertEqual(len(FakeReranker.pairs), stage3c.TOP_N)
        self.assertEqual(len(ranking), stage3c.TOP_K)

    def test_3c_sorts_descending_and_keeps_documents_with_sources(self):
        collection = FakeCollection()
        vector_hits = stage3c.retrieve_candidates(
            collection, [0.1], stage3c.TOP_N
        )
        ranking = stage3c.rerank(
            "Wann liegt Notwehr nach Schweizer Recht vor?",
            [hit["document"] for hit in vector_hits],
            stage3c.TOP_K,
            model_factory=FakeReranker,
        )
        selected = [vector_hits[index] for index, _ in ranking]

        self.assertEqual(
            ranking,
            [(1, 0.9), (3, 0.8), (6, 0.7), (7, 0.6)],
        )
        self.assertEqual(
            [
                (hit["document"], hit["metadata"]["source"])
                for hit in selected
            ],
            [
                ("chunk-1", "source-1.md"),
                ("chunk-3", "source-3.md"),
                ("chunk-6", "source-6.md"),
                ("chunk-7", "source-7.md"),
            ],
        )

    def test_swiss_legal_question_changes_3b_order_after_reranking(self):
        class LegalCollection:
            def query(self, query_embeddings, n_results, include):
                return {
                    "documents": [[
                        "Allgemeine Bestimmungen des Strafgesetzbuchs.",
                        "Art. 15: Ein rechtswidriger Angriff darf in "
                        "angemessener Weise abgewehrt werden.",
                        "Bestimmungen über die Strafzumessung.",
                        "Verfahrensrechtliche Zuständigkeiten.",
                    ]],
                    "metadatas": [[
                        {"source": "SR_311.0_StGB_de.md"},
                        {"source": "SR_311.0_StGB_de.md"},
                        {"source": "SR_311.0_StGB_de.md"},
                        {"source": "SR_312.0_StPO_de.md"},
                    ]],
                }

        class LegalReranker:
            def __init__(self, model_name):
                pass

            def predict(self, pairs, show_progress_bar=False):
                return [0.1, 0.9, 0.2, 0.0]

        question = "Wann liegt Notwehr nach Schweizer Recht vor?"
        collection = LegalCollection()
        classical = stage3b.retrieve_top_k(collection, [0.1], stage3b.TOP_K)
        candidates = stage3c.retrieve_candidates(
            collection, [0.1], stage3c.TOP_N
        )
        ranking = stage3c.rerank(
            question,
            [hit["document"] for hit in candidates],
            stage3c.TOP_K,
            model_factory=LegalReranker,
        )
        reranked = [candidates[index] for index, _ in ranking]

        self.assertNotIn("Art. 15", classical[0]["document"])
        self.assertIn("Art. 15", reranked[0]["document"])


if __name__ == "__main__":
    unittest.main()
