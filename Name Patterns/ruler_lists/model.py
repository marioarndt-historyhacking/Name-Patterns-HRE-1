"""Datenmodell fuer importierte Herrscher und ihre Quellen."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple


class Role(str, Enum):
    """Rolle bei der ersten Koenigserhebung."""

    KING = "king"
    CO_KING = "co_king"
    COUNTER_KING = "counter_king"

    @property
    def german(self) -> str:
        return {
            Role.KING: "König",
            Role.CO_KING: "Mitkönig",
            Role.COUNTER_KING: "Gegenkönig",
        }[self]


@dataclass(frozen=True)
class SourceInfo:
    """Nachweis, auf welcher Wikipedia-Fassung ein Import beruht."""

    page_title: str
    page_url: str
    revision_id: Optional[int]
    fetched_at: str
    language: str = "de"


@dataclass(frozen=True)
class RulerRecord:
    """Eine Person, einsortiert bei ihrer ersten Koenigserhebung."""

    person_id: str
    canonical_name: str
    analysis_name: str
    country: str
    elevation_year: int
    role: Role
    source_order: int
    source_chronicle: str
    source_section: str = ""
    elevation_date: Optional[str] = None
    later_roles: Tuple[str, ...] = ()


@dataclass
class ImportResult:
    """Gefilterte Herrscherliste samt Quellen- und Pruefinformationen."""

    country: str
    start_year: int
    end_year: int
    records: List[RulerRecord]
    source: SourceInfo
    warnings: List[str] = field(default_factory=list)

    def validate(self) -> None:
        if self.start_year > self.end_year:
            raise ValueError("Startjahr darf nicht nach dem Endjahr liegen")
        ids = [record.person_id for record in self.records]
        if len(ids) != len(set(ids)):
            raise ValueError("Dieselbe Person ist mehrfach in der Ergebnisliste")
        keys = [(r.elevation_year, r.source_order) for r in self.records]
        if keys != sorted(keys):
            raise ValueError("Ergebnisliste ist nicht chronologisch sortiert")
        for record in self.records:
            if not self.start_year <= record.elevation_year <= self.end_year:
                raise ValueError(
                    f"{record.canonical_name}: Erhebungsjahr ausserhalb des Zeitraums"
                )
            if not record.analysis_name.strip():
                raise ValueError(f"{record.canonical_name}: leerer Analysename")
