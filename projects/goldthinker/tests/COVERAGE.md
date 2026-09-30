# Coverage matrix

Counts of vectors per pattern and requested test type (dormant vectors are counted in their pattern). `—` = not applicable to that pattern by construction (see legend). Both directions are counted together for patterns that have two sides.

| pattern | Clean YES | Clean NO | Boundary (exact / just in / just out) | Right shape, wrong trend / no prior state | Source variant qualifies, BASE does not (dormant) | Confirmation succeeds / fails / expires | Stop-entry triggers / expires | Target already passed | Insufficient R:R | No structural target | Weekend / rollover entry | Spread-sensitive fill | SL/TP ordering from ticks | Missing ticks -> STOP FIRST | Early setup: bid detects, ask/bid executes | RAW horizon_end | Disabled pip variant -> no trade | vectors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P01 Hammer | 2 | 1 | 17 | 3 | 1 | 6 | — | — | — | — | 1 | 1 | 4 | 1 | — | 8 | 1 | 54 |
| P02 Shooting Star | 2 | 1 | 15 | 3 | 1 | 1 | — | — | — | — | 1 | 1 | 4 | 1 | — | 2 | 1 | 44 |
| P03 Pin Bar | 2 | 2 | 38 | 8 | — | — | — | — | 2 | 2 | 2 | 2 | 8 | 2 | — | 2 | 2 | 99 |
| P04 Dragonfly Doji | 1 | 1 | 11 | 3 | — | 2 | — | — | — | — | 1 | 1 | 4 | 1 | — | 1 | 1 | 39 |
| P05 Gravestone Doji | 1 | 1 | 11 | 3 | — | 1 | — | — | — | — | 1 | 1 | 4 | 1 | — | 1 | 1 | 33 |
| P06 Bullish Engulfing | 2 | 1 | 18 | 3 | 1 | — | — | — | 1 | 1 | 1 | 1 | 4 | 1 | — | 1 | 1 | 53 |
| P07 Bearish Engulfing | 2 | 1 | 15 | 3 | 1 | — | — | — | 1 | 1 | 1 | 1 | 4 | 1 | — | 1 | 1 | 46 |
| P08 Outside Bar | 2 | 4 | 24 | 8 | — | — | — | 2 | 6 | 4 | 2 | 2 | 10 | 2 | — | 2 | — | 105 |
| P09 Inside Bar Breakout | 2 | 4 | 10 | 6 | — | 14 | — | — | 2 | 2 | 4 | 2 | 8 | 2 | — | 2 | 2 | 80 |
| P10 Tweezer Top | 1 | 1 | 16 | 3 | 1 | — | 1 | — | — | — | 1 | 1 | 4 | 1 | — | 1 | 1 | 39 |
| P11 Tweezer Bottom | 1 | 1 | 16 | 3 | 1 | — | 1 | — | — | — | 1 | 1 | 4 | 1 | — | 1 | 1 | 39 |
| P12 Piercing Line | 1 | 1 | 17 | 3 | — | — | — | — | 1 | 1 | 1 | 1 | 5 | 1 | — | 1 | — | 51 |
| P13 Dark Cloud Cover | 1 | 1 | 17 | 3 | — | — | — | — | 1 | 1 | 1 | 1 | 5 | 1 | — | 1 | — | 45 |
| P14 Kicker | 2 | 2 | 24 | 6 | — | — | — | — | 2 | 4 | 2 | 2 | 10 | 2 | — | 2 | — | 97 |
| P14E Kicker Early | 2 | 2 | 6 | 3 | — | — | — | — | 2 | 1 | 2 | 1 | 5 | 2 | 25 | 1 | — | 33 |
| P15 Morning Star | 1 | 2 | 15 | 3 | — | — | — | 3 | — | — | 1 | 1 | 5 | 1 | — | 1 | — | 44 |
| P16 Evening Star | 1 | 2 | 15 | 3 | — | — | — | 2 | — | — | 1 | 1 | 5 | 1 | — | 1 | — | 43 |
| P17 Three White Soldiers | 1 | 1 | 18 | 4 | — | 4 | 12 | 1 | — | — | 3 | 1 | 4 | 1 | — | 1 | — | 49 |
| P18 Three Black Crows | 1 | 1 | 18 | 4 | — | 4 | 12 | 1 | — | — | 3 | 1 | 4 | 1 | — | 1 | — | 49 |
| P19 Abandoned Baby | 2 | 4 | 26 | 6 | — | — | — | — | 2 | 2 | 2 | 2 | 10 | 2 | — | 2 | — | 74 |
| P19E Abandoned Baby Early | 2 | 2 | 6 | 2 | — | — | — | — | 2 | 1 | 2 | 1 | 5 | 2 | 20 | 1 | — | 27 |
| P20 Rising Three Methods | 1 | 1 | 13 | 3 | — | — | — | 1 | 2 | — | 1 | 1 | 4 | 1 | — | 1 | — | 39 |
| P21 Falling Three Methods | 1 | 1 | 13 | 3 | — | — | — | 1 | 2 | — | 1 | 1 | 4 | 1 | — | 1 | — | 38 |
| P22 Inside Bar Sweep Reclaim | 4 | 2 | 14 | 8 | — | — | — | — | 2 | 2 | 2 | 2 | 8 | 2 | — | 2 | — | 80 |

Legend for `—`: *source-only qualification* exists only where a pip-dependent SRC-PS variant relaxes the prior state or tolerance (Hammer, Shooting Star, Engulfings, Tweezers); *confirmation* only where a rule has a confirmation bar (Hammer, Shooting Star, Dragonfly, Gravestone SRC-PS variants, and the Inside Bar breakout window); *stop-entry* only for Tweezers (dormant) and the three-candle continuation patterns; *target already passed* only where a target can lie behind the entry (partial-target stars, measured-move soldiers/crows, Fibonacci Rising/Falling); *insufficient R:R* and *no structural target* only where a source variant uses T_SR / T_SWING / a minimum reward; *early bid/ask* only for the two early setups; *disabled pip variant* only for the ten pip-dependent variants.

Overlap vectors: 21 in `OVERLAPS.md` (Hammer/Dragonfly/Pin Bar, Engulfing/Outside Bar/Tweezer Bottom, Piercing vs Engulfing (disjoint at both boundaries), Morning Star vs Abandoned Baby (subset), Inside Bar vs Sweep & Reclaim, Kicker vs Kicker Early; each also as its bearish mirror except the early-setup pair). Hub counters: 7 vectors in `HUB_COUNTERS.md`. Timeframe / bar-boundary and execution vectors: `EXECUTION_AND_TIMEFRAMES.md`.

## Global rule pack (`GLOBAL_RULES.md`)

| Requested area | Vectors |
|---|---|
| ATR | GV-G-ATR-01..05 |
| Size classes (LARGE / SMALL / DOJI) | GV-G-CLS-01..03 |
| Swings and confirmation lag | GV-G-SW-01..04 |
| Trend (UP / DOWN / RANGE / UNDETERMINED, no look-ahead) | GV-G-TR-01..05 |
| S/R clustering, zone width, AT_SUPPORT/RESISTANCE, round-50 | GV-G-ZN-01..11 |
| Sessions incl. DST divergence, half-open boundaries | GV-G-SS-01..03 |
| News windows | GV-G-NW-01..03 |
| Gaps | GV-G-GP-01..02 |
| Sizing, tick value, min lot, commission | GV-G-SZ-01..04, GV-EX-CM-01..02 |
| Broker closures, bar completion, open_elapsed, data gaps | GV-G-CAL-01..04, GV-TF-* |
| RSI (Wilder) and warm-up | GV-G-RS-01..03, GV-P06-H05/H06 |
| Target snapshot (zones_prepattern vs zones_at_entry, frozen target) | GV-G-SN-01 |
| Executable-price quantisation (A-30) | GV-G-QT-01, GV-P01-Q01, GV-P08-Q01..03, GV-P16-Q01 |
| End to end: bars -> ATR/trend/zones -> pattern -> signal | GV-E2E-01a..c, GV-E2E-02, GV-E2E-03 |
| Tick-path RAW (mfe_before_mae_h) | GV-P01-M01..M05, GV-P02-M01, GV-EX-B06 |
