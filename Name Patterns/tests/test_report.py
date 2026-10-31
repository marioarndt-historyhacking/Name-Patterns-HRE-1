"""Tests fuer die eindeutige Signifikanzangabe im Textbericht."""

from __future__ import annotations

import unittest

from name_patterns.data import HRR_KINGS
from name_patterns.model import SearchConfig
from name_patterns.report import format_scored_report
from name_patterns.scoring import Measure, NullModel, score_chains
from name_patterns.search import find_chains


class TestSignificanceOutput(unittest.TestCase):
    def setUp(self):
        chains = find_chains(
            HRR_KINGS,
            ("Konrad", "Heinrich"),
            "Heinrich",
            SearchConfig(max_deviations=0, min_blocks=3),
        )
        self.scored = score_chains(HRR_KINGS, chains, Measure.COVERAGE)[:1]
        self.null = NullModel(
            trials=100,
            scores=tuple([0.0] * 100),
            measure=Measure.COVERAGE,
        )

    def test_significant_yes_is_an_explicit_line(self):
        self.scored[0].p_value = 0.01
        report = format_scored_report(HRR_KINGS, self.scored, self.null, limit=1)
        self.assertIn("p-Wert:      0.0100   (gemessen an Abdeckung)", report)
        self.assertIn("Signifikant:  ja (p < 0.05)", report)

    def test_significant_no_is_an_explicit_line(self):
        self.scored[0].p_value = 0.05
        report = format_scored_report(HRR_KINGS, self.scored, self.null, limit=1)
        self.assertIn("Signifikant:  nein (p >= 0.05)", report)

    def test_no_significance_line_without_permutation_test(self):
        report = format_scored_report(HRR_KINGS, self.scored, None, limit=1)
        self.assertNotIn("p-Wert:", report)
        self.assertNotIn("Signifikant:", report)


if __name__ == "__main__":
    unittest.main()
