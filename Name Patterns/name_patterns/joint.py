"""Mehrere Listen gemeinsam auswerten.

Die Listen werden **nicht** aneinandergehaengt -- das wuerde Bloecke erlauben,
die ueber die Grenze zweier Dynastien reichen, und solche Bloecke bedeuten
nichts.  Verbunden wird stattdessen die *Evidenz*: drei unabhaengige Tests zu
einer Aussage.

Zwei Wege, die sich gegenseitig kontrollieren:

**Gemeinsamer Permutationstest** (bevorzugt).  Pro Durchlauf wird *jede* Liste
fuer sich umsortiert und die gemeinsame Kennzahl berechnet.  Das setzt nichts
voraus ausser der Unabhaengigkeit der Listen und ist damit die ehrlichere
Rechnung.

**Fishers Methode** als Gegenprobe.  Verbindet die Einzel-p-Werte analytisch.
Setzt voraus, dass diese unter der Nullhypothese gleichverteilt sind -- bei
Monte-Carlo-p-Werten mit Plus-Eins-Korrektur naeherungsweise erfuellt, aber eben
nur naeherungsweise.  Stimmen beide Wege ueberein, ist das Ergebnis belastbar.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

from .discovery import discover
from .model import Chain, Names, SearchConfig
from .scoring import Measure, chain_statistic, name_probabilities


@dataclass
class ListOutcome:
    """Das Ergebnis einer einzelnen Liste."""

    name: str
    size: int
    chain: Optional[Chain]
    statistic: float
    p_value: float

    @property
    def covered(self) -> int:
        return self.chain.covered if self.chain else 0


@dataclass
class JointResult:
    """Die gemeinsame Auswertung mehrerer Listen."""

    outcomes: List[ListOutcome]
    trials: int
    measure: Measure
    #: Mittelwert der Kennzahl ueber die Listen, beobachtet.
    observed_mean: float = 0.0
    #: Verteilung dieses Mittelwerts unter gemeinsamer Permutation.
    null_means: Tuple[float, ...] = ()
    #: Wie oft der Zufall *alle* Listen zugleich mindestens so gut ordnete.
    all_at_once: int = 0

    @property
    def p_mean(self) -> float:
        hits = sum(1 for m in self.null_means if m >= self.observed_mean)
        return (1 + hits) / (1 + self.trials)

    @property
    def p_all(self) -> float:
        return (1 + self.all_at_once) / (1 + self.trials)

    @property
    def p_fisher(self) -> float:
        return fisher_combined([o.p_value for o in self.outcomes])


def chi2_survival_even_df(x: float, df: int) -> float:
    """P(X^2 > x) fuer gerade Freiheitsgrade -- exakt und ohne SciPy.

    Fuer ``df = 2k`` gilt die endliche Reihe
    ``exp(-x/2) * sum_{i<k} (x/2)^i / i!``.  Fishers Methode liefert immer
    gerade Freiheitsgrade (``2`` je kombiniertem Test), deshalb genuegt das.
    """
    if df % 2 != 0:
        raise ValueError("nur gerade Freiheitsgrade")
    if x <= 0:
        return 1.0
    half = x / 2.0
    total = 0.0
    term = 1.0
    for i in range(df // 2):
        if i:
            term *= half / i
        total += term
    return min(1.0, math.exp(-half) * total)


def fisher_combined(p_values: Sequence[float]) -> float:
    """Fishers Methode: verbindet unabhaengige p-Werte zu einem."""
    usable = [p for p in p_values if p > 0.0]
    if not usable:
        return 0.0
    statistic = -2.0 * sum(math.log(p) for p in usable)
    return chi2_survival_even_df(statistic, 2 * len(usable))


def _best_statistic(
    sequence: Names,
    config: SearchConfig,
    measure: Measure,
    probs: Dict[str, float],
) -> Tuple[Optional[Chain], float]:
    chains = discover(sequence, config)
    if not chains:
        return None, 0.0
    best = max(chains, key=lambda c: chain_statistic(sequence, c, measure, probs))
    return best, chain_statistic(sequence, best, measure, probs)


def evaluate_jointly(
    datasets: Sequence[Tuple[str, List[str]]],
    config: SearchConfig,
    *,
    trials: int = 2000,
    seed: Optional[int] = None,
    measure: Measure = Measure.COVERAGE,
) -> JointResult:
    """Wertet mehrere Listen einzeln und gemeinsam aus.

    ``datasets`` sind Paare aus Name und Namensliste.  Auf alle wird dieselbe
    Konfiguration angewandt -- ohne das waere der gemeinsame Test wertlos, weil
    sich die Einzelergebnisse dann nicht mehr vergleichen liessen.
    """
    probs = [name_probabilities(seq) for _, seq in datasets]
    observed: List[float] = []
    chains: List[Optional[Chain]] = []
    for (name, sequence), p in zip(datasets, probs):
        chain, value = _best_statistic(sequence, config, measure, p)
        chains.append(chain)
        observed.append(value)

    rng = random.Random(seed)
    pools = [list(seq) for _, seq in datasets]
    hits = [0] * len(datasets)
    null_means: List[float] = []
    all_at_once = 0

    for _ in range(trials):
        values: List[float] = []
        for index, pool in enumerate(pools):
            rng.shuffle(pool)
            _, value = _best_statistic(pool, config, measure, probs[index])
            values.append(value)
            if value >= observed[index]:
                hits[index] += 1
        null_means.append(sum(values) / len(values))
        if all(v >= o for v, o in zip(values, observed)):
            all_at_once += 1

    outcomes = [
        ListOutcome(
            name=name,
            size=len(sequence),
            chain=chain,
            statistic=value,
            p_value=(1 + hit) / (1 + trials),
        )
        for (name, sequence), chain, value, hit in zip(
            datasets, chains, observed, hits
        )
    ]
    return JointResult(
        outcomes=outcomes,
        trials=trials,
        measure=measure,
        observed_mean=sum(observed) / len(observed),
        null_means=tuple(null_means),
        all_at_once=all_at_once,
    )


def _main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    from .data import load_names
    from .model import PatternKind

    parser = argparse.ArgumentParser(
        prog="name-patterns-joint",
        description="Wertet mehrere Namenslisten einzeln und gemeinsam aus.",
    )
    parser.add_argument("data", nargs="+", help="Namenslisten, eine Datei je Liste")
    parser.add_argument("--trials", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--d", default="0")
    parser.add_argument("--min-blocks", type=int, default=3)
    parser.add_argument("--max-gap", type=int, default=12)
    parser.add_argument("--max-interruption", type=int, default=4)
    parser.add_argument("-t", "--max-deviations", type=int, default=0)
    args = parser.parse_args(argv)

    from pathlib import Path

    datasets = [(Path(p).stem, load_names(p)) for p in args.data]
    config = SearchConfig(
        max_deviations=args.max_deviations,
        min_blocks=args.min_blocks,
        max_gap=args.max_gap,
        allowed_d=tuple(int(p) for p in args.d.split(",") if p.strip()),
        max_interruption=args.max_interruption,
        families=(PatternKind.BOOKEND,),
    )
    result = evaluate_jointly(
        datasets, config, trials=args.trials, seed=args.seed
    )

    print(f"{'Liste':16s} {'n':>4} {'Bloecke':>8} {'Laenge':>7} {'Abdeckung':>11} {'p':>9}")
    print("-" * 60)
    for outcome in result.outcomes:
        chain = outcome.chain
        blocks = len(chain.placements) if chain else 0
        length = chain.placements[0].block.length if chain else 0
        print(
            f"{outcome.name:16s} {outcome.size:4d} {blocks:8d} {length:7d} "
            f"{outcome.covered:5d}/{outcome.size:<5d} {outcome.p_value:9.5f}"
        )
    print()
    print(f"Gemeinsam ueber {result.trials} Durchlaeufe:")
    print(f"  mittlere Abdeckung   beobachtet {result.observed_mean:.1%}, "
          f"Zufall {sum(result.null_means) / len(result.null_means):.1%}, "
          f"bester Zufall {max(result.null_means):.1%}")
    print(f"  p (mittlere Abdeckung) = {result.p_mean:.6f}")
    print(f"  p (alle zugleich)      = {result.p_all:.6f}"
          f"   [{result.all_at_once} von {result.trials}]")
    print(f"  p (Fisher, Gegenprobe) = {result.p_fisher:.3e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
