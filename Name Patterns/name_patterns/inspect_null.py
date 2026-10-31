"""Die Umsortierungen des Signifikanztests sichtbar machen.

Der p-Wert sagt nur, *wie oft* der Zufall mithalten konnte -- nicht, wie diese
Zufallstreffer aussehen.  Dieses Modul schreibt die ersten ``N`` Permutationen
als Markdown-Tabelle heraus und markiert diejenigen, die dieselbe
Regelmaessigkeit tragen wie die Ausgangsliste.

Aufruf::

    python3 -m name_patterns.inspect_null --data Denmark_Kings.txt \\
        --d 0 --max-interruption 4 --trials 100 --seed 42 -o Denmark_Null.md

Die Permutationen entstehen exakt wie in :func:`name_patterns.scoring.build_null_model`
-- gleicher Startwert, gleiche Reihenfolge der Aufrufe -- und sind damit
dieselben, auf denen der p-Wert beruht.
"""

from __future__ import annotations

import argparse
import random
from collections import Counter
from pathlib import Path
from typing import Iterator, List, Optional, Sequence, Tuple

from .data import load_names, normalize
from .discovery import discover
from .model import Chain, Names, PatternKind, SearchConfig
from .report import interruptions
from .scoring import Measure, chain_bits, chain_statistic, name_probabilities


def permutations(
    sequence: Names, trials: int, seed: Optional[int]
) -> Iterator[List[str]]:
    """Liefert dieselben Umsortierungen wie das Nullmodell, der Reihe nach."""
    pool = list(sequence)
    rng = random.Random(seed)
    for _ in range(trials):
        rng.shuffle(pool)
        yield list(pool)


def best_chain(
    sequence: Names,
    config: SearchConfig,
    measure: Measure = Measure.BITS,
) -> Optional[Chain]:
    """Die beste Kette einer Liste unter der gewaehlten Messgroesse.

    Wichtig: die Messgroesse entscheidet mit, *welche* Kette als beste gilt.
    Nach Bit gewinnt die mit den meisten Bloecken, nach Abdeckung die, die den
    groessten Teil der Liste erklaert -- das ist nicht dieselbe.
    """
    chains = discover(sequence, config)
    if not chains:
        return None
    probs = name_probabilities(sequence)
    return max(
        chains,
        key=lambda c: (chain_statistic(sequence, c, measure, probs), c.score),
    )


def _mark(names: Sequence[str], chain: Optional[Chain]) -> List[str]:
    """Setzt die Klammern der gefundenen Kette fett."""
    cells = list(names)
    if chain is None:
        return cells
    for placement in chain.placements:
        for position in (placement.block.anchor_pos, placement.block.echo_pos):
            cells[position] = f"**{cells[position]}**"
    return cells


def _coverage_cells(chain: Optional[Chain], total: int) -> List[str]:
    """Abdeckung und Zahl der Ausbrecher -- auch fuer Nicht-Treffer aussagekraeftig."""
    if chain is None:
        return ["0%", str(total)]
    return [f"{chain.coverage(total):.0%}", str(len(chain.outsiders(total)))]


def _describe(chain: Optional[Chain]) -> Tuple[str, str, str, str]:
    if chain is None:
        return ("", "", "", "")
    if chain.kind is PatternKind.BOOKEND:
        names = " / ".join(chain.bookend_names)
    else:
        names = chain.describe_motif()
    return (
        str(len(chain.placements)),
        str(chain.x0) if chain.d == 0 else f"{chain.x0}+j·{chain.d}",
        ", ".join(str(gap) for gap in interruptions(chain)),
        names,
    )


def build_markdown(
    sequence: Names,
    config: SearchConfig,
    trials: int,
    seed: Optional[int],
    source: str,
    stats_trials: int = 0,
    measure: Measure = Measure.BITS,
) -> str:
    probs = name_probabilities(sequence)
    total = len(sequence)
    reference = best_chain(sequence, config, measure)
    observed = chain_statistic(sequence, reference, measure, probs)

    lines: List[str] = [
        f"# Nullmodell-Umsortierungen: {source}",
        "",
        f"Die ersten **{trials}** Permutationen des Signifikanztests, "
        f"Startwert `{seed}`.",
        "",
        "## Was hier geprüft wird",
        "",
        f"- Liste: {len(sequence)} Namen aus `{source}`",
        f"- Familien: {', '.join(k.value for k in config.families)}",
        f"- Schrittweiten `d`: {', '.join(str(d) for d in config.allowed_d)}",
        f"- höchstens {config.max_interruption} Namen zwischen zwei Blöcken"
        if config.max_interruption is not None
        else "- Abstand zwischen Blöcken unbegrenzt",
        f"- mindestens {config.min_blocks} Blöcke, "
        f"Abweichungsbudget {config.max_deviations}",
        "",
        "Das Nullmodell **permutiert nur**: jede Zeile enthält exakt dieselben "
        "Namen wie die Ausgangsliste, in anderer Reihenfolge. Geprüft wird also "
        "allein, ob die *Anordnung* bemerkenswert ist.",
        "",
    ]

    if reference is not None:
        blocks, rule, gaps, names = _describe(reference)
        lines += [
            "## Der Befund, gegen den verglichen wird",
            "",
            f"**{blocks} Blöcke**, x = {rule} (konstant), Klammern: {names}, "
            f"Unterbrechungen: {gaps}.",
            "",
            f"Die Kette erfasst **{reference.covered} von {total} Namen** "
            f"({reference.coverage(total):.0%}); "
            f"{len(reference.outsiders(total))} brechen aus der Ordnung aus, "
            f"die längste unstrukturierte Strecke ist {reference.max_outsider_run(total)} "
            f"Namen lang. Seltenheit: {chain_bits(probs, reference):.1f} Bit.",
            "",
            "Zwei Markierungen, weil „gleiche Regelmässigkeit\" zweierlei "
            "heissen kann:",
            "",
            (
                f"- **✓** — zählt für den p-Wert: die gleiche Suche erreicht in "
                f"der Umsortierung mindestens {observed:.0%} Abdeckung."
                if measure is Measure.COVERAGE
                else
                f"- **✓** — zählt für den p-Wert: die gleiche Suche findet "
                f"mindestens {observed:.1f} Bit. Da alle Permutationen dieselben "
                "Namenshäufigkeiten haben, ist eine Klammer überall gleich viel "
                f"wert; der Vergleich läuft damit auf „mindestens {blocks} Blöcke "
                "ohne Abweichung\" hinaus — **die Blocklänge darf eine andere sein**."
            ),
            f"- **★** — strenger: die Kette hat zusätzlich dieselbe Blocklänge "
            f"x = {reference.x0} wie die Ausgangsliste.",
            "",
            "Der Unterschied ist erheblich, siehe die Auswertung am Ende.",
            "",
        ]

    width = len(sequence)
    header = ["#", "✓", "★", "Abd.", "aussen", "Blöcke", "x", "Zwischen", "Klammern"] + [
        str(i) for i in range(width)
    ]
    lines += [
        "## Die Umsortierungen",
        "",
        "Fett gesetzt sind die Namen, die einen Block öffnen oder schliessen.",
        "",
        "| " + " | ".join(header) + " |",
        "|" + "---|" * len(header),
    ]

    reference_row = (
        ["**Original**", "—", "—"]
        + _coverage_cells(reference, total)
        + list(_describe(reference))
        + _mark(sequence, reference)
    )
    lines.append("| " + " | ".join(reference_row) + " |")

    shown: List[Tuple[int, Chain, bool]] = []
    total_hits = 0
    strict_hits = 0
    by_x: Counter = Counter()
    max_cov = 0.0

    for index, shuffled in enumerate(
        permutations(sequence, max(trials, stats_trials), seed), start=1
    ):
        chain = best_chain(shuffled, config, measure)
        value = chain_statistic(shuffled, chain, measure, probs)
        is_hit = observed > 0 and value >= observed
        same_length = bool(
            is_hit
            and chain is not None
            and reference is not None
            and chain.x0 == reference.x0
            and chain.d == reference.d
        )
        if chain is not None:
            max_cov = max(max_cov, chain.coverage(total))
        if is_hit and chain is not None:
            total_hits += 1
            by_x[chain.x0] += 1
            if same_length:
                strict_hits += 1
        if index <= trials:
            if is_hit and chain is not None:
                shown.append((index, chain, same_length))
            row = (
                [str(index), "✓" if is_hit else "", "★" if same_length else ""]
                + _coverage_cells(chain, total)
                + list(_describe(chain if is_hit else None))
                + _mark(shuffled, chain if is_hit else None)
            )
            lines.append("| " + " | ".join(row) + " |")

    runs = max(trials, stats_trials)
    # Plus-Eins-Korrektur wie im Nullmodell: p wird bei endlich vielen
    # Durchlaeufen nie exakt 0.
    p_any = (1 + total_hits) / (1 + runs)
    p_strict = (1 + strict_hits) / (1 + runs)
    lines += [
        "",
        "## Auswertung",
        "",
        f"Über **{runs}** Permutationen"
        + (f" (die Tabelle oben zeigt die ersten {trials})." if runs > trials else "."),
        "",
        "| Kriterium | Treffer | Anteil | p |",
        "|---|---|---|---|",
        f"| ✓ irgendeine Kette gleicher Güte | {total_hits} | "
        f"{total_hits / runs:.1%} | {p_any:.3f} |",
        f"| ★ zusätzlich gleiche Blocklänge | {strict_hits} | "
        f"{strict_hits / runs:.1%} | {p_strict:.4f} |",
        "",
    ]

    if total_hits and reference is not None:
        spread = ", ".join(f"x={x}: {count}" for x, count in sorted(by_x.items()))
        choices = len(by_x)
        corrected = min(1.0, choices * p_strict)
        if measure is Measure.COVERAGE:
            explanation = [
                "### Was die Abdeckung misst",
                "",
                f"Die Blocklängen der Zufallstreffer: {spread}.",
                "",
                "Unter dieser Messgrösse zählt nicht mehr, *wie viele* Blöcke "
                "eine Kette hat, sondern wie viel der Liste sie erklärt. Damit "
                "fallen die kurzen Ketten heraus, die den Bit-Wert dominiert "
                "haben: drei Blöcke zu je drei Namen erfassen neun von "
                f"{total} Positionen, das reicht nicht mehr.",
                "",
                "Deshalb ist die ★-Zeile hier fast deckungsgleich mit der "
                f"✓-Zeile — wer in einer Liste von {total} Namen mit drei "
                "Blöcken hohe Abdeckung erreichen will, braucht zwangsläufig "
                "Blöcke dieser Länge. Die Blocklänge ist also kein freier "
                "Parameter mehr, über den man sich hinterher etwas aussuchen "
                "könnte, und eine Bonferroni-Korrektur erübrigt sich.",
                "",
                "### Und was heisst das nun?",
                "",
                f"In **{total_hits} von {runs}** Umsortierungen erreicht der "
                f"Zufall eine mindestens so hohe Abdeckung wie die "
                f"Geschichtsschreibung — **p = {p_any:.3f}**.",
                "",
                f"Die Ausgangsliste ist damit geordneter als {1 - p_any:.1%} "
                "aller Umsortierungen. Sie ist aber **nicht** die geordnetste "
                f"mögliche: der beste Zufallstreffer erreicht "
                f"{max_cov:.0%} Abdeckung gegenüber "
                f"{reference.coverage(total):.0%} der Königsliste.",
                "",
            ]
        else:
            explanation = [
                "### Woran der Unterschied liegt",
                "",
                f"Die Blocklängen der Zufallstreffer verteilen sich so: {spread}.",
                "",
                "Kurze Blöcke sind billig zu haben — bei `x=0` genügen zwei "
                "gleiche Namen nebeneinander, und davon gibt es in einer Liste "
                "mit häufigen Namen viele. Die Suche akzeptiert *jede* "
                "konstante Blocklänge, deshalb wird der p-Wert von diesen "
                "kurzen Ketten getragen, nicht von Ketten, die dem Befund "
                "wirklich ähneln. Wer danach fragt, wie viel der Liste das "
                "Muster *erklärt*, nimmt `--measure coverage`.",
                "",
                "### Und was heisst das nun?",
                "",
                "Beide Zahlen sind richtig, sie beantworten verschiedene Fragen:",
                "",
                f"- „Wie oft findet der Zufall *irgendeine* Regelmässigkeit "
                f"dieser Art?\" → p = {p_any:.3f}.",
                f"- „Wie oft findet er eine mit genau x = {reference.x0}?\" → "
                f"p = {p_strict:.4f}.",
                "",
                "Die zweite Zahl darf man nur verwenden, wenn die Blocklänge "
                "**vorab** feststand. Sucht man sie sich nach Sichtung der "
                f"Daten aus, hat man unter {choices} beobachteten Blocklängen "
                "die günstigste gewählt, und das muss korrigiert werden: "
                f"{choices} · {p_strict:.4f} = **{corrected:.3f}** (Bonferroni).",
                "",
            ]
        lines += explanation + [
            f"### Die Treffer unter den ersten {trials}",
            "",
            "| # | | Blöcke | x | Klammern | Positionen | Zwischen |",
            "|---|---|---|---|---|---|---|",
        ]
        for index, chain, same_length in shown:
            blocks, rule, gaps, names = _describe(chain)
            spans = " ".join(
                f"{p.block.anchor_pos}–{p.block.echo_pos}" for p in chain.placements
            )
            mark = "★" if same_length else ""
            lines.append(
                f"| {index} | {mark} | {blocks} | {rule} | {names} | {spans} | {gaps} |"
            )
        lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="name-patterns-inspect",
        description="Schreibt die Umsortierungen des Nullmodells als Markdown-Tabelle.",
    )
    parser.add_argument("--data", required=True, help="Namensliste, ein Eintrag pro Zeile")
    parser.add_argument("-o", "--out", required=True, help="Zieldatei (.md)")
    parser.add_argument(
        "--trials", type=int, default=100, help="Wie viele Umsortierungen die Tabelle zeigt"
    )
    parser.add_argument(
        "--stats-trials",
        type=int,
        default=0,
        help="Permutationen fuer die Auswertung (Default: wie --trials)",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--d", default="0", help="Erlaubte Schrittweiten (Default: 0)")
    parser.add_argument("--min-blocks", type=int, default=3)
    parser.add_argument("--max-gap", type=int, default=12)
    parser.add_argument("--max-interruption", type=int, default=None)
    parser.add_argument("-t", "--max-deviations", type=int, default=0)
    parser.add_argument(
        "--family", choices=("fixed", "bookend", "both"), default="bookend"
    )
    parser.add_argument(
        "--measure",
        choices=("coverage", "bits"),
        default="coverage",
        help="Woran Treffer gemessen werden (Default: coverage)",
    )
    parser.add_argument("--raw-names", action="store_true")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    raw = load_names(args.data, normalize_names=False)
    sequence = raw if args.raw_names else normalize(raw)[0]

    families = {
        "fixed": (PatternKind.FIXED,),
        "bookend": (PatternKind.BOOKEND,),
        "both": (PatternKind.FIXED, PatternKind.BOOKEND),
    }[args.family]

    config = SearchConfig(
        max_deviations=args.max_deviations,
        min_blocks=args.min_blocks,
        max_gap=args.max_gap,
        allowed_d=tuple(int(p) for p in args.d.split(",") if p.strip()),
        max_interruption=args.max_interruption,
        families=families,
    )

    text = build_markdown(
        sequence,
        config,
        args.trials,
        args.seed,
        Path(args.data).name,
        stats_trials=args.stats_trials,
        measure=Measure(args.measure),
    )
    Path(args.out).write_text(text, encoding="utf-8")
    print(f"{args.trials} Umsortierungen geschrieben nach {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
