# Namensmuster in der Herrscherfolge des Heiligen Römischen Reiches

## Vergleich der Zeiträume 911–1313 und 1314–1806 sowie die 113-Jahres-Folge der Vorgänger Konrads I.–IV.

**Ausführlicher Arbeitsbericht und Grundlage für einen wissenschaftsnahen Artikel**  
**Stand:** 28. Oktober 2026  
**Untersuchungsgebiet:** ausschließlich das ostfränkische und Heilige Römische Reich

---

## Kurzfassung

Der Bericht untersucht zwei miteinander verbundene Auffälligkeiten in der
Reihenfolge der Könige, Mitkönige und Gegenkönige des ostfränkischen und
Heiligen Römischen Reiches:

1. Im Zeitraum 911–1313 bildet die Namensfolge ein weitgehend geschlossenes
   Kettenmuster. Vier Blöcke beginnen jeweils mit `Konrad, Heinrich` und enden
   mit `Heinrich`. Die Zahl der Namen zwischen Blockanfang und Blockende wächst
   von 3 über 4 und 5 auf 6.
2. Die Todesjahre der jeweiligen Vorgänger Konrads I., II., III. und IV. lauten
   911, 1024, 1137 und 1250. Sie bilden eine exakte arithmetische Folge mit
   dreimal 113 Jahren Abstand.

Die Hauptanalyse vergleicht den historisch abgegrenzten Zeitraum 911–1313 mit
der anschließenden Periode 1314–1806. Die Suche ist nicht auf das bereits
bekannte Konrad-Heinrich-Motiv beschränkt. Sie darf innerhalb der derzeit
implementierten Regeln beliebige Namen, zwei unterschiedliche Musterfamilien,
den günstigsten Unterabschnitt sowie konstante oder um eins wachsende Abstände
auswählen. Sämtliche Auswahlmöglichkeiten werden in den Zufallsdurchläufen
erneut zugelassen.

Die wichtigsten Ergebnisse sind:

| Prüfung | Ergebnis |
|---|---:|
| Vollständige Mustersuche 911–1313 | `p = 0,0160` |
| Mustersuche 1314–1806 | keine zulässige Kette aus mindestens drei Blöcken |
| Direkter Vergleich „früh stärker als spät“ | `p = 0,0009` |
| 113-Jahres-Folge, Konrad und Jahre fest vorgegeben | exakt `p = 0,00000369` |
| 113-Jahres-Folge, Name frei und global korrigiert | exakt `p = 0,00015514` |
| Namenskette und 113-Jahres-Folge gemeinsam | Monte Carlo `p = 0,000097` |

Der gemeinsame Wert beruht auf einer Million Zufallsanordnungen. 96 davon
erzeugten gleichzeitig eine mindestens ebenso starke Namenskette und eine
mindestens ebenso starke Belegung der vier 113-Jahres-Ereignisse. Das
95-%-Wilson-Intervall der Monte-Carlo-Trefferquote beträgt ungefähr
`0,000079–0,000117`.

Diese Ergebnisse sind unter den definierten Permutationsnullmodellen deutlich
signifikant. Sie beweisen weder eine bestimmte historische Ursache noch, dass
die Herrscherfolge im allgemeinen Sinne „nicht zufällig“ sei. Sie zeigen, dass
die konkret definierten Ordnungsmerkmale unter zufälliger Neuverteilung der
beobachteten Namen nur selten mindestens ebenso stark auftreten.

---

## 1. Ausgangspunkt und Forschungsfrage

### 1.1 Die beobachtete Namenskette

Ausgangspunkt ist die Folge der Herrscher zwischen Konrad I. und Heinrich VII.
In vereinheitlichten Rufnamen geschrieben, kann sie in vier Blöcke gegliedert
werden:

```text
Block 1: Konrad Heinrich [Otto Otto Otto] Heinrich
Block 2: Konrad Heinrich [Heinrich Rudolf Hermann Konrad] Heinrich
Block 3: Konrad Heinrich [Friedrich Heinrich Philipp Otto Friedrich] Heinrich
Block 4: Konrad Heinrich [Wilhelm Richard Alfons Rudolf Adolf Albrecht] Heinrich
```

Jeder Block besitzt dieselbe äußere Form:

```text
Konrad, Heinrich + x weitere Namen + Heinrich
```

Die Zahl `x` wächst regelmäßig:

```text
3, 4, 5, 6
```

Formal lautet die Regel:

```text
x(j) = 3 + j
```

`j` ist die bei null beginnende Blocknummer. Der erste Block hat `j = 0` und
damit `x = 3`; der vierte Block hat `j = 3` und damit `x = 6`.

### 1.2 Die historische Periodenhypothese

Die Fragestellung lautet nicht lediglich, ob irgendwo in der langen Geschichte
des Reiches irgendeine auffällige Folge gefunden werden kann. Die zu prüfende
Hypothese ist enger:

> Die erkennbare Namensstruktur ist auf einen mittelalterlichen Zeitraum
> konzentriert, der im HRR von 911 bis 1313 reicht, und setzt sich in der
> anschließenden Zeit bis zum Ende des Reiches nicht in vergleichbarer Stärke
> fort.

Deshalb werden zwei Perioden mit denselben Regeln getrennt untersucht:

- **früher Untersuchungszeitraum:** 911–1313;
- **später Vergleichszeitraum:** 1314–1806.

Die Grenze bezieht sich auf das Jahr der ersten Königserhebung. Heinrich VII.
wurde 1308 erhoben und starb 1313. Die nächste Erhebung in der verwendeten
Liste erfolgte 1314. Das Ende 1806 bezeichnet die Auflösung des Reiches; der
letzte enthaltene Herrscher, Franz II., wurde bereits 1792 erhoben.

### 1.3 Die zweite Beobachtung: dreimal 113 Jahre

Zu dem Namensmuster tritt eine zeitliche Regelmäßigkeit. Betrachtet werden die
Todesjahre der regulären Vorgänger Konrads I. bis IV.:

| Konrad | Vorgänger | Todesjahr |
|---|---|---:|
| Konrad I. | Ludwig IV. das Kind | 911 |
| Konrad II. | Heinrich II. | 1024 |
| Konrad III. | Lothar III. | 1137 |
| Konrad IV. | Friedrich II. | 1250 |

Die Differenzen sind:

```text
1024 − 911  = 113
1137 − 1024 = 113
1250 − 1137 = 113
```

Die Jahreszahlen bilden damit die arithmetische Folge

```text
911, 1024, 1137, 1250.
```

Diese zweite Auffälligkeit ist nicht unabhängig vom Namensmuster, weil beide
auf denselben vier Konraden beruhen. Gerade deshalb ist für eine gemeinsame
Bewertung ein gemeinsamer Permutationstest nötig.

---

## 2. Datengrundlage

### 2.1 Quelle und Reproduzierbarkeit

Die Herrscherliste wurde aus der deutschsprachigen Wikipedia-Seite
[„Liste der römisch-deutschen Herrscher“](https://de.wikipedia.org/wiki/Liste_der_r%C3%B6misch-deutschen_Herrscher)
erzeugt. Der für diese Auswertung gespeicherte Import dokumentiert:

- Wikipedia-Revisions-ID: `271353392`;
- Abrufzeit: 28. Oktober 2026, 06:04:20 UTC;
- SHA-256 der Namensdatei:
  `9ff7e9b5b1b6540ec4935b941137d9ff28a9cb0964ea1aac9153a8bca3ab30b0`.

Die vollständige Liste beginnt 843 nach der Teilung von Verdun und reicht bis
zum Ende des Reiches 1806. Sie enthält 64 Personen.

### 2.2 Aufnahmeregeln

Für die Namensliste gelten folgende Regeln:

1. Sortiert wird nach der ersten Königserhebung.
2. Jede Person erscheint nur einmal.
3. Eine zweite Amtszeit oder eine spätere Anerkennung erzeugt keinen neuen
   Eintrag.
4. Könige, Mitkönige und Gegenkönige werden aufgenommen.
5. Bei nur jahrgenau bekannten Gleichständen gilt die Reihenfolge der
   Wikipedia-Tabelle.
6. Für die Musteranalyse wird der Rufname vereinheitlicht. Beispielsweise
   zählen `Heinrich II.` und `Heinrich VII.` beide als `Heinrich`.
7. Vollständige Namen, Rollen, Erhebungsjahre und Quellenangaben bleiben in der
   CSV-Prüfdatei erhalten.

Diese Trennung ist wichtig: Die statistische Analyse verwendet kurze Rufnamen,
während die historische Prüfung weiterhin auf die konkreten Personen
zurückgreifen kann.

### 2.3 Umfang der Perioden

| Bereich | Zahl der Personen | Verwendung |
|---|---:|---|
| 843–910 | 6 | Kontext und vollständige Ereignisfolge |
| 911–1313 | 31 | primärer Namensmustertest |
| 1314–1806 | 27 | später Vergleichszeitraum |
| 843–1806 insgesamt | 64 | vollständige Herrscherliste |

Die Perioden enthalten unterschiedlich viele Kalenderjahre, aber ähnlich viele
Herrscherpositionen. Statistisch maßgeblich ist für die Namensmuster die
Reihenfolge der Personen, nicht die Dauer ihrer Herrschaft.

### 2.4 Ereignistabelle für die 113-Jahres-Analyse

Die Todesjahresanalyse verwendet eine eigene kontrollierte Tabelle mit 52
regulären Vorgänger-Nachfolger-Zuordnungen von 843 bis 1806. Für jedes Ereignis
werden festgehalten:

- Identität des Vorgängers;
- Todesjahr des Vorgängers;
- stabile Personenkennung des Nachfolgers;
- vereinheitlichter Nachfolgername.

Personen, die ausschließlich Gegenkönige blieben, werden nicht als reguläre
Nachfolger aufgenommen. Ein früherer Gegenkönig, der später regulärer König
wurde, kann für diese spätere Stellung aufgenommen werden. Das betrifft etwa
Konrad III. Konrad IV. war bereits Mitkönig; Friedrich II. wird in der
regulären Zuordnung dennoch als sein Vorgänger geführt.

Historisch ist ergänzend festzuhalten, dass Konrad IV. nach 1250 nicht
unbestritten der einzige König war: Wilhelm von Holland bestand als
Gegenkönig fort. Die statistische Regel behauptet deshalb nicht, Konrad IV. sei
im gesamten Reich konkurrenzlos gewesen. Sie verwendet die dokumentierte
reguläre Vorgängerbeziehung Friedrich II. → Konrad IV.

---

## 3. Welche Muster sucht das Programm?

### 3.1 Blöcke und Ketten

Ein Block ist eine Folge aus einem Anfangsmotiv, einer Zahl von Füllpositionen
und einem Abschluss. Mehrere nicht überlappende Blöcke bilden eine Kette, wenn
die Zahl der Füllpositionen einer einfachen arithmetischen Regel folgt.

```text
x(j) = x0 + j × d
```

- `x0`: Füllzahl des ersten Blocks;
- `j`: Blocknummer;
- `d`: Schrittweite.

In der Referenzanalyse sind `d = 0` und `d = 1` zugelassen:

- `d = 0`: alle Blöcke haben denselben inneren Abstand;
- `d = 1`: der innere Abstand wächst von Block zu Block um eins.

Mindestens drei Blöcke sind erforderlich. In der hier berichteten
Referenzkonfiguration werden keine Abweichungen, ausgelassenen Kettenglieder
oder um eins fehlerhaften Abstände toleriert.

### 3.2 Musterfamilie FIXED

Bei `FIXED` bleiben Anfangsmotiv und Abschlussname in allen Blöcken gleich.

Allgemeines Beispiel:

```text
X, Y ... Z
X, Y .... Z
X, Y ..... Z
```

Das beobachtete HRR-Muster lautet:

```text
Konrad, Heinrich ... Heinrich.
```

Die Discovery-Suche kennt diese Namen nicht im Voraus. Sie probiert alle
ein- und zweiteiligen Anfangsmotive und alle Abschlussnamen, die häufig genug
vorkommen, um mindestens drei Blöcke bilden zu können. Damit sind unter anderem
folgende Formen möglich:

```text
X ... X
X ... Y
X, Y ... Y
X, Y ... Z
```

### 3.3 Musterfamilie BOOKEND

Bei `BOOKEND` wird jeder einzelne Block durch denselben Namen eröffnet und
geschlossen. Der Name darf sich jedoch zwischen den Blöcken ändern:

```text
A [Füllnamen] A
B [Füllnamen] B
C [Füllnamen] C
```

Ein rein fiktives Beispiel mit konstantem Abstand wäre:

```text
Karl    [vier Namen] Karl
Ludwig  [vier Namen] Ludwig
Otto    [vier Namen] Otto
```

Hier wiederholt sich nicht ein konkreter Name, sondern die abstrakte
Klammerstruktur. Diese Familie wird im HRR-Test vollständig mitgesucht, auch
wenn der beobachtete Sieger zur Familie `FIXED` gehört.

### 3.4 Discovery statt nachträglicher Motivfixierung

Der zentrale Unterschied zwischen einer engen und einer global korrigierten
Prüfung lässt sich an zwei Fragen verdeutlichen:

1. **Enge Frage:** Wie selten ist genau das vorher festgelegte Motiv
   `Konrad, Heinrich ... Heinrich`?
2. **Discovery-Frage:** Wie selten ist das beste Muster, wenn das Programm
   Namen, Motivfamilie, Abschnitt und Abstand selbst auswählen darf?

Für die Artikelhauptaussage ist die zweite Frage entscheidend. Alles, was das
Programm in den historischen Daten auswählen darf, darf es deshalb auch in
jeder Zufallspermutation auswählen.

---

## 4. Bewertung der Namensmuster

### 4.1 Abdeckung

Die Abdeckung zählt, wie viele Positionen der Liste innerhalb der Blöcke
liegen. Das beobachtete Muster umfasst 30 von 31 Positionen:

```text
Abdeckung = 30 / 31 ≈ 0,9677 = 96,77 %.
```

Nur eine Position liegt außerhalb der vier Blöcke.

### 4.2 Lokale Dichte und Scan-Score

Ein sehr kurzer perfekter Treffer soll nicht automatisch eine lange, nahezu
geschlossene Struktur übertreffen. Deshalb kombiniert der Scan-Score Länge und
Dichte:

```text
Scan-Score = abgedeckte Positionen
             × lokale Abdeckung
             × Abweichungsfaktor.
```

Da keine Abweichungen zugelassen und beobachtet werden, ist der
Abweichungsfaktor hier 1. Für das HRR-Muster:

```text
Scan-Score = 30 × (30 / 31)
           = 29,032258...
           ≈ 29,0323.
```

Zur Gegenüberstellung unterschiedlich langer Perioden wird zusätzlich durch
die Periodenlänge geteilt:

```text
standardisierte Stärke = 29,0323 / 31
                        ≈ 0,936524.
```

### 4.3 Warum der frühere Wert 0,0015 nicht derselbe Test ist

Eine frühere Auswertung bewertete das Motiv nach seiner Namensseltenheit in
Bit. Sie ergab bei 2.000 Permutationen `p = 0,0015`. Die Bit-Kennzahl belohnt,
dass ein relativ seltenes, zweiteiliges Motiv viermal auftritt.

Die jetzige Hauptanalyse fragt dagegen, wie viel der Liste durch irgendeine
zulässige Struktur geordnet wird. Mit derselben Liste, demselben Seed und 2.000
Permutationen ergibt diese Abdeckungsfrage `p = 0,0155`; mit 10.000
Permutationen stabilisiert sich die Schätzung bei `p = 0,0160`.

Beide Werte sind rechnerisch richtig, beantworten aber verschiedene Fragen:

| Wert | Frage |
|---:|---|
| `p = 0,0015` | Wie selten ist ein mindestens ebenso ungewöhnliches Namensmotiv? |
| `p = 0,0160` | Wie selten ist irgendeine mindestens ebenso starke Listenstruktur? |

Für die allgemeine Mustersuche wird deshalb `0,0160` als Hauptwert verwendet.

---

## 5. Der Monte-Carlo-Permutationstest in verständlicher Form

### 5.1 Grundidee

Die beobachtete Liste enthält Namen mit sehr unterschiedlichen Häufigkeiten.
`Heinrich` kommt häufig vor, andere Namen nur einmal. Ein sinnvoller
Zufallsvergleich darf diese Häufigkeiten nicht verändern.

Der Permutationstest geht daher so vor:

1. Alle Namen bleiben erhalten.
2. Nur ihre Reihenfolge wird zufällig vertauscht.
3. Auf der Zufallsliste läuft dieselbe vollständige Mustersuche.
4. Der beste Zufallsscore wird gespeichert.
5. Der Vorgang wird häufig wiederholt.

Anschaulich entspricht das einem Kartenspiel: Auf den Karten stehen die realen
Herrschernamen. Es werden keine Karten hinzugefügt oder entfernt; der Stapel
wird nur neu gemischt.

### 5.2 Der p-Wert

Der p-Wert ist der Anteil der Zufallslisten, deren bestes Ergebnis mindestens
so stark ist wie das historische Ergebnis. Verwendet wird die Plus-eins-
Korrektur:

```text
p = (Trefferzahl + 1) / (Zahl der Permutationen + 1).
```

Diese Korrektur verhindert einen p-Wert von exakt null. Auch wenn in einer
endlichen Simulation kein Zufallstreffer beobachtet wird, ist die theoretische
Wahrscheinlichkeit nicht bewiesenermaßen null.

### 5.3 Was ein p-Wert nicht bedeutet

Ein p-Wert von `0,0160` bedeutet nicht:

- dass die reale Liste mit 1,6 % Wahrscheinlichkeit zufällig sei;
- dass das Muster mit 98,4 % Wahrscheinlichkeit absichtlich erzeugt worden sei;
- dass eine bestimmte historische Ursache bewiesen sei.

Er bedeutet:

> Unter dem verwendeten Modell zufälliger Namensreihenfolgen erzeugen ungefähr
> 1,6 % der Zufallslisten nach derselben umfassenden Suche einen mindestens
> ebenso hohen Score.

---

## 6. Ergebnis des Zeitraums 911–1313

### 6.1 Gefundenes Muster

Die vollständige Discovery über `FIXED` und `BOOKEND` wählt als stärkstes
Ergebnis erneut:

```text
Konrad Heinrich ... Heinrich
x = 3 + j.
```

Die vier Blöcke lauten nach Listenindizes:

| Block | Indexbereich | x | Blocklänge |
|---:|---:|---:|---:|
| 1 | 0–5 | 3 | 6 Namen |
| 2 | 6–12 | 4 | 7 Namen |
| 3 | 14–21 | 5 | 8 Namen |
| 4 | 22–30 | 6 | 9 Namen |

Die vier Blocklängen wachsen somit ebenfalls regelmäßig von 6 über 7 und 8
auf 9 Namen.

### 6.2 Statistisches Ergebnis

Bei 10.000 Permutationen mit Seed 42 ergibt sich:

```text
beobachteter Scan-Score: 29,0323
p-Wert:                  0,0160
Signifikanzschwelle:     0,05
Ergebnis:                signifikant
```

Der Mittelwert der besten Zufallsscores beträgt 18,2494. Das 95-%-Quantil
liegt bei 26,0357. Der historische Wert 29,0323 liegt damit deutlich oberhalb
des typischen Zufallsbereichs, obwohl einzelne Zufallslisten noch höhere Werte
bis 30 erreichen.

Der p-Wert berücksichtigt bereits:

- freie Wahl der Namen;
- ein- oder zweiteiliges Anfangsmotiv;
- freie Wahl des Abschlussnamens;
- Auswahl zwischen `FIXED` und `BOOKEND`;
- freie Wahl von `x0`;
- Wahl zwischen `d = 0` und `d = 1`;
- freie Wahl des besten Unterintervalls;
- Mindestlänge von drei Blöcken.

---

## 7. Ergebnis des Zeitraums 1314–1806

Auf die 27 Personen des späteren Abschnitts wird exakt dieselbe Suche
angewendet. Unter den festgelegten Anforderungen findet das Programm keine
Kette aus mindestens drei Blöcken.

Das Ergebnis lautet daher nicht „p = 1“ und auch nicht „bewiesene
Musterfreiheit“. Es lautet präzise:

> Keine Struktur aus den derzeit implementierten Familien `FIXED` und
> `BOOKEND` erfüllt im Zeitraum 1314–1806 gleichzeitig die Mindestlänge von
> drei Blöcken, die zugelassenen Schrittweiten und die Nulltoleranz für
> Abweichungen.

Andere, noch nicht programmierte Muster könnten existieren. Auch schwächere
Zweierfolgen werden durch die Mindestanforderung absichtlich nicht als Kette
gewertet.

Der späte Abschnitt dient deshalb als negative historische Kontrollperiode:
Das Verfahren, das im frühen Abschnitt eine nahezu vollständige Struktur
findet, findet unter denselben Regeln später keine zulässige Kette.

---

## 8. Direkter Vergleich beider Zeiträume

### 8.1 Warum zwei getrennte Signifikanzentscheidungen nicht genügen

Aus „früh signifikant“ und „spät nicht signifikant“ folgt nicht automatisch,
dass sich beide Perioden signifikant unterscheiden. Zwei p-Werte knapp auf
unterschiedlichen Seiten von 0,05 könnten nahezu dieselbe Datenlage
repräsentieren.

Deshalb wird die Differenz der standardisierten Musterstärken direkt geprüft:

```text
Differenz = Stärke(911–1313) − Stärke(1314–1806)
          = 0,936524 − 0
          = 0,936524.
```

### 8.2 Nullmodell des Periodenvergleichs

Die 31 frühen und 27 späten Namen werden zusammengelegt. Anschließend werden
sie zufällig auf neue Gruppen derselben Größen verteilt:

```text
31 Namen → künstlicher früher Abschnitt
27 Namen → künstlicher später Abschnitt.
```

In beiden künstlichen Abschnitten läuft wieder die vollständige
`FIXED`-/`BOOKEND`-Discovery. Dieser Vorgang wird 10.000-mal wiederholt.

Gezählt wird, wie häufig die zufällige Differenz mindestens so groß ist wie die
historisch beobachtete Differenz.

### 8.3 Ergebnis

```text
gerichteter Vergleichs-p-Wert: 0,0009
Fragestellung:                  früh stärker als spät
Ergebnis:                       signifikant
```

Der Test spricht somit nicht nur für ein auffälliges Muster im frühen
Zeitraum. Er spricht auch dafür, dass die mit dem derzeitigen Verfahren
messbare Struktur zeitlich auf diesen frühen Abschnitt konzentriert ist.

Das Nullmodell erfasst dabei gemeinsam:

- Unterschiede in der Reihenfolge der Namen;
- Unterschiede in den Namenshäufigkeiten beider Perioden.

Es trennt nicht, welcher Anteil des Ergebnisses auf einer besonderen Anordnung
und welcher auf einem historischen Wandel des Namensrepertoires beruht. Für die
Hypothese einer zeitlich begrenzten Gesamtstruktur ist beides relevant; für
eine kausale Deutung müsste beides später getrennt modelliert werden.

---

## 9. Die 113-Jahres-Folge als eigener statistischer Befund

### 9.1 Allgemeine Ereignisregel

Die Regel wird nicht auf vier Einzelfälle zugeschnitten, sondern allgemein
formuliert:

> Betrachtet wird das Todesjahr des regulären Vorgängers eines Königs, der in
> der betreffenden regulären Herrschaft nicht ausschließlich als Gegenkönig
> geführt wird.

Anschließend wird über alle 52 Ereignisse geprüft, ob mindestens vier
Todesjahre eine exakte arithmetische Folge bilden und auf diesen Positionen
derselbe Nachfolgername steht.

Das Programm darf dabei zunächst frei suchen nach:

- dem Nachfolgernamen;
- dem Anfangsjahr;
- dem Endjahr;
- dem positiven Jahresabstand.

### 9.2 Einzigartigkeit der Jahresfolge

Aus 52 Positionen lassen sich

```text
C(52,4) = 270725
```

Viererauswahlen bilden. Jede dieser Auswahlen wird geprüft. Nur eine einzige
besteht aus vier verschiedenen Jahren mit exakt gleichem Abstand:

```text
911, 1024, 1137, 1250.
```

Auf allen vier Positionen lautet der Nachfolgername `Konrad`.

### 9.3 Gezielter exakter p-Wert

Wenn sowohl der Name Konrad als auch die vier Jahrespositionen als vorher
festgelegt gelten, müssen die vier vorhandenen Konrad-Labels genau diese vier
Positionen besetzen. Unter zufälliger Verteilung der Labels gibt es nur eine
günstige Auswahl:

```text
p = 1 / C(52,4)
  = 1 / 270725
  = 0,0000036938.
```

Das entspricht ungefähr 3,7 günstigen Fällen unter einer Million gleich
wahrscheinlicher Positionsauswahlen.

### 9.4 Global für die Namenswahl korrigierter exakter p-Wert

Da Konrad anhand der historischen Daten aufgefallen ist, ist der gezielte Wert
für die Hauptbewertung zu eng. Jeder andere hinreichend häufige Name muss
ebenfalls die Möglichkeit erhalten, die einzige Viererfolge zu besetzen.

Kommt ein Name `k`-mal vor, gibt es

```text
C(k,4)
```

Möglichkeiten, vier seiner Labels auszuwählen. Über alle Namen summiert
ergeben sich 42 günstige Belegungen. Deshalb:

```text
p_global = 42 / 270725
         = 0,0001551390
         ≈ 0,00015514.
```

Dieser Wert berücksichtigt die freie Namenswahl. Anfangsjahr, Endjahr und
Abstand sind ebenfalls global geprüft, weil alle 270.725 Viererauswahlen
untersucht wurden und nur eine exakte Jahresprogression existiert.

### 9.5 Was dieses Nullmodell prüft

Der Test hält die realen Todesjahre fest und vertauscht die Nachfolgernamen.
Er beantwortet:

> Wie ungewöhnlich ist es, dass die einzige exakte Viererprogression der
> beobachteten Vorgänger-Todesjahre viermal denselben Nachfolgernamen trägt?

Er beantwortet nicht:

> Wie wahrscheinlich ist es biologisch, politisch oder genealogisch, dass
> genau diese Herrscher in diesen Jahren starben?

Für die zweite Frage wäre ein historisch-biologisches Modell von Lebensdauer,
Erhebung, Mitregierung und Nachfolge nötig. Der verwendete bedingte
Permutationstest vermeidet solche schwer begründbaren Annahmen.

### 9.6 Jahreszahlen und exakte Kalendertage

Die Folge ist auf der Ebene der historisch normalisierten Jahreszahlen exakt.
Sie behauptet keine identischen Abstände in Tagen. Die bekannten Todestage
liegen in unterschiedlichen Monaten. Das ist kein Rechenfehler, sondern die
vorab definierte zeitliche Auflösung des Tests: Die Maßeinheit ist das Jahr.

---

## 10. Gemeinsamer p-Wert beider Besonderheiten

### 10.1 Warum die Einzelwerte nicht multipliziert werden dürfen

Eine einfache Multiplikation von

```text
0,0160 × 0,00015514
```

wäre nur unter geeigneten Unabhängigkeitsannahmen zulässig. Diese sind hier
nicht gegeben: Sowohl die Namenskette als auch die Ereignisfolge beruhen auf
den vier Konraden. Eine Zufallsanordnung, die den einen Befund begünstigt, kann
deshalb auch den anderen wahrscheinlicher machen.

### 10.2 Gemeinsames Nullmodell

Der gemeinsame Test verwendet eine Million Permutationen der 31 Namen des
Zeitraums 911–1313. Jede Zufallsanordnung muss zwei Bedingungen gleichzeitig
erfüllen:

1. Die vollständige `FIXED`-/`BOOKEND`-Discovery erreicht mindestens den
   beobachteten Scan-Score 29,0323.
2. Die vier Positionen der 113-Jahres-Ereignisfolge tragen denselben
   Nachfolgernamen.

Erst wenn beide Bedingungen erfüllt sind, zählt die Permutation als Treffer.

### 10.3 Ergebnis

Von einer Million Zufallsanordnungen erfüllen 96 beide Bedingungen. Mit der
Plus-eins-Korrektur:

```text
p_gemeinsam = (96 + 1) / (1.000.000 + 1)
             = 0,0000969999
             ≈ 0,000097.
```

Das entspricht ungefähr einem gemeinsamen Zufallstreffer unter 10.309
Permutationsexperimenten.

Weil der Wert simuliert und nicht kombinatorisch exakt berechnet wird, besitzt
er Monte-Carlo-Unsicherheit. Das Wilson-Intervall für die zugrunde liegende
Trefferquote beträgt bei 95 % Konfidenz ungefähr:

```text
0,000079 bis 0,000117.
```

Auch das obere Ende dieses Intervalls liegt weit unter 0,05.

---

## 11. Gesamtergebnisse im Zusammenhang

| Ebene | Nullhypothese | Ergebnis |
|---|---|---:|
| Frühe Namenskette | Zufällige Reihenfolge derselben 31 Namen; vollständige Mustersuche | `p = 0,0160` |
| Später Abschnitt | Gleiche Suchregeln auf 27 späteren Namen | keine zulässige Dreierkette |
| Periodendifferenz | Zufällige Neuverteilung der 58 Namen auf Gruppen von 31 und 27 | `p = 0,0009` |
| 113 Jahre, gezielt | Vier Konrad-Labels zufällig auf 52 Ereignisse verteilt | exakt `p = 0,00000369` |
| 113 Jahre, global | Beliebiger Nachfolgername darf die Viererfolge besetzen | exakt `p = 0,00015514` |
| Gemeinsamer Befund | Beide Strukturen müssen in derselben Permutation mindestens gleich stark sein | `p = 0,000097` |

Die Werte beantworten unterschiedliche Fragen und sollten nicht gegeneinander
ausgespielt werden. Insbesondere ersetzt der gemeinsame p-Wert nicht die
Einzelanalysen: Er fasst zwei konkrete abhängige Auffälligkeiten zusammen,
während der Periodenvergleich die zeitliche Konzentration der implementierten
Muster untersucht.

---

## 12. Sachgerechte Interpretation

### 12.1 Was die Ergebnisse stützen

Unter den festgelegten Regeln stützen die Ergebnisse folgende Aussagen:

1. Die Namensordnung von 911–1313 ist gemessen am besten frei auswählbaren
   `FIXED`-/`BOOKEND`-Muster ungewöhnlich stark.
2. Eine entsprechende zulässige Kette wird im Zeitraum 1314–1806 nicht
   gefunden.
3. Die standardisierte Musterstärke ist statistisch signifikant auf den frühen
   Zeitraum konzentriert.
4. Die Vorgänger-Todesjahre der vier regulären Konrade bilden eine unter allen
   erfassten Ereignissen einzigartige exakte Viererprogression.
5. Die gleichzeitige Ausprägung von Namenskette und Todesjahresfolge tritt im
   gemeinsamen Permutationsmodell nur sehr selten auf.

### 12.2 Was die Ergebnisse nicht beweisen

Die Analyse beweist nicht:

- eine bewusste historische Planung;
- eine übernatürliche Ursache;
- einen unbekannten allgemeinen Mechanismus;
- die Unabhängigkeit aufeinanderfolgender Herrscher;
- dass nach 1313 keinerlei anderes Muster existiert;
- dass alle denkbaren Musterformen bereits implementiert sind.

Statistische Signifikanz beschreibt die Seltenheit unter einem Nullmodell. Die
historische Erklärung bleibt eine eigenständige Forschungsfrage.

---

## 13. Methodische Grenzen und offene Fragen

### 13.1 Nachträgliche Entdeckung

Das Konrad-Heinrich-Muster und die 113-Jahres-Folge wurden nicht in einer
vollständig unabhängigen Stichprobe vorhergesagt. Die Analysen korrigieren
deshalb möglichst viele tatsächlich verwendete Auswahlmöglichkeiten:

- freie Namen;
- freie Musterfamilie;
- freier Unterabschnitt;
- freie Schrittweite innerhalb der zugelassenen Menge;
- bei der Ereignisfolge freie Namenswahl, freie vier Jahrespositionen und
  freier positiver Abstand.

Unbekannte Suchentscheidungen, die nicht formalisiert wurden, können jedoch
nicht rückwirkend korrigiert werden.

### 13.2 Festlegung der Periodengrenze

Der Vergleich behandelt 1313/1314 als historisch begründete Grenze. Würden
zahlreiche Grenzjahre ausprobiert und anschließend nur das günstigste
berichtet, wäre `p = 0,0009` zu klein. Eine spätere Untersuchung frei wählbarer
Grenzen müsste die Grenzwahl in jeder Permutation wiederholen.

### 13.3 Historische Abhängigkeiten

Herrschernamen sind nicht unabhängig gezogen. Dynastien wiederholen Namen
bewusst, Mitkönige werden häufig innerhalb der Familie erhoben, und
Nachfolgekonflikte verändern die Liste. Das einfache Permutationsmodell
zerstört diese Zusammenhänge.

Das ist für die Frage „Ist die beobachtete Reihenfolge unter freier
Neuanordnung ungewöhnlich?“ angemessen. Für eine Erklärung gegenüber einem
realistischeren dynastischen Zufallsmodell wären zusätzliche Modelle nötig,
etwa Permutationen innerhalb von Dynastien oder Simulationen mit
dynastiespezifischen Namenswahrscheinlichkeiten.

### 13.4 Definition regulärer Nachfolge

Das HRR besitzt keine durchgehend einfache lineare Nachfolge. Teilreiche,
Mitkönigtum, Gegenkönigtum, Absetzung und spätere Anerkennung erzeugen
Grenzfälle. Die Ereignistabelle verwendet deshalb kontrollierte
Vorgängerzuordnungen und schließt ausschließlich als Gegenkönige verbliebene
Nachfolger aus.

Für eine Veröffentlichung sollte die vollständige 52-zeilige Ereignistabelle
als Anhang veröffentlicht und jede Zuordnung historisch belegt werden.

### 13.5 Noch unbekannte Musterfamilien

`FIXED` und `BOOKEND` decken nicht jede denkbare Struktur ab. Beispielsweise
könnten symmetrische, alternierende oder genealogisch definierte Muster später
hinzukommen. Neue Familien vergrößern den Suchraum und erfordern eine erneute
globale Berechnung der p-Werte.

---

## 14. Reproduktion

### 14.1 Herrscherliste erzeugen

```bash
python3 build_ruler_list.py \
  --country hrr --start 843 --end 1806 \
  --refresh --output HRR_Kings_843_1806.txt
```

### 14.2 Periodenvergleich

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

### 14.3 Ereignisfolge und gemeinsamer Test

```bash
python3 -m name_patterns.succession \
  --timeline HRR_Kings_843_1806.csv \
  --trials 1000000 --seed 42 \
  --output HRR_113_Jahre_und_Gesamtsignifikanz.txt
```

### 14.4 Automatisierte Tests

```bash
python3 -m unittest discover -s tests -t .
```

Zum Stand dieses Berichts bestehen 186 automatisierte Tests.

---

## 15. Dateien und Prüfpfad

| Datei | Funktion |
|---|---|
| `HRR_Kings_843_1806.txt` | Namensliste für die Analyse |
| `HRR_Kings_843_1806.csv` | vollständige Namen, Jahre, Rollen und Quellenmetadaten |
| `HRR_Kings_843_1806_Bericht.md` | Import- und Quellenbericht |
| `HRR_911_1313_vs_1314_1806_Periodenvergleich.txt` | numerisches Ergebnis des Periodentests |
| `HRR_113_Jahre_und_Gesamtsignifikanz.txt` | numerisches Ergebnis der Ereignis- und Gesamtprüfung |
| `ZEITRAUMVERGLEICH_911_1806.md` | technische Dokumentation des Periodenvergleichs |
| `EREIGNISFOLGE_113_JAHRE.md` | technische Dokumentation der 113-Jahres-Prüfung |
| `name_patterns/periods.py` | Implementierung des Periodenvergleichs |
| `name_patterns/succession.py` | Ereignistabelle, exakte Kombinatorik und gemeinsamer Test |

---

## 16. Vorschlag für den Aufbau eines späteren Artikels

Aus diesem Bericht lässt sich ein Artikel mit folgender Gliederung entwickeln:

1. **Einleitung:** Beschreibung der beobachteten Namenskette und der
   113-Jahres-Folge.
2. **Historischer Datenbestand:** Auswahlregeln für Könige, Mitkönige und
   Gegenkönige sowie Begründung der Periodengrenze.
3. **Formalisierung:** Definition von Blöcken, Ketten, `FIXED`, `BOOKEND` und
   Vorgänger-Todesjahr-Ereignissen.
4. **Statistische Methoden:** Permutationstest, Scan-Score, Plus-eins-Korrektur,
   exakte Kombinatorik und gemeinsamer Test.
5. **Ergebnisse:** früher Zeitraum, später Zeitraum, direkter Vergleich,
   113-Jahres-Folge und gemeinsamer p-Wert.
6. **Robustheit:** alternative Toleranzen, andere Periodengrenzen,
   dynastiesensitive Nullmodelle und Sensitivitätsanalysen.
7. **Historische Diskussion:** mögliche Bedeutung von Dynastien, Wahlkönigtum,
   Mitkönigtum und Namensmoden.
8. **Grenzen und Ausblick:** noch nicht implementierte Musterfamilien und
   spätere, getrennte Vergleiche mit anderen Reichen.

Für eine Veröffentlichung sollten zusätzlich eine vollständige Tabelle aller
64 Herrscher und aller 52 Vorgängerereignisse, die Softwareversion, der
Quellcode sowie die unveränderten Ergebnisdateien als reproduzierbarer Anhang
bereitgestellt werden.

---

## Schlussfolgerung

Die HRR-Herrscherfolge zeigt im Zeitraum 911–1313 unter den derzeit
implementierten Suchregeln eine statistisch signifikante Namensstruktur. Die
gleiche Suche findet im Zeitraum 1314–1806 keine zulässige Dreierkette; der
direkte Periodenvergleich bestätigt eine signifikante Konzentration auf den
frühen Abschnitt. Zusätzlich bilden die Todesjahre der regulären Vorgänger
Konrads I.–IV. die einzige exakte viergliedrige arithmetische Folge unter 52
kontrollierten Ereignissen. Der gemeinsame Permutationstest für beide
abhängigen Auffälligkeiten ergibt `p = 0,000097`.

Die statistische Aussage ist damit klar: Unter den definierten
Permutationsmodellen ist die gemeinsame Struktur ungewöhnlich. Die Frage nach
ihrer historischen Ursache bleibt offen und muss von der statistischen
Feststellung getrennt untersucht werden.
