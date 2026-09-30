# P18 Three Black Crows — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.3.1 · vector pack GV-0.2 · **49 vectors** (49 firm)

Strategies covered: `GT-3BLACKCROWS-BEAR-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-3BLACKCROWS-BEAR-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4200.00/4200.20/4198.20/4198.40 ; 4199.20/4199.40/4196.00/4196.20 ; 4198.00/4198.20/4194.80/4195.00 | UP | 4 | shape ✔ · formed ✔ | — | Bar 1 body exactly 0.40*ATR = 1.60 (R 2.00): passes. |
| `B02` | 4200.00/4200.20/4198.21/4198.41 ; 4199.20/4199.40/4196.00/4196.20 ; 4198.00/4198.20/4194.80/4195.00 | UP | 4 | no shape | (1 clause) | Bar 1 body 1.59: fails only bar1 B>=0.40ATR. |
| `B03` | 4200.00/4200.20/4196.80/4197.00 ; 4198.00/4199.00/4194.00/4195.00 ; 4196.00/4196.20/4192.80/4193.00 | UP | 4 | shape ✔ · formed ✔ | — | Bar 2 body exactly 0.60*R (B 3.0, R 5.0: UW 1.0, LW 1.0): passes. |
| `B04` | 4200.00/4200.20/4196.80/4197.00 ; 4198.00/4199.00/4193.99/4195.00 ; 4196.00/4196.20/4192.80/4193.00 | UP | 4 | no shape | (1 clause) | Bar 2 R = 5.01 (B/R = 0.5988): fails only bar2 B>=0.60R. |
| `B05` | 4200.00/4200.20/4195.80/4196.00 ; 4198.00/4198.00/4190.00/4192.00 ; 4194.00/4194.20/4188.80/4189.00 | UP | 4 | shape ✔ · formed ✔ | — | Bar 2 upper wick exactly 0.25*R (B 6, UW 2.0, LW 0, R 8): passes. |
| `B06` | 4200.00/4200.20/4195.80/4196.00 ; 4198.00/4198.00/4189.99/4192.00 ; 4194.00/4194.20/4188.80/4189.00 | UP | 4 | no shape | (1 clause) | Bar 2 upper wick 2.01 (R 8.01; limit 2.0025): fails only bar2 UW<=0.25R. |
| `B07` | 4200.00/4200.20/4195.80/4196.00 ; 4200.00/4200.20/4193.80/4194.00 ; 4196.00/4196.20/4190.80/4191.00 | UP | 4 | shape ✔ · formed ✔ | — | Bar 2 opens exactly at bar 1's open (4200.00): inside body 1: passes. |
| `B08` | 4200.00/4200.20/4195.80/4196.00 ; 4200.01/4200.21/4193.80/4194.00 ; 4196.00/4196.20/4190.80/4191.00 | UP | 4 | no shape | (1 clause) | Bar 2 opens 0.01 below bar 1's open: fails only open2 in body1. |
| `B09` | 4200.00/4200.20/4195.80/4196.00 ; 4196.00/4196.20/4189.80/4190.00 ; 4192.00/4192.20/4186.80/4187.00 | UP | 4 | shape ✔ · formed ✔ | — | Bar 2 opens exactly at bar 1's close (4204.00): passes. |
| `B10` | 4200.00/4200.20/4195.80/4196.00 ; 4195.99/4196.19/4189.79/4189.99 ; 4192.00/4192.20/4186.80/4187.00 | UP | 4 | no shape | (1 clause) | Bar 2 opens 0.01 above bar 1's close: fails only open2 in body1. |
| `B11` | 4200.00/4200.20/4196.80/4197.00 ; 4199.00/4199.20/4196.80/4197.00 ; 4198.00/4198.20/4194.80/4195.00 | UP | 4 | no shape | (1 clause) | Bar 2 closes exactly at bar 1's close: fails only C2>C1 (strict). |
| `B12` | 4200.00/4200.20/4196.80/4197.00 ; 4199.00/4199.20/4196.79/4196.99 ; 4198.00/4198.20/4194.80/4195.00 | UP | 4 | shape ✔ · formed ✔ | — | Bar 2 closes 0.01 above bar 1's close: passes. |
| `B13` | 4200.00/4200.20/4195.80/4196.00 ; 4198.00/4198.20/4189.80/4190.00 ; 4193.00/4193.20/4187.80/4188.00 | UP | 4 | shape ✔ · formed ✔ | — | Largest body exactly 2x the smallest (4.0 vs 8.0): passes. |
| `B14` | 4200.00/4200.20/4195.80/4196.00 ; 4198.00/4198.20/4189.79/4189.99 ; 4193.00/4193.20/4187.80/4188.00 | UP | 4 | no shape | (1 clause) | Largest body 8.01 vs smallest 4.0: fails only the similarity clause. |
| `N01` | 4200.00/4200.20/4195.80/4196.00 ; 4198.00/4198.20/4191.80/4192.00 ; 4192.00/4197.00/4191.80/4196.80 | UP | 4 | no shape | (2 clause) | Bar 3 is bearish: fails colour, C3>C2 and its own body-position clauses. |
| `NZ1` | 4200.00/4200.50/4195.50/4196.00 ; 4196.00/4200.50/4195.50/4200.00 ; 4200.00/4200.50/4195.50/4196.00 | UP | 4 | canonical: no event; variant: no event | — | Bull, bear, bull: colours break the soldiers. |
| `T01` | 4200.00/4200.20/4195.80/4196.00 ; 4198.00/4198.20/4191.80/4192.00 ; 4194.00/4194.20/4188.80/4189.00 | DOWN | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Three White Soldiers: no prior-state requirement in the canonical rule (trend UP recorded as context). |
| `T02` | 4200.00/4200.20/4195.80/4196.00 ; 4198.00/4198.20/4191.80/4192.00 ; 4194.00/4194.20/4188.80/4189.00 | RANGE | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Three White Soldiers: no prior-state requirement in the canonical rule (trend RANGE recorded as context). |
| `T03` | 4200.00/4200.20/4195.80/4196.00 ; 4198.00/4198.20/4191.80/4192.00 ; 4194.00/4194.20/4188.80/4189.00 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Three White Soldiers: no prior-state requirement in the canonical rule (trend UNDETERMINED recorded as context). |
| `T04` | 4200.00/4200.20/4195.80/4196.00 ; 4198.00/4198.20/4191.80/4192.00 ; 4194.00/4194.20/4188.80/4189.00 | UP | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Three White Soldiers: no prior-state requirement in the canonical rule (trend DOWN recorded as context). |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:45:02 4188.80/4189.00; 09-16 10:47:00 4183.00/4183.20; 09-16 10:50:00 4165.40/4165.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4200.40; R: 11.60; target(s): 4165.60; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:45:02 4188.80/4189.00; 09-16 10:47:00 4194.60/4194.80; 09-16 10:50:00 4200.20/4200.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4200.40; R: 11.60; target(s): 4165.60; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4197.60 < stop): fill = that tick's bid, not the stop (G9): -34/29R. | 09-16 10:45:02 4188.80/4189.00; 09-16 10:47:00 4202.20/4202.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4200.40; R: 11.60; target(s): 4165.60; exit: STOP net -34/29 (≈-1.1724)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:45:02 4188.80/4189.00; 09-16 10:46:40 4200.20/4200.40; 09-16 10:48:20 4165.40/4165.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4200.40; R: 11.60; target(s): 4165.60; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:45:02 4188.80/4189.00; 09-16 10:46:40 4165.40/4165.60; 09-16 10:48:20 4200.20/4200.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4200.40; R: 11.60; target(s): 4165.60; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:45:02 4188.80/4189.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4200.40; R: 11.60; target(s): 4165.60; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:45:02 4188.50/4189.00; 09-16 10:48:20 4164.20/4164.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; spread_at_entry: 0.50; entry: 4188.50; stop: 4200.40; R: 11.90; target(s): 4164.70; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 11:00:00 4188.80/4189.00; 09-16 11:01:40 4165.40/4165.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4200.40; R: 11.60; target(s): 4165.60; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 11:00:01 4188.80/4189.00; 09-16 11:01:40 4165.40/4165.60 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:45:02 4198.40/4198.90; 09-16 10:46:40 4193.90/4194.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4198.40; R: 2.00; target(s): 4194.40; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:45:02 4198.41/4198.91; 09-16 10:46:40 4193.91/4194.41 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4240.80 > target 4234.40): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:45:02 4188.80/4189.00; 09-16 10:47:00 4159.00/4159.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4200.40; R: 11.60; target(s): 4165.60; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4188.80/4189.00; 09-21 00:30:00 4165.40/4165.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4188.80; stop: 4200.40; R: 11.60; target(s): 4165.60; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4188.80/4189.00; 09-21 00:30:00 4165.40/4165.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4188.80; stop: 4200.40; R: 11.60; target(s): 4165.60; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4188.80/4189.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P18-R01` · `GT-3BLACKCROWS-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P17-R01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.20 | 4195.80 | 4196.00 |
| 2 | 09-16 10:15 | 4198.00 | 4198.20 | 4191.80 | 4192.00 |
| 3 | 09-16 10:30 | 4194.00 | 4194.20 | 4188.80 | 4189.00 |
| 4 | 09-16 10:45 | 4189.00 | 4191.00 | 4186.00 | 4188.00 |
| 5 | 09-16 11:00 | 4188.00 | 4190.00 | 4185.00 | 4187.00 |
| 6 | 09-16 11:15 | 4187.00 | 4192.00 | 4186.00 | 4190.00 |
| 7 | 09-16 11:30 | 4190.00 | 4193.00 | 4187.00 | 4189.00 |
| 8 | 09-16 11:45 | 4188.00 | 4191.00 | 4184.00 | 4186.00 |
| 9 | 09-16 12:00 | 4186.00 | 4198.00 | 4180.00 | 4185.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4189.00 | h1: ret=1.00, mfe=3.00, mae=2.00, end_index=3 | h3: ret=-1.00, mfe=4.00, mae=3.00, end_index=5 | h5: ret=3.00, mfe=5.00, mae=4.00, end_index=7 | h10: NULL | h20: NULL

#### `GV-P18-Y01` · `GT-3BLACKCROWS-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P17-Y01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.20 | 4195.80 | 4196.00 |
| 2 | 09-16 10:15 | 4198.00 | 4198.20 | 4191.80 | 4192.00 |
| 3 | 09-16 10:30 | 4194.00 | 4194.20 | 4188.80 | 4189.00 |

Ticks (bid/ask): 09-16 10:45:02 4188.80/4189.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:45:00Z
- entry: 4188.80
- stop: 4200.40
- R: 11.60
- target(s): 4165.60

### Variant `SRC-PS`

#### `GV-P18-V01` · `GT-3BLACKCROWS-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P17-V01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> STOP_ENTRY: armed at 10:45 (bar 3 completes), buy-stop trigger = H3 = 4211.20, valid for the next three completed bars (to 11:30). A tick at 10:50 with ask 4211.10 does not trigger; at 11:10 ask = 4211.20 reaches the trigger exactly -> filled at that ASK. Stop L3-0.20 = 4205.60 (R 5.60); measured-move target 4222.60 (2.04R). signal_time = the trigger tick.

Tags: variant-clean-yes, stop-entry, trigger-exact
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.20 | 4195.80 | 4196.00 |
| 2 | 09-16 10:15 | 4198.00 | 4198.20 | 4191.80 | 4192.00 |
| 3 | 09-16 10:30 | 4194.00 | 4194.20 | 4188.80 | 4189.00 |

Ticks (bid/ask): 09-16 10:50:00 4188.90/4189.10; 09-16 11:10:00 4188.80/4189.00; 09-16 11:20:00 4177.20/4177.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4188.80
- signal time: 2026-09-16T11:10:00Z
- entry: 4188.80
- stop: 4194.40
- R: 5.60
- target(s): 4177.40
- exit: TARGET net 57/28 (≈2.0357)R

#### `GV-P18-V02` · `GT-3BLACKCROWS-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P17-V02` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Ask 4211.19 (one tick under the trigger): no fill.

Tags: stop-entry, trigger-boundary
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.20 | 4195.80 | 4196.00 |
| 2 | 09-16 10:15 | 4198.00 | 4198.20 | 4191.80 | 4192.00 |
| 3 | 09-16 10:30 | 4194.00 | 4194.20 | 4188.80 | 4189.00 |

Ticks (bid/ask): 09-16 11:10:00 4188.81/4189.01

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: EXPIRED
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4188.80

#### `GV-P18-V03` · `GT-3BLACKCROWS-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P17-V03` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Trigger reached only at 11:30:01, one second after the third bar completes: EXPIRED (no trade).

Tags: stop-entry, expiry
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.20 | 4195.80 | 4196.00 |
| 2 | 09-16 10:15 | 4198.00 | 4198.20 | 4191.80 | 4192.00 |
| 3 | 09-16 10:30 | 4194.00 | 4194.20 | 4188.80 | 4189.00 |

Ticks (bid/ask): 09-16 11:30:01 4188.60/4188.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: EXPIRED
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4188.80

#### `GV-P18-V04` · `GT-3BLACKCROWS-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P17-V04` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Trigger tick stamped exactly 11:30:00, the instant the third bar completes. Bars are half-open, so that tick belongs to the FOURTH bar (11:30-11:45): too late -> EXPIRED (ruling A-18: bar membership, not timestamp equality).

Tags: stop-entry, expiry, boundary
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.20 | 4195.80 | 4196.00 |
| 2 | 09-16 10:15 | 4198.00 | 4198.20 | 4191.80 | 4192.00 |
| 3 | 09-16 10:30 | 4194.00 | 4194.20 | 4188.80 | 4189.00 |

Ticks (bid/ask): 09-16 11:30:00 4188.60/4188.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: EXPIRED
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4188.80

#### `GV-P18-V04b` · `GT-3BLACKCROWS-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P17-V04b` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Trigger tick at 11:29:59, the last second of the third bar: it belongs to the window -> filled at the ask 4211.40 (bid 4211.20 + 0.20).

Tags: stop-entry, expiry, boundary
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.20 | 4195.80 | 4196.00 |
| 2 | 09-16 10:15 | 4198.00 | 4198.20 | 4191.80 | 4192.00 |
| 3 | 09-16 10:30 | 4194.00 | 4194.20 | 4188.80 | 4189.00 |

Ticks (bid/ask): 09-16 11:29:59 4188.60/4188.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4188.80
- signal time: 2026-09-16T11:29:59Z
- entry: 4188.60
- stop: 4194.40
- R: 5.80

#### `GV-P18-V05` · `GT-3BLACKCROWS-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P17-V05` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Price falls to the stop level (bid 4205.60) BEFORE the trigger: order cancelled, INVALIDATED_BEFORE_ENTRY. A later trigger tick does nothing.

Tags: stop-entry, invalidated
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.20 | 4195.80 | 4196.00 |
| 2 | 09-16 10:15 | 4198.00 | 4198.20 | 4191.80 | 4192.00 |
| 3 | 09-16 10:30 | 4194.00 | 4194.20 | 4188.80 | 4189.00 |

Ticks (bid/ask): 09-16 10:55:00 4194.20/4194.40; 09-16 11:10:00 4188.60/4188.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: INVALIDATED_BEFORE_ENTRY
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4188.80

#### `GV-P18-V06` · `GT-3BLACKCROWS-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P17-V06` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Bid 4205.61 (one tick above the stop level) does NOT cancel the order; the trigger later fills.

Tags: stop-entry, invalidated, boundary
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.20 | 4195.80 | 4196.00 |
| 2 | 09-16 10:15 | 4198.00 | 4198.20 | 4191.80 | 4192.00 |
| 3 | 09-16 10:30 | 4194.00 | 4194.20 | 4188.80 | 4189.00 |

Ticks (bid/ask): 09-16 10:55:00 4194.19/4194.39; 09-16 11:10:00 4188.60/4188.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4188.80
- signal time: 2026-09-16T11:10:00Z
- entry: 4188.60
- stop: 4194.40
- R: 5.80

#### `GV-P18-V07` · `GT-3BLACKCROWS-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P17-V07` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> A tick at 10:40 with ask 4211.50 is BEFORE the pattern completed (armed at 10:45): ignored. No later trigger -> EXPIRED.

Tags: stop-entry, before-arm
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.20 | 4195.80 | 4196.00 |
| 2 | 09-16 10:15 | 4198.00 | 4198.20 | 4191.80 | 4192.00 |
| 3 | 09-16 10:30 | 4194.00 | 4194.20 | 4188.80 | 4189.00 |

Ticks (bid/ask): 09-16 10:40:00 4188.50/4188.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: EXPIRED
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4188.80

#### `GV-P18-V08` · `GT-3BLACKCROWS-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P17-V08` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Gap: the first tick above the trigger is already at ask 4223.20, beyond the 4222.60 target: entered at 4223.20 would leave the target behind the entry -> SKIPPED_TARGET_ALREADY_PASSED.

Tags: stop-entry, target-already-passed
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.20 | 4195.80 | 4196.00 |
| 2 | 09-16 10:15 | 4198.00 | 4198.20 | 4191.80 | 4192.00 |
| 3 | 09-16 10:30 | 4194.00 | 4194.20 | 4188.80 | 4189.00 |

Ticks (bid/ask): 09-16 11:10:00 4176.80/4177.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_TARGET_ALREADY_PASSED
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4188.80
- signal time: 2026-09-16T11:10:00Z

#### `GV-P18-V09` · `GT-3BLACKCROWS-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P17-V09` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Buy-stop fills at the ASK even when it gaps above the trigger: ask 4212.20 -> entry 4212.20 (R 6.60), target 4222.60 (1.58R), stop hit later.

Tags: stop-entry, gap-above-trigger
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.20 | 4195.80 | 4196.00 |
| 2 | 09-16 10:15 | 4198.00 | 4198.20 | 4191.80 | 4192.00 |
| 3 | 09-16 10:30 | 4194.00 | 4194.20 | 4188.80 | 4189.00 |

Ticks (bid/ask): 09-16 11:10:00 4187.80/4188.00; 09-16 11:40:00 4194.20/4194.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- arm time: 2026-09-16T10:45:00Z
- expiry time: 2026-09-16T11:30:00Z
- trigger: 4188.80
- signal time: 2026-09-16T11:10:00Z
- entry: 4187.80
- stop: 4194.40
- R: 6.60
- target(s): 4177.40
- exit: STOP net -1.00R

#### `GV-P18-V10` · `GT-3BLACKCROWS-BEAR-v1.0/SRC-PS` · H1
*Mirror of `GV-P17-V10` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Weekend: the H1 pattern completes at the Friday 22:00 close (arm_time). The order lives through the next THREE completed bars after the reopening (Sun 23:00, Mon 00:00, Mon 01:00) -> expiry Mon 02:00. A trigger at Sun 23:30 fills.

Tags: stop-entry, weekend-entry
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 19:00 | 4200.00 | 4200.20 | 4195.80 | 4196.00 |
| 2 | 09-18 20:00 | 4198.00 | 4198.20 | 4191.80 | 4192.00 |
| 3 | 09-18 21:00 | 4194.00 | 4194.20 | 4188.80 | 4189.00 |

Ticks (bid/ask): 09-20 23:30:00 4188.60/4188.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- arm time: 2026-09-18T22:00:00Z
- expiry time: 2026-09-21T02:00:00Z
- trigger: 4188.80
- signal time: 2026-09-20T23:30:00Z
- entry: 4188.60
- stop: 4194.40
- R: 5.80

#### `GV-P18-V11` · `GT-3BLACKCROWS-BEAR-v1.0/SRC-PS` · H1
*Mirror of `GV-P17-V11` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Same weekend order, trigger tick at Mon 02:00:01 (after the third bar): EXPIRED.

Tags: stop-entry, weekend-entry, expiry
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 19:00 | 4200.00 | 4200.20 | 4195.80 | 4196.00 |
| 2 | 09-18 20:00 | 4198.00 | 4198.20 | 4191.80 | 4192.00 |
| 3 | 09-18 21:00 | 4194.00 | 4194.20 | 4188.80 | 4189.00 |

Ticks (bid/ask): 09-21 02:00:01 4188.60/4188.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: EXPIRED
- arm time: 2026-09-18T22:00:00Z
- expiry time: 2026-09-21T02:00:00Z
- trigger: 4188.80

