"""Tests fuer die Sichtbarmachung der Nullmodell-Umsortierungen."""

from __future__ import annotations

import unittest
from collections import Counter
from pathlib import Path

from name_patterns.data import load_names
from name_patterns.inspect_null import (
    best_chain,
    build_markdown,
    permutations,
)
from name_patterns.model import PatternKind, SearchConfig
from name_patterns.scoring import build_null_model, chain_bits, name_probabilities

PROJECT = Path(__file__).resolve().parent.parent

CONFIG = SearchConfig(
    max_deviations=0,
    min_blocks=3,
    allowed_d=(0,),
    max_interruption=4,
    families=(PatternKind.BOOKEND,),
)


def denmark():
    return load_names(PROJECT / "Denmark_Kings.txt")


class TestPermutations(unittest.TestCase):
    def test_same_seed_reproduces_the_same_order(self):
        first = list(permutations(denmark(), 5, seed=42))
        second = list(permutations(denmark(), 5, seed=42))
        self.assertEqual(first, second)

    def test_each_permutation_keeps_the_name_multiset(self):
        """Das Nullmodell sortiert nur um -- Haeufigkeiten bleiben exakt gleich."""
        sequence = denmark()
        expected = Counter(sequence)
        for shuffled in permutations(sequence, 20, seed=1):
            self.assertEqual(Counter(shuffled), expected)
            self.assertEqual(len(shuffled), len(sequence))

    def test_permutations_actually_differ(self):
        sequence = denmark()
        shuffles = list(permutations(sequence, 10, seed=1))
        self.assertNotEqual(shuffles[0], sequence)
        self.assertNotEqual(shuffles[0], shuffles[1])

    def test_they_are_the_permutations_the_p_value_is_built_on(self):
        """Kernzusage der Datei: gezeigt wird, worauf der p-Wert beruht.

        Wuerde hier eine andere Zufallsfolge entstehen, waere die Tabelle
        huebsch, aber nicht die Grundlage des Tests.
        """
        sequence = denmark()
        probs = name_probabilities(sequence)
        trials, seed = 30, 42

        from_module = [
            max((chain_bits(probs, c) for c in [best_chain(p, CONFIG)] if c), default=0.0)
            for p in permutations(sequence, trials, seed)
        ]
        null = build_null_model(sequence, CONFIG, trials=trials, seed=seed)
        self.assertEqual(from_module, list(null.scores))


class TestMarkdown(unittest.TestCase):
    def setUp(self):
        self.sequence = denmark()
        self.text = build_markdown(
            self.sequence, CONFIG, trials=10, seed=42, source="Denmark_Kings.txt"
        )

    def test_contains_a_row_per_permutation_plus_the_original(self):
        rows = [
            line for line in self.text.splitlines()
            if line.startswith("| ") and "---" not in line
        ]
        # Kopfzeilen der drei Tabellen plus Originalzeile plus 10 Permutationen.
        permutation_rows = [
            line for line in rows
            if line.startswith("| 1 |") or line.startswith("| **Original**")
        ]
        self.assertTrue(permutation_rows)
        self.assertIn("| **Original** |", self.text)

    def test_every_king_appears_in_the_original_row(self):
        original = next(
            line for line in self.text.splitlines()
            if line.startswith("| **Original**")
        )
        for name in set(self.sequence):
            self.assertIn(name, original)

    def test_bookends_of_the_reference_chain_are_marked(self):
        reference = best_chain(self.sequence, CONFIG)
        self.assertIsNotNone(reference)
        original = next(
            line for line in self.text.splitlines()
            if line.startswith("| **Original**")
        )
        for name in reference.bookend_names:
            self.assertIn(f"**{name}**", original)

    def test_reports_both_criteria(self):
        self.assertIn("irgendeine Kette gleicher Güte", self.text)
        self.assertIn("gleiche Blocklänge", self.text)
        self.assertIn("Bonferroni", self.text)

    def test_stats_can_use_more_permutations_than_the_table_shows(self):
        text = build_markdown(
            self.sequence,
            CONFIG,
            trials=5,
            seed=42,
            source="Denmark_Kings.txt",
            stats_trials=50,
        )
        self.assertIn("Über **50** Permutationen", text)
        self.assertIn("die Tabelle oben zeigt die ersten 5", text)

    def test_survives_a_list_without_any_pattern(self):
        text = build_markdown(
            [f"n{i}" for i in range(20)],
            CONFIG,
            trials=3,
            seed=1,
            source="synthetic",
        )
        self.assertIn("Die Umsortierungen", text)


if __name__ == "__main__":
    unittest.main()
