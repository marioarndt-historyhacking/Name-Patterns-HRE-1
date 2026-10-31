"""Tests der global korrigierten Intervallsuche."""

from __future__ import annotations

import unittest
from pathlib import Path

from name_patterns.discovery import Motif
from name_patterns.model import PatternKind, SearchConfig
from name_patterns.periods import (
    PeriodSpec,
    assess_period_pair,
    format_period_contrast,
    parse_period_pair,
    select_period,
)
from name_patterns.timeline import (
    assess_interval,
    best_interval,
    format_interval_report,
    load_timeline,
)


PROJECT = Path(__file__).resolve().parent.parent


class TestFullHRRTimeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.timeline = load_timeline(PROJECT / "HRR_Kings_843_1806.csv")
        cls.sequence = [entry.analysis_name for entry in cls.timeline]
        cls.config = SearchConfig(
            min_blocks=3,
            max_deviations=0,
            allowed_d=(0, 1),
            families=(PatternKind.FIXED,),
        )
        cls.motif = Motif(("Konrad", "Heinrich"), "Heinrich")

    def test_timeline_has_full_wikipedia_span(self):
        self.assertEqual(len(self.timeline), 64)
        self.assertEqual(self.timeline[0].elevation_year, 843)
        self.assertEqual(self.timeline[-1].elevation_year, 1792)

    def test_known_pattern_is_best_for_the_fixed_motif(self):
        finding = best_interval(
            self.sequence, self.config, motif=self.motif, timeline=self.timeline
        )
        self.assertIsNotNone(finding)
        assert finding is not None
        self.assertEqual(finding.chain.span, (6, 36))
        self.assertEqual((finding.start_year, finding.end_year), (911, 1308))
        self.assertEqual(finding.covered, 30)
        self.assertEqual(finding.span_length, 31)
        self.assertAlmostEqual(finding.local_coverage, 30 / 31)

    def test_permutation_repeats_free_interval_search(self):
        first = assess_interval(
            self.sequence, self.config, motif=self.motif,
            timeline=self.timeline, trials=20, seed=7,
        )
        second = assess_interval(
            self.sequence, self.config, motif=self.motif,
            timeline=self.timeline, trials=20, seed=7,
        )
        self.assertEqual(first[1].scores, second[1].scores)  # type: ignore[union-attr]
        self.assertGreater(first[2], 0.0)

    def test_report_states_global_correction_and_years(self):
        finding, null, p_value = assess_interval(
            self.sequence, self.config, motif=self.motif,
            timeline=self.timeline, trials=20, seed=7,
        )
        report = format_interval_report(self.sequence, finding, null, p_value)
        self.assertIn("(911–1308)", report)
        self.assertIn("Globaler p-Wert:", report)
        self.assertIn("freie Intervallsuche", report)


class TestPeriodComparison(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.timeline = load_timeline(PROJECT / "HRR_Kings_843_1806.csv")
        cls.config = SearchConfig(
            min_blocks=3,
            max_deviations=0,
            allowed_d=(0, 1),
            families=(PatternKind.FIXED, PatternKind.BOOKEND),
        )

    def test_period_parser_and_inclusive_selection(self):
        early, late = parse_period_pair("911:1313,1314:1806")
        self.assertEqual(early, PeriodSpec(911, 1313))
        self.assertEqual(late, PeriodSpec(1314, 1806))
        early_names, early_timeline = select_period(self.timeline, early)
        late_names, late_timeline = select_period(self.timeline, late)
        self.assertEqual(len(early_names), 31)
        self.assertEqual(len(late_names), 27)
        self.assertEqual(early_timeline[0].elevation_year, 911)
        self.assertEqual(late_timeline[0].elevation_year, 1314)

    def test_pair_assessment_is_reproducible_and_searches_both_families(self):
        args = (
            self.timeline,
            self.config,
            PeriodSpec(911, 1313),
            PeriodSpec(1314, 1806),
        )
        first = assess_period_pair(*args, trials=12, seed=11)
        second = assess_period_pair(*args, trials=12, seed=11)
        self.assertEqual(first.null_differences, second.null_differences)
        self.assertEqual(first.p_value, second.p_value)
        self.assertIsNotNone(first.first.finding)
        # Im spaeten HRR-Abschnitt erfuellt derzeit keine Kette die
        # Mindestanforderung von drei Bloecken. Das ist ein gueltiges
        # Negativkontroll-Ergebnis, kein Fehler der Suche.
        self.assertIsNone(first.second.finding)
        self.assertEqual(first.second.strength, 0.0)

    def test_report_contains_all_three_tests(self):
        result = assess_period_pair(
            self.timeline,
            self.config,
            PeriodSpec(911, 1313),
            PeriodSpec(1314, 1806),
            trials=12,
            seed=11,
        )
        report = format_period_contrast(result)
        self.assertIn("Zeitraum 911–1313", report)
        self.assertIn("Zeitraum 1314–1806", report)
        self.assertIn("FIXED und BOOKEND", report)
        self.assertIn("Vergleichs-p-Wert", report)


if __name__ == "__main__":
    unittest.main()
