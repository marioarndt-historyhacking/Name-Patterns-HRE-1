"""Tests fuer die gemeinsame Auswertung mehrerer Listen."""

from __future__ import annotations

import math
import unittest
from pathlib import Path

from name_patterns.data import load_names
from name_patterns.joint import (
    chi2_survival_even_df,
    evaluate_jointly,
    fisher_combined,
)
from name_patterns.model import PatternKind, SearchConfig
from name_patterns.scoring import Measure

PROJECT = Path(__file__).resolve().parent.parent

CONFIG = SearchConfig(
    max_deviations=0,
    min_blocks=3,
    allowed_d=(0,),
    max_interruption=4,
    families=(PatternKind.BOOKEND,),
)


def kings(name):
    return (name, load_names(PROJECT / f"{name}_Kings.txt"))


class TestChiSquare(unittest.TestCase):
    def test_two_degrees_of_freedom_is_a_plain_exponential(self):
        for x in (0.5, 2.0, 7.0):
            self.assertAlmostEqual(chi2_survival_even_df(x, 2), math.exp(-x / 2))

    def test_four_degrees_of_freedom(self):
        x = 2.0
        self.assertAlmostEqual(
            chi2_survival_even_df(x, 4), math.exp(-x / 2) * (1 + x / 2)
        )

    def test_zero_and_negative_return_one(self):
        self.assertEqual(chi2_survival_even_df(0.0, 6), 1.0)
        self.assertEqual(chi2_survival_even_df(-3.0, 6), 1.0)

    def test_survival_decreases_with_x(self):
        values = [chi2_survival_even_df(x, 6) for x in (1, 5, 10, 30)]
        self.assertEqual(values, sorted(values, reverse=True))

    def test_odd_degrees_are_rejected(self):
        with self.assertRaises(ValueError):
            chi2_survival_even_df(1.0, 3)


class TestFisher(unittest.TestCase):
    def test_uninformative_p_values_stay_uninformative(self):
        """Zwei p-Werte von 0.5 duerfen zusammen nichts beweisen."""
        self.assertGreater(fisher_combined([0.5, 0.5]), 0.3)

    def test_small_p_values_combine_to_something_smaller(self):
        combined = fisher_combined([0.02, 0.02, 0.02])
        self.assertLess(combined, 0.02)

    def test_a_single_value_reproduces_itself(self):
        self.assertAlmostEqual(fisher_combined([0.03]), 0.03, places=6)

    def test_empty_input_is_safe(self):
        self.assertEqual(fisher_combined([]), 0.0)


class TestJointEvaluation(unittest.TestCase):
    def setUp(self):
        self.datasets = [kings("Scotland"), kings("Denmark"), kings("Norway")]
        self.result = evaluate_jointly(
            self.datasets, CONFIG, trials=200, seed=42, measure=Measure.COVERAGE
        )

    def test_reports_one_outcome_per_list(self):
        self.assertEqual(
            [o.name for o in self.result.outcomes],
            ["Scotland", "Denmark", "Norway"],
        )

    def test_each_list_keeps_its_own_finding(self):
        by_name = {o.name: o for o in self.result.outcomes}
        self.assertEqual(by_name["Scotland"].covered, 24)
        self.assertEqual(by_name["Denmark"].covered, 24)
        self.assertEqual(by_name["Norway"].covered, 28)

    def test_all_three_at_once_is_never_easier_than_the_hardest_single(self):
        """Ein gemeinsamer Treffer verlangt jede Liste einzeln -- also hoechstens
        so oft wie die seltenste davon."""
        hardest = min(o.p_value for o in self.result.outcomes)
        self.assertLessEqual(self.result.p_all, hardest + 1e-9)

    def test_observed_mean_beats_the_null(self):
        null_mean = sum(self.result.null_means) / len(self.result.null_means)
        self.assertGreater(self.result.observed_mean, null_mean)

    def test_null_means_are_shares(self):
        self.assertEqual(len(self.result.null_means), 200)
        self.assertTrue(all(0.0 <= m <= 1.0 for m in self.result.null_means))

    def test_permutation_and_fisher_broadly_agree(self):
        """Zwei Wege mit verschiedenen Voraussetzungen, ein Ergebnis.

        Sie muessen nicht identisch sein -- Fisher setzt gleichverteilte
        p-Werte voraus, der Permutationstest nichts.  Wichtig ist, dass beide
        dieselbe Groessenordnung liefern.
        """
        self.assertLess(self.result.p_fisher, 0.01)
        self.assertLess(self.result.p_mean, 0.01)

    def test_same_seed_reproduces_the_result(self):
        again = evaluate_jointly(
            self.datasets, CONFIG, trials=200, seed=42, measure=Measure.COVERAGE
        )
        self.assertEqual(again.null_means, self.result.null_means)
        self.assertEqual(again.all_at_once, self.result.all_at_once)

    def test_lists_without_a_pattern_produce_no_joint_evidence(self):
        noise = [
            ("a", [f"n{i}" for i in range(27)]),
            ("b", [f"m{i}" for i in range(27)]),
        ]
        result = evaluate_jointly(noise, CONFIG, trials=50, seed=1)
        self.assertEqual(result.observed_mean, 0.0)
        self.assertTrue(all(o.chain is None for o in result.outcomes))


if __name__ == "__main__":
    unittest.main()
