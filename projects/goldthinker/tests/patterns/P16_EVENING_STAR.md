# P16 Evening Star — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.3.2 · vector pack GV-0.2 · **43 vectors** (43 firm)

Strategies covered: `GT-EVENINGSTAR-BEAR-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-EVENINGSTAR-BEAR-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4190.00/4197.00/4189.50/4196.50 ; 4197.00/4198.00/4195.80/4196.00 ; 4195.50/4196.00/4190.50/4190.80 | UP | 4 | shape ✔ · formed ✔ | — | SMALL(C2): B exactly 1.00 (0.25*ATR), R 2.20: passes. |
| `B02` | 4190.00/4197.00/4189.50/4196.50 ; 4197.00/4198.00/4195.79/4195.99 ; 4195.50/4196.00/4190.50/4190.80 | UP | 4 | no shape | (1 clause) | SMALL(C2): B = 1.01: fails SMALL only. |
| `B03` | 4190.00/4197.00/4189.50/4196.50 ; 4197.00/4198.00/4195.60/4196.60 ; 4195.50/4196.00/4190.50/4190.80 | UP | 4 | shape ✔ · formed ✔ | — | SMALL(C2): R exactly 2.40 (0.60*ATR), B 0.40: passes. |
| `B04` | 4190.00/4197.00/4189.50/4196.50 ; 4197.00/4198.00/4195.59/4196.60 ; 4195.50/4196.00/4190.50/4190.80 | UP | 4 | no shape | (1 clause) | SMALL(C2): R = 2.41: fails SMALL only. |
| `B05` | 4190.00/4197.00/4189.50/4196.50 ; 4196.10/4197.00/4196.00/4196.05 ; 4195.50/4196.00/4190.50/4190.80 | UP | 4 | shape ✔ · formed ✔ | — | O2 exactly C1 + 0.10*ATR = 4203.90: passes. |
| `B06` | 4190.00/4197.00/4189.50/4196.50 ; 4196.09/4197.00/4196.00/4196.05 ; 4195.50/4196.00/4190.50/4190.80 | UP | 4 | no shape | (1 clause) | O2 = 4203.91: only the star-opening clause fails. |
| `B07` | 4190.00/4197.00/4189.50/4196.50 ; 4197.00/4198.00/4196.20/4196.60 ; 4196.20/4196.50/4193.00/4193.25 | UP | 4 | no shape | (1 clause) | C3 exactly at the C1 midpoint 4206.75: fails C3>mid1 (strict) only. |
| `B08` | 4190.00/4197.00/4189.50/4196.50 ; 4197.00/4198.00/4196.20/4196.60 ; 4196.20/4196.50/4193.00/4193.24 | UP | 4 | shape ✔ · formed ✔ | — | C3 = midpoint + 0.01: passes. |
| `B09` | 4190.00/4192.80/4189.60/4192.40 ; 4192.50/4193.00/4191.40/4191.54 ; 4192.00/4192.20/4187.00/4187.50 | UP | 4 | shape ✔ · formed ✔ | — | B2 exactly 0.40*B1 (B1=2.40 -> B2=0.96; C1 LARGE on both B and R boundaries): passes. |
| `B10` | 4190.00/4192.80/4189.60/4192.40 ; 4192.50/4193.00/4191.39/4191.53 ; 4192.00/4192.20/4187.00/4187.50 | UP | 4 | no shape | (1 clause) | B2 = 0.97 vs 0.4*2.40 = 0.96: only B2<=0.40B1 fails (SMALL still passes). |
| `F01` | 4190.00/4197.00/4189.50/4196.50 ; 4197.00/4198.00/4196.20/4196.60 ; 4195.50/4196.00/4190.50/4190.80 | UP | 4 | shape ✔ · formed ✔ | — | Star body top 4203.40 < C1 close 4203.50: star_gap true (flag only). |
| `N01` | 4190.00/4197.00/4189.50/4196.50 ; 4197.00/4198.00/4196.20/4196.60 ; 4196.50/4196.60/4195.40/4195.50 | UP | 4 | no shape | (2 clause) | C3 not LARGE (small bull): fails LARGE(C3) and the midpoint test. |
| `N02` | 4190.00/4197.00/4189.50/4196.50 ; 4197.00/4198.00/4196.20/4196.60 ; 4190.80/4196.00/4190.50/4195.50 | UP | 4 | no shape | (2 clause) | C3 bearish: fails colour. |
| `N03` | 4190.00/4197.00/4189.50/4196.50 ; 4197.00/4198.00/4192.00/4193.00 ; 4195.50/4196.00/4190.50/4190.80 | UP | 4 | no shape | (2 clause) | C2 is a LARGE candle, not a star: fails SMALL and B2<=0.40B1. |
| `NZ1` | 4200.00/4200.50/4195.50/4196.00 ; 4196.00/4196.50/4191.50/4192.00 ; 4192.00/4192.50/4187.50/4188.00 | UP | 4 | canonical: no event; variant: no event | — | Three bullish candles: no star, no bearish C1. |
| `T01` | 4190.00/4197.00/4189.50/4196.50 ; 4197.00/4198.00/4196.20/4196.60 ; 4195.50/4196.00/4190.50/4190.80 | DOWN | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Morning Star shape after UP: not formed. |
| `T02` | 4190.00/4197.00/4189.50/4196.50 ; 4197.00/4198.00/4196.20/4196.60 ; 4195.50/4196.00/4190.50/4190.80 | RANGE | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Morning Star shape after RANGE: not formed. |
| `T03` | 4190.00/4197.00/4189.50/4196.50 ; 4197.00/4198.00/4196.20/4196.60 ; 4195.50/4196.00/4190.50/4190.80 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Morning Star shape after UNDETERMINED: not formed. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:45:02 4190.60/4190.80; 09-16 10:47:00 4186.80/4187.00; 09-16 10:50:00 4175.20/4175.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.20; R: 7.60; target(s): 4175.40; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:45:02 4190.60/4190.80; 09-16 10:47:00 4194.40/4194.60; 09-16 10:50:00 4198.00/4198.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.20; R: 7.60; target(s): 4175.40; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4199.80 < stop): fill = that tick's bid, not the stop (G9): -24/19R. | 09-16 10:45:02 4190.60/4190.80; 09-16 10:47:00 4200.00/4200.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.20; R: 7.60; target(s): 4175.40; exit: STOP net -24/19 (≈-1.2632)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:45:02 4190.60/4190.80; 09-16 10:46:40 4198.00/4198.20; 09-16 10:48:20 4175.20/4175.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.20; R: 7.60; target(s): 4175.40; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:45:02 4190.60/4190.80; 09-16 10:46:40 4175.20/4175.40; 09-16 10:48:20 4198.00/4198.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.20; R: 7.60; target(s): 4175.40; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:45:02 4190.60/4190.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.20; R: 7.60; target(s): 4175.40; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:45:02 4190.30/4190.80; 09-16 10:48:20 4174.00/4174.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; spread_at_entry: 0.50; entry: 4190.30; stop: 4198.20; R: 7.90; target(s): 4174.50; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 11:00:00 4190.60/4190.80; 09-16 11:01:40 4175.20/4175.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.20; R: 7.60; target(s): 4175.40; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 11:00:01 4190.60/4190.80; 09-16 11:01:40 4175.20/4175.40 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:45:02 4196.20/4196.70; 09-16 10:46:40 4191.70/4192.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4196.20; R: 2.00; target(s): 4192.20; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:45:02 4196.21/4196.71; 09-16 10:46:40 4191.71/4192.21 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4231.00 > target 4224.60): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:45:02 4190.60/4190.80; 09-16 10:47:00 4168.80/4169.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.20; R: 7.60; target(s): 4175.40; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4190.60/4190.80; 09-21 00:30:00 4175.20/4175.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4190.60; stop: 4198.20; R: 7.60; target(s): 4175.40; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4190.60/4190.80; 09-21 00:30:00 4175.20/4175.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4190.60; stop: 4198.20; R: 7.60; target(s): 4175.40; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4190.60/4190.80 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P16-R01` · `GT-EVENINGSTAR-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P15-R01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.50 | 4196.50 |
| 2 | 09-16 10:15 | 4197.00 | 4198.00 | 4196.20 | 4196.60 |
| 3 | 09-16 10:30 | 4195.50 | 4196.00 | 4190.50 | 4190.80 |
| 4 | 09-16 10:45 | 4190.80 | 4192.80 | 4187.80 | 4189.80 |
| 5 | 09-16 11:00 | 4189.80 | 4191.80 | 4186.80 | 4188.80 |
| 6 | 09-16 11:15 | 4188.80 | 4193.80 | 4187.80 | 4191.80 |
| 7 | 09-16 11:30 | 4191.80 | 4194.80 | 4188.80 | 4190.80 |
| 8 | 09-16 11:45 | 4189.80 | 4192.80 | 4185.80 | 4187.80 |
| 9 | 09-16 12:00 | 4187.80 | 4199.80 | 4181.80 | 4186.80 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4190.80 | h1: ret=1.00, mfe=3.00, mae=2.00, end_index=3 | h3: ret=-1.00, mfe=4.00, mae=3.00, end_index=5 | h5: ret=3.00, mfe=5.00, mae=4.00, end_index=7 | h10: NULL | h20: NULL

#### `GV-P16-Y01` · `GT-EVENINGSTAR-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P15-Y01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.50 | 4196.50 |
| 2 | 09-16 10:15 | 4197.00 | 4198.00 | 4196.20 | 4196.60 |
| 3 | 09-16 10:30 | 4195.50 | 4196.00 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4190.60/4190.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:45:00Z
- entry: 4190.60
- stop: 4198.20
- R: 7.60
- target(s): 4175.40

### Variant `SRC-PS`

#### `GV-P16-Q01` · `GT-EVENINGSTAR-BEAR-v1.0/SRC-PS` · M15
> A-30 on a partial target: TP2 is the near edge (top) of the zone below TP1, 4184.004 off-grid; for a SHORT a structural target rounds toward the entry (up) -> 4184.01. Stop max(H1,H2)+0.20 = 4198.20.

Tags: quantisation, structural-target, partials, A-30
Context: atr=4 · trend=UP · zones_entry=[4183.00-4184.004]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.50 | 4196.50 |
| 2 | 09-16 10:15 | 4197.00 | 4198.00 | 4196.20 | 4196.60 |
| 3 | 09-16 10:30 | 4195.50 | 4196.00 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4190.80/4191.00; 09-16 10:46:40 4189.30/4189.50; 09-16 10:47:30 4183.81/4184.01

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4190.80
- stop: 4198.20
- R: 7.40
- target(s): 4189.50, 4184.01
- exit: TARGET net 437/925 (≈0.4724)R

#### `GV-P16-V01` · `GT-EVENINGSTAR-BEAR-v1.0/SRC-PS` · M15
> SRC-PS Evening Star: SELL at the bid 4190.80; stop = H2 + 0.20 = 4198.20; R 7.40; TP1 = L1 (4189.50) closes 60%; TP2 = near edge (top) of the nearest live zone below TP1 (4184.00) closes 40%: +0.5811R.

Tags: variant-clean-yes, partials
Context: atr=4 · trend=UP · zones_entry=[4183.00-4184.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.50 | 4196.50 |
| 2 | 09-16 10:15 | 4197.00 | 4198.00 | 4196.20 | 4196.60 |
| 3 | 09-16 10:30 | 4195.50 | 4196.00 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4190.80/4191.00; 09-16 10:46:40 4189.30/4189.50; 09-16 10:47:30 4183.80/4184.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4190.80
- stop: 4198.20
- R: 7.40
- target(s): 4189.50, 4184.00
- exit: TARGET net 35/74 (≈0.4730)R

#### `GV-P16-V02` · `GT-EVENINGSTAR-BEAR-v1.0/SRC-PS` · M15
> TP1 then the stop: -0.2946R.

Tags: partials, tp1-then-stop
Context: atr=4 · trend=UP · zones_entry=[4183.00-4184.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.50 | 4196.50 |
| 2 | 09-16 10:15 | 4197.00 | 4198.00 | 4196.20 | 4196.60 |
| 3 | 09-16 10:30 | 4195.50 | 4196.00 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4190.80/4191.00; 09-16 10:46:40 4189.30/4189.50; 09-16 10:47:30 4198.00/4198.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4190.80
- stop: 4198.20
- R: 7.40
- target(s): 4189.50, 4184.00
- exit: MIXED net -109/370 (≈-0.2946)R

#### `GV-P16-V03` · `GT-EVENINGSTAR-BEAR-v1.0/SRC-PS` · M15
> Stopped before TP1: -1.00R.

Tags: partials, sl-first-ticks
Context: atr=4 · trend=UP · zones_entry=[4183.00-4184.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.50 | 4196.50 |
| 2 | 09-16 10:15 | 4197.00 | 4198.00 | 4196.20 | 4196.60 |
| 3 | 09-16 10:30 | 4195.50 | 4196.00 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4190.80/4191.00; 09-16 10:46:40 4198.00/4198.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4190.80
- stop: 4198.20
- R: 7.40
- target(s): 4189.50, 4184.00
- exit: STOP net -1.00R

#### `GV-P16-V04` · `GT-EVENINGSTAR-BEAR-v1.0/SRC-PS` · M15
> Entry bid 4189.50 = TP1: not beyond the entry -> SKIPPED_TARGET_ALREADY_PASSED.

Tags: target-already-passed, boundary
Context: atr=4 · trend=UP · zones_entry=[4183.00-4184.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.50 | 4196.50 |
| 2 | 09-16 10:15 | 4197.00 | 4198.00 | 4196.20 | 4196.60 |
| 3 | 09-16 10:30 | 4195.50 | 4196.00 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4189.50/4189.70

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_TARGET_ALREADY_PASSED

#### `GV-P16-V05` · `GT-EVENINGSTAR-BEAR-v1.0/SRC-PS` · M15
> Entry bid 4189.51: TP1 is 0.01 beyond -> trade.

Tags: target-already-passed, boundary
Context: atr=4 · trend=UP · zones_entry=[4183.00-4184.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.50 | 4196.50 |
| 2 | 09-16 10:15 | 4197.00 | 4198.00 | 4196.20 | 4196.60 |
| 3 | 09-16 10:30 | 4195.50 | 4196.00 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4189.51/4189.71; 09-16 10:46:40 4189.30/4189.50; 09-16 10:47:30 4183.80/4184.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4189.51
- stop: 4198.20
- R: 8.69
- target(s): 4189.50, 4184.00
- exit: TARGET net 221/869 (≈0.2543)R

#### `GV-P16-V06` · `GT-EVENINGSTAR-BEAR-v1.0/SRC-PS` · M15
> No live zone below TP1: TP2 does not exist; TP1 hit leaves 40% open (PARTIAL_OPEN).

Tags: partials, no-tp2
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.50 | 4196.50 |
| 2 | 09-16 10:15 | 4197.00 | 4198.00 | 4196.20 | 4196.60 |
| 3 | 09-16 10:30 | 4195.50 | 4196.00 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4190.80/4191.00; 09-16 10:46:40 4189.30/4189.50

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4190.80
- stop: 4198.20
- R: 7.40
- target(s): 4189.50, None
- exit: PARTIAL_OPEN

#### `GV-P16-V07` · `GT-EVENINGSTAR-BEAR-v1.0/SRC-PS` · M15
> Case where H2 (4196.90) is BELOW H1 (4197.00). Ruling A-17 makes the stop policy symmetric with the Morning Star: max(H1,H2)+0.20 = 4197.20 (not H2+0.20 = 4197.10).

Tags: asymmetry, stop-policy
Context: atr=4 · trend=UP · zones_entry=[4183.00-4184.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.50 | 4196.50 |
| 2 | 09-16 10:15 | 4196.50 | 4196.90 | 4196.20 | 4196.60 |
| 3 | 09-16 10:30 | 4195.50 | 4196.00 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4190.80/4191.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- stop: 4197.20

