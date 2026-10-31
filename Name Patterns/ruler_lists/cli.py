"""Kommandozeile zum Erzeugen von Herrscherlisten."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .export import export_all
from .fetch import FetchError
from .registry import available_countries, get_adapter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="build-ruler-list",
        description=(
            "Erzeugt aus einer Wikipedia-Herrscherliste eine chronologische "
            "Eingabedatei fuer Name Patterns."
        ),
    )
    parser.add_argument("--country", default="hrr", help="Laenderadapter (Default: hrr)")
    parser.add_argument("--start", type=int, default=911, help="Erstes Erhebungsjahr")
    parser.add_argument("--end", type=int, default=1313, help="Letztes Erhebungsjahr")
    parser.add_argument(
        "--exclude-counter-kings",
        action="store_true",
        help="Gegenkoenige nicht ausgeben",
    )
    parser.add_argument(
        "--exclude-co-kings",
        action="store_true",
        help="Mitkoenige nicht ausgeben",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path(".cache") / "wikipedia",
        help="Verzeichnis fuer Wikipedia-Caches",
    )
    parser.add_argument("--offline", action="store_true", help="Nur lokalen Cache verwenden")
    parser.add_argument("--refresh", action="store_true", help="Cache aus Wikipedia erneuern")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("HRR_Kings_911_1313.txt"),
        help="Zieldatei; CSV und Bericht werden daneben erzeugt",
    )
    parser.add_argument(
        "--list-countries", action="store_true", help="Verfuegbare Laenderadapter anzeigen"
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.list_countries:
        for code, label in available_countries():
            print(f"{code:8s} {label}")
        return 0
    if args.offline and args.refresh:
        parser.error("--offline und --refresh koennen nicht kombiniert werden")
    try:
        adapter = get_adapter(args.country)
        result = adapter.import_rulers(
            args.start,
            args.end,
            include_counter_kings=not args.exclude_counter_kings,
            include_co_kings=not args.exclude_co_kings,
            cache_dir=args.cache_dir,
            offline=args.offline,
            refresh=args.refresh,
        )
        paths = export_all(result, args.output)
    except (ValueError, FetchError, OSError) as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 2

    print(f"{len(result.records)} Personen fuer {args.start}-{args.end} erzeugt:")
    for label, path in paths.items():
        print(f"  {label:8s} {path}")
    for warning in result.warnings:
        print(f"Warnung: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
