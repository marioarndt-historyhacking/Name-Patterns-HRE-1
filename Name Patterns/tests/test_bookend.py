"""Tests fuer die Familie BOOKEND: ``?N ... ?N`` mit pro Block freier Variable."""

from __future__ import annotations

import unittest
from pathlib import Path
from typing import List

from name_patterns.data import HRR_KINGS, load_names
from name_patterns.discovery import discover
from name_patterns.index import find_bookend_blocks
from name_patterns.model import PatternKind, SearchConfig
from name_patterns.report import interruptions
from name_patterns.scoring import (
    block_bits,
    bookend_bits,
    chain_bits,
    name_probabilities,
    score_chains,
    simpson_index,
)
from name_patterns.search import find_bookend_chains

PROJECT = Path(__file__).resolve().parent.parent
NORWAY_FILE = PROJECT / "Norway_Kings.txt"


def norway() -> List[str]:
    return load_names(NORWAY_FILE)


class TestBookendBlocks(unittest.TestCase):
    def test_pairs_of_the_same_name_form_blocks(self):
        blocks = find_bookend_blocks(["A", "z", "A"], max_gap=5)
        self.assertEqual([(b.anchor_pos, b.x, b.name) for b in blocks], [(0, 1, "A")])

    def test_every_pair_is_collected_not_just_neighbours(self):
        blocks = find_bookend_blocks(["A", "A", "A"], max_gap=5)
        self.assertEqual(
            sorted((b.anchor_pos, b.echo_pos) for b in blocks),
            [(0, 1), (0, 2), (1, 2)],
        )

    def test_max_gap_limits_the_span(self):
        sequence = ["A", "z", "z", "z", "A"]
        self.assertTrue(
            any(b.name == "A" for b in find_bookend_blocks(sequence, max_gap=3))
        )
        self.assertFalse(
            any(b.name == "A" for b in find_bookend_blocks(sequence, max_gap=2))
        )

    def test_names_occurring_once_produce_nothing(self):
        self.assertEqual(find_bookend_blocks(["A", "B", "C"], max_gap=5), [])

    def test_blocks_are_sorted_by_anchor_position(self):
        blocks = find_bookend_blocks(norway(), max_gap=12)
        positions = [b.anchor_pos for b in blocks]
        self.assertEqual(positions, sorted(positions))


class TestNorwayGoldenCase(unittest.TestCase):
    """Die norwegische Koenigsliste: Olav / Oeystein / Hakon, je 7 Namen."""

    def setUp(self):
        self.sequence = norway()
        self.config = SearchConfig(
            max_deviations=0, min_blocks=3, allowed_d=(0,), max_interruption=3
        )
        self.chains = find_bookend_chains(self.sequence, self.config)

    def test_finds_three_blocks_of_equal_length(self):
        best = self.chains[0]
        self.assertEqual(len(best.placements), 3)
        self.assertEqual(best.d, 0)
        self.assertEqual([p.block.x for p in best.placements], [5, 5, 5])
        self.assertEqual([p.block.length for p in best.placements], [7, 7, 7])

    def test_each_block_is_bracketed_by_a_different_name(self):
        best = self.chains[0]
        self.assertEqual(best.bookend_names, ["Olav", "Öystein", "Hakon"])
        self.assertTrue(best.distinct_bookends)

    def test_block_positions_match_the_source_table(self):
        best = self.chains[0]
        self.assertEqual(
            [(p.block.anchor_pos, p.block.echo_pos) for p in best.placements],
            [(0, 6), (9, 15), (16, 22)],
        )

    def test_interruptions_are_two_and_zero(self):
        """Zwischen Block 1 und 2 stehen Magnus und Olav, zwischen 2 und 3 nichts."""
        self.assertEqual(interruptions(self.chains[0]), [2, 0])

    def test_chain_is_marked_as_bookend_family(self):
        self.assertIs(self.chains[0].kind, PatternKind.BOOKEND)
        self.assertEqual(self.chains[0].describe_motif(), "?N ... ?N")

    def test_found_without_pinning_the_step_width(self):
        """Auch wenn wachsende Blocklaengen zugelassen sind, gewinnt d=0."""
        chains = find_bookend_chains(
            self.sequence,
            SearchConfig(
                max_deviations=0, min_blocks=3, allowed_d=(0, 1), max_interruption=3
            ),
        )
        best = score_chains(self.sequence, chains)[0].chain
        self.assertEqual(best.bookend_names, ["Olav", "Öystein", "Hakon"])

    def test_discovery_finds_it_without_any_hint(self):
        chains = discover(
            self.sequence,
            SearchConfig(
                max_deviations=0, min_blocks=3, allowed_d=(0,), max_interruption=3
            ),
        )
        best = score_chains(self.sequence, chains)[0].chain
        self.assertIs(best.kind, PatternKind.BOOKEND)
        self.assertEqual(best.bookend_names, ["Olav", "Öystein", "Hakon"])


class TestDenmarkGoldenCase(unittest.TestCase):
    """Die daenische Liste: dasselbe Strukturmuster, aber mit 8er-Bloecken."""

    def setUp(self):
        self.sequence = load_names(PROJECT / "Denmark_Kings.txt")
        self.chains = find_bookend_chains(
            self.sequence,
            SearchConfig(
                max_deviations=0, min_blocks=3, allowed_d=(0,), max_interruption=4
            ),
        )

    def test_finds_three_blocks_of_eight(self):
        best = self.chains[0]
        self.assertEqual(len(best.placements), 3)
        self.assertEqual([p.block.x for p in best.placements], [6, 6, 6])
        self.assertEqual([p.block.length for p in best.placements], [8, 8, 8])

    def test_bracketed_by_three_different_names(self):
        best = self.chains[0]
        self.assertEqual(best.bookend_names, ["Harald", "Knut", "Waldemar"])
        self.assertTrue(best.distinct_bookends)

    def test_block_positions(self):
        self.assertEqual(
            [(p.block.anchor_pos, p.block.echo_pos) for p in self.chains[0].placements],
            [(1, 8), (9, 16), (19, 26)],
        )

    def test_interruptions_are_zero_and_two(self):
        self.assertEqual(interruptions(self.chains[0]), [0, 2])

    def test_comma_typo_in_the_source_is_harmless(self):
        """Zeile 15 der Quelldatei schreibt 'Erik III,' mit Komma statt Punkt.

        Die Rufnamen-Regel schneidet ohnehin am ersten Leerzeichen ab, der
        Tippfehler steckt im zweiten Token und richtet keinen Schaden an.
        """
        self.assertEqual(self.sequence[14], "Erik")
        self.assertEqual(self.sequence.count("Erik"), 6)


class TestInterruptionBound(unittest.TestCase):
    def test_tight_bound_breaks_the_norwegian_chain(self):
        """Zwischen Block 1 und 2 liegen 2 Namen -- mit Schranke 1 zerfaellt die Kette."""
        chains = find_bookend_chains(
            norway(),
            SearchConfig(
                max_deviations=0, min_blocks=3, allowed_d=(0,), max_interruption=1
            ),
        )
        self.assertFalse(
            any(c.bookend_names == ["Olav", "Öystein", "Hakon"] for c in chains)
        )

    def test_bound_of_two_still_admits_it(self):
        chains = find_bookend_chains(
            norway(),
            SearchConfig(
                max_deviations=0, min_blocks=3, allowed_d=(0,), max_interruption=2
            ),
        )
        self.assertTrue(
            any(c.bookend_names == ["Olav", "Öystein", "Hakon"] for c in chains)
        )

    def test_unbounded_is_the_default(self):
        self.assertIsNone(SearchConfig().max_interruption)

    def test_bound_applies_to_the_fixed_family_too(self):
        """'Lothar' unterbricht die HRR-Kette um genau einen Namen."""
        from name_patterns.search import find_chains

        strict = find_chains(
            HRR_KINGS,
            ("Konrad", "Heinrich"),
            "Heinrich",
            SearchConfig(max_deviations=0, min_blocks=4, max_interruption=0),
        )
        self.assertEqual(strict, [])
        relaxed = find_chains(
            HRR_KINGS,
            ("Konrad", "Heinrich"),
            "Heinrich",
            SearchConfig(max_deviations=0, min_blocks=4, max_interruption=1),
        )
        self.assertEqual(len(relaxed[0].placements), 4)


class TestBookendScoring(unittest.TestCase):
    def test_simpson_index_is_the_collision_probability(self):
        probs = name_probabilities(["A", "A", "B", "B"])
        self.assertAlmostEqual(simpson_index(probs), 0.5)

    def test_free_bracket_is_less_surprising_than_a_fixed_rare_name(self):
        """Der entscheidende Punkt der Bit-Anpassung.

        Bei freier Variable genuegt *Gleichheit*, nicht ein bestimmter Name.
        Mit der Formel fuer feste Namen bekaeme BOOKEND aufgeblaehte Werte und
        verdraengte die spezifischeren Treffer aus der Rangliste.
        """
        sequence = ["haeufig"] * 90 + ["selten"] * 10
        probs = name_probabilities(sequence)
        self.assertLess(
            bookend_bits(probs), block_bits(probs, ("selten",), "selten")
        )

    def test_chain_bits_uses_the_bookend_formula(self):
        sequence = norway()
        probs = name_probabilities(sequence)
        chains = find_bookend_chains(
            sequence,
            SearchConfig(
                max_deviations=0, min_blocks=3, allowed_d=(0,), max_interruption=3
            ),
        )
        best = chains[0]
        self.assertAlmostEqual(
            chain_bits(probs, best), best.score * bookend_bits(probs)
        )

    def test_uniform_distribution_gives_more_bits_than_a_skewed_one(self):
        uniform = name_probabilities([f"n{i}" for i in range(10)])
        skewed = name_probabilities(["A"] * 9 + ["B"])
        self.assertGreater(bookend_bits(uniform), bookend_bits(skewed))

    def test_empty_distribution_is_safe(self):
        self.assertEqual(bookend_bits({}), 0.0)


class TestFamilySelection(unittest.TestCase):
    def test_bookend_can_be_switched_off(self):
        config = SearchConfig(
            max_deviations=0, min_blocks=3, families=(PatternKind.FIXED,)
        )
        for chain in discover(norway(), config):
            self.assertIs(chain.kind, PatternKind.FIXED)

    def test_fixed_can_be_switched_off(self):
        config = SearchConfig(
            max_deviations=0, min_blocks=3, families=(PatternKind.BOOKEND,)
        )
        for chain in discover(HRR_KINGS, config):
            self.assertIs(chain.kind, PatternKind.BOOKEND)

    def test_hrr_pattern_still_wins_when_both_families_compete(self):
        """Regression: die neue Familie darf den alten Befund nicht verdraengen."""
        config = SearchConfig(max_deviations=0, min_blocks=3)
        self.assertEqual(
            config.families, (PatternKind.FIXED, PatternKind.BOOKEND)
        )
        best = score_chains(HRR_KINGS, discover(HRR_KINGS, config))[0].chain
        self.assertIs(best.kind, PatternKind.FIXED)
        self.assertEqual(best.anchor, ("Konrad", "Heinrich"))


if __name__ == "__main__":
    unittest.main()
