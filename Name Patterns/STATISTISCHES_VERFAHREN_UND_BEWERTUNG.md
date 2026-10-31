# Statistisches Verfahren und Bewertung der Ergebnisse

## Kurzantwort

Der statistische Kern des Programms ist ein **Monte-Carlo-Permutationstest**.
Das ist ein anerkanntes, nichtparametrisches statistisches Verfahren.

Das Programm vergleicht die in der ursprünglichen Namensliste gefundene
Regelmäßigkeit mit Regelmäßigkeiten, die entstehen, wenn exakt dieselben Namen
viele Male zufällig neu angeordnet werden. So wird geprüft, ob die beobachtete
Ordnung unter einem klar definierten Zufallsmodell ungewöhnlich stark ist.

Die Methode ist grundsätzlich seriös und für diese Fragestellung gut geeignet.
Ihre Aussage ist jedoch enger, als Formulierungen wie „Das Muster ist bewiesen“
vermuten lassen könnten. Ein kleiner p-Wert zeigt eine unter dem Nullmodell
ungewöhnliche Anordnung. Er beweist weder eine historische Ursache noch eine
bewusste Konstruktion der Namensfolge.

## 1. Warum überhaupt ein statistischer Test benötigt wird

In einer längeren Namensliste lassen sich häufig irgendwelche Wiederholungen
finden. Das gilt besonders dann, wenn:

- mehrere Namen oft vorkommen,
- viele mögliche Start- und Endnamen geprüft werden,
- verschiedene Blocklängen erlaubt sind,
- mehrere Schrittweiten untersucht werden,
- Abweichungen oder fehlende Blöcke toleriert werden und
- anschließend nur der beste Treffer betrachtet wird.

Eine gefundene Regelmäßigkeit ist deshalb noch kein Beleg dafür, dass die
Anordnung außergewöhnlich ist. Je größer der Suchraum, desto wahrscheinlicher
ist es, dass der Zufall wenigstens ein scheinbar interessantes Muster liefert.

Der Permutationstest beantwortet daher nicht nur die Frage:

> Gibt es im Original ein Muster?

Sondern die strengere Frage:

> Wie häufig findet genau dieselbe Suchmethode in zufällig umsortierten Listen
> einen mindestens ebenso starken Treffer?

Erst dieser Vergleich macht aus der reinen Mustersuche eine statistische
Bewertung.

## 2. Die Nullhypothese

Jeder statistische Test benötigt eine Nullhypothese. Sie beschreibt den Zustand,
der als Zufall oder als Abwesenheit des untersuchten Effekts gelten soll.

Die Nullhypothese dieses Programms lautet sinngemäß:

> Die Reihenfolge der vorhandenen Namen enthält keine stärkere Regelmäßigkeit,
> als bei einer zufälligen Anordnung derselben Namen zu erwarten wäre.

Wichtig ist die Formulierung „derselben Namen“. Das Programm erzeugt keine
neuen Namen und verändert auch ihre Häufigkeiten nicht. Wenn Heinrich zehnmal,
Konrad viermal und Otto dreimal vorkommt, gilt das in jeder Zufallsliste
weiterhin. Nur die Positionen werden neu verteilt.

Damit werden zwei Dinge konstant gehalten:

1. die Länge der Liste und
2. die Häufigkeitsverteilung der Namen.

Geprüft wird ausschließlich, ob die **Reihenfolge** ungewöhnlich stark geordnet
ist.

## 3. Was „Permutation“ bedeutet

Eine Permutation ist eine andere Reihenfolge derselben Elemente.

Aus der kurzen Liste

```text
A, B, A, C
```

könnten beispielsweise folgende Permutationen entstehen:

```text
C, A, B, A
A, C, A, B
B, A, A, C
```

In jeder Liste kommen weiterhin zwei A, ein B und ein C vor. Deshalb bleibt
die unterschiedliche Häufigkeit der Namen im Zufallstest erhalten.

Der vollständige Permutationstest würde alle unterscheidbaren Anordnungen
berechnen. Deren Zahl wächst jedoch sehr schnell. Bei realen Listen ist eine
vollständige Aufzählung meist unpraktisch. Das Programm zieht deshalb eine
große Zufallsstichprobe möglicher Permutationen. Das ist der
**Monte-Carlo-Anteil** des Verfahrens.

## 4. Ablauf des Monte-Carlo-Permutationstests

Das Verfahren lässt sich in sieben Schritten zusammenfassen.

### Schritt 1: Originaldaten auswerten

Zunächst führt das Programm die Mustersuche auf der ursprünglichen Namensliste
aus. Es bewertet die gefundenen Ketten nach der ausgewählten Messgröße:

- `coverage`: Anteil der Liste, den das Muster abdeckt, oder
- `bits`: frequenzabhängiger Überraschungswert des Motivs.

Der beste beobachtete Wert heißt im Folgenden `T_beobachtet`.

### Schritt 2: Namen zufällig umsortieren

Die Namensliste wird zufällig gemischt. Es entsteht eine Liste mit exakt
denselben Namen und Häufigkeiten, aber einer anderen Reihenfolge.

### Schritt 3: Dieselbe Suche wiederholen

Auf der Zufallsliste wird dieselbe Suchkonfiguration angewandt:

- dieselben Musterfamilien,
- dieselben erlaubten Schrittweiten,
- dieselbe Mindestzahl von Blöcken,
- dieselbe maximale Blocklänge,
- dieselben Unterbrechungsgrenzen und
- dasselbe Abweichungsbudget.

Das ist entscheidend. Der Zufall darf weder strengeren noch großzügigeren
Regeln unterliegen als das Original.

### Schritt 4: Besten Zufallstreffer bestimmen

Aus allen Treffern der Zufallsliste wird der beste Wert ausgewählt. Dieser Wert
heißt beispielsweise `T_zufall,1`.

Es wird nicht nur ein willkürlich ausgewählter Zufallstreffer mit dem Original
verglichen. Der **beste** Zufallstreffer wird verwendet. Dadurch wird
berücksichtigt, dass die Suchmethode viele mögliche Positionen und Motive
prüft.

### Schritt 5: Sehr oft wiederholen

Die Schritte 2 bis 4 werden beispielsweise 2.000-, 5.000- oder 20.000-mal
wiederholt. Dadurch entsteht eine empirische Nullverteilung:

```text
T_zufall,1, T_zufall,2, ..., T_zufall,N
```

Diese Verteilung zeigt, wie stark die besten Muster normalerweise werden, wenn
nur die Reihenfolge zufällig ist.

### Schritt 6: Mindestens gleich gute Zufallstreffer zählen

Ein Zufallsdurchlauf zählt als Treffer, wenn gilt:

```text
T_zufall ≥ T_beobachtet
```

Gleichstände werden also als Zufallserfolg gewertet. Das ist eine konservative
Entscheidung zugunsten der Nullhypothese.

### Schritt 7: p-Wert berechnen

Das Programm verwendet die Formel:

```text
p = (1 + Zahl mindestens gleich guter Zufallstreffer)
    / (1 + Zahl der Permutationen)
```

Diese Plus-Eins-Korrektur ist eine anerkannte Vorgehensweise für
Monte-Carlo-Tests. Sie verhindert, dass bei endlich vielen Zufallsdurchläufen
ein unmöglicherweise exakt sicherer Wert von `p = 0` ausgegeben wird.

## 5. Beispiel für die Berechnung

Angenommen, es werden 2.000 zufällige Umsortierungen erzeugt. In 39 dieser
Listen findet die Suche ein Muster, das mindestens so stark wie das Muster im
Original ist.

Dann ergibt sich:

```text
p = (1 + 39) / (1 + 2000)
  = 40 / 2001
  ≈ 0,020
```

Unter dem verwendeten Nullmodell erreicht der Zufall also in ungefähr zwei
Prozent der Fälle einen mindestens gleich starken Treffer.

Wenn keine einzige der 2.000 Permutationen mithält, lautet der p-Wert nicht
null, sondern:

```text
p = 1 / 2001 ≈ 0,00050
```

Das Ergebnis bedeutet dann lediglich, dass die vorhandene Simulation den
p-Wert nur bis zu dieser Größenordnung auflösen kann. Für eine genauere
Schätzung eines sehr kleinen p-Werts wären mehr Durchläufe erforderlich.

## 6. Warum dieses Verfahren anerkannt ist

Permutationstests gehören zu den etablierten nichtparametrischen
Testverfahren. „Nichtparametrisch“ bedeutet hier, dass keine bestimmte
Normalverteilung oder eine vergleichbare theoretische Form der Messwerte
vorausgesetzt werden muss.

Die Zufallsverteilung der Teststatistik wird unmittelbar aus den vorliegenden
Daten erzeugt. Das ist besonders hilfreich, wenn die Suchstatistik – wie in
diesem Programm – aus einem komplexen Algorithmus stammt und keine einfache
bekannte theoretische Verteilung besitzt.

Für das vorliegende Programm ist das passend, weil sich die Verteilung des
besten Mustertreffers kaum mit einer einfachen Standardformel bestimmen ließe.
Der Suchvorgang umfasst konkurrierende Blöcke, verschiedene Motive,
Schrittweiten, mögliche Abweichungen und eine Auswahl des besten Ergebnisses.
Der Permutationstest kann diesen gesamten Ablauf als geschlossenes Verfahren
behandeln.

## 7. Die Teststatistik: Woran „mindestens so gut“ gemessen wird

Der Permutationstest ist nur der Rahmen. Zusätzlich muss festgelegt werden,
welche Kennzahl die Stärke eines Musters ausdrückt. Das Programm bietet dafür
Abdeckung und Bit-Wert an.

### 7.1 Abdeckung

Die Abdeckung ist der Anteil der Listenpositionen, die innerhalb der Blöcke
einer gefundenen Kette liegen:

```text
Abdeckung = abgedeckte Positionen / alle Positionen
```

Wenn 24 von 27 Namen innerhalb der Blöcke liegen, beträgt sie etwa 89 Prozent.

Abdeckung beantwortet die Frage:

> Wie viel der gesamten Liste wird von der Regelmäßigkeit erfasst?

Dieses Maß berücksichtigt die Blocklänge. Drei lange Blöcke können deshalb
eine höhere Abdeckung als drei kurze Blöcke erreichen.

### 7.2 Bit-Wert

Der Bit-Wert bewertet, wie überraschend das konkrete Motiv angesichts der
Namenshäufigkeiten ist. Seltene Namen erhalten einen größeren Beitrag als sehr
häufige Namen.

Für ein festes Motiv berechnet das Programm vereinfacht:

```text
Bit pro Block = −log2(Produkt der Häufigkeitsanteile
                       der Anchor- und Echo-Namen)
```

Dieser Wert wird mit der effektiven Blockzahl multipliziert. Abweichungen
verringern dabei die effektive Blockzahl.

Bei der freien BOOKEND-Klammer wird nicht ein bestimmter Name vorhergesagt.
Deshalb nutzt das Programm die Wahrscheinlichkeit, dass zwei Positionen
überhaupt denselben Namen tragen. Diese wird durch den Simpson-Index

```text
Summe p(Name)²
```

beschrieben.

### 7.3 Unterschied der beiden Maße

Die beiden Teststatistiken beantworten verschiedene Fragen:

| Messgröße | Hauptfrage |
|---|---|
| Abdeckung | Wie viel der Liste wird strukturell erfasst? |
| Bit | Wie überraschend ist das konkrete Namensmotiv? |

Ein Muster kann einen hohen Bit-Wert, aber geringe Abdeckung besitzen. Ebenso
kann ein großflächiges Muster aus häufigen Namen bestehen und deshalb trotz
hoher Abdeckung einen mäßigen Bit-Wert haben.

Der p-Wert muss deshalb immer zusammen mit seiner Messbasis genannt werden.
Ein „p-Wert des Musters“ ohne Angabe von Abdeckung oder Bit ist unvollständig.

## 8. Automatische Discovery und Mehrfachsuche

Ein zentraler Vorteil der Implementierung ist die Behandlung der automatischen
Motivsuche.

### Vorgegebenes Motiv

Wenn Anchor und Echo bereits vor Betrachtung der Daten feststanden, darf das
Nullmodell nur dieses eine Motiv suchen. Die statistische Frage lautet dann:

> Wie oft würde dieses vorab festgelegte Motiv unter zufälliger Anordnung
> mindestens ebenso gut passen?

### Automatisch gefundenes Motiv

Bei `--discover` werden viele mögliche Motive untersucht und das beste Ergebnis
ausgewählt. Dann muss jede Zufallsumsortierung dieselbe vollständige Discovery
durchlaufen.

Die statistische Frage lautet hier:

> Wie oft würde eine ebenso breite Suche unter zufälliger Anordnung irgendein
> mindestens ebenso gutes Motiv finden?

Das ist deutlich strenger und methodisch richtig. Würde man nach der Discovery
im Nullmodell nur das gewonnene Motiv prüfen, würde man den Auswahlvorteil des
Originals unterschätzen. Der p-Wert wäre dann zu günstig.

## 9. Interpretation der p-Werte

### p kleiner als 0,05

Das Programm bezeichnet `p < 0,05` als statistisch signifikant. Diese
konventionelle Grenze bedeutet:

> Unter dem verwendeten Nullmodell erzeugten weniger als fünf Prozent der
> Zufallsanordnungen einen mindestens ebenso starken Treffer.

Das ist ein Hinweis darauf, dass die ursprüngliche Reihenfolge ungewöhnlich
stark geordnet ist.

### p um 0,05

Ein Ergebnis knapp unter oder über 0,05 sollte nicht als harter Gegensatz
„bewiesen“ gegen „widerlegt“ behandelt werden. Monte-Carlo-p-Werte schwanken
etwas mit der Zufallsstichprobe. Auch die fachliche Plausibilität des
Nullmodells und die vorherige Festlegung der Parameter sind entscheidend.

### Großer p-Wert

Ein großer p-Wert bedeutet, dass zufällige Umsortierungen häufig mindestens
gleich starke Treffer liefern. Das beobachtete Muster hebt sich dann unter der
gewählten Messgröße nicht deutlich vom Zufall ab.

Das beweist nicht, dass überhaupt keine Struktur existiert. Es bedeutet nur,
dass die vorliegende Methode unter dieser Konfiguration keine ungewöhnlich
starke Struktur nachweisen konnte.

## 10. Was der p-Wert nicht bedeutet

Ein p-Wert von 0,02 bedeutet nicht:

- „Die Wahrscheinlichkeit, dass das Muster Zufall ist, beträgt zwei Prozent.“
- „Die historische Hypothese ist mit 98 Prozent Wahrscheinlichkeit wahr.“
- „Das Muster wurde absichtlich erzeugt.“
- „Das Ergebnis wird in anderen Daten sicher wiederkehren.“
- „Es existiert keine alternative Erklärung.“

Der p-Wert ist bedingt auf die Nullhypothese und die verwendete Testmethode. Er
beantwortet:

> Falls die Reihenfolge austauschbar und zufällig wäre, wie häufig würde die
> festgelegte Suchmethode mindestens einen ebenso starken Treffer erzeugen?

Das ist eine wichtige, aber begrenzte Aussage.

## 11. Zentrale Voraussetzung: Austauschbarkeit

Die wichtigste Annahme des Permutationstests ist, dass die Namen unter der
Nullhypothese frei umsortiert werden dürfen. Statistisch wird dies als
**Austauschbarkeit** bezeichnet.

Diese Annahme wäre verletzt oder zumindest fraglich, wenn die Reihenfolge auch
ohne das gesuchte Muster durch andere Mechanismen geprägt ist, zum Beispiel:

- unterschiedliche Namensmoden in verschiedenen Jahrhunderten,
- dynastische Familienabhängigkeiten,
- systematische Wiederverwendung von Namen in bestimmten Zeitabschnitten,
- regionale oder sprachliche Veränderungen,
- redaktionelle Auswahlregeln der Quelle oder
- voneinander abhängige Einträge.

Das aktuelle Nullmodell erhält nur die Gesamthäufigkeit jedes Namens. Es erhält
nicht automatisch zeitliche Häufungen oder dynastische Teilstrukturen.

Falls solche Strukturen fachlich wichtig sind, wäre ein eingeschränktes
Nullmodell denkbar, das beispielsweise nur innerhalb historischer Abschnitte
permutiert. Das wäre jedoch eine andere statistische Fragestellung und müsste
vor der Auswertung fachlich begründet werden.

## 12. Bewertung des Bit-Werts

Der Bit-Wert verwendet ein etabliertes Konzept: den negativen Logarithmus einer
Wahrscheinlichkeit als Informations- oder Überraschungsmaß. Auch der
Simpson-Index für freie Klammern ist ein anerkanntes Maß.

Die konkrete Bit-Berechnung des Programms ist dennoch keine vollständige
Wahrscheinlichkeitsmodellierung der gesamten Liste. Sie multipliziert relative
Namenshäufigkeiten und behandelt die beteiligten Positionen dadurch in
vereinfachter Weise. Abhängigkeiten, Ziehen ohne Zurücklegen und historische
Prozesse werden nicht vollständig modelliert.

Deshalb sollte der Bit-Wert vor allem als nachvollziehbares Rankingmaß für
Motive verstanden werden. Für die eigentliche statistische Absicherung ist der
empirische Permutationstest wichtiger.

## 13. Bewertung der Abdeckungskennzahl

Die Abdeckung ist leicht verständlich und unmittelbar aus den gefundenen
Blöcken berechenbar. Sie ist besonders geeignet, wenn die Forschungsfrage
lautet, wie viel der Listenanordnung durch ein Muster erfasst wird.

Sie ist jedoch eine projektspezifisch gewählte Teststatistik und keine
universelle Standardkennzahl für Namensfolgen. Das ist statistisch nicht
grundsätzlich problematisch: Permutationstests können auch eigens definierte
Teststatistiken korrekt kalibrieren.

Problematisch wäre eine nachträgliche Auswahl allein deshalb, weil diese
Kennzahl für eine bestimmte untersuchte Liste einen günstigen p-Wert erzeugt.
Wurde die Abdeckung an einer Liste entwickelt, ist deren Ergebnis explorativ.
Eine Anwendung derselben unveränderten Kennzahl auf unabhängige neue Listen ist
methodisch deutlich aussagekräftiger.

## 14. Parameterwahl und Mehrfachtests

Das Nullmodell korrigiert die Suche innerhalb **eines festgelegten
Programmlaufs**. Es wiederholt beispielsweise alle erlaubten Motive und
Musterfamilien in jeder Permutation.

Es korrigiert aber nicht automatisch für eine externe Auswahl aus vielen
separaten Analysen. Ein Problem entsteht beispielsweise, wenn nacheinander
zahlreiche Werte für `max_gap`, `d`, `max_interruption`, Abweichungsbudget und
Messgröße ausprobiert werden und anschließend nur der kleinste p-Wert berichtet
wird.

Für eine bestätigende Analyse sollten daher möglichst vorab festgelegt werden:

- die Daten und ihre Normalisierung,
- die Musterfamilie,
- die erlaubten Schrittweiten,
- Mindestzahl und maximale Länge der Blöcke,
- Unterbrechungs- und Abweichungsregeln,
- die Teststatistik sowie
- die Zahl der Permutationen.

Alternativ kann eine explorativ entwickelte Regel unverändert auf einer neuen,
bei der Entwicklung nicht verwendeten Liste geprüft werden.

## 15. Anzahl der Permutationen und Genauigkeit

Mehr Permutationen erhöhen die Präzision der Schätzung. Sie machen das Muster
nicht inhaltlich stärker.

Die kleinstmögliche Ausgabe bei null Zufallstreffern beträgt:

| Permutationen | kleinster p-Wert |
|---:|---:|
| 100 | 1/101 ≈ 0,0099 |
| 500 | 1/501 ≈ 0,0020 |
| 2.000 | 1/2001 ≈ 0,00050 |
| 20.000 | 1/20001 ≈ 0,000050 |

Für eine grobe Einordnung genügen häufig einige Tausend Durchläufe. Liegt das
Ergebnis nahe an einer Entscheidungsgrenze oder sollen sehr kleine p-Werte
geschätzt werden, sind mehr Durchläufe sinnvoll.

Ein fester Seed macht einen Lauf exakt reproduzierbar. Zur Prüfung der
Monte-Carlo-Stabilität kann die Analyse zusätzlich mit mehreren Seeds
wiederholt werden. Diese Wiederholungen ersetzen aber keine unabhängigen Daten.

## 16. Gemeinsame Auswertung mehrerer Listen

Für mehrere Listen verwendet das Programm zwei Verfahren.

### 16.1 Gemeinsamer Permutationstest

Jede Liste wird separat gemischt und separat durchsucht. Anschließend werden
die besten Kennzahlen über die Listen gemittelt. So entstehen eine beobachtete
mittlere Kennzahl und eine Nullverteilung zufälliger Mittelwerte.

Zusätzlich zählt das Programm, wie oft alle Zufallslisten gleichzeitig
mindestens so gut wie ihre jeweiligen Originale sind.

Dieses Verfahren ist grundsätzlich passend, weil keine künstlichen Blöcke über
die Grenzen zweier Listen gebildet werden.

### 16.2 Fishers Methode

Als Gegenprobe kombiniert das Programm die Einzel-p-Werte durch Fishers
Methode:

```text
X² = −2 × Summe ln(p_i)
```

Unter den Voraussetzungen des Verfahrens folgt diese Statistik einer
Chi-Quadrat-Verteilung mit zweimal so vielen Freiheitsgraden wie kombinierten
p-Werten.

Fishers Methode ist ein anerkanntes Standardverfahren. Sie setzt jedoch voraus,
dass die Einzeltests ausreichend unabhängig sind. Historisch oder quellenmäßig
eng verbundene Listen können diese Voraussetzung verletzen.

## 17. Gesamtbewertung des Verfahrens

### Methodische Stärken

1. Der Monte-Carlo-Permutationstest ist ein anerkanntes nichtparametrisches
   Verfahren.
2. Die Häufigkeiten der Namen bleiben im Nullmodell exakt erhalten.
3. Auf Original und Zufallslisten wird dieselbe Suche angewandt.
4. Bei Discovery wird die vollständige Motivsuche in jeder Permutation
   wiederholt.
5. Der beste Zufallstreffer wird mit dem beobachteten Treffer verglichen.
6. Gleichstände zählen zugunsten des Nullmodells.
7. Die Plus-Eins-Korrektur verhindert unzulässige p-Werte von null.
8. Feste Seeds ermöglichen reproduzierbare Ergebnisse.
9. Die gemeinsame Auswertung hält unterschiedliche Listen getrennt.
10. Fishers Methode liefert eine anerkannte analytische Gegenprobe.

### Methodische Grenzen

1. Das Ergebnis hängt von der Austauschbarkeit der Listenpositionen ab.
2. Historische Zeittrends und dynastische Abhängigkeiten sind im einfachen
   Nullmodell nicht enthalten.
3. Die Abdeckungskennzahl und der Suchalgorithmus sind projektspezifisch.
4. Der Bit-Wert ist ein vereinfachtes Überraschungsmaß, kein vollständiges
   generatives Modell.
5. Nachträglich ausprobierte separate Konfigurationen werden nicht gemeinsam
   korrigiert.
6. Eine an Entwicklungsdaten ausgewählte Kennzahl liefert zunächst
   explorative, nicht bestätigende Evidenz.
7. Statistische Signifikanz beweist weder Kausalität noch historische Absicht.
8. Gemeinsame Tests benötigen ausreichend unabhängige Listen.

## 18. Empfohlene Formulierung der Ergebnisse

Eine methodisch angemessene Ergebnisbeschreibung könnte lauten:

> Mit der vorab beschriebenen Mustersuche wurde eine Kette gefunden, die
> 24 von 27 Listenpositionen abdeckt. In 39 von 2.000 zufälligen
> Umsortierungen derselben Namensmenge erreichte die vollständige Suche eine
> mindestens ebenso hohe Abdeckung. Mit Plus-Eins-Korrektur ergibt sich
> p = 0,020. Unter dem verwendeten Permutationsmodell ist die beobachtete
> Anordnung damit ungewöhnlich. Das Ergebnis belegt jedoch keine historische
> Ursache oder bewusste Konstruktion.

Zu vermeiden wären Formulierungen wie:

- „Das Muster ist zu 98 Prozent bewiesen.“
- „Nur mit zwei Prozent Wahrscheinlichkeit ist es Zufall.“
- „Der p-Wert beweist eine absichtliche Ordnung.“
- „Keine Permutation war besser, also ist das Original optimal.“

Wenn in einer endlichen Stichprobe keine Permutation besser war, darf nur
gesagt werden, dass **in dieser Stichprobe** keine bessere gefunden wurde.

## 19. Schlussfolgerung

Der statistische Kern des Programms ist fachlich anerkannt und sinnvoll
implementiert. Der Monte-Carlo-Permutationstest ist gerade deshalb geeignet,
weil die komplexe Verteilung des besten Suchtreffers nicht analytisch bekannt
sein muss. Positiv ist insbesondere, dass die gesamte Such- und
Auswahllogik auch auf jede Zufallsliste angewandt wird.

Die stärkste vertretbare Aussage lautet:

> Das gefundene Muster ist unter dem festgelegten Permutationsmodell und der
> verwendeten Messgröße ungewöhnlich stark.

Weitergehende Aussagen über historische Ursachen, Absicht oder allgemeine
Gesetzmäßigkeiten benötigen zusätzliche fachliche Belege, robuste vorab
festgelegte Analysen und möglichst unabhängige Bestätigungsdaten.
