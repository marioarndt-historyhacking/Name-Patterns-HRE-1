"""Stufe 4: Bewertung nach Seltenheit und Monte-Carlo-Signifikanz.

Zwei getrennte Groessen, die zusammen erst aussagekraeftig werden:

**bits** -- wie unwahrscheinlich das Motiv als solches ist.  Ein Muster auf
einem sehr haeufigen Namen ist wenig ueberraschend; eines auf seltenen Namen
viel mehr.  Das macht Ketten verschiedener Motive ueberhaupt erst vergleichbar
und ersetzt in der Discovery die reine Kettenlaenge als Rangkriterium.

**p-Wert** -- wie oft ein mindestens so guter Treffer auftaucht, wenn man
dieselbe Namensmenge zufaellig umsortiert.  Das ist die eigentliche Kontrolle:
mit einem Abweichungsbudget von 2 oder 3 findet man in *jeder* hinreichend
langen Liste irgendein "Muster".  Erst der Vergleich gegen den Zufall trennt
Befund von Rauschen.

Das Nullmodell permutiert die Liste.  Die Haeufigkeit jedes Namens bleibt dabei
exakt erhalten -- gepruefte Frage ist also allein, ob die *Anordnung*
bemerkenswert ist.
"""

from __future__ import annotations

import math
import random
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from .discovery import Motif, discover
from .model import Chain, Names, PatternKind, SearchConfig
from .search import find_chains

#: Rueckmeldung waehrend langer Monte-Carlo-Laeufe: (erledigt, gesamt).
Progress = Callable[[int, int], None]


def name_probabilities(sequence: Names) -> Dict[str, float]:
    """Relative Haeufigkeit jedes Namens.

    Unter Permutation invariant -- deshalb genuegt es, sie einmal fuer die
    Originalliste zu berechnen und in allen Monte-Carlo-Durchlaeufen
    weiterzuverwenden.
    """
    total = len(sequence)
    if total == 0:
        return {}
    return {name: count / total for name, count in Counter(sequence).items()}


def block_bits(probs: Dict[str, float], anchor: Tuple[str, ...], echo: str) -> float:
    """Ueberraschungswert eines einzelnen Blocktreffers in Bit.

    Ein Block verlangt, dass an einer Stelle das Anchor-Tupel steht *und* im
    passenden Abstand das Echo.  Unter dem Nullmodell ist das das Produkt der
    Einzelwahrscheinlichkeiten; in Bit also die Summe der Einzelbeitraege.
    """
    p = 1.0
    for name in tuple(anchor) + (echo,):
        p *= probs.get(name, 0.0)
    if p <= 0.0:
        return 0.0
    return -math.log2(p)


def simpson_index(probs: Dict[str, float]) -> float:
    """Wahrscheinlichkeit, dass zwei zufaellige Positionen denselben Namen tragen.

    Summe der quadrierten Haeufigkeiten.  Das ist die richtige Bezugsgroesse
    fuer eine *freie* Klammer ``?N ... ?N``: gefordert ist nicht ein bestimmter
    Name, sondern nur Gleichheit.
    """
    return sum(p * p for p in probs.values())


def bookend_bits(probs: Dict[str, float]) -> float:
    """Ueberraschungswert einer freien Klammer in Bit.

    Deutlich weniger als bei einem festen seltenen Namen -- und genau das ist
    der Punkt: mit freier Variable bildet *jedes* Namenspaar im richtigen
    Abstand einen Blockkandidaten.  Wuerde man hier die Formel fuer feste Namen
    verwenden, bekaeme die Familie BOOKEND systematisch aufgeblaehte Werte und
    verdraengte die spezifischeren Treffer aus der Rangliste.
    """
    collision = simpson_index(probs)
    if collision <= 0.0:
        return 0.0
    return -math.log2(collision)


def chain_bits(probs: Dict[str, float], chain: Chain) -> float:
    """Ueberraschungswert der ganzen Kette in Bit.

    Effektive Blockzahl (Laenge minus Abweichungsstrafe) mal Bit pro Block.
    Abweichungen senken den Wert, laengere Anchor und seltenere Namen heben ihn.
    """
    if chain.kind is PatternKind.BOOKEND:
        per_block = bookend_bits(probs)
    else:
        per_block = block_bits(probs, chain.anchor, chain.echo)
    return max(0.0, chain.score) * per_block


class Measure(str, Enum):
    """Woran gemessen wird, ob eine Anordnung bemerkenswert ist."""

    #: Ueberraschungswert des Motivs.  Fragt: "wie unwahrscheinlich ist dieses
    #: Muster als solches?"  Zaehlt Bloecke, nicht deren Laenge.
    BITS = "bits"
    #: Anteil der Liste, den das Muster erfasst.  Fragt: "wie viel der
    #: Anordnung wird durch die Ordnung erklaert?"  Drei Bloecke zu je acht
    #: Namen erklaeren dreimal so viel wie drei zu je drei -- die Bit-Groesse
    #: sieht darin keinen Unterschied, die Abdeckung schon.
    COVERAGE = "coverage"


def chain_statistic(
    sequence: Names,
    chain: Optional[Chain],
    measure: Measure = Measure.BITS,
    probs: Optional[Dict[str, float]] = None,
) -> float:
    """Die Kennzahl einer Kette unter der gewaehlten Messgroesse."""
    if chain is None:
        return 0.0
    if measure is Measure.COVERAGE:
        return chain.coverage(len(sequence))
    return chain_bits(probs if probs is not None else name_probabilities(sequence), chain)


@dataclass(frozen=True)
class NullModel:
    """Verteilung der besten Trefferguete unter zufaelliger Umsortierung."""

    trials: int
    #: Bester Bit-Wert je Durchlauf.
    scores: Tuple[float, ...]
    #: ``None`` bei motivweiter Suche, sonst das fest vorgegebene Motiv.
    motif: Optional[Motif] = None
    #: Woran gemessen wurde.
    measure: "Measure" = None  # type: ignore[assignment]

    @property
    def best(self) -> float:
        return max(self.scores) if self.scores else 0.0

    @property
    def mean(self) -> float:
        return sum(self.scores) / len(self.scores) if self.scores else 0.0

    @property
    def p95(self) -> float:
        if not self.scores:
            return 0.0
        ordered = sorted(self.scores)
        index = min(len(ordered) - 1, int(0.95 * len(ordered)))
        return ordered[index]

    def p_value(self, observed: float) -> float:
        """Anteil der Durchlaeufe, die mindestens so gut waren.

        Mit Plus-Eins-Korrektur in Zaehler und Nenner -- so wird der p-Wert nie
        exakt 0, was bei endlich vielen Durchlaeufen auch nicht behauptet
        werden darf.
        """
        hits = sum(1 for score in self.scores if score >= observed)
        return (1 + hits) / (1 + self.trials)


@dataclass
class ScoredChain:
    """Eine Kette samt Bewertung."""

    chain: Chain
    bits: float
    p_value: Optional[float] = None
    #: Anteil der Liste, den die Kette erfasst.
    coverage: float = 0.0
    #: Positionen, die aus der Ordnung ausbrechen.
    outsiders: int = 0
    #: Laengste ununterbrochene Strecke ausserhalb aller Bloecke.
    max_outsider_run: int = 0

    @property
    def significant(self) -> bool:
        return self.p_value is not None and self.p_value < 0.05


def score_chains(
    sequence: Names,
    chains: Sequence[Chain],
    measure: Measure = Measure.BITS,
) -> List[ScoredChain]:
    """Bewertet Ketten und sortiert absteigend nach der gewaehlten Messgroesse.

    Die Sortierung muss der Messgroesse folgen: haengt der p-Wert an der
    Abdeckung, waere eine Rangliste nach Bit irrefuehrend -- oben stuende dann
    womoeglich eine Kette mit schlechterem p-Wert als die darunter.
    """
    probs = name_probabilities(sequence)
    total = len(sequence)
    scored = [
        ScoredChain(
            chain=c,
            bits=chain_bits(probs, c),
            coverage=c.coverage(total),
            outsiders=len(c.outsiders(total)),
            max_outsider_run=c.max_outsider_run(total),
        )
        for c in chains
    ]
    if measure is Measure.COVERAGE:
        scored.sort(key=lambda s: (-s.coverage, -s.bits, s.chain.span[0]))
    else:
        scored.sort(key=lambda s: (-s.bits, -s.chain.score, s.chain.span[0]))
    return scored


def build_null_model(
    sequence: Names,
    config: SearchConfig,
    *,
    motif: Optional[Motif] = None,
    trials: int = 500,
    seed: Optional[int] = None,
    progress: Optional[Progress] = None,
    measure: Measure = Measure.BITS,
) -> NullModel:
    """Permutiert die Liste ``trials`` mal und merkt sich den jeweils besten Treffer.

    Ohne ``motif`` wird pro Durchlauf die volle Discovery gefahren.  Das ist
    teurer, aber die ehrliche Vergleichsgroesse, wenn man den Befund selbst per
    Discovery gefunden hat: es beruecksichtigt, dass sehr viele Motive geprueft
    wurden und eines davon rein zufaellig passen konnte.

    Mit ``motif`` wird nur dieses eine Motiv geprueft -- richtig, wenn man eine
    Hypothese vorab hatte.
    """
    probs = name_probabilities(sequence)
    shuffled = list(sequence)
    rng = random.Random(seed)
    scores: List[float] = []

    for done in range(trials):
        rng.shuffle(shuffled)
        if motif is None:
            found = discover(shuffled, config)
        else:
            found = find_chains(shuffled, motif.anchor, motif.echo, config)
        scores.append(
            max(
                (
                    chain_statistic(shuffled, c, measure, probs)
                    for c in found
                ),
                default=0.0,
            )
        )
        if progress is not None:
            progress(done + 1, trials)

    return NullModel(
        trials=trials, scores=tuple(scores), motif=motif, measure=measure
    )


def assess(
    sequence: Names,
    chains: Sequence[Chain],
    config: SearchConfig,
    *,
    motif: Optional[Motif] = None,
    trials: int = 500,
    seed: Optional[int] = None,
    progress: Optional[Progress] = None,
    measure: Measure = Measure.BITS,
) -> Tuple[List[ScoredChain], Optional[NullModel]]:
    """Bewertet Ketten und versieht sie mit p-Werten aus *einem* Nullmodell.

    Das Nullmodell haengt nur an Liste und Konfiguration, nicht an der einzelnen
    Kette -- ein Durchlauf genuegt also fuer alle Treffer.
    """
    scored = score_chains(sequence, chains, measure)
    if trials <= 0 or not scored:
        return scored, None

    null = build_null_model(
        sequence,
        config,
        motif=motif,
        trials=trials,
        seed=seed,
        progress=progress,
        measure=measure,
    )
    for entry in scored:
        observed = entry.coverage if measure is Measure.COVERAGE else entry.bits
        entry.p_value = null.p_value(observed)
    return scored, null
