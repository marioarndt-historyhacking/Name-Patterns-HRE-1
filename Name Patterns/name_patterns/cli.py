"""Kommandozeile fuer die Mustersuche.

Zwei Betriebsarten:

* **vorgegebenes Motiv** (Default) -- Anchor und Echo kommen per Option.
* **Discovery** (``--discover``) -- das Programm sucht die Motive selbst.

Mit ``--significance N`` wird der Befund zusaetzlich gegen ``N`` zufaellige
Umsortierungen derselben Namensmenge geprueft.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional, Sequence

from .data import HRR_KINGS, load_name_metadata, load_names, name_file_sha256, normalize
from .discovery import Motif, collapse_restatements, discover
from .model import DeviationKind, PatternKind, SearchConfig
from .periods import assess_period_pair, format_period_contrast, parse_period_pair
from .report import format_scored_report
from .scoring import Measure, assess
from .search import find_bookend_chains, find_chains
from .timeline import assess_interval, format_interval_report, load_timeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="name-patterns",
        description=(
            "Sucht in einer Namensliste Bloecke der Form "
            "'Anchor + x Fuellnamen + Echo', deren x konstant bleibt oder "
            "um 1 waechst."
        ),
    )
    motif = parser.add_argument_group("Motiv")
    motif.add_argument(
        "--discover",
        action="store_true",
        help="Anchor und Echo automatisch suchen statt sie vorzugeben",
    )
    motif.add_argument(
        "--anchor",
        default="Konrad,Heinrich",
        help="Anchor-Motiv, Namen mit Komma getrennt (Default: Konrad,Heinrich)",
    )
    motif.add_argument(
        "--echo", default="Heinrich", help="Name, der einen Block schliesst"
    )
    motif.add_argument(
        "--max-anchor-len",
        type=int,
        default=2,
        help="Laengster Anchor, den die Discovery ausprobiert (Default: 2)",
    )
    motif.add_argument(
        "--family",
        choices=("fixed", "bookend", "both"),
        default="both",
        help=(
            "Musterfamilie: 'fixed' = feste Namen (Konrad Heinrich ... Heinrich), "
            "'bookend' = gleicher Name als Klammer, pro Block neu (?N ... ?N), "
            "'both' = beide (Default)"
        ),
    )

    search = parser.add_argument_group("Suche")
    search.add_argument(
        "--data",
        help="Datei mit einem Namen pro Zeile (Default: eingebaute Koenigsliste)",
    )
    search.add_argument(
        "-t",
        "--max-deviations",
        type=int,
        default=0,
        help="Budget an tolerierten Abweichungen pro Kette (Default: 0)",
    )
    search.add_argument(
        "--gap-slack",
        type=int,
        default=1,
        help="Erlaubter Betrag, um den x vom Sollwert abweichen darf (Default: 1)",
    )
    search.add_argument(
        "--min-blocks", type=int, default=3, help="Mindestlaenge einer Kette"
    )
    search.add_argument(
        "--max-gap", type=int, default=12, help="Groesstes zulaessiges x"
    )
    search.add_argument(
        "--d",
        default="0,1",
        help="Erlaubte Schrittweiten, mit Komma getrennt (Default: 0,1)",
    )
    search.add_argument(
        "--no-skip",
        action="store_true",
        help="Fehlende Kettenglieder nicht tolerieren",
    )
    search.add_argument(
        "--no-gap-slack",
        action="store_true",
        help="Abweichende x-Werte nicht tolerieren",
    )
    search.add_argument(
        "--max-interruption",
        type=int,
        default=None,
        metavar="N",
        help=(
            "Hoechstens N Namen zwischen zwei Bloecken "
            "(Default: unbegrenzt)"
        ),
    )
    search.add_argument(
        "--raw-names",
        action="store_true",
        help=(
            "Eintraege unveraendert uebernehmen; ohne dies zaehlt nur der "
            "Rufname bis zum ersten Leerzeichen ('Inge II. Bardsson' -> 'Inge')"
        ),
    )
    search.add_argument(
        "--name-mode",
        choices=("first-token", "full"),
        help=(
            "Namensbehandlung: 'first-token' nutzt nur den Rufnamen (Default), "
            "'full' den ganzen Eintrag; --raw-names bleibt Alias fuer 'full'"
        ),
    )
    search.add_argument(
        "--show-input-metadata",
        action="store_true",
        help="Kommentar-Metadaten und SHA-256 der Eingabedatei anzeigen",
    )
    search.add_argument(
        "--scan-intervals",
        action="store_true",
        help=(
            "Gesamtliste durchsuchen und den global besten Musterabschnitt waehlen; "
            "der Permutationstest wiederholt die freie Zeitraumwahl"
        ),
    )
    search.add_argument(
        "--timeline-metadata",
        help=(
            "CSV des Herrscherimports fuer Anfangs-/Endjahre; ohne Angabe wird "
            "neben --data eine gleichnamige .csv gesucht"
        ),
    )
    search.add_argument(
        "--compare-periods",
        metavar="START:ENDE,START:ENDE",
        help=(
            "Zwei historisch festgelegte Zeitraeume getrennt testen und direkt "
            "vergleichen; durchsucht zwingend FIXED und BOOKEND"
        ),
    )

    stats = parser.add_argument_group("Signifikanz")
    stats.add_argument(
        "-s",
        "--significance",
        type=int,
        default=0,
        metavar="N",
        help="Gegen N zufaellige Umsortierungen pruefen (0 = aus)",
    )
    stats.add_argument(
        "--measure",
        choices=("coverage", "bits"),
        default="coverage",
        help=(
            "Woran gemessen wird: 'coverage' (Default) = Anteil der Liste, den "
            "das Muster erfasst -- zaehlt die Blocklaenge mit; 'bits' = "
            "Seltenheit des Motivs, zaehlt nur die Zahl der Bloecke"
        ),
    )
    stats.add_argument(
        "--seed", type=int, help="Startwert des Zufallsgenerators, macht Laeufe reproduzierbar"
    )
    stats.add_argument(
        "--quiet", action="store_true", help="Keine Fortschrittsanzeige"
    )

    parser.add_argument(
        "--limit", type=int, default=5, help="Wie viele Ketten ausgegeben werden"
    )
    parser.add_argument(
        "--report-output",
        help="Bericht zusaetzlich als UTF-8-Textdatei speichern",
    )
    return parser


def _progress(done: int, total: int) -> None:
    step = max(1, total // 20)
    if done % step == 0 or done == total:
        percent = 100 * done / total
        print(f"\rPermutationen: {done}/{total} ({percent:.0f}%)", end="", file=sys.stderr)
    if done == total:
        print(file=sys.stderr)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.data:
        raw = load_names(args.data, normalize_names=False)
        use_full_names = args.raw_names or args.name_mode == "full"
        if use_full_names:
            sequence, changed = raw, 0
        else:
            sequence, changed = normalize(raw)
        print(f"{len(sequence)} Namen aus {args.data}", end="")
        print(f", {changed} auf den Rufnamen gekuerzt." if changed else ".")
        if args.show_input_metadata:
            metadata = load_name_metadata(args.data)
            print(f"SHA-256: {name_file_sha256(args.data)}")
            if metadata:
                print("Eingabe-Metadaten:")
                for key, value in metadata.items():
                    print(f"  {key}: {value}")
            else:
                print("Eingabe-Metadaten: keine")
        print()
    else:
        sequence = HRR_KINGS

    kinds: List[DeviationKind] = []
    if not args.no_gap_slack:
        kinds.append(DeviationKind.GAP_OFF_BY)
    if not args.no_skip:
        kinds.append(DeviationKind.SKIP)

    families = {
        "fixed": (PatternKind.FIXED,),
        "bookend": (PatternKind.BOOKEND,),
        "both": (PatternKind.FIXED, PatternKind.BOOKEND),
    }[args.family]

    config = SearchConfig(
        max_deviations=args.max_deviations,
        gap_slack=args.gap_slack,
        min_blocks=args.min_blocks,
        max_gap=args.max_gap,
        allowed_d=tuple(int(p) for p in args.d.split(",") if p.strip()),
        allowed_deviations=tuple(kinds),
        max_anchor_len=args.max_anchor_len,
        max_interruption=args.max_interruption,
        families=families,
    )

    if args.compare_periods:
        if not args.data:
            parser.error("--compare-periods benoetigt --data mit einer Gesamtliste")
        if not args.discover:
            parser.error("--compare-periods muss mit --discover laufen")
        timeline_path = args.timeline_metadata
        if timeline_path is None:
            from pathlib import Path

            inferred = Path(args.data).with_suffix(".csv")
            timeline_path = str(inferred) if inferred.exists() else None
        if timeline_path is None:
            parser.error("--compare-periods benoetigt --timeline-metadata")
        try:
            first_period, second_period = parse_period_pair(args.compare_periods)
        except ValueError as exc:
            parser.error(str(exc))
        if families != (PatternKind.FIXED, PatternKind.BOOKEND):
            parser.error("--compare-periods muss mit --family both laufen")
        contrast = assess_period_pair(
            load_timeline(timeline_path),
            config,
            first_period,
            second_period,
            trials=args.significance,
            seed=args.seed,
            progress=None if args.quiet else _progress,
        )
        period_report = format_period_contrast(contrast)
        print(period_report)
        if args.report_output:
            from pathlib import Path

            Path(args.report_output).write_text(period_report + "\n", encoding="utf-8")
        return 0

    if args.scan_intervals:
        if not args.data:
            parser.error("--scan-intervals benoetigt --data mit einer Gesamtliste")
        timeline_path = args.timeline_metadata
        if timeline_path is None:
            from pathlib import Path

            inferred = Path(args.data).with_suffix(".csv")
            timeline_path = str(inferred) if inferred.exists() else None
        timeline = load_timeline(timeline_path) if timeline_path else None
        if args.discover:
            interval_motif = None
        else:
            interval_anchor = tuple(
                part.strip() for part in args.anchor.split(",") if part.strip()
            )
            if not interval_anchor:
                parser.error("--anchor darf nicht leer sein")
            interval_motif = Motif(anchor=interval_anchor, echo=args.echo)
        finding, interval_null, interval_p = assess_interval(
            sequence,
            config,
            motif=interval_motif,
            timeline=timeline,
            trials=args.significance,
            seed=args.seed,
            progress=None if args.quiet else _progress,
        )
        interval_report = format_interval_report(
            sequence, finding, interval_null, interval_p
        )
        print(interval_report)
        if args.report_output:
            from pathlib import Path

            Path(args.report_output).write_text(interval_report + "\n", encoding="utf-8")
        return 0 if finding is not None else 1

    motif = None
    if args.discover:
        chains = discover(sequence, config)
    else:
        chains = []
        if PatternKind.FIXED in families:
            anchor = tuple(
                part.strip() for part in args.anchor.split(",") if part.strip()
            )
            if not anchor:
                parser.error("--anchor darf nicht leer sein")
            chains.extend(find_chains(sequence, anchor, args.echo, config))
            if families == (PatternKind.FIXED,):
                motif = Motif(anchor=anchor, echo=args.echo)
        if PatternKind.BOOKEND in families:
            chains.extend(find_bookend_chains(sequence, config))
        chains = collapse_restatements(chains)

    scored, null = assess(
        sequence,
        chains,
        config,
        motif=motif,
        trials=args.significance,
        seed=args.seed,
        measure=Measure(args.measure),
        progress=None if args.quiet else _progress,
    )
    report = format_scored_report(sequence, scored, null, limit=args.limit)
    print(report)
    if args.report_output:
        from pathlib import Path

        Path(args.report_output).write_text(report + "\n", encoding="utf-8")
    return 0 if scored else 1


if __name__ == "__main__":
    raise SystemExit(main())
