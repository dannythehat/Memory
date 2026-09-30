# P15 Morning Star — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.2.2 · vector pack GV-0.1 · **44 vectors** (44 firm)

Strategies covered: `GT-MORNINGSTAR-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-MORNINGSTAR-BULL-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4210.00/4210.50/4203.00/4203.50 ; 4203.00/4204.20/4202.00/4204.00 ; 4204.50/4209.50/4204.00/4209.20 | DOWN | 4 | shape ✔ · formed ✔ | — | SMALL(C2): B exactly 1.00 (0.25*ATR), R 2.20: passes. |
| `B02` | 4210.00/4210.50/4203.00/4203.50 ; 4203.00/4204.21/4202.00/4204.01 ; 4204.50/4209.50/4204.00/4209.20 | DOWN | 4 | no shape | SMALL(C2) | SMALL(C2): B = 1.01: fails SMALL only. |
| `B03` | 4210.00/4210.50/4203.00/4203.50 ; 4203.00/4204.40/4202.00/4203.40 ; 4204.50/4209.50/4204.00/4209.20 | DOWN | 4 | shape ✔ · formed ✔ | — | SMALL(C2): R exactly 2.40 (0.60*ATR), B 0.40: passes. |
| `B04` | 4210.00/4210.50/4203.00/4203.50 ; 4203.00/4204.41/4202.00/4203.40 ; 4204.50/4209.50/4204.00/4209.20 | DOWN | 4 | no shape | SMALL(C2) | SMALL(C2): R = 2.41: fails SMALL only. |
| `B05` | 4210.00/4210.50/4203.00/4203.50 ; 4203.90/4204.00/4203.00/4203.95 ; 4204.50/4209.50/4204.00/4209.20 | DOWN | 4 | shape ✔ · formed ✔ | — | O2 exactly C1 + 0.10*ATR = 4203.90: passes. |
| `B06` | 4210.00/4210.50/4203.00/4203.50 ; 4203.91/4204.00/4203.00/4203.95 ; 4204.50/4209.50/4204.00/4209.20 | DOWN | 4 | no shape | O2<=C1+0.10ATR | O2 = 4203.91: only the star-opening clause fails. |
| `B07` | 4210.00/4210.50/4203.00/4203.50 ; 4203.00/4203.80/4202.00/4203.40 ; 4203.80/4207.00/4203.50/4206.75 | DOWN | 4 | no shape | C3>mid1 | C3 exactly at the C1 midpoint 4206.75: fails C3>mid1 (strict) only. |
| `B08` | 4210.00/4210.50/4203.00/4203.50 ; 4203.00/4203.80/4202.00/4203.40 ; 4203.80/4207.00/4203.50/4206.76 | DOWN | 4 | shape ✔ · formed ✔ | — | C3 = midpoint + 0.01: passes. |
| `B09` | 4210.00/4210.40/4207.20/4207.60 ; 4207.50/4208.60/4207.00/4208.46 ; 4208.00/4213.00/4207.80/4212.50 | DOWN | 4 | shape ✔ · formed ✔ | — | B2 exactly 0.40*B1 (B1=2.40 -> B2=0.96; C1 LARGE on both B and R boundaries): passes. |
| `B10` | 4210.00/4210.40/4207.20/4207.60 ; 4207.50/4208.61/4207.00/4208.47 ; 4208.00/4213.00/4207.80/4212.50 | DOWN | 4 | no shape | B2<=0.40B1 | B2 = 0.97 vs 0.4*2.40 = 0.96: only B2<=0.40B1 fails (SMALL still passes). |
| `F01` | 4210.00/4210.50/4203.00/4203.50 ; 4203.00/4203.80/4202.00/4203.40 ; 4204.50/4209.50/4204.00/4209.20 | DOWN | 4 | shape ✔ · formed ✔ | — | Star body top 4203.40 < C1 close 4203.50: star_gap true (flag only). |
| `N01` | 4210.00/4210.50/4203.00/4203.50 ; 4203.00/4203.80/4202.00/4203.40 ; 4203.50/4204.60/4203.40/4204.50 | DOWN | 4 | no shape | LARGE(C3), C3>mid1 | C3 not LARGE (small bull): fails LARGE(C3) and the midpoint test. |
| `N02` | 4210.00/4210.50/4203.00/4203.50 ; 4203.00/4203.80/4202.00/4203.40 ; 4209.20/4209.50/4204.00/4204.50 | DOWN | 4 | no shape | C3 bull, C3>mid1 | C3 bearish: fails colour. |
| `N03` | 4210.00/4210.50/4203.00/4203.50 ; 4203.00/4208.00/4202.00/4207.00 ; 4204.50/4209.50/4204.00/4209.20 | DOWN | 4 | no shape | SMALL(C2), B2<=0.40B1 | C2 is a LARGE candle, not a star: fails SMALL and B2<=0.40B1. |
| `NZ1` | 4200.00/4204.50/4199.50/4204.00 ; 4204.00/4208.50/4203.50/4208.00 ; 4208.00/4212.50/4207.50/4212.00 | DOWN | 4 | canonical: no event; variant: no event | — | Three bullish candles: no star, no bearish C1. |
| `T01` | 4210.00/4210.50/4203.00/4203.50 ; 4203.00/4203.80/4202.00/4203.40 ; 4204.50/4209.50/4204.00/4209.20 | UP | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Morning Star shape after UP: not formed. |
| `T02` | 4210.00/4210.50/4203.00/4203.50 ; 4203.00/4203.80/4202.00/4203.40 ; 4204.50/4209.50/4204.00/4209.20 | RANGE | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Morning Star shape after RANGE: not formed. |
| `T03` | 4210.00/4210.50/4203.00/4203.50 ; 4203.00/4203.80/4202.00/4203.40 ; 4204.50/4209.50/4204.00/4209.20 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Morning Star shape after UNDETERMINED: not formed. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:45:02 4209.20/4209.40; 09-16 10:47:00 4213.00/4213.20; 09-16 10:50:00 4224.60/4224.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.80; R: 7.60; target(s): 4224.60; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:45:02 4209.20/4209.40; 09-16 10:47:00 4205.40/4205.60; 09-16 10:50:00 4201.80/4202.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.80; R: 7.60; target(s): 4224.60; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4199.80 < stop): fill = that tick's bid, not the stop (G9): -24/19R. | 09-16 10:45:02 4209.20/4209.40; 09-16 10:47:00 4199.80/4200.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.80; R: 7.60; target(s): 4224.60; exit: STOP net -24/19 (≈-1.2632)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:45:02 4209.20/4209.40; 09-16 10:46:40 4201.80/4202.00; 09-16 10:48:20 4224.60/4224.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.80; R: 7.60; target(s): 4224.60; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:45:02 4209.20/4209.40; 09-16 10:46:40 4224.60/4224.80; 09-16 10:48:20 4201.80/4202.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.80; R: 7.60; target(s): 4224.60; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:45:02 4209.20/4209.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.80; R: 7.60; target(s): 4224.60; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:45:02 4209.20/4209.70; 09-16 10:48:20 4225.50/4226.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.70; stop: 4201.80; R: 7.90; target(s): 4225.50; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 11:00:00 4209.20/4209.40; 09-16 11:01:40 4224.60/4224.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.80; R: 7.60; target(s): 4224.60; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 11:00:01 4209.20/4209.40; 09-16 11:01:40 4224.60/4224.80 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:45:02 4203.30/4203.80; 09-16 10:46:40 4207.80/4208.30 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4203.80; R: 2.00; target(s): 4207.80; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:45:02 4203.29/4203.79; 09-16 10:46:40 4207.79/4208.29 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4231.00 > target 4224.60): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:45:02 4209.20/4209.40; 09-16 10:47:00 4231.00/4231.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.80; R: 7.60; target(s): 4224.60; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4209.20/4209.40; 09-21 00:30:00 4224.60/4224.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4209.40; stop: 4201.80; R: 7.60; target(s): 4224.60; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4209.20/4209.40; 09-21 00:30:00 4224.60/4224.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4209.40; stop: 4201.80; R: 7.60; target(s): 4224.60; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4209.20/4209.40 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P15-R01` · `GT-MORNINGSTAR-BULL-v1.0/BASE` · M15
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.00 | 4203.50 |
| 2 | 09-16 10:15 | 4203.00 | 4203.80 | 4202.00 | 4203.40 |
| 3 | 09-16 10:30 | 4204.50 | 4209.50 | 4204.00 | 4209.20 |
| 4 | 09-16 10:45 | 4209.20 | 4212.20 | 4207.20 | 4210.20 |
| 5 | 09-16 11:00 | 4210.20 | 4213.20 | 4208.20 | 4211.20 |
| 6 | 09-16 11:15 | 4211.20 | 4212.20 | 4206.20 | 4208.20 |
| 7 | 09-16 11:30 | 4208.20 | 4211.20 | 4205.20 | 4209.20 |
| 8 | 09-16 11:45 | 4210.20 | 4214.20 | 4207.20 | 4212.20 |
| 9 | 09-16 12:00 | 4212.20 | 4218.20 | 4200.20 | 4213.20 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4209.20 | h1: ret=1.00, mfe=3.00, mae=-2.00, end_index=3 | h3: ret=-1.00, mfe=4.00, mae=-3.00, end_index=5 | h5: ret=3.00, mfe=5.00, mae=-4.00, end_index=7 | h10: NULL | h20: NULL

#### `GV-P15-V00` · `GT-MORNINGSTAR-BULL-v1.0/BASE` · M15
> BASE on a Morning Star whose C3 low (4201.50) is below both earlier lows: BASE stop = min(L1,L2,L3)-0.20 = 4201.30.

Tags: base-vs-source
Context: atr=4 · trend=DOWN · swings=H4218.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.00 | 4203.50 |
| 2 | 09-16 10:15 | 4203.00 | 4203.80 | 4202.00 | 4203.40 |
| 3 | 09-16 10:30 | 4203.00 | 4209.50 | 4201.50 | 4209.00 |

Ticks (bid/ask): 09-16 10:45:02 4209.00/4209.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4209.20
- stop: 4201.30
- R: 7.90
- target(s): 4225.00

#### `GV-P15-Y01` · `GT-MORNINGSTAR-BULL-v1.0/BASE` · M15
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.00 | 4203.50 |
| 2 | 09-16 10:15 | 4203.00 | 4203.80 | 4202.00 | 4203.40 |
| 3 | 09-16 10:30 | 4204.50 | 4209.50 | 4204.00 | 4209.20 |

Ticks (bid/ask): 09-16 10:45:02 4209.20/4209.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:45:00Z
- entry: 4209.40
- stop: 4201.80
- R: 7.60
- target(s): 4224.60

### Variant `SRC-PS`

#### `GV-P15-V01` · `GT-MORNINGSTAR-BULL-v1.0/SRC-PS` · M15
> SRC-PS: stop = min(L1,L2) - 0.20 = 4201.80 (C3's lower low is ignored); entry ask 4209.20; R 7.40; TP1 = H1 4210.50 closes 60%; TP2 = nearest confirmed swing high above TP1 (4218.00) for 40%. Both hit: 0.6*1.30/7.40 + 0.4*8.80/7.40 = +0.5811R.

Tags: variant-clean-yes, partials, base-vs-source
Context: atr=4 · trend=DOWN · swings=H4218.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.00 | 4203.50 |
| 2 | 09-16 10:15 | 4203.00 | 4203.80 | 4202.00 | 4203.40 |
| 3 | 09-16 10:30 | 4203.00 | 4209.50 | 4201.50 | 4209.00 |

Ticks (bid/ask): 09-16 10:45:02 4209.00/4209.20; 09-16 10:46:40 4210.50/4210.70; 09-16 10:47:30 4218.00/4218.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4209.20
- stop: 4201.80
- R: 7.40
- target(s): 4210.50, 4218.00
- exit: TARGET net 43/74 (≈0.5811)R

#### `GV-P15-V02` · `GT-MORNINGSTAR-BULL-v1.0/SRC-PS` · M15
> TP1 hit then price returns to the (unmoved) stop: 60% at +0.1757R and 40% at -1R = -0.2946R.

Tags: partials, tp1-then-stop
Context: atr=4 · trend=DOWN · swings=H4218.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.00 | 4203.50 |
| 2 | 09-16 10:15 | 4203.00 | 4203.80 | 4202.00 | 4203.40 |
| 3 | 09-16 10:30 | 4203.00 | 4209.50 | 4201.50 | 4209.00 |

Ticks (bid/ask): 09-16 10:45:02 4209.00/4209.20; 09-16 10:46:40 4210.50/4210.70; 09-16 10:47:30 4201.80/4202.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4209.20
- stop: 4201.80
- R: 7.40
- target(s): 4210.50, 4218.00
- exit: MIXED net -109/370 (≈-0.2946)R

#### `GV-P15-V03` · `GT-MORNINGSTAR-BULL-v1.0/SRC-PS` · M15
> Stop hit before TP1: -1.00R on the full position.

Tags: partials, sl-first-ticks
Context: atr=4 · trend=DOWN · swings=H4218.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.00 | 4203.50 |
| 2 | 09-16 10:15 | 4203.00 | 4203.80 | 4202.00 | 4203.40 |
| 3 | 09-16 10:30 | 4203.00 | 4209.50 | 4201.50 | 4209.00 |

Ticks (bid/ask): 09-16 10:45:02 4209.00/4209.20; 09-16 10:46:40 4201.80/4202.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4209.20
- stop: 4201.80
- R: 7.40
- target(s): 4210.50, 4218.00
- exit: STOP net -1.00R

#### `GV-P15-V04` · `GT-MORNINGSTAR-BULL-v1.0/SRC-PS` · M15
> No confirmed swing high above TP1: TP2 does not exist and the remaining 40% runs to stop/time stop. Here TP1 hits and the remainder is still open when the ticks end (PARTIAL_OPEN).

Tags: partials, no-tp2
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.00 | 4203.50 |
| 2 | 09-16 10:15 | 4203.00 | 4203.80 | 4202.00 | 4203.40 |
| 3 | 09-16 10:30 | 4203.00 | 4209.50 | 4201.50 | 4209.00 |

Ticks (bid/ask): 09-16 10:45:02 4209.00/4209.20; 09-16 10:46:40 4210.50/4210.70

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4209.20
- stop: 4201.80
- R: 7.40
- target(s): 4210.50, None
- exit: PARTIAL_OPEN

#### `GV-P15-V05` · `GT-MORNINGSTAR-BULL-v1.0/SRC-PS` · M15
> No TP2: TP1 hit, then stop: 0.6*0.1757 - 0.4 = -0.2946R.

Tags: partials, no-tp2, tp1-then-stop
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.00 | 4203.50 |
| 2 | 09-16 10:15 | 4203.00 | 4203.80 | 4202.00 | 4203.40 |
| 3 | 09-16 10:30 | 4203.00 | 4209.50 | 4201.50 | 4209.00 |

Ticks (bid/ask): 09-16 10:45:02 4209.00/4209.20; 09-16 10:46:40 4210.50/4210.70; 09-16 10:47:30 4201.80/4202.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4209.20
- stop: 4201.80
- R: 7.40
- target(s): 4210.50, None
- exit: MIXED net -109/370 (≈-0.2946)R

#### `GV-P15-V06` · `GT-MORNINGSTAR-BULL-v1.0/SRC-PS` · M15
> Entry ask 4210.70 is ABOVE TP1 (H1 = 4210.50): target already passed -> SKIPPED_TARGET_ALREADY_PASSED (no retrospective profit).

Tags: target-already-passed
Context: atr=4 · trend=DOWN · swings=H4218.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.00 | 4203.50 |
| 2 | 09-16 10:15 | 4203.00 | 4203.80 | 4202.00 | 4203.40 |
| 3 | 09-16 10:30 | 4203.00 | 4209.50 | 4201.50 | 4209.00 |

Ticks (bid/ask): 09-16 10:45:02 4210.50/4210.70

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_TARGET_ALREADY_PASSED
- entry: 4210.70
- stop: 4201.80
- R: 8.90

#### `GV-P15-V07` · `GT-MORNINGSTAR-BULL-v1.0/SRC-PS` · M15
> Entry ask 4210.50 EQUALS TP1: not strictly beyond the entry -> SKIPPED_TARGET_ALREADY_PASSED.

Tags: target-already-passed, boundary
Context: atr=4 · trend=DOWN · swings=H4218.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.00 | 4203.50 |
| 2 | 09-16 10:15 | 4203.00 | 4203.80 | 4202.00 | 4203.40 |
| 3 | 09-16 10:30 | 4203.00 | 4209.50 | 4201.50 | 4209.00 |

Ticks (bid/ask): 09-16 10:45:02 4210.30/4210.50

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_TARGET_ALREADY_PASSED
- entry: 4210.50
- stop: 4201.80
- R: 8.70

#### `GV-P15-V08` · `GT-MORNINGSTAR-BULL-v1.0/SRC-PS` · M15
> Entry ask 4210.49: TP1 is 0.01 beyond the entry -> trade taken.

Tags: target-already-passed, boundary
Context: atr=4 · trend=DOWN · swings=H4218.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.00 | 4203.50 |
| 2 | 09-16 10:15 | 4203.00 | 4203.80 | 4202.00 | 4203.40 |
| 3 | 09-16 10:30 | 4203.00 | 4209.50 | 4201.50 | 4209.00 |

Ticks (bid/ask): 09-16 10:45:02 4210.29/4210.49; 09-16 10:46:40 4210.50/4210.70; 09-16 10:47:30 4218.00/4218.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4210.49
- stop: 4201.80
- R: 8.69
- target(s): 4210.50, 4218.00
- exit: TARGET net 301/869 (≈0.3464)R

