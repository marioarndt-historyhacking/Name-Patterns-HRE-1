"""Kleiner HTML-Tabellenparser ohne externe Abhaengigkeiten."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from html import unescape
from html.parser import HTMLParser
from typing import Dict, List, Optional


@dataclass
class Cell:
    text: str = ""
    links: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class Row:
    cells: List[Cell]
    section: str = ""


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(value)).strip()


class WikiTableParser(HTMLParser):
    """Extrahiert Ueberschriften und Zeilen aus MediaWiki-Tabellen."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: List[Row] = []
        self._table_depth = 0
        self._row: Optional[List[Cell]] = None
        self._cell_parts: Optional[List[str]] = None
        self._cell_links: List[Dict[str, str]] = []
        self._heading_parts: Optional[List[str]] = None
        self._section = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "table":
            self._table_depth += 1
        elif tag in ("h2", "h3") and self._table_depth == 0:
            self._heading_parts = []
        elif tag == "tr" and self._table_depth:
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell_parts = []
            self._cell_links = []
        elif tag == "a" and self._cell_parts is not None:
            self._cell_links.append(
                {key: value for key, value in attrs_dict.items() if key in ("href", "title")}
            )
        elif tag == "br" and self._cell_parts is not None:
            self._cell_parts.append(" ")

    def handle_data(self, data):
        if self._cell_parts is not None:
            self._cell_parts.append(data)
        if self._heading_parts is not None:
            self._heading_parts.append(data)

    def handle_endtag(self, tag):
        if tag in ("h2", "h3") and self._heading_parts is not None:
            self._section = clean_text("".join(self._heading_parts)).replace("[Bearbeiten]", "")
            self._heading_parts = None
        elif tag in ("td", "th") and self._cell_parts is not None:
            assert self._row is not None
            self._row.append(
                Cell(clean_text("".join(self._cell_parts)), list(self._cell_links))
            )
            self._cell_parts = None
            self._cell_links = []
        elif tag == "tr" and self._row is not None:
            if self._row:
                self.rows.append(Row(self._row, self._section))
            self._row = None
        elif tag == "table" and self._table_depth:
            self._table_depth -= 1


def parse_rows(html: str) -> List[Row]:
    parser = WikiTableParser()
    parser.feed(html)
    return parser.rows
