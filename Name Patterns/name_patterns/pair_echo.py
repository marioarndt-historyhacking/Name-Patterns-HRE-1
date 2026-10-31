"""Globale Suche fuer ``X, Y, [n Namen], Y`` mit wachsendem ``n``.

Die Namen X und Y werden fuer jeden Block neu gebunden. Zwischen zwei Bloecken
darf in der Referenzkonfiguration insgesamt hoechstens eine Listenposition
ausserhalb der Bloecke liegen. Die Discovery waehlt Anfang, X/Y-Namen und den
Startwert von n frei; jede Permutation wiederholt dieselbe Suche.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from .succession import wilson_interval
from .timeline import TimelineEntry, load_timeline


EMPEROR_PREFIX: Tuple[str, ...] = ("Karl", "Ludwig", "Lothar", "Ludwig")
EMPEROR_SUFFIX_IDS: Tuple[str, ...] = (
    "maximilian-i",
    "karl-v",
    "ferdinand-i",
    "maximilian-ii",
    "rudolf-ii",
    "matthias-habsburg",
    "ferdinand-ii",
    "ferdinand-iii",
    "leopold-i",
    "joseph-i",
    "karl-vi",
)
KING_SUFFIX_WITH_FERDINAND_IV_IDS: Tuple[str, ...] = (
    "maximilian-i", "karl-v", "ferdinand-i", "maximilian-ii", "rudolf-ii",
    "matthias-habsburg", "ferdinand-ii", "ferdinand-iii", "ferdinand-iv",
    "leopold-i", "joseph-i", "karl-vi",
)


@dataclass(frozen=True)
class PairEchoBlock:
    start: int
    end: int
    n: int
    x_name: str
    y_name: str

    @property
    def covered(self) -> int:
        return self.n + 3


@dataclass(frozen=True)
class PairEchoFinding:
    blocks: Tuple[PairEchoBlock, ...]
    outsiders: int
    covered: int
    span: int
    score: float
    n_skips: int = 0

    @property
    def key(self) -> Tuple[int, float]:
        return len(self.blocks), self.score


@dataclass(frozen=True)
class PairEchoResult:
    label: str
    sequence: Tuple[str, ...]
    finding: PairEchoFinding
    trials: int
    hits: int
    p_value: float
    seed: int


def build_variants(
    timeline: Sequence[TimelineEntry],
) -> Tuple[Tuple[str, ...], Tuple[str, ...]]:
    """Erzeugt die festgelegte Siebener- und Achterliste.

    Der Praefix ist die Kaiserfolge Karl der Grosse bis Ludwig II. Danach folgt
    die ostfraenkisch/roemisch-deutsche Liste ab den Erhebungen 876. Karlmann
    wird regelgebunden als ``Karl`` analysiert. Die Achtervariante haengt die
    Kaiserfolge Maximilian I. bis Karl VI. an; Ferdinand IV. ist nicht Teil
    dieser Kaiserfolge.
    """
    middle = tuple(
        "Karl" if entry.analysis_name == "Karlmann" else entry.analysis_name
        for entry in timeline
        if 876 <= entry.elevation_year <= 1440
    )
    seven = EMPEROR_PREFIX + middle
    names_by_id = {entry.person_id: entry.analysis_name for entry in timeline}
    try:
        suffix = tuple(names_by_id[person_id] for person_id in EMPEROR_SUFFIX_IDS)
    except KeyError as exc:
        raise ValueError(f"Kaiser fehlt in Timeline: {exc.args[0]}") from exc
    return seven, seven + suffix


def build_variant_with_ferdinand_iv(
    timeline: Sequence[TimelineEntry],
) -> Tuple[str, ...]:
    """Fortgesetzte Koenigsliste bis Karl VI., Ferdinand IV. eingeschlossen."""
    seven, _ = build_variants(timeline)
    names_by_id = {entry.person_id: entry.analysis_name for entry in timeline}
    try:
        suffix = tuple(
            names_by_id[person_id] for person_id in KING_SUFFIX_WITH_FERDINAND_IV_IDS
        )
    except KeyError as exc:
        raise ValueError(f"Koenig fehlt in Timeline: {exc.args[0]}") from exc
    return seven + suffix


def candidate_blocks(sequence: Sequence[str]) -> Dict[int, List[PairEchoBlock]]:
    """Alle Bloecke mit X != Y und gleicher zweiter/letzter Position."""
    by_n: Dict[int, List[PairEchoBlock]] = {}
    total = len(sequence)
    for start in range(total - 3):
        x_name, y_name = sequence[start], sequence[start + 1]
        if x_name == y_name:
            continue
        for n in range(1, total):
            end = start + n + 2
            if end >= total:
                break
            if sequence[end] == y_name:
                by_n.setdefault(n, []).append(
                    PairEchoBlock(start, end, n, x_name, y_name)
                )
    return by_n


def best_pair_echo(
    sequence: Sequence[str], *, max_total_outsiders: int = 1, max_n_skips: int = 0
) -> Optional[PairEchoFinding]:
    """Beste Kette; zuerst mehr Bloecke, dann dichtere/groessere Abdeckung."""
    by_n = candidate_blocks(sequence)
    # Pro Block und Outsiderbudget: beste (laengste) Kette, die dort endet.
    states: Dict[
        PairEchoBlock, Dict[Tuple[int, int], Tuple[PairEchoBlock, ...]]
    ] = {}
    best: Optional[PairEchoFinding] = None
    for n in sorted(by_n):
        for block in by_n[n]:
            block_states: Dict[
                Tuple[int, int], Tuple[PairEchoBlock, ...]
            ] = {(0, 0): (block,)}
            for delta in range(1, max_n_skips + 2):
                for previous in by_n.get(n - delta, ()):
                    if previous.end >= block.start:
                        continue
                    gap = block.start - previous.end - 1
                    for (used, skipped), chain in states.get(previous, {}).items():
                        new_used = used + gap
                        new_skipped = skipped + delta - 1
                        if (
                            new_used > max_total_outsiders
                            or new_skipped > max_n_skips
                        ):
                            continue
                        candidate = chain + (block,)
                        state_key = (new_used, new_skipped)
                        current = block_states.get(state_key)
                        if current is None or len(candidate) > len(current):
                            block_states[state_key] = candidate
            states[block] = block_states
            for (used, skipped), chain in block_states.items():
                covered = sum(item.covered for item in chain)
                span = chain[-1].end - chain[0].start + 1
                score = covered * covered / span
                finding = PairEchoFinding(chain, used, covered, span, score, skipped)
                if best is None or finding.key > best.key:
                    best = finding
    return best


def max_chain_length(
    sequence: Sequence[str], *, max_total_outsiders: int = 1
) -> int:
    """Schnelle Nullmodell-Kennzahl ohne Rekonstruktion der gesamten Kette."""
    by_n = candidate_blocks(sequence)
    states: Dict[PairEchoBlock, Tuple[int, int]] = {}
    maximum = 0
    for n in sorted(by_n):
        for block in by_n[n]:
            best_by_budget = [1] * (max_total_outsiders + 1)
            for previous in by_n.get(n - 1, ()):
                if previous.end >= block.start:
                    continue
                gap = block.start - previous.end - 1
                previous_state = states.get(previous)
                if previous_state is None:
                    continue
                prev_zero, prev_one = previous_state
                if gap == 0:
                    best_by_budget[0] = max(best_by_budget[0], prev_zero + 1)
                    if max_total_outsiders >= 1:
                        best_by_budget[1] = max(best_by_budget[1], prev_one + 1)
                elif gap == 1 and max_total_outsiders >= 1:
                    best_by_budget[1] = max(best_by_budget[1], prev_zero + 1)
            zero = best_by_budget[0]
            one = best_by_budget[1] if max_total_outsiders >= 1 else zero
            states[block] = (zero, one)
            maximum = max(maximum, zero, one)
    return maximum


def has_chain_length(
    sequence: Sequence[str],
    target: int,
    *,
    max_total_outsiders: int = 1,
    max_n_skips: int = 0,
) -> bool:
    """Prueft eine Ziel-Laenge in O(Listenlaenge × Ziel-Laenge).

    Bei einem festen ``n`` kann der naechste Block wegen des gesamten
    Outsiderbudgets nur direkt oder eine Position spaeter beginnen. Fuer lange
    Monte-Carlo-Laeufe vermeidet das die vollstaendige Kandidatenrangliste.
    """
    total = len(sequence)
    for start_n in range(1, total):
        required = target * (start_n + 3) + target * (target - 1) // 2
        if required > total:
            break
        states = set()
        end_offset = start_n + 2
        for start in range(total - end_offset):
            end = start + end_offset
            if sequence[start] != sequence[start + 1] and sequence[start + 1] == sequence[end]:
                states.add((end, 0, 0, start_n))
        if not states:
            continue
        for _step in range(1, target):
            next_states = set()
            for previous_end, used, skipped, previous_n in states:
                for gap in range(max_total_outsiders - used + 1):
                    for extra_skip in range(max_n_skips - skipped + 1):
                        n = previous_n + 1 + extra_skip
                        start = previous_end + 1 + gap
                        end = start + n + 2
                        if end >= total:
                            continue
                        if (
                            sequence[start] != sequence[start + 1]
                            and sequence[start + 1] == sequence[end]
                        ):
                            next_states.add(
                                (end, used + gap, skipped + extra_skip, n)
                            )
            states = next_states
            if not states:
                break
        if states:
            return True
    return False


def assess_variant(
    sequence: Sequence[str],
    label: str,
    *,
    trials: int = 1_000_000,
    seed: int = 42,
    max_n_skips: int = 0,
) -> PairEchoResult:
    finding = best_pair_echo(sequence, max_n_skips=max_n_skips)
    if finding is None:
        raise ValueError("Keine PAIR_ECHO-Kette gefunden")
    threshold = len(finding.blocks)
    shuffled = list(sequence)
    rng = random.Random(seed)
    hits = 0
    for _ in range(trials):
        rng.shuffle(shuffled)
        if has_chain_length(shuffled, threshold, max_n_skips=max_n_skips):
            hits += 1
    return PairEchoResult(
        label=label,
        sequence=tuple(sequence),
        finding=finding,
        trials=trials,
        hits=hits,
        p_value=(hits + 1) / (trials + 1),
        seed=seed,
    )


def format_result(result: PairEchoResult) -> str:
    finding = result.finding
    low, high = wilson_interval(result.hits, result.trials)
    lines = [
        f"PAIR_ECHO-Analyse: {result.label}",
        "",
        "Regel:        X, Y, [n Namen], Y; n waechst grundsaetzlich um 1",
        "Discovery:    X/Y, Startposition und Start-n frei; Karlmann -> Karl",
        "Toleranz:     hoechstens 1 Position insgesamt ausserhalb der Bloecke",
        f"n-Spruenge:   {finding.n_skips} uebersprungene Sollwerte",
        f"Listenlaenge: {len(result.sequence)}",
        f"Bloecke:      {len(finding.blocks)}",
        f"Abgedeckt:    {finding.covered}/{finding.span} im Musterintervall "
        f"({finding.covered / finding.span:.2%})",
        f"Scan-Score:   {finding.score:.6f}",
        "",
        "Bloecke:",
    ]
    for block in finding.blocks:
        lines.append(
            f"  n={block.n}: Index {block.start}..{block.end}; "
            f"X={block.x_name}, Y={block.y_name}"
        )
    lines += [
        "",
        f"Permutationen: {result.trials}",
        f"Zufallstreffer: {result.hits}",
        f"Globaler p-Wert mit Plus-eins-Korrektur: {result.p_value:.8f}",
        f"Wilson-Intervall der Trefferquote (95 %): {low:.8f}–{high:.8f}",
        "Signifikant:   " + ("ja (p < 0.05)" if result.p_value < 0.05 else "nein"),
        "",
        "Der p-Wert vergleicht die maximale Zahl aufeinanderfolgender n-Bloecke.",
        "Jede Permutation darf ihre eigene beste PAIR_ECHO-Kette waehlen.",
    ]
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeline", default="HRR_Kings_843_1806.csv")
    parser.add_argument(
        "--variant",
        choices=("7", "8", "8-kings", "both", "all"),
        default="both",
    )
    parser.add_argument("--trials", type=int, default=1_000_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    timeline = load_timeline(args.timeline)
    seven, eight = build_variants(timeline)
    eight_kings = build_variant_with_ferdinand_iv(timeline)
    requested = []
    if args.variant in ("7", "both", "all"):
        requested.append((seven, "7er-Folge bis Friedrich III.", 0))
    if args.variant in ("8", "both", "all"):
        requested.append((eight, "8er-Folge bis Karl VI. (Kaiser)", 0))
    if args.variant in ("8-kings", "all"):
        requested.append((eight_kings, "8er-Koenigsfolge mit Ferdinand IV.", 1))
    reports = [
        format_result(
            assess_variant(
                seq,
                label,
                trials=args.trials,
                seed=args.seed,
                max_n_skips=skips,
            )
        )
        for seq, label, skips in requested
    ]
    report = "\n\n" + ("\n\n" + "=" * 78 + "\n\n").join(reports)
    print(report.lstrip())
    if args.output:
        Path(args.output).write_text(report.lstrip() + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
