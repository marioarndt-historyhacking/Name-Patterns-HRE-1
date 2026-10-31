"""Datenmodell der Mustersuche.

Begriffe (siehe README):

* **Anchor** -- Motiv, das einen Block eroeffnet, z.B. ``("Konrad", "Heinrich")``.
* **Echo**   -- Name, der den Block schliesst, z.B. ``"Heinrich"``.
* **Block**  -- ein Vorkommen von Anchor + ``x`` Fuellnamen + Echo.
* **Chain**  -- Folge disjunkter Bloecke, deren ``x``-Werte eine arithmetische
  Folge ``x0, x0+d, x0+2d, ...`` bilden.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Sequence, Set, Tuple


class PatternKind(str, Enum):
    """Die beiden Musterfamilien."""

    #: Anchor und Echo sind feste Namen, ueber alle Bloecke hinweg dieselben.
    #: Beispiel: ``Konrad Heinrich ... Heinrich``.
    FIXED = "fixed"
    #: Jeder Block wird von *demselben* Namen eingeklammert -- welcher das ist,
    #: wird pro Block neu gebunden.  Beispiel: ``Olav ... Olav``, dann
    #: ``Oeystein ... Oeystein``, dann ``Hakon ... Hakon``.
    BOOKEND = "bookend"


class DeviationKind(str, Enum):
    """Arten tolerierter Abweichungen (Stufe 2)."""

    #: Der Block sitzt an der richtigen Stelle, aber ``x`` weicht vom Sollwert ab.
    GAP_OFF_BY = "gap_off_by"
    #: An dieser Kettenposition fehlt ein Block ganz; die Progression laeuft weiter.
    SKIP = "skip"


@dataclass(frozen=True)
class Block:
    """Ein Anchor-Echo-Block in der Namensliste.

    ``echo_pos`` ist redundant (``anchor_pos + anchor_len + x``), wird aber
    mitgefuehrt, damit Bloecke ohne Kenntnis des Anchors verglichen werden
    koennen.
    """

    anchor_pos: int
    x: int
    echo_pos: int
    #: Bei :attr:`PatternKind.BOOKEND` der Name, der diesen Block einklammert.
    #: Bei :attr:`PatternKind.FIXED` ``None`` -- dort steht das Motiv an der Kette.
    name: Optional[str] = None

    @property
    def span(self) -> Tuple[int, int]:
        """Erster und letzter belegter Index (beide inklusive)."""
        return (self.anchor_pos, self.echo_pos)

    @property
    def length(self) -> int:
        """Gesamtzahl der Namen im Block, Klammern eingeschlossen."""
        return self.echo_pos - self.anchor_pos + 1


@dataclass(frozen=True)
class Deviation:
    """Eine einzelne Abweichung vom idealen Muster."""

    kind: DeviationKind
    #: Position in der Kette (j), an der die Abweichung auftritt.
    chain_index: int
    #: Sollwert von x an dieser Kettenposition.
    expected_x: int
    #: Tatsaechliches x -- ``None`` bei :attr:`DeviationKind.SKIP`.
    actual_x: Optional[int] = None

    def describe(self) -> str:
        if self.kind is DeviationKind.SKIP:
            return f"j={self.chain_index}: uebersprungen (Soll x={self.expected_x})"
        diff = (self.actual_x or 0) - self.expected_x
        return (
            f"j={self.chain_index}: x={self.actual_x} statt {self.expected_x} "
            f"({diff:+d})"
        )


@dataclass(frozen=True)
class Placement:
    """Ein Block an einer konkreten Kettenposition."""

    chain_index: int
    block: Block
    expected_x: int
    deviation: Optional[Deviation] = None


@dataclass
class Chain:
    """Eine gefundene Musterkette."""

    anchor: Tuple[str, ...]
    echo: str
    x0: int
    d: int
    placements: List[Placement] = field(default_factory=list)
    deviations: List[Deviation] = field(default_factory=list)
    #: Straffaktor je Abweichung -- vom SearchConfig durchgereicht.
    deviation_penalty: float = 0.5
    kind: PatternKind = PatternKind.FIXED

    @property
    def blocks(self) -> List[Block]:
        return [p.block for p in self.placements]

    @property
    def bookend_names(self) -> List[str]:
        """Die je Block gebundenen Klammernamen (nur bei BOOKEND belegt)."""
        return [p.block.name for p in self.placements if p.block.name is not None]

    @property
    def distinct_bookends(self) -> bool:
        """Ob jeder Block von einem *anderen* Namen eingeklammert wird.

        Im norwegischen Fall (Olav / Oeystein / Hakon) trifft das zu und ist
        gerade das Auffaellige -- gefordert wird es aber nicht.
        """
        names = self.bookend_names
        return len(names) == len(set(names))

    def describe_motif(self) -> str:
        if self.kind is PatternKind.BOOKEND:
            return "?N ... ?N"
        return f"{' '.join(self.anchor)} ... {self.echo}"

    # -- Abdeckung -------------------------------------------------------
    #
    # Wie viel der Liste das Muster ueberhaupt erklaert.  Die Zahl der Bloecke
    # allein sagt das nicht: drei Bloecke zu je drei Namen erklaeren neun
    # Positionen, drei Bloecke zu je acht Namen vierundzwanzig.  Fuer die
    # Frage "ist diese Anordnung geordneter als eine zufaellige?" ist die
    # Abdeckung die passendere Groesse.

    def covered_positions(self) -> Set[int]:
        """Alle Indizes, die innerhalb eines Blocks liegen (Klammern inklusive)."""
        covered: Set[int] = set()
        for placement in self.placements:
            covered.update(
                range(placement.block.anchor_pos, placement.block.echo_pos + 1)
            )
        return covered

    @property
    def covered(self) -> int:
        return len(self.covered_positions())

    def coverage(self, total: int) -> float:
        """Anteil der Liste, der vom Muster erfasst wird."""
        return self.covered / total if total else 0.0

    def outsiders(self, total: int) -> List[int]:
        """Positionen, die aus der Ordnung ausbrechen -- auch vor und nach der Kette."""
        covered = self.covered_positions()
        return [i for i in range(total) if i not in covered]

    def max_outsider_run(self, total: int) -> int:
        """Laengste ununterbrochene Strecke ausserhalb aller Bloecke.

        Anders als ``max_interruption`` zaehlt das auch die Raender: eine Kette,
        die erst in der Mitte der Liste beginnt, laesst vorne eine lange
        unstrukturierte Strecke, und die gehoert zur Beurteilung dazu.
        """
        covered = self.covered_positions()
        longest = current = 0
        for i in range(total):
            if i in covered:
                current = 0
            else:
                current += 1
                longest = max(longest, current)
        return longest

    @property
    def score(self) -> float:
        """Vorlaeufiger Score (Stufe 1+2).

        Laenge der Kette, abzueglich einer Strafe je Abweichung.  Die
        aussagekraeftigere Bewertung inklusive Monte-Carlo-Signifikanz ist
        Stufe 4 und bewusst noch nicht enthalten.
        """
        return len(self.placements) - self.deviation_penalty * len(self.deviations)

    @property
    def span(self) -> Tuple[int, int]:
        return (self.placements[0].block.anchor_pos, self.placements[-1].block.echo_pos)

    def expected_x_at(self, chain_index: int) -> int:
        return self.x0 + chain_index * self.d

    def signature(self) -> Tuple[int, ...]:
        """Identitaet ueber die belegten Anchor-Positionen (fuer Dedup)."""
        return tuple(p.block.anchor_pos for p in self.placements)

    def rule(self) -> str:
        if self.d == 0:
            return f"x = {self.x0} (konstant)"
        return f"x = {self.x0} + j*{self.d}"


@dataclass(frozen=True)
class SearchConfig:
    """Alle Stellschrauben der Suche an einem Ort."""

    #: Budget an tolerierten Abweichungen pro Kette (Anforderung 3).
    max_deviations: int = 0
    #: Wie weit ``x`` bei GAP_OFF_BY vom Sollwert abweichen darf.
    gap_slack: int = 1
    #: Ketten unterhalb dieser Blockzahl werden verworfen.
    min_blocks: int = 3
    #: Groesstes zulaessiges x beim Einsammeln der Blockkandidaten.
    max_gap: int = 12
    #: Erlaubte Schrittweiten der arithmetischen Folge (Anforderung 2).
    allowed_d: Tuple[int, ...] = (0, 1)
    #: Welche Abweichungsarten ueberhaupt erlaubt sind.
    allowed_deviations: Tuple[DeviationKind, ...] = (
        DeviationKind.GAP_OFF_BY,
        DeviationKind.SKIP,
    )
    deviation_penalty: float = 0.5
    #: Maximale Anchor-Laenge bei der automatischen Motivsuche (Stufe 3).
    max_anchor_len: int = 2
    #: Hoechstzahl an Namen zwischen zwei aufeinanderfolgenden Bloecken.
    #: ``None`` = unbegrenzt; dann duerfen Bloecke beliebig weit auseinanderliegen.
    #: Die Schranke gilt zwischen *gesetzten* Bloecken und wird durch ein
    #: uebersprungenes Kettenglied nicht gelockert.
    max_interruption: Optional[int] = None
    #: Welche Musterfamilien die Discovery durchsucht.
    families: Tuple[PatternKind, ...] = (PatternKind.FIXED, PatternKind.BOOKEND)

    def allows(self, kind: DeviationKind) -> bool:
        return kind in self.allowed_deviations

    def searches(self, kind: PatternKind) -> bool:
        return kind in self.families


Names = Sequence[str]
