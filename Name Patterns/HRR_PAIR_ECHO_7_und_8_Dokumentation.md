# Analyse der Siebener- und Achterfolge `X, Y, n, Y`

## Untersuchungsziel

Geprüft werden zwei getrennt festgelegte Varianten einer abstrahierten
Herrscherfolge des ostfränkischen und Heiligen Römischen Reiches:

1. sieben Blöcke von Karl dem Großen bis Friedrich III.;
2. acht Blöcke von Karl dem Großen bis Karl VI.

Die allgemeine Blockform lautet:

```text
X, Y, [n beliebige Namen], Y
```

Von Block zu Block wächst `n` exakt um eins. Die Namen `X` und `Y` werden für
jeden Block neu gebunden und dürfen zwischen den Blöcken wechseln.

## Festgelegte Listenbildung

### Gemeinsamer Beginn

Der Anfang besteht aus der karolingischen Kaiserfolge:

```text
Karl der Große, Ludwig I., Lothar I., Ludwig II.
```

Danach folgen die ab 876 neu erhobenen ostfränkischen beziehungsweise
römisch-deutschen Herrscher der kontrollierten Wikipedia-Liste.

`Karlmann` wird vor der Analyse zu `Karl` normalisiert. Die Regel beruht auf
der Zerlegung des Namens in `Karl` und `Mann` und wird sowohl im beobachteten
Datensatz als auch in allen Permutationen unverändert verwendet.

### Siebenerfolge

Die erste Variante endet mit Friedrich III. und enthält 50 Positionen.

### Achterfolge

Die zweite Variante hängt an die Siebenerfolge die Kaiserfolge von
Maximilian I. bis Karl VI. an:

```text
Maximilian I., Karl V., Ferdinand I., Maximilian II., Rudolf II., Matthias,
Ferdinand II., Ferdinand III., Leopold I., Joseph I., Karl VI.
```

Ferdinand IV. wird nicht aufgenommen, da er kein Kaiser war. Die zweite
Variante enthält 61 Positionen.

## Gefundene sieben Blöcke

| n | Index | X | Y | Blocklänge |
|---:|---:|---|---|---:|
| 1 | 0–3 | Karl | Ludwig | 4 |
| 2 | 4–8 | Karl | Ludwig | 5 |
| 3 | 9–14 | Konrad | Heinrich | 6 |
| 4 | 15–21 | Konrad | Heinrich | 7 |
| 5 | 23–30 | Konrad | Heinrich | 8 |
| 6 | 31–39 | Konrad | Heinrich | 9 |
| 7 | 40–49 | Ludwig | Friedrich | 10 |

Zwischen dem vierten und fünften Block liegt Lothar III. als einzige nicht
abgedeckte Position. Die sieben Blöcke erfassen 49 von 50 Positionen:

```text
Abdeckung = 49 / 50 = 98,00 %
Scan-Score = 49 × 49 / 50 = 48,02
```

## Zusätzlicher achter Block

Die Achtervariante enthält zusätzlich:

| n | Index | X | Y | Blocklänge |
|---:|---:|---|---|---:|
| 8 | 50–60 | Maximilian | Karl | 11 |

Damit werden 60 von 61 Positionen abgedeckt:

```text
Abdeckung = 60 / 61 ≈ 98,36 %
Scan-Score = 60 × 60 / 61 ≈ 59,016393
```

## Global korrigierte Discovery

Der Permutationstest prüft nicht nur die beobachteten Namen. In jeder
Zufallsliste darf das Programm erneut wählen:

- die Namen `X` und `Y` jedes Blocks;
- die Startposition der Kette;
- den Anfangswert von `n`;
- die bestmögliche Folge aufeinanderfolgender `n`-Werte.

Es gelten in Original und Zufallslisten dieselben Bedingungen:

- `X` und `Y` müssen innerhalb eines Blocks verschieden sein;
- die zweite und die letzte Position eines Blocks müssen denselben Namen
  tragen;
- `n` wächst zwischen aufeinanderfolgenden Blöcken exakt um eins;
- Blöcke dürfen sich nicht überlappen;
- insgesamt ist höchstens eine Position zwischen den Blöcken erlaubt, die zu
  keinem Block gehört;
- die Häufigkeit aller Namen bleibt durch Permutation exakt erhalten.

Als primäre Teststatistik dient die maximale Zahl aufeinanderfolgender
`n`-Blöcke. Erst bei Gleichstand würden Abdeckung und Dichte entscheiden. Das
ist sachgerecht, weil die Besonderheit gerade in der ununterbrochenen Folge
`n = 1, 2, ..., 7` beziehungsweise `1, 2, ..., 8` besteht.

## Ergebnis der Siebenerfolge

Bei 1.000.000 Permutationen mit Seed 42 erreicht keine Zufallsliste sieben
aufeinanderfolgende Blöcke:

```text
Zufallstreffer: 0 / 1.000.000
Plus-eins-p-Wert: 1 / 1.000.001
p ≈ 0,00000100
```

Da null Treffer beobachtet wurden, ist `0,000001` vor allem die numerische
Auflösungsgrenze des Monte-Carlo-Laufs. Das 95-%-Wilson-Intervall der
Trefferquote reicht von 0 bis ungefähr `0,00000384`.

Die Siebenerfolge ist unter diesem Nullmodell deutlich signifikant.

## Ergebnis der Achterfolge

Auch bei der Achterfolge erreicht keine von 1.000.000 Zufallslisten die
beobachtete Kettenlänge:

```text
Zufallstreffer: 0 / 1.000.000
Plus-eins-p-Wert: 1 / 1.000.001
p ≈ 0,00000100
```

Das 95-%-Wilson-Intervall reicht ebenfalls von 0 bis ungefähr `0,00000384`.
Die Achterfolge ist unter ihrem Nullmodell deutlich signifikant.

## Zwei Varianten und Mehrfachprüfung

Die Achterfolge enthält die Siebenerfolge vollständig; beide Tests sind daher
stark abhängig. Werden sie dennoch als zwei getrennte, nachträglich betrachtete
Hypothesen berichtet, kann konservativ eine Bonferroni-Korrektur vorgenommen
werden:

```text
p_adjustiert ≤ 2 × 0,000001 = 0,000002.
```

Auch diese konservative Korrektur ändert die Signifikanzentscheidung nicht.
Wegen der null beobachteten Treffer sollte die Monte-Carlo-Obergrenze jedoch
zusätzlich genannt werden.

## Reichweite der Aussage

Die p-Werte sind global für die Suche **innerhalb der jeweils festgelegten
Namensliste** korrigiert. Sie berücksichtigen die freie Wahl von `X`, `Y`,
Startposition und `n`-Beginn.

Sie korrigieren nicht nachträglich über jede denkbare historische
Listenbildung. Insbesondere werden folgende Entscheidungen als Bestandteil der
Hypothese festgehalten und nicht zufällig variiert:

- Beginn bei Karl dem Großen;
- Übergang zur ostfränkischen Liste ab den neuen Erhebungen von 876;
- Behandlung von Karlmann als Karl;
- Ende der Siebenerliste bei Friedrich III.;
- Verwendung der Kaiserfolge für den achten Block;
- Ausschluss Ferdinands IV. aus der Kaiserfolge;
- Ende der Achterliste bei Karl VI.;
- höchstens eine Position außerhalb der Blöcke.

Die statistische Aussage lautet deshalb präzise:

> Unter zufälliger Neuordnung derselben Namen innerhalb der beiden definierten
> Listen wurde in jeweils einer Million Durchläufen keine ebenso lange
> `PAIR_ECHO`-Kette gefunden.

Eine historische oder kausale Erklärung folgt daraus nicht automatisch.

## Reproduktion

```bash
python3 -m name_patterns.pair_echo \
  --timeline HRR_Kings_843_1806.csv \
  --variant both --trials 1000000 --seed 42 \
  --output HRR_PAIR_ECHO_7_und_8_Analyse.txt
```
