"""Adapter fuer die deutschsprachige Wikipedia-Liste der HRR-Herrscher.

Die Wikipedia-Tabelle ist fuer Menschen geschrieben; die Herrschaftschronik
vermischt Herzogs-, Koenigs- und Kaiserjahre.  Der Adapter verwendet deshalb
eine versionierte, fachlich kontrollierbare Zuordnung der ersten
Koenigserhebung und validiert jeden Eintrag gegen die live abgerufene Tabelle.
So werden Jahreszahlen nicht versehentlich aus einem anderen Amt herausgelesen.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from ..fetch import fetch_wikipedia_page
from ..html_tables import Row, parse_rows
from ..model import ImportResult, Role, RulerRecord, SourceInfo
from .base import CountryAdapter


@dataclass(frozen=True)
class CatalogEntry:
    person_id: str
    names: Tuple[str, ...]
    analysis_name: str
    elevation_year: int
    role: Role
    later_roles: Tuple[str, ...] = ()


# Kontrollierte Interpretation der Wikipedia-Herrschaftschronik.  Die Reihenfolge
# hier ist nicht die Ergebnisreihenfolge; sortiert wird nach Erhebungsjahr und
# anschliessend nach der Reihenfolge der Zeilen in der Wikipedia-Tabelle.
CATALOG: Tuple[CatalogEntry, ...] = (
    CatalogEntry("ludwig-ii-deutsche", ("Ludwig II. der Deutsche",), "Ludwig", 843, Role.KING),
    CatalogEntry("karlmann-ostfranken", ("Karlmann",), "Karlmann", 876, Role.KING),
    CatalogEntry("ludwig-iii-juengere", ("Ludwig III. der Jüngere",), "Ludwig", 876, Role.KING),
    CatalogEntry("karl-iii-dicke", ("Karl III. der Dicke",), "Karl", 876, Role.KING, ("Kaiser",)),
    CatalogEntry("arnolf-kaernten", ("Arnolf von Kärnten",), "Arnolf", 887, Role.KING, ("Kaiser",)),
    CatalogEntry("ludwig-iv-kind", ("Ludwig IV. das Kind",), "Ludwig", 900, Role.KING),
    CatalogEntry("konrad-i", ("Konrad I.",), "Konrad", 911, Role.KING),
    CatalogEntry("heinrich-i", ("Heinrich I.",), "Heinrich", 919, Role.KING),
    CatalogEntry("otto-i", ("Otto I. der Große",), "Otto", 936, Role.KING),
    CatalogEntry("otto-ii", ("Otto II.",), "Otto", 961, Role.CO_KING, ("König", "Kaiser")),
    CatalogEntry("otto-iii", ("Otto III.",), "Otto", 983, Role.KING, ("Kaiser",)),
    CatalogEntry("heinrich-ii", ("Heinrich II.",), "Heinrich", 1002, Role.KING),
    CatalogEntry("konrad-ii", ("Konrad II.",), "Konrad", 1024, Role.KING),
    CatalogEntry("heinrich-iii", ("Heinrich III.",), "Heinrich", 1028, Role.CO_KING, ("König", "Kaiser")),
    CatalogEntry("heinrich-iv", ("Heinrich IV.",), "Heinrich", 1056, Role.KING),
    CatalogEntry("rudolf-rheinfelden", ("Rudolf von Rheinfelden",), "Rudolf", 1077, Role.COUNTER_KING),
    CatalogEntry("hermann-salm", ("Hermann von Luxemburg, Graf von Salm", "Hermann von Salm"), "Hermann", 1081, Role.COUNTER_KING),
    CatalogEntry("konrad-sohn-heinrich-iv", ("Konrad (III.)",), "Konrad", 1087, Role.CO_KING, ("Gegenkönig",)),
    CatalogEntry("heinrich-v", ("Heinrich V.",), "Heinrich", 1099, Role.CO_KING, ("König", "Kaiser")),
    CatalogEntry("lothar-iii", ("Lothar III.",), "Lothar", 1125, Role.KING),
    CatalogEntry("konrad-iii", ("Konrad III.",), "Konrad", 1127, Role.COUNTER_KING, ("König",)),
    CatalogEntry("heinrich-sohn-konrad-iii", ("Heinrich (VI.)",), "Heinrich", 1147, Role.CO_KING),
    CatalogEntry("friedrich-i", ("Friedrich I. Barbarossa",), "Friedrich", 1152, Role.KING),
    CatalogEntry("heinrich-vi", ("Heinrich VI.",), "Heinrich", 1169, Role.CO_KING, ("König", "Kaiser")),
    CatalogEntry("philipp-schwaben", ("Philipp von Schwaben",), "Philipp", 1198, Role.KING),
    CatalogEntry("otto-iv", ("Otto IV. von Braunschweig",), "Otto", 1198, Role.KING),
    CatalogEntry("friedrich-ii", ("Friedrich II.",), "Friedrich", 1212, Role.COUNTER_KING, ("König", "Kaiser")),
    CatalogEntry("heinrich-vii", ("Heinrich (VII.)",), "Heinrich", 1220, Role.CO_KING),
    CatalogEntry("konrad-iv", ("Konrad IV.",), "Konrad", 1237, Role.CO_KING, ("König",)),
    CatalogEntry("heinrich-raspe", ("Heinrich Raspe",), "Heinrich", 1246, Role.COUNTER_KING),
    CatalogEntry("wilhelm-holland", ("Wilhelm von Holland",), "Wilhelm", 1248, Role.COUNTER_KING, ("König",)),
    CatalogEntry("richard-cornwall", ("Richard von Cornwall",), "Richard", 1257, Role.KING),
    CatalogEntry("alfons-kastilien", ("Alfons von Kastilien",), "Alfons", 1257, Role.COUNTER_KING),
    CatalogEntry("rudolf-i", ("Rudolf I. von Habsburg",), "Rudolf", 1273, Role.KING),
    CatalogEntry("adolf-nassau", ("Adolf von Nassau",), "Adolf", 1292, Role.KING),
    CatalogEntry("albrecht-i", ("Albrecht I. von Habsburg",), "Albrecht", 1298, Role.COUNTER_KING, ("König",)),
    CatalogEntry("heinrich-vii-lux", ("Heinrich VII., Luxemburger", "Heinrich VII."), "Heinrich", 1308, Role.KING),
    CatalogEntry("ludwig-iv-bayer", ("Ludwig IV., der Bayer, Wittelsbacher",), "Ludwig", 1314, Role.KING, ("Kaiser",)),
    CatalogEntry("friedrich-schoene", ("Friedrich der Schöne, Habsburger",), "Friedrich", 1314, Role.COUNTER_KING),
    CatalogEntry("karl-iv", ("Karl IV. von Luxemburg",), "Karl", 1346, Role.COUNTER_KING, ("König", "Kaiser")),
    CatalogEntry("guenther-schwarzburg", ("Günther von Schwarzburg",), "Günther", 1349, Role.COUNTER_KING),
    CatalogEntry("wenzel-luxemburg", ("Wenzel von Luxemburg",), "Wenzel", 1376, Role.CO_KING, ("König",)),
    CatalogEntry("ruprecht-pfalz", ("Ruprecht von der Pfalz, Wittelsbacher",), "Ruprecht", 1400, Role.KING),
    CatalogEntry("jobst-maehren", ("Jobst von Mähren, Luxemburger",), "Jobst", 1410, Role.KING),
    CatalogEntry("sigismund-luxemburg", ("Sigismund von Luxemburg",), "Sigismund", 1411, Role.KING, ("Kaiser",)),
    CatalogEntry("albrecht-ii", ("Albrecht II.",), "Albrecht", 1438, Role.KING),
    CatalogEntry("friedrich-iii", ("Friedrich III.",), "Friedrich", 1440, Role.KING, ("Kaiser",)),
    CatalogEntry("maximilian-i", ("Maximilian I.",), "Maximilian", 1486, Role.CO_KING, ("König", "Kaiser")),
    CatalogEntry("karl-v", ("Karl V.",), "Karl", 1519, Role.KING, ("Kaiser",)),
    CatalogEntry("ferdinand-i", ("Ferdinand I.",), "Ferdinand", 1531, Role.CO_KING, ("König", "Kaiser")),
    CatalogEntry("maximilian-ii", ("Maximilian II.",), "Maximilian", 1562, Role.CO_KING, ("König", "Kaiser")),
    CatalogEntry("rudolf-ii", ("Rudolf II.",), "Rudolf", 1575, Role.CO_KING, ("König", "Kaiser")),
    CatalogEntry("matthias-habsburg", ("Matthias",), "Matthias", 1612, Role.KING, ("Kaiser",)),
    CatalogEntry("ferdinand-ii", ("Ferdinand II.",), "Ferdinand", 1619, Role.KING, ("Kaiser",)),
    CatalogEntry("ferdinand-iii", ("Ferdinand III.",), "Ferdinand", 1636, Role.CO_KING, ("König", "Kaiser")),
    CatalogEntry("ferdinand-iv", ("Ferdinand IV.",), "Ferdinand", 1653, Role.CO_KING),
    CatalogEntry("leopold-i", ("Leopold I.",), "Leopold", 1658, Role.KING, ("Kaiser",)),
    CatalogEntry("joseph-i", ("Joseph I.",), "Joseph", 1690, Role.CO_KING, ("König", "Kaiser")),
    CatalogEntry("karl-vi", ("Karl VI.",), "Karl", 1711, Role.KING, ("Kaiser",)),
    CatalogEntry("karl-vii", ("Karl VII.",), "Karl", 1742, Role.KING, ("Kaiser",)),
    CatalogEntry("franz-i", ("Franz I.",), "Franz", 1745, Role.KING, ("Kaiser",)),
    CatalogEntry("joseph-ii", ("Joseph II.",), "Joseph", 1764, Role.CO_KING, ("Kaiser",)),
    CatalogEntry("leopold-ii", ("Leopold II.",), "Leopold", 1790, Role.KING, ("Kaiser",)),
    CatalogEntry("franz-ii", ("Franz II.",), "Franz", 1792, Role.KING, ("Kaiser",)),
)


def _row_name(row: Row) -> Optional[str]:
    if len(row.cells) < 2:
        return None
    candidate = row.cells[1].text.strip()
    return candidate or None


def records_from_html(html: str) -> Tuple[List[RulerRecord], List[str]]:
    """Validiert den kontrollierten Katalog gegen die aktuelle Wikipedia-Tabelle."""
    rows = parse_rows(html)
    name_rows: Dict[str, Tuple[int, Row]] = {}
    for order, row in enumerate(rows):
        name = _row_name(row)
        if name:
            name_rows.setdefault(name, (order, row))

    records: List[RulerRecord] = []
    warnings: List[str] = []
    for fallback_order, entry in enumerate(CATALOG):
        match: Optional[Tuple[int, Row]] = None
        matched_name = ""
        for name in entry.names:
            if name in name_rows:
                match = name_rows[name]
                matched_name = name
                break
        if match is None:
            expected = " / ".join(entry.names)
            raise ValueError(
                f"Wikipedia-Format oder Inhalt geaendert: Zeile fuer '{expected}' fehlt"
            )
        source_order, row = match
        chronicle = row.cells[2].text if len(row.cells) > 2 else ""
        if str(entry.elevation_year) not in chronicle:
            warnings.append(
                f"{matched_name}: Erhebungsjahr {entry.elevation_year} "
                "kommt in der aktuellen Herrschaftschronik nicht vor"
            )
        records.append(
            RulerRecord(
                person_id=entry.person_id,
                canonical_name=matched_name,
                analysis_name=entry.analysis_name,
                country="hrr",
                elevation_year=entry.elevation_year,
                role=entry.role,
                source_order=source_order,
                source_chronicle=chronicle,
                source_section=row.section,
                later_roles=entry.later_roles,
            )
        )
    return records, warnings


class HRRAdapter(CountryAdapter):
    code = "hrr"
    label = "Ostfränkisches und Heiliges Römisches Reich"
    source_title = "Liste der römisch-deutschen Herrscher"
    source_url = "https://de.wikipedia.org/wiki/Liste_der_r%C3%B6misch-deutschen_Herrscher"

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
        if start_year > end_year:
            raise ValueError("Startjahr darf nicht nach dem Endjahr liegen")
        page = fetch_wikipedia_page(
            self.source_title, cache_dir, offline=offline, refresh=refresh
        )
        records, warnings = records_from_html(page.html)
        selected = [
            record
            for record in records
            if start_year <= record.elevation_year <= end_year
            and (include_counter_kings or record.role is not Role.COUNTER_KING)
            and (include_co_kings or record.role is not Role.CO_KING)
        ]
        selected.sort(key=lambda record: (record.elevation_year, record.source_order))
        if page.from_cache:
            warnings.append("Wikipedia-Seite wurde aus dem lokalen Cache gelesen")
        result = ImportResult(
            country=self.code,
            start_year=start_year,
            end_year=end_year,
            records=selected,
            source=SourceInfo(
                page_title=page.title,
                page_url=self.source_url,
                revision_id=page.revision_id,
                fetched_at=page.fetched_at,
            ),
            warnings=warnings,
        )
        result.validate()
        return result
