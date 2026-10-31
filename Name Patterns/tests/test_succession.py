"""Tests der exakten Vorgaenger-Todesjahr-Folge."""

import unittest
from pathlib import Path

from name_patterns.succession import (
    EVENTS,
    arithmetic_index_sets,
    assess_joint,
    exact_event_p_values,
    observed_progressions,
    wilson_interval,
)
from name_patterns.timeline import load_timeline


PROJECT = Path(__file__).resolve().parent.parent


class TestSuccessionProgression(unittest.TestCase):
    def test_controlled_table_has_unique_four_term_progression(self):
        self.assertEqual(len(EVENTS), 52)
        progressions = arithmetic_index_sets(EVENTS)
        self.assertEqual(len(progressions), 1)
        finding = observed_progressions()[0]
        self.assertEqual(finding.name, "Konrad")
        self.assertEqual(finding.years, (911, 1024, 1137, 1250))
        self.assertEqual(finding.step, 113)

    def test_exact_targeted_and_global_p_values(self):
        targeted, global_p, favorable = exact_event_p_values()
        self.assertAlmostEqual(targeted, 1 / 270725)
        self.assertEqual(favorable, 42)
        self.assertAlmostEqual(global_p, 42 / 270725)
        self.assertLess(global_p, 0.001)

    def test_joint_test_is_reproducible(self):
        timeline = load_timeline(PROJECT / "HRR_Kings_843_1806.csv")
        first = assess_joint(timeline, trials=100, seed=9)
        second = assess_joint(timeline, trials=100, seed=9)
        self.assertEqual(first.hits, second.hits)
        self.assertEqual(first.joint_p, second.joint_p)
        self.assertGreater(first.joint_p, 0.0)

    def test_wilson_interval_contains_empirical_rate(self):
        low, high = wilson_interval(96, 1_000_000)
        self.assertLess(low, 96 / 1_000_000)
        self.assertGreater(high, 96 / 1_000_000)


if __name__ == "__main__":
    unittest.main()
