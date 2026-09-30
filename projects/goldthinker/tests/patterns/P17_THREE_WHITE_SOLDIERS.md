# P17 Three White Soldiers — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.2.2 · vector pack GV-0.1 · **48 vectors** (47 firm, 1 provisional)

Strategies covered: `GT-3WHITESOLDIERS-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-3WHITESOLDIERS-BULL-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4200.00/4201.80/4199.80/4201.60 ; 4200.80/4204.00/4200.60/4203.80 ; 4202.00/4205.20/4201.80/4205.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Bar 1 body exactly 0.40*ATR = 1.60 (R 2.00): passes. |
| `B02` | 4200.00/4201.79/4199.80/4201.59 ; 4200.80/4204.00/4200.60/4203.80 ; 4202.00/4205.20/4201.80/4205.00 | DOWN | 4 | no shape | bar1 B>=0.40ATR | Bar 1 body 1.59: fails only bar1 B>=0.40ATR. |
| `B03` | 4200.00/4203.20/4199.80/4203.00 ; 4202.00/4206.00/4201.00/4205.00 ; 4204.00/4207.20/4203.80/4207.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Bar 2 body exactly 0.60*R (B 3.0, R 5.0: UW 1.0, LW 1.0): passes. |
| `B04` | 4200.00/4203.20/4199.80/4203.00 ; 4202.00/4206.01/4201.00/4205.00 ; 4204.00/4207.20/4203.80/4207.00 | DOWN | 4 | no shape | bar2 B>=0.60R | Bar 2 R = 5.01 (B/R = 0.5988): fails only bar2 B>=0.60R. |
| `B05` | 4200.00/4204.20/4199.80/4204.00 ; 4202.00/4210.00/4202.00/4208.00 ; 4206.00/4211.20/4205.80/4211.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Bar 2 upper wick exactly 0.25*R (B 6, UW 2.0, LW 0, R 8): passes. |
| `B06` | 4200.00/4204.20/4199.80/4204.00 ; 4202.00/4210.01/4202.00/4208.00 ; 4206.00/4211.20/4205.80/4211.00 | DOWN | 4 | no shape | bar2 UW<=0.25R | Bar 2 upper wick 2.01 (R 8.01; limit 2.0025): fails only bar2 UW<=0.25R. |
| `B07` | 4200.00/4204.20/4199.80/4204.00 ; 4200.00/4206.20/4199.80/4206.00 ; 4204.00/4209.20/4203.80/4209.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Bar 2 opens exactly at bar 1's open (4200.00): inside body 1: passes. |
| `B08` | 4200.00/4204.20/4199.80/4204.00 ; 4199.99/4206.20/4199.79/4206.00 ; 4204.00/4209.20/4203.80/4209.00 | DOWN | 4 | no shape | open2 in body1 | Bar 2 opens 0.01 below bar 1's open: fails only open2 in body1. |
| `B09` | 4200.00/4204.20/4199.80/4204.00 ; 4204.00/4210.20/4203.80/4210.00 ; 4208.00/4213.20/4207.80/4213.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Bar 2 opens exactly at bar 1's close (4204.00): passes. |
| `B10` | 4200.00/4204.20/4199.80/4204.00 ; 4204.01/4210.21/4203.81/4210.01 ; 4208.00/4213.20/4207.80/4213.00 | DOWN | 4 | no shape | open2 in body1 | Bar 2 opens 0.01 above bar 1's close: fails only open2 in body1. |
| `B11` | 4200.00/4203.20/4199.80/4203.00 ; 4201.00/4203.20/4200.80/4203.00 ; 4202.00/4205.20/4201.80/4205.00 | DOWN | 4 | no shape | C2>C1 | Bar 2 closes exactly at bar 1's close: fails only C2>C1 (strict). |
| `B12` | 4200.00/4203.20/4199.80/4203.00 ; 4201.00/4203.21/4200.80/4203.01 ; 4202.00/4205.20/4201.80/4205.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Bar 2 closes 0.01 above bar 1's close: passes. |
| `B13` | 4200.00/4204.20/4199.80/4204.00 ; 4202.00/4210.20/4201.80/4210.00 ; 4207.00/4212.20/4206.80/4212.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Largest body exactly 2x the smallest (4.0 vs 8.0): passes. |
| `B14` | 4200.00/4204.20/4199.80/4204.00 ; 4202.00/4210.21/4201.80/4210.01 ; 4207.00/4212.20/4206.80/4212.00 | DOWN | 4 | no shape | max(B)<=2*min(B) | Largest body 8.01 vs smallest 4.0: fails only the similarity clause. |
| `N01` | 4200.00/4204.20/4199.80/4204.00 ; 4202.00/4208.20/4201.80/4208.00 ; 4208.00/4208.20/4203.00/4203.20 | DOWN | 4 | no shape | bar3 bull, C3>C2 | Bar 3 is bearish: fails colour, C3>C2 and its own body-position clauses. |
| `NZ1` | 4200.00/4204.50/4199.50/4204.00 ; 4204.00/4204.50/4199.50/4200.00 ; 4200.00/4204.50/4199.50/4204.00 | DOWN | 4 | canonical: no event; variant: no event | — | Bull, bear, bull: colours break the soldiers. |
| `T01` | 4200.00/4204.20/4199.80/4204.00 ; 4202.00/4208.20/4201.80/4208.00 ; 4206.00/4211.20/4205.80/4211.00 | UP | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Three White Soldiers: no prior-state requirement in the canonical rule (trend UP recorded as context). |
| `T02` | 4200.00/4204.20/4199.80/4204.00 ; 4202.00/4208.20/4201.80/4208.00 ; 4206.00/4211.20/4205.80/4211.00 | RANGE | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Three White Soldiers: no prior-state requirement in the canonical rule (trend RANGE recorded as context). |
| `T03` | 4200.00/4204.20/4199.80/4204.00 ; 4202.00/4208.20/4201.80/4208.00 ; 4206.00/4211.20/4205.80/4211.00 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Three White Soldiers: no prior-state requirement in the canonical rule (trend UNDETERMINED recorded as context). |
| `T04` | 4200.00/4204.20/4199.80/4204.00 ; 4202.00/4208.20/4201.80/4208.00 ; 4206.00/4211.20/4205.80/4211.00 | DOWN | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Three White Soldiers: no prior-state requirement in the canonical rule (trend DOWN recorded as context). |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:45:02 4211.00/4211.20; 09-16 10:47:00 4216.80/4217.00; 09-16 10:50:00 4234.40/4234.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4199.60; R: 11.60; target(s): 4234.40; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:45:02 4211.00/4211.20; 09-16 10:47:00 4205.20/4205.40; 09-16 10:50:00 4199.60/4199.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4199.60; R: 11.60; target(s): 4234.40; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4197.60 < stop): fill = that tick's bid, not the stop (G9): -34/29R. | 09-16 10:45:02 4211.00/4211.20; 09-16 10:47:00 4197.60/4197.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4199.60; R: 11.60; target(s): 4234.40; exit: STOP net -34/29 (≈-1.1724)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:45:02 4211.00/4211.20; 09-16 10:46:40 4199.60/4199.80; 09-16 10:48:20 4234.40/4234.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4199.60; R: 11.60; target(s): 4234.40; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:45:02 4211.00/4211.20; 09-16 10:46:40 4234.40/4234.60; 09-16 10:48:20 4199.60/4199.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4199.60; R: 11.60; target(s): 4234.40; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:45:02 4211.00/4211.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4199.60; R: 11.60; target(s): 4234.40; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:45:02 4211.00/4211.50; 09-16 10:48:20 4235.30/4235.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.50; stop: 4199.60; R: 11.90; target(s): 4235.30; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 11:00:00 4211.00/4211.20; 09-16 11:01:40 4234.40/4234.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4199.60; R: 11.60; target(s): 4234.40; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 11:00:01 4211.00/4211.20; 09-16 11:01:40 4234.40/4234.60 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:45:02 4201.10/4201.60; 09-16 10:46:40 4205.60/4206.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4201.60; R: 2.00; target(s): 4205.60; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:45:02 4201.09/4201.59; 09-16 10:46:40 4205.59/4206.09 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4240.80 > target 4234.40): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:45:02 4211.00/4211.20; 09-16 10:47:00 4240.80/4241.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4199.60; R: 11.60; target(s): 4234.40; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4211.00/4211.20; 09-21 00:30:00 4234.40/4234.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4211.20; stop: 4199.60; R: 11.60; target(s): 4234.40; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4211.00/4211.20; 09-21 00:30:00 4234.40/4234.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4211.20; stop: 4199.60; R: 11.60; target(s): 4234.40; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4211.00/4211.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P17-R01` · `GT-3WHITESOLDIERS-BULL-v1.0/BASE` · M15
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4204.20 | 4199.80 | 4204.00 |
| 2 | 09-16 10:15 | 4202.00 | 4208.20 | 4201.80 | 4208.00 |
| 3 | 09-16 10:30 | 4206.00 | 4211.20 | 4205.80 | 4211.00 |
| 4 | 09-16 10:45 | 4211.00 | 4214.00 | 4209.00 | 4212.00 |
| 5 | 09-16 11:00 | 4212.00 | 4215.00 | 4210.00 | 4213.00 |
| 6 | 09-16 11:15 | 4213.00 | 4214.00 | 4208.00 | 4210.00 |
| 7 | 09-16 11:30 | 4210.00 | 4213.00 | 4207.00 | 4211.00 |
| 8 | 09-16 11:45 | 4212.00 | 4216.00 | 4209.00 | 4214.00 |
| 9 | 09-16 12:00 | 4214.00 | 4220.00 | 4202.00 | 4215.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4211.00 | h1: ret=1.00, mfe=3.00, mae=-2.00, end_index=3 | h3: ret=-1.00, mfe=4.00, mae=-3.00, end_index=5 | h5: ret=3.00, mfe=5.00, mae=-4.00, end_index=7 | h10: NULL | h20: NULL

#### `GV-P17-Y01` · `GT-3WHITESOLDIERS-BULL-v1.0/BASE` · M15
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4204.20 | 4199.80 | 4204.00 |
| 2 | 09-16 10:15 | 4202.00 | 4208.20 | 4201.80 | 4208.00 |
| 3 | 09-16 10:30 | 4206.00 | 4211.20 | 4205.80 | 4211.00 |

Ticks (bid/ask): 09-16 10:45:02 4211.00/4211.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:45:00Z
- entry: 4211.20
- stop: 4199.60
- R: 11.60
- target(s): 4234.40

### Variant `SRC-PS`

#### `GV-P17-V01` · `GT-3WHITESOLDIERS-BULL-v1.0/SRC-PS` · M15
> STOP_ENTRY: armed at 10:45 (bar 3 completes), buy-stop trigger = H3 = 4211.20, valid for the next three completed bars (to 11:30). A tick at 10:50 with ask 4211.10 does not trigger; at 11:10 ask = 4211.20 reaches the trigger exactly -> filled at that ASK. Stop L3-0.20 = 4205.60 (R 5.60); measured-move target 4222.60 (2.04R). signal_time = the trigger tick.

Tags: variant-clean-yes, stop-entry, trigger-exact
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4204.20 | 4199.80 | 4204.00 |
| 2 | 09-16 10:15 | 4202.00 | 4208.20 | 4201.80 | 4208.00 |
| 3 | 09-16 10:30 | 4206.00 | 4211.20 | 4205.80 | 4211.00 |

Ticks (bid/ask): 09-16 10:50:00 4210.90/4211.10; 09-16 11:10:00 4211.00/4211.20; 09-16 11:20:00 4222.60/4222.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4211.20
- signal time: 2026-09-16T11:10:00Z
- entry: 4211.20
- stop: 4205.60
- R: 5.60
- target(s): 4222.60
- exit: TARGET net 57/28 (≈2.0357)R

#### `GV-P17-V02` · `GT-3WHITESOLDIERS-BULL-v1.0/SRC-PS` · M15
> Ask 4211.19 (one tick under the trigger): no fill.

Tags: stop-entry, trigger-boundary
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4204.20 | 4199.80 | 4204.00 |
| 2 | 09-16 10:15 | 4202.00 | 4208.20 | 4201.80 | 4208.00 |
| 3 | 09-16 10:30 | 4206.00 | 4211.20 | 4205.80 | 4211.00 |

Ticks (bid/ask): 09-16 11:10:00 4210.99/4211.19

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: EXPIRED
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4211.20

#### `GV-P17-V03` · `GT-3WHITESOLDIERS-BULL-v1.0/SRC-PS` · M15
> Trigger reached only at 11:30:01, one second after the third bar completes: EXPIRED (no trade).

Tags: stop-entry, expiry
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4204.20 | 4199.80 | 4204.00 |
| 2 | 09-16 10:15 | 4202.00 | 4208.20 | 4201.80 | 4208.00 |
| 3 | 09-16 10:30 | 4206.00 | 4211.20 | 4205.80 | 4211.00 |

Ticks (bid/ask): 09-16 11:30:01 4211.20/4211.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: EXPIRED
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4211.20

#### `GV-P17-V04` · `GT-3WHITESOLDIERS-BULL-v1.0/SRC-PS` · M15 · **PROVISIONAL**
> Trigger reached exactly at 11:30:00, the instant the third bar completes. [PROVISIONAL: the spec does not say whether the completion instant belongs to the window (A-18); the calculator treats it as inside.]

Tags: stop-entry, expiry, boundary
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4204.20 | 4199.80 | 4204.00 |
| 2 | 09-16 10:15 | 4202.00 | 4208.20 | 4201.80 | 4208.00 |
| 3 | 09-16 10:30 | 4206.00 | 4211.20 | 4205.80 | 4211.00 |

Ticks (bid/ask): 09-16 11:30:00 4211.20/4211.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4211.20
- signal time: 2026-09-16T11:30:00Z
- entry: 4211.40
- stop: 4205.60
- R: 5.80

#### `GV-P17-V05` · `GT-3WHITESOLDIERS-BULL-v1.0/SRC-PS` · M15
> Price falls to the stop level (bid 4205.60) BEFORE the trigger: order cancelled, INVALIDATED_BEFORE_ENTRY. A later trigger tick does nothing.

Tags: stop-entry, invalidated
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4204.20 | 4199.80 | 4204.00 |
| 2 | 09-16 10:15 | 4202.00 | 4208.20 | 4201.80 | 4208.00 |
| 3 | 09-16 10:30 | 4206.00 | 4211.20 | 4205.80 | 4211.00 |

Ticks (bid/ask): 09-16 10:55:00 4205.60/4205.80; 09-16 11:10:00 4211.20/4211.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: INVALIDATED_BEFORE_ENTRY
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4211.20

#### `GV-P17-V06` · `GT-3WHITESOLDIERS-BULL-v1.0/SRC-PS` · M15
> Bid 4205.61 (one tick above the stop level) does NOT cancel the order; the trigger later fills.

Tags: stop-entry, invalidated, boundary
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4204.20 | 4199.80 | 4204.00 |
| 2 | 09-16 10:15 | 4202.00 | 4208.20 | 4201.80 | 4208.00 |
| 3 | 09-16 10:30 | 4206.00 | 4211.20 | 4205.80 | 4211.00 |

Ticks (bid/ask): 09-16 10:55:00 4205.61/4205.81; 09-16 11:10:00 4211.20/4211.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4211.20
- signal time: 2026-09-16T11:10:00Z
- entry: 4211.40
- stop: 4205.60
- R: 5.80

#### `GV-P17-V07` · `GT-3WHITESOLDIERS-BULL-v1.0/SRC-PS` · M15
> A tick at 10:40 with ask 4211.50 is BEFORE the pattern completed (armed at 10:45): ignored. No later trigger -> EXPIRED.

Tags: stop-entry, before-arm
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4204.20 | 4199.80 | 4204.00 |
| 2 | 09-16 10:15 | 4202.00 | 4208.20 | 4201.80 | 4208.00 |
| 3 | 09-16 10:30 | 4206.00 | 4211.20 | 4205.80 | 4211.00 |

Ticks (bid/ask): 09-16 10:40:00 4211.30/4211.50

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: EXPIRED
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4211.20

#### `GV-P17-V08` · `GT-3WHITESOLDIERS-BULL-v1.0/SRC-PS` · M15
> Gap: the first tick above the trigger is already at ask 4223.20, beyond the 4222.60 target: entered at 4223.20 would leave the target behind the entry -> SKIPPED_TARGET_ALREADY_PASSED.

Tags: stop-entry, target-already-passed
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4204.20 | 4199.80 | 4204.00 |
| 2 | 09-16 10:15 | 4202.00 | 4208.20 | 4201.80 | 4208.00 |
| 3 | 09-16 10:30 | 4206.00 | 4211.20 | 4205.80 | 4211.00 |

Ticks (bid/ask): 09-16 11:10:00 4223.00/4223.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_TARGET_ALREADY_PASSED
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4211.20
- signal time: 2026-09-16T11:10:00Z

#### `GV-P17-V09` · `GT-3WHITESOLDIERS-BULL-v1.0/SRC-PS` · M15
> Buy-stop fills at the ASK even when it gaps above the trigger: ask 4212.20 -> entry 4212.20 (R 6.60), target 4222.60 (1.58R), stop hit later.

Tags: stop-entry, gap-above-trigger
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4204.20 | 4199.80 | 4204.00 |
| 2 | 09-16 10:15 | 4202.00 | 4208.20 | 4201.80 | 4208.00 |
| 3 | 09-16 10:30 | 4206.00 | 4211.20 | 4205.80 | 4211.00 |

Ticks (bid/ask): 09-16 11:10:00 4212.00/4212.20; 09-16 11:40:00 4205.60/4205.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4211.20
- signal time: 2026-09-16T11:10:00Z
- entry: 4212.20
- stop: 4205.60
- R: 6.60
- target(s): 4222.60
- exit: STOP net -1.00R

#### `GV-P17-V10` · `GT-3WHITESOLDIERS-BULL-v1.0/SRC-PS` · H1
> Weekend: the H1 pattern completes at the Friday 22:00 close (arm_time). The order lives through the next THREE completed bars after the reopening (Sun 23:00, Mon 00:00, Mon 01:00) -> expiry Mon 02:00. A trigger at Sun 23:30 fills.

Tags: stop-entry, weekend-entry
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 19:00 | 4200.00 | 4204.20 | 4199.80 | 4204.00 |
| 2 | 09-18 20:00 | 4202.00 | 4208.20 | 4201.80 | 4208.00 |
| 3 | 09-18 21:00 | 4206.00 | 4211.20 | 4205.80 | 4211.00 |

Ticks (bid/ask): 09-20 23:30:00 4211.20/4211.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- arm time: 2026-09-18T22:00:00Z
- expiry time: 2026-09-21T02:00:00Z
- trigger: 4211.20
- signal time: 2026-09-20T23:30:00Z
- entry: 4211.40
- stop: 4205.60
- R: 5.80

#### `GV-P17-V11` · `GT-3WHITESOLDIERS-BULL-v1.0/SRC-PS` · H1
> Same weekend order, trigger tick at Mon 02:00:01 (after the third bar): EXPIRED.

Tags: stop-entry, weekend-entry, expiry
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 19:00 | 4200.00 | 4204.20 | 4199.80 | 4204.00 |
| 2 | 09-18 20:00 | 4202.00 | 4208.20 | 4201.80 | 4208.00 |
| 3 | 09-18 21:00 | 4206.00 | 4211.20 | 4205.80 | 4211.00 |

Ticks (bid/ask): 09-21 02:00:01 4211.20/4211.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: EXPIRED
- arm time: 2026-09-18T22:00:00Z
- expiry time: 2026-09-21T02:00:00Z
- trigger: 4211.20

