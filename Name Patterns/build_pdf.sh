#!/bin/bash
# Erzeugt aus einem Bericht (HTML) ein PDF, indem Chrome das echte Layout druckt.
#
#   ./build_pdf.sh                    -> HRR_Bericht.html  =>  HRR_Bericht.pdf
#   ./build_pdf.sh Norwegen_Bericht   -> Norwegen_Bericht.html => .pdf
#
# Voraussetzung: Google Chrome unter /Applications.

set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
NAME="${1:-HRR_Bericht}"
NAME="${NAME%.html}"          # Endung abschneiden, falls mitgegeben
DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$DIR/$NAME.html"
OUT="$DIR/$NAME.pdf"

if [ ! -x "$CHROME" ]; then
  echo "Chrome nicht gefunden unter: $CHROME" >&2
  exit 1
fi
if [ ! -f "$SRC" ]; then
  echo "Datei nicht gefunden: $SRC" >&2
  exit 1
fi

# file:// braucht prozentkodierte Leerzeichen im Pfad ("Name Patterns").
URL="file://$(printf '%s' "$SRC" | sed 's/ /%20/g')"

# --virtual-time-budget gibt den Google-Fonts genug Zeit zum Laden; ohne das
# druckt Chrome gelegentlich mit der Ersatzschrift.
"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$OUT" --virtual-time-budget=12000 "$URL" 2>/dev/null

if command -v python3 >/dev/null && python3 -c "import pypdf" 2>/dev/null; then
  PAGES=$(python3 -c "from pypdf import PdfReader; print(len(PdfReader('$OUT').pages))")
  echo "$NAME.pdf erzeugt — $PAGES Seiten, $(du -h "$OUT" | cut -f1)"
else
  echo "$NAME.pdf erzeugt — $(du -h "$OUT" | cut -f1)"
fi
