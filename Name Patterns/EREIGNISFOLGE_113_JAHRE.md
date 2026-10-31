# Die 113-Jahres-Folge der Vorgänger Konrads I.–IV.

## Beobachtung

Für die vier regulären Könige Konrad I. bis Konrad IV. ergeben sich folgende
Vorgänger-Todesjahre:

| König | Vorgänger | Todesjahr des Vorgängers |
|---|---|---:|
| Konrad I. | Ludwig IV. das Kind | 911 |
| Konrad II. | Heinrich II. | 1024 |
| Konrad III. | Lothar III. | 1137 |
| Konrad IV. | Friedrich II. | 1250 |

Damit gilt exakt auf der Ebene der modern normalisierten Jahreszahlen:

```text
1024 - 911  = 113
1137 - 1024 = 113
1250 - 1137 = 113
```

Konrad III. war früher Gegenkönig, seine hier relevante spätere reguläre
Königsherrschaft wird jedoch nicht als Gegenkönigtum behandelt. Konrad IV. war
bereits Mitkönig; Friedrich II. wird gleichwohl als sein Vorgänger geführt.
Ausschließlich als Gegenkönige verbliebene Nachfolger sind aus der
Ereignistabelle ausgeschlossen.

## Kontrollierte Vergleichsbasis

`name_patterns/succession.py` enthält 52 reguläre Vorgänger-Nachfolger-
Zuordnungen von 843 bis 1806. Für jede Zuordnung werden Vorgänger, Todesjahr,
stabile Personenkennung und Rufname des Nachfolgers festgehalten.

Parallele Teilreiche und konkurrierende reguläre Ansprüche können mehr als
einen Nachfolger desselben Vorgängers erzeugen. Ausschließlich als Gegenkönige
geführte Personen werden dagegen nicht als Nachfolger aufgenommen.

Unter den 52 Todesjahrespositionen existiert genau eine Auswahl von vier
verschiedenen Jahren, die eine exakte arithmetische Folge bildet:

```text
911, 1024, 1137, 1250
```

Auf diesen vier Positionen steht jedes Mal der Nachfolgername `Konrad`.

## Gezielter exakter p-Wert

Das Nullmodell hält alle 52 Ereignisjahre und die beobachteten Häufigkeiten der
Nachfolgernamen fest. Nur die Namen werden zufällig auf die Ereignisse
verteilt.

Wenn `Konrad` und die vier Jahrespositionen als vorab festgelegt gelten, müssen
alle vier vorhandenen Konrad-Labels genau auf diese vier Positionen fallen:

```text
p = 1 / C(52, 4)
  = 1 / 270725
  = 0,0000036938
```

## Global für die Namenswahl korrigierter p-Wert

Da der Name Konrad anhand der Daten aufgefallen ist, wird zusätzlich jedem
anderen hinreichend häufigen Namen gestattet, die einzige Viererfolge zu
belegen. Für einen Namen mit Häufigkeit `k` gibt es `C(k,4)` Möglichkeiten,
vier seiner Labels auf die Folge zu legen. Über alle Namen ergeben sich 42
günstige Belegungen:

```text
p_global = 42 / C(52, 4)
         = 42 / 270725
         = 0,0001551390
```

Dieser Wert korrigiert die freie Namenswahl. Die Wahl von Anfangsjahr und
Abstand ist ebenfalls abgedeckt, weil sämtliche Viererauswahlen der 52
Jahrespositionen untersucht wurden und nur eine davon überhaupt eine exakte
arithmetische Folge bildet.

## Gemeinsamer Test mit dem Namenskettenmuster

Der p-Wert der Namenskette 911–1313 beträgt bei vollständiger FIXED- und
BOOKEND-Discovery `0,0160`. Dieser Wert darf nicht mit dem Ereignis-p-Wert
multipliziert werden, weil beide Befunde dieselben vier Konrade betreffen und
daher abhängig sind.

Stattdessen wird ein gemeinsamer Permutationstest durchgeführt:

1. Die 31 Herrschernamen des Zeitraums 911–1313 werden gemeinsam vertauscht.
2. Die vollständige FIXED-/BOOKEND-Suche wird auf der Zufallsliste wiederholt.
3. Gleichzeitig wird geprüft, ob die vier 113-Jahres-Ereignispositionen
   denselben Nachfolgernamen tragen.
4. Ein Zufallslauf zählt nur, wenn außerdem der Namensketten-Scan-Score
   mindestens den beobachteten Wert erreicht.

Bei einer Million Permutationen mit Seed 42 erfüllen 96 Zufallsanordnungen
beide Bedingungen. Mit Plus-eins-Korrektur:

```text
p_gemeinsam = (96 + 1) / (1.000.000 + 1)
             = 0,0000969999
             ≈ 0,000097
```

Der gemeinsame Befund ist damit an der Schwelle 0,05 deutlich signifikant.

## Interpretation und Grenze des Nullmodells

Der exakte Ereignistest ist ein bedingter Permutationstest. Er hält die
historisch beobachteten Todesjahre fest und prüft, wie ungewöhnlich ihre
Zuordnung zu den Nachfolgernamen ist. Er simuliert nicht die Entstehung von
Todesjahren biologisch oder historisch neu.

Der gemeinsame Test bewertet die konkrete Kombination aus derzeit
implementiertem Namenskettenmuster und exakter Ereignisfolge. Noch unbekannte
Musterfamilien, alternative historische Ereignisdefinitionen und eine
nachträgliche Suche über zahlreiche andere Zeitkennzahlen sind darin nicht
enthalten. Die Ergebnisse sollten deshalb zusammen mit der klar dokumentierten
Definition der Ereignistabelle berichtet werden.
