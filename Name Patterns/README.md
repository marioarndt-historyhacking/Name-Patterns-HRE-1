# Name Patterns

Sucht in einer Namensliste regelmässige Wiederholungsmuster: Blöcke der Form

```
Anchor  +  x beliebige Füllnamen  +  Echo
```

deren Abstand `x` über die Blöcke hinweg entweder **konstant** bleibt oder **um 1
wächst** — mit einem einstellbaren Budget an tolerierten Abweichungen.

Ausgangspunkt ist die Liste der römisch-deutschen Könige, in der sich das Muster
`Konrad → Heinrich … Heinrich` viermal wiederholt, mit wachsendem Abstand
3 → 4 → 5 → 6.

## Schnellstart

```bash
python3 -m name_patterns.cli
```

Ausgabe:

```
Muster:      Konrad Heinrich ... Heinrich
Regel:       x = 3 + j*1
Blöcke:      4   Abweichungen: 0   Score: 4.00
Bereich:     Index 0..30

  j=0       0..5  x=3   Konrad Heinrich [Otto Otto Otto] Heinrich
  j=1      6..12  x=4   Konrad Heinrich [Heinrich Rudolf Hermann Konrad] Heinrich
  j=2     14..21  x=5   Konrad Heinrich [Friedrich Heinrich Philipp Otto Friedrich] Heinrich
  j=3     22..30  x=6   Konrad Heinrich [Wilhelm Richard Alfons Rudolf Adolf Albrecht] Heinrich
```

Ohne Vorgabe eines Motivs, mit Signifikanzprüfung:

```bash
python3 -m name_patterns.cli --discover --significance 2000 --seed 42
```

Tests:

```bash
python3 -m unittest discover -s tests -t .
```

## Herrscherlisten aus Wikipedia erzeugen

`build_ruler_list.py` erzeugt eine direkt lesbare Namensdatei sowie eine CSV-
Prüfdatei und einen Markdown-Bericht. Für das ostfränkische und Heilige
Römische Reich von 911 bis 1313:

```bash
python3 build_ruler_list.py \
    --country hrr --start 911 --end 1313 \
    --refresh --output HRR_Kings_911_1313.txt
```

Die erzeugte Textdatei kann unmittelbar verwendet werden:

```bash
python3 -m name_patterns.cli \
    --data HRR_Kings_911_1313.txt \
    --discover --show-input-metadata \
    --measure coverage --significance 2000 --seed 42 --quiet
```

`--significance 2000` führt 2.000 zufällige Umsortierungen aus. Erst dadurch
kann das Programm einen p-Wert und die Entscheidung an der Schwelle 0,05
ausgeben. Der Ergebnisblock enthält dann ausdrücklich:

```text
p-Wert:      0.0155   (gemessen an Abdeckung)
Signifikant:  ja (p < 0.05)
```

Bei `p >= 0.05` steht entsprechend `Signifikant: nein`. `--seed 42` macht den
Monte-Carlo-Lauf reproduzierbar; `--quiet` unterdrückt nur die laufende
Fortschrittsanzeige, nicht das Ergebnis.

Die Liste ist nach der ersten Königserhebung sortiert. Gegenkönige und
Mitkönige sind standardmäßig enthalten; dieselbe Person erscheint auch bei
späterer Anerkennung oder einer zweiten Amtszeit nur einmal. Optionen:

```text
--exclude-counter-kings   Gegenkönige auslassen
--exclude-co-kings        Mitkönige auslassen
--offline                 ausschließlich den lokalen Wikipedia-Cache nutzen
--refresh                 Wikipedia-Cache erneuern
--list-countries          verfügbare Länderadapter anzeigen
```

Neue Länder werden als Adapter in `ruler_lists/sources/` ergänzt. Da
Wikipedia-Herrscherlisten unterschiedlich aufgebaut sind, wird bewusst kein
scheinbar universeller, aber unzuverlässiger Tabellenparser verwendet. Details
stehen in `RULER_LIST_IMPORT.md`.

## Gesamtliste 843–1806 und freie Intervallsuche

Die vollständige Wikipedia-Herrscherfolge wird so erzeugt:

```bash
python3 build_ruler_list.py \
    --country hrr --start 843 --end 1806 \
    --refresh --output HRR_Kings_843_1806.txt
```

Sie enthält 64 Personen. Die letzte Erhebung ist diejenige Franz’ II. im Jahr
1792; seine Herrschaft und das HRR enden 1806.

Das bekannte Motiv kann über die vollständige Liste geprüft werden, ohne den
Zeitraum 911–1313 vorzugeben:

```bash
python3 -m name_patterns.cli \
    --data HRR_Kings_843_1806.txt \
    --timeline-metadata HRR_Kings_843_1806.csv \
    --scan-intervals --family fixed \
    --anchor Konrad,Heinrich --echo Heinrich \
    --d 0,1 --min-blocks 3 --max-deviations 0 \
    --significance 10000 --seed 42 --quiet
```

`--scan-intervals` lässt die Kettensuche Anfang und Ende selbst bestimmen. Die
Kennzahl ist `abgedeckte Positionen × lokale Abdeckung × Abweichungsfaktor`.
In jeder Permutation werden Anfang, Ende, `x0` und Schrittweite neu gewählt.

Für das fest vorgegebene Motiv ergibt die Referenzrechnung `p = 0.0001` und
damit ein signifikantes Ergebnis. Da das Motiv ursprünglich anhand derselben
Daten entdeckt wurde, ist zusätzlich die strengere Discovery-Korrektur wichtig:

```bash
python3 -m name_patterns.cli \
    --data HRR_Kings_843_1806.txt \
    --timeline-metadata HRR_Kings_843_1806.csv \
    --scan-intervals --discover --family fixed \
    --d 0,1 --min-blocks 3 --max-deviations 0 \
    --significance 10000 --seed 42 --quiet
```

Hier darf jede Permutation zusätzlich ihr bestes festes Anchor/Echo-Motiv
wählen. Ergebnis: `p = 0.0749`, also nicht signifikant an der 0,05-Schwelle.
Beide Werte beantworten verschiedene Fragen und werden getrennt berichtet.
Details stehen in `VOLLZEITRAUM_ANALYSE.md`.

## Historisch festgelegter Früh–Spät-Vergleich

Für die eigentliche Hypothese werden die Zeiträume 911–1313 und 1314–1806
getrennt untersucht. Beide Tests durchsuchen **alle derzeit implementierten
Musterfamilien**: feste Anchor/Echo-Motive (`FIXED`) und die pro Block frei
gebundene Namensklammer (`BOOKEND`). Motiv, Intervall, `x0` und Schrittweite
werden in jeder Permutation neu ausgewählt.

```bash
python3 -m name_patterns.cli \
    --data HRR_Kings_843_1806.txt \
    --timeline-metadata HRR_Kings_843_1806.csv \
    --compare-periods 911:1313,1314:1806 \
    --discover --family both \
    --d 0,1 --min-blocks 3 --max-deviations 0 \
    --significance 10000 --seed 42 --quiet \
    --report-output HRR_911_1313_vs_1314_1806_Periodenvergleich.txt
```

Referenzergebnis:

| Prüfung | Ergebnis |
|---|---:|
| Discovery 911–1313 | `p = 0.0160`, signifikant |
| Discovery 1314–1806 | keine zulässige Kette aus mindestens drei Blöcken |
| gerichteter Früh–Spät-Vergleich | `p = 0.0009`, signifikant |

Der direkte Vergleich verwendet den durch die Periodenlänge geteilten
Scan-Score. Im Nullmodell werden die Namen beider Zeiträume gepoolt, zufällig
auf Teile derselben Größen verteilt und beide Teile vollständig neu
durchsucht. Er prüft damit, ob die derzeit erkennbaren Muster auf den frühen
Zeitraum konzentriert sind. Einzelheiten und Grenzen stehen in
`ZEITRAUMVERGLEICH_911_1806.md`.

## Exakte 113-Jahres-Folge der Konrad-Vorgänger

Die kontrollierte reguläre Vorgängerfolge enthält die Todesjahre
`911, 1024, 1137, 1250`. Sie gehören zu den Vorgängern Konrads I.–IV. und
bilden mit dreimal 113 Jahren die einzige exakte viergliedrige arithmetische
Folge unter den 52 erfassten regulären Vorgänger-Nachfolger-Ereignissen von
843 bis 1806.

```bash
python3 -m name_patterns.succession \
    --timeline HRR_Kings_843_1806.csv \
    --trials 1000000 --seed 42 \
    --output HRR_113_Jahre_und_Gesamtsignifikanz.txt
```

| Prüfung | p-Wert |
|---|---:|
| Konrad und die vier Jahre als fest vorgegeben | exakt `0.00000369` |
| Name frei gewählt, dadurch global korrigiert | exakt `0.00015514` |
| Namenskette 911–1313 | `0.0160` |
| beide Befunde gleichzeitig | Monte Carlo `0.000097` |

Der gemeinsame Wert beruht auf 96 Treffern in einer Million gemeinsamer
Permutationen. Er ist keine Multiplikation der Einzelwerte: Eine
Zufallsanordnung muss gleichzeitig eine mindestens ebenso starke Namenskette
und eine mindestens ebenso starke Ereignisfolge erzeugen. Methodik,
Datenabgrenzung und Einschränkungen stehen in `EREIGNISFOLGE_113_JAHRE.md`.

## Abstrahierte PAIR_ECHO-Folge von Karl dem Großen bis Karl VI.

Die zusätzliche Musterfamilie `PAIR_ECHO` sucht Blöcke der Form
`X, Y, [n Namen], Y`, wobei `X` und `Y` pro Block frei sind und `n` von Block
zu Block exakt um eins wächst. `Karlmann` wird für diese Analyse als `Karl`
normalisiert.

```bash
python3 -m name_patterns.pair_echo \
    --timeline HRR_Kings_843_1806.csv \
    --variant both --trials 1000000 --seed 42 \
    --output HRR_PAIR_ECHO_7_und_8_Analyse.txt
```

| Variante | Abdeckung | Zufallstreffer | Plus-eins-p |
|---|---:|---:|---:|
| 7 Blöcke bis Friedrich III. | 49/50 = 98,00 % | 0/1.000.000 | `0,000001` |
| 8 Blöcke bis Karl VI. | 60/61 = 98,36 % | 0/1.000.000 | `0,000001` |

Die 95-%-Wilson-Obergrenze der Trefferquote beträgt in beiden Läufen ungefähr
`0,00000384`. Einzelheiten zur Listenbildung, Discovery-Korrektur und den
Grenzen des Nullmodells stehen in `HRR_PAIR_ECHO_7_und_8_Dokumentation.md`.

Eine getrennte Sensitivitätsanalyse setzt die Königsliste unter Einschluss
Ferdinands IV. fort. Der achte Block besitzt dann `n = 9` statt `n = 8`; das
Nullmodell erlaubt deshalb jeder Permutation einmal das Überspringen eines
beliebigen Sollwerts. Auch hierbei entstanden in einer Million Permutationen
keine Zufallstreffer (`p = 0,000001`, Wilson-Obergrenze etwa `0,00000384`).
Details stehen in `HRR_PAIR_ECHO_8_mit_Ferdinand_IV_Dokumentation.md`.

## Begriffe

| Begriff | Bedeutung |
|---|---|
| **Anchor** | Motiv, das einen Block eröffnet, z.B. `("Konrad", "Heinrich")` |
| **Echo** | Name, der den Block schliesst, z.B. `"Heinrich"` |
| **Block** | ein Vorkommen von Anchor + `x` Füllnamen + Echo |
| **Chain** | Folge disjunkter Blöcke, deren `x`-Werte `x₀, x₀+d, x₀+2d, …` bilden |
| **j** | Position eines Blocks innerhalb der Kette (0-basiert) |
| **d** | Schrittweite der Progression; `0` = konstant, `1` = wachsend |

## Warum keine einfache Lücken-Zählung reicht

Naheliegend wäre: alle Vorkommen von „Heinrich" nehmen und die Abstände
dazwischen anschauen. Das scheitert an den echten Daten:

```
Heinrich@  [1, 5, 7, 8, 12, 15, 17, 21, 23, 30]
Abstände:  [3, 1, 0, 3,  2,  1,  3,  1,  6]
```

Die gesuchte Folge **3, 4, 5, 6** kommt darin nicht vor — es gibt Zusatz-Heinrichs
(Index 8 und 17), die keine Blockgrenze sind. Das Muster ist eine *Teilfolge*,
keine lückenlose Kette.

Ebenso scheitert ein gieriger Scan „nimm den nächsten Konrad als Blockstart":
Konrad an Index 11 steckt **innerhalb** von Block 2. Von 16 Blockkandidaten
gehören nur 4 zur richtigen Kette. Deshalb ist der Kern eine echte Suche über
Blockketten und kein Durchlauf von links nach rechts.

## Aufbau

| Datei | Inhalt |
|---|---|
| `name_patterns/model.py` | Datentypen: `Block`, `Chain`, `Deviation`, `SearchConfig` |
| `name_patterns/index.py` | Phase 1+2: Vorkommen indizieren, Blockkandidaten sammeln |
| `name_patterns/search.py` | Phase 3: DP-Chaining — der eigentliche Algorithmus |
| `name_patterns/discovery.py` | Phase 2b: Motivkandidaten finden (Stufe 3) |
| `name_patterns/scoring.py` | Phase 4: Seltenheit in Bit, Monte-Carlo-p-Wert (Stufe 4) |
| `name_patterns/report.py` | lesbare Ausgabe |
| `name_patterns/cli.py` | Kommandozeile |
| `name_patterns/inspect_null.py` | Umsortierungen des Nullmodells als Tabelle |
| `name_patterns/joint.py` | mehrere Listen gemeinsam auswerten |
| `name_patterns/data.py` | Königsliste + Loader für eigene Dateien |

Der Suchkern in `search.py`: sind `x₀` und `d` festgelegt, steht der Sollwert an
jeder Kettenposition fest (`x₀ + j·d`). Eine Dynamische Programmierung über die
Blockkandidaten sucht dann die längste Kette, die dieses Soll einhält.
Zustand ist `(Blockindex, j, Restbudget)`; maximiert wird die Blockzahl, bei
Gleichstand gewinnt die Variante mit weniger Abweichungen.

## Toleranz

`max_deviations` ist ein gemeinsames Budget für zwei Abweichungsarten:

| Art | Bedeutung |
|---|---|
| `GAP_OFF_BY` | `x` weicht um bis zu `gap_slack` vom Sollwert ab |
| `SKIP` | ein Kettenglied fehlt ganz; `j` springt weiter |

**Wichtige Festlegung:** Nach einer Abweichung läuft die Progression am
*Sollwert* weiter, nicht am gemessenen Wert. Bei Soll 3,4,5,6 und Ist 3,4,**6**,6
zählt das als *eine* Abweichung — der vierte Block ist wieder exakt. Rechnete man
am Istwert weiter, würde ein einzelner Ausreisser die ganze Kette entgleisen
lassen.

Blöcke müssen **nicht** aneinandergrenzen. „Lothar" (Index 13) sitzt zwischen
zwei Blöcken und kostet deshalb kein Budget — das ist gewollt.

## Zwei Musterfamilien

**FIXED** — Anchor und Echo sind feste Namen, über alle Blöcke dieselben:
`Konrad Heinrich … Heinrich`. Das ist der Fall der Königsliste des HRR.

**BOOKEND** — jeder Block wird von *demselben* Namen eingeklammert, aber welcher
das ist, wird **pro Block neu gebunden**: `?N … ?N`. In der norwegischen Liste
sind das Olav … Olav, dann Öystein … Öystein, dann Hakon … Hakon. Was sich
wiederholt, ist die Struktur, nicht das Motiv.

Kein `--anchor X --echo Y` kann die zweite Familie ausdrücken, und die Discovery
über feste Namen findet sie auch nicht — deshalb eine eigene Blocksuche. Der
Verkettungskern ist derselbe: er schaut nur auf `x`, nicht darauf, wie ein Block
zustande kam.

```bash
python3 -m name_patterns.cli --data Norway_Kings.txt --family bookend --d 0 --max-interruption 3
```

```
Muster:      ?N ... ?N
Regel:       x = 5 (konstant)
Blöcke:      3   Abweichungen: 0   Score: 3.00
Klammern:    Olav / Öystein / Hakon   (alle verschieden)
Blocklänge:  7 Namen je Block
Zwischen:    2, 0  (Namen zwischen den Blöcken)

  j=0    0..6  x=5   Olav [Olav Knut Magnus Harald Magnus] Olav
  j=1   9..15  x=5   Öystein [Sigurd Magnus Harald Sigurd Inge] Öystein
  j=2  16..22  x=5   Hakon [Magnus Öystein Sverre Jon Inge] Hakon
```

### Nachbarschaft

`--max-interruption N` begrenzt, wie viele Namen zwischen zwei Blöcken stehen
dürfen. Für die Familie BOOKEND ist das konstitutiv („mehrfach nacheinander"),
für FIXED optional. Default ist unbegrenzt. Die Schranke gilt zwischen
*gesetzten* Blöcken und wird durch ein übersprungenes Kettenglied nicht
gelockert — wer beides kombiniert, muss `N` entsprechend erhöhen.

### Rufnamen

Für die Mustersuche zählt nur der **Rufname: alles bis zum ersten Leerzeichen**.
Sonst wären `Olav I.` und `Olav III.` verschiedene Namen und keine Klammer würde
greifen. Diese eine Regel erledigt beide Fälle:

| Eintrag | zählt als |
|---|---|
| `Olav III.` | `Olav` |
| `Friedrich Barbarossa` | `Friedrich` |
| `Guttorm Sigurdsson` | `Guttorm` |
| `Inge II. Bardsson` | `Inge` |

`load_names()` normalisiert per Default und meldet, wie viele Einträge betroffen
waren — eine stille Veränderung der Eingabe wäre genau die Art Detail, die
später Verwirrung stiftet. `--raw-names` schaltet es aus.

Zusätzlich läuft `strip_ordinal()` über den ersten Token. Das greift nur bei der
Schreibweise ohne Leerzeichen (`OlavIII.`) und ändert an sauber getrennten
Einträgen nichts.

## Die Umsortierungen ansehen

Der p-Wert sagt nur, *wie oft* der Zufall mithalten konnte — nicht, wie diese
Zufallstreffer aussehen. `inspect_null` schreibt sie als Markdown-Tabelle heraus,
eine Zeile je Permutation, alle Namen nebeneinander, Blockklammern fett:

```bash
python3 -m name_patterns.inspect_null --data Denmark_Kings.txt \
    --family bookend --d 0 --max-interruption 4 \
    --trials 100 --stats-trials 2000 --seed 42 -o Denmark_Nullmodell.md
```

Die Permutationen entstehen mit demselben Startwert und in derselben Reihenfolge
wie im Signifikanztest — es sind also genau die, auf denen der p-Wert beruht.
Ein Test hält das fest.

`--trials` steuert die Tabellenlänge, `--stats-trials` die Auswertung darunter.

## Discovery: Motive selbst finden

Mit `--discover` werden Anchor und Echo nicht vorgegeben, sondern gesucht. Der
Suchraum bleibt klein durch zwei **exakte** Prunings — keine Heuristiken:

- Jeder Block braucht ein Anchor-Vorkommen → Anchor mit weniger als
  `min_blocks` Vorkommen können keine gültige Kette tragen.
- Dasselbe gilt für das Echo.

Was hier wegfällt, hätte ohnehin keine Kette der geforderten Mindestlänge
ergeben. Auf der Königsliste bleiben so nur wenige Dutzend Motivkandidaten.

## Zwei Messgrössen: Seltenheit oder Abdeckung?

Die Frage „ist diese Anordnung geordneter als eine zufällige?" lässt sich auf
zwei Arten messen, und sie geben verschiedene Antworten.

**`--measure bits`** zählt, wie unwahrscheinlich das *Motiv* ist. Drei
Blöcke sind drei Blöcke — ob je drei oder je acht Namen lang, macht keinen
Unterschied.

**`--measure coverage`** (Default) zählt, wie viel der Liste das Muster *erklärt*. Drei
Blöcke zu je acht Namen erfassen 24 Positionen, drei zu je drei nur neun.

Der Unterschied ist praktisch entscheidend. Auf der dänischen Liste:

| Messgrösse | p | |
|---|---|---|
| `bits` | 0.576 | nicht signifikant |
| `coverage` | **0.020** | signifikant |

Nach Bit wird der p-Wert von kurzen Zufallsketten getragen, die mit dem Befund
strukturell nichts gemein haben — sie decken im Mittel nur 47 % der Liste ab und
lassen unstrukturierte Strecken von im Schnitt 8,5 Namen stehen. Die
Königsliste erfasst dagegen 24 von 27 Namen; nur drei brechen aus, die längste
Lücke ist zwei Namen lang.

Der Report zeigt beides, und nennt an der p-Wert-Zeile, welche der beiden
gerade zugrunde liegt — derselbe Befund bekommt je nach Wahl 0.02 oder 0.37:

```
Abdeckung:   24/27 Namen (89%), 3 ausserhalb, laengste Aussenstrecke 2
Seltenheit:  8.7 Bit
p-Wert:      0.0195   (gemessen an Abdeckung)
Signifikant:  ja (p < 0.05)
```

Seit die Abdeckung sich als die passende Grösse erwiesen hat, ist sie der
Default. `--measure bits` stellt das alte Verhalten wieder her.

`max_outsider_run` zählt dabei auch die Ränder — eine Kette, die erst in der
Mitte beginnt, lässt vorne eine lange unstrukturierte Strecke, und die gehört
zur Beurteilung dazu. `--max-interruption` allein sieht das nicht, weil es nur
*zwischen* Blöcken misst.

## Signifikanz: Befund oder Rauschen?

Zwei getrennte Grössen, die erst zusammen aussagekräftig sind.

**Seltenheit (Bit)** — wie unwahrscheinlich das Motiv als solches ist. Ein Muster
auf einem sehr häufigen Namen ist wenig überraschend, eines auf seltenen Namen
viel mehr. Erst das macht Ketten *verschiedener* Motive vergleichbar. Auf der
Königsliste rangiert damit `Konrad Heinrich … Heinrich` (4 Blöcke, 23.6 Bit) vor
`Konrad … Heinrich` (5 Blöcke, 21.3 Bit): die längere Kette ist nicht die
interessantere.

**p-Wert** — wie oft ein mindestens so guter Treffer auftaucht, wenn man dieselbe
Namensmenge zufällig umsortiert. Das Nullmodell permutiert die Liste, die
Häufigkeit jedes Namens bleibt exakt erhalten. Geprüft wird also allein, ob die
*Anordnung* bemerkenswert ist.

Ergebnis der **Bit-/Seltenheitsbewertung** bei 2000 Permutationen:

| Muster | Blöcke | Bit | p | |
|---|---|---|---|---|
| `Konrad Heinrich … Heinrich`, x=3+j | 4 | 23.6 | **0.0015** | signifikant |
| `Konrad … Heinrich`, x=0 | 5 | 21.3 | **0.0125** | signifikant |
| `Heinrich … Konrad`, x=4+j | 3 | 12.8 | 0.906 | Rauschen |

Diese p-Werte beziehen sich auf die Kennzahl `--measure bits`. Sie fragen, wie
oft die Discovery in einer Zufallsreihenfolge ein mindestens ebenso seltenes
Namensmotiv findet. Der Wert `0.0015` ist daher **nicht** dieselbe statistische
Prüfung wie der spätere Periodentest mit Abdeckungs-/Scan-Score.

Mit derselben Liste, demselben Suchraum, 2000 Permutationen und Seed 42, aber
`--measure coverage`, ergibt sich für `Konrad Heinrich … Heinrich`
`p = 0.0155`. Der neue Periodentest reproduziert bei 2000 Permutationen
ebenfalls `p = 0.0155`; mit 10000 Permutationen lautet die stabilere Schätzung
`p = 0.0160`. Der Unterschied zwischen `0.0015` und rund `0.016` entsteht also
vor allem durch die **andere Teststatistik**, nicht durch eine andere
Herrscherliste oder die zusätzliche BOOKEND-Familie.

Der dritte Treffer sieht in der Rohausgabe plausibel aus, ist aber nur ein
Nebeneffekt davon, dass beide Namen häufig sind — neun von zehn zufälligen
Umsortierungen liefern etwas mindestens so Gutes. Genau dafür ist die Prüfung da:
mit einem Abweichungsbudget von 2 oder 3 findet man in *jeder* hinreichend langen
Liste irgendein „Muster".

### Bits bei freier Klammer

Für BOOKEND wäre die Formel für feste Namen falsch. Gefordert ist dort nicht ein
bestimmter Name, sondern nur *Gleichheit* — die richtige Bezugsgrösse ist der
Simpson-Index `Σ p(N)²`, also die Wahrscheinlichkeit, dass zwei Positionen
denselben Namen tragen. Mit der alten Formel bekäme die neue Familie
systematisch aufgeblähte Werte und verdrängte die spezifischeren Treffer aus der
Rangliste.

### Norwegen: die Gegenprobe

Die Abdeckungs-Messung wurde an der dänischen Liste entwickelt. Norwegen ist
damit der unabhängige Test — dieselbe Messgrösse, unverändert, auf Daten, die
bei ihrer Entwicklung keine Rolle gespielt haben.

```
Muster:      ?N ... ?N          Regel: x = 5 (konstant)
Klammern:    Olav / Öystein / Hakon / Hakon
Abdeckung:   28/34 Namen (82%), 6 ausserhalb, längste Aussenstrecke 4

  j=0    0..6   Olav [Olav Knut Magnus Harald Magnus] Olav
  j=1   9..15   Öystein [Sigurd Magnus Harald Sigurd Inge] Öystein
  j=2  16..22   Hakon [Magnus Öystein Sverre Jon Inge] Hakon
  j=3  27..33   Hakon [Skule Magnus Erik Hakon Magnus] Hakon
```

| Konfiguration | Blöcke | Abdeckung | p (bits) | p (coverage) |
|---|---|---|---|---|
| `--d 0 --max-interruption 4` | 4 | 82 % | 0.124 | **0.025** |
| `--d 0 --max-interruption 8` | 4 | 82 % | 0.286 | **0.025** |
| `--d 0` ohne Schranke | 4 | 82 % | 0.404 | **0.025** |
| `--d 0,1 --max-interruption 4` | 4 | 82 % | 0.205 | **0.040** |
| beide Familien | 4 | 82 % | 0.366 | **0.045** |
| `--d 0 -t 1 --max-interruption 4` | 4 | 82 % | 0.171 | 0.097 |
| `--d 0 --max-interruption 2` | 3 | 62 % | 0.323 | 0.107 |

Signifikant in fünf von sieben Konfigurationen, über fünf Startwerte stabil bei
p = 0.016–0.021. Die beiden Ausnahmen sind erklärbar und keine Gegenbefunde:

- **`--max-interruption 2`** schneidet den vierten Block mechanisch ab, denn vor
  ihm stehen vier unsystematische Könige. Übrig bleiben drei Blöcke mit 62 %
  Abdeckung. Anders als bei Dänemark (grösste Unterbrechung 2) ist die Schranke
  hier also nicht beliebig — sie muss mindestens 4 sein, sonst sucht man ein
  anderes Muster.
- **`-t 1`** erlaubt Abweichungen und vergrössert damit den Suchraum, in dem
  auch das Nullmodell mehr findet.

### Schottland: der deutlichste Befund

27 Könige vom 9. bis zum Ende des 13. Jahrhunderts.

```
Muster:      ?N ... ?N          Regel: x = 4 (konstant)
Klammern:    Donald / Malcolm / Duncan / Alexander   (alle verschieden)
Abdeckung:   24/27 Namen (89%), 3 ausserhalb, längste Aussenstrecke 1

  j=0    1..6   Donald [Konstantin Aedh Eochaid Giric] Donald
  j=1   8..13   Malcolm [Indulf Dubh Culen Kenneth] Malcolm
  j=2  14..19   Duncan [Macbeth Lulach Malcolm Donald] Duncan
  j=3  21..26   Alexander [David Malcolm Wilhelm Alexander] Alexander
```

Vier Blöcke zu je sechs Königen, vier verschiedene Klammernamen, und die
Ausbrecher stehen **einzeln** — die längste unstrukturierte Strecke ist ein
einziger Name.

Als bisher einzige Liste hält der Befund **unter beiden Messgrössen** und in
allen sieben Konfigurationen:

| Konfiguration | p (bits) | p (coverage) |
|---|---|---|
| `--d 0 --max-interruption 1` | **0.0020** | **0.0020** |
| `--d 0 --max-interruption 4` | **0.0070** | **0.0050** |
| `--d 0 --max-interruption 8` | **0.0150** | **0.0050** |
| `--d 0` ohne Schranke | **0.0200** | **0.0050** |
| `--d 0,1 --max-interruption 4` | **0.0090** | **0.0060** |
| `--d 0 -t 1 --max-interruption 4` | **0.0080** | **0.0080** |
| beide Familien | **0.0170** | **0.0060** |

Über fünf Startwerte stabil bei p = 0.001–0.003.

Der Unterschied zu den anderen Listen liegt in der Namensverteilung:

| Liste | n | verschiedene Namen | Simpson | Bit je Klammer |
|---|---|---|---|---|
| **Schottland** | 27 | **17** | **0.078** | **3.68** |
| Dänemark | 27 | 11 | 0.133 | 2.91 |
| Norwegen | 34 | 15 | 0.107 | 3.22 |

Schottland hat auf gleicher Listenlänge deutlich mehr verschiedene Namen als
Dänemark. Zufällige Klammern sind damit teurer, und der Befund hebt sich stärker
vom Rauschen ab — die mittlere Abdeckung im Nullmodell liegt bei 3 % gegenüber
28 % in Dänemark.

**Und hier trifft die Vermutung zu, die für Dänemark widerlegt war:** in 5000
Umsortierungen erreicht keine einzige eine höhere Abdeckung als 24/27, acht
kommen gleichauf. Das ist eine Aussage über die Stichprobe, kein Beweis der
theoretischen Maximalität — aber ein deutlicher Unterschied zu Dänemark, wo eine
Permutation die Liste lückenlos kachelte.

### Alle drei Listen nebeneinander

| | Schottland | Dänemark | Norwegen |
|---|---|---|---|
| Zeitraum | 9.–13. Jh. | bis 1332 | bis 1380 |
| Länge | 27 | 27 | 34 |
| Blöcke × Länge | 4 × 6 | 3 × 8 | 4 × 7 |
| Klammern verschieden | ja (4) | ja (3) | nein (Hakon 2×) |
| Abdeckung | 89 % | 89 % | 82 % |
| Ausbrecher | 3 | 3 | 6 |
| längste Aussenstrecke | **1** | 2 | 4 |
| p (bits) | **0.007** | 0.576 | 0.113 |
| **p (coverage)** | **0.003** | **0.020** | **0.021** |
| Umsortierung besser? | keine von 5000 | eine (100 %) | ja (97 %) |

Drei Listen, überlappender Zeitraum, dasselbe Bauprinzip bei drei verschiedenen
Blocklängen (6, 8, 7).

## Die drei Listen gemeinsam auswerten

```bash
python3 -m name_patterns.joint Scotland_Kings.txt Denmark_Kings.txt Norway_Kings.txt \
    --trials 20000 --seed 42
```

Die Listen werden dabei **nicht aneinandergehängt** — das würde Blöcke erlauben,
die über die Grenze zweier Dynastien reichen, und solche Blöcke bedeuten nichts.
Verbunden wird die *Evidenz*: drei unabhängige Tests zu einer Aussage, mit
identischer Konfiguration für alle drei.

Zwei Wege, die sich gegenseitig kontrollieren:

**Gemeinsamer Permutationstest.** Pro Durchlauf wird jede Liste für sich
umsortiert und die mittlere Abdeckung berechnet. Setzt nichts voraus ausser der
Unabhängigkeit der Listen.

**Fishers Methode** als Gegenprobe. Verbindet die Einzel-p-Werte analytisch,
setzt dafür aber gleichverteilte p-Werte unter der Nullhypothese voraus — bei
Monte-Carlo-Werten nur näherungsweise erfüllt.

Ergebnis über 20 000 Durchläufe:

| | beobachtet | Zufall (Mittel) | bester Zufall |
|---|---|---|---|
| mittlere Abdeckung | **86.7 %** | 18.8 % | 77.6 % |

| Test | p |
|---|---|
| mittlere Abdeckung | **< 0.00005** (0 von 20 000) |
| alle drei zugleich | **< 0.00005** (0 von 20 000) |
| Fisher (Gegenprobe) | 4.4 · 10⁻⁵ |

Beide Wege liefern dieselbe Grössenordnung, obwohl sie verschiedene
Voraussetzungen machen. In keinem einzigen von 20 000 Durchläufen erreichte der
Zufall gleichzeitig alle drei Listen.

### Wie viele Durchläufe? Und was sie *nicht* bewirken

Mehr Durchläufe machen einen Befund **nicht** signifikanter. Der p-Wert ist eine
Eigenschaft der Daten und des Tests; die Simulation schätzt ihn nur. Mehr
Durchläufe verengen das Konfidenzintervall dieser Schätzung, sie verschieben
nicht den geschätzten Wert.

Gemessen, je fünf Startwerte:

| Liste | N=500 | N=2000 | N=8000 | N=32000 | Spanne bei N=500 → N=32000 |
|---|---|---|---|---|---|
| Schottland | 0.0032 | 0.0019 | 0.0014 | 0.0013 | 0.0040 → 0.0010 |
| Dänemark | 0.0216 | 0.0191 | 0.0181 | 0.0171 | 0.0220 → 0.0032 |
| Norwegen | 0.0240 | 0.0181 | 0.0182 | 0.0184 | 0.0140 → 0.0014 |

Was sich wirklich verbessert, ist die **Streuung**: bei Norwegen von 0.014 auf
0.0014, also um den Faktor zehn. Der Mittelwert selbst bleibt ab N=2000 stabil
bei 0.018 — er sinkt gerade nicht.

Der leichte Rückgang bei Schottland und Dänemark hat einen anderen Grund, und es
ist kein Gewinn an Signifikanz, sondern der Abbau einer Verzerrung. Die
Plus-Eins-Korrektur `(1 + Treffer)/(1 + N)` verschiebt die Schätzung
systematisch nach oben:

```
E[p̂] = p + (1 - p)/(1 + N)
```

Der Aufschlag beträgt 0.0020 bei N=500 und nur noch 0.00003 bei N=32000. Er
fällt umso mehr ins Gewicht, je kleiner der wahre p-Wert ist — deshalb wandert
Schottland am stärksten, Norwegen (dessen p-Wert zehnmal grösser ist) gar nicht.
Die Vorhersage trifft die Messung auf die vierte Stelle:

| N | Aufschlag | Schottland Vorhersage/gemessen | Norwegen Vorhersage/gemessen |
|---|---|---|---|
| 500 | 0.00199 | 0.00321 / 0.00319 | 0.02029 / 0.02395 |
| 2000 | 0.00050 | 0.00172 / 0.00190 | 0.01882 / 0.01809 |
| 32000 | 0.00003 | 0.00125 / 0.00125 | 0.01836 / 0.01836 |

Beste Schätzungen der wahren Werte: **Schottland 0.0012, Dänemark 0.0171,
Norwegen 0.0183.**

Praktisch heisst das: N=2000 genügt, um eine Grössenordnung zu bestimmen.
N=20000 lohnt nur, wenn der p-Wert nahe an die Auflösungsgrenze `1/(N+1)` kommt
— wie beim gemeinsamen Test oben, der bei N=2000 mit „0 von 2000" schlicht
nichts Genaueres sagen konnte.

### Der ehrliche Vorbehalt

Die Abdeckungs-Messung wurde an der dänischen Liste entwickelt. Deren p-Wert ist
damit explorativ, nicht bestätigend. Rechnet man **nur** die beiden Listen, die
bei der Entwicklung keine Rolle gespielt haben:

| | Schottland + Norwegen |
|---|---|
| mittlere Abdeckung | 85.6 % (Zufall 14.5 %) |
| p (mittlere Abdeckung) | **0.0001** (1 von 20 000) |
| p (Fisher) | 1.9 · 10⁻⁴ |

Der Befund hält also auch ohne die Liste, an der die Messgrösse entstanden ist.

### Dänemark: signifikant, sobald man die richtige Grösse misst

Die dänische Liste (27 Könige, Gorm der Alte bis zum Interregnum 1332) trägt
dieselbe Struktur wie die norwegische — drei gleich lange Blöcke, von je einem
anderen Namen eingeklammert, fast lückenlos hintereinander. Nur sind es
**8er-Blöcke**:

```
Muster:      ?N ... ?N          Regel: x = 6 (konstant)
Klammern:    Harald / Knut / Waldemar   (alle verschieden)
Abdeckung:   24/27 Namen (89%), 3 ausserhalb, längste Aussenstrecke 2

  j=0    1..8   Harald [Sven Harald Knut Knut Magnus Sven] Harald
  j=1   9..16   Knut [Olaf Erik Niels Erik Erik Sven] Knut
  j=2  19..26   Waldemar [Erik Abel Christoph Erik Erik Christoph] Waldemar
```

Nur **Gorm der Alte, Waldemar I. und Knut VI.** brechen aus der Ordnung aus.

Über sieben Konfigurationen und fünf Startwerte hinweg:

| Konfiguration | Abdeckung | p (bits) | p (coverage) |
|---|---|---|---|
| `--d 0 --max-interruption 2` | 89 % | 0.382 | **0.018** |
| `--d 0 --max-interruption 4` | 89 % | 0.576 | **0.018** |
| `--d 0 --max-interruption 8` | 89 % | 0.774 | **0.017** |
| `--d 0` ohne Schranke | 89 % | 0.864 | **0.017** |
| `--d 0,1 --max-interruption 4` | 89 % | 0.734 | **0.038** |
| `--d 0 -t 1 --max-interruption 4` | 89 % | 0.668 | **0.032** |
| beide Familien | 89 % | 0.795 | **0.044** |

Nach Abdeckung ist der Befund in **jeder** Konfiguration signifikant, über fünf
Startwerte stabil bei p = 0.016–0.022. Nach Bit in keiner.

Bemerkenswert: unter der Abdeckung ist das Ergebnis von `--max-interruption`
praktisch unabhängig (0.017–0.018 für 2, 4, 8 und unbegrenzt). Die Messgrösse
übernimmt die Aufgabe der Schranke — eine Kette mit grossen Lücken hat
automatisch geringe Abdeckung. Wer nach Abdeckung misst, braucht die Schranke
kaum noch.

**Die Liste ist aber nicht die geordnetste mögliche.** Umsortierung 622
(Startwert 42) kachelt sie lückenlos mit drei Blöcken zu je neun Namen — 27 von
27, keine Ausbrecher:

```
ORIGINAL:      [1-8] [9-16] [19-26]     24/27 = 89%,  3 außerhalb
ZUFALL #622:   [0-8] [9-17] [18-26]     27/27 = 100%, 0 außerhalb
```

Der Zufall kann also mehr Ordnung erzeugen als die Geschichtsschreibung — in
etwa 1 von 2000 Fällen.

## Optionen

```
Motiv:
  --family {fixed,bookend,both}  Musterfamilie (Default: both)
  --discover               Anchor und Echo automatisch suchen
  --anchor Konrad,Heinrich Anchor-Motiv (Namen mit Komma getrennt)
  --echo Heinrich          Name, der einen Block schliesst
  --max-anchor-len N       längster Anchor, den die Discovery probiert (Default 2)

Suche:
  --data datei.txt           eigene Liste, ein Name pro Zeile, # = Kommentar
  -t, --max-deviations N     Abweichungsbudget (Default 0)
  --gap-slack N              erlaubter Betrag der x-Abweichung (Default 1)
  --min-blocks N             Mindestlänge einer Kette (Default 3)
  --max-gap N                grösstes zulässiges x (Default 12)
  --max-interruption N       höchstens N Namen zwischen zwei Blöcken
  --d 0,1                    erlaubte Schrittweiten
  --no-skip / --no-gap-slack einzelne Abweichungsarten abschalten
  --raw-names                Einträge unverändert übernehmen

Signifikanz:
  -s, --significance N     gegen N zufällige Umsortierungen prüfen (0 = aus)
  --measure {coverage,bits}  woran gemessen wird (Default: coverage)
  --seed N                 macht Läufe reproduzierbar
  --quiet                  keine Fortschrittsanzeige

  --limit N                wie viele Ketten ausgegeben werden
```

## Stand

Umgesetzt: Kern, Toleranz, Discovery, Signifikanz und beide Musterfamilien.
158 Tests, keine externen Abhängigkeiten (nur stdlib, Tests mit `unittest`),
lauffähig ab Python 3.9.

Mitgelieferte Listen: `HRR_Kings.txt` (31), `Norway_Kings.txt` (34, bis 1380),
`Denmark_Kings.txt` (27, bis 1332), `Scotland_Kings.txt` (27, bis 1292).

Laufzeit auf der Königsliste: Suche unter 1 ms, ein Discovery-Nullmodell rund
1.5 ms je Permutation — 2000 Permutationen also etwa 3 Sekunden.

### Zwei Kennzahlen, zwei Aufgaben

`Chain.score` ist rein strukturell (Kettenlänge minus Strafe je Abweichung) und
kennt die Liste nicht — er dient dem Vergleich *innerhalb* eines Motivs und der
Deduplizierung. `scoring.chain_bits()` gewichtet zusätzlich die Seltenheit der
beteiligten Namen und ist das Rangkriterium *zwischen* Motiven. Der p-Wert ist
die einzige kalibrierte Grösse — nur er berücksichtigt, wie viele Motive
überhaupt geprüft wurden.

### Mögliche Erweiterungen

- Weitere Abweichungsarten aus dem ursprünglichen Entwurf: `ECHO_SUBST`
  (Echo ist ein anderer Name) und `ANCHOR_PARTIAL` (nur ein Teil des
  Anchor-Tupels passt). Das Budget-System in `SearchConfig` ist darauf
  vorbereitet.
- Klammernamen als verschieden *fordern* statt nur zu melden — wäre eine
  weitere Familie; nach der Messung oben würde sie den p-Wert allerdings kaum
  bewegen.
- Andere Schrittweiten als 0 und 1 gehen bereits über `--d` (z.B. `--d -1` für
  schrumpfende Abstände).
