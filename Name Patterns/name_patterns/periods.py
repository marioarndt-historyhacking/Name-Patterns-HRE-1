"""Vergleich historisch vorab festgelegter Zeitraeume.

Jeder Zeitraum erhaelt zunaechst einen eigenen globalen Discovery-Test. Fuer
den direkten Vergleich werden die Namen beider Perioden gepoolt, zufaellig auf
Perioden gleicher Groesse verteilt und in beiden Teilen erneut vollstaendig
durchsucht. Damit gehoeren Motiv-, Familien- und Intervallwahl zum Nullmodell.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence, Tuple

from .model import Names, PatternKind, SearchConfig
from .timeline import (
    IntervalFinding,
    IntervalNullModel,
    TimelineEntry,
    assess_interval,
    best_interval,
    format_interval_report,
)


Progress = Callable[[int, int], None]


@dataclass(frozen=True)
class PeriodSpec:
    start_year: int
    end_year: int

    def __post_init__(self) -> None:
        if self.start_year > self.end_year:
            raise ValueError("Periodenbeginn darf nicht nach dem Periodenende liegen")

    @property
    def label(self) -> str:
        return f"{self.start_year}–{self.end_year}"


@dataclass(frozen=True)
class PeriodAssessment:
    spec: PeriodSpec
    sequence: Tuple[str, ...]
    timeline: Tuple[TimelineEntry, ...]
    finding: Optional[IntervalFinding]
    null: Optional[IntervalNullModel]
    p_value: Optional[float]

    @property
    def strength(self) -> float:
        """Laengenstandardisierter Scan-Score zwischen 0 und ungefaehr 1."""
        if self.finding is None or not self.sequence:
            return 0.0
        return self.finding.score / len(self.sequence)


@dataclass(frozen=True)
class PeriodContrast:
    first: PeriodAssessment
    second: PeriodAssessment
    trials: int
    null_differences: Tuple[float, ...]
    observed_difference: float
    p_value: Optional[float]


def parse_period_pair(value: str) -> Tuple[PeriodSpec, PeriodSpec]:
    """Liest ``START:ENDE,START:ENDE``."""
    try:
        raw_periods = [part.strip() for part in value.split(",")]
        if len(raw_periods) != 2:
            raise ValueError
        parsed = []
        for raw in raw_periods:
            start, end = (int(part.strip()) for part in raw.split(":"))
            parsed.append(PeriodSpec(start, end))
        return parsed[0], parsed[1]
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Zeitraeume muessen als START:ENDE,START:ENDE angegeben werden"
        ) from exc


def select_period(
    timeline: Sequence[TimelineEntry], spec: PeriodSpec
) -> Tuple[Tuple[str, ...], Tuple[TimelineEntry, ...]]:
    """Waehlt Eintraege nach dem Jahr ihrer ersten Erhebung, Grenzen inklusive."""
    selected = tuple(
        entry for entry in timeline
        if spec.start_year <= entry.elevation_year <= spec.end_year
    )
    return tuple(entry.analysis_name for entry in selected), selected


def _strength(sequence: Names, config: SearchConfig) -> float:
    finding = best_interval(sequence, config, motif=None)
    return finding.score / len(sequence) if finding is not None and sequence else 0.0


def assess_period_pair(
    timeline: Sequence[TimelineEntry],
    config: SearchConfig,
    first_spec: PeriodSpec,
    second_spec: PeriodSpec,
    *,
    trials: int = 0,
    seed: Optional[int] = None,
    progress: Optional[Progress] = None,
) -> PeriodContrast:
    """Berechnet zwei Einzeltests und den gerichteten Vergleich ``erste > zweite``.

    Die Einzeltests permutieren innerhalb einer Periode. Der Kontrast poolt
    beide Perioden und verteilt die Namen zufaellig neu auf Teile unveraenderter
    Groesse. Der Kontrast umfasst daher Unterschiede der Namenshaeufigkeiten
    ebenso wie Unterschiede ihrer Reihenfolge.
    """
    if set(config.families) != {PatternKind.FIXED, PatternKind.BOOKEND}:
        raise ValueError("Der Periodenvergleich muss FIXED und BOOKEND durchsuchen")

    first_sequence, first_timeline = select_period(timeline, first_spec)
    second_sequence, second_timeline = select_period(timeline, second_spec)
    if not first_sequence or not second_sequence:
        raise ValueError("Beide Zeitraeume muessen mindestens einen Eintrag enthalten")

    first_found, first_null, first_p = assess_interval(
        first_sequence,
        config,
        motif=None,
        timeline=first_timeline,
        trials=trials,
        seed=seed,
    )
    second_seed = None if seed is None else seed + 1
    second_found, second_null, second_p = assess_interval(
        second_sequence,
        config,
        motif=None,
        timeline=second_timeline,
        trials=trials,
        seed=second_seed,
    )
    first = PeriodAssessment(
        first_spec, first_sequence, first_timeline, first_found, first_null, first_p
    )
    second = PeriodAssessment(
        second_spec,
        second_sequence,
        second_timeline,
        second_found,
        second_null,
        second_p,
    )
    observed = first.strength - second.strength

    differences: List[float] = []
    if trials > 0:
        contrast_seed = None if seed is None else seed + 2
        rng = random.Random(contrast_seed)
        pooled = list(first_sequence + second_sequence)
        first_size = len(first_sequence)
        for done in range(trials):
            rng.shuffle(pooled)
            random_first = pooled[:first_size]
            random_second = pooled[first_size:]
            differences.append(
                _strength(random_first, config) - _strength(random_second, config)
            )
            if progress is not None:
                progress(done + 1, trials)
        hits = sum(value >= observed for value in differences)
        p_value: Optional[float] = (hits + 1) / (trials + 1)
    else:
        p_value = None

    return PeriodContrast(
        first=first,
        second=second,
        trials=trials,
        null_differences=tuple(differences),
        observed_difference=observed,
        p_value=p_value,
    )


def format_period_contrast(contrast: PeriodContrast) -> str:
    """Menschenlesbarer Gesamtbericht fuer Einzeltests und Kontrast."""
    lines = [
        "Vergleich historisch festgelegter Zeitraeume",
        "",
        "Suchraum: FIXED und BOOKEND; freie Motiv- und Intervallsuche",
        "Jahresgrenzen beziehen sich auf das Jahr der ersten Erhebung.",
    ]
    for assessment in (contrast.first, contrast.second):
        lines += [
            "",
            "=" * 72,
            f"Zeitraum {assessment.spec.label} ({len(assessment.sequence)} Personen)",
            "=" * 72,
            format_interval_report(
                assessment.sequence,
                assessment.finding,
                assessment.null,
                assessment.p_value,
            ),
            f"Standardisierte Musterstaerke: {assessment.strength:.6f}",
        ]

    lines += [
        "",
        "=" * 72,
        "Direkter Frueh-Spaet-Vergleich",
        "=" * 72,
        f"Differenz der standardisierten Staerken: {contrast.observed_difference:.6f}",
    ]
    if contrast.p_value is not None:
        lines += [
            f"Gerichteter Vergleichs-p-Wert (frueh > spaet): {contrast.p_value:.4f}",
            "Signifikant:   "
            + ("ja (p < 0.05)" if contrast.p_value < 0.05 else "nein (p >= 0.05)"),
            f"Nullmodell:   {contrast.trials} gepoolte Neuverteilungen auf Perioden "
            "gleicher Groesse; in beiden Teilen volle Suche",
        ]
    lines += [
        "",
        "Hinweis: Der Vergleich prueft die zeitliche Konzentration der derzeit "
        "implementierten Musterfamilien. Noch unbekannte Musterformen sind nicht "
        "Bestandteil des Suchraums.",
    ]
    return "\n".join(lines)
