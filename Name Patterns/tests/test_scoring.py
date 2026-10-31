"""Tests fuer Stufe 4: Bewertung nach Seltenheit und Monte-Carlo-Signifikanz."""

from __future__ import annotations

import math
import unittest

from name_patterns.data import HRR_KINGS
from name_patterns.discovery import Motif, discover
from name_patterns.model import SearchConfig
from name_patterns.scoring import (
    NullModel,
    assess,
    block_bits,
    build_null_model,
    chain_bits,
    name_probabilities,
    score_chains,
)
from name_patterns.search import find_chains

from .test_search import KH


class TestNameProbabilities(unittest.TestCase):
    def test_probabilities_sum_to_one(self):
        probs = name_probabilities(HRR_KINGS)
        self.assertAlmostEqual(sum(probs.values()), 1.0)

    def test_empty_sequence(self):
        self.assertEqual(name_probabilities([]), {})

    def test_frequency_is_preserved_under_shuffling(self):
        """Das Nullmodell permutiert nur -- die Haeufigkeiten bleiben gleich.

        Genau deshalb darf die Bit-Berechnung die Wahrscheinlichkeiten der
        Originalliste in allen Durchlaeufen weiterverwenden.
        """
        shuffled = list(reversed(HRR_KINGS))
        self.assertEqual(name_probabilities(HRR_KINGS), name_probabilities(shuffled))


class TestBits(unittest.TestCase):
    def test_rarer_names_are_worth_more_bits(self):
        sequence = ["haeufig"] * 90 + ["selten"] * 10
        probs = name_probabilities(sequence)
        self.assertGreater(
            block_bits(probs, ("selten",), "selten"),
            block_bits(probs, ("haeufig",), "haeufig"),
        )

    def test_longer_anchor_is_worth_more_bits(self):
        probs = name_probabilities(HRR_KINGS)
        self.assertGreater(
            block_bits(probs, KH, "Heinrich"),
            block_bits(probs, ("Heinrich",), "Heinrich"),
        )

    def test_bits_match_the_definition(self):
        sequence = ["A"] * 2 + ["B"] * 2
        probs = name_probabilities(sequence)
        self.assertAlmostEqual(block_bits(probs, ("A",), "B"), -math.log2(0.25))

    def test_unknown_name_yields_zero_bits(self):
        probs = name_probabilities(["A", "B"])
        self.assertEqual(block_bits(probs, ("gibtsnicht",), "A"), 0.0)

    def test_deviations_lower_the_bit_score(self):
        config = SearchConfig(max_deviations=1, min_blocks=3)
        probs = name_probabilities(HRR_KINGS)
        chains = find_chains(HRR_KINGS, KH, "Heinrich", config)
        clean = next(c for c in chains if not c.deviations)
        same_motif_bits = block_bits(probs, KH, "Heinrich")
        # Eine Abweichung kostet deviation_penalty effektive Bloecke.
        expected_drop = clean.deviation_penalty * same_motif_bits
        self.assertAlmostEqual(
            chain_bits(probs, clean) - expected_drop,
            (clean.score - clean.deviation_penalty) * same_motif_bits,
        )


class TestNullModel(unittest.TestCase):
    def setUp(self):
        self.null = NullModel(trials=4, scores=(1.0, 2.0, 3.0, 10.0))

    def test_summary_statistics(self):
        self.assertEqual(self.null.best, 10.0)
        self.assertAlmostEqual(self.null.mean, 4.0)

    def test_p_value_never_reaches_zero(self):
        """Bei endlich vielen Durchlaeufen darf p=0 nicht behauptet werden."""
        self.assertGreater(self.null.p_value(1000.0), 0.0)
        self.assertAlmostEqual(self.null.p_value(1000.0), 1 / 5)

    def test_p_value_counts_ties_as_hits(self):
        self.assertAlmostEqual(self.null.p_value(10.0), 2 / 5)

    def test_p_value_is_monotone(self):
        self.assertLessEqual(self.null.p_value(5.0), self.null.p_value(2.0))

    def test_empty_distribution_is_safe(self):
        empty = NullModel(trials=0, scores=())
        self.assertEqual(empty.best, 0.0)
        self.assertEqual(empty.mean, 0.0)
        self.assertEqual(empty.p95, 0.0)


class TestMonteCarlo(unittest.TestCase):
    def test_same_seed_gives_the_same_distribution(self):
        config = SearchConfig(max_deviations=0, min_blocks=3)
        first = build_null_model(HRR_KINGS, config, trials=30, seed=7)
        second = build_null_model(HRR_KINGS, config, trials=30, seed=7)
        self.assertEqual(first.scores, second.scores)

    def test_different_seeds_differ(self):
        config = SearchConfig(max_deviations=0, min_blocks=3)
        first = build_null_model(HRR_KINGS, config, trials=30, seed=7)
        second = build_null_model(HRR_KINGS, config, trials=30, seed=8)
        self.assertNotEqual(first.scores, second.scores)

    def test_specific_motif_is_never_matched_by_chance(self):
        """Der Zufall bringt das historische Motiv gelegentlich hervor -- aber nie so gut.

        Ein paar Permutationen enthalten durchaus eine Kette dieses Motivs;
        keine davon erreicht die Guete des echten Befunds.  Mit vorab
        festgelegtem Anchor und Echo faellt der p-Wert noch deutlicher aus als
        in der Discovery, wo sich der Treffer gegen alle mitgeprueften Motive
        behaupten muss.
        """
        config = SearchConfig(max_deviations=0, min_blocks=3)
        motif = Motif(anchor=KH, echo="Heinrich")
        probs = name_probabilities(HRR_KINGS)
        observed = max(
            chain_bits(probs, c)
            for c in find_chains(HRR_KINGS, KH, "Heinrich", config)
        )
        null = build_null_model(
            HRR_KINGS, config, motif=motif, trials=200, seed=7
        )
        self.assertTrue(any(score > 0 for score in null.scores))
        self.assertLess(null.best, observed)
        self.assertLess(null.p_value(observed), 0.02)

    def test_progress_callback_reports_every_trial(self):
        seen = []
        config = SearchConfig(max_deviations=0, min_blocks=3)
        build_null_model(
            HRR_KINGS,
            config,
            motif=Motif(anchor=KH, echo="Heinrich"),
            trials=5,
            seed=1,
            progress=lambda done, total: seen.append((done, total)),
        )
        self.assertEqual(seen, [(1, 5), (2, 5), (3, 5), (4, 5), (5, 5)])

    def test_historical_pattern_is_significant(self):
        config = SearchConfig(max_deviations=0, min_blocks=3)
        chains = discover(HRR_KINGS, config)
        scored, null = assess(HRR_KINGS, chains, config, trials=300, seed=42)
        self.assertIsNotNone(null)
        best = scored[0]
        self.assertEqual(best.chain.anchor, KH)
        self.assertLess(best.p_value, 0.05)
        self.assertTrue(best.significant)

    def test_a_chance_pattern_is_not_significant(self):
        """Nicht jeder Treffer ueberlebt den Vergleich mit dem Zufall.

        'Heinrich ... Konrad' sieht in der Rohausgabe plausibel aus, ist aber
        nur ein Nebeneffekt davon, dass beide Namen haeufig sind.
        """
        config = SearchConfig(max_deviations=0, min_blocks=3)
        chains = discover(HRR_KINGS, config)
        scored, _ = assess(HRR_KINGS, chains, config, trials=300, seed=42)
        weak = [
            s for s in scored
            if s.chain.anchor == ("Heinrich",) and s.chain.echo == "Konrad"
        ]
        self.assertTrue(weak)
        self.assertFalse(weak[0].significant)

    def test_assess_without_trials_leaves_p_values_unset(self):
        config = SearchConfig(max_deviations=0, min_blocks=3)
        chains = discover(HRR_KINGS, config)
        scored, null = assess(HRR_KINGS, chains, config, trials=0)
        self.assertIsNone(null)
        self.assertTrue(all(s.p_value is None for s in scored))
        self.assertFalse(any(s.significant for s in scored))

    def test_assess_on_empty_input(self):
        scored, null = assess(HRR_KINGS, [], SearchConfig(), trials=10)
        self.assertEqual(scored, [])
        self.assertIsNone(null)


class TestScoreOrdering(unittest.TestCase):
    def test_scored_chains_come_back_sorted_by_bits(self):
        chains = discover(HRR_KINGS, SearchConfig(max_deviations=0, min_blocks=3))
        scored = score_chains(HRR_KINGS, chains)
        bits = [s.bits for s in scored]
        self.assertEqual(bits, sorted(bits, reverse=True))


if __name__ == "__main__":
    unittest.main()
