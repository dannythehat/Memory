# P02 Shooting Star — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.3 · vector pack GV-0.2 · **44 vectors** (3 dormant, 41 firm)

Strategies covered: `GT-SHOOTINGSTAR-BEAR-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-SHOOTINGSTAR-BEAR-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4200.50/4202.00/4200.00/4200.10 | UP | 4 | shape ✔ · formed ✔ | — | R exactly 0.50*ATR = 2.00 -> passes (>=). |
| `B02` | 4200.49/4202.00/4199.99/4200.09 | UP | 4 | shape ✔ · formed ✔ | — | R = 2.01 (just inside). |
| `B03` | 4200.51/4202.00/4200.01/4200.11 | UP | 4 | no shape | (1 clause) | R = 1.99 (just outside) -> only the range clause fails. |
| `B04` | 4203.40/4210.00/4200.00/4200.10 | UP | 4 | shape ✔ · formed ✔ | — | LW exactly 2*B (R=10: LW 6.60, B 3.30, UW 0.10) -> passes. |
| `B05` | 4203.40/4210.00/4200.01/4200.11 | UP | 4 | shape ✔ · formed ✔ | — | LW just above 2*B (B=3.29). |
| `B06` | 4203.40/4210.00/4199.99/4200.09 | UP | 4 | no shape | (1 clause) | LW just below 2*B (B=3.31, LW 6.60 < 6.62) -> only LW>=2B fails. |
| `B07` | 4201.60/4206.00/4200.00/4200.60 | UP | 4 | shape ✔ · formed ✔ | — | UW exactly 0.10*R (R=6.00, UW 0.60) -> passes. |
| `B08` | 4201.60/4206.00/4200.01/4200.60 | UP | 4 | shape ✔ · formed ✔ | — | UW just inside (0.59, R=5.99, limit 0.599). |
| `B09` | 4201.60/4206.00/4199.99/4200.60 | UP | 4 | no shape | (1 clause) | UW just outside (0.61 > 0.601) -> only UW clause fails. |
| `B10` | 4203.50/4210.00/4200.00/4200.90 | UP | 4 | shape ✔ · formed ✔ | — | Body bottom exactly at L+0.65R (R=10.00, LW=6.50) -> passes. |
| `B11` | 4203.49/4210.00/4199.99/4200.89 | UP | 4 | shape ✔ · formed ✔ | — | Body bottom just above the line (LW 6.51, R=10.01). |
| `B12` | 4203.51/4210.00/4200.01/4200.91 | UP | 4 | no shape | (1 clause) | Body bottom just below the line (LW 6.49, R=9.99: line 6.4935) -> only the position clause fails. |
| `N01` | 4200.00/4200.00/4193.50/4199.80 | UP | 4 | no shape | (3 clause) | Clean NO: all range above the body (that is a shooting-star shape), no lower wick. |
| `N02` | 4200.40/4206.00/4200.00/4201.40 | UP | 4 | shape ✔ · formed ✔ | — | Bearish-coloured body is fine (colour is not part of the shape). |
| `N03` | 4200.40/4206.00/4200.00/4200.40 | UP | 4 | shape ✔ · formed ✔ | — | Zero body (open = close) with a long lower wick: passes (LW>=0). |
| `N04` | 4200.00/4200.00/4200.00/4200.00 | UP | 4 | no shape | — | Zero range (O=H=L=C): R=0 bars never take part in any pattern (G0). |
| `QF1` | 4200.00/4206.00/4199.50/4199.80 | DOWN | 4 | canonical: SHAPE_DETECTED; candidate: INVERTED_HAMMER; variant: no event; disposition: NOT_QUALIFIED; qualification_failures: PRIOR_STATE | — | The BASE variant of a shape in the wrong trend records the single failure PRIOR_STATE (candidate HANGING_MAN logged). |
| `T01` | 4200.00/4206.00/4199.50/4199.80 | DOWN | 4 | canonical: SHAPE_DETECTED; candidate: INVERTED_HAMMER; variant: no event | — | Same shape after an UPTREND: SHAPE_DETECTED, not formed, candidate HANGING_MAN (G0b). |
| `T02` | 4200.00/4206.00/4199.50/4199.80 | RANGE | 4 | canonical: SHAPE_DETECTED; candidate: None; variant: no event | — | Shape after RANGE: shape yes, pattern not formed, no candidate. |
| `T03` | 4200.00/4206.00/4199.50/4199.80 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; candidate: None; variant: no event | — | Trend UNDETERMINED (fewer than two swings each side): shape yes, not formed. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:15:02 4199.60/4199.80; 09-16 10:17:00 4196.30/4196.50; 09-16 10:20:00 4186.20/4186.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.60; stop: 4206.20; R: 6.60; target(s): 4186.40; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:15:02 4199.60/4199.80; 09-16 10:17:00 4202.90/4203.10; 09-16 10:20:00 4206.00/4206.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.60; stop: 4206.20; R: 6.60; target(s): 4186.40; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4191.80 < stop): fill = that tick's bid, not the stop (G9): -43/33R. | 09-16 10:15:02 4199.60/4199.80; 09-16 10:17:00 4208.00/4208.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.60; stop: 4206.20; R: 6.60; target(s): 4186.40; exit: STOP net -43/33 (≈-1.3030)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:15:02 4199.60/4199.80; 09-16 10:16:40 4206.00/4206.20; 09-16 10:18:20 4186.20/4186.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.60; stop: 4206.20; R: 6.60; target(s): 4186.40; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:15:02 4199.60/4199.80; 09-16 10:16:40 4186.20/4186.40; 09-16 10:18:20 4206.00/4206.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.60; stop: 4206.20; R: 6.60; target(s): 4186.40; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:15:02 4199.60/4199.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.60; stop: 4206.20; R: 6.60; target(s): 4186.40; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:15:02 4199.30/4199.80; 09-16 10:18:20 4185.00/4185.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; spread_at_entry: 0.50; entry: 4199.30; stop: 4206.20; R: 6.90; target(s): 4185.50; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:30:00 4199.60/4199.80; 09-16 10:31:40 4186.20/4186.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.60; stop: 4206.20; R: 6.60; target(s): 4186.40; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:30:01 4199.60/4199.80; 09-16 10:31:40 4186.20/4186.40 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:15:02 4204.20/4204.70; 09-16 10:16:40 4199.70/4200.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4204.20; R: 2.00; target(s): 4200.20; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:15:02 4204.21/4204.71; 09-16 10:16:40 4199.71/4200.21 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4220.00 > target 4213.60): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:15:02 4199.60/4199.80; 09-16 10:17:00 4179.80/4180.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.60; stop: 4206.20; R: 6.60; target(s): 4186.40; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4199.60/4199.80; 09-21 00:30:00 4186.20/4186.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4199.60; stop: 4206.20; R: 6.60; target(s): 4186.40; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4199.60/4199.80; 09-21 00:30:00 4186.20/4186.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4199.60; stop: 4206.20; R: 6.60; target(s): 4186.40; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4199.60/4199.80 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P02-M01` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · M15
> Short: favourable = ref minus the low (4.80 at 10:20), adverse = the high minus ref (1.20 at 10:16, first) -> FALSE.

Tags: raw, mfe-before-mae
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |
| 2 | 09-16 10:15 | 4199.80 | 4201.00 | 4195.00 | 4196.00 |

Ticks (bid/ask): 09-16 10:15:00 4199.80/4200.00; 09-16 10:16:00 4201.00/4201.20; 09-16 10:20:00 4195.00/4195.20; 09-16 10:25:00 4196.00/4196.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — h1: mfe=4.80, mae=1.20, mfe_before_mae=False

#### `GV-P02-Q01` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P01-Q01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> A-30: ATR 4.1 -> G_BUFFER = max(0.20, 0.05 x 4.1 = 0.205) = 0.205, so the exact stop 4194.00 - 0.205 = 4193.795 lies between ticks. Long stops round AWAY from the entry (down): 4193.79. R = 4200.40 - 4193.79 = 6.61, 2R target 4213.62 (already on the grid). The virtual trade and the Vantage mirror use the same 4193.79.

Tags: quantisation, A-30
Context: atr=4.1 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |

Ticks (bid/ask): 09-16 10:15:02 4199.60/4199.80; 09-16 10:16:40 4186.18/4186.38

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4199.60
- stop: 4206.21
- stop_exact: 4206.205
- R: 6.61
- target(s): 4186.38
- lots: 100/661 (≈0.1513)
- exit: TARGET net 2.00R

#### `GV-P02-R01` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P01-R01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |
| 2 | 09-16 10:15 | 4199.80 | 4201.80 | 4196.80 | 4198.80 |
| 3 | 09-16 10:30 | 4198.80 | 4200.80 | 4195.80 | 4197.80 |
| 4 | 09-16 10:45 | 4197.80 | 4202.80 | 4196.80 | 4200.80 |
| 5 | 09-16 11:00 | 4200.80 | 4203.80 | 4197.80 | 4199.80 |
| 6 | 09-16 11:15 | 4198.80 | 4201.80 | 4194.80 | 4196.80 |
| 7 | 09-16 11:30 | 4196.80 | 4208.80 | 4190.80 | 4195.80 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4199.80 | h1: ret=1.00, mfe=3.00, mae=2.00, end_index=1 | h3: ret=-1.00, mfe=4.00, mae=3.00, end_index=3 | h5: ret=3.00, mfe=5.00, mae=4.00, end_index=5 | h10: NULL | h20: NULL

#### `GV-P02-Y00` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P01-Y00` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Spec example. R=6.5>=2.0, B=0.20, LW=6.0>=0.40, UW=0.30<=0.65, min(O,C)=4200.00>=4198.225. TREND DOWN -> pattern formed; BUY at ask 4200.40, stop 4194.00-0.20=4193.80, R=6.60, 2R target 4213.60.

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |

Ticks (bid/ask): 09-16 10:15:02 4199.60/4199.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- candidate: None
- failing clauses: 0
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:15:00Z
- entry: 4199.60
- stop: 4206.20
- R: 6.60
- target(s): 4186.40
- lots: 5/33 (≈0.1515)

#### `GV-P02-Y01` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P01-Y01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |

Ticks (bid/ask): 09-16 10:15:02 4199.60/4199.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:15:00Z
- entry: 4199.60
- stop: 4206.20
- R: 6.60
- target(s): 4186.40

### Variant `SRC-PS`

#### `GV-DORM-P02-01` · `GT-SHOOTINGSTAR-BEAR-v1.0/SRC-PS` · M15 · **DORMANT**
> DORMANT. Source Shooting Star: confirmed by a bearish C2 closing below min(O1,C1)=4199.80 (4198.50). SELL at the bid 4198.50; stop = H1 + 20 pips x $0.10 = 4208.00; R 9.50; T_SWING(1.5): swing low 4184.00 = 1.53R.

Tags: dormant, confirmation
Context: atr=4 · trend=UP · swings=L4184.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |
| 2 | 09-16 10:15 | 4199.70 | 4199.90 | 4198.00 | 4198.50 |

Ticks (bid/ask): 09-16 10:30:02 4198.50/4198.70; 09-16 10:31:40 4183.80/4184.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4198.50
- stop: 4208.00
- R: 9.50
- target(s): 4184.00
- exit: TARGET net 29/19 (≈1.5263)R

#### `GV-DORM-P02-02` · `GT-SHOOTINGSTAR-BEAR-v1.0/SRC-PS` · M15 · **DORMANT**
> Signal at 03:00 UTC (ASIA_ONLY): the source skips Asia-only shooting stars.

Tags: dormant, session
Context: atr=4 · trend=UP · swings=L4184.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 02:30 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |
| 2 | 09-16 02:45 | 4199.70 | 4199.90 | 4198.00 | 4198.50 |

Ticks (bid/ask): 09-16 03:00:02 4198.50/4198.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SESSION_FILTER
- signal time: 2026-09-16T03:00:00Z

#### `GV-DORM-P02-03` · `GT-SHOOTINGSTAR-BEAR-v1.0/SRC-PS` · M15 · **DORMANT**
> Source-only qualification: trend DOWN (canonical fails) but the high (4206.00) is 0.20 below a resistance zone -> AT_RESISTANCE -> qualifies. Signal 07:15 UTC = 08:15 BST: London is open, so not skipped.

Tags: dormant, source-only-qualification, session
Context: atr=4 · trend=DOWN · zones_pre=[4206.20-4207.00] · swings=L4184.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 06:45 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |
| 2 | 09-16 07:00 | 4199.70 | 4199.90 | 4198.00 | 4198.50 |

Ticks (bid/ask): 09-16 07:15:02 4198.50/4198.70; 09-16 07:16:40 4183.80/4184.00

- canonical: SHAPE_DETECTED
- candidate: INVERTED_HAMMER
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T07:15:00Z

#### `GV-P02-DIS` · `GT-SHOOTINGSTAR-BEAR-v1.0/SRC-PS` · M15
> DISABLED_PENDING_PIP_CONFIRMATION (D-032): the BASE pattern forms exactly as in GV-P02-Y01 (canonical events are still logged), but this source variant depends on PIP_SRC_USD, so it emits NO variant events, opens NO trade and has no ledger. The BASE strategy on the same candle is unaffected.

Tags: disabled-variant
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |

Ticks (bid/ask): 09-16 10:15:02 4199.60/4199.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant status: DISABLED_PENDING_PIP_CONFIRMATION
- variant: no event

