"""Tests fuer Stufe 1 (Kern) und Stufe 2 (Toleranz)."""

from __future__ import annotations

import unittest
from typing import List, Sequence, Tuple

from name_patterns.data import HRR_KINGS
from name_patterns.index import candidate_range, find_blocks
from name_patterns.model import DeviationKind, SearchConfig
from name_patterns.search import find_chains

KH = ("Konrad", "Heinrich")


def build_sequence(gaps: Sequence[int], separator: int = 0) -> List[str]:
    """Baut eine Liste aus Bloecken ``K H <x Fuellnamen> H``.

    Fuellnamen sind eindeutig, damit sie nie zufaellig als Anchor oder Echo
    durchgehen und die Tests genau die vorgegebenen Bloecke pruefen.
    """
    out: List[str] = []
    counter = 0
    for block_index, x in enumerate(gaps):
        if block_index and separator:
            for _ in range(separator):
                out.append(f"sep{counter}")
                counter += 1
        out.extend(KH)
        for _ in range(x):
            out.append(f"f{counter}")
            counter += 1
        out.append("Heinrich")
    return out


def anchor_positions(chain) -> Tuple[int, ...]:
    return tuple(p.block.anchor_pos for p in chain.placements)


class TestBlocks(unittest.TestCase):
    def test_find_blocks_collects_every_candidate(self):
        sequence = build_sequence([3])
        blocks = find_blocks(sequence, KH, "Heinrich", max_gap=12)
        self.assertEqual([(b.anchor_pos, b.x) for b in blocks], [(0, 3)])

    def test_blocks_are_sorted_by_anchor_position(self):
        blocks = find_blocks(HRR_KINGS, KH, "Heinrich", max_gap=12)
        positions = [b.anchor_pos for b in blocks]
        self.assertEqual(positions, sorted(positions))

    def test_candidate_range_skips_overlapping_blocks(self):
        blocks = find_blocks(HRR_KINGS, KH, "Heinrich", max_gap=12)
        positions = [b.anchor_pos for b in blocks]
        for block in blocks:
            low, high = candidate_range(positions, block.echo_pos, None)
            self.assertEqual(high, len(blocks))
            for j in range(low, high):
                self.assertGreater(blocks[j].anchor_pos, block.echo_pos)

    def test_candidate_range_honours_the_interruption_bound(self):
        positions = [0, 5, 9, 20]
        # Echo bei 4, hoechstens 3 Namen dazwischen -> Anchor bis 8 erlaubt.
        low, high = candidate_range(positions, 4, 3)
        self.assertEqual(positions[low:high], [5])

    def test_candidate_range_without_bound_takes_everything_after(self):
        positions = [0, 5, 9, 20]
        low, high = candidate_range(positions, 4, None)
        self.assertEqual(positions[low:high], [5, 9, 20])


class TestGoldenCase(unittest.TestCase):
    """Der historische Fall: Konrad -> Heinrich ... Heinrich mit x = 3,4,5,6."""

    def setUp(self):
        self.config = SearchConfig(max_deviations=0, min_blocks=3)
        self.chains = find_chains(HRR_KINGS, KH, "Heinrich", self.config)

    def test_best_chain_is_the_growing_pattern(self):
        best = self.chains[0]
        self.assertEqual(len(best.placements), 4)
        self.assertEqual(best.x0, 3)
        self.assertEqual(best.d, 1)
        self.assertEqual([p.block.x for p in best.placements], [3, 4, 5, 6])
        self.assertEqual(best.deviations, [])

    def test_konrad_inside_a_block_is_not_used_as_a_block_start(self):
        """Konrad an Index 11 steckt mitten in Block 2.

        Genau hier scheitert ein gieriger Scan, der einfach den naechsten
        Konrad als Blockstart nimmt.
        """
        best = self.chains[0]
        self.assertEqual(anchor_positions(best), (0, 6, 14, 22))
        self.assertNotIn(11, anchor_positions(best))

    def test_blocks_do_not_overlap(self):
        for chain in self.chains:
            blocks = chain.blocks
            for earlier, later in zip(blocks, blocks[1:]):
                self.assertGreater(later.anchor_pos, earlier.echo_pos)

    def test_lothar_between_blocks_costs_no_budget(self):
        """'Lothar' (Index 13) liegt zwischen zwei Bloecken.

        Bloecke muessen nicht aneinandergrenzen, deshalb kostet das keine
        Abweichung -- die Kette wird auch mit Budget 0 gefunden.
        """
        self.assertEqual(self.config.max_deviations, 0)
        self.assertEqual(len(self.chains[0].placements), 4)


class TestConstantGaps(unittest.TestCase):
    def test_finds_constant_pattern(self):
        sequence = build_sequence([2, 2, 2], separator=1)
        chains = find_chains(
            sequence,
            KH,
            "Heinrich",
            SearchConfig(max_deviations=0, min_blocks=3, allowed_d=(0,)),
        )
        best = chains[0]
        self.assertEqual(best.d, 0)
        self.assertEqual(best.x0, 2)
        self.assertEqual([p.block.x for p in best.placements], [2, 2, 2])


class TestTolerance(unittest.TestCase):
    """Stufe 2: geringfuegige Abweichungen."""

    def setUp(self):
        # Soll waere 3,4,5,6 -- tatsaechlich steht an j=2 eine 6.
        self.sequence = build_sequence([3, 4, 6, 6], separator=1)

    def test_strict_search_misses_the_full_chain(self):
        chains = find_chains(
            self.sequence,
            KH,
            "Heinrich",
            SearchConfig(max_deviations=0, min_blocks=4),
        )
        self.assertEqual(chains, [])

    def test_one_deviation_recovers_the_full_chain(self):
        chains = find_chains(
            self.sequence,
            KH,
            "Heinrich",
            SearchConfig(max_deviations=1, min_blocks=4, gap_slack=1),
        )
        best = chains[0]
        self.assertEqual(len(best.placements), 4)
        self.assertEqual(len(best.deviations), 1)
        deviation = best.deviations[0]
        self.assertIs(deviation.kind, DeviationKind.GAP_OFF_BY)
        self.assertEqual(deviation.chain_index, 2)
        self.assertEqual(deviation.expected_x, 5)
        self.assertEqual(deviation.actual_x, 6)

    def test_progression_continues_from_the_expected_value(self):
        """Nach der Abweichung gilt wieder der Sollwert, nicht der Istwert.

        Bei 3,4,6,6 ist der vierte Block nur dann exakt, wenn ab j=3 weiter
        mit 6 (= 3 + 3*1) gerechnet wird und nicht mit 7 (= 6 + 1).
        """
        chains = find_chains(
            self.sequence,
            KH,
            "Heinrich",
            SearchConfig(max_deviations=1, min_blocks=4, gap_slack=1),
        )
        best = chains[0]
        self.assertEqual(best.expected_x_at(3), 6)
        self.assertIsNone(best.placements[3].deviation)

    def test_deviation_beyond_slack_is_rejected(self):
        sequence = build_sequence([3, 4, 9, 6], separator=1)
        chains = find_chains(
            sequence,
            KH,
            "Heinrich",
            SearchConfig(
                max_deviations=1,
                min_blocks=4,
                gap_slack=1,
                allowed_deviations=(DeviationKind.GAP_OFF_BY,),
            ),
        )
        self.assertEqual(chains, [])


class TestSkipDeviation(unittest.TestCase):
    def test_missing_chain_link_is_tolerated(self):
        # x = 3, 4, <fehlt>, 6 -- nur SKIP erlaubt, damit der Fall eindeutig ist.
        sequence = build_sequence([3, 4, 6], separator=1)
        chains = find_chains(
            sequence,
            KH,
            "Heinrich",
            SearchConfig(
                max_deviations=1,
                min_blocks=3,
                allowed_d=(1,),
                allowed_deviations=(DeviationKind.SKIP,),
            ),
        )
        best = chains[0]
        self.assertEqual(len(best.placements), 3)
        self.assertEqual([p.chain_index for p in best.placements], [0, 1, 3])
        self.assertEqual(len(best.deviations), 1)
        self.assertIs(best.deviations[0].kind, DeviationKind.SKIP)
        self.assertEqual(best.deviations[0].chain_index, 2)

    def test_chain_never_ends_on_a_skip(self):
        sequence = build_sequence([3, 4, 5], separator=1)
        chains = find_chains(
            sequence,
            KH,
            "Heinrich",
            SearchConfig(max_deviations=2, min_blocks=3, allowed_d=(1,)),
        )
        for chain in chains:
            last_placement = max(p.chain_index for p in chain.placements)
            for deviation in chain.deviations:
                self.assertLess(deviation.chain_index, last_placement)


class TestNegatives(unittest.TestCase):
    def test_sequence_without_the_motif_yields_nothing(self):
        sequence = [f"n{i}" for i in range(40)]
        chains = find_chains(
            sequence, KH, "Heinrich", SearchConfig(max_deviations=3, min_blocks=3)
        )
        self.assertEqual(chains, [])

    def test_min_blocks_filters_short_chains(self):
        sequence = build_sequence([3, 4], separator=1)
        chains = find_chains(
            sequence, KH, "Heinrich", SearchConfig(max_deviations=0, min_blocks=3)
        )
        self.assertEqual(chains, [])

    def test_empty_anchor_is_rejected(self):
        with self.assertRaises(ValueError):
            find_chains(HRR_KINGS, (), "Heinrich", SearchConfig())


if __name__ == "__main__":
    unittest.main()
