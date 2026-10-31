# Getrennte PAIR_ECHO-Analyse unter Einschluss Ferdinands IV.

## Fragestellung

Diese Analyse setzt nach Friedrich III. die vollständige Königsliste fort und
schließt Ferdinand IV. ein. Anders als in der reinen Kaiserfolge wird somit
kein Herrscher wegen des fehlenden Kaisertitels entfernt.

Die Blockregel lautet weiterhin:

```text
X, Y, [n Namen], Y
```

Die ersten sieben Blöcke besitzen `n = 1,2,3,4,5,6,7`. Durch Ferdinand IV.
enthält der achte Block neun statt acht Füllnamen:

```text
n = 1, 2, 3, 4, 5, 6, 7, 9.
```

Die Abweichung wird als einmaliges Überspringen des Sollwerts `n = 8`
formalisiert. Im Signifikanztest darf jede Zufallspermutation ebenfalls einmal
an beliebiger Stelle einen `n`-Wert überspringen.

## Beobachtete Liste

Die Liste enthält 62 Positionen. `Karlmann` wird wie in den anderen
PAIR_ECHO-Analysen regelgebunden als `Karl` behandelt.

| Block | Index | X | Y | n | Blocklänge |
|---:|---:|---|---|---:|---:|
| 1 | 0–3 | Karl | Ludwig | 1 | 4 |
| 2 | 4–8 | Karl | Ludwig | 2 | 5 |
| 3 | 9–14 | Konrad | Heinrich | 3 | 6 |
| 4 | 15–21 | Konrad | Heinrich | 4 | 7 |
| 5 | 23–30 | Konrad | Heinrich | 5 | 8 |
| 6 | 31–39 | Konrad | Heinrich | 6 | 9 |
| 7 | 40–49 | Ludwig | Friedrich | 7 | 10 |
| 8 | 50–61 | Maximilian | Karl | 9 | 12 |

Lothar III. bleibt die einzige Position außerhalb der Blöcke:

```text
Abdeckung = 61 / 62 ≈ 98,39 %
Scan-Score = 61 × 61 / 62 ≈ 60,016129
```

## Nullmodell

In jeder Zufallspermutation bleiben alle Namen und ihre Häufigkeiten erhalten;
nur die Reihenfolge wird vertauscht. Das Programm darf erneut frei wählen:

- die Namen `X` und `Y` jedes Blocks;
- die Startposition;
- den ersten Wert von `n`;
- die beste Folge wachsender `n`-Werte;
- die Stelle des einen erlaubten übersprungenen `n`-Werts;
- eine insgesamt erlaubte Position zwischen den Blöcken.

Die primäre Teststatistik ist die maximale Zahl der Blöcke. Eine Zufallsliste
gilt als mindestens ebenso stark, wenn sie unter diesen großzügigeren Regeln
acht oder mehr Blöcke erzeugt.

## Ergebnis

Bei 1.000.000 Permutationen mit Seed 42 wurde kein Treffer beobachtet:

```text
Zufallstreffer: 0 / 1.000.000
p = (0 + 1) / (1.000.000 + 1)
  ≈ 0,00000100
```

Das 95-%-Wilson-Intervall der simulierten Trefferquote reicht von 0 bis
ungefähr `0,00000384`. Der Befund ist unter dem verwendeten Nullmodell deutlich
signifikant.

Da keine Zufallstreffer auftraten, ist `0,000001` keine präzise Bestimmung der
theoretischen Wahrscheinlichkeit, sondern die Plus-eins-Auflösungsgrenze der
Millionenrechnung.

## Vergleich mit der Kaiserfilter-Variante

| Variante | n-Folge | Abdeckung | Treffer | Plus-eins-p |
|---|---|---:|---:|---:|
| Kaiserfolge ohne Ferdinand IV. | 1–8 | 60/61 = 98,36 % | 0/1.000.000 | `0,000001` |
| Königsliste mit Ferdinand IV. | 1–7, 9 | 61/62 = 98,39 % | 0/1.000.000 | `0,000001` |

Der zweite Test ist methodisch konservativer hinsichtlich der Personenauswahl,
weil Ferdinand IV. nicht entfernt wird. Dafür führt er eine klar ausgewiesene
Mustertoleranz ein. Diese Toleranz wird vollständig in jeder Permutation
wiederholt.

## Reproduktion

```bash
python3 -m name_patterns.pair_echo \
  --timeline HRR_Kings_843_1806.csv \
  --variant 8-kings --trials 1000000 --seed 42 \
  --output HRR_PAIR_ECHO_8_mit_Ferdinand_IV_Analyse.txt
```
