"""Globale Suche nach dem staerksten Musterabschnitt einer Gesamtliste.

Der Zeitraum wird nicht vorgegeben.  Jede gefundene Kette definiert durch ihren
ersten und letzten Block selbst ein Intervall.  In jeder Permutation wird die
gesamte Suche wiederholt; dadurch ist die freie Wahl von Anfang und Ende im
p-Wert enthalten.
"""

from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple

from .discovery import Motif, discover
from .model import Chain, Names, PatternKind, SearchConfig
from .search import find_bookend_chains, find_chains


Progress = Callable[[int, int], None]


@dataclass(frozen=True)
class TimelineEntry:
    position: int
    analysis_name: str
    canonical_name: str
    elevation_year: int
    role: str = ""
    person_id: str = ""


@dataclass(frozen=True)
class IntervalFinding:
    chain: Chain
    span_length: int
    covered: int
    local_coverage: float
    score: float
    start_year: Optional[int] = None
    end_year: Optional[int] = None


@dataclass(frozen=True)
class IntervalNullModel:
    trials: int
    scores: Tuple[float, ...]
    discovery: bool

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
        return ordered[min(len(ordered) - 1, int(0.95 * len(ordered)))]

    def p_value(self, observed: float) -> float:
        hits = sum(1 for score in self.scores if score >= observed)
        return (1 + hits) / (1 + self.trials)


def load_timeline(path: str | Path) -> List[TimelineEntry]:
    """Liest die vom Herrscherimport erzeugte CSV-Datei."""
    entries: List[TimelineEntry] = []
    with Path(path).open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            entries.append(
                TimelineEntry(
                    position=int(row["position"]),
                    analysis_name=row["analysis_name"],
                    canonical_name=row["canonical_name"],
                    elevation_year=int(row["elevation_year"]),
                    role=row.get("role", ""),
                    person_id=row.get("person_id", ""),
                )
            )
    positions = [entry.position for entry in entries]
    if positions != list(range(1, len(entries) + 1)):
        raise ValueError("Timeline-CSV muss lueckenlos nach position sortiert sein")
    return entries


def interval_score(chain: Chain) -> Tuple[int, float, float]:
    """Multiskalen-Score eines automatisch gewaehlten Abschnitts.

    ``covered * local_coverage`` belohnt sowohl substantielle Laenge als auch
    Dichte.  Ein kurzer perfekter Dreierblock kann dadurch keinen fast
    lueckenlosen Abschnitt mit vielen abgedeckten Personen verdraengen.  Der
    letzte Faktor uebertraegt die vorhandene Abweichungsstrafe proportional.
    """
    span_length = chain.span[1] - chain.span[0] + 1
    local_coverage = chain.covered / span_length if span_length else 0.0
    quality = chain.score / len(chain.placements) if chain.placements else 0.0
    score = chain.covered * local_coverage * max(0.0, quality)
    return span_length, local_coverage, score


def _candidate_chains(
    sequence: Names,
    config: SearchConfig,
    motif: Optional[Motif],
) -> List[Chain]:
    if motif is None:
        return discover(sequence, config)
    chains: List[Chain] = []
    if config.searches(PatternKind.FIXED):
        chains.extend(find_chains(sequence, motif.anchor, motif.echo, config))
    if config.searches(PatternKind.BOOKEND):
        chains.extend(find_bookend_chains(sequence, config))
    return chains


def best_interval(
    sequence: Names,
    config: SearchConfig,
    *,
    motif: Optional[Motif],
    timeline: Optional[Sequence[TimelineEntry]] = None,
) -> Optional[IntervalFinding]:
    """Waehlt den staerksten von der Kettensuche selbst definierten Abschnitt."""
    candidates = _candidate_chains(sequence, config, motif)
    if not candidates:
        return None

    def key(chain: Chain):
        span, local, score = interval_score(chain)
        return (score, chain.covered, local, chain.score, -span, -chain.span[0])

    chain = max(candidates, key=key)
    span_length, local_coverage, score = interval_score(chain)
    start_year = end_year = None
    if timeline is not None:
        if len(timeline) != len(sequence):
            raise ValueError("Timeline und Namensliste haben unterschiedliche Laengen")
        start_year = timeline[chain.span[0]].elevation_year
        end_year = timeline[chain.span[1]].elevation_year
    return IntervalFinding(
        chain=chain,
        span_length=span_length,
        covered=chain.covered,
        local_coverage=local_coverage,
        score=score,
        start_year=start_year,
        end_year=end_year,
    )


def assess_interval(
    sequence: Names,
    config: SearchConfig,
    *,
    motif: Optional[Motif],
    timeline: Optional[Sequence[TimelineEntry]] = None,
    trials: int = 0,
    seed: Optional[int] = None,
    progress: Optional[Progress] = None,
) -> Tuple[Optional[IntervalFinding], Optional[IntervalNullModel], Optional[float]]:
    """Befund und global korrigierten p-Wert der freien Intervallsuche."""
    observed = best_interval(sequence, config, motif=motif, timeline=timeline)
    if observed is None or trials <= 0:
        return observed, None, None

    rng = random.Random(seed)
    shuffled = list(sequence)
    scores: List[float] = []
    for done in range(trials):
        rng.shuffle(shuffled)
        found = best_interval(shuffled, config, motif=motif)
        scores.append(found.score if found is not None else 0.0)
        if progress is not None:
            progress(done + 1, trials)
    null = IntervalNullModel(
        trials=trials,
        scores=tuple(scores),
        discovery=motif is None,
    )
    return observed, null, null.p_value(observed.score)


def format_interval_report(
    sequence: Names,
    finding: Optional[IntervalFinding],
    null: Optional[IntervalNullModel],
    p_value: Optional[float],
) -> str:
    if finding is None:
        return "Kein Musterabschnitt gefunden, der die Vorgaben erfuellt."
    chain = finding.chain
    start = f"{finding.start_year}" if finding.start_year is not None else str(chain.span[0])
    end = f"{finding.end_year}" if finding.end_year is not None else str(chain.span[1])
    lines = [
        "Global beste Intervallkette",
        "",
        f"Muster:       {chain.describe_motif()}",
        f"Regel:        {chain.rule()}",
        f"Intervall:    Index {chain.span[0]}..{chain.span[1]} ({start}–{end})",
        f"Spannweite:   {finding.span_length} Listenpositionen",
        f"Abgedeckt:    {finding.covered}/{finding.span_length} im Intervall "
        f"({finding.local_coverage:.0%}); {finding.covered}/{len(sequence)} der Gesamtliste",
        f"Bloecke:      {len(chain.placements)}; Abweichungen: {len(chain.deviations)}",
        f"Scan-Score:   {finding.score:.4f}",
    ]
    if p_value is not None:
        lines += [
            f"Globaler p-Wert: {p_value:.4f}",
            "Signifikant:   " + ("ja (p < 0.05)" if p_value < 0.05 else "nein (p >= 0.05)"),
        ]
    lines += ["", "Bloecke:"]
    for placement in chain.placements:
        block = placement.block
        lines.append(
            f"  j={placement.chain_index}: Index {block.anchor_pos}..{block.echo_pos}, "
            f"x={block.x}"
        )
    if null is not None:
        scope = "volle Motiv- und Intervallsuche" if null.discovery else "festes Motiv, freie Intervallsuche"
        lines += [
            "",
            f"Nullmodell:   {null.trials} Permutationen; {scope}",
            f"Zufallsscore: Mittel {null.mean:.4f}, 95%-Quantil {null.p95:.4f}, "
            f"Maximum {null.best:.4f}",
            "Der p-Wert wiederholt in jeder Permutation die Wahl von Anfang, Ende, "
            "x0 und Schrittweite.",
        ]
    return "\n".join(lines)
