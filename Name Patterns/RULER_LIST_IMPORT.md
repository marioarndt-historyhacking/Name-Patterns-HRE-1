# Wikipedia-Importer für Herrscherlisten

## Zweck

Der Importer erzeugt chronologisch geordnete Namenslisten für das Programm
Name Patterns. Die erste vollständig unterstützte Quelle ist die
deutschsprachige Wikipedia-Liste der römisch-deutschen Herrscher.

Der Standardaufruf erzeugt die Könige, Mitkönige und Gegenkönige des
ostfränkischen und Heiligen Römischen Reiches, deren erste Königserhebung
zwischen 911 und 1313 liegt:

```bash
python3 build_ruler_list.py \
  --country hrr \
  --start 911 \
  --end 1313 \
  --refresh \
  --output HRR_Kings_911_1313.txt
```

## Erzeugte Dateien

Aus `HRR_Kings_911_1313.txt` entstehen drei Dateien:

1. `HRR_Kings_911_1313.txt`: unmittelbare Eingabe für Name Patterns;
2. `HRR_Kings_911_1313.csv`: vollständige Namen, Erhebungsjahre, Rollen,
   Quelltext und Wikipedia-Revision zur maschinellen Prüfung;
3. `HRR_Kings_911_1313_Bericht.md`: lesbare Dokumentation der Quelle und aller
   aufgenommenen Personen.

Die Textdatei besitzt Kommentar-Metadaten. `load_names()` ignoriert diese
Kommentare wie bisher. Die Datei bleibt deshalb mit der vorhandenen Analyse
kompatibel.

## Fachliche Regeln

- Der Zeitraum bezieht sich auf das Jahr der **ersten Königserhebung**.
- Grenzen sind einschließlich: `--start 911 --end 1313` schließt beide Jahre
  ein.
- Gegenkönige und Mitkönige sind standardmäßig enthalten.
- Eine Person erscheint genau einmal.
- War eine Person zunächst Gegenkönig und später anerkannter König, bleibt sie
  bei ihrer ersten Erhebung einsortiert.
- Eine zweite Amtszeit erzeugt keinen zweiten Eintrag.
- Gibt Wikipedia nur dasselbe Jahr für zwei Personen an, entscheidet die
  Reihenfolge der Wikipedia-Tabelle. Es wird kein unbekanntes Tagesdatum
  erfunden.
- Für Name Patterns wird der Rufname exportiert; die CSV-Datei erhält den
  vollständigen Namen.

Der Zeitraum endet mit Heinrich VII., dessen Königserhebung 1308 erfolgte und
dessen Herrschaft 1313 endete. Die Doppelwahl Ludwigs des Bayern und Friedrichs
des Schönen von 1314 liegt außerhalb des gewählten Zeitraums.

## Warum die Jahreszuordnung kontrolliert ist

Die Wikipedia-Spalte „Herrschafts-Chronik“ enthält in einem einzigen Text
häufig mehrere Ämter und Jahreszahlen: Herzogtum, Mitkönigtum, Königtum,
italienisches Königtum und Kaisertum. Ein allgemeiner regulärer Ausdruck könnte
deshalb leicht ein Herzogs- oder Kaiserjahr als Königserhebung missverstehen.

Der HRR-Adapter besitzt eine transparente, getestete Zuordnung der ersten
Königserhebung zu jeder Person. Bei jedem Abruf wird diese Zuordnung gegen die
aktuelle Wikipedia-Tabelle validiert:

- Jede erwartete Person muss in der Tabelle vorkommen.
- Das zugeordnete Erhebungsjahr muss im aktuellen Chroniktext vorkommen.
- Fehlende Personen führen zu einem Fehler statt zu einer still fehlerhaften
  Liste.
- Ein fehlendes Jahr erzeugt eine sichtbare Warnung.

Damit ist die notwendige historische Interpretation überprüfbar, während
Änderungen der Wikipedia-Struktur nicht unbemerkt falsche Daten produzieren.

## Cache und Reproduzierbarkeit

Der Abruf erfolgt über die MediaWiki-API. Im Cache werden gespeichert:

- Seitentitel,
- Revisions-ID,
- UTC-Abrufzeit und
- das gerenderte HTML der Seite.

Ohne `--refresh` wird ein vorhandener Cache wiederverwendet. `--offline`
verbietet einen Netzabruf und verlangt einen vorhandenen Cache. Scheitert ein
Onlineabruf, verwendet das Programm einen vorhandenen Cache und gibt dies als
Warnung aus.

Die Revisions-ID steht in allen Exporten. Der Bericht enthält zusätzlich den
SHA-256-Hash der Textdatei. Damit lässt sich später feststellen, mit welcher
konkreten Eingabe ein Analyseergebnis erzeugt wurde.

## Eingabemetadaten in Name Patterns anzeigen

```bash
python3 -m name_patterns.cli \
  --data HRR_Kings_911_1313.txt \
  --discover \
  --show-input-metadata \
  --measure coverage \
  --significance 2000 \
  --seed 42 \
  --quiet
```

Die Option zeigt die Kommentar-Metadaten und den SHA-256-Hash vor dem
Analysebericht. Durch `--significance 2000` berechnet der Bericht zusätzlich
den Monte-Carlo-p-Wert und gibt die Signifikanzentscheidung als eigene Zeile
`Signifikant: ja` beziehungsweise `Signifikant: nein` aus. Ohne eine positive
Zahl bei `--significance` gibt es keine Zufallsverteilung und deshalb weder
p-Wert noch Signifikanzentscheidung. Alte Dateien ohne Kopfzeilen funktionieren
unverändert.

Die Namensbehandlung kann nun außerdem ausdrücklich gewählt werden:

```text
--name-mode first-token   nur Rufname; Standard
--name-mode full          vollständiger Zeileneintrag
```

`--raw-names` bleibt als kompatibler Alias für `--name-mode full` erhalten.

## Länder und Zeiträume

Verfügbare Adapter:

```bash
python3 build_ruler_list.py --list-countries
```

Ein anderer Zeitraum wird ohne Programmänderung gewählt:

```bash
python3 build_ruler_list.py \
  --country hrr --start 1000 --end 1200 \
  --output HRR_Kings_1000_1200.txt
```

Die kontrollierte HRR-Zuordnung deckt die vollständige Wikipedia-Liste von 843
bis zum Ende des Reichs 1806 ab. Sie enthält 64 Personen; das letzte
Erhebungsjahr ist 1792, da Franz II. bis zur Auflösung des HRR 1806 herrschte.
Der vollständige Referenzexport heißt `HRR_Kings_843_1806.txt`.

## Einen weiteren Länderadapter ergänzen

1. Neue Klasse unter `ruler_lists/sources/` erstellen.
2. `CountryAdapter` implementieren.
3. Wikipedia-Seite und landesspezifische Tabellenstruktur festlegen.
4. Regeln für erste Erhebung, Gegenkönige, Mitkönige und Personenidentität
   dokumentieren.
5. Adapter in `ruler_lists/registry.py` registrieren.
6. Gespeicherte HTML-Fixture und historische Referenztests ergänzen.

Die gemeinsame Infrastruktur für Cache, Zeitraumfilter, Rollenfilter,
Deduplizierung und Exporte muss dabei nicht neu geschrieben werden.

## Tests

```bash
python3 -m unittest discover -s tests -t .
```

Die Importtests verwenden eine lokale HTML-Fixture und benötigen kein Netzwerk.
Sie prüfen unter anderem:

- alle 31 Referenzpersonen von 911 bis 1313,
- chronologische Sortierung statt bloßer Tabellenreihenfolge,
- Rollenfilter,
- eindeutige Personenkennungen,
- Reaktion auf geänderte Wikipedia-Zeilen,
- TXT-, CSV- und Markdown-Export,
- direkte Lesbarkeit durch `load_names()` und
- Metadatenextraktion.
