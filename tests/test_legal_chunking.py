import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "legal_ingest", ROOT / "rag-3a-ingest.py"
)
legal_ingest = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(legal_ingest)


class LegalChunkingTest(unittest.TestCase):
    def test_articles_are_primary_boundaries(self):
        chunks = legal_ingest.legal_chunk(
            "Einleitung\n\n"
            "Art. 1 Zweck\nDer erste Artikel.\n"
            "Art. 2 Geltungsbereich\nDer zweite Artikel."
        )

        self.assertEqual(len(chunks), 3)
        self.assertTrue(chunks[1].startswith("Art. 1"))
        self.assertTrue(chunks[2].startswith("Art. 2"))
        self.assertEqual(
            max(len(legal_ingest.ARTICLE_HEADING_RE.findall(c)) for c in chunks),
            1,
        )

    def test_toc_page_and_reference_only_footnote_are_removed(self):
        text = (
            "## PDF-Seite 1\n\n"
            "Inhaltsverzeichnis\n\n"
            "Zweck ................................ Art. 1\n"
            "Geltungsbereich ...................... Art. 2\n"
            "Organisation ......................... Art. 3\n"
            "Verfahren ............................ Art. 4\n"
            "Rechtsmittel ......................... Art. 5\n\n"
            "8 SR 210\n\n"
            "Art. 1 Zweck\nDiese Bestimmung bleibt erhalten."
        )

        chunks = legal_ingest.legal_chunk(text)
        joined = "\n".join(chunks)

        self.assertNotIn("Inhaltsverzeichnis", joined)
        self.assertNotIn("8 SR 210", joined)
        self.assertIn("Art. 1 Zweck", joined)

    def test_oversized_article_splits_without_exceeding_budget(self):
        sentence = "Diese Bestimmung enthält einen vollständigen Rechtssatz. "
        text = "Art. 13 Handlungsfähigkeit\n" + sentence * 40

        chunks = legal_ingest.legal_chunk(text, max_size=240)

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 240 for chunk in chunks))
        self.assertTrue(chunks[0].startswith("Art. 13"))
        self.assertTrue(
            all(chunk.startswith("Art. 13") for chunk in chunks[1:])
        )
        self.assertTrue(all(not chunk.endswith("vollständ") for chunk in chunks))

    def test_small_related_blocks_are_packed(self):
        chunks = legal_ingest.legal_chunk(
            "# Gesetz\n\nKurzer Kontext.\n\nNoch ein kurzer Kontext.",
            max_size=200,
        )

        self.assertEqual(chunks, [
            "# Gesetz\n\nKurzer Kontext.\n\nNoch ein kurzer Kontext."
        ])


if __name__ == "__main__":
    unittest.main()
