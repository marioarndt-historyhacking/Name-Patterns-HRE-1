"""Beispieldaten, Loader und Normalisierung von Namenslisten."""

from __future__ import annotations

import re
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple

#: Ordnungszahl am Ende eines Eintrags: roemische Ziffern, optional mit Punkt.
#: Deckt beide Schreibweisen ab -- ``Olav I.`` ebenso wie ``OlavI.``.
#: Die Ziffern muessen grossgeschrieben sein; da Vornamen auf Kleinbuchstaben
#: enden, kann die Regel keinem echten Namen etwas abschneiden.
ORDINAL = re.compile(r"\s*[IVXLCDM]+\.?\s*$")

#: Roemisch-deutsche Koenige/Kaiser, Konrad I. bis Heinrich VII.
#: Spiegelt ``HRR_Kings.txt`` und dient als Default, wenn ``--data`` fehlt.
HRR_KINGS: List[str] = [
    "Konrad", "Heinrich", "Otto", "Otto", "Otto", "Heinrich",

    "Konrad", "Heinrich",
    "Heinrich", "Rudolf", "Hermann", "Konrad",
    "Heinrich",

    "Lothar",

    "Konrad", "Heinrich",
    "Friedrich", "Heinrich", "Philipp", "Otto", "Friedrich",
    "Heinrich",

    "Konrad", "Heinrich",
    "Wilhelm", "Richard", "Alfons", "Rudolf", "Adolf", "Albrecht",
    "Heinrich",
]


def strip_ordinal(name: str) -> str:
    """Entfernt eine angehaengte Ordnungszahl: ``Olav III.`` -> ``Olav``.

    Namen ohne Ordnungszahl bleiben unveraendert.  Bestuende ein Eintrag nur
    aus einer Ordnungszahl, bliebe er ebenfalls stehen -- lieber ein
    unerwarteter Name als ein leerer.
    """
    stripped = ORDINAL.sub("", name).strip()
    return stripped or name.strip()


def given_name(entry: str) -> str:
    """Der Rufname eines Eintrags: alles bis zum ersten Leerzeichen.

    Diese eine Regel erledigt beide Faelle:

    * Ordnungszahlen  -- ``Olav III.``          -> ``Olav``
    * Beinamen        -- ``Friedrich Barbarossa`` -> ``Friedrich``
    * beides zugleich -- ``Inge II. Bardsson``  -> ``Inge``

    Anschliessend laeuft noch :func:`strip_ordinal` ueber den Token.  Das
    greift nur, wenn die Ordnungszahl ohne Leerzeichen anhaengt (``OlavIII.``)
    -- bei sauber getrennten Eintraegen aendert es nichts.
    """
    parts = entry.split()
    if not parts:
        return entry.strip()
    return strip_ordinal(parts[0])


def normalize(names: List[str]) -> Tuple[List[str], int]:
    """Normalisiert eine Liste und meldet, wie viele Eintraege sich geaendert haben.

    Die Zahl wandert in die Ausgabe: eine stille Veraenderung der Eingabe waere
    genau die Art Detail, die spaeter Verwirrung stiftet.
    """
    cleaned = [given_name(name) for name in names]
    changed = sum(1 for before, after in zip(names, cleaned) if before != after)
    return cleaned, changed


def load_names(path: str | Path, normalize_names: bool = True) -> List[str]:
    """Liest eine Namensliste: ein Eintrag pro Zeile, ``#`` leitet Kommentare ein.

    Per Default zaehlt nur der Rufname -- sonst waeren ``Olav I.`` und
    ``Olav III.`` verschiedene Namen und keine Klammer wuerde greifen.
    """
    names: List[str] = []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            names.append(line)
    return normalize(names)[0] if normalize_names else names


def load_name_metadata(path: str | Path) -> Dict[str, str]:
    """Liest ``# Schluessel: Wert``-Kopfzeilen einer Namensdatei.

    Freie Kommentare ohne Doppelpunkt bleiben unberuecksichtigt.  Die normale
    Mustersuche funktioniert weiterhin mit alten Dateien ohne Metadaten.
    """
    metadata: Dict[str, str] = {}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if not stripped.startswith("#"):
            if stripped:
                break
            continue
        comment = stripped[1:].strip()
        if ":" in comment:
            key, value = comment.split(":", 1)
            metadata[key.strip()] = value.strip()
    return metadata


def name_file_sha256(path: str | Path) -> str:
    """SHA-256 der unveraenderten Eingabedatei fuer reproduzierbare Berichte."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
