"""Schnittstelle fuer erweiterbare Laenderadapter."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ..model import ImportResult


class CountryAdapter(ABC):
    code: str
    label: str
    source_title: str

    @abstractmethod
    def import_rulers(
        self,
        start_year: int,
        end_year: int,
        *,
        include_counter_kings: bool,
        include_co_kings: bool,
        cache_dir: Path,
        offline: bool,
        refresh: bool,
    ) -> ImportResult:
        raise NotImplementedError
