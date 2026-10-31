# Ausführliche Programmdokumentation: Name Patterns

## 1. Zweck des Programms

Das Programm untersucht geordnete Listen von Namen, zum Beispiel chronologische
Herrscherlisten. Es sucht darin wiederkehrende **Anordnungsstrukturen**. Eine
solche Struktur besteht aus mehreren Blöcken, deren innere Abstände einer
einfachen Regel folgen.

Ein Block der festen Musterfamilie sieht so aus:

```text
Anchor + x Füllnamen + Echo
```

Beispiel:

```text
Konrad Heinrich + 3 andere Namen + Heinrich
```

`Anchor` ist eine zusammenhängende Folge am Blockanfang, `Echo` ein Name am
Blockende und `x` die Zahl der Namen dazwischen. Mehrere Blöcke bilden eine
Kette, wenn ihre `x`-Werte konstant bleiben oder regelmäßig wachsen. Die
historische Beispieldatei enthält etwa die Folge `x = 3, 4, 5, 6`.

Daneben gibt es die freie Klammerfamilie **BOOKEND**:

```text
?N + x Füllnamen + ?N
```

Hier muss der Name am Anfang und Ende *innerhalb eines Blocks* gleich sein. Er
darf jedoch von Block zu Block wechseln. Beispielsweise kann ein Block mit
Olav, der nächste mit Öystein und der dritte mit Hakon eingerahmt sein. Gesucht
wird dann nicht ein bestimmter Name, sondern die abstrakte Klammerstruktur.

Das Programm kann:

1. ein vorgegebenes Muster suchen,
2. Muster automatisch entdecken,
3. kleine Abweichungen tolerieren,
4. Treffer nach Seltenheit oder Listenabdeckung bewerten,
5. die Treffer durch zufällige Umsortierungen statistisch prüfen,
6. mehrere Listen gemeinsam auswerten und
7. die Zufallsumsortierungen in einem lesbaren Bericht sichtbar machen.

## 2. Was das Programm nicht feststellt

Ein gefundener Treffer ist zunächst eine formale Regelmäßigkeit in der
Reihenfolge der Eingabedaten. Auch ein kleiner p-Wert beweist keine historische
Ursache, bewusste Konstruktion oder inhaltliche Abhängigkeit. Er besagt nur,
dass eine mindestens gleich starke formale Ordnung unter dem verwendeten
Nullmodell selten auftrat.

Die Ergebnisse hängen von der Eingabeliste und von den vor der Auswertung
gewählten Suchparametern ab. Insbesondere verändern zusätzliche erlaubte
Musterfamilien, Schrittweiten, Abweichungen oder größere Unterbrechungen den
Suchraum. Ein größerer Suchraum hilft auch Zufallslisten, Treffer zu erzeugen,
und kann daher den p-Wert erhöhen.

## 3. Dateien und Verantwortlichkeiten

| Datei | Aufgabe |
|---|---|
| `name_patterns/data.py` | Eingabedateien lesen, Kommentare entfernen und Namen normalisieren |
| `name_patterns/model.py` | Zentrale Datentypen und Suchkonfiguration definieren |
| `name_patterns/index.py` | Namenspositionen und mögliche Blöcke sammeln |
| `name_patterns/search.py` | Aus Blöcken optimale, nicht überlappende Ketten bilden |
| `name_patterns/discovery.py` | Mögliche feste Motive automatisch erzeugen und durchsuchen |
| `name_patterns/scoring.py` | Seltenheit, Abdeckung, Nullmodell und p-Werte berechnen |
| `name_patterns/report.py` | Ergebnisse als verständlichen Text formatieren |
| `name_patterns/cli.py` | Kommandozeilenoberfläche der normalen Suche |
| `name_patterns/inspect_null.py` | Einzelne Zufallsumsortierungen als Markdown-Tabelle ausgeben |
| `name_patterns/joint.py` | Mehrere Listen getrennt durchsuchen und ihre Evidenz verbinden |
| `tests/` | Automatisierte Prüfungen aller wesentlichen Regeln und Beispielbefunde |
| `build_pdf.sh` | Einen vorhandenen HTML-Bericht über Chrome als PDF drucken |

## 4. Datenfluss vom Aufruf bis zum Ergebnis

Der normale Ablauf ist:

```text
Textdatei oder eingebaute Liste
        ↓
Einlesen und Normalisieren
        ↓
Suchkonfiguration aufbauen
        ↓
Blockkandidaten erzeugen
        ↓
regelmäßige Blockketten suchen
        ↓
inhaltlich gleiche Treffer zusammenfassen
        ↓
nach Abdeckung oder Bit bewerten
        ↓
optional: Nullmodell durch Umsortierungen
        ↓
Textbericht
```

Bei `--discover` wird vor der Blocksuche zusätzlich eine Menge möglicher
Anchor/Echo-Motive erzeugt. Bei `--family bookend` entfällt diese Motiverzeugung,
weil die Klammer eine freie Variable ist.

## 5. Eingabe und Normalisierung

### 5.1 Dateiformat

`load_names()` erwartet eine UTF-8-Textdatei mit einem Eintrag pro Zeile.
Leere Zeilen werden ignoriert. Alles hinter `#` gilt als Kommentar und wird
ebenfalls ignoriert.

### 5.2 Warum Namen gekürzt werden

Standardmäßig zählt nur das erste Wort eines Eintrags als Rufname:

| Eingabe | verwendeter Name |
|---|---|
| `Olav III.` | `Olav` |
| `Friedrich Barbarossa` | `Friedrich` |
| `Inge II. Bardsson` | `Inge` |

Ohne diese Normalisierung wären `Olav I.` und `Olav III.` verschiedene Werte,
obwohl für die untersuchte Struktur derselbe Rufname gemeint ist. Zusätzlich
entfernt `strip_ordinal()` angehängte römische Zahlen wie in `OlavIII.`.

Die Option `--raw-names` schaltet die Kürzung aus. Das kann sinnvoll sein, wenn
vollständige Bezeichnungen bewusst unterschieden werden sollen. Dann ändern
sich jedoch die Häufigkeiten, Blockkandidaten und statistischen Ergebnisse.

### 5.3 Wichtige Konsequenz

Die Normalisierung ist eine fachliche Annahme und nicht bloß Kosmetik. Zwei
verschiedene Personen mit demselben Rufnamen werden für die Mustersuche als
derselbe Name behandelt. Das Programm untersucht Namensformen, nicht
Personenidentitäten.

## 6. Das interne Datenmodell

### 6.1 `Block`

Ein Block speichert:

- `anchor_pos`: Startindex in der Liste,
- `x`: Zahl der Füllnamen,
- `echo_pos`: Endindex,
- `name`: nur bei BOOKEND der gebundene Klammername.

Die Länge eines Blocks ist `echo_pos - anchor_pos + 1`. Bei einem einteiligen
Anchor entspricht sie `x + 2`; bei einem zweiteiligen Anchor `x + 3`.

### 6.2 `Placement`

Ein Placement ordnet einen realen Block einer Sollposition `j` in der Kette
zu. Es speichert außerdem den erwarteten `x`-Wert und gegebenenfalls eine
Abweichung.

### 6.3 `Deviation`

Es gibt zwei Abweichungsarten:

- `GAP_OFF_BY`: Ein Block existiert, aber sein `x` weicht innerhalb der
  erlaubten Toleranz vom Soll ab.
- `SKIP`: An einer Sollposition fehlt ein ganzer Block; die mathematische Folge
  läuft danach weiter.

Beide verbrauchen je einen Punkt aus `max_deviations`.

### 6.4 `Chain`

Eine Kette enthält Motiv, Musterfamilie, Startwert `x0`, Schrittweite `d`, alle
gesetzten Blöcke und Abweichungen. Der vorläufige Suchscore lautet:

```text
Score = Zahl der gesetzten Blöcke
        − deviation_penalty × Zahl der Abweichungen
```

Standardmäßig kostet eine Abweichung 0,5 Punkte. Dieser Score steuert die
Auswahl während der Suche. Er ist nicht mit dem späteren Bit-Wert oder p-Wert
gleichzusetzen.

### 6.5 `SearchConfig`

Die Konfiguration bündelt unter anderem Mindestzahl der Blöcke, maximale
Fülllänge, erlaubte Schrittweiten, Abweichungsbudget, Toleranzbreite,
Unterbrechungsgrenze, maximale Anchor-Länge und Musterfamilien.

## 7. Erzeugung der Blockkandidaten

### 7.1 Feste Motive

`find_anchor_positions()` sucht jedes zusammenhängende Auftreten des Anchors.
Für jeden solchen Start testet `find_blocks()` alle `x` von 0 bis `max_gap`.
Liegt an der berechneten Endposition der Echo-Name, wird ein Blockkandidat
angelegt.

Bewusst werden **alle** Kandidaten gesammelt. Das Programm nimmt nicht einfach
den ersten passenden Endpunkt. Diese Vollständigkeit ist notwendig, weil ein
scheinbarer Blockstart in Wahrheit innerhalb eines später ausgewählten Blocks
liegen kann.

### 7.2 Freie Klammern

`find_bookend_blocks()` gruppiert zunächst alle Positionen nach Namen. Für
jeden Namen werden alle Positionspaare gebildet, deren Abstand `max_gap` nicht
überschreitet. Jedes Paar ist ein Kandidat `Name ... Name`.

Auch hier werden nicht nur benachbarte Vorkommen desselben Namens verwendet.
Ein weiter entferntes Paar kann Teil der besten Gesamtkette sein.

### 7.3 Zulässige Nachfolger

`candidate_range()` bestimmt per Binärsuche, welche Blockstarts nach einem
gewählten Block folgen dürfen:

- Der nächste Start muss hinter dem vorherigen Echo liegen. Blöcke dürfen
  daher nicht überlappen.
- Wenn `max_interruption` gesetzt ist, dürfen höchstens so viele Namen zwischen
  den Blöcken stehen.

Namen zwischen zwei Blöcken sind keine Abweichung. Sie werden nur durch
`max_interruption` begrenzt.

## 8. Kernalgorithmus: dynamische Programmierung

### 8.1 Die mathematische Regel

Für eine Kette ist an Position `j` der erwartete Abstand festgelegt:

```text
erwartetes x(j) = x0 + j × d
```

`d = 0` bedeutet konstante Abstände; `d = 1` bedeutet, dass jeder folgende
Block einen Füllnamen länger ist. Standardmäßig werden beide Werte geprüft.

### 8.2 Warum kein einfacher Durchlauf genügt

Zu einem Anchor können mehrere Echo-Positionen passen. Außerdem können
zusätzliche Anchor- oder Echo-Vorkommen innerhalb eines größeren Blocks liegen.
Eine Entscheidung für den jeweils nächsten Treffer kann deshalb später die
beste Kette verhindern. Die Suche muss Alternativen vergleichen.

### 8.3 Rekursiver Zustand

Die Funktion `_extend()` merkt sich Ergebnisse für den Zustand:

```text
(Endposition des vorigen Blocks, Kettenposition j, Restbudget)
```

`x0` und `d` sind während eines solchen Suchlaufs bereits fest. Für jeden
Zustand wird die beste mögliche Fortsetzung berechnet und im Memo gespeichert.
Wird derselbe Zustand erneut erreicht, kann das gespeicherte Ergebnis sofort
verwendet werden. Das ist dynamische Programmierung beziehungsweise
Memoisierung.

Die Zukunft hängt an der Echo-Position und nicht an der Identität des
vorherigen Blockobjekts: Zwei Kandidaten, die an derselben Stelle enden, haben
dieselben möglichen Nachfolger.

### 8.4 Entscheidungen an einer Kettenposition

Für jeden zulässigen Folgeblock gibt es drei Fälle:

1. `x` entspricht exakt dem Soll: Der Block wird ohne Budgetkosten gesetzt.
2. `x` liegt höchstens `gap_slack` daneben und `GAP_OFF_BY` ist erlaubt: Der
   Block wird gesetzt und kostet einen Abweichungspunkt.
3. Der Block passt nicht: Er wird an dieser Stelle nicht verwendet.

Zusätzlich kann die gesamte Sollposition als `SKIP` ausgelassen werden, sofern
Budget vorhanden ist. Ein Skip am Kettenende wird verworfen, da er keinen
weiteren Block erschließt und nur Budget kosten würde.

### 8.5 Auswahl der besten Fortsetzung

Zuerst gewinnt die Alternative mit mehr gesetzten Blöcken. Bei gleicher
Blockzahl gewinnt die mit weniger Abweichungen. Erst nach Aufbau kompletter
Ketten wird der konfigurierbare Abweichungsabzug im allgemeinen Chain-Score
sichtbar.

### 8.6 Verhalten nach einem Ausreißer

Die Folge wird immer anhand des **Sollwerts** fortgesetzt. Bei Sollwerten
`3, 4, 5, 6` und Messwerten `3, 4, 6, 6` ist nur der dritte Block abweichend.
Der vierte Sollwert bleibt 6. Würde man stattdessen vom gemessenen Ausreißer
weiterrechnen, entstünde fälschlich der nächste Sollwert 7.

### 8.7 Deduplizierung

Nach der Suche werden Ketten nach Score, Abweichungszahl, Start und
Schrittweite sortiert. Eine Kette wird entfernt, wenn alle ihre Anchor-Positionen
bereits vollständig in einer besseren Kette enthalten sind.

## 9. Automatische Motiventdeckung

Für FIXED bildet `candidate_motifs()` mögliche Anchor/Echo-Paare. Als Anchor
dienen zusammenhängende n-Gramme bis `max_anchor_len`; als Echo einzelne Namen.

Der Suchraum wird durch zwei verlustfreie Regeln reduziert:

- Ein Anchor muss mindestens `min_blocks`-mal vorkommen.
- Ein Echo muss mindestens `min_blocks`-mal vorkommen.

Ein selteneres Element kann schon logisch keine Kette mit der geforderten
Blockzahl bilden. Diese Filter sind daher keine ungefähren Heuristiken.

Für jedes verbleibende Paar läuft die vollständige Kettensuche. BOOKEND braucht
keine Motivliste, da dort nur die Gleichheit der beiden Klammern verlangt wird.

`collapse_restatements()` fasst danach Treffer zusammen, die dieselben
Echo-Positionen und dieselbe Schrittweite beschreiben. Wenn etwa ein einteiliger
und ein zweiteiliger Anchor dieselbe Regelmäßigkeit wiedergeben, bleibt wegen
der Sortierung die spezifischere Variante mit längerem Anchor erhalten.

## 10. Bewertungsmethoden

### 10.1 Abdeckung

Alle Positionen innerhalb aller ausgewählten Blöcke gelten als abgedeckt,
einschließlich Anchor und Echo. Da sich Kettenblöcke nicht überlappen, ist die
Abdeckung anschaulich die Summe ihrer Längen geteilt durch die Listenlänge:

```text
Abdeckung = Zahl abgedeckter Positionen / Zahl aller Positionen
```

Zusätzlich werden die Zahl nicht abgedeckter Positionen und die längste
zusammenhängende Außenstrecke ermittelt. Diese Außenstrecke berücksichtigt auch
Namen vor dem ersten und nach dem letzten Block.

Abdeckung beantwortet: **Wie viel der gesamten Liste wird von der gefundenen
Struktur erfasst?** Lange Blöcke zählen deshalb stärker als kurze.

### 10.2 Bit-Wert eines festen Motivs

Zunächst wird für jeden Namen seine relative Häufigkeit berechnet:

```text
p(Name) = Anzahl des Namens / Listenlänge
```

Für einen festen Block wird das Produkt der Wahrscheinlichkeiten aller
Anchor-Namen und des Echo-Namens gebildet. Der Überraschungswert lautet:

```text
Bit pro Block = −log2(Produkt der beteiligten Namenswahrscheinlichkeiten)
```

Seltene Namen und längere Anchor ergeben mehr Bit. Der Kettenwert ist:

```text
Chain-Bit = max(0, Chain-Score) × Bit pro Block
```

Der Bit-Wert beantwortet: **Wie überraschend ist dieses konkrete Motiv unter
den beobachteten Namenshäufigkeiten?** Die Länge der Füllstrecke geht nicht ein.

### 10.3 Bit-Wert einer freien Klammer

Bei BOOKEND ist kein bestimmter Name vorgeschrieben. Relevant ist die
Wahrscheinlichkeit, dass zwei zufällig betrachtete Positionen denselben Namen
tragen. Dafür verwendet das Programm den Simpson-Index:

```text
Kollisionswahrscheinlichkeit = Summe über alle Namen von p(Name)²
Bit pro Klammer = −log2(Kollisionswahrscheinlichkeit)
```

Das verhindert, dass eine freie Klammer so bewertet wird, als sei ein ganz
bestimmter seltener Name vorhergesagt worden.

### 10.4 Ranking

Bei `--measure coverage` wird zuerst nach größerer Abdeckung, dann nach mehr
Bit und schließlich nach früherem Start sortiert. Bei `--measure bits` wird
zuerst nach Bit, dann nach Chain-Score und Start sortiert.

Die beiden Maße dürfen nicht verwechselt werden. Eine kurze, seltene
Namenskombination kann viel Bit haben, aber nur einen kleinen Teil der Liste
erklären. Eine lange Klammerstruktur kann viel abdecken, obwohl ihre Namen
häufig sind.

## 11. Monte-Carlo-Nullmodell und p-Wert

### 11.1 Grundidee

Das Nullmodell mischt dieselbe Namensliste wiederholt zufällig durch. Dabei
bleiben Listenlänge und Häufigkeit jedes Namens exakt erhalten. Verändert wird
nur die Reihenfolge.

In jeder Umsortierung läuft dieselbe Suche mit denselben Parametern. Gespeichert
wird jeweils der **beste** Zufallstreffer nach der gewählten Messgröße. Dadurch
berücksichtigt die Prüfung automatisch, dass innerhalb eines Durchlaufs viele
Positionen und – bei Discovery – viele Motive ausprobiert werden.

### 11.2 Vorgegebenes Motiv oder Discovery

Wenn das Motiv vor der Analyse feststand, kann das Nullmodell nur dieses Motiv
prüfen. Wurde es jedoch erst durch `--discover` gefunden, muss jede
Zufallsumsortierung ebenfalls die volle Discovery durchlaufen. Andernfalls
würde der p-Wert den Auswahlvorteil des nachträglich besten Motivs ignorieren.

### 11.3 Berechnung des p-Werts

Als Treffer zählt jede Permutation, deren bester Wert mindestens so groß wie
der beobachtete Wert ist. Gleichstände zählen also gegen den Befund.

```text
p = (1 + Zahl der Zufallstreffer) / (1 + Zahl der Durchläufe)
```

Die Plus-Eins-Korrektur verhindert die falsche Aussage `p = 0`. Bei 2.000
Durchläufen ist der kleinste mögliche ausgegebene Wert `1/2001`.

`p < 0,05` wird im Bericht als signifikant bezeichnet. Diese Schwelle ist eine
Konvention und kein Naturgesetz. Der p-Wert ist auch keine Wahrscheinlichkeit,
dass der gefundene Zusammenhang „wahr“ ist.

### 11.4 Startwert und Reproduzierbarkeit

`--seed` initialisiert den Pseudozufallszahlengenerator. Gleiche Daten,
Parameter, Durchlaufzahl und gleicher Seed erzeugen dieselbe Nullverteilung.
Ohne festen Seed kann das Ergebnis leicht schwanken.

Mehr Durchläufe verbessern die Genauigkeit der Monte-Carlo-Schätzung. Sie
ändern nicht die Information in der Ursprungsliste und machen einen Befund
nicht an sich stärker.

## 12. Sichtprüfung des Nullmodells

`name_patterns.inspect_null` erzeugt eine Markdown-Tabelle mit Original und
Umsortierungen. Klammerpositionen gefundener Ketten werden fett markiert. Ein
Häkchen kennzeichnet eine Umsortierung, die unter dem gewählten Maß mindestens
den Originalwert erreicht. Ein Stern verlangt zusätzlich dieselbe Blocklänge
und Schrittweite.

`--trials` steuert die Zahl sichtbarer Tabellenzeilen; `--stats-trials` kann
für die Statistik eine größere Zahl verwenden. Die Permutationen werden in
derselben Reihenfolge wie im normalen Nullmodell erzeugt.

## 13. Gemeinsame Auswertung mehrerer Listen

`joint.py` hängt die Listen ausdrücklich **nicht** zusammen. Jede Liste wird
für sich durchsucht, damit niemals ein Block über eine Listengrenze reicht.

### 13.1 Gemeinsamer Permutationstest

In jedem Durchlauf wird jede Liste separat gemischt und separat ausgewertet.
Anschließend wird der Mittelwert ihrer besten Kennzahlen gebildet. Der
beobachtete Mittelwert wird mit dieser Nullverteilung verglichen.

Zusätzlich zählt `p_all`, wie oft alle Zufallslisten im selben Durchlauf ihren
jeweiligen beobachteten Wert erreichen oder übertreffen.

### 13.2 Fishers Methode

Als analytische Gegenprobe werden die Einzel-p-Werte kombiniert:

```text
Fisher-Statistik = −2 × Summe von ln(p_i)
```

Unter den Voraussetzungen der Methode folgt diese Größe näherungsweise einer
Chi-Quadrat-Verteilung mit `2 × Zahl der Listen` Freiheitsgraden. Da dieser Wert
immer gerade ist, berechnet das Programm die Überlebenswahrscheinlichkeit durch
eine endliche Reihe und benötigt dafür kein SciPy.

Beide gemeinsamen Verfahren setzen voraus, dass die Listen voneinander
unabhängig genug sind. Überlappende Quellen oder gegenseitige historische
Abhängigkeiten können diese Voraussetzung verletzen.

## 14. Kommandozeile

Einfacher Start mit eingebauten HRR-Daten:

```bash
python3 -m name_patterns.cli
```

Automatische Suche mit 2.000 Zufallsumsortierungen:

```bash
python3 -m name_patterns.cli --discover --significance 2000 --seed 42
```

BOOKEND auf einer Datei mit konstantem `x` und höchstens vier Namen zwischen
Blöcken:

```bash
python3 -m name_patterns.cli --data Norway_Kings.txt \
  --family bookend --d 0 --max-interruption 4 \
  --significance 2000 --seed 42
```

Wichtige Parameter:

| Option | Bedeutung |
|---|---|
| `--data DATEI` | eigene Liste statt eingebauter Beispieldaten |
| `--discover` | Motiv automatisch suchen |
| `--anchor`, `--echo` | festes Motiv vorgeben |
| `--family` | `fixed`, `bookend` oder `both` |
| `--min-blocks` | Mindestzahl real gesetzter Blöcke |
| `--max-gap` | größtes zulässiges `x` eines Kandidaten |
| `--d` | erlaubte Schrittweiten, z. B. `0,1` |
| `--max-deviations` | gemeinsames Budget für Gap-Abweichungen und Skips |
| `--gap-slack` | größter Betrag einer tolerierten `x`-Abweichung |
| `--no-skip` | fehlende Kettenglieder verbieten |
| `--no-gap-slack` | abweichende `x`-Werte verbieten |
| `--max-interruption` | höchstens so viele Namen zwischen gesetzten Blöcken |
| `--measure` | `coverage` oder `bits` |
| `--significance N` | Zahl der Nullmodell-Durchläufe; 0 deaktiviert sie |
| `--seed` | reproduzierbarer Zufallsstartwert |
| `--limit` | Zahl der angezeigten Treffer |

## 15. Tests und geprüfte Eigenschaften

Die Testsuite umfasst 158 Tests. Zum Zeitpunkt dieser Dokumentation laufen
alle erfolgreich mit:

```bash
python3 -m unittest discover -s tests -t .
```

Geprüft werden unter anderem:

- Laden und Normalisieren von Namen,
- vollständige Kandidatensammlung,
- Überlappungsverbot und Unterbrechungsgrenzen,
- konstante und wachsende Folgen,
- beide Abweichungsarten,
- Fortsetzung am Sollwert nach einem Ausreißer,
- feste und freie Musterfamilie,
- verlustfreie Discovery-Filter und Zusammenfassung gleicher Befunde,
- Abdeckung, Außenpositionen und längste Außenstrecke,
- Bit-Formeln und Simpson-Index,
- Reproduzierbarkeit des Nullmodells,
- Plus-Eins-p-Werte und Gleichstandsbehandlung,
- bekannte Beispielbefunde für HRR, Dänemark, Norwegen und Schottland,
- gemeinsame Permutation und Fishers Methode.

Tests zeigen, dass die Implementierung die spezifizierten Regeln erfüllt. Sie
belegen nicht, dass die fachlichen Annahmen für jede denkbare historische oder
linguistische Fragestellung passend sind.

## 16. Grenzen und methodische Vorsicht

1. **Austauschbarkeit im Nullmodell:** Das Mischen setzt voraus, dass unter der
   Nullhypothese jede Reihenfolge der vorhandenen Namen als Vergleich dienen
   darf. Zeitliche Trends oder dynastische Häufungen werden nicht gesondert
   modelliert.
2. **Namensnormalisierung:** Nur der erste Token zählt. Gleichnamige Personen
   werden zusammengelegt; alternative Schreibweisen werden nicht automatisch
   harmonisiert.
3. **Parameterwahl:** Werden Parameter nach Sichtung der Ergebnisse geändert,
   ist die Analyse explorativ. Ein bestätigender Test sollte Regeln möglichst
   vorher festlegen oder auf neuen Daten wiederholen.
4. **Mehrfachsuche:** Die volle Discovery wird im Nullmodell korrekt
   wiederholt. Manuelle Auswahl zwischen vielen separat ausgeführten
   Konfigurationen wird dagegen nicht automatisch korrigiert.
5. **Bit-Näherung:** Die Multiplikation relativer Namenshäufigkeiten ist ein
   verständliches Überraschungsmaß, aber kein vollständiges generatives Modell
   einer Ziehung ohne Zurücklegen. Der permutationbasierte p-Wert ist deshalb
   die wichtigere empirische Kontrolle.
6. **Signifikanz ist keine Wirkung:** Ein kleiner p-Wert misst Ungewöhnlichkeit
   relativ zum Modell, nicht Größe, historische Bedeutung oder Kausalität.
7. **Unabhängigkeit mehrerer Listen:** Die gemeinsame Auswertung ist nur dann
   sauber interpretierbar, wenn die Listen nicht lediglich Varianten derselben
   Quelle oder stark voneinander abhängig sind.
8. **Rechenaufwand:** Discovery und viele Permutationen wiederholen die gesamte
   Suche. Große Listen, große `max_gap`-Werte, lange Anchor und weite
   Toleranzen können die Laufzeit stark erhöhen.

## 17. Zusammenfassung

Das Programm ist eine mehrstufige Mustersuche für geordnete Namenslisten. Es
sammelt zunächst alle möglichen Blöcke, findet daraus mit dynamischer
Programmierung die besten nicht überlappenden arithmetischen Ketten und kann
dabei genau definierte Abweichungen zulassen. Die Resultate werden entweder
nach erklärter Listenabdeckung oder nach einem frequenzabhängigen Bit-Maß
geordnet. Ein Permutationstest vergleicht den besten beobachteten Treffer mit
den besten Treffern in zufällig umsortierten Versionen derselben Namensmenge.

Die technische Stärke liegt darin, dass Alternativen vollständig verglichen,
Discovery-Effekte im Nullmodell wiederholt und zwei semantisch verschiedene
Musterfamilien mit demselben Suchkern behandelt werden. Die fachlich wichtigste
Vorsicht besteht darin, formale statistische Ungewöhnlichkeit nicht als Beweis
für einen historischen Entstehungsmechanismus zu interpretieren.
