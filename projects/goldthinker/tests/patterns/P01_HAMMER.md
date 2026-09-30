# P01 Hammer — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.3.1 · vector pack GV-0.2 · **54 vectors** (7 dormant, 47 firm)

Strategies covered: `GT-HAMMER-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-HAMMER-BULL-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4199.50/4200.00/4198.00/4199.90 | DOWN | 4 | shape ✔ · formed ✔ | — | R exactly 0.50*ATR = 2.00 -> passes (>=). |
| `B02` | 4199.51/4200.01/4198.00/4199.91 | DOWN | 4 | shape ✔ · formed ✔ | — | R = 2.01 (just inside). |
| `B03` | 4199.49/4199.99/4198.00/4199.89 | DOWN | 4 | no shape | R>=0.50ATR | R = 1.99 (just outside) -> only the range clause fails. |
| `B04` | 4196.60/4200.00/4190.00/4199.90 | DOWN | 4 | shape ✔ · formed ✔ | — | LW exactly 2*B (R=10: LW 6.60, B 3.30, UW 0.10) -> passes. |
| `B05` | 4196.60/4199.99/4190.00/4199.89 | DOWN | 4 | shape ✔ · formed ✔ | — | LW just above 2*B (B=3.29). |
| `B06` | 4196.60/4200.01/4190.00/4199.91 | DOWN | 4 | no shape | LW>=2B | LW just below 2*B (B=3.31, LW 6.60 < 6.62) -> only LW>=2B fails. |
| `B07` | 4198.40/4200.00/4194.00/4199.40 | DOWN | 4 | shape ✔ · formed ✔ | — | UW exactly 0.10*R (R=6.00, UW 0.60) -> passes. |
| `B08` | 4198.40/4199.99/4194.00/4199.40 | DOWN | 4 | shape ✔ · formed ✔ | — | UW just inside (0.59, R=5.99, limit 0.599). |
| `B09` | 4198.40/4200.01/4194.00/4199.40 | DOWN | 4 | no shape | UW<=0.10R | UW just outside (0.61 > 0.601) -> only UW clause fails. |
| `B10` | 4196.50/4200.00/4190.00/4199.10 | DOWN | 4 | shape ✔ · formed ✔ | — | Body bottom exactly at L+0.65R (R=10.00, LW=6.50) -> passes. |
| `B11` | 4196.51/4200.01/4190.00/4199.11 | DOWN | 4 | shape ✔ · formed ✔ | — | Body bottom just above the line (LW 6.51, R=10.01). |
| `B12` | 4196.49/4199.99/4190.00/4199.09 | DOWN | 4 | no shape | body_in_top35% | Body bottom just below the line (LW 6.49, R=9.99: line 6.4935) -> only the position clause fails. |
| `N01` | 4200.00/4206.50/4200.00/4200.20 | DOWN | 4 | no shape | LW>=2B, UW<=0.10R, body_in_top35% | Clean NO: all range above the body (that is a shooting-star shape), no lower wick. |
| `N02` | 4199.60/4200.00/4194.00/4198.60 | DOWN | 4 | shape ✔ · formed ✔ | — | Bearish-coloured body is fine (colour is not part of the shape). |
| `N03` | 4199.60/4200.00/4194.00/4199.60 | DOWN | 4 | shape ✔ · formed ✔ | — | Zero body (open = close) with a long lower wick: passes (LW>=0). |
| `N04` | 4200.00/4200.00/4200.00/4200.00 | DOWN | 4 | no shape | — | Zero range (O=H=L=C): R=0 bars never take part in any pattern (G0). |
| `QF1` | 4200.00/4200.50/4194.00/4200.20 | UP | 4 | canonical: SHAPE_DETECTED; candidate: HANGING_MAN; variant: no event; disposition: NOT_QUALIFIED; qualification_failures: PRIOR_STATE | — | The BASE variant of a shape in the wrong trend records the single failure PRIOR_STATE (candidate HANGING_MAN logged). |
| `T01` | 4200.00/4200.50/4194.00/4200.20 | UP | 4 | canonical: SHAPE_DETECTED; candidate: HANGING_MAN; variant: no event | — | Same shape after an UPTREND: SHAPE_DETECTED, not formed, candidate HANGING_MAN (G0b). |
| `T02` | 4200.00/4200.50/4194.00/4200.20 | RANGE | 4 | canonical: SHAPE_DETECTED; candidate: None; variant: no event | — | Shape after RANGE: shape yes, pattern not formed, no candidate. |
| `T03` | 4200.00/4200.50/4194.00/4200.20 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; candidate: None; variant: no event | — | Trend UNDETERMINED (fewer than two swings each side): shape yes, not formed. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:15:02 4200.20/4200.40; 09-16 10:17:00 4203.50/4203.70; 09-16 10:20:00 4213.60/4213.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.40; stop: 4193.80; R: 6.60; target(s): 4213.60; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:15:02 4200.20/4200.40; 09-16 10:17:00 4196.90/4197.10; 09-16 10:20:00 4193.80/4194.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.40; stop: 4193.80; R: 6.60; target(s): 4213.60; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4191.80 < stop): fill = that tick's bid, not the stop (G9): -43/33R. | 09-16 10:15:02 4200.20/4200.40; 09-16 10:17:00 4191.80/4192.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.40; stop: 4193.80; R: 6.60; target(s): 4213.60; exit: STOP net -43/33 (≈-1.3030)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:15:02 4200.20/4200.40; 09-16 10:16:40 4193.80/4194.00; 09-16 10:18:20 4213.60/4213.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.40; stop: 4193.80; R: 6.60; target(s): 4213.60; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:15:02 4200.20/4200.40; 09-16 10:16:40 4213.60/4213.80; 09-16 10:18:20 4193.80/4194.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.40; stop: 4193.80; R: 6.60; target(s): 4213.60; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:15:02 4200.20/4200.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.40; stop: 4193.80; R: 6.60; target(s): 4213.60; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:15:02 4200.20/4200.70; 09-16 10:18:20 4214.50/4215.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; spread_at_entry: 0.50; entry: 4200.70; stop: 4193.80; R: 6.90; target(s): 4214.50; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:30:00 4200.20/4200.40; 09-16 10:31:40 4213.60/4213.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.40; stop: 4193.80; R: 6.60; target(s): 4213.60; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:30:01 4200.20/4200.40; 09-16 10:31:40 4213.60/4213.80 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:15:02 4195.30/4195.80; 09-16 10:16:40 4199.80/4200.30 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4195.80; R: 2.00; target(s): 4199.80; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:15:02 4195.29/4195.79; 09-16 10:16:40 4199.79/4200.29 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4220.00 > target 4213.60): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:15:02 4200.20/4200.40; 09-16 10:17:00 4220.00/4220.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.40; stop: 4193.80; R: 6.60; target(s): 4213.60; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4200.20/4200.40; 09-21 00:30:00 4213.60/4213.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4200.40; stop: 4193.80; R: 6.60; target(s): 4213.60; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4200.20/4200.40; 09-21 00:30:00 4213.60/4213.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4200.40; stop: 4193.80; R: 6.60; target(s): 4213.60; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4200.20/4200.40 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P01-M01` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> mfe_before_mae_h (0.3): BID ticks from the reference time (10:15) to the horizon end (10:30). MAE 2.20 is reached at 10:16, MFE 2.80 only at 10:20 -> the adverse extreme comes FIRST -> FALSE.

Tags: raw, mfe-before-mae
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.20 | 4203.00 | 4198.00 | 4202.00 |

Ticks (bid/ask): 09-16 10:15:00 4200.20/4200.40; 09-16 10:16:00 4198.00/4198.20; 09-16 10:20:00 4203.00/4203.20; 09-16 10:25:00 4202.00/4202.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — h1: mfe=2.80, mae=2.20, mfe_before_mae=False

#### `GV-P01-M02` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> Same bar, ticks reversed: MFE 2.80 at 10:16 before MAE 2.20 at 10:20 -> TRUE.

Tags: raw, mfe-before-mae
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.20 | 4203.00 | 4198.00 | 4202.00 |

Ticks (bid/ask): 09-16 10:15:00 4200.20/4200.40; 09-16 10:16:00 4203.00/4203.20; 09-16 10:20:00 4198.00/4198.20; 09-16 10:25:00 4202.00/4202.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — h1: mfe=2.80, mae=2.20, mfe_before_mae=True

#### `GV-P01-M03` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> MAE = 0 (price never trades below the reference): mfe_before_mae is NULL.

Tags: raw, mfe-before-mae
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.20 | 4203.00 | 4200.20 | 4202.00 |

Ticks (bid/ask): 09-16 10:15:00 4200.20/4200.40; 09-16 10:20:00 4203.00/4203.20; 09-16 10:25:00 4202.00/4202.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — h1: mfe=2.80, mae=0.00, mfe_before_mae=None

#### `GV-P01-M04` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> The ticks do not reach the bar's extremes (highest tick 4202.00, lowest 4199.00 vs bar 4203.00 / 4198.00): the tick path does not cover the window -> NULL.

Tags: raw, mfe-before-mae
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.20 | 4203.00 | 4198.00 | 4202.00 |

Ticks (bid/ask): 09-16 10:15:00 4200.20/4200.40; 09-16 10:16:00 4199.00/4199.20; 09-16 10:20:00 4202.00/4202.20; 09-16 10:25:00 4202.00/4202.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — h1: mfe=2.80, mae=2.20, mfe_before_mae=None

#### `GV-P01-M05` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> Horizons differ: h1 window (bar 1 only) has MAE 0 -> NULL; h3 window (bars 1-3) has MFE 3.80 at 10:20 and MAE 4.20 only at 10:50 -> TRUE; h5 needs bars that do not exist -> NULL.

Tags: raw, mfe-before-mae, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.20 | 4204.00 | 4200.20 | 4203.00 |
| 3 | 09-16 10:30 | 4203.00 | 4203.50 | 4201.00 | 4202.00 |
| 4 | 09-16 10:45 | 4202.00 | 4202.50 | 4196.00 | 4197.00 |

Ticks (bid/ask): 09-16 10:15:00 4200.20/4200.40; 09-16 10:20:00 4204.00/4204.20; 09-16 10:29:59 4203.00/4203.20; 09-16 10:35:00 4203.50/4203.70; 09-16 10:40:00 4201.00/4201.20; 09-16 10:44:59 4202.00/4202.20; 09-16 10:46:00 4202.50/4202.70; 09-16 10:50:00 4196.00/4196.20; 09-16 10:55:00 4197.00/4197.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — h1: mfe=3.80, mae=0.00, mfe_before_mae=None | h3: mfe=3.80, mae=4.20, mfe_before_mae=True | h5: NULL

#### `GV-P01-Q01` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> A-30: ATR 4.1 -> G_BUFFER = max(0.20, 0.05 x 4.1 = 0.205) = 0.205, so the exact stop 4194.00 - 0.205 = 4193.795 lies between ticks. Long stops round AWAY from the entry (down): 4193.79. R = 4200.40 - 4193.79 = 6.61, 2R target 4213.62 (already on the grid). The virtual trade and the Vantage mirror use the same 4193.79.

Tags: quantisation, A-30
Context: atr=4.1 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-16 10:15:02 4200.20/4200.40; 09-16 10:16:40 4213.62/4213.82

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4200.40
- stop: 4193.79
- stop_exact: 4193.795
- R: 6.61
- target(s): 4213.62
- lots: 100/661 (≈0.1513)
- exit: TARGET net 2.00R

#### `GV-P01-R01` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.20 | 4203.20 | 4198.20 | 4201.20 |
| 3 | 09-16 10:30 | 4201.20 | 4204.20 | 4199.20 | 4202.20 |
| 4 | 09-16 10:45 | 4202.20 | 4203.20 | 4197.20 | 4199.20 |
| 5 | 09-16 11:00 | 4199.20 | 4202.20 | 4196.20 | 4200.20 |
| 6 | 09-16 11:15 | 4201.20 | 4205.20 | 4198.20 | 4203.20 |
| 7 | 09-16 11:30 | 4203.20 | 4209.20 | 4191.20 | 4204.20 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4200.20 | h1: ret=1.00, mfe=3.00, mae=2.00, end_index=1 | h3: ret=-1.00, mfe=4.00, mae=3.00, end_index=3 | h5: ret=3.00, mfe=5.00, mae=4.00, end_index=5 | h10: NULL | h20: NULL

#### `GV-P01-R02` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> RAW with all five horizons: ref = open of the bar after the signal (4200.20); ret_h = close[s+h] - ref = 0.10*h, MFE_h = 0.10*h + 0.05 (each bar's high is 0.05 above its close), MAE_h stays 0.05 (a non-negative magnitude) (the first bar's low). 21 bars follow, so h20 is populated (end index 20); a 20th bar missing would make h20 NULL.

Tags: raw, horizon_end, close-based
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.20 | 4200.35 | 4200.15 | 4200.30 |
| 3 | 09-16 10:30 | 4200.30 | 4200.45 | 4200.25 | 4200.40 |
| 4 | 09-16 10:45 | 4200.40 | 4200.55 | 4200.35 | 4200.50 |
| 5 | 09-16 11:00 | 4200.50 | 4200.65 | 4200.45 | 4200.60 |
| 6 | 09-16 11:15 | 4200.60 | 4200.75 | 4200.55 | 4200.70 |
| 7 | 09-16 11:30 | 4200.70 | 4200.85 | 4200.65 | 4200.80 |
| 8 | 09-16 11:45 | 4200.80 | 4200.95 | 4200.75 | 4200.90 |
| 9 | 09-16 12:00 | 4200.90 | 4201.05 | 4200.85 | 4201.00 |
| 10 | 09-16 12:15 | 4201.00 | 4201.15 | 4200.95 | 4201.10 |
| 11 | 09-16 12:30 | 4201.10 | 4201.25 | 4201.05 | 4201.20 |
| 12 | 09-16 12:45 | 4201.20 | 4201.35 | 4201.15 | 4201.30 |
| 13 | 09-16 13:00 | 4201.30 | 4201.45 | 4201.25 | 4201.40 |
| 14 | 09-16 13:15 | 4201.40 | 4201.55 | 4201.35 | 4201.50 |
| 15 | 09-16 13:30 | 4201.50 | 4201.65 | 4201.45 | 4201.60 |
| 16 | 09-16 13:45 | 4201.60 | 4201.75 | 4201.55 | 4201.70 |
| 17 | 09-16 14:00 | 4201.70 | 4201.85 | 4201.65 | 4201.80 |
| 18 | 09-16 14:15 | 4201.80 | 4201.95 | 4201.75 | 4201.90 |
| 19 | 09-16 14:30 | 4201.90 | 4202.05 | 4201.85 | 4202.00 |
| 20 | 09-16 14:45 | 4202.00 | 4202.15 | 4201.95 | 4202.10 |
| 21 | 09-16 15:00 | 4202.10 | 4202.25 | 4202.05 | 4202.20 |
| 22 | 09-16 15:15 | 4202.20 | 4202.35 | 4202.15 | 4202.30 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4200.20 | h1: end_index=1, ret=0.10, mfe=0.15, mae=0.05 | h3: end_index=3, ret=0.30, mfe=0.35, mae=0.05 | h5: end_index=5, ret=0.50, mfe=0.55, mae=0.05 | h10: end_index=10, ret=1.00, mfe=1.05, mae=0.05 | h20: end_index=20, ret=2.00, mfe=2.05, mae=0.05

#### `GV-P01-R03` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> Only 19 bars follow the signal: h20 needs bar s+20 -> NULL (data gap in the window); h10 is still populated.

Tags: raw, null-window
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.20 | 4200.35 | 4200.15 | 4200.30 |
| 3 | 09-16 10:30 | 4200.30 | 4200.45 | 4200.25 | 4200.40 |
| 4 | 09-16 10:45 | 4200.40 | 4200.55 | 4200.35 | 4200.50 |
| 5 | 09-16 11:00 | 4200.50 | 4200.65 | 4200.45 | 4200.60 |
| 6 | 09-16 11:15 | 4200.60 | 4200.75 | 4200.55 | 4200.70 |
| 7 | 09-16 11:30 | 4200.70 | 4200.85 | 4200.65 | 4200.80 |
| 8 | 09-16 11:45 | 4200.80 | 4200.95 | 4200.75 | 4200.90 |
| 9 | 09-16 12:00 | 4200.90 | 4201.05 | 4200.85 | 4201.00 |
| 10 | 09-16 12:15 | 4201.00 | 4201.15 | 4200.95 | 4201.10 |
| 11 | 09-16 12:30 | 4201.10 | 4201.25 | 4201.05 | 4201.20 |
| 12 | 09-16 12:45 | 4201.20 | 4201.35 | 4201.15 | 4201.30 |
| 13 | 09-16 13:00 | 4201.30 | 4201.45 | 4201.25 | 4201.40 |
| 14 | 09-16 13:15 | 4201.40 | 4201.55 | 4201.35 | 4201.50 |
| 15 | 09-16 13:30 | 4201.50 | 4201.65 | 4201.45 | 4201.60 |
| 16 | 09-16 13:45 | 4201.60 | 4201.75 | 4201.55 | 4201.70 |
| 17 | 09-16 14:00 | 4201.70 | 4201.85 | 4201.65 | 4201.80 |
| 18 | 09-16 14:15 | 4201.80 | 4201.95 | 4201.75 | 4201.90 |
| 19 | 09-16 14:30 | 4201.90 | 4202.05 | 4201.85 | 4202.00 |
| 20 | 09-16 14:45 | 4202.00 | 4202.15 | 4201.95 | 4202.10 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — h10: end_index=10, ret=1.00 | h20: NULL

#### `GV-P01-Y00` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> Spec example. R=6.5>=2.0, B=0.20, LW=6.0>=0.40, UW=0.30<=0.65, min(O,C)=4200.00>=4198.225. TREND DOWN -> pattern formed; BUY at ask 4200.40, stop 4194.00-0.20=4193.80, R=6.60, 2R target 4213.60.

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-16 10:15:02 4200.20/4200.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- candidate: None
- failing clause(s): none
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:15:00Z
- entry: 4200.40
- stop: 4193.80
- R: 6.60
- target(s): 4213.60
- lots: 5/33 (≈0.1515)

#### `GV-P01-Y01` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-16 10:15:02 4200.20/4200.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:15:00Z
- entry: 4200.40
- stop: 4193.80
- R: 6.60
- target(s): 4213.60

### Variant `SRC-PS`

#### `GV-DORM-P01-01` · `GT-HAMMER-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> DORMANT (PIP_SRC_USD = 0.10 assumed). Source variant qualifies while BASE does NOT: trend RANGE (canonical prior state fails, shape only) but the low sits at support, so 'DOWN OR AT_SUPPORT' holds. Confirmation: C2 bullish, close 4201.50 > H1 4200.50. Signal at C2 completion; stop = L1 - 17.5 pips x $0.10 = 4192.25; entry ask 4201.70; R 9.45; target 2R = 4220.60.

Tags: dormant, source-only-qualification, confirmation
Context: atr=4 · trend=RANGE · zones_pre=[4193.50-4193.90]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.30 | 4202.00 | 4200.00 | 4201.50 |

Ticks (bid/ask): 09-16 10:30:02 4201.50/4201.70; 09-16 10:31:40 4220.60/4220.80

- canonical: SHAPE_DETECTED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4201.70
- stop: 4192.25
- R: 9.45
- target(s): 4220.60
- exit: TARGET net 2.00R

#### `GV-DORM-P01-02` · `GT-HAMMER-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> Qualifies through the DOWN branch (no support zone): base formed too.

Tags: dormant, confirmation
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.30 | 4202.00 | 4200.00 | 4201.50 |

Ticks (bid/ask): 09-16 10:30:02 4201.50/4201.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- stop: 4192.25

#### `GV-DORM-P01-03` · `GT-HAMMER-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> Trend UP and no support: neither branch true -> variant not qualified (Hanging Man candidate logged).

Tags: dormant, variant-not-qualified
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.30 | 4202.00 | 4200.00 | 4201.50 |

Ticks (bid/ask): 09-16 10:30:02 4201.50/4201.70

- canonical: SHAPE_DETECTED
- candidate: HANGING_MAN
- variant: no event

#### `GV-DORM-P01-04` · `GT-HAMMER-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> Confirmation close exactly at H1 (4200.50): needs C2close > H1 -> expired (no trade, no retry).

Tags: dormant, confirmation, boundary, expiry
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.30 | 4200.60 | 4200.00 | 4200.50 |

Ticks (bid/ask): 09-16 10:30:02 4201.50/4201.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: EXPIRED_NO_CONFIRMATION

#### `GV-DORM-P01-05` · `GT-HAMMER-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> Confirmation close 4200.51 (one tick above H1): confirmed.

Tags: dormant, confirmation, boundary
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.30 | 4201.00 | 4200.00 | 4200.51 |

Ticks (bid/ask): 09-16 10:30:02 4201.50/4201.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE

#### `GV-DORM-P01-06` · `GT-HAMMER-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> C2 is bearish: confirmation fails -> expired.

Tags: dormant, confirmation, expiry
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.30 | 4200.40 | 4199.00 | 4199.50 |

Ticks (bid/ask): 09-16 10:30:02 4201.50/4201.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: EXPIRED_NO_CONFIRMATION

#### `GV-DORM-P01-07` · `GT-HAMMER-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> Only C1 exists so far: the variant is qualified and waiting (no expiry before C2 completes).

Tags: dormant, confirmation, pending
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: PENDING_CONFIRMATION

#### `GV-P01-DIS` · `GT-HAMMER-BULL-v1.0/SRC-PS` · M15
> DISABLED_PENDING_PIP_CONFIRMATION (D-032): the BASE pattern forms exactly as in GV-P01-Y01 (canonical events are still logged), but this source variant depends on PIP_SRC_USD, so it emits NO variant events, opens NO trade and has no ledger. The BASE strategy on the same candle is unaffected.

Tags: disabled-variant
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-16 10:15:02 4200.20/4200.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant status: DISABLED_PENDING_PIP_CONFIRMATION
- variant: no event

