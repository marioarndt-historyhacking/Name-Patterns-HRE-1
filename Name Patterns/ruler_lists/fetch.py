"""Wikipedia ueber die MediaWiki-API abrufen und lokal cachen."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_URL = "https://de.wikipedia.org/w/api.php"
USER_AGENT = "NamePatternsRulerImporter/1.0 (educational research)"


@dataclass(frozen=True)
class FetchedPage:
    title: str
    revision_id: Optional[int]
    fetched_at: str
    html: str
    from_cache: bool = False


class FetchError(RuntimeError):
    """Verstaendlicher Fehler beim Abruf oder Lesen einer Wikipedia-Seite."""


def _cache_name(title: str) -> str:
    safe = "".join(ch.lower() if ch.isalnum() else "_" for ch in title)
    while "__" in safe:
        safe = safe.replace("__", "_")
    return safe.strip("_") + ".json"


def fetch_wikipedia_page(
    title: str,
    cache_dir: Path,
    *,
    offline: bool = False,
    refresh: bool = False,
    timeout: int = 30,
) -> FetchedPage:
    """Liefert gerendertes HTML und Revisionsnummer, online oder aus dem Cache."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / _cache_name(title)

    if offline or (cache_path.exists() and not refresh):
        if not cache_path.exists():
            raise FetchError(f"Kein Cache fuer '{title}' vorhanden: {cache_path}")
        try:
            data = json.loads(cache_path.read_text(encoding="utf-8"))
            return FetchedPage(
                title=data["title"],
                revision_id=data.get("revision_id"),
                fetched_at=data["fetched_at"],
                html=data["html"],
                from_cache=True,
            )
        except (OSError, KeyError, ValueError) as exc:
            raise FetchError(f"Ungueltiger Wikipedia-Cache: {cache_path}") from exc

    query = urlencode(
        {
            "action": "parse",
            "page": title,
            "prop": "text|revid",
            "format": "json",
            "formatversion": "2",
        }
    )
    request = Request(f"{API_URL}?{query}", headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
        parsed = payload["parse"]
        html = parsed["text"]
        if isinstance(html, dict):  # Kompatibilitaet mit formatversion=1-Caches.
            html = html["*"]
        fetched_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        stored = {
            "title": parsed["title"],
            "revision_id": parsed.get("revid"),
            "fetched_at": fetched_at,
            "html": html,
        }
        cache_path.write_text(
            json.dumps(stored, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return FetchedPage(
            title=stored["title"],
            revision_id=stored["revision_id"],
            fetched_at=fetched_at,
            html=html,
        )
    except Exception as exc:
        if cache_path.exists():
            try:
                data = json.loads(cache_path.read_text(encoding="utf-8"))
                return FetchedPage(
                    title=data["title"],
                    revision_id=data.get("revision_id"),
                    fetched_at=data["fetched_at"],
                    html=data["html"],
                    from_cache=True,
                )
            except Exception:
                pass
        raise FetchError(f"Wikipedia-Abruf fuer '{title}' fehlgeschlagen: {exc}") from exc
