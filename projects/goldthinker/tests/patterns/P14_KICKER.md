# P14 Kicker — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.3.1 · vector pack GV-0.2 · **97 vectors** (97 firm)

Strategies covered: `GT-KICKER-BEAR-v1.0`, `GT-KICKER-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-KICKER-BEAR-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01m` | 4190.00/4196.50/4189.50/4196.00 ; 4190.00/4190.20/4182.50/4182.60 | UP | 4 | shape ✔ · formed ✔ | — | O2 exactly O1 (4210.00): C2's body touches C1's body top but does not overlap -> passes. |
| `B02m` | 4190.00/4196.50/4189.50/4196.00 ; 4190.01/4190.20/4182.50/4182.60 | UP | 4 | no shape | (1 clause) | O2 = O1 - 0.01: only O2>=O1 fails. |
| `B03m` | 4190.00/4196.50/4189.50/4196.00 ; 4189.00/4189.50/4182.00/4182.75 | UP | 4 | shape ✔ · formed ✔ | — | Close exactly at H2 - 0.10*R2 (R2=7.50: 4217.25): passes. |
| `B04m` | 4190.00/4196.50/4189.50/4196.00 ; 4189.00/4189.50/4182.00/4182.76 | UP | 4 | no shape | (1 clause) | Close 0.01 lower: only the close-near-high clause fails. |
| `B05m` | 4190.00/4196.50/4189.50/4196.00 ; 4189.00/4189.10/4186.90/4187.00 | UP | 4 | no shape | (1 clause) | C2 is not LARGE (B=2.0, R=2.2): fails LARGE(C2) only. |
| `B06m` | 4194.00/4196.20/4193.70/4196.00 ; 4193.00/4193.50/4186.00/4186.20 | UP | 4 | no shape | (1 clause) | C1 is not LARGE (small bearish candle, B=2.0, R=2.5): fails LARGE(C1) only. |
| `F01m` | 4190.00/4196.50/4189.50/4196.00 ; 4189.80/4190.00/4182.00/4182.10 | UP | 4 | shape ✔ · formed ✔ | — | gap_thr 0.20: O2 = O1 + 0.20 exactly -> bull_gap_flag true. |
| `F02m` | 4190.00/4196.50/4189.50/4196.00 ; 4189.81/4190.00/4182.00/4182.10 | UP | 4 | shape ✔ · formed ✔ | — | O2 = O1 + 0.19: flag false; pattern still forms. |
| `N01m` | 4190.00/4196.50/4189.50/4196.00 ; 4183.00/4189.50/4182.00/4189.00 | UP | 4 | no shape | (2 clause) | C2 bearish (opens 4217, closes 4211): fails colour and the close-near-high test. |
| `NZ1m` | 4200.00/4200.50/4195.50/4196.00 ; 4196.00/4196.50/4191.50/4192.00 | UP | 4 | canonical: no event; variant: no event | — | Two bullish candles: no bearish LARGE C1. |
| `T01m` | 4190.00/4196.50/4189.50/4196.00 ; 4189.00/4189.50/4182.00/4182.20 | DOWN | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Kicker shape after UP: not formed (bullish kicker needs DOWN). |
| `T02m` | 4190.00/4196.50/4189.50/4196.00 ; 4189.00/4189.50/4182.00/4182.20 | RANGE | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Kicker shape after RANGE: not formed (bullish kicker needs DOWN). |
| `T03m` | 4190.00/4196.50/4189.50/4196.00 ; 4189.00/4189.50/4182.00/4182.20 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Kicker shape after UNDETERMINED: not formed (bullish kicker needs DOWN). |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01m` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:30:02 4182.00/4182.20; 09-16 10:32:00 4174.65/4174.85; 09-16 10:35:00 4152.40/4152.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4182.00; stop: 4196.70; R: 14.70; target(s): 4152.60; exit: TARGET net 2.00R |
| `L02m` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:30:02 4182.00/4182.20; 09-16 10:32:00 4189.35/4189.55; 09-16 10:35:00 4196.50/4196.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4182.00; stop: 4196.70; R: 14.70; target(s): 4152.60; exit: STOP net -1.00R |
| `L03m` | Tick gaps through the stop (bid 4201.30 < stop): fill = that tick's bid, not the stop (G9): -167/147R. | 09-16 10:30:02 4182.00/4182.20; 09-16 10:32:00 4198.50/4198.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4182.00; stop: 4196.70; R: 14.70; target(s): 4152.60; exit: STOP net -167/147 (≈-1.1361)R |
| `L04m` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:30:02 4182.00/4182.20; 09-16 10:31:40 4196.50/4196.70; 09-16 10:33:20 4152.40/4152.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4182.00; stop: 4196.70; R: 14.70; target(s): 4152.60; exit: STOP net -1.00R |
| `L05m` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:30:02 4182.00/4182.20; 09-16 10:31:40 4152.40/4152.60; 09-16 10:33:20 4196.50/4196.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4182.00; stop: 4196.70; R: 14.70; target(s): 4152.60; exit: TARGET net 2.00R |
| `L06m` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:30:02 4182.00/4182.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4182.00; stop: 4196.70; R: 14.70; target(s): 4152.60; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07m` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:30:02 4181.70/4182.20; 09-16 10:33:20 4151.20/4151.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; spread_at_entry: 0.50; entry: 4181.70; stop: 4196.70; R: 15.00; target(s): 4151.70; exit: TARGET net 2.00R |
| `L08m` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:45:00 4182.00/4182.20; 09-16 10:46:40 4152.40/4152.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4182.00; stop: 4196.70; R: 14.70; target(s): 4152.60; exit: TARGET net 2.00R |
| `L09m` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:45:01 4182.00/4182.20; 09-16 10:46:40 4152.40/4152.60 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10m` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:30:02 4194.70/4195.20; 09-16 10:31:40 4190.20/4190.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4194.70; R: 2.00; target(s): 4190.70; exit: TARGET net 2.00R |
| `L11m` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:30:02 4194.71/4195.21; 09-16 10:31:40 4190.21/4190.71 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12m` | Tick jumps far past the target (bid 4253.80 > target 4247.40): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:30:02 4182.00/4182.20; 09-16 10:32:00 4146.00/4146.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4182.00; stop: 4196.70; R: 14.70; target(s): 4152.60; exit: TARGET net 2.00R |
| `W01m` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4182.00/4182.20; 09-21 00:30:00 4152.40/4152.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4182.00; stop: 4196.70; R: 14.70; target(s): 4152.60; entry_across_break: True; exit: TARGET net 2.00R |
| `W02m` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4182.00/4182.20; 09-21 00:30:00 4152.40/4152.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4182.00; stop: 4196.70; R: 14.70; target(s): 4152.60; entry_across_break: True; exit: TARGET net 2.00R |
| `W03m` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4182.00/4182.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P14-R01m` · `GT-KICKER-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P14-R01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4189.00 | 4189.50 | 4182.00 | 4182.20 |
| 3 | 09-16 10:30 | 4182.20 | 4184.20 | 4179.20 | 4181.20 |
| 4 | 09-16 10:45 | 4181.20 | 4183.20 | 4178.20 | 4180.20 |
| 5 | 09-16 11:00 | 4180.20 | 4185.20 | 4179.20 | 4183.20 |
| 6 | 09-16 11:15 | 4183.20 | 4186.20 | 4180.20 | 4182.20 |
| 7 | 09-16 11:30 | 4181.20 | 4184.20 | 4177.20 | 4179.20 |
| 8 | 09-16 11:45 | 4179.20 | 4191.20 | 4173.20 | 4178.20 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4182.20 | h1: ret=1.00, mfe=3.00, mae=2.00, end_index=2 | h3: ret=-1.00, mfe=4.00, mae=3.00, end_index=4 | h5: ret=3.00, mfe=5.00, mae=4.00, end_index=6 | h10: NULL | h20: NULL

#### `GV-P14-V00m` · `GT-KICKER-BEAR-v1.0/BASE` · H1
*Mirror of `GV-P14-V00` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> BASE on the same bars: stop = min(L1,L2) - 0.20; L2 (4203.40) is below L1 (4203.50), so the stop is 4203.20. Compare V01-H1: the source variant stops beyond C1's low only (4203.30).

Tags: base-vs-source
Context: atr=4 · trend=UP · swings=L4150.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 11:00 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-16 12:00:02 4178.80/4179.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4178.80
- stop: 4196.80
- R: 18.00
- target(s): 4142.80

#### `GV-P14-Y01m` · `GT-KICKER-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P14-Y01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4189.00 | 4189.50 | 4182.00 | 4182.20 |

Ticks (bid/ask): 09-16 10:30:02 4182.00/4182.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4182.00
- stop: 4196.70
- R: 14.70
- target(s): 4152.60

### Variant `SRC-PS-COMPLETED`

#### `GV-P14-V01-D1m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · D1
*Mirror of `GV-P14-V01-D1` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> D1 is an allowed timeframe for the source Kicker. Stop = C1's low - 0.20 = 4203.30 (not C2's, unlike the baseline); entry ask 4221.20; R 17.90; T_SWING(1.5) = swing high 4250.00 (1.61R) -> trade. Signal at the scheduled closure start, entry after the closure (entry_across_break).

Tags: variant, tf-gate, tf-D1
Context: atr=4 · trend=UP · swings=L4150.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-13 23:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-14 23:00 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-15 23:00:02 4178.80/4179.00; 09-15 23:01:42 4149.80/4150.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-15T22:00:00Z
- entry: 4178.80
- stop: 4196.70
- R: 17.90
- target(s): 4150.00
- exit: TARGET net 288/179 (≈1.6089)R

#### `GV-P14-V01-H1m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · H1
*Mirror of `GV-P14-V01-H1` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> H1 is an allowed timeframe for the source Kicker. Stop = C1's low - 0.20 = 4203.30 (not C2's, unlike the baseline); entry ask 4221.20; R 17.90; T_SWING(1.5) = swing high 4250.00 (1.61R) -> trade.

Tags: variant, tf-gate, tf-H1
Context: atr=4 · trend=UP · swings=L4150.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 11:00 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-16 12:00:02 4178.80/4179.00; 09-16 12:01:40 4149.80/4150.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T12:00:00Z
- entry: 4178.80
- stop: 4196.70
- R: 17.90
- target(s): 4150.00
- exit: TARGET net 288/179 (≈1.6089)R

#### `GV-P14-V01-H4m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · H4
*Mirror of `GV-P14-V01-H4` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> H4 is an allowed timeframe for the source Kicker. Stop = C1's low - 0.20 = 4203.30 (not C2's, unlike the baseline); entry ask 4221.20; R 17.90; T_SWING(1.5) = swing high 4250.00 (1.61R) -> trade. Signal at the scheduled closure start, entry after the closure (entry_across_break).

Tags: variant, tf-gate, tf-H4
Context: atr=4 · trend=UP · swings=L4150.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 11:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 15:00 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-16 19:00:02 4178.80/4179.00; 09-16 19:01:42 4149.80/4150.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T19:00:00Z
- entry: 4178.80
- stop: 4196.70
- R: 17.90
- target(s): 4150.00
- exit: TARGET net 288/179 (≈1.6089)R

#### `GV-P14-V01-M15m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · M15
*Mirror of `GV-P14-V01-M15` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> M15 is NOT in {H1,H4,D1,W1,MN1}: the BASE pattern still forms but the source variant records SKIPPED_TF_NOT_ALLOWED and no trade.

Tags: variant, tf-gate, tf-M15
Context: atr=4 · trend=UP · swings=L4150.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-16 10:30:02 4178.80/4179.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

#### `GV-P14-V01-M1m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · M1
*Mirror of `GV-P14-V01-M1` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> M1 is NOT in {H1,H4,D1,W1,MN1}: the BASE pattern still forms but the source variant records SKIPPED_TF_NOT_ALLOWED and no trade.

Tags: variant, tf-gate, tf-M1
Context: atr=4 · trend=UP · swings=L4150.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:01 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-16 10:02:02 4178.80/4179.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

#### `GV-P14-V01-M30m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · M30
*Mirror of `GV-P14-V01-M30` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> M30 is NOT in {H1,H4,D1,W1,MN1}: the BASE pattern still forms but the source variant records SKIPPED_TF_NOT_ALLOWED and no trade.

Tags: variant, tf-gate, tf-M30
Context: atr=4 · trend=UP · swings=L4150.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:30 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-16 11:00:02 4178.80/4179.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

#### `GV-P14-V01-M5m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · M5
*Mirror of `GV-P14-V01-M5` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> M5 is NOT in {H1,H4,D1,W1,MN1}: the BASE pattern still forms but the source variant records SKIPPED_TF_NOT_ALLOWED and no trade.

Tags: variant, tf-gate, tf-M5
Context: atr=4 · trend=UP · swings=L4150.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:05 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-16 10:10:02 4178.80/4179.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

#### `GV-P14-V01-MN1m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · MN1
*Mirror of `GV-P14-V01-MN1` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> MN1 is an allowed timeframe for the source Kicker. Stop = C1's low - 0.20 = 4203.30 (not C2's, unlike the baseline); entry ask 4221.20; R 17.90; T_SWING(1.5) = swing high 4250.00 (1.61R) -> trade. Signal at the scheduled closure start, entry after the closure (entry_across_break).

Tags: variant, tf-gate, tf-MN1
Context: atr=4 · trend=UP · swings=L4150.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 06-30 23:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 08-02 23:00 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 08-31 23:00:02 4178.80/4179.00; 08-31 23:01:42 4149.80/4150.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-08-31T22:00:00Z
- entry: 4178.80
- stop: 4196.70
- R: 17.90
- target(s): 4150.00
- exit: TARGET net 288/179 (≈1.6089)R

#### `GV-P14-V01-W1m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · W1
*Mirror of `GV-P14-V01-W1` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> W1 is an allowed timeframe for the source Kicker. Stop = C1's low - 0.20 = 4203.30 (not C2's, unlike the baseline); entry ask 4221.20; R 17.90; T_SWING(1.5) = swing high 4250.00 (1.61R) -> trade. Signal at the scheduled closure start, entry after the closure (entry_across_break).

Tags: variant, tf-gate, tf-W1
Context: atr=4 · trend=UP · swings=L4150.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 08-30 23:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-06 23:00 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-13 23:00:02 4178.80/4179.00; 09-13 23:01:42 4149.80/4150.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-11T22:00:00Z
- entry: 4178.80
- stop: 4196.70
- R: 17.90
- target(s): 4150.00
- exit: TARGET net 288/179 (≈1.6089)R

#### `GV-P14-V02m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · H1
*Mirror of `GV-P14-V02` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Swing exactly 1.5R (4221.20 + 1.5*17.90 = 4248.05): accepted.

Tags: T_SWING, boundary
Context: atr=4 · trend=UP · swings=L4151.95

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 11:00 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-16 12:00:02 4178.80/4179.00; 09-16 12:01:40 4151.75/4151.95

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4178.80
- stop: 4196.70
- R: 17.90
- target(s): 4151.95
- exit: TARGET net 1.50R

#### `GV-P14-V03m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · H1
*Mirror of `GV-P14-V03` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Swing 4248.04: 26.84/17.90 = 1.4994R -> SKIPPED_SRC_RR.

Tags: T_SWING, boundary, insufficient-rr
Context: atr=4 · trend=UP · swings=L4151.96

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 11:00 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-16 12:00:02 4178.80/4179.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4178.80
- stop: 4196.70
- R: 17.90

#### `GV-P14-V04m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · H1
*Mirror of `GV-P14-V04` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> No confirmed swing at all -> SKIPPED_SRC_NO_TARGET.

Tags: T_SWING, no-target
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 11:00 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-16 12:00:02 4178.80/4179.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4178.80
- stop: 4196.70
- R: 17.90

#### `GV-P14-V05m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · H1
*Mirror of `GV-P14-V05` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Only a swing HIGH below the entry and a swing LOW above it: for a BUY only swing highs above the entry count -> NO_TARGET.

Tags: T_SWING, no-target
Context: atr=4 · trend=UP · swings=L4200.00, H4140.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 11:00 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-16 12:00:02 4178.80/4179.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4178.80
- stop: 4196.70
- R: 17.90

#### `GV-P14-V06m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · H1
*Mirror of `GV-P14-V06` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Nearest swing high (4230.00 = 0.49R) fails; the farther one (4260.00) would pass but is NOT used (nearest-only) -> SKIPPED_SRC_RR.

Tags: T_SWING, nearest-only
Context: atr=4 · trend=UP · swings=L4170.00, L4140.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 11:00 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-16 12:00:02 4178.80/4179.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4178.80
- stop: 4196.70
- R: 17.90

#### `GV-P14-V07m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · H1
*Mirror of `GV-P14-V07` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Swing high exactly AT the entry price is not beyond it -> NO_TARGET.

Tags: T_SWING, target-validity, boundary
Context: atr=4 · trend=UP · swings=L4178.80

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 11:00 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-16 12:00:02 4178.80/4179.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4178.80
- stop: 4196.70
- R: 17.90

#### `GV-P14-V08m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · H1
*Mirror of `GV-P14-V08` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Stopped at 4203.30.

Tags: variant, sl-first-ticks
Context: atr=4 · trend=UP · swings=L4150.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 11:00 | 4190.00 | 4196.60 | 4178.80 | 4179.00 |

Ticks (bid/ask): 09-16 12:00:02 4178.80/4179.00; 09-16 12:01:40 4196.50/4196.70

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4178.80
- stop: 4196.70
- R: 17.90
- target(s): 4150.00
- exit: STOP net -1.00R

#### `GV-P14-V09m` · `GT-KICKER-BEAR-v1.0/SRC-PS-COMPLETED` · H1
*Mirror of `GV-P14-V09` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Ordinary kicker (C2 low above C1 low): source stop and baseline stop coincide here (C1's low 4203.50 - 0.20).

Tags: variant
Context: atr=4 · trend=UP · swings=L4150.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 11:00 | 4189.00 | 4189.50 | 4182.00 | 4182.20 |

Ticks (bid/ask): 09-16 12:00:02 4182.00/4182.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4182.00
- stop: 4196.70

## `GT-KICKER-BULL-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4210.00/4210.50/4203.50/4204.00 ; 4210.00/4217.50/4209.80/4217.40 | DOWN | 4 | shape ✔ · formed ✔ | — | O2 exactly O1 (4210.00): C2's body touches C1's body top but does not overlap -> passes. |
| `B02` | 4210.00/4210.50/4203.50/4204.00 ; 4209.99/4217.50/4209.80/4217.40 | DOWN | 4 | no shape | O2>=O1 | O2 = O1 - 0.01: only O2>=O1 fails. |
| `B03` | 4210.00/4210.50/4203.50/4204.00 ; 4211.00/4218.00/4210.50/4217.25 | DOWN | 4 | shape ✔ · formed ✔ | — | Close exactly at H2 - 0.10*R2 (R2=7.50: 4217.25): passes. |
| `B04` | 4210.00/4210.50/4203.50/4204.00 ; 4211.00/4218.00/4210.50/4217.24 | DOWN | 4 | no shape | C2>=H2-0.10R2 | Close 0.01 lower: only the close-near-high clause fails. |
| `B05` | 4210.00/4210.50/4203.50/4204.00 ; 4211.00/4213.10/4210.90/4213.00 | DOWN | 4 | no shape | LARGE(K2) | C2 is not LARGE (B=2.0, R=2.2): fails LARGE(C2) only. |
| `B06` | 4206.00/4206.30/4203.80/4204.00 ; 4207.00/4214.00/4206.50/4213.80 | DOWN | 4 | no shape | LARGE(K1) | C1 is not LARGE (small bearish candle, B=2.0, R=2.5): fails LARGE(C1) only. |
| `F01` | 4210.00/4210.50/4203.50/4204.00 ; 4210.20/4218.00/4210.00/4217.90 | DOWN | 4 | shape ✔ · formed ✔ | — | gap_thr 0.20: O2 = O1 + 0.20 exactly -> bull_gap_flag true. |
| `F02` | 4210.00/4210.50/4203.50/4204.00 ; 4210.19/4218.00/4210.00/4217.90 | DOWN | 4 | shape ✔ · formed ✔ | — | O2 = O1 + 0.19: flag false; pattern still forms. |
| `N01` | 4210.00/4210.50/4203.50/4204.00 ; 4217.00/4218.00/4210.50/4211.00 | DOWN | 4 | no shape | K2 bull, C2>=H2-0.10R2 | C2 bearish (opens 4217, closes 4211): fails colour and the close-near-high test. |
| `NZ1` | 4200.00/4204.50/4199.50/4204.00 ; 4204.00/4208.50/4203.50/4208.00 | DOWN | 4 | canonical: no event; variant: no event | — | Two bullish candles: no bearish LARGE C1. |
| `T01` | 4210.00/4210.50/4203.50/4204.00 ; 4211.00/4218.00/4210.50/4217.80 | UP | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Kicker shape after UP: not formed (bullish kicker needs DOWN). |
| `T02` | 4210.00/4210.50/4203.50/4204.00 ; 4211.00/4218.00/4210.50/4217.80 | RANGE | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Kicker shape after RANGE: not formed (bullish kicker needs DOWN). |
| `T03` | 4210.00/4210.50/4203.50/4204.00 ; 4211.00/4218.00/4210.50/4217.80 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Kicker shape after UNDETERMINED: not formed (bullish kicker needs DOWN). |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:30:02 4217.80/4218.00; 09-16 10:32:00 4225.15/4225.35; 09-16 10:35:00 4247.40/4247.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4218.00; stop: 4203.30; R: 14.70; target(s): 4247.40; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:30:02 4217.80/4218.00; 09-16 10:32:00 4210.45/4210.65; 09-16 10:35:00 4203.30/4203.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4218.00; stop: 4203.30; R: 14.70; target(s): 4247.40; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4201.30 < stop): fill = that tick's bid, not the stop (G9): -167/147R. | 09-16 10:30:02 4217.80/4218.00; 09-16 10:32:00 4201.30/4201.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4218.00; stop: 4203.30; R: 14.70; target(s): 4247.40; exit: STOP net -167/147 (≈-1.1361)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:30:02 4217.80/4218.00; 09-16 10:31:40 4203.30/4203.50; 09-16 10:33:20 4247.40/4247.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4218.00; stop: 4203.30; R: 14.70; target(s): 4247.40; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:30:02 4217.80/4218.00; 09-16 10:31:40 4247.40/4247.60; 09-16 10:33:20 4203.30/4203.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4218.00; stop: 4203.30; R: 14.70; target(s): 4247.40; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:30:02 4217.80/4218.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4218.00; stop: 4203.30; R: 14.70; target(s): 4247.40; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:30:02 4217.80/4218.30; 09-16 10:33:20 4248.30/4248.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; spread_at_entry: 0.50; entry: 4218.30; stop: 4203.30; R: 15.00; target(s): 4248.30; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:45:00 4217.80/4218.00; 09-16 10:46:40 4247.40/4247.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4218.00; stop: 4203.30; R: 14.70; target(s): 4247.40; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:45:01 4217.80/4218.00; 09-16 10:46:40 4247.40/4247.60 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:30:02 4204.80/4205.30; 09-16 10:31:40 4209.30/4209.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4205.30; R: 2.00; target(s): 4209.30; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:30:02 4204.79/4205.29; 09-16 10:31:40 4209.29/4209.79 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4253.80 > target 4247.40): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:30:02 4217.80/4218.00; 09-16 10:32:00 4253.80/4254.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4218.00; stop: 4203.30; R: 14.70; target(s): 4247.40; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4217.80/4218.00; 09-21 00:30:00 4247.40/4247.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4218.00; stop: 4203.30; R: 14.70; target(s): 4247.40; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4217.80/4218.00; 09-21 00:30:00 4247.40/4247.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4218.00; stop: 4203.30; R: 14.70; target(s): 4247.40; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4217.80/4218.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P14-R01` · `GT-KICKER-BULL-v1.0/BASE` · M15
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4211.00 | 4218.00 | 4210.50 | 4217.80 |
| 3 | 09-16 10:30 | 4217.80 | 4220.80 | 4215.80 | 4218.80 |
| 4 | 09-16 10:45 | 4218.80 | 4221.80 | 4216.80 | 4219.80 |
| 5 | 09-16 11:00 | 4219.80 | 4220.80 | 4214.80 | 4216.80 |
| 6 | 09-16 11:15 | 4216.80 | 4219.80 | 4213.80 | 4217.80 |
| 7 | 09-16 11:30 | 4218.80 | 4222.80 | 4215.80 | 4220.80 |
| 8 | 09-16 11:45 | 4220.80 | 4226.80 | 4208.80 | 4221.80 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4217.80 | h1: ret=1.00, mfe=3.00, mae=2.00, end_index=2 | h3: ret=-1.00, mfe=4.00, mae=3.00, end_index=4 | h5: ret=3.00, mfe=5.00, mae=4.00, end_index=6 | h10: NULL | h20: NULL

#### `GV-P14-V00` · `GT-KICKER-BULL-v1.0/BASE` · H1
> BASE on the same bars: stop = min(L1,L2) - 0.20; L2 (4203.40) is below L1 (4203.50), so the stop is 4203.20. Compare V01-H1: the source variant stops beyond C1's low only (4203.30).

Tags: base-vs-source
Context: atr=4 · trend=DOWN · swings=H4250.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 11:00 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-16 12:00:02 4221.00/4221.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4221.20
- stop: 4203.20
- R: 18.00
- target(s): 4257.20

#### `GV-P14-Y01` · `GT-KICKER-BULL-v1.0/BASE` · M15
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4211.00 | 4218.00 | 4210.50 | 4217.80 |

Ticks (bid/ask): 09-16 10:30:02 4217.80/4218.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4218.00
- stop: 4203.30
- R: 14.70
- target(s): 4247.40

### Variant `SRC-PS-COMPLETED`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `QF1` | 4210.00/4210.50/4203.50/4204.00 ; 4210.00/4221.20/4203.40/4221.00 | UP | 4 | canonical: SHAPE_DETECTED; variant: no event; disposition: NOT_QUALIFIED; qualification_failures: TF_NOT_ALLOWED, PRIOR_STATE | — | Source Kicker on M15 (not allowed) after an UPTREND (prior state fails): both failures kept. |

#### `GV-P14-V01-D1` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · D1
> D1 is an allowed timeframe for the source Kicker. Stop = C1's low - 0.20 = 4203.30 (not C2's, unlike the baseline); entry ask 4221.20; R 17.90; T_SWING(1.5) = swing high 4250.00 (1.61R) -> trade. Signal at the scheduled closure start, entry after the closure (entry_across_break).

Tags: variant, tf-gate, tf-D1
Context: atr=4 · trend=DOWN · swings=H4250.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-13 23:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-14 23:00 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-15 23:00:02 4221.00/4221.20; 09-15 23:01:42 4250.00/4250.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-15T22:00:00Z
- entry: 4221.20
- stop: 4203.30
- R: 17.90
- target(s): 4250.00
- exit: TARGET net 288/179 (≈1.6089)R

#### `GV-P14-V01-H1` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · H1
> H1 is an allowed timeframe for the source Kicker. Stop = C1's low - 0.20 = 4203.30 (not C2's, unlike the baseline); entry ask 4221.20; R 17.90; T_SWING(1.5) = swing high 4250.00 (1.61R) -> trade.

Tags: variant, tf-gate, tf-H1
Context: atr=4 · trend=DOWN · swings=H4250.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 11:00 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-16 12:00:02 4221.00/4221.20; 09-16 12:01:40 4250.00/4250.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T12:00:00Z
- entry: 4221.20
- stop: 4203.30
- R: 17.90
- target(s): 4250.00
- exit: TARGET net 288/179 (≈1.6089)R

#### `GV-P14-V01-H4` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · H4
> H4 is an allowed timeframe for the source Kicker. Stop = C1's low - 0.20 = 4203.30 (not C2's, unlike the baseline); entry ask 4221.20; R 17.90; T_SWING(1.5) = swing high 4250.00 (1.61R) -> trade. Signal at the scheduled closure start, entry after the closure (entry_across_break).

Tags: variant, tf-gate, tf-H4
Context: atr=4 · trend=DOWN · swings=H4250.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 11:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 15:00 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-16 19:00:02 4221.00/4221.20; 09-16 19:01:42 4250.00/4250.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T19:00:00Z
- entry: 4221.20
- stop: 4203.30
- R: 17.90
- target(s): 4250.00
- exit: TARGET net 288/179 (≈1.6089)R

#### `GV-P14-V01-M1` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · M1
> M1 is NOT in {H1,H4,D1,W1,MN1}: the BASE pattern still forms but the source variant records SKIPPED_TF_NOT_ALLOWED and no trade.

Tags: variant, tf-gate, tf-M1
Context: atr=4 · trend=DOWN · swings=H4250.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:01 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-16 10:02:02 4221.00/4221.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

#### `GV-P14-V01-M15` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · M15
> M15 is NOT in {H1,H4,D1,W1,MN1}: the BASE pattern still forms but the source variant records SKIPPED_TF_NOT_ALLOWED and no trade.

Tags: variant, tf-gate, tf-M15
Context: atr=4 · trend=DOWN · swings=H4250.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-16 10:30:02 4221.00/4221.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

#### `GV-P14-V01-M30` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · M30
> M30 is NOT in {H1,H4,D1,W1,MN1}: the BASE pattern still forms but the source variant records SKIPPED_TF_NOT_ALLOWED and no trade.

Tags: variant, tf-gate, tf-M30
Context: atr=4 · trend=DOWN · swings=H4250.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:30 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-16 11:00:02 4221.00/4221.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

#### `GV-P14-V01-M5` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · M5
> M5 is NOT in {H1,H4,D1,W1,MN1}: the BASE pattern still forms but the source variant records SKIPPED_TF_NOT_ALLOWED and no trade.

Tags: variant, tf-gate, tf-M5
Context: atr=4 · trend=DOWN · swings=H4250.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:05 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-16 10:10:02 4221.00/4221.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

#### `GV-P14-V01-MN1` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · MN1
> MN1 is an allowed timeframe for the source Kicker. Stop = C1's low - 0.20 = 4203.30 (not C2's, unlike the baseline); entry ask 4221.20; R 17.90; T_SWING(1.5) = swing high 4250.00 (1.61R) -> trade. Signal at the scheduled closure start, entry after the closure (entry_across_break).

Tags: variant, tf-gate, tf-MN1
Context: atr=4 · trend=DOWN · swings=H4250.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 06-30 23:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 08-02 23:00 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 08-31 23:00:02 4221.00/4221.20; 08-31 23:01:42 4250.00/4250.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-08-31T22:00:00Z
- entry: 4221.20
- stop: 4203.30
- R: 17.90
- target(s): 4250.00
- exit: TARGET net 288/179 (≈1.6089)R

#### `GV-P14-V01-W1` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · W1
> W1 is an allowed timeframe for the source Kicker. Stop = C1's low - 0.20 = 4203.30 (not C2's, unlike the baseline); entry ask 4221.20; R 17.90; T_SWING(1.5) = swing high 4250.00 (1.61R) -> trade. Signal at the scheduled closure start, entry after the closure (entry_across_break).

Tags: variant, tf-gate, tf-W1
Context: atr=4 · trend=DOWN · swings=H4250.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 08-30 23:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-06 23:00 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-13 23:00:02 4221.00/4221.20; 09-13 23:01:42 4250.00/4250.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-11T22:00:00Z
- entry: 4221.20
- stop: 4203.30
- R: 17.90
- target(s): 4250.00
- exit: TARGET net 288/179 (≈1.6089)R

#### `GV-P14-V02` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · H1
> Swing exactly 1.5R (4221.20 + 1.5*17.90 = 4248.05): accepted.

Tags: T_SWING, boundary
Context: atr=4 · trend=DOWN · swings=H4248.05

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 11:00 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-16 12:00:02 4221.00/4221.20; 09-16 12:01:40 4248.05/4248.25

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4221.20
- stop: 4203.30
- R: 17.90
- target(s): 4248.05
- exit: TARGET net 1.50R

#### `GV-P14-V03` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · H1
> Swing 4248.04: 26.84/17.90 = 1.4994R -> SKIPPED_SRC_RR.

Tags: T_SWING, boundary, insufficient-rr
Context: atr=4 · trend=DOWN · swings=H4248.04

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 11:00 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-16 12:00:02 4221.00/4221.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4221.20
- stop: 4203.30
- R: 17.90

#### `GV-P14-V04` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · H1
> No confirmed swing at all -> SKIPPED_SRC_NO_TARGET.

Tags: T_SWING, no-target
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 11:00 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-16 12:00:02 4221.00/4221.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4221.20
- stop: 4203.30
- R: 17.90

#### `GV-P14-V05` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · H1
> Only a swing HIGH below the entry and a swing LOW above it: for a BUY only swing highs above the entry count -> NO_TARGET.

Tags: T_SWING, no-target
Context: atr=4 · trend=DOWN · swings=H4200.00, L4260.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 11:00 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-16 12:00:02 4221.00/4221.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4221.20
- stop: 4203.30
- R: 17.90

#### `GV-P14-V06` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · H1
> Nearest swing high (4230.00 = 0.49R) fails; the farther one (4260.00) would pass but is NOT used (nearest-only) -> SKIPPED_SRC_RR.

Tags: T_SWING, nearest-only
Context: atr=4 · trend=DOWN · swings=H4230.00, H4260.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 11:00 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-16 12:00:02 4221.00/4221.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4221.20
- stop: 4203.30
- R: 17.90

#### `GV-P14-V07` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · H1
> Swing high exactly AT the entry price is not beyond it -> NO_TARGET.

Tags: T_SWING, target-validity, boundary
Context: atr=4 · trend=DOWN · swings=H4221.20

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 11:00 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-16 12:00:02 4221.00/4221.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4221.20
- stop: 4203.30
- R: 17.90

#### `GV-P14-V08` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · H1
> Stopped at 4203.30.

Tags: variant, sl-first-ticks
Context: atr=4 · trend=DOWN · swings=H4250.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 11:00 | 4210.00 | 4221.20 | 4203.40 | 4221.00 |

Ticks (bid/ask): 09-16 12:00:02 4221.00/4221.20; 09-16 12:01:40 4203.30/4203.50

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4221.20
- stop: 4203.30
- R: 17.90
- target(s): 4250.00
- exit: STOP net -1.00R

#### `GV-P14-V09` · `GT-KICKER-BULL-v1.0/SRC-PS-COMPLETED` · H1
> Ordinary kicker (C2 low above C1 low): source stop and baseline stop coincide here (C1's low 4203.50 - 0.20).

Tags: variant
Context: atr=4 · trend=DOWN · swings=H4250.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 11:00 | 4211.00 | 4218.00 | 4210.50 | 4217.80 |

Ticks (bid/ask): 09-16 12:00:02 4217.80/4218.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4218.00
- stop: 4203.30

