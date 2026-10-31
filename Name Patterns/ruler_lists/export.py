"""Ausgabe fuer die Mustersuche und fuer die Quellenpruefung."""

from __future__ import annotations

import csv
import hashlib
import io
from pathlib import Path
from typing import Dict

from .model import ImportResult


def render_names(result: ImportResult) -> str:
    revision = result.source.revision_id if result.source.revision_id is not None else "unbekannt"
    lines = [
        "# Automatisch erzeugte Herrscherliste fuer Name Patterns",
        f"# Land: {result.country}",
        f"# Zeitraum der ersten Koenigserhebung: {result.start_year}-{result.end_year}",
        f"# Quelle: {result.source.page_url}",
        f"# Wikipedia-Revision: {revision}",
        f"# Abrufzeit (UTC): {result.source.fetched_at}",
        "# Sortierung: erste Koenigserhebung; bei Gleichstand Wikipedia-Tabellenreihenfolge",
        "# Jede Person erscheint nur einmal; spaetere Amtszeiten/Rollen werden nicht wiederholt.",
        "",
    ]
    lines.extend(record.analysis_name for record in result.records)
    return "\n".join(lines) + "\n"


def render_csv(result: ImportResult) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "position",
            "analysis_name",
            "canonical_name",
            "person_id",
            "elevation_year",
            "role",
            "role_de",
            "later_roles",
            "source_section",
            "source_chronicle",
            "source_order",
            "source_url",
            "revision_id",
        ]
    )
    for position, record in enumerate(result.records, start=1):
        writer.writerow(
            [
                position,
                record.analysis_name,
                record.canonical_name,
                record.person_id,
                record.elevation_year,
                record.role.value,
                record.role.german,
                "; ".join(record.later_roles),
                record.source_section,
                record.source_chronicle,
                record.source_order,
                result.source.page_url,
                result.source.revision_id or "",
            ]
        )
    return buffer.getvalue()


def render_markdown(result: ImportResult, names_sha256: str = "") -> str:
    revision = result.source.revision_id if result.source.revision_id is not None else "unbekannt"
    lines = [
        f"# Herrscherliste {result.start_year}-{result.end_year}: {result.country.upper()}",
        "",
        "## Erzeugungsregeln",
        "",
        "- Sortiert nach der ersten Königserhebung.",
        "- Jede Person erscheint genau einmal.",
        "- Eine spätere zweite Amtszeit oder spätere Anerkennung erzeugt keinen neuen Eintrag.",
        "- Bei nur jahrgenauen Gleichständen gilt die Reihenfolge der Wikipedia-Tabelle.",
        "- Die Analysedatei enthält nur den für Name Patterns verwendeten Rufnamen.",
        "",
        "## Quelle",
        "",
        f"- Seite: [{result.source.page_title}]({result.source.page_url})",
        f"- Revisions-ID: `{revision}`",
        f"- Abrufzeit (UTC): `{result.source.fetched_at}`",
    ]
    if names_sha256:
        lines.append(f"- SHA-256 der Eingabedatei: `{names_sha256}`")
    lines += [
        "",
        f"## Einträge ({len(result.records)})",
        "",
        "| # | Analyse | Vollständiger Name | erste Erhebung | Rolle | spätere Rollen |",
        "|---:|---|---|---:|---|---|",
    ]
    for position, record in enumerate(result.records, start=1):
        lines.append(
            f"| {position} | {record.analysis_name} | {record.canonical_name} | "
            f"{record.elevation_year} | {record.role.german} | "
            f"{', '.join(record.later_roles) or '—'} |"
        )
    if result.warnings:
        lines += ["", "## Hinweise", ""]
        lines.extend(f"- {warning}" for warning in result.warnings)
    return "\n".join(lines) + "\n"


def export_all(result: ImportResult, output: Path) -> Dict[str, Path]:
    """Schreibt kompatible TXT-, pruefbare CSV- und lesbare Markdown-Datei."""
    output.parent.mkdir(parents=True, exist_ok=True)
    txt_path = output
    csv_path = output.with_suffix(".csv")
    report_path = output.with_name(output.stem + "_Bericht.md")

    names = render_names(result)
    output.write_text(names, encoding="utf-8")
    csv_path.write_text(render_csv(result), encoding="utf-8")
    digest = hashlib.sha256(names.encode("utf-8")).hexdigest()
    report_path.write_text(render_markdown(result, digest), encoding="utf-8")
    return {"names": txt_path, "metadata": csv_path, "report": report_path}
