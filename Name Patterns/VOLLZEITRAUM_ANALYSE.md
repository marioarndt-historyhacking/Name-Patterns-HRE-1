# Analyse des Namensmusters über die vollständige HRR-Herrscherliste

## 1. Fragestellung

Diese Analyse prüft, ob das bereits bekannte Namensmuster

```text
Konrad, Heinrich, ... , Heinrich
```

in der vollständigen Folge der Könige und Gegenkönige des ostfränkischen und
Heiligen Römischen Reiches von 843 bis 1806 einen auffälligen zusammenhängenden
Abschnitt bildet. Anfang und Ende dieses Abschnitts werden dem Programm **nicht**
vorgegeben. Das Programm muss sie aus der gesamten Liste auswählen.

Die Analyse ist damit strenger als eine Prüfung nur der Jahre 911 bis 1313:
Ein zufälliges Muster könnte grundsätzlich an jeder Stelle der Gesamtliste
liegen. Diese zusätzliche Auswahlmöglichkeit wird im Permutationstest
berücksichtigt.

## 2. Datengrundlage

Die Datei `HRR_Kings_843_1806.txt` enthält 64 Personen in der Reihenfolge ihrer
ersten Erhebung. Grundlage ist die deutschsprachige Wikipedia-Liste der
Herrscher des ostfränkischen und Heiligen Römischen Reiches.

Dabei gelten folgende Regeln:

- Die Liste beginnt 843 nach der Teilung von Verdun.
- Könige, Gegenkönige und Mitkönige werden berücksichtigt.
- Eine Person mit mehreren Amtszeiten erscheint nur bei ihrer ersten Erhebung.
- Die Liste endet mit Franz II. Seine Erhebung war 1792; das Reich endete 1806.
- Für die Mustersuche wird nur der vereinheitlichte Rufname verwendet. Zusätze
  und Ordnungszahlen bleiben in der CSV-Datei zur Kontrolle erhalten.

Die Datei `HRR_Kings_843_1806.csv` enthält zusätzlich Erhebungsjahr, Rolle,
vollständige Bezeichnung und Quellenangaben. Der Bericht
`HRR_Kings_843_1806_Bericht.md` dokumentiert den Import.

## 3. Gesuchtes Kettenmuster

Ein Block beginnt mit den beiden Namen `Konrad, Heinrich` und endet mit einem
weiteren `Heinrich`. Dazwischen dürfen `x` andere Listeneinträge stehen. Mehrere
Blöcke bilden eine Kette, wenn sich `x` regelmäßig entwickelt:

```text
x(j) = x0 + j * d
```

`j` bezeichnet die Nummer des Blocks, `x0` die anfängliche Zahl der
Zwischeneinträge und `d` die Schrittweite. In der Referenzanalyse sind
`d = 0` und `d = 1` zugelassen. Mindestens drei Blöcke sind erforderlich;
Abweichungen werden nicht zugelassen.

Das Programm findet als beste Kette vier Blöcke mit

```text
x = 3, 4, 5, 6.
```

## 4. Automatische Wahl des Zeitabschnitts

Für jede zulässige Kette wird als Abschnitt die Position vom Beginn des ersten
bis zum Ende des letzten Blocks verwendet. Die Bewertung lautet:

```text
Scan-Score = abgedeckte Positionen
             * lokale Abdeckung
             * Abweichungsfaktor
```

Die lokale Abdeckung ist der Anteil der Positionen innerhalb des Abschnitts,
die zu einem gefundenen Block gehören. Der Abweichungsfaktor stammt aus der
bereits vorhandenen Kettenbewertung und bestraft zugelassene Abweichungen.

Die beste gefundene Kette liegt bei den Listenindizes 6 bis 36. Laut den
Erhebungsjahren in der CSV-Datei entspricht dies **911 bis 1308**. Das Ende 1308
ist das Erhebungsjahr Heinrichs VII.; die frühere manuelle Betrachtung bis 1313
schloss zusätzlich dessen späteres Todesjahr ein.

Die vier Blöcke sind:

| Block | Listenindex | Zahl der Zwischeneinträge |
|---:|---:|---:|
| 1 | 6–11 | 3 |
| 2 | 12–18 | 4 |
| 3 | 20–27 | 5 |
| 4 | 28–36 | 6 |

30 der 31 Positionen des automatisch gefundenen Abschnitts werden abgedeckt.
Die lokale Abdeckung beträgt damit rund 97 Prozent. Der Scan-Score ist 29,0323.

## 5. Globaler Monte-Carlo-Permutationstest

Beim Permutationstest bleiben alle 64 Namen und damit auch ihre Häufigkeiten
unverändert. Nur ihre Reihenfolge wird zufällig vertauscht. Anschließend wird
auf jeder zufälligen Liste die **vollständige Suche erneut ausgeführt**. Das
Zufallsverfahren darf also ebenfalls den günstigsten Anfang, das günstigste
Ende, `x0` und die Schrittweite wählen.

Der globale p-Wert wird mit der üblichen Plus-eins-Korrektur berechnet:

```text
p = (Zahl der Zufallsscores mindestens so groß wie der beobachtete Score + 1)
    / (Zahl der Permutationen + 1)
```

Verwendet wurden 10.000 Permutationen und der feste Zufallsstartwert 42. Die
Plus-eins-Korrektur verhindert einen irreführenden p-Wert von exakt null. Bei
10.000 Wiederholungen ist 1/10.001 = 0,00009999 der kleinste berichtbare Wert.

## 6. Ergebnis A: Das Namensmotiv gilt als vorher festgelegt

Wenn ausschließlich das konkrete Motiv `Konrad, Heinrich, ... , Heinrich`
geprüft wird, erreicht keine der 10.000 zufälligen Reihenfolgen den beobachteten
Score. Mit der Plus-eins-Korrektur ergibt sich:

```text
p = 0,0001
signifikant bei alpha = 0,05: ja
```

Dies ist starke Evidenz gegen eine rein zufällige Anordnung **unter der
Voraussetzung, dass genau dieses Motiv unabhängig von der untersuchten Liste
vorab festgelegt war**. Der p-Wert berücksichtigt bereits, dass der günstigste
Zeitabschnitt der Gesamtliste ausgewählt wurde.

## 7. Ergebnis B: Das Namensmotiv wurde in denselben Daten entdeckt

Historisch wurde das konkrete Motiv durch Betrachtung dieser Herrscherfolge
gefunden. Deshalb ist eine zweite, strengere Rechnung notwendig. In ihr darf
jede Zufallspermutation nicht nur den besten Zeitraum, sondern zusätzlich ihr
eigenes bestes Anchor/Echo-Namensmotiv aus der implementierten festen
Motivfamilie auswählen.

Diese Rechnung ergibt:

```text
p = 0,0749
signifikant bei alpha = 0,05: nein
```

Der beobachtete Befund ist damit weiterhin ungewöhnlich, überschreitet nach
dieser Korrektur aber die übliche Signifikanzschwelle von 0,05. Anders gesagt:
Unter dem verwendeten Nullmodell erzeugten ungefähr 7,5 Prozent der zufälligen
Listen nach umfassender Suche einen mindestens ebenso hohen Bestwert.

## 8. Warum beide p-Werte richtig sein können

Die Werte beantworten unterschiedliche Fragen:

- `p = 0,0001`: Wie selten ist dieses **vorher festgelegte** Konrad-Heinrich-
  Motiv, wenn nur sein bester Zeitraum frei gewählt wird?
- `p = 0,0749`: Wie selten ist der Befund, wenn auch das untersuchte
  Namensmotiv erst nach Durchsicht derselben Daten ausgewählt werden durfte?

Der erste Wert darf deshalb nicht ohne Hinweis auf die nachträgliche
Motivauswahl als abschließender Beweis verwendet werden. Für eine
konfirmatorische Untersuchung wäre eine unabhängig vorab festgelegte Regel
oder eine unabhängige Herrscherliste nötig. Für die gegenwärtige explorative
Analyse ist `p = 0,0749` die vorsichtigere Hauptbewertung.

## 9. Reproduktion

Festes Motiv:

```bash
python3 -m name_patterns.cli \
  --data HRR_Kings_843_1806.txt \
  --timeline-metadata HRR_Kings_843_1806.csv \
  --scan-intervals --family fixed \
  --anchor Konrad,Heinrich --echo Heinrich \
  --d 0,1 --min-blocks 3 --max-deviations 0 \
  --significance 10000 --seed 42 --quiet \
  --report-output HRR_843_1806_Intervalltest_Festes_Motiv.txt
```

Motiv- und Intervallsuche:

```bash
python3 -m name_patterns.cli \
  --data HRR_Kings_843_1806.txt \
  --timeline-metadata HRR_Kings_843_1806.csv \
  --scan-intervals --discover --family fixed \
  --d 0,1 --min-blocks 3 --max-deviations 0 \
  --significance 10000 --seed 42 --quiet \
  --report-output HRR_843_1806_Intervalltest_Discovery.txt
```

## 10. Abgrenzung des jetzigen Ausbaustands

Noch nicht Bestandteil dieses Tests sind die zeitliche Konzentration einzelner
Namen, die 113-Jahres-Abstände, unterschiedliche mittelalterliche Jahresanfänge,
Todesjahre, dynastische Abhängigkeiten oder der Vergleich mit anderen Ländern.
Diese Aspekte können später als zusätzliche, vorher klar definierte Kennzahlen
und Nullmodelle ergänzt werden. Sie sollten nicht nachträglich in denselben
p-Wert eingerechnet werden, ohne die dadurch entstehenden zusätzlichen
Auswahlmöglichkeiten ebenfalls in jeder Permutation zu wiederholen.
