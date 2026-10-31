"""Phase 3: aus Blockkandidaten die laengsten regelmaessigen Ketten bauen.

Kernidee: Sind Startwert ``x0`` und Schrittweite ``d`` festgelegt, steht der
Sollwert an jeder Kettenposition ``j`` fest (``x0 + j*d``).  Damit laesst sich
per Dynamischer Programmierung ueber die Blockkandidaten laufen und die laengste
Kette bestimmen, die dieses Soll einhaelt -- mit einem Budget an Abweichungen.

Der Kern ist unabhaengig davon, *wie* ein Block zustande kam: er schaut nur auf
``x``.  Deshalb tragen ihn beide Musterfamilien gemeinsam -- feste Anchor/Echo
ebenso wie die freie Klammer ``?N ... ?N``.

Entscheidende Festlegung (Stufe 2): nach einer Abweichung laeuft die Progression
am **Sollwert** weiter, nicht am tatsaechlich gemessenen Wert.  Sonst wuerde ein
einzelner Ausreisser die ganze Kette entgleisen lassen.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple, Union

from .index import candidate_range, find_blocks, find_bookend_blocks
from .model import (
    Block,
    Chain,
    Deviation,
    DeviationKind,
    Names,
    PatternKind,
    Placement,
    SearchConfig,
)

#: Ein Schritt in der Kette ist entweder ein gesetzter Block oder ein Auslassen.
Entry = Union[Placement, Deviation]

#: (Anzahl gesetzter Bloecke, Anzahl Abweichungen, Schritte)
Result = Tuple[int, int, List[Entry]]

_EMPTY: Result = (0, 0, [])


def find_chains(
    sequence: Names,
    anchor: Tuple[str, ...],
    echo: str,
    config: SearchConfig,
) -> List[Chain]:
    """Ketten fuer ein festes Anchor/Echo-Paar (Familie FIXED)."""
    blocks = find_blocks(sequence, anchor, echo, config.max_gap)
    return build_chains(blocks, config, kind=PatternKind.FIXED, anchor=anchor, echo=echo)


def find_bookend_chains(sequence: Names, config: SearchConfig) -> List[Chain]:
    """Ketten aus Bloecken, die von demselben Namen eingeklammert werden.

    Familie BOOKEND: der Klammername ist eine freie Variable und wird pro Block
    neu gebunden -- ``Olav ... Olav``, dann ``Oeystein ... Oeystein``, dann
    ``Hakon ... Hakon``.  Was sich wiederholt, ist die Struktur, nicht das Motiv.
    """
    blocks = find_bookend_blocks(sequence, config.max_gap)
    return build_chains(blocks, config, kind=PatternKind.BOOKEND)


def find_chains_for_blocks(
    blocks: Sequence[Block],
    anchor: Tuple[str, ...],
    echo: str,
    config: SearchConfig,
) -> List[Chain]:
    """Wie :func:`find_chains`, aber auf bereits eingesammelten Bloecken."""
    return build_chains(
        list(blocks), config, kind=PatternKind.FIXED, anchor=anchor, echo=echo
    )


def build_chains(
    blocks: Sequence[Block],
    config: SearchConfig,
    *,
    kind: PatternKind = PatternKind.FIXED,
    anchor: Tuple[str, ...] = (),
    echo: str = "",
) -> List[Chain]:
    """Verkettet Blockkandidaten -- gemeinsamer Kern beider Musterfamilien.

    Ergebnis ist nach Score absteigend sortiert und dedupliziert: Ketten, die
    vollstaendig in einer besseren Kette enthalten sind, fallen weg.
    """
    block_list = list(blocks)
    if not block_list:
        return []

    anchor_positions = [b.anchor_pos for b in block_list]
    chains: List[Chain] = []

    for d in config.allowed_d:
        # Memo pro (x0, d) -- verschiedene Startbloecke mit gleichem x0 teilen es.
        memos: Dict[int, Dict[Tuple[int, int, int], Result]] = {}
        for start in block_list:
            memo = memos.setdefault(start.x, {})
            _, _, entries = _extend(
                block_list,
                anchor_positions,
                start.echo_pos,
                1,
                config.max_deviations,
                start.x,
                d,
                config,
                memo,
            )
            chain = _build_chain(
                anchor, echo, start.x, d, start, entries, config, kind
            )
            if len(chain.placements) >= config.min_blocks:
                chains.append(chain)

    return _dedupe(chains)


def _extend(
    blocks: Sequence[Block],
    anchor_positions: Sequence[int],
    previous_echo: int,
    j: int,
    budget: int,
    x0: int,
    d: int,
    config: SearchConfig,
    memo: Dict[Tuple[int, int, int], Result],
) -> Result:
    """Beste Fortsetzung hinter einem Echo an ``previous_echo``, Kettenposition ``j``.

    Maximiert die Zahl gesetzter Bloecke; bei Gleichstand gewinnt die Variante
    mit weniger Abweichungen.

    Der Zustand haengt am *Echo* des Vorgaengers, nicht an dessen Index: zwei
    Bloecke, die an derselben Stelle enden, haben dieselbe Zukunft.
    """
    key = (previous_echo, j, budget)
    cached = memo.get(key)
    if cached is not None:
        return cached

    # j waechst nur durch Setzen (hoechstens einmal je Block) oder Ueberspringen
    # (hoechstens max_deviations mal) -- damit terminiert die Rekursion.
    if j > len(blocks) + config.max_deviations:
        return _EMPTY

    expected = x0 + j * d
    best: Result = _EMPTY
    low, high = candidate_range(
        anchor_positions, previous_echo, config.max_interruption
    )

    for i in range(low, high):
        diff = blocks[i].x - expected
        if diff == 0:
            cost, dev = 0, None
        elif (
            config.allows(DeviationKind.GAP_OFF_BY)
            and budget >= 1
            and abs(diff) <= config.gap_slack
        ):
            cost = 1
            dev = Deviation(
                kind=DeviationKind.GAP_OFF_BY,
                chain_index=j,
                expected_x=expected,
                actual_x=blocks[i].x,
            )
        else:
            continue

        sub_count, sub_devs, sub_entries = _extend(
            blocks,
            anchor_positions,
            blocks[i].echo_pos,
            j + 1,
            budget - cost,
            x0,
            d,
            config,
            memo,
        )
        placement = Placement(
            chain_index=j, block=blocks[i], expected_x=expected, deviation=dev
        )
        candidate = (1 + sub_count, cost + sub_devs, [placement] + sub_entries)
        if _better(candidate, best):
            best = candidate

    if config.allows(DeviationKind.SKIP) and budget >= 1:
        sub_count, sub_devs, sub_entries = _extend(
            blocks,
            anchor_positions,
            previous_echo,
            j + 1,
            budget - 1,
            x0,
            d,
            config,
            memo,
        )
        # Ein Auslassen am Kettenende brauchte niemand -- es kostet nur Budget.
        if sub_count > 0:
            skip = Deviation(
                kind=DeviationKind.SKIP, chain_index=j, expected_x=expected
            )
            candidate = (sub_count, 1 + sub_devs, [skip] + sub_entries)
            if _better(candidate, best):
                best = candidate

    memo[key] = best
    return best


def _better(candidate: Result, current: Result) -> bool:
    """Mehr Bloecke schlaegt weniger; bei Gleichstand weniger Abweichungen."""
    return (candidate[0], -candidate[1]) > (current[0], -current[1])


def _build_chain(
    anchor: Tuple[str, ...],
    echo: str,
    x0: int,
    d: int,
    start_block: Block,
    entries: Sequence[Entry],
    config: SearchConfig,
    kind: PatternKind,
) -> Chain:
    placements: List[Placement] = [
        Placement(chain_index=0, block=start_block, expected_x=x0, deviation=None)
    ]
    deviations: List[Deviation] = []
    for entry in entries:
        if isinstance(entry, Placement):
            placements.append(entry)
            if entry.deviation is not None:
                deviations.append(entry.deviation)
        else:
            deviations.append(entry)
    deviations.sort(key=lambda dev: dev.chain_index)
    return Chain(
        anchor=anchor,
        echo=echo,
        x0=x0,
        d=d,
        placements=placements,
        deviations=deviations,
        deviation_penalty=config.deviation_penalty,
        kind=kind,
    )


def _dedupe(chains: List[Chain]) -> List[Chain]:
    """Verwirft Ketten, die vollstaendig in einer besseren Kette stecken."""
    ordered = sorted(
        chains,
        key=lambda c: (-c.score, len(c.deviations), c.span[0], c.d),
    )
    kept: List[Chain] = []
    kept_sets: List[frozenset] = []
    for chain in ordered:
        signature = frozenset(chain.signature())
        if any(signature <= other for other in kept_sets):
            continue
        kept.append(chain)
        kept_sets.append(signature)
    return kept
