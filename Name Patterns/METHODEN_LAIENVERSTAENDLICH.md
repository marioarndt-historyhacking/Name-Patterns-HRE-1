# Die Auswertungsmethoden – allgemeinverständlich erklärt

## Die Grundfrage

Stellen Sie sich eine lange Reihe von Namen vor. Das Programm fragt nicht nur:
„Welcher Name kommt häufig vor?“, sondern:

> Tauchen bestimmte Namen oder Namensklammern mehrmals in einem regelmäßigen
> Abstandsschema auf?

Ein vereinfachtes Beispiel:

```text
A ... 3 Namen ... B
A ... 4 Namen ... B
A ... 5 Namen ... B
A ... 6 Namen ... B
```

Die vier Abschnitte werden als Blöcke betrachtet. Ihre Zwischenräume wachsen
regelmäßig: 3, 4, 5, 6. Das ist das gesuchte Muster.

## Zwei Arten von Mustern

### 1. Festes Motiv

Anfang und Ende sind vorgegeben und bleiben gleich. Zum Beispiel beginnt jeder
Block mit `Konrad Heinrich` und endet mit `Heinrich`.

Das ist vergleichbar mit einem Gedicht, in dem mehrere Strophen mit derselben
Wortfolge anfangen und demselben Wort enden.

### 2. Freie Klammer

Jeder Block beginnt und endet mit demselben Namen, aber der Name darf im
nächsten Block wechseln:

```text
Olav ... Olav
Öystein ... Öystein
Hakon ... Hakon
```

Hier wiederholt sich die Bauform, nicht der konkrete Name. Vergleichbar wäre
eine Reihe von Schachteln, bei denen Deckel und Boden jeder einzelnen Schachtel
dieselbe Farbe haben, die Farbe zwischen den Schachteln aber wechseln darf.

## Warum das Programm alle Möglichkeiten betrachtet

Ein Name kann mehrfach vorkommen. Dadurch sind oft mehrere Blockenden denkbar.
Wer immer nur den nächsten passenden Namen nimmt, kann sich früh falsch
entscheiden und das größere Muster verpassen.

Das Programm sammelt deshalb zunächst alle plausiblen Blöcke. Danach vergleicht
es systematisch, welche Kombination die beste zusammenhängende Kette ergibt.
Bereits gelöste Teilprobleme merkt es sich. In der Informatik heißt dieses
Verfahren „dynamische Programmierung“.

Eine alltagsnahe Analogie ist eine Routenplanung: An einer Kreuzung wird nicht
blind die zuerst sichtbare Straße genommen. Mehrere Fortsetzungen werden
verglichen, und bekannte Teilstrecken müssen nicht immer neu berechnet werden.

## Welche Regel die Abstände erfüllen

Für die erste Blockposition gilt ein Startwert `x0`. Danach kommt pro Schritt
ein fester Betrag `d` hinzu:

```text
x = x0 + Position × d
```

- `d = 0`: alle Blöcke haben gleich viele Füllnamen.
- `d = 1`: jeder folgende Block hat einen Füllnamen mehr.

Andere Schrittweiten können ebenfalls eingestellt werden.

## Wie kleine Fehler behandelt werden

Reale Daten sind selten vollkommen sauber. Das Programm kann daher ein
begrenztes Fehlerbudget erhalten.

Es kennt zwei Fehlerarten:

1. **Abstand knapp daneben:** Statt der erwarteten 5 stehen etwa 6 Namen im
   Block.
2. **Ganzes Glied fehlt:** Die erwartete Stufe 5 fehlt, aber eine spätere Stufe
   6 ist vorhanden.

Jeder solche Fall verbraucht einen Punkt des Budgets. Entscheidend ist: Nach
einem Ausreißer orientiert sich das Programm weiter am ursprünglichen Plan.
Aus der Sollfolge 3, 4, 5, 6 wird durch einen gemessenen Wert 6 an dritter
Stelle nicht plötzlich 3, 4, 6, 7.

Namen, die zwischen zwei vollständigen Blöcken stehen, gelten nicht automatisch
als Fehler. Optional kann man aber begrenzen, wie groß diese Unterbrechungen
sein dürfen.

## Wie ein Treffer bewertet wird

Das Programm verwendet zwei verschiedene Blickwinkel.

### Abdeckung: Wie viel der Liste wird erklärt?

Liegt ein Name innerhalb eines gefundenen Blocks, gilt seine Position als
abgedeckt. Die Abdeckung ist der Anteil aller abgedeckten Positionen an der
gesamten Liste.

Beispiel: Erfassen die Blöcke 24 von 27 Namen, beträgt die Abdeckung ungefähr
89 Prozent.

Dieses Maß bevorzugt Strukturen, die einen großen Teil der Liste umfassen. Drei
lange Blöcke können deshalb stärker sein als drei sehr kurze Blöcke.

Zusätzlich meldet das Programm:

- wie viele Namen außerhalb der Blöcke stehen und
- wie lang die größte ununterbrochene Strecke außerhalb der Blöcke ist.

Das verhindert, dass eine kleine Struktur in der Listenmitte so wirkt, als
erkläre sie die gesamte Liste.

### Bit-Wert: Wie überraschend sind die beteiligten Namen?

Ein häufig vorkommender Name ist leichter zufällig zu treffen als ein seltener.
Der Bit-Wert berücksichtigt diesen Unterschied.

Vereinfacht gilt: Je seltener die verlangten Namen und je mehr passende Blöcke,
desto größer der Überraschungswert. Eine Verdopplung der Unwahrscheinlichkeit
entspricht einem zusätzlichen Bit.

Bei einer freien Klammer darf das Programm nicht so tun, als sei ein bestimmter
seltener Name vorhergesagt worden. Deshalb misst es dort, wie wahrscheinlich
es allgemein ist, zweimal denselben Namen zu ziehen. Wenn wenige Namen die
Liste dominieren, sind gleiche Paare häufig und wenig überraschend. Bei vielen
gleichmäßig verteilten Namen sind sie seltener.

### Warum beide Werte sinnvoll sind

Abdeckung und Bit beantworten verschiedene Fragen:

- **Abdeckung:** Wie viel der Liste folgt der Struktur?
- **Bit:** Wie überraschend ist das Namensmotiv?

Ein Muster kann seltene Namen enthalten, aber nur einen kleinen Listenteil
abdecken. Umgekehrt kann eine großflächige Struktur auf häufigen Namen beruhen.
Darum zeigt der Bericht beide Größen, auch wenn nur eine davon für das Ranking
und den p-Wert ausgewählt wird.

## Wie geprüft wird, ob Zufall eine Erklärung sein könnte

Ein sichtbares Muster ist nicht automatisch bemerkenswert. Wenn viele
Möglichkeiten durchsucht werden, findet man fast immer irgendeine
Regelmäßigkeit.

Das Programm führt daher einen Zufallstest durch:

1. Es nimmt genau dieselben Namen wie im Original.
2. Es mischt nur ihre Reihenfolge.
3. Es führt auf dieser Mischliste dieselbe vollständige Suche aus.
4. Es notiert den besten Zufallstreffer.
5. Es wiederholt dies zum Beispiel 2.000-mal.

Dadurch bleiben alle Namenshäufigkeiten gleich. Geprüft wird nur, ob die
ursprüngliche Reihenfolge ungewöhnlich stark geordnet ist.

## Was der p-Wert bedeutet

Der p-Wert ist der Anteil der Zufallsdurchläufe, die mindestens so gut wie das
Original waren. Wenn beispielsweise ungefähr 2 von 100 Mischungen mithalten,
liegt der p-Wert ungefähr bei 0,02.

Das Programm zählt Gleichstände als Zufallstreffer und addiert aus Vorsicht je
einen künstlichen Treffer und Durchlauf. Deshalb kann es bei endlich vielen
Versuchen niemals exakt `p = 0` melden.

Ein kleiner p-Wert bedeutet:

> Unter diesem konkreten Zufallsmodell war eine mindestens gleich starke
> Ordnung selten.

Er bedeutet **nicht**:

- Die Wahrscheinlichkeit, dass die historische Erklärung wahr ist, beträgt
  98 Prozent.
- Das Muster wurde absichtlich erzeugt.
- Es gibt keine andere inhaltliche oder datenbedingte Erklärung.
- Das Muster wird in einer neuen Liste sicher wiederkehren.

## Warum bei automatischer Suche anders geprüft werden muss

Wenn ein Motiv vor der Untersuchung festgelegt war, genügt es, dieses Motiv in
den Mischlisten zu prüfen.

Wenn das Programm dagegen viele Motive durchsucht und anschließend das beste
zeigt, müssen auch die Mischlisten dieselbe breite Suche durchlaufen. Sonst
würde das Original von der Auswahl aus vielen Chancen profitieren, der Zufall
aber nicht. Die Implementierung berücksichtigt diesen Unterschied.

## Was ein fester Zufallsstartwert bewirkt

Ein `seed` ist eine Startzahl für den Pseudozufallsgenerator. Mit demselben Seed
entstehen dieselben Mischungen. Das macht Analysen reproduzierbar.

Mehr Mischungen liefern eine genauere Schätzung des p-Werts. Sie machen die
Originaldaten aber nicht „signifikanter“. Bei wenigen Durchläufen schwankt die
Schätzung stärker und sehr kleine p-Werte können nur grob aufgelöst werden.

## Wie mehrere Listen gemeinsam geprüft werden

Mehrere Herrscherlisten werden nicht zu einer künstlichen Riesenliste
zusammengefügt. Jede wird getrennt durchsucht. In jedem Zufallsdurchlauf wird
auch jede Liste separat gemischt.

Danach fragt das Programm unter anderem:

- Wie oft erreicht der Zufall eine mindestens ebenso hohe **mittlere** Qualität
  über alle Listen?
- Wie oft sind **alle** Zufallslisten gleichzeitig mindestens so gut wie ihre
  Originale?

Als zweite, mathematische Gegenprobe verbindet es die Einzel-p-Werte mit
Fishers Methode. Stimmen die Ergebnisse beider Wege ungefähr überein, ist das
beruhigend; beide beruhen jedoch weiterhin auf ihren jeweiligen Annahmen.

## Die wichtigsten Annahmen in einfacher Sprache

1. Die Reihenfolge ist die untersuchte Information. Beim Zufallstest darf sie
   vollständig gemischt werden.
2. Nur der Rufname zählt, sofern `--raw-names` nicht gesetzt ist.
3. Die erlaubten Musterformen und Toleranzen bestimmen, was überhaupt als
   Treffer gelten kann.
4. Werden viele Einstellungen ausprobiert und nur die günstigste berichtet,
   ist das Ergebnis weniger streng als ein vorher festgelegter Test.
5. Mehrere gemeinsam ausgewertete Listen sollten hinreichend unabhängig sein.
6. Ein statistisch ungewöhnliches Muster braucht weiterhin eine fachliche
   Interpretation und Quellenkritik.

## Praktische Leseregel für einen Ergebnisbericht

Lesen Sie die Ausgabe in dieser Reihenfolge:

1. **Muster und Regel:** Was wiederholt sich und wie verändert sich `x`?
2. **Blöcke und Abweichungen:** Wie oft tritt es auf und wie viele Ausnahmen
   wurden zugelassen?
3. **Abdeckung:** Wie viel der Liste wird tatsächlich erfasst?
4. **Außenstrecke:** Liegt der Rest verstreut oder als großer ungeklärter
   Abschnitt vor?
5. **Bit:** Ist das konkrete Namensmotiv häufig oder selten?
6. **p-Wert und Messbasis:** Wurde gegen Abdeckung oder Bit verglichen?
7. **Nullmodell:** War es ein vorgegebenes Motiv oder eine volle Discovery?
8. **Parameterwahl:** Waren diese Regeln vorher festgelegt oder erst nach
   Betrachtung der Daten gewählt?

Erst das gemeinsame Bild dieser Angaben erlaubt eine verantwortbare Aussage.
