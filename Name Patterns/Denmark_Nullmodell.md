# Nullmodell-Umsortierungen: Denmark_Kings.txt

Die ersten **100** Permutationen des Signifikanztests, Startwert `42`.

## Was hier geprüft wird

- Liste: 27 Namen aus `Denmark_Kings.txt`
- Familien: bookend
- Schrittweiten `d`: 0
- höchstens 4 Namen zwischen zwei Blöcken
- mindestens 3 Blöcke, Abweichungsbudget 0

Das Nullmodell **permutiert nur**: jede Zeile enthält exakt dieselben Namen wie die Ausgangsliste, in anderer Reihenfolge. Geprüft wird also allein, ob die *Anordnung* bemerkenswert ist.

## Der Befund, gegen den verglichen wird

**3 Blöcke**, x = 6 (konstant), Klammern: Harald / Knut / Waldemar, Unterbrechungen: 0, 2.

Die Kette erfasst **24 von 27 Namen** (89%); 3 brechen aus der Ordnung aus, die längste unstrukturierte Strecke ist 2 Namen lang. Seltenheit: 8.7 Bit.

Zwei Markierungen, weil „gleiche Regelmässigkeit" zweierlei heissen kann:

- **✓** — zählt für den p-Wert: die gleiche Suche erreicht in der Umsortierung mindestens 89% Abdeckung.
- **★** — strenger: die Kette hat zusätzlich dieselbe Blocklänge x = 6 wie die Ausgangsliste.

Der Unterschied ist erheblich, siehe die Auswertung am Ende.

## Die Umsortierungen

Fett gesetzt sind die Namen, die einen Block öffnen oder schliessen.

| # | ✓ | ★ | Abd. | aussen | Blöcke | x | Zwischen | Klammern | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Original** | — | — | 89% | 3 | 3 | 6 | 0, 2 | Harald / Knut / Waldemar | Gorm | **Harald** | Sven | Harald | Knut | Knut | Magnus | Sven | **Harald** | **Knut** | Olaf | Erik | Niels | Erik | Erik | Sven | **Knut** | Waldemar | Knut | **Waldemar** | Erik | Abel | Christoph | Erik | Erik | Christoph | **Waldemar** |
| 1 |  |  | 0% | 27 |  |  |  |  | Knut | Niels | Knut | Waldemar | Waldemar | Magnus | Knut | Olaf | Sven | Christoph | Erik | Knut | Harald | Erik | Erik | Erik | Sven | Waldemar | Christoph | Knut | Abel | Sven | Harald | Erik | Gorm | Harald | Erik |
| 2 |  |  | 44% | 15 |  |  |  |  | Knut | Sven | Harald | Olaf | Knut | Erik | Sven | Gorm | Erik | Christoph | Knut | Erik | Erik | Waldemar | Niels | Waldemar | Abel | Knut | Waldemar | Harald | Erik | Erik | Harald | Magnus | Knut | Sven | Christoph |
| 3 |  |  | 0% | 27 |  |  |  |  | Knut | Knut | Niels | Erik | Erik | Harald | Abel | Waldemar | Erik | Christoph | Knut | Knut | Erik | Olaf | Waldemar | Magnus | Sven | Gorm | Sven | Harald | Sven | Waldemar | Erik | Harald | Erik | Christoph | Knut |
| 4 |  |  | 56% | 12 |  |  |  |  | Magnus | Erik | Sven | Sven | Knut | Christoph | Niels | Abel | Waldemar | Knut | Erik | Knut | Christoph | Knut | Olaf | Knut | Erik | Harald | Erik | Erik | Waldemar | Erik | Waldemar | Gorm | Harald | Sven | Harald |
| 5 |  |  | 44% | 15 |  |  |  |  | Erik | Knut | Knut | Erik | Niels | Harald | Erik | Knut | Magnus | Erik | Sven | Erik | Sven | Sven | Christoph | Harald | Knut | Waldemar | Erik | Harald | Abel | Gorm | Waldemar | Knut | Olaf | Waldemar | Christoph |
| 6 |  |  | 0% | 27 |  |  |  |  | Waldemar | Erik | Harald | Knut | Harald | Erik | Waldemar | Erik | Sven | Olaf | Knut | Knut | Erik | Niels | Knut | Sven | Gorm | Abel | Erik | Erik | Waldemar | Magnus | Knut | Christoph | Harald | Christoph | Sven |
| 7 |  |  | 59% | 11 |  |  |  |  | Niels | Erik | Harald | Christoph | Sven | Harald | Waldemar | Christoph | Erik | Waldemar | Erik | Magnus | Knut | Erik | Sven | Olaf | Knut | Knut | Knut | Sven | Knut | Erik | Waldemar | Gorm | Abel | Erik | Harald |
| 8 |  |  | 0% | 27 |  |  |  |  | Waldemar | Knut | Harald | Erik | Gorm | Sven | Niels | Erik | Olaf | Erik | Christoph | Erik | Sven | Abel | Christoph | Magnus | Knut | Waldemar | Knut | Harald | Waldemar | Erik | Sven | Knut | Erik | Harald | Knut |
| 9 |  |  | 0% | 27 |  |  |  |  | Christoph | Erik | Knut | Harald | Sven | Abel | Niels | Erik | Sven | Waldemar | Olaf | Erik | Magnus | Knut | Gorm | Erik | Knut | Knut | Christoph | Erik | Harald | Erik | Knut | Waldemar | Sven | Harald | Waldemar |
| 10 |  |  | 56% | 12 |  |  |  |  | Sven | Abel | Sven | Christoph | Christoph | Knut | Knut | Waldemar | Niels | Knut | Erik | Sven | Knut | Waldemar | Erik | Erik | Olaf | Magnus | Harald | Harald | Erik | Gorm | Waldemar | Harald | Erik | Knut | Erik |
| 11 |  |  | 0% | 27 |  |  |  |  | Erik | Knut | Erik | Knut | Niels | Christoph | Erik | Gorm | Christoph | Sven | Harald | Olaf | Waldemar | Harald | Erik | Knut | Knut | Harald | Erik | Waldemar | Knut | Waldemar | Sven | Sven | Magnus | Erik | Abel |
| 12 |  |  | 33% | 18 |  |  |  |  | Erik | Sven | Olaf | Harald | Niels | Erik | Gorm | Knut | Knut | Abel | Waldemar | Erik | Sven | Christoph | Erik | Christoph | Knut | Knut | Waldemar | Waldemar | Harald | Magnus | Harald | Erik | Knut | Erik | Sven |
| 13 |  |  | 59% | 11 |  |  |  |  | Sven | Abel | Sven | Harald | Erik | Erik | Knut | Erik | Christoph | Erik | Erik | Harald | Erik | Knut | Niels | Knut | Sven | Gorm | Knut | Waldemar | Knut | Harald | Waldemar | Magnus | Christoph | Olaf | Waldemar |
| 14 |  |  | 44% | 15 |  |  |  |  | Christoph | Abel | Harald | Niels | Waldemar | Erik | Knut | Sven | Erik | Magnus | Harald | Olaf | Waldemar | Knut | Knut | Erik | Erik | Knut | Erik | Waldemar | Harald | Erik | Christoph | Sven | Knut | Gorm | Sven |
| 15 |  |  | 67% | 9 |  |  |  |  | Gorm | Knut | Harald | Erik | Knut | Harald | Knut | Olaf | Waldemar | Erik | Abel | Christoph | Christoph | Sven | Erik | Erik | Erik | Harald | Knut | Waldemar | Magnus | Erik | Waldemar | Knut | Sven | Sven | Niels |
| 16 |  |  | 56% | 12 |  |  |  |  | Erik | Erik | Olaf | Sven | Erik | Knut | Waldemar | Erik | Abel | Christoph | Harald | Erik | Sven | Magnus | Knut | Waldemar | Christoph | Knut | Knut | Knut | Harald | Erik | Gorm | Niels | Sven | Waldemar | Harald |
| 17 |  |  | 78% | 6 |  |  |  |  | Knut | Abel | Knut | Christoph | Sven | Christoph | Knut | Waldemar | Harald | Waldemar | Erik | Erik | Sven | Olaf | Sven | Waldemar | Harald | Harald | Erik | Erik | Magnus | Gorm | Knut | Erik | Erik | Niels | Knut |
| 18 |  |  | 0% | 27 |  |  |  |  | Christoph | Waldemar | Harald | Erik | Sven | Knut | Waldemar | Erik | Sven | Abel | Niels | Christoph | Erik | Olaf | Erik | Knut | Harald | Erik | Magnus | Knut | Harald | Erik | Sven | Knut | Gorm | Knut | Waldemar |
| 19 |  |  | 59% | 11 |  |  |  |  | Knut | Erik | Abel | Sven | Harald | Gorm | Sven | Knut | Knut | Harald | Erik | Erik | Christoph | Erik | Waldemar | Waldemar | Sven | Waldemar | Magnus | Erik | Erik | Harald | Knut | Olaf | Niels | Knut | Christoph |
| 20 |  |  | 0% | 27 |  |  |  |  | Sven | Erik | Gorm | Knut | Erik | Knut | Knut | Erik | Niels | Magnus | Abel | Knut | Waldemar | Erik | Waldemar | Sven | Harald | Waldemar | Christoph | Christoph | Erik | Erik | Harald | Knut | Sven | Harald | Olaf |
| 21 |  |  | 22% | 21 |  |  |  |  | Knut | Waldemar | Sven | Knut | Gorm | Erik | Olaf | Erik | Waldemar | Magnus | Sven | Niels | Erik | Erik | Harald | Knut | Sven | Harald | Knut | Knut | Erik | Waldemar | Abel | Erik | Christoph | Christoph | Harald |
| 22 |  |  | 56% | 12 |  |  |  |  | Waldemar | Sven | Niels | Christoph | Gorm | Erik | Magnus | Abel | Erik | Christoph | Harald | Sven | Waldemar | Knut | Harald | Erik | Erik | Olaf | Knut | Erik | Harald | Sven | Knut | Knut | Erik | Waldemar | Knut |
| 23 |  |  | 0% | 27 |  |  |  |  | Sven | Waldemar | Harald | Christoph | Sven | Erik | Magnus | Knut | Erik | Knut | Waldemar | Niels | Abel | Erik | Erik | Knut | Knut | Knut | Harald | Erik | Olaf | Erik | Sven | Waldemar | Gorm | Harald | Christoph |
| 24 |  |  | 0% | 27 |  |  |  |  | Erik | Sven | Olaf | Erik | Knut | Harald | Waldemar | Abel | Waldemar | Erik | Harald | Niels | Magnus | Christoph | Knut | Sven | Gorm | Knut | Erik | Waldemar | Christoph | Knut | Knut | Sven | Harald | Erik | Erik |
| 25 |  |  | 33% | 18 |  |  |  |  | Harald | Knut | Knut | Knut | Harald | Olaf | Sven | Abel | Erik | Christoph | Gorm | Waldemar | Erik | Erik | Waldemar | Erik | Niels | Knut | Sven | Harald | Sven | Erik | Knut | Erik | Magnus | Christoph | Waldemar |
| 26 |  |  | 0% | 27 |  |  |  |  | Erik | Knut | Erik | Niels | Magnus | Christoph | Knut | Sven | Erik | Waldemar | Abel | Knut | Sven | Waldemar | Knut | Sven | Erik | Harald | Knut | Harald | Harald | Waldemar | Olaf | Erik | Christoph | Erik | Gorm |
| 27 |  |  | 44% | 15 |  |  |  |  | Harald | Waldemar | Christoph | Erik | Magnus | Waldemar | Knut | Olaf | Niels | Erik | Harald | Knut | Erik | Knut | Abel | Sven | Knut | Knut | Harald | Erik | Sven | Erik | Gorm | Waldemar | Erik | Sven | Christoph |
| 28 |  |  | 0% | 27 |  |  |  |  | Olaf | Knut | Christoph | Sven | Sven | Erik | Erik | Knut | Harald | Gorm | Knut | Magnus | Harald | Christoph | Waldemar | Erik | Waldemar | Erik | Waldemar | Knut | Niels | Abel | Knut | Harald | Erik | Erik | Sven |
| 29 |  |  | 30% | 19 |  |  |  |  | Waldemar | Sven | Niels | Gorm | Erik | Erik | Harald | Harald | Erik | Harald | Knut | Knut | Erik | Erik | Olaf | Knut | Waldemar | Christoph | Sven | Christoph | Erik | Magnus | Knut | Waldemar | Sven | Knut | Abel |
| 30 | ✓ | ★ | 89% | 3 | 3 | 6 | 2, 0 | Erik / Harald / Knut | **Erik** | Waldemar | Knut | Sven | Waldemar | Erik | Waldemar | **Erik** | Harald | Erik | **Harald** | Magnus | Gorm | Sven | Knut | Abel | Niels | **Harald** | **Knut** | Erik | Sven | Erik | Olaf | Knut | Christoph | **Knut** | Christoph |
| 31 |  |  | 56% | 12 |  |  |  |  | Gorm | Waldemar | Waldemar | Abel | Erik | Knut | Erik | Knut | Sven | Knut | Sven | Erik | Erik | Christoph | Sven | Knut | Waldemar | Niels | Erik | Harald | Olaf | Erik | Christoph | Harald | Harald | Knut | Magnus |
| 32 |  |  | 0% | 27 |  |  |  |  | Erik | Sven | Harald | Gorm | Waldemar | Erik | Sven | Waldemar | Abel | Olaf | Magnus | Erik | Knut | Harald | Knut | Sven | Christoph | Harald | Waldemar | Niels | Knut | Erik | Erik | Erik | Knut | Knut | Christoph |
| 33 |  |  | 67% | 9 |  |  |  |  | Sven | Harald | Knut | Knut | Waldemar | Knut | Magnus | Erik | Knut | Erik | Erik | Waldemar | Harald | Erik | Harald | Erik | Knut | Gorm | Olaf | Niels | Christoph | Waldemar | Abel | Sven | Erik | Christoph | Sven |
| 34 |  |  | 56% | 12 |  |  |  |  | Knut | Sven | Sven | Knut | Gorm | Waldemar | Erik | Knut | Harald | Magnus | Waldemar | Harald | Erik | Waldemar | Abel | Knut | Erik | Harald | Niels | Christoph | Erik | Olaf | Sven | Knut | Erik | Erik | Christoph |
| 35 |  |  | 22% | 21 |  |  |  |  | Harald | Harald | Erik | Christoph | Waldemar | Sven | Waldemar | Sven | Knut | Knut | Erik | Magnus | Gorm | Niels | Knut | Abel | Erik | Erik | Erik | Erik | Olaf | Christoph | Waldemar | Harald | Knut | Knut | Sven |
| 36 |  |  | 0% | 27 |  |  |  |  | Waldemar | Olaf | Knut | Erik | Erik | Christoph | Waldemar | Gorm | Erik | Harald | Knut | Erik | Magnus | Waldemar | Christoph | Harald | Knut | Abel | Knut | Niels | Harald | Knut | Erik | Erik | Sven | Sven | Sven |
| 37 |  |  | 44% | 15 |  |  |  |  | Knut | Sven | Harald | Knut | Knut | Waldemar | Erik | Waldemar | Erik | Magnus | Waldemar | Knut | Erik | Sven | Niels | Christoph | Sven | Harald | Christoph | Olaf | Knut | Erik | Erik | Erik | Harald | Gorm | Abel |
| 38 |  |  | 67% | 9 |  |  |  |  | Sven | Erik | Sven | Christoph | Magnus | Knut | Abel | Knut | Erik | Erik | Knut | Niels | Waldemar | Harald | Erik | Waldemar | Sven | Gorm | Harald | Knut | Christoph | Erik | Waldemar | Harald | Knut | Erik | Olaf |
| 39 |  |  | 44% | 15 |  |  |  |  | Knut | Waldemar | Harald | Olaf | Niels | Christoph | Erik | Knut | Sven | Erik | Abel | Harald | Sven | Magnus | Knut | Sven | Erik | Erik | Gorm | Waldemar | Erik | Waldemar | Harald | Knut | Knut | Christoph | Erik |
| 40 |  |  | 0% | 27 |  |  |  |  | Magnus | Christoph | Harald | Knut | Knut | Harald | Sven | Erik | Waldemar | Waldemar | Harald | Erik | Gorm | Abel | Knut | Olaf | Sven | Christoph | Erik | Niels | Erik | Sven | Erik | Waldemar | Knut | Knut | Erik |
| 41 |  |  | 0% | 27 |  |  |  |  | Harald | Knut | Christoph | Harald | Knut | Magnus | Erik | Gorm | Erik | Sven | Erik | Sven | Harald | Niels | Knut | Erik | Christoph | Waldemar | Abel | Waldemar | Sven | Waldemar | Erik | Olaf | Knut | Erik | Knut |
| 42 |  |  | 0% | 27 |  |  |  |  | Christoph | Erik | Erik | Erik | Sven | Knut | Christoph | Harald | Waldemar | Gorm | Erik | Niels | Harald | Erik | Magnus | Sven | Waldemar | Knut | Knut | Erik | Waldemar | Abel | Knut | Olaf | Sven | Harald | Knut |
| 43 |  |  | 0% | 27 |  |  |  |  | Christoph | Gorm | Waldemar | Knut | Niels | Knut | Erik | Erik | Christoph | Waldemar | Waldemar | Magnus | Harald | Knut | Erik | Harald | Erik | Knut | Sven | Sven | Abel | Harald | Knut | Sven | Olaf | Erik | Erik |
| 44 |  |  | 0% | 27 |  |  |  |  | Harald | Erik | Erik | Erik | Knut | Christoph | Christoph | Knut | Sven | Niels | Magnus | Erik | Knut | Erik | Waldemar | Gorm | Harald | Olaf | Sven | Knut | Erik | Waldemar | Abel | Harald | Knut | Sven | Waldemar |
| 45 |  |  | 22% | 21 |  |  |  |  | Olaf | Waldemar | Waldemar | Erik | Sven | Christoph | Sven | Christoph | Harald | Gorm | Erik | Erik | Knut | Knut | Abel | Knut | Harald | Knut | Knut | Erik | Waldemar | Erik | Niels | Sven | Magnus | Erik | Harald |
| 46 |  |  | 30% | 19 |  |  |  |  | Knut | Magnus | Erik | Erik | Waldemar | Knut | Knut | Erik | Erik | Sven | Erik | Sven | Knut | Harald | Harald | Waldemar | Christoph | Knut | Gorm | Niels | Olaf | Sven | Erik | Harald | Waldemar | Abel | Christoph |
| 47 |  |  | 33% | 18 |  |  |  |  | Knut | Christoph | Erik | Erik | Erik | Waldemar | Knut | Harald | Knut | Erik | Waldemar | Christoph | Harald | Olaf | Harald | Magnus | Niels | Erik | Abel | Knut | Sven | Sven | Waldemar | Sven | Gorm | Knut | Erik |
| 48 |  |  | 0% | 27 |  |  |  |  | Knut | Knut | Knut | Harald | Harald | Olaf | Waldemar | Sven | Knut | Magnus | Knut | Erik | Waldemar | Niels | Sven | Erik | Erik | Christoph | Abel | Waldemar | Harald | Erik | Christoph | Gorm | Erik | Erik | Sven |
| 49 |  |  | 0% | 27 |  |  |  |  | Erik | Erik | Christoph | Erik | Niels | Olaf | Waldemar | Christoph | Harald | Knut | Abel | Knut | Waldemar | Erik | Knut | Erik | Waldemar | Sven | Harald | Knut | Sven | Harald | Knut | Gorm | Magnus | Erik | Sven |
| 50 |  |  | 67% | 9 |  |  |  |  | Olaf | Knut | Sven | Harald | Waldemar | Erik | Gorm | Harald | Niels | Waldemar | Knut | Sven | Erik | Waldemar | Erik | Knut | Knut | Christoph | Magnus | Abel | Sven | Knut | Erik | Erik | Christoph | Harald | Erik |
| 51 |  |  | 22% | 21 |  |  |  |  | Erik | Knut | Niels | Erik | Knut | Sven | Gorm | Knut | Waldemar | Harald | Christoph | Erik | Erik | Olaf | Abel | Sven | Knut | Harald | Harald | Waldemar | Magnus | Waldemar | Christoph | Erik | Erik | Knut | Sven |
| 52 |  |  | 33% | 18 |  |  |  |  | Sven | Harald | Knut | Sven | Waldemar | Knut | Waldemar | Olaf | Erik | Erik | Harald | Christoph | Harald | Knut | Magnus | Knut | Christoph | Sven | Erik | Erik | Niels | Abel | Erik | Gorm | Waldemar | Erik | Knut |
| 53 | ✓ | ★ | 89% | 3 | 3 | 6 | 0, 0 | Harald / Erik / Waldemar | Knut | Erik | **Harald** | Niels | Knut | Magnus | Harald | Waldemar | Christoph | **Harald** | **Erik** | Knut | Gorm | Abel | Erik | Olaf | Christoph | **Erik** | **Waldemar** | Sven | Sven | Knut | Knut | Sven | Erik | **Waldemar** | Erik |
| 54 |  |  | 0% | 27 |  |  |  |  | Erik | Knut | Magnus | Erik | Harald | Knut | Waldemar | Christoph | Abel | Sven | Erik | Gorm | Harald | Knut | Olaf | Knut | Sven | Harald | Knut | Erik | Sven | Waldemar | Erik | Erik | Niels | Waldemar | Christoph |
| 55 |  |  | 0% | 27 |  |  |  |  | Erik | Harald | Knut | Magnus | Christoph | Knut | Erik | Waldemar | Erik | Christoph | Waldemar | Erik | Gorm | Niels | Knut | Knut | Olaf | Sven | Sven | Waldemar | Harald | Erik | Harald | Knut | Sven | Erik | Abel |
| 56 |  |  | 56% | 12 |  |  |  |  | Erik | Waldemar | Sven | Harald | Christoph | Waldemar | Sven | Erik | Sven | Knut | Gorm | Erik | Knut | Harald | Harald | Olaf | Knut | Knut | Christoph | Erik | Erik | Erik | Abel | Waldemar | Magnus | Knut | Niels |
| 57 |  |  | 0% | 27 |  |  |  |  | Knut | Olaf | Christoph | Waldemar | Christoph | Harald | Erik | Erik | Sven | Waldemar | Abel | Knut | Erik | Gorm | Sven | Sven | Knut | Harald | Knut | Magnus | Erik | Knut | Waldemar | Niels | Erik | Erik | Harald |
| 58 |  |  | 67% | 9 |  |  |  |  | Harald | Erik | Waldemar | Erik | Christoph | Sven | Erik | Knut | Sven | Olaf | Erik | Knut | Harald | Christoph | Gorm | Erik | Erik | Knut | Abel | Waldemar | Niels | Harald | Knut | Sven | Waldemar | Knut | Magnus |
| 59 |  |  | 44% | 15 |  |  |  |  | Niels | Magnus | Sven | Erik | Sven | Christoph | Erik | Erik | Knut | Erik | Knut | Harald | Harald | Knut | Harald | Waldemar | Christoph | Erik | Waldemar | Waldemar | Abel | Knut | Olaf | Knut | Sven | Erik | Gorm |
| 60 |  |  | 56% | 12 |  |  |  |  | Erik | Knut | Christoph | Knut | Sven | Waldemar | Olaf | Harald | Sven | Harald | Knut | Niels | Erik | Erik | Knut | Magnus | Abel | Erik | Waldemar | Waldemar | Erik | Gorm | Knut | Harald | Erik | Christoph | Sven |
| 61 |  |  | 0% | 27 |  |  |  |  | Harald | Sven | Knut | Knut | Gorm | Christoph | Knut | Knut | Waldemar | Erik | Knut | Sven | Waldemar | Erik | Olaf | Christoph | Niels | Abel | Harald | Erik | Erik | Sven | Waldemar | Erik | Harald | Magnus | Erik |
| 62 |  |  | 67% | 9 |  |  |  |  | Gorm | Magnus | Waldemar | Knut | Harald | Christoph | Niels | Sven | Erik | Erik | Abel | Erik | Sven | Harald | Knut | Knut | Sven | Olaf | Christoph | Knut | Harald | Waldemar | Knut | Erik | Erik | Erik | Waldemar |
| 63 |  |  | 67% | 9 |  |  |  |  | Gorm | Erik | Waldemar | Harald | Sven | Christoph | Erik | Abel | Magnus | Christoph | Erik | Knut | Knut | Olaf | Waldemar | Erik | Sven | Harald | Knut | Erik | Niels | Knut | Erik | Knut | Harald | Sven | Waldemar |
| 64 |  |  | 33% | 18 |  |  |  |  | Erik | Harald | Knut | Olaf | Magnus | Harald | Sven | Erik | Christoph | Gorm | Christoph | Knut | Sven | Erik | Abel | Erik | Waldemar | Waldemar | Sven | Waldemar | Knut | Erik | Erik | Harald | Niels | Knut | Knut |
| 65 |  |  | 0% | 27 |  |  |  |  | Harald | Magnus | Erik | Christoph | Sven | Knut | Erik | Erik | Erik | Harald | Olaf | Christoph | Knut | Sven | Erik | Waldemar | Harald | Abel | Sven | Waldemar | Erik | Waldemar | Niels | Knut | Knut | Gorm | Knut |
| 66 |  |  | 0% | 27 |  |  |  |  | Sven | Niels | Knut | Christoph | Waldemar | Erik | Erik | Olaf | Harald | Harald | Abel | Knut | Erik | Sven | Gorm | Sven | Christoph | Knut | Waldemar | Knut | Waldemar | Erik | Erik | Magnus | Knut | Erik | Harald |
| 67 |  |  | 37% | 17 |  |  |  |  | Christoph | Christoph | Olaf | Sven | Sven | Gorm | Erik | Erik | Erik | Erik | Harald | Sven | Niels | Waldemar | Knut | Knut | Erik | Harald | Knut | Harald | Waldemar | Knut | Abel | Waldemar | Knut | Erik | Magnus |
| 68 |  |  | 0% | 27 |  |  |  |  | Magnus | Sven | Harald | Waldemar | Niels | Knut | Knut | Knut | Abel | Harald | Erik | Waldemar | Knut | Christoph | Olaf | Sven | Erik | Waldemar | Knut | Harald | Erik | Gorm | Erik | Erik | Christoph | Sven | Erik |
| 69 |  |  | 0% | 27 |  |  |  |  | Magnus | Knut | Gorm | Knut | Erik | Erik | Harald | Sven | Abel | Waldemar | Erik | Waldemar | Knut | Erik | Harald | Erik | Knut | Waldemar | Christoph | Sven | Olaf | Christoph | Harald | Erik | Sven | Knut | Niels |
| 70 |  |  | 0% | 27 |  |  |  |  | Erik | Christoph | Olaf | Knut | Gorm | Knut | Magnus | Waldemar | Niels | Waldemar | Erik | Christoph | Sven | Sven | Erik | Knut | Abel | Erik | Harald | Erik | Erik | Harald | Knut | Knut | Waldemar | Sven | Harald |
| 71 |  |  | 78% | 6 |  |  |  |  | Erik | Gorm | Waldemar | Knut | Waldemar | Niels | Erik | Erik | Knut | Erik | Knut | Knut | Harald | Magnus | Knut | Harald | Abel | Sven | Christoph | Sven | Erik | Christoph | Erik | Waldemar | Olaf | Sven | Harald |
| 72 |  |  | 0% | 27 |  |  |  |  | Waldemar | Erik | Abel | Niels | Erik | Harald | Knut | Gorm | Erik | Knut | Harald | Christoph | Sven | Magnus | Knut | Knut | Christoph | Waldemar | Erik | Sven | Knut | Sven | Olaf | Waldemar | Erik | Harald | Erik |
| 73 |  |  | 67% | 9 |  |  |  |  | Erik | Olaf | Harald | Harald | Erik | Waldemar | Sven | Erik | Harald | Knut | Erik | Knut | Erik | Sven | Christoph | Erik | Christoph | Waldemar | Waldemar | Knut | Niels | Abel | Knut | Sven | Knut | Magnus | Gorm |
| 74 |  |  | 0% | 27 |  |  |  |  | Knut | Harald | Knut | Erik | Gorm | Christoph | Sven | Erik | Harald | Sven | Abel | Waldemar | Niels | Waldemar | Erik | Knut | Knut | Olaf | Erik | Erik | Erik | Knut | Sven | Magnus | Waldemar | Christoph | Harald |
| 75 |  |  | 0% | 27 |  |  |  |  | Waldemar | Sven | Christoph | Harald | Waldemar | Harald | Erik | Sven | Knut | Erik | Niels | Waldemar | Knut | Erik | Erik | Harald | Sven | Knut | Gorm | Magnus | Knut | Erik | Knut | Christoph | Erik | Abel | Olaf |
| 76 |  |  | 67% | 9 |  |  |  |  | Gorm | Olaf | Christoph | Knut | Magnus | Waldemar | Knut | Waldemar | Sven | Erik | Sven | Christoph | Harald | Erik | Harald | Erik | Knut | Erik | Abel | Harald | Knut | Niels | Knut | Sven | Erik | Waldemar | Erik |
| 77 |  |  | 0% | 27 |  |  |  |  | Knut | Erik | Olaf | Sven | Sven | Harald | Niels | Magnus | Knut | Harald | Erik | Christoph | Gorm | Waldemar | Knut | Abel | Waldemar | Erik | Harald | Knut | Waldemar | Erik | Christoph | Knut | Sven | Erik | Erik |
| 78 |  |  | 0% | 27 |  |  |  |  | Abel | Niels | Waldemar | Knut | Waldemar | Waldemar | Sven | Knut | Harald | Harald | Erik | Sven | Christoph | Erik | Harald | Gorm | Erik | Christoph | Magnus | Olaf | Erik | Erik | Knut | Erik | Knut | Sven | Knut |
| 79 |  |  | 0% | 27 |  |  |  |  | Waldemar | Harald | Erik | Olaf | Sven | Knut | Niels | Sven | Erik | Magnus | Knut | Sven | Harald | Christoph | Waldemar | Erik | Knut | Erik | Gorm | Waldemar | Abel | Knut | Knut | Harald | Erik | Erik | Christoph |
| 80 |  |  | 0% | 27 |  |  |  |  | Erik | Niels | Sven | Sven | Erik | Harald | Waldemar | Olaf | Knut | Erik | Christoph | Harald | Abel | Waldemar | Christoph | Knut | Magnus | Gorm | Erik | Erik | Sven | Harald | Knut | Knut | Erik | Waldemar | Knut |
| 81 |  |  | 33% | 18 |  |  |  |  | Sven | Magnus | Waldemar | Sven | Erik | Harald | Knut | Harald | Niels | Christoph | Waldemar | Knut | Olaf | Knut | Knut | Abel | Erik | Erik | Sven | Erik | Erik | Waldemar | Christoph | Knut | Erik | Gorm | Harald |
| 82 |  |  | 22% | 21 |  |  |  |  | Christoph | Waldemar | Harald | Gorm | Olaf | Sven | Knut | Knut | Niels | Knut | Christoph | Waldemar | Erik | Waldemar | Abel | Knut | Sven | Magnus | Erik | Knut | Harald | Harald | Sven | Erik | Erik | Erik | Erik |
| 83 |  |  | 33% | 18 |  |  |  |  | Erik | Harald | Knut | Abel | Knut | Niels | Knut | Gorm | Sven | Waldemar | Waldemar | Erik | Christoph | Erik | Waldemar | Christoph | Erik | Erik | Erik | Sven | Sven | Harald | Magnus | Knut | Knut | Harald | Olaf |
| 84 |  |  | 0% | 27 |  |  |  |  | Erik | Erik | Erik | Knut | Sven | Magnus | Knut | Waldemar | Erik | Olaf | Erik | Abel | Erik | Knut | Knut | Sven | Niels | Harald | Knut | Waldemar | Harald | Christoph | Harald | Gorm | Christoph | Waldemar | Sven |
| 85 |  |  | 67% | 9 |  |  |  |  | Magnus | Sven | Erik | Waldemar | Sven | Knut | Gorm | Knut | Christoph | Olaf | Knut | Sven | Erik | Erik | Erik | Harald | Waldemar | Erik | Harald | Knut | Waldemar | Erik | Knut | Harald | Niels | Abel | Christoph |
| 86 |  |  | 22% | 21 |  |  |  |  | Gorm | Erik | Sven | Harald | Knut | Erik | Knut | Christoph | Erik | Sven | Sven | Waldemar | Knut | Knut | Waldemar | Knut | Niels | Abel | Erik | Erik | Magnus | Harald | Olaf | Christoph | Erik | Waldemar | Harald |
| 87 |  |  | 44% | 15 |  |  |  |  | Magnus | Sven | Harald | Gorm | Erik | Sven | Knut | Knut | Sven | Christoph | Waldemar | Niels | Erik | Knut | Harald | Olaf | Knut | Abel | Erik | Harald | Waldemar | Erik | Erik | Knut | Waldemar | Christoph | Erik |
| 88 |  |  | 0% | 27 |  |  |  |  | Knut | Knut | Gorm | Waldemar | Waldemar | Erik | Olaf | Christoph | Sven | Knut | Sven | Erik | Harald | Harald | Magnus | Sven | Erik | Erik | Knut | Harald | Knut | Erik | Christoph | Abel | Waldemar | Niels | Erik |
| 89 |  |  | 0% | 27 |  |  |  |  | Gorm | Magnus | Erik | Waldemar | Niels | Knut | Sven | Waldemar | Olaf | Knut | Erik | Erik | Knut | Harald | Christoph | Christoph | Sven | Erik | Waldemar | Erik | Sven | Knut | Knut | Abel | Harald | Harald | Erik |
| 90 |  |  | 30% | 19 |  |  |  |  | Erik | Erik | Erik | Olaf | Christoph | Harald | Harald | Sven | Knut | Knut | Gorm | Waldemar | Erik | Erik | Knut | Harald | Waldemar | Niels | Knut | Erik | Sven | Sven | Knut | Christoph | Waldemar | Magnus | Abel |
| 91 |  |  | 0% | 27 |  |  |  |  | Erik | Erik | Knut | Sven | Waldemar | Olaf | Erik | Magnus | Knut | Waldemar | Knut | Knut | Sven | Erik | Harald | Erik | Sven | Harald | Gorm | Niels | Harald | Waldemar | Christoph | Knut | Erik | Abel | Christoph |
| 92 |  |  | 0% | 27 |  |  |  |  | Sven | Waldemar | Harald | Harald | Erik | Erik | Christoph | Knut | Olaf | Sven | Waldemar | Sven | Niels | Gorm | Erik | Knut | Knut | Knut | Harald | Knut | Erik | Erik | Christoph | Abel | Erik | Waldemar | Magnus |
| 93 |  |  | 0% | 27 |  |  |  |  | Knut | Harald | Erik | Knut | Niels | Waldemar | Erik | Waldemar | Harald | Sven | Gorm | Erik | Erik | Sven | Sven | Harald | Erik | Knut | Magnus | Waldemar | Knut | Christoph | Christoph | Knut | Abel | Olaf | Erik |
| 94 |  |  | 0% | 27 |  |  |  |  | Erik | Erik | Waldemar | Harald | Sven | Sven | Erik | Abel | Harald | Knut | Gorm | Magnus | Waldemar | Erik | Erik | Erik | Knut | Olaf | Sven | Waldemar | Knut | Knut | Niels | Christoph | Knut | Harald | Christoph |
| 95 |  |  | 0% | 27 |  |  |  |  | Olaf | Christoph | Sven | Erik | Knut | Knut | Knut | Erik | Magnus | Waldemar | Erik | Harald | Harald | Knut | Abel | Waldemar | Gorm | Harald | Sven | Niels | Erik | Christoph | Knut | Sven | Erik | Waldemar | Erik |
| 96 |  |  | 33% | 18 |  |  |  |  | Harald | Waldemar | Knut | Erik | Erik | Erik | Erik | Abel | Sven | Gorm | Christoph | Niels | Christoph | Harald | Waldemar | Knut | Harald | Sven | Knut | Sven | Waldemar | Erik | Olaf | Knut | Knut | Magnus | Erik |
| 97 |  |  | 78% | 6 |  |  |  |  | Christoph | Sven | Erik | Harald | Erik | Magnus | Erik | Harald | Erik | Knut | Erik | Knut | Waldemar | Olaf | Sven | Erik | Niels | Knut | Harald | Waldemar | Knut | Gorm | Christoph | Sven | Knut | Waldemar | Abel |
| 98 |  |  | 33% | 18 |  |  |  |  | Knut | Harald | Erik | Gorm | Niels | Sven | Christoph | Magnus | Christoph | Harald | Erik | Sven | Knut | Waldemar | Erik | Abel | Erik | Knut | Knut | Olaf | Knut | Waldemar | Sven | Waldemar | Erik | Erik | Harald |
| 99 |  |  | 33% | 18 |  |  |  |  | Waldemar | Harald | Harald | Sven | Sven | Olaf | Erik | Waldemar | Erik | Harald | Christoph | Waldemar | Magnus | Knut | Knut | Knut | Erik | Abel | Christoph | Gorm | Erik | Erik | Erik | Sven | Niels | Knut | Knut |
| 100 |  |  | 0% | 27 |  |  |  |  | Gorm | Magnus | Erik | Erik | Olaf | Sven | Erik | Christoph | Harald | Knut | Niels | Sven | Knut | Waldemar | Knut | Abel | Erik | Erik | Waldemar | Knut | Harald | Harald | Christoph | Erik | Sven | Waldemar | Knut |

## Auswertung

Über **2000** Permutationen (die Tabelle oben zeigt die ersten 100).

| Kriterium | Treffer | Anteil | p |
|---|---|---|---|
| ✓ irgendeine Kette gleicher Güte | 39 | 1.9% | 0.020 |
| ★ zusätzlich gleiche Blocklänge | 35 | 1.8% | 0.0180 |

### Was die Abdeckung misst

Die Blocklängen der Zufallstreffer: x=4: 3, x=6: 35, x=7: 1.

Unter dieser Messgrösse zählt nicht mehr, *wie viele* Blöcke eine Kette hat, sondern wie viel der Liste sie erklärt. Damit fallen die kurzen Ketten heraus, die den Bit-Wert dominiert haben: drei Blöcke zu je drei Namen erfassen neun von 27 Positionen, das reicht nicht mehr.

Deshalb ist die ★-Zeile hier fast deckungsgleich mit der ✓-Zeile — wer in einer Liste von 27 Namen mit drei Blöcken hohe Abdeckung erreichen will, braucht zwangsläufig Blöcke dieser Länge. Die Blocklänge ist also kein freier Parameter mehr, über den man sich hinterher etwas aussuchen könnte, und eine Bonferroni-Korrektur erübrigt sich.

### Und was heisst das nun?

In **39 von 2000** Umsortierungen erreicht der Zufall eine mindestens so hohe Abdeckung wie die Geschichtsschreibung — **p = 0.020**.

Die Ausgangsliste ist damit geordneter als 98.0% aller Umsortierungen. Sie ist aber **nicht** die geordnetste mögliche: der beste Zufallstreffer erreicht 100% Abdeckung gegenüber 89% der Königsliste.

### Die Treffer unter den ersten 100

| # | | Blöcke | x | Klammern | Positionen | Zwischen |
|---|---|---|---|---|---|---|
| 30 | ★ | 3 | 6 | Erik / Harald / Knut | 0–7 10–17 18–25 | 2, 0 |
| 53 | ★ | 3 | 6 | Harald / Erik / Waldemar | 2–9 10–17 18–25 | 0, 0 |
