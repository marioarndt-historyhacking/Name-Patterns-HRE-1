"""Tests fuer Laden und Normalisieren der Namenslisten."""

from __future__ import annotations

import unittest
from pathlib import Path

from name_patterns.data import (
    HRR_KINGS,
    given_name,
    load_names,
    normalize,
    strip_ordinal,
)

PROJECT = Path(__file__).resolve().parent.parent


class TestStripOrdinal(unittest.TestCase):
    def test_space_separated_ordinal(self):
        self.assertEqual(strip_ordinal("Olav III."), "Olav")

    def test_ordinal_attached_without_space(self):
        """Beide Schreibweisen muessen greifen -- die Quelldatei hatte erst diese."""
        self.assertEqual(strip_ordinal("OlavIII."), "Olav")

    def test_ordinal_without_trailing_dot(self):
        self.assertEqual(strip_ordinal("Ludwig XIV"), "Ludwig")

    def test_name_without_ordinal_is_untouched(self):
        for name in ("Olav", "Sverre", "Jon", "Inge", "Öystein"):
            self.assertEqual(strip_ordinal(name), name)

    def test_lowercase_endings_are_not_mistaken_for_numerals(self):
        """Vornamen enden klein -- die Regel kann ihnen nichts abschneiden."""
        for name in ("Olav", "Ivan", "Vladimir", "Otto", "Heinrich"):
            self.assertEqual(strip_ordinal(name), name)

    def test_surrounding_whitespace_is_removed(self):
        self.assertEqual(strip_ordinal("  Inge  "), "Inge")

    def test_bare_numeral_is_kept_rather_than_emptied(self):
        self.assertEqual(strip_ordinal("III."), "III.")


class TestGivenName(unittest.TestCase):
    """Nur der Teil bis zum ersten Leerzeichen zaehlt."""

    def test_epithet_is_dropped(self):
        self.assertEqual(given_name("Friedrich Barbarossa"), "Friedrich")

    def test_patronymic_is_dropped(self):
        self.assertEqual(given_name("Guttorm Sigurdsson"), "Guttorm")

    def test_ordinal_and_epithet_together(self):
        self.assertEqual(given_name("Inge II. Bardsson"), "Inge")

    def test_plain_ordinal(self):
        self.assertEqual(given_name("Olav III."), "Olav")

    def test_attached_ordinal_still_handled(self):
        """Fallback fuer die alte Schreibweise ohne Leerzeichen."""
        self.assertEqual(given_name("OlavIII."), "Olav")

    def test_single_name_is_untouched(self):
        for name in ("Sverre", "Jon", "Öystein"):
            self.assertEqual(given_name(name), name)

    def test_empty_entry_is_safe(self):
        self.assertEqual(given_name("   "), "")


class TestNormalize(unittest.TestCase):
    def test_reports_how_many_entries_changed(self):
        cleaned, changed = normalize(["Olav I.", "Sverre", "Hakon II."])
        self.assertEqual(cleaned, ["Olav", "Sverre", "Hakon"])
        self.assertEqual(changed, 2)

    def test_counts_epithets_too(self):
        cleaned, changed = normalize(["Friedrich Barbarossa", "Otto"])
        self.assertEqual(cleaned, ["Friedrich", "Otto"])
        self.assertEqual(changed, 1)

    def test_nothing_to_do(self):
        cleaned, changed = normalize(["Konrad", "Heinrich"])
        self.assertEqual(cleaned, ["Konrad", "Heinrich"])
        self.assertEqual(changed, 0)


class TestLoadNames(unittest.TestCase):
    def setUp(self):
        self.norway = PROJECT / "Norway_Kings.txt"
        self.hrr = PROJECT / "HRR_Kings.txt"

    def test_hrr_file_matches_the_builtin_list(self):
        """Faengt ein Auseinanderlaufen von Datei und eingebauter Liste ab."""
        self.assertEqual(load_names(self.hrr), HRR_KINGS)

    def test_norway_file_starts_with_the_source_table(self):
        """Der Anfang der Liste ist stabil, auch wenn sie hinten waechst."""
        self.assertEqual(
            load_names(self.norway)[:23],
            [
                "Olav", "Olav", "Knut", "Magnus", "Harald", "Magnus", "Olav",
                "Magnus", "Olav",
                "Öystein", "Sigurd", "Magnus", "Harald", "Sigurd", "Inge",
                "Öystein",
                "Hakon", "Magnus", "Öystein", "Sverre", "Jon", "Inge", "Hakon",
            ],
        )

    def test_every_loaded_entry_is_a_bare_given_name(self):
        """Strukturelle Invariante -- gilt, wie weit die Liste auch waechst."""
        for name in load_names(self.norway):
            self.assertEqual(name, name.strip())
            self.assertNotIn(" ", name)
            self.assertFalse(name.endswith("."))

    def test_normalization_is_on_by_default(self):
        self.assertNotIn("Olav I.", load_names(self.norway))

    def test_raw_loading_is_possible(self):
        raw = load_names(self.norway, normalize_names=False)
        self.assertIn("Olav I.", raw)
        self.assertEqual(len(raw), len(load_names(self.norway)))

    def test_trailing_whitespace_in_the_file_is_stripped(self):
        """Zeile 15 der Quelldatei traegt ein Leerzeichen am Ende."""
        raw = load_names(self.norway, normalize_names=False)
        self.assertIn("Inge", raw)
        self.assertNotIn("Inge ", raw)

    def test_comments_and_blank_lines_are_ignored(self):
        path = PROJECT / "tests" / "_tmp_names.txt"
        path.write_text("# Kommentar\nOlav I.\n\n  \nHakon II.  # nachgestellt\n")
        try:
            self.assertEqual(load_names(path), ["Olav", "Hakon"])
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
