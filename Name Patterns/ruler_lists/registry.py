"""Registry der verfuegbaren Laenderadapter."""

from __future__ import annotations

from typing import Dict, List, Tuple

from .sources.base import CountryAdapter
from .sources.hrr_dewiki import HRRAdapter


_ADAPTERS: Dict[str, CountryAdapter] = {
    adapter.code: adapter for adapter in (HRRAdapter(),)
}


def get_adapter(code: str) -> CountryAdapter:
    try:
        return _ADAPTERS[code.lower()]
    except KeyError as exc:
        choices = ", ".join(sorted(_ADAPTERS))
        raise ValueError(f"Unbekanntes Land '{code}'. Verfuegbar: {choices}") from exc


def available_countries() -> List[Tuple[str, str]]:
    return sorted((code, adapter.label) for code, adapter in _ADAPTERS.items())
