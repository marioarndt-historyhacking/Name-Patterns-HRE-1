"""Lesbare Ausgabe gefundener Ketten."""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence

from .model import Chain, DeviationKind, Names, PatternKind
from .scoring import Measure, NullModel, ScoredChain


def format_chain(
    sequence: Names,
    chain: Chain,
    show_context: bool = True,
    extra: Optional[Sequence[str]] = None,
) -> str:
    """Eine Kette als mehrzeiligen Textblock."""
    head = [
        f"Muster:      {chain.describe_motif()}",
        f"Regel:       {chain.rule()}",
        f"Bloecke:     {len(chain.placements)}"
        f"   Abweichungen: {len(chain.deviations)}"
        f"   Score: {chain.score:.2f}",
    ]
    if chain.kind is PatternKind.BOOKEND:
        names = " / ".join(chain.bookend_names)
        distinct = "alle verschieden" if chain.distinct_bookends else "mit Wiederholung"
        head.append(f"Klammern:    {names}   ({distinct})")
        head.append(
            f"Blocklaenge: {chain.placements[0].block.length} Namen"
            + (" je Block" if chain.d == 0 else ", wachsend")
        )
    gaps = interruptions(chain)
    if gaps:
        head.append(
            "Zwischen:    "
            + ", ".join(str(gap) for gap in gaps)
            + "  (Namen zwischen den Bloecken)"
        )
    head.extend(extra or [])
    head.append(f"Bereich:     Index {chain.span[0]}..{chain.span[1]}")
    if not show_context:
        return "\n".join(head)

    by_index = {p.chain_index: p for p in chain.placements}
    skips: Dict[int, object] = {
        dev.chain_index: dev
        for dev in chain.deviations
        if dev.kind is DeviationKind.SKIP
    }
    last = max(list(by_index) + list(skips))

    rows: List[str] = []
    for j in range(last + 1):
        expected = chain.expected_x_at(j)
        if j in skips:
            rows.append(f"  j={j}  {'--':>9}  Soll x={expected}   (uebersprungen)")
            continue
        placement = by_index.get(j)
        if placement is None:
            continue
        block = placement.block
        marker = " !" if placement.deviation is not None else "  "
        position = f"{block.anchor_pos}..{block.echo_pos}"
        rows.append(
            f"  j={j}  {position:>9}  x={block.x}{marker} "
            f"{_render_block(sequence, chain, placement.block)}"
        )
    return "\n".join(head + [""] + rows)


def interruptions(chain: Chain) -> List[int]:
    """Namen zwischen je zwei aufeinanderfolgenden Bloecken."""
    blocks = chain.blocks
    return [
        later.anchor_pos - earlier.echo_pos - 1
        for earlier, later in zip(blocks, blocks[1:])
    ]


def _render_block(sequence: Names, chain: Chain, block) -> str:
    # Bei einer freien Klammer ist der Anchor genau ein Name.
    k = 1 if chain.kind is PatternKind.BOOKEND else len(chain.anchor)
    anchor = " ".join(sequence[block.anchor_pos : block.anchor_pos + k])
    fillers = sequence[block.anchor_pos + k : block.echo_pos]
    filler_text = " ".join(fillers)
    return f"{anchor} [{filler_text}] {sequence[block.echo_pos]}"


def format_report(sequence: Names, chains: Iterable[Chain], limit: int = 5) -> str:
    """Die besten Ketten untereinander (ohne Bewertung nach Seltenheit)."""
    chains = list(chains)
    if not chains:
        return "Keine Kette gefunden, die die Vorgaben erfuellt."

    parts: List[str] = [f"{len(chains)} Kette(n) gefunden."]
    for rank, chain in enumerate(chains[:limit], start=1):
        parts.append("")
        parts.append(f"--- #{rank} " + "-" * 56)
        parts.append(format_chain(sequence, chain))
        parts.extend(_deviation_lines(chain))
    if len(chains) > limit:
        parts.append("")
        parts.append(f"... {len(chains) - limit} weitere ausgeblendet.")
    return "\n".join(parts)


def format_scored_report(
    sequence: Names,
    scored: Sequence[ScoredChain],
    null: Optional[NullModel] = None,
    limit: int = 5,
) -> str:
    # Die Messgroesse gehoert an den p-Wert: derselbe Befund bekommt je nach
    # Wahl 0.02 oder 0.37, und ohne den Zusatz ist nicht erkennbar, welcher
    # von beiden gerade dasteht.
    """Bewertete Ketten inklusive Seltenheit und -- falls vorhanden -- p-Wert."""
    if not scored:
        return "Keine Kette gefunden, die die Vorgaben erfuellt."

    parts: List[str] = [f"{len(scored)} Kette(n) gefunden."]
    for rank, entry in enumerate(scored[:limit], start=1):
        extra = [
            f"Abdeckung:   {entry.chain.covered}/{len(sequence)} Namen "
            f"({entry.coverage:.0%}), {entry.outsiders} ausserhalb, "
            f"laengste Aussenstrecke {entry.max_outsider_run}",
            f"Seltenheit:  {entry.bits:.1f} Bit",
        ]
        if entry.p_value is not None:
            basis = (
                "Abdeckung"
                if null is not None and null.measure is Measure.COVERAGE
                else "Bit"
            )
            extra.append(
                f"p-Wert:      {entry.p_value:.4f}   (gemessen an {basis})"
            )
            extra.append(
                "Signifikant:  "
                + ("ja (p < 0.05)" if entry.significant else "nein (p >= 0.05)")
            )
        parts.append("")
        parts.append(f"--- #{rank} " + "-" * 56)
        parts.append(format_chain(sequence, entry.chain, extra=extra))
        parts.extend(_deviation_lines(entry.chain))
    if len(scored) > limit:
        parts.append("")
        parts.append(f"... {len(scored) - limit} weitere ausgeblendet.")
    if null is not None:
        parts.append("")
        parts.append(format_null_model(null))
    return "\n".join(parts)


def format_null_model(null: NullModel) -> str:
    """Kurzfassung der Zufallsverteilung, gegen die geprueft wurde."""
    scope = f"Motiv {null.motif}" if null.motif is not None else "volle Discovery"
    if null.measure is Measure.COVERAGE:
        unit, fmt = "Abdeckung", "{:.0%}"
    else:
        unit, fmt = "Bit", "{:.1f}"
    return "\n".join(
        [
            f"Nullmodell:  {null.trials} Permutationen, {scope}, gemessen an "
            f"{'der Abdeckung' if null.measure is Measure.COVERAGE else 'Bit'}",
            f"             bester Zufallstreffer {fmt.format(null.best)} {unit},"
            f" Mittel {fmt.format(null.mean)}, 95%-Quantil {fmt.format(null.p95)}",
        ]
    )


def _deviation_lines(chain: Chain) -> List[str]:
    return [f"      Abweichung: {dev.describe()}" for dev in chain.deviations]
