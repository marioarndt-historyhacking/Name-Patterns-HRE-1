"""Exakte 113-Jahres-Folge und gemeinsamer Test mit dem Namensmuster.

Die Ereignistabelle bildet die regulaere Nachfolgebeziehung ab: Zu jedem
Koenig, der nicht ausschliesslich Gegenkoenig blieb, steht das Todesjahr seines
in der Herrscherfolge angegebenen Vorgaengers. Parallel- und Mitkoenigtum
aendern diese fachlich kontrollierte Vorgaengerzuordnung nicht.
"""

from __future__ import annotations

import argparse
import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from .model import PatternKind, SearchConfig
from .timeline import TimelineEntry, best_interval, load_timeline


@dataclass(frozen=True)
class SuccessionEvent:
    predecessor: str
    predecessor_death_year: int
    successor_person_id: str
    successor_name: str


# Kontrollierte regulaere Vorgaengerfolge nach der deutschsprachigen Wikipedia.
# Ausschliesslich als Gegenkoenige gefuehrte Nachfolger sind nicht enthalten.
# Die Todesjahre sind die modern normalisierten Jahreszahlen der Biographien.
EVENTS: Tuple[SuccessionEvent, ...] = (
    SuccessionEvent("Ludwig II. der Deutsche", 876, "karlmann-ostfranken", "Karlmann"),
    SuccessionEvent("Ludwig II. der Deutsche", 876, "ludwig-iii-juengere", "Ludwig"),
    SuccessionEvent("Ludwig II. der Deutsche", 876, "karl-iii-dicke", "Karl"),
    SuccessionEvent("Karl III. der Dicke", 888, "arnolf-kaernten", "Arnolf"),
    SuccessionEvent("Arnolf von Kärnten", 899, "ludwig-iv-kind", "Ludwig"),
    SuccessionEvent("Ludwig IV. das Kind", 911, "konrad-i", "Konrad"),
    SuccessionEvent("Konrad I.", 918, "heinrich-i", "Heinrich"),
    SuccessionEvent("Heinrich I.", 936, "otto-i", "Otto"),
    SuccessionEvent("Otto I.", 973, "otto-ii", "Otto"),
    SuccessionEvent("Otto II.", 983, "otto-iii", "Otto"),
    SuccessionEvent("Otto III.", 1002, "heinrich-ii", "Heinrich"),
    SuccessionEvent("Heinrich II.", 1024, "konrad-ii", "Konrad"),
    SuccessionEvent("Konrad II.", 1039, "heinrich-iii", "Heinrich"),
    SuccessionEvent("Heinrich III.", 1056, "heinrich-iv", "Heinrich"),
    SuccessionEvent("Heinrich IV.", 1106, "heinrich-v", "Heinrich"),
    SuccessionEvent("Heinrich V.", 1125, "lothar-iii", "Lothar"),
    SuccessionEvent("Lothar III.", 1137, "konrad-iii", "Konrad"),
    SuccessionEvent("Konrad III.", 1152, "friedrich-i", "Friedrich"),
    SuccessionEvent("Friedrich I.", 1190, "heinrich-vi", "Heinrich"),
    SuccessionEvent("Heinrich VI.", 1197, "philipp-schwaben", "Philipp"),
    SuccessionEvent("Heinrich VI.", 1197, "otto-iv", "Otto"),
    SuccessionEvent("Otto IV.", 1218, "friedrich-ii", "Friedrich"),
    SuccessionEvent("Friedrich II.", 1250, "konrad-iv", "Konrad"),
    SuccessionEvent("Wilhelm von Holland", 1256, "richard-cornwall", "Richard"),
    SuccessionEvent("Richard von Cornwall", 1272, "rudolf-i", "Rudolf"),
    SuccessionEvent("Rudolf I.", 1291, "adolf-nassau", "Adolf"),
    SuccessionEvent("Adolf von Nassau", 1298, "albrecht-i", "Albrecht"),
    SuccessionEvent("Albrecht I.", 1308, "heinrich-vii-lux", "Heinrich"),
    SuccessionEvent("Heinrich VII.", 1313, "ludwig-iv-bayer", "Ludwig"),
    SuccessionEvent("Ludwig IV.", 1347, "karl-iv", "Karl"),
    SuccessionEvent("Karl IV.", 1378, "wenzel-luxemburg", "Wenzel"),
    SuccessionEvent("Wenzel", 1419, "ruprecht-pfalz", "Ruprecht"),
    SuccessionEvent("Ruprecht", 1410, "jobst-maehren", "Jobst"),
    SuccessionEvent("Jobst von Mähren", 1411, "sigismund-luxemburg", "Sigismund"),
    SuccessionEvent("Sigismund", 1437, "albrecht-ii", "Albrecht"),
    SuccessionEvent("Albrecht II.", 1439, "friedrich-iii", "Friedrich"),
    SuccessionEvent("Friedrich III.", 1493, "maximilian-i", "Maximilian"),
    SuccessionEvent("Maximilian I.", 1519, "karl-v", "Karl"),
    SuccessionEvent("Karl V.", 1558, "ferdinand-i", "Ferdinand"),
    SuccessionEvent("Ferdinand I.", 1564, "maximilian-ii", "Maximilian"),
    SuccessionEvent("Maximilian II.", 1576, "rudolf-ii", "Rudolf"),
    SuccessionEvent("Rudolf II.", 1612, "matthias-habsburg", "Matthias"),
    SuccessionEvent("Matthias", 1619, "ferdinand-ii", "Ferdinand"),
    SuccessionEvent("Ferdinand II.", 1637, "ferdinand-iii", "Ferdinand"),
    SuccessionEvent("Ferdinand III.", 1657, "leopold-i", "Leopold"),
    SuccessionEvent("Leopold I.", 1705, "joseph-i", "Joseph"),
    SuccessionEvent("Joseph I.", 1711, "karl-vi", "Karl"),
    SuccessionEvent("Karl VI.", 1740, "karl-vii", "Karl"),
    SuccessionEvent("Karl VII.", 1745, "franz-i", "Franz"),
    SuccessionEvent("Franz I.", 1765, "joseph-ii", "Joseph"),
    SuccessionEvent("Joseph II.", 1790, "leopold-ii", "Leopold"),
    SuccessionEvent("Leopold II.", 1792, "franz-ii", "Franz"),
)


@dataclass(frozen=True)
class Progression:
    name: str
    years: Tuple[int, ...]

    @property
    def step(self) -> int:
        return self.years[1] - self.years[0]


@dataclass(frozen=True)
class JointResult:
    trials: int
    hits: int
    name_pattern_p: float
    event_targeted_p: float
    event_global_p: float
    joint_p: float
    observed_chain_score: float


def wilson_interval(hits: int, trials: int, z: float = 1.96) -> Tuple[float, float]:
    """Wilson-Intervall fuer die Monte-Carlo-Trefferwahrscheinlichkeit."""
    if trials <= 0:
        return (0.0, 1.0)
    proportion = hits / trials
    denominator = 1 + z * z / trials
    center = (proportion + z * z / (2 * trials)) / denominator
    radius = (
        z
        * math.sqrt(
            proportion * (1 - proportion) / trials
            + z * z / (4 * trials * trials)
        )
        / denominator
    )
    return center - radius, center + radius


def arithmetic_index_sets(
    events: Sequence[SuccessionEvent], length: int = 4
) -> List[Tuple[int, ...]]:
    """Alle Indexmengen mit verschiedenen Jahren in exakter Progression."""
    result: List[Tuple[int, ...]] = []
    for indices in combinations(range(len(events)), length):
        years = sorted(events[index].predecessor_death_year for index in indices)
        if len(set(years)) != length:
            continue
        step = years[1] - years[0]
        if step > 0 and all(
            years[pos] - years[pos - 1] == step for pos in range(2, length)
        ):
            result.append(indices)
    return result


def observed_progressions(
    events: Sequence[SuccessionEvent] = EVENTS, length: int = 4
) -> List[Progression]:
    result: List[Progression] = []
    for indices in arithmetic_index_sets(events, length):
        names = {events[index].successor_name for index in indices}
        if len(names) == 1:
            years = tuple(sorted(events[index].predecessor_death_year for index in indices))
            result.append(Progression(next(iter(names)), years))
    return result


def exact_event_p_values(
    events: Sequence[SuccessionEvent] = EVENTS,
    *,
    target_name: str = "Konrad",
    target_years: Tuple[int, ...] = (911, 1024, 1137, 1250),
) -> Tuple[float, float, int]:
    """Gezielter und global namens-korrigierter exakter Permutations-p-Wert.

    Fuer die vorliegenden Ereignisjahre existiert genau eine viergliedrige
    Progression. Unter zufaelliger Verteilung der beobachteten Namenshaeufigkeit
    ist der gezielte Wert ``1 / C(n, 4)``. Der globale Wert summiert ueber alle
    Namen, die vier gleiche Labels auf diese Positionen legen koennten.
    """
    progressions = arithmetic_index_sets(events, len(target_years))
    matching = [
        indices for indices in progressions
        if tuple(sorted(events[i].predecessor_death_year for i in indices)) == target_years
    ]
    if len(progressions) != 1 or len(matching) != 1:
        raise ValueError("Exakte Formel setzt genau eine viergliedrige Jahresfolge voraus")
    counts = Counter(event.successor_name for event in events)
    n = len(events)
    denominator = math.comb(n, len(target_years))
    if counts[target_name] < len(target_years):
        raise ValueError("Zielname kommt fuer die Zielfolge nicht oft genug vor")
    targeted = 1 / denominator
    global_hits = sum(
        math.comb(count, len(target_years))
        for count in counts.values()
        if count >= len(target_years)
    )
    return targeted, global_hits / denominator, global_hits


def _early_timeline(timeline: Sequence[TimelineEntry]) -> List[TimelineEntry]:
    return [entry for entry in timeline if 911 <= entry.elevation_year <= 1313]


def assess_joint(
    timeline: Sequence[TimelineEntry],
    *,
    trials: int = 1_000_000,
    seed: int = 42,
    name_pattern_p: float = 0.0160,
) -> JointResult:
    """Gemeinsamer Permutationstest statt unzulaessiger p-Wert-Multiplikation.

    Die 31 Namen werden gemeinsam permutiert. Ein Treffer muss zugleich einen
    mindestens so hohen Discovery-Scan-Score und eine viergliedrige gleiche
    Namensbelegung der 113-Jahres-Ereignisse erreichen. Der Ereignisfilter wird
    zuerst ausgewertet; das haelt auch grosse Referenzlaeufe schnell.
    """
    early = _early_timeline(timeline)
    sequence = [entry.analysis_name for entry in early]
    positions: Dict[str, int] = {entry.person_id: i for i, entry in enumerate(early)}
    target_events = [
        event for event in EVENTS
        if event.predecessor_death_year in (911, 1024, 1137, 1250)
        and event.successor_person_id in positions
    ]
    if len(target_events) != 4:
        raise ValueError("Die vier Konrad-Ereignisse fehlen in der Timeline")
    target_positions = tuple(positions[event.successor_person_id] for event in target_events)
    config = SearchConfig(
        min_blocks=3,
        max_deviations=0,
        allowed_d=(0, 1),
        families=(PatternKind.FIXED, PatternKind.BOOKEND),
    )
    observed = best_interval(sequence, config, motif=None)
    if observed is None:
        raise ValueError("Kein beobachtetes Namensmuster gefunden")

    shuffled = list(sequence)
    rng = random.Random(seed)
    hits = 0
    for _ in range(trials):
        rng.shuffle(shuffled)
        if len({shuffled[index] for index in target_positions}) != 1:
            continue
        candidate = best_interval(shuffled, config, motif=None)
        if candidate is not None and candidate.score >= observed.score:
            hits += 1

    targeted, global_p, _ = exact_event_p_values()
    return JointResult(
        trials=trials,
        hits=hits,
        name_pattern_p=name_pattern_p,
        event_targeted_p=targeted,
        event_global_p=global_p,
        joint_p=(hits + 1) / (trials + 1),
        observed_chain_score=observed.score,
    )


def format_report(result: JointResult) -> str:
    progression = observed_progressions()[0]
    _, _, global_hits = exact_event_p_values()
    ci_low, ci_high = wilson_interval(result.hits, result.trials)
    return "\n".join(
        [
            "113-Jahres-Ereignisfolge und gemeinsamer Signifikanztest",
            "",
            f"Ereignisse:   {', '.join(str(y) for y in progression.years)}",
            f"Name:         {progression.name}",
            f"Abstand:      {progression.step} Jahre (dreimal exakt)",
            f"Suchbasis:    {len(EVENTS)} regulaere Vorgaenger-Nachfolger-Ereignisse, 843–1806",
            "Viererfolgen:  genau 1 in den beobachteten Todesjahren",
            "",
            f"Gezielter exakter p-Wert (Konrad und Jahre fest): {result.event_targeted_p:.8f}",
            f"Globaler exakter p-Wert (Name frei):             {result.event_global_p:.8f}",
            f"Global guenstige Namensbelegungen:                {global_hits}",
            "",
            f"Namensketten-p-Wert 911–1313:                     {result.name_pattern_p:.4f}",
            f"Gemeinsamer Permutations-p-Wert:                  {result.joint_p:.6f}",
            f"Gemeinsame Zufallstreffer:                         {result.hits}/{result.trials}",
            f"Monte-Carlo-Unsicherheit (Wilson 95 %):             {ci_low:.6f}–{ci_high:.6f}",
            "Signifikant:                                      "
            + ("ja (p < 0.05)" if result.joint_p < 0.05 else "nein (p >= 0.05)"),
            "",
            "Der gemeinsame Wert wurde nicht durch Multiplikation der Einzel-p-Werte erzeugt.",
            "In jeder Permutation mussten beide Befunde gleichzeitig mindestens so stark sein.",
        ]
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeline", default="HRR_Kings_843_1806.csv")
    parser.add_argument("--trials", type=int, default=1_000_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    result = assess_joint(load_timeline(args.timeline), trials=args.trials, seed=args.seed)
    report = format_report(result)
    print(report)
    if args.output:
        Path(args.output).write_text(report + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
