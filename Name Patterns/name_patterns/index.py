"""Phase 1+2: Vorkommen indizieren und Blockkandidaten einsammeln."""

from __future__ import annotations

from bisect import bisect_right
from collections import defaultdict
from typing import Dict, List, Optional, Sequence, Tuple

from .model import Block, Names


def build_occurrences(sequence: Names) -> Dict[str, List[int]]:
    """Name -> aufsteigende Liste seiner Positionen."""
    occ: Dict[str, List[int]] = defaultdict(list)
    for i, name in enumerate(sequence):
        occ[name].append(i)
    return dict(occ)


def find_anchor_positions(sequence: Names, anchor: Tuple[str, ...]) -> List[int]:
    """Alle Startpositionen, an denen das Anchor-Tupel zusammenhaengend passt."""
    if not anchor:
        raise ValueError("anchor darf nicht leer sein")
    k = len(anchor)
    return [
        i
        for i in range(len(sequence) - k + 1)
        if tuple(sequence[i : i + k]) == anchor
    ]


def find_blocks(
    sequence: Names,
    anchor: Tuple[str, ...],
    echo: str,
    max_gap: int,
) -> List[Block]:
    """Alle Blockkandidaten ``anchor + x Fuellnamen + echo``.

    Aufsteigend sortiert nach ``(anchor_pos, x)``.  Es wird bewusst *jeder*
    Kandidat gesammelt -- welche davon zu einer Kette gehoeren, entscheidet
    erst :mod:`name_patterns.search`.  Ein gieriger Ansatz ("nimm den naechsten
    passenden Block") scheitert an den echten Daten, weil dort ein Konrad
    mitten in einem Block steht und faelschlich als Blockstart erkannt wuerde.
    """
    k = len(anchor)
    blocks: List[Block] = []
    for a in find_anchor_positions(sequence, anchor):
        for x in range(0, max_gap + 1):
            e = a + k + x
            if e >= len(sequence):
                break
            if sequence[e] == echo:
                blocks.append(Block(anchor_pos=a, x=x, echo_pos=e))
    return blocks


def find_bookend_blocks(sequence: Names, max_gap: int) -> List[Block]:
    """Alle Bloecke, die von *demselben* Namen eingeklammert werden.

    Der Klammername ist hier eine freie Variable: gesucht ist ``?N ... ?N``,
    und ``?N`` wird pro Block neu gebunden.  Kein festes Anchor/Echo-Paar kann
    das ausdruecken -- deshalb eine eigene Blocksuche.

    Statt alle Positionspaare durchzugehen, laeuft die Suche ueber die
    Vorkommensliste je Name: das ist genau die Menge der moeglichen Klammern.
    """
    blocks: List[Block] = []
    for name, positions in build_occurrences(sequence).items():
        for i, start in enumerate(positions):
            for end in positions[i + 1 :]:
                x = end - start - 1
                if x > max_gap:
                    break
                blocks.append(Block(anchor_pos=start, x=x, echo_pos=end, name=name))
    blocks.sort(key=lambda b: (b.anchor_pos, b.x))
    return blocks


def candidate_range(
    anchor_positions: Sequence[int],
    previous_echo: int,
    max_interruption: Optional[int],
) -> Tuple[int, int]:
    """Indexfenster der Bloecke, die auf ein Echo an ``previous_echo`` folgen duerfen.

    Untere Grenze: Ketten duerfen sich nicht ueberschneiden, der naechste
    Anchor muss also hinter dem aktuellen Echo liegen.  Obere Grenze: hoechstens
    ``max_interruption`` Namen dazwischen -- bei ``None`` entfaellt sie.

    ``anchor_positions`` muss aufsteigend sortiert sein.
    """
    low = bisect_right(anchor_positions, previous_echo)
    if max_interruption is None:
        return low, len(anchor_positions)
    return low, bisect_right(anchor_positions, previous_echo + max_interruption + 1)
