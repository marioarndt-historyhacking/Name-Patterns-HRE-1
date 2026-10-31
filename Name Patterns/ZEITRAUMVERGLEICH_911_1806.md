# Vergleich der HRR-Zeiträume 911–1313 und 1314–1806

## Fragestellung

Die primäre historische Hypothese lautet nicht, dass irgendwann innerhalb der
gesamten Reichsgeschichte irgendein Muster auftritt. Geprüft wird vielmehr, ob
die derzeit erkennbaren Namensmuster im historisch festgelegten Zeitraum
911–1313 ungewöhnlich stark sind und ob diese Struktur im anschließenden
Zeitraum 1314–1806 fehlt oder deutlich schwächer ist.

Die Jahresgrenzen beziehen sich auf das Jahr der ersten Königserhebung. Der
frühe Abschnitt enthält 31, der späte Abschnitt 27 Personen. Die sechs
Herrscher von 843 bis 910 sind nicht Bestandteil dieses Hypothesentests.

## Durchsuchte Musterfamilien

In beiden Zeiträumen gelten exakt dieselben Suchregeln:

1. **FIXED:** Ein ein- oder zweiteiliges Anfangsmotiv und ein Endname bleiben
   über alle Blöcke gleich, zum Beispiel `X, Y, ... , Y` oder `X ... Z`.
2. **BOOKEND:** Jeder Block wird durch denselben Namen eröffnet und beendet;
   dieser Name darf sich aber von Block zu Block ändern, beispielsweise
   `X ... X`, danach `Y ... Y`, danach `Z ... Z`.

Die Suche probiert alle Kandidaten, die häufig genug vorkommen, um mindestens
drei Blöcke bilden zu können. Zugelassen sind konstante Abstände und um eins
wachsende Abstände (`d = 0` oder `d = 1`). In dieser Referenzrechnung werden
keine Abweichungen oder fehlenden Kettenglieder toleriert.

Damit werden alle gegenwärtig im Programm implementierten Musterformen
berücksichtigt. Noch nicht formulierte und daher noch nicht programmierte
Musterformen können naturgemäß nicht in den p-Wert eingehen.

## Drei statistische Prüfungen

### 1. Früher Zeitraum 911–1313

Die Namen dieses Zeitraums werden 10.000-mal untereinander vertauscht. Nach
jeder Vertauschung sucht das Programm erneut das beste FIXED- oder BOOKEND-
Muster, seinen besten Abschnitt, `x0` und die Schrittweite.

Das beobachtete beste Muster ist:

```text
Konrad Heinrich ... Heinrich
x = 3, 4, 5, 6
```

Es umfasst 30 von 31 Listenpositionen. Ergebnis:

```text
p = 0,0160
signifikant bei alpha = 0,05: ja
```

Dieser p-Wert ist bereits für die Auswahl zwischen den beiden Musterfamilien,
die freie Namenswahl und die freie Wahl des Unterintervalls korrigiert.

### 2. Später Zeitraum 1314–1806

Mit genau denselben Regeln findet das Programm keine Kette, die die
Mindestanforderung von drei Blöcken erfüllt. Deshalb gibt es hier keinen
beobachteten Muster-Score und keinen gewöhnlichen oberen Tail-p-Wert. Das
Ergebnis ist als negative Kontrollbeobachtung zu lesen, nicht als Beweis, dass
in der späteren Liste keinerlei denkbare Struktur existiert.

### 3. Direkter Früh–Spät-Vergleich

„Früh signifikant, spät nicht signifikant“ beweist für sich genommen noch
keinen signifikanten Unterschied. Deshalb wird zusätzlich eine direkte
Vergleichsstatistik verwendet:

```text
standardisierte Stärke = Scan-Score / Zahl der Personen im Zeitraum

Differenz = standardisierte Stärke früh
            - standardisierte Stärke spät
```

Beobachtet werden 0,936524 im frühen und 0 im späten Zeitraum, also eine
Differenz von 0,936524.

Für das Vergleichsnullmodell werden alle 58 Namen beider Zeiträume gepoolt,
zufällig auf Gruppen von erneut 31 und 27 Personen verteilt und innerhalb
beider Gruppen vollständig nach FIXED und BOOKEND durchsucht. Dies wird
10.000-mal wiederholt. Geprüft wird gerichtet, ob der frühe Zeitraum stärker
ist als der späte.

```text
p = 0,0009
signifikant bei alpha = 0,05: ja
```

## Interpretation

Unter dem verwendeten Nullmodell sprechen die Ergebnisse dafür, dass die mit
den derzeit implementierten Regeln erkennbare Namensstruktur auf den Zeitraum
911–1313 konzentriert ist:

- Innerhalb von 911–1313 ist der beste, vollkommen frei ausgewählte Befund
  signifikant (`p = 0,0160`).
- Nach 1313 wird keine entsprechende Kette aus mindestens drei Blöcken
  gefunden.
- Die Stärkeverteilung zwischen beiden Zeiträumen ist im direkten Vergleich
  signifikant (`p = 0,0009`).

Der Vergleichs-p-Wert erfasst sowohl Unterschiede der Namenshäufigkeiten als
auch Unterschiede ihrer Reihenfolge. Das ist für die Hypothese einer zeitlich
begrenzten Namensstruktur sinnvoll, bedeutet aber auch: Er trennt nicht
zwischen einem Wechsel des Namensrepertoires und einer besonderen Anordnung
bei gleichbleibendem Repertoire.

## Wichtige Grenzen

- Die Grenze 1313/1314 muss historisch begründet und unabhängig vom errechneten
  Bestwert behandelt werden. Würde man viele Grenzjahre ausprobieren und nur
  das günstigste berichten, müsste diese Grenzwahl ebenfalls in das Nullmodell.
- Unbekannte, noch nicht implementierte Musterfamilien sind nicht korrigiert.
- Das Ergebnis ist keine Wahrscheinlichkeit dafür, dass die Herrscherfolge
  „zufällig“ oder „nicht zufällig“ ist. Es bewertet definierte Teststatistiken
  unter einem konkreten Permutationsnullmodell.
- Dynastien, Erbfolgeregeln, politische Abhängigkeiten und zeitlich wechselnde
  Namensmoden sind im einfachen Permutationsmodell nicht gesondert modelliert.

## Reproduktion

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
