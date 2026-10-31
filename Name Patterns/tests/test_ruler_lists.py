"""Tests fuer den erweiterbaren Wikipedia-Herrscherimport."""

from __future__ import annotations

import csv
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from name_patterns.data import load_name_metadata, load_names
from ruler_lists.export import export_all, render_csv, render_names
from ruler_lists.fetch import FetchError, FetchedPage, fetch_wikipedia_page
from ruler_lists.model import Role
from ruler_lists.registry import available_countries, get_adapter
from ruler_lists.sources.hrr_dewiki import CATALOG, records_from_html


PROJECT = Path(__file__).resolve().parent.parent
FIXTURE = PROJECT / "tests" / "fixtures" / "hrr_wikipedia.html"


def fixture_page() -> FetchedPage:
    return FetchedPage(
        title="Liste der römisch-deutschen Herrscher",
        revision_id=123456,
        fetched_at="2026-10-25T00:00:00+00:00",
        html=FIXTURE.read_text(encoding="utf-8"),
    )


class TestHRRParsing(unittest.TestCase):
    def test_every_catalog_entry_is_found(self):
        records, warnings = records_from_html(fixture_page().html)
        self.assertEqual(len(records), len(CATALOG))
        self.assertEqual(warnings, [])

    def test_sorting_uses_first_elevation_not_table_order(self):
        # Die Fixture spiegelt den Wikipedia-Fall: Konrad steht in der Tabelle
        # vor Rudolf und Hermann, wurde aber erst nach beiden zum Mitkoenig.
        adapter = get_adapter("hrr")
        with patch(
            "ruler_lists.sources.hrr_dewiki.fetch_wikipedia_page",
            return_value=fixture_page(),
        ):
            result = adapter.import_rulers(
                1070, 1090,
                include_counter_kings=True,
                include_co_kings=True,
                cache_dir=Path("ignored"), offline=True, refresh=False,
            )
        self.assertEqual(
            [r.canonical_name for r in result.records],
            ["Rudolf von Rheinfelden", "Hermann von Luxemburg, Graf von Salm", "Konrad (III.)"],
        )

    def test_complete_911_1313_reference_list_has_31_people(self):
        adapter = get_adapter("hrr")
        with patch(
            "ruler_lists.sources.hrr_dewiki.fetch_wikipedia_page",
            return_value=fixture_page(),
        ):
            result = adapter.import_rulers(
                911, 1313,
                include_counter_kings=True,
                include_co_kings=True,
                cache_dir=Path("ignored"), offline=True, refresh=False,
            )
        self.assertEqual(len(result.records), 31)
        self.assertEqual(result.records[0].canonical_name, "Konrad I.")
        self.assertEqual(result.records[-1].canonical_name, "Heinrich VII., Luxemburger")
        self.assertNotIn("Ludwig IV.", [r.canonical_name for r in result.records])
        self.assertEqual(len({r.person_id for r in result.records}), 31)

    def test_complete_843_1806_reference_list_has_64_people(self):
        adapter = get_adapter("hrr")
        with patch(
            "ruler_lists.sources.hrr_dewiki.fetch_wikipedia_page",
            return_value=fixture_page(),
        ):
            result = adapter.import_rulers(
                843, 1806,
                include_counter_kings=True,
                include_co_kings=True,
                cache_dir=Path("ignored"), offline=True, refresh=False,
            )
        self.assertEqual(len(result.records), 64)
        self.assertEqual(result.records[0].canonical_name, "Ludwig II. der Deutsche")
        self.assertEqual(result.records[-1].canonical_name, "Franz II.")
        self.assertEqual(len({r.person_id for r in result.records}), 64)

    def test_role_filters_are_independent(self):
        adapter = get_adapter("hrr")
        with patch(
            "ruler_lists.sources.hrr_dewiki.fetch_wikipedia_page",
            return_value=fixture_page(),
        ):
            result = adapter.import_rulers(
                911, 1313,
                include_counter_kings=False,
                include_co_kings=False,
                cache_dir=Path("ignored"), offline=True, refresh=False,
            )
        self.assertTrue(all(r.role is Role.KING for r in result.records))

    def test_changed_wikipedia_row_fails_loudly(self):
        broken = fixture_page().html.replace("Konrad I.", "Person entfernt")
        with self.assertRaisesRegex(ValueError, "Konrad I"):
            records_from_html(broken)


class TestExports(unittest.TestCase):
    def setUp(self):
        adapter = get_adapter("hrr")
        with patch(
            "ruler_lists.sources.hrr_dewiki.fetch_wikipedia_page",
            return_value=fixture_page(),
        ):
            self.result = adapter.import_rulers(
                911, 1313,
                include_counter_kings=True,
                include_co_kings=True,
                cache_dir=Path("ignored"), offline=True, refresh=False,
            )

    def test_name_export_is_directly_loadable(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "kings.txt"
            paths = export_all(self.result, output)
            names = load_names(paths["names"])
            self.assertEqual(names, [r.analysis_name for r in self.result.records])
            self.assertTrue(paths["metadata"].exists())
            self.assertTrue(paths["report"].exists())

    def test_name_export_contains_revision_metadata(self):
        text = render_names(self.result)
        self.assertIn("# Wikipedia-Revision: 123456", text)

    def test_csv_has_one_row_per_person(self):
        rows = list(csv.DictReader(io.StringIO(render_csv(self.result))))
        self.assertEqual(len(rows), 31)
        self.assertEqual(rows[0]["analysis_name"], "Konrad")
        self.assertEqual(rows[-1]["elevation_year"], "1308")

    def test_metadata_loader_reads_generated_header(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "kings.txt"
            path.write_text(render_names(self.result), encoding="utf-8")
            metadata = load_name_metadata(path)
        self.assertEqual(metadata["Wikipedia-Revision"], "123456")
        self.assertEqual(metadata["Land"], "hrr")


class TestRegistry(unittest.TestCase):
    def test_hrr_is_registered(self):
        self.assertIn(("hrr", "Ostfränkisches und Heiliges Römisches Reich"), available_countries())

    def test_unknown_country_is_clear(self):
        with self.assertRaisesRegex(ValueError, "Verfuegbar: hrr"):
            get_adapter("unbekannt")


class TestFetchCache(unittest.TestCase):
    def test_offline_cache_is_read_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            path = cache / "beispiel.json"
            path.write_text(
                '{"title":"Beispiel","revision_id":7,'
                '"fetched_at":"2026-01-01T00:00:00+00:00","html":"<p>ok</p>"}',
                encoding="utf-8",
            )
            page = fetch_wikipedia_page("Beispiel", cache, offline=True)
        self.assertTrue(page.from_cache)
        self.assertEqual(page.revision_id, 7)
        self.assertEqual(page.html, "<p>ok</p>")

    def test_offline_without_cache_is_clear(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(FetchError, "Kein Cache"):
                fetch_wikipedia_page("Fehlt", Path(directory), offline=True)


if __name__ == "__main__":
    unittest.main()
