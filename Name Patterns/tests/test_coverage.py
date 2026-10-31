"""Tests fuer die Abdeckung: wie viel der Liste ein Muster erklaert.

Die Blockzahl allein misst das nicht.  Drei Bloecke zu je drei Namen erklaeren
neun Positionen, drei zu je acht vierundzwanzig -- fuer die Frage "ist diese
Anordnung geordneter als eine zufaellige?" ist das der entscheidende Unterschied.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from name_patterns.data import load_names
from name_patterns.inspect_null import best_chain, permutations
from name_patterns.model import Block, Chain, PatternKind, Placement, SearchConfig
from name_patterns.scoring import Measure, assess, build_null_model, chain_statistic
from name_patterns.search import find_bookend_chains

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


def chain_of(spans):
    return Chain(
        anchor=(),
        echo="",
        x0=0,
        d=0,
        kind=PatternKind.BOOKEND,
        placements=[
            Placement(
                chain_index=i,
                block=Block(anchor_pos=a, x=b - a - 1, echo_pos=b, name="N"),
                expected_x=b - a - 1,
            )
            for i, (a, b) in enumerate(spans)
        ],
    )


class TestCoverageArithmetic(unittest.TestCase):
    def test_covered_counts_bookends_too(self):
        self.assertEqual(chain_of([(0, 2)]).covered, 3)

    def test_disjoint_blocks_add_up(self):
        self.assertEqual(chain_of([(0, 2), (5, 7)]).covered, 6)

    def test_coverage_is_a_share_of_the_whole_list(self):
        self.assertAlmostEqual(chain_of([(0, 4)]).coverage(10), 0.5)

    def test_outsiders_include_head_and_tail(self):
        """Namen vor dem ersten und nach dem letzten Block brechen auch aus."""
        chain = chain_of([(2, 4)])
        self.assertEqual(chain.outsiders(7), [0, 1, 5, 6])

    def test_max_outsider_run_spans_the_edges(self):
        chain = chain_of([(4, 6)])
        self.assertEqual(chain.max_outsider_run(10), 4)

    def test_max_outsider_run_is_zero_when_fully_covered(self):
        self.assertEqual(chain_of([(0, 4)]).max_outsider_run(5), 0)

    def test_empty_total_is_safe(self):
        self.assertEqual(chain_of([(0, 1)]).coverage(0), 0.0)


class TestDenmarkCoverage(unittest.TestCase):
    """Die gemessenen Werte der Königsliste."""

    def setUp(self):
        self.sequence = denmark()
        self.chain = find_bookend_chains(self.sequence, CONFIG)[0]

    def test_covers_all_but_three_kings(self):
        total = len(self.sequence)
        self.assertEqual(self.chain.covered, 24)
        self.assertEqual(total, 27)
        self.assertAlmostEqual(self.chain.coverage(total), 24 / 27)

    def test_the_three_outsiders_are_gorm_waldemar_and_knut(self):
        outsiders = self.chain.outsiders(len(self.sequence))
        self.assertEqual(outsiders, [0, 17, 18])
        self.assertEqual(
            [self.sequence[i] for i in outsiders], ["Gorm", "Waldemar", "Knut"]
        )

    def test_longest_unstructured_stretch_is_two(self):
        self.assertEqual(self.chain.max_outsider_run(len(self.sequence)), 2)


class TestMeasure(unittest.TestCase):
    def test_coverage_statistic_differs_from_bits(self):
        sequence = denmark()
        chain = find_bookend_chains(sequence, CONFIG)[0]
        self.assertNotAlmostEqual(
            chain_statistic(sequence, chain, Measure.COVERAGE),
            chain_statistic(sequence, chain, Measure.BITS),
        )

    def test_missing_chain_scores_zero(self):
        self.assertEqual(chain_statistic(denmark(), None, Measure.COVERAGE), 0.0)

    def test_null_model_records_its_measure(self):
        null = build_null_model(
            denmark(), CONFIG, trials=10, seed=1, measure=Measure.COVERAGE
        )
        self.assertIs(null.measure, Measure.COVERAGE)
        self.assertTrue(all(0.0 <= s <= 1.0 for s in null.scores))

    def test_coverage_separates_the_danish_finding_from_noise(self):
        """Der Kern der Sache.

        Nach Bit ist der Befund nicht signifikant, weil kurze Zufallsketten
        gleich viel zaehlen.  Nach Abdeckung schon, weil dort die Blocklaenge
        mitzaehlt.
        """
        sequence = denmark()
        chains = find_bookend_chains(sequence, CONFIG)
        _, by_bits = assess(
            sequence, chains, CONFIG, trials=500, seed=42, measure=Measure.BITS
        )
        scored, by_coverage = assess(
            sequence, chains, CONFIG, trials=500, seed=42, measure=Measure.COVERAGE
        )
        best = scored[0]
        self.assertGreater(by_bits.p_value(best.bits), 0.05)
        self.assertLess(by_coverage.p_value(best.coverage), 0.05)


class TestConjectureRefuted(unittest.TestCase):
    def test_a_shuffle_reaches_higher_coverage_than_the_original(self):
        """Die Königsliste ist nicht die geordnetste mögliche Anordnung.

        Umsortierung 622 (Startwert 42) kachelt die Liste lückenlos mit drei
        Blöcken zu je neun Namen -- 27 von 27 gegenüber 24 von 27.
        """
        sequence = denmark()
        total = len(sequence)
        original = best_chain(sequence, CONFIG, Measure.COVERAGE)
        self.assertEqual(original.covered, 24)

        for index, shuffled in enumerate(permutations(sequence, 700, seed=42), 1):
            if index != 622:
                continue
            chain = best_chain(shuffled, CONFIG, Measure.COVERAGE)
            self.assertIsNotNone(chain)
            self.assertEqual(chain.covered, total)
            self.assertEqual(chain.max_outsider_run(total), 0)
            self.assertEqual(len(chain.placements), 3)
            self.assertEqual([p.block.length for p in chain.placements], [9, 9, 9])
            break
        else:
            self.fail("Umsortierung 622 nicht erreicht")



class TestNorwayCoverage(unittest.TestCase):
    """Die Gegenprobe: dieselbe Messgroesse auf der norwegischen Liste.

    Die Abdeckung wurde an Daenemark entwickelt; Norwegen hat dabei keine Rolle
    gespielt.  Dass der Befund dort ebenso signifikant ausfaellt, ist deshalb
    eine Bestaetigung und keine Anpassung.
    """

    def setUp(self):
        self.sequence = load_names(PROJECT / "Norway_Kings.txt")
        self.chain = find_bookend_chains(self.sequence, CONFIG)[0]

    def test_four_blocks_cover_all_but_six_kings(self):
        total = len(self.sequence)
        self.assertEqual(total, 34)
        self.assertEqual(len(self.chain.placements), 4)
        self.assertEqual(self.chain.covered, 28)
        self.assertEqual(len(self.chain.outsiders(total)), 6)
        self.assertEqual(self.chain.max_outsider_run(total), 4)

    def test_significant_under_coverage_but_not_under_bits(self):
        chains = find_bookend_chains(self.sequence, CONFIG)
        scored, by_coverage = assess(
            self.sequence, chains, CONFIG, trials=500, seed=42,
            measure=Measure.COVERAGE,
        )
        _, by_bits = assess(
            self.sequence, chains, CONFIG, trials=500, seed=42, measure=Measure.BITS
        )
        best = scored[0]
        self.assertLess(by_coverage.p_value(best.coverage), 0.05)
        self.assertGreater(by_bits.p_value(best.bits), 0.05)

    def test_a_tight_bound_cuts_off_the_fourth_block(self):
        """Vor dem vierten Block stehen vier unsystematische Koenige.

        Anders als bei Daenemark ist die Schranke hier nicht beliebig: unter 4
        sucht man ein anderes Muster.
        """
        tight = SearchConfig(
            max_deviations=0, min_blocks=3, allowed_d=(0,),
            max_interruption=2, families=(PatternKind.BOOKEND,),
        )
        chains = find_bookend_chains(self.sequence, tight)
        self.assertTrue(all(len(c.placements) < 4 for c in chains))


class TestScotlandCoverage(unittest.TestCase):
    """Schottland: der bislang deutlichste Befund.

    Als einzige der drei Listen ist er auch unter der Bit-Messung signifikant.
    Der Grund liegt in der Namensverteilung: 17 verschiedene Namen auf 27
    Positionen, Simpson-Index 0.078 -- Zufallsklammern sind hier viel teurer
    als in Daenemark (11 Namen, 0.133).
    """

    def setUp(self):
        self.sequence = load_names(PROJECT / "Scotland_Kings.txt")
        self.chain = find_bookend_chains(self.sequence, CONFIG)[0]

    def test_ordinals_are_normalised_in_either_spelling(self):
        """Die Quelldatei stand zeitweise als 'DuncanI.' ohne Leerzeichen da.

        Der Test prueft deshalb das Ergebnis, nicht die Schreibweise: beide
        Formen muessen auf denselben Rufnamen fuehren.
        """
        from name_patterns.data import given_name

        self.assertEqual(self.sequence[14], "Duncan")
        self.assertEqual(given_name("DuncanI."), "Duncan")
        self.assertEqual(given_name("Duncan I."), "Duncan")

    def test_four_blocks_of_six_with_four_distinct_bookends(self):
        self.assertEqual(len(self.chain.placements), 4)
        self.assertEqual([p.block.length for p in self.chain.placements], [6, 6, 6, 6])
        self.assertTrue(self.chain.distinct_bookends)

    def test_covers_all_but_three_kings_with_no_gap_longer_than_one(self):
        total = len(self.sequence)
        self.assertEqual(total, 27)
        self.assertEqual(self.chain.covered, 24)
        self.assertEqual(self.chain.max_outsider_run(total), 1)

    def test_significant_under_both_measures(self):
        """Anders als Daenemark und Norwegen haelt der Befund auch nach Bit."""
        chains = find_bookend_chains(self.sequence, CONFIG)
        scored, by_coverage = assess(
            self.sequence, chains, CONFIG, trials=500, seed=42,
            measure=Measure.COVERAGE,
        )
        _, by_bits = assess(
            self.sequence, chains, CONFIG, trials=500, seed=42, measure=Measure.BITS
        )
        best = scored[0]
        self.assertLess(by_coverage.p_value(best.coverage), 0.05)
        self.assertLess(by_bits.p_value(best.bits), 0.05)

    def test_no_shuffle_in_the_sample_exceeds_the_original(self):
        """Empirisch, nicht bewiesen: in 500 Umsortierungen kommt keine darueber.

        Anders als bei Daenemark, wo eine Permutation die Liste lueckenlos
        kachelt.  Das ist eine Aussage ueber die Stichprobe, kein Beweis, dass
        24/27 das theoretische Maximum waere.
        """
        total = len(self.sequence)
        for shuffled in permutations(self.sequence, 500, seed=42):
            chain = best_chain(shuffled, CONFIG, Measure.COVERAGE)
            if chain is not None:
                self.assertLessEqual(chain.covered, self.chain.covered)
                self.assertLess(chain.covered, total)

if __name__ == "__main__":
    unittest.main()
