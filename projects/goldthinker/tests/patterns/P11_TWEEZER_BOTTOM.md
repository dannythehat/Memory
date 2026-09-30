# P11 Tweezer Bottom — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.2.2 · vector pack GV-0.1 · **39 vectors** (1 dormant, 38 firm)

Strategies covered: `GT-TWEEZERBOTTOM-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-TWEEZERBOTTOM-BULL-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `A01` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4199.40/4205.00 | DOWN | 8 | shape ✔ · formed ✔ | — | ATR 8 -> tol 0.40. Difference 0.40 passes. |
| `A02` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4199.41/4205.00 | DOWN | 8 | no shape | |L1-L2|<=tol | ATR 8: difference 0.41 fails. |
| `A03` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4199.05/4205.00 | DOWN | 1 | shape ✔ · formed ✔ | — | ATR 1 -> tol = max(0.03, 0.05) = 0.05. Difference 0.05 passes. |
| `A04` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4199.06/4205.00 | DOWN | 1 | no shape | |L1-L2|<=tol | ATR 1: difference 0.06 fails. |
| `A05` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4199.03/4205.00 | DOWN | 0.5 | shape ✔ · formed ✔ | — | ATR 0.5 -> 0.05*ATR = 0.025 < 3 ticks 0.03, so tol = 0.03. Difference 0.03 passes. |
| `A06` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4199.04/4205.00 | DOWN | 0.5 | no shape | |L1-L2|<=tol | ATR 0.5: difference 0.04 fails (the 3-tick floor is 0.03). |
| `B01` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4199.20/4205.00 | DOWN | 4 | shape ✔ · formed ✔ | — | ATR 4 -> tol = max(3*tick 0.03, 0.05*4 = 0.20) = 0.20. |L1-L2| = 0.20 (L2 above L1): passes. |
| `B02` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4199.19/4205.00 | DOWN | 4 | shape ✔ · formed ✔ | — | |L1-L2| = 0.19. |
| `B03` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4199.21/4205.00 | DOWN | 4 | no shape | |L1-L2|<=tol | |L1-L2| = 0.21 -> only the tolerance clause fails. |
| `B04` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4198.80/4205.00 | DOWN | 4 | shape ✔ · formed ✔ | — | L2 BELOW L1 by exactly 0.20 (4198.80): passes (absolute difference). |
| `B05` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4198.79/4205.00 | DOWN | 4 | no shape | |L1-L2|<=tol | L2 below L1 by 0.21: fails. |
| `B06` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4199.00/4205.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Equal lows (difference 0): passes. |
| `F01` | 4205.00/4206.00/4199.00/4200.75 ; 4199.50/4205.50/4199.10/4205.00 | DOWN | 4 | shape ✔ · formed ✔ | — | C1 closes exactly at L1+0.25*R1 (4200.75): flag c1_low25 true (<=). |
| `F02` | 4205.00/4206.00/4199.00/4200.76 ; 4199.50/4205.50/4199.10/4205.00 | DOWN | 4 | shape ✔ · formed ✔ | — | C1 closes 0.01 above the line: flag false; pattern still forms. |
| `N01` | 4200.00/4206.00/4199.00/4205.00 ; 4199.50/4205.50/4199.10/4205.00 | DOWN | 4 | no shape | C1 bear | C1 bullish: fails colour. |
| `N02` | 4205.00/4206.00/4199.00/4200.00 ; 4205.00/4205.50/4199.10/4199.50 | DOWN | 4 | no shape | C2 bull | C2 bearish: fails colour. |
| `NZ1` | 4200.00/4204.50/4199.50/4204.00 ; 4204.00/4208.50/4203.50/4208.00 | DOWN | 4 | canonical: no event; variant: no event | — | Two bullish candles: C1 must be bearish. |
| `T01` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4199.10/4205.00 | UP | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Tweezer shape after UP: not formed. |
| `T02` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4199.10/4205.00 | RANGE | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Tweezer shape after RANGE: not formed. |
| `T03` | 4205.00/4206.00/4199.00/4200.00 ; 4199.50/4205.50/4199.10/4205.00 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Tweezer shape after UNDETERMINED: not formed. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:30:02 4205.00/4205.20; 09-16 10:32:00 4208.20/4208.40; 09-16 10:35:00 4218.00/4218.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4205.20; stop: 4198.80; R: 6.40; target(s): 4218.00; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:30:02 4205.00/4205.20; 09-16 10:32:00 4201.80/4202.00; 09-16 10:35:00 4198.80/4199.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4205.20; stop: 4198.80; R: 6.40; target(s): 4218.00; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4196.80 < stop): fill = that tick's bid, not the stop (G9): -1.3125R. | 09-16 10:30:02 4205.00/4205.20; 09-16 10:32:00 4196.80/4197.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4205.20; stop: 4198.80; R: 6.40; target(s): 4218.00; exit: STOP net -1.3125R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:30:02 4205.00/4205.20; 09-16 10:31:40 4198.80/4199.00; 09-16 10:33:20 4218.00/4218.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4205.20; stop: 4198.80; R: 6.40; target(s): 4218.00; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:30:02 4205.00/4205.20; 09-16 10:31:40 4218.00/4218.20; 09-16 10:33:20 4198.80/4199.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4205.20; stop: 4198.80; R: 6.40; target(s): 4218.00; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:30:02 4205.00/4205.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4205.20; stop: 4198.80; R: 6.40; target(s): 4218.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:30:02 4205.00/4205.50; 09-16 10:33:20 4218.90/4219.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4205.50; stop: 4198.80; R: 6.70; target(s): 4218.90; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:45:00 4205.00/4205.20; 09-16 10:46:40 4218.00/4218.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4205.20; stop: 4198.80; R: 6.40; target(s): 4218.00; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:45:01 4205.00/4205.20; 09-16 10:46:40 4218.00/4218.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:30:02 4200.30/4200.80; 09-16 10:31:40 4204.80/4205.30 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.80; R: 2.00; target(s): 4204.80; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:30:02 4200.29/4200.79; 09-16 10:31:40 4204.79/4205.29 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4224.40 > target 4218.00): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:30:02 4205.00/4205.20; 09-16 10:32:00 4224.40/4224.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4205.20; stop: 4198.80; R: 6.40; target(s): 4218.00; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4205.00/4205.20; 09-21 00:30:00 4218.00/4218.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4205.20; stop: 4198.80; R: 6.40; target(s): 4218.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4205.00/4205.20; 09-21 00:30:00 4218.00/4218.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4205.20; stop: 4198.80; R: 6.40; target(s): 4218.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4205.00/4205.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P11-R01` · `GT-TWEEZERBOTTOM-BULL-v1.0/BASE` · M15
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4206.00 | 4199.00 | 4200.00 |
| 2 | 09-16 10:15 | 4199.50 | 4205.50 | 4199.10 | 4205.00 |
| 3 | 09-16 10:30 | 4205.00 | 4208.00 | 4203.00 | 4206.00 |
| 4 | 09-16 10:45 | 4206.00 | 4209.00 | 4204.00 | 4207.00 |
| 5 | 09-16 11:00 | 4207.00 | 4208.00 | 4202.00 | 4204.00 |
| 6 | 09-16 11:15 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 7 | 09-16 11:30 | 4206.00 | 4210.00 | 4203.00 | 4208.00 |
| 8 | 09-16 11:45 | 4208.00 | 4214.00 | 4196.00 | 4209.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4205.00 | h1: ret=1.00, mfe=3.00, mae=-2.00, end_index=2 | h3: ret=-1.00, mfe=4.00, mae=-3.00, end_index=4 | h5: ret=3.00, mfe=5.00, mae=-4.00, end_index=6 | h10: NULL | h20: NULL

#### `GV-P11-Y01` · `GT-TWEEZERBOTTOM-BULL-v1.0/BASE` · M15
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4206.00 | 4199.00 | 4200.00 |
| 2 | 09-16 10:15 | 4199.50 | 4205.50 | 4199.10 | 4205.00 |

Ticks (bid/ask): 09-16 10:30:02 4205.00/4205.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4205.20
- stop: 4198.80
- R: 6.40
- target(s): 4218.00

### Variant `SRC-PS`

#### `GV-DORM-P11-01` · `GT-TWEEZERBOTTOM-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> DORMANT. Lows differ by 0.25: no canonical Tweezer Bottom, but the source variant (tol 0.30) qualifies. STOP_ENTRY buy trigger H2 = 4205.50; the first tick with ask >= 4205.50 fills at that ask 4205.60; stop min(L1,L2) - 3 pips x $0.10 = 4198.70; R 6.90; T_SWING(1.5) 4216.00 = 1.507R.

Tags: dormant, source-only-qualification, stop-entry
Context: atr=4 · trend=DOWN · zones_pre=[4198.50-4198.70] · swings=H4216.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4206.00 | 4199.00 | 4200.00 |
| 2 | 09-16 10:15 | 4199.50 | 4205.50 | 4199.25 | 4205.00 |

Ticks (bid/ask): 09-16 10:40:00 4205.40/4205.60; 09-16 10:50:00 4216.00/4216.20

- canonical: no event
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- trigger: 4205.50
- signal time: 2026-09-16T10:40:00Z
- entry: 4205.60
- stop: 4198.70
- R: 6.90
- target(s): 4216.00
- exit: TARGET net 104/69 (≈1.5072)R

#### `GV-P11-DIS` · `GT-TWEEZERBOTTOM-BULL-v1.0/SRC-PS` · M15
> DISABLED_PENDING_PIP_CONFIRMATION (D-032): the BASE pattern forms exactly as in GV-P11-Y01 (canonical events are still logged), but this source variant depends on PIP_SRC_USD, so it emits NO variant events, opens NO trade and has no ledger. The BASE strategy on the same candle is unaffected.

Tags: disabled-variant
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4206.00 | 4199.00 | 4200.00 |
| 2 | 09-16 10:15 | 4199.50 | 4205.50 | 4199.10 | 4205.00 |

Ticks (bid/ask): 09-16 10:30:02 4205.00/4205.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant status: DISABLED_PENDING_PIP_CONFIRMATION
- variant: no event

