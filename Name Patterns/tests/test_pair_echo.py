"""Tests der abstrahierten X,Y,n,Y-Musterfamilie."""

import unittest
from pathlib import Path

from name_patterns.pair_echo import (
    assess_variant,
    best_pair_echo,
    build_variant_with_ferdinand_iv,
    build_variants,
    has_chain_length,
    max_chain_length,
)
from name_patterns.timeline import load_timeline


PROJECT = Path(__file__).resolve().parent.parent


class TestPairEcho(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        timeline = load_timeline(PROJECT / "HRR_Kings_843_1806.csv")
        cls.seven, cls.eight = build_variants(timeline)
        cls.eight_kings = build_variant_with_ferdinand_iv(timeline)

    def test_variant_lengths_and_karlmann_normalization(self):
        self.assertEqual(len(self.seven), 50)
        self.assertEqual(len(self.eight), 61)
        self.assertEqual(self.seven[:9], (
            "Karl", "Ludwig", "Lothar", "Ludwig",
            "Karl", "Ludwig", "Karl", "Arnolf", "Ludwig",
        ))
        self.assertNotIn("Karlmann", self.seven)

    def test_seven_blocks_cover_49_of_50(self):
        finding = best_pair_echo(self.seven)
        self.assertIsNotNone(finding)
        assert finding is not None
        self.assertEqual(tuple(block.n for block in finding.blocks), tuple(range(1, 8)))
        self.assertEqual((finding.covered, finding.span), (49, 50))
        self.assertEqual(finding.outsiders, 1)

    def test_eight_blocks_cover_60_of_61(self):
        finding = best_pair_echo(self.eight)
        self.assertIsNotNone(finding)
        assert finding is not None
        self.assertEqual(tuple(block.n for block in finding.blocks), tuple(range(1, 9)))
        self.assertEqual((finding.covered, finding.span), (60, 61))
        self.assertEqual(finding.blocks[-1].x_name, "Maximilian")
        self.assertEqual(finding.blocks[-1].y_name, "Karl")

    def test_fast_length_matches_full_search(self):
        self.assertEqual(max_chain_length(self.seven), 7)
        self.assertEqual(max_chain_length(self.eight), 8)
        self.assertTrue(has_chain_length(self.seven, 7))
        self.assertTrue(has_chain_length(self.eight, 8))

    def test_king_variant_keeps_ferdinand_iv_and_skips_n8(self):
        self.assertEqual(len(self.eight_kings), 62)
        finding = best_pair_echo(self.eight_kings, max_n_skips=1)
        self.assertIsNotNone(finding)
        assert finding is not None
        self.assertEqual(
            tuple(block.n for block in finding.blocks),
            (1, 2, 3, 4, 5, 6, 7, 9),
        )
        self.assertEqual(finding.n_skips, 1)
        self.assertEqual((finding.covered, finding.span), (61, 62))
        self.assertTrue(
            has_chain_length(self.eight_kings, 8, max_n_skips=1)
        )

    def test_permutation_is_reproducible(self):
        first = assess_variant(self.seven, "test", trials=50, seed=3)
        second = assess_variant(self.seven, "test", trials=50, seed=3)
        self.assertEqual((first.hits, first.p_value), (second.hits, second.p_value))


if __name__ == "__main__":
    unittest.main()
