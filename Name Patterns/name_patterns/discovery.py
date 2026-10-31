"""Stufe 3: Anchor und Echo automatisch finden statt sie vorzugeben.

Der Suchraum waere naiv riesig (alle Namenstupel x alle Namen).  Zwei exakte
Prunings machen ihn klein, ohne einen Treffer zu verlieren:

* Jeder Block einer Kette braucht ein Anchor-Vorkommen -- ein Anchor, der
  seltener als ``min_blocks`` mal auftritt, kann keine gueltige Kette tragen.
* Dasselbe gilt fuer das Echo.

Beides sind harte Notwendigkeiten, keine Heuristiken: was hier wegfaellt,
haette ohnehin keine Kette der geforderten Mindestlaenge ergeben.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Dict, FrozenSet, List, Sequence, Tuple

from .index import build_occurrences
from .model import Chain, Names, PatternKind, SearchConfig
from .search import find_bookend_chains, find_chains


@dataclass(frozen=True)
class Motif:
    """Ein Anchor/Echo-Paar, das die Suche ausprobieren soll."""

    anchor: Tuple[str, ...]
    echo: str

    def __str__(self) -> str:
        return f"{' '.join(self.anchor)} ... {self.echo}"


def frequent_ngrams(
    sequence: Names, length: int, min_count: int
) -> List[Tuple[str, ...]]:
    """Alle zusammenhaengenden n-Gramme, die mindestens ``min_count`` mal vorkommen."""
    if length <= 0 or length > len(sequence):
        return []
    counts: Counter = Counter(
        tuple(sequence[i : i + length])
        for i in range(len(sequence) - length + 1)
    )
    return sorted(gram for gram, count in counts.items() if count >= min_count)


def candidate_motifs(sequence: Names, config: SearchConfig) -> List[Motif]:
    """Alle Anchor/Echo-Paare, die ueberhaupt eine Kette tragen koennen.

    Enthaelt bewusst auch den Fall ``anchor == (echo,)`` -- also die schlichte
    Wiederholung eines einzelnen Namens in regelmaessigen Abstaenden.
    """
    occurrences = build_occurrences(sequence)
    echoes = sorted(
        name for name, positions in occurrences.items()
        if len(positions) >= config.min_blocks
    )
    anchors: List[Tuple[str, ...]] = []
    for length in range(1, max(1, config.max_anchor_len) + 1):
        anchors.extend(frequent_ngrams(sequence, length, config.min_blocks))

    return [Motif(anchor=anchor, echo=echo) for anchor in anchors for echo in echoes]


def discover(sequence: Names, config: SearchConfig) -> List[Chain]:
    """Sucht ueber alle Motivkandidaten beider Familien und sammelt die Ketten.

    Sortiert nach :attr:`Chain.score`; die inhaltlich aussagekraeftigere
    Reihenfolge stellt :mod:`name_patterns.scoring` her, das die Seltenheit der
    beteiligten Namen mitbewertet.

    Die Familie BOOKEND braucht keine Kandidatenaufzaehlung: ihr Motiv ist eine
    freie Variable, also gibt es genau eine Suche statt vieler.
    """
    chains: List[Chain] = []
    if config.searches(PatternKind.FIXED):
        for motif in candidate_motifs(sequence, config):
            chains.extend(find_chains(sequence, motif.anchor, motif.echo, config))
    if config.searches(PatternKind.BOOKEND):
        chains.extend(find_bookend_chains(sequence, config))
    return collapse_restatements(chains)


def collapse_restatements(chains: Sequence[Chain]) -> List[Chain]:
    """Fasst Ketten zusammen, die dieselbe Regelmaessigkeit anders benennen.

    Beispiel: ``Konrad Heinrich ... Heinrich`` und ``Heinrich ... Heinrich``
    koennen exakt dieselben Echo-Positionen treffen.  Dann beschreiben sie
    denselben Befund, und nur die spezifischere Variante (laengerer Anchor,
    also unwahrscheinlicheres Motiv) bleibt stehen.
    """
    ordered = sorted(
        chains,
        key=lambda c: (-c.score, -len(c.anchor), len(c.deviations), c.span[0]),
    )
    seen: Dict[Tuple[FrozenSet[int], int], Chain] = {}
    result: List[Chain] = []
    for chain in ordered:
        key = (frozenset(p.block.echo_pos for p in chain.placements), chain.d)
        if key in seen:
            continue
        seen[key] = chain
        result.append(chain)
    return result
