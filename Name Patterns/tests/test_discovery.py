"""Tests fuer Stufe 3: automatische Motivsuche."""

from __future__ import annotations

import unittest

from name_patterns.data import HRR_KINGS
from name_patterns.discovery import (
    Motif,
    candidate_motifs,
    collapse_restatements,
    discover,
    frequent_ngrams,
)
from name_patterns.model import PatternKind, SearchConfig
from name_patterns.scoring import score_chains

from .test_search import KH, build_sequence


class TestFrequentNgrams(unittest.TestCase):
    def test_counts_contiguous_grams(self):
        sequence = ["A", "B", "A", "B", "A", "B"]
        self.assertEqual(frequent_ngrams(sequence, 2, 3), [("A", "B")])

    def test_threshold_excludes_rare_grams(self):
        sequence = ["A", "B", "A", "B", "C", "D"]
        self.assertEqual(frequent_ngrams(sequence, 2, 3), [])

    def test_length_beyond_sequence_is_empty(self):
        self.assertEqual(frequent_ngrams(["A"], 5, 1), [])


class TestCandidateMotifs(unittest.TestCase):
    def setUp(self):
        self.config = SearchConfig(min_blocks=3, max_anchor_len=2)
        self.motifs = candidate_motifs(HRR_KINGS, self.config)

    def test_contains_the_historical_motif(self):
        self.assertIn(Motif(anchor=KH, echo="Heinrich"), self.motifs)

    def test_allows_a_name_to_be_its_own_anchor_and_echo(self):
        """Die schlichte Wiederholung eines Namens ist ein zulaessiges Motiv."""
        self.assertIn(Motif(anchor=("Heinrich",), echo="Heinrich"), self.motifs)

    def test_prunes_names_that_cannot_fill_min_blocks(self):
        """'Lothar' kommt nur einmal vor und kann keine Kette der Laenge 3 tragen."""
        for motif in self.motifs:
            self.assertNotEqual(motif.echo, "Lothar")
            self.assertNotIn("Lothar", motif.anchor)

    def test_raising_min_blocks_shrinks_the_candidate_set(self):
        strict = candidate_motifs(HRR_KINGS, SearchConfig(min_blocks=5))
        self.assertLess(len(strict), len(self.motifs))


class TestDiscovery(unittest.TestCase):
    def test_finds_the_historical_pattern_without_being_told(self):
        chains = discover(HRR_KINGS, SearchConfig(max_deviations=0, min_blocks=3))
        best = score_chains(HRR_KINGS, chains)[0].chain
        self.assertEqual(best.anchor, KH)
        self.assertEqual(best.echo, "Heinrich")
        self.assertEqual(best.x0, 3)
        self.assertEqual(best.d, 1)
        self.assertEqual([p.block.x for p in best.placements], [3, 4, 5, 6])

    def test_rarity_outranks_raw_length(self):
        """Die laengste Kette ist nicht automatisch die interessanteste.

        'Konrad ... Heinrich' hat mehr Bloecke, das gesuchte Muster aber das
        unwahrscheinlichere Motiv -- und gewinnt deshalb nach Bit.
        """
        chains = discover(HRR_KINGS, SearchConfig(max_deviations=0, min_blocks=3))
        scored = score_chains(HRR_KINGS, chains)
        best = scored[0]
        longest = max(chains, key=lambda c: len(c.placements))
        self.assertGreater(len(longest.placements), len(best.chain.placements))
        self.assertEqual(best.chain.anchor, KH)

    def test_discovery_on_a_synthetic_sequence(self):
        sequence = build_sequence([2, 3, 4], separator=2)
        chains = discover(sequence, SearchConfig(max_deviations=0, min_blocks=3))
        self.assertTrue(
            any(c.anchor == KH and c.echo == "Heinrich" and c.d == 1 for c in chains)
        )

    def test_no_motif_survives_in_a_list_of_unique_names(self):
        sequence = [f"n{i}" for i in range(40)]
        self.assertEqual(discover(sequence, SearchConfig(min_blocks=3)), [])

    def test_max_anchor_len_limits_motif_length(self):
        """Die Schranke gilt nur fuer FIXED -- BOOKEND hat gar keinen Anchor."""
        chains = discover(
            HRR_KINGS, SearchConfig(max_deviations=0, min_blocks=3, max_anchor_len=1)
        )
        fixed = [c for c in chains if c.kind is PatternKind.FIXED]
        self.assertTrue(fixed)
        for chain in fixed:
            self.assertEqual(len(chain.anchor), 1)


class TestCollapseRestatements(unittest.TestCase):
    def test_same_echo_positions_keep_only_the_more_specific_motif(self):
        config = SearchConfig(max_deviations=0, min_blocks=3)
        collapsed = discover(HRR_KINGS, config)
        keys = [
            (frozenset(p.block.echo_pos for p in c.placements), c.d)
            for c in collapsed
        ]
        self.assertEqual(len(keys), len(set(keys)))

    def test_empty_input(self):
        self.assertEqual(collapse_restatements([]), [])


if __name__ == "__main__":
    unittest.main()
