# P19 Abandoned Baby — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.2.2 · vector pack GV-0.1 · **74 vectors** (74 firm)

Strategies covered: `GT-ABABY-BEAR-v1.0`, `GT-ABABY-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-ABABY-BEAR-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `A01m` | 4180.00/4190.00/4179.50/4188.00 ; 4191.00/4192.00/4190.40/4190.95 ; 4189.50/4190.00/4180.00/4180.50 | UP | 8 | shape ✔ · formed ✔ | — | ATR 8 -> gap_thr = max(0.10, 0.40) = 0.40. L1=4210.00 so H2 <= 4209.60 (exactly) passes; L3 >= H2+0.40 = 4210.00 (exactly) passes. |
| `A02m` | 4180.00/4190.00/4179.50/4188.00 ; 4191.00/4192.00/4190.39/4190.95 ; 4189.50/4190.00/4180.00/4180.50 | UP | 8 | no shape | (2 clause) | ATR 8: H2 = 4209.61 breaks the 0.40 gap; and then L3 4210.00 < H2+0.40. |
| `A03m` | 4190.00/4191.10/4189.90/4191.00 ; 4191.50/4191.80/4191.20/4191.48 ; 4191.00/4191.10/4189.80/4190.00 | UP | 1 | shape ✔ · formed ✔ | — | ATR 1 -> gap_thr = max(0.10, 0.05) = 0.10 (the fixed floor wins). H2 = L1 - 0.10 exactly; L3 = H2 + 0.10 exactly. |
| `B01m` | 4190.00/4196.50/4189.50/4196.00 ; 4197.00/4198.20/4196.70/4196.95 ; 4196.00/4196.40/4190.40/4190.80 | UP | 4 | shape ✔ · formed ✔ | — | H2 exactly L1 - gap_thr (4203.30; gap_thr = 0.20): passes (L3 kept clear at 4203.60). |
| `B02m` | 4190.00/4196.50/4189.50/4196.00 ; 4197.00/4198.20/4196.69/4196.95 ; 4196.00/4196.40/4190.40/4190.80 | UP | 4 | no shape | (1 clause) | H2 = 4203.31 (0.01 too high): fails only H2<=L1-gap. |
| `B03m` | 4190.00/4196.50/4189.50/4196.00 ; 4197.20/4198.20/4196.80/4197.15 ; 4196.00/4196.60/4190.50/4190.80 | UP | 4 | shape ✔ · formed ✔ | — | L3 exactly H2 + gap_thr (H2 4203.20 -> L3 4203.40): passes. |
| `B04m` | 4190.00/4196.50/4189.50/4196.00 ; 4197.20/4198.20/4196.80/4197.15 ; 4196.00/4196.61/4190.50/4190.80 | UP | 4 | no shape | (1 clause) | L3 = 4203.39: fails only L3>=H2+gap. |
| `B05m` | 4190.00/4196.50/4189.50/4196.00 ; 4197.20/4198.80/4196.80/4197.10 ; 4196.00/4196.50/4190.50/4190.80 | UP | 4 | shape ✔ · formed ✔ | — | DOJI(C2) exactly B = 0.05R (R 2.00, B 0.10): passes. |
| `B06m` | 4190.00/4196.50/4189.50/4196.00 ; 4197.20/4198.80/4196.80/4197.09 ; 4196.00/4196.50/4190.50/4190.80 | UP | 4 | no shape | (1 clause) | DOJI(C2) with B = 0.11 (R 2.00): fails only DOJI. |
| `N01m` | 4190.00/4196.50/4189.50/4196.00 ; 4195.50/4196.20/4195.00/4195.45 ; 4196.00/4196.50/4190.50/4190.80 | UP | 4 | no shape | (2 clause) | C2 overlaps C1 (no gap): fails the first gap clause; L3 clause also fails. |
| `N02m` | 4190.00/4197.00/4189.50/4196.50 ; 4197.00/4198.00/4196.20/4196.60 ; 4195.50/4196.00/4190.50/4190.80 | UP | 4 | no shape | (2 clause) | Ordinary Morning Star (small star that overlaps): abandoned baby requires TRUE gaps on both sides. |
| `NZ1m` | 4190.00/4194.50/4189.50/4194.00 ; 4194.00/4194.50/4189.50/4190.00 ; 4190.00/4190.50/4185.50/4186.00 | UP | 4 | canonical: no event; variant: no event | — | Bear, bull, bull with no doji and no gaps. |
| `T01m` | 4190.00/4196.50/4189.50/4196.00 ; 4197.20/4198.20/4196.80/4197.15 ; 4196.00/4196.50/4190.50/4190.80 | DOWN | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Abandoned Baby shape after UP: not formed. |
| `T02m` | 4190.00/4196.50/4189.50/4196.00 ; 4197.20/4198.20/4196.80/4197.15 ; 4196.00/4196.50/4190.50/4190.80 | RANGE | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Abandoned Baby shape after RANGE: not formed. |
| `T03m` | 4190.00/4196.50/4189.50/4196.00 ; 4197.20/4198.20/4196.80/4197.15 ; 4196.00/4196.50/4190.50/4190.80 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Abandoned Baby shape after UNDETERMINED: not formed. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01m` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:45:02 4190.60/4190.80; 09-16 10:47:00 4186.70/4186.90; 09-16 10:50:00 4174.80/4175.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.40; R: 7.80; target(s): 4175.00; exit: TARGET net 2.00R |
| `L02m` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:45:02 4190.60/4190.80; 09-16 10:47:00 4194.50/4194.70; 09-16 10:50:00 4198.20/4198.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.40; R: 7.80; target(s): 4175.00; exit: STOP net -1.00R |
| `L03m` | Tick gaps through the stop (bid 4199.60 < stop): fill = that tick's bid, not the stop (G9): -49/39R. | 09-16 10:45:02 4190.60/4190.80; 09-16 10:47:00 4200.20/4200.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.40; R: 7.80; target(s): 4175.00; exit: STOP net -49/39 (≈-1.2564)R |
| `L04m` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:45:02 4190.60/4190.80; 09-16 10:46:40 4198.20/4198.40; 09-16 10:48:20 4174.80/4175.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.40; R: 7.80; target(s): 4175.00; exit: STOP net -1.00R |
| `L05m` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:45:02 4190.60/4190.80; 09-16 10:46:40 4174.80/4175.00; 09-16 10:48:20 4198.20/4198.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.40; R: 7.80; target(s): 4175.00; exit: TARGET net 2.00R |
| `L06m` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:45:02 4190.60/4190.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.40; R: 7.80; target(s): 4175.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07m` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:45:02 4190.30/4190.80; 09-16 10:48:20 4173.60/4174.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.30; stop: 4198.40; R: 8.10; target(s): 4174.10; exit: TARGET net 2.00R |
| `L08m` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 11:00:00 4190.60/4190.80; 09-16 11:01:40 4174.80/4175.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.40; R: 7.80; target(s): 4175.00; exit: TARGET net 2.00R |
| `L09m` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 11:00:01 4190.60/4190.80; 09-16 11:01:40 4174.80/4175.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10m` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:45:02 4196.40/4196.90; 09-16 10:46:40 4191.90/4192.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4196.40; R: 2.00; target(s): 4192.40; exit: TARGET net 2.00R |
| `L11m` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:45:02 4196.41/4196.91; 09-16 10:46:40 4191.91/4192.41 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12m` | Tick jumps far past the target (bid 4231.40 > target 4225.00): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:45:02 4190.60/4190.80; 09-16 10:47:00 4168.40/4168.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.60; stop: 4198.40; R: 7.80; target(s): 4175.00; exit: TARGET net 2.00R |
| `W01m` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4190.60/4190.80; 09-21 00:30:00 4174.80/4175.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4190.60; stop: 4198.40; R: 7.80; target(s): 4175.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W02m` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4190.60/4190.80; 09-21 00:30:00 4174.80/4175.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4190.60; stop: 4198.40; R: 7.80; target(s): 4175.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W03m` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4190.60/4190.80 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P19-R01m` · `GT-ABABY-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P19-R01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4197.20 | 4198.20 | 4196.80 | 4197.15 |
| 3 | 09-16 10:30 | 4196.00 | 4196.50 | 4190.50 | 4190.80 |
| 4 | 09-16 10:45 | 4190.80 | 4192.80 | 4187.80 | 4189.80 |
| 5 | 09-16 11:00 | 4189.80 | 4191.80 | 4186.80 | 4188.80 |
| 6 | 09-16 11:15 | 4188.80 | 4193.80 | 4187.80 | 4191.80 |
| 7 | 09-16 11:30 | 4191.80 | 4194.80 | 4188.80 | 4190.80 |
| 8 | 09-16 11:45 | 4189.80 | 4192.80 | 4185.80 | 4187.80 |
| 9 | 09-16 12:00 | 4187.80 | 4199.80 | 4181.80 | 4186.80 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4190.80 | h1: ret=1.00, mfe=3.00, mae=-2.00, end_index=3 | h3: ret=-1.00, mfe=4.00, mae=-3.00, end_index=5 | h5: ret=3.00, mfe=5.00, mae=-4.00, end_index=7 | h10: NULL | h20: NULL

#### `GV-P19-Y01m` · `GT-ABABY-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P19-Y01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4197.20 | 4198.20 | 4196.80 | 4197.15 |
| 3 | 09-16 10:30 | 4196.00 | 4196.50 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4190.60/4190.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:45:00Z
- entry: 4190.60
- stop: 4198.40
- R: 7.80
- target(s): 4175.00

### Variant `SRC-PS-COMPLETED`

#### `GV-P19-V01m` · `GT-ABABY-BEAR-v1.0/SRC-PS-COMPLETED` · M15
*Mirror of `GV-P19-V01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> SRC-PS Abandoned Baby: stop L2-0.20 = 4201.60 (equal to the baseline stop by construction: the doji's low is always the lowest). Entry ask 4209.40; R 7.80; T_SWING(1.5): swing 4222.00 = 1.62R -> trade.

Tags: variant-clean-yes, T_SWING
Context: atr=4 · trend=UP · swings=L4178.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4197.20 | 4198.20 | 4196.80 | 4197.15 |
| 3 | 09-16 10:30 | 4196.00 | 4196.50 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4190.60/4190.80; 09-16 10:46:40 4177.80/4178.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4190.60
- stop: 4198.40
- R: 7.80
- target(s): 4178.00
- exit: TARGET net 21/13 (≈1.6154)R

#### `GV-P19-V02m` · `GT-ABABY-BEAR-v1.0/SRC-PS-COMPLETED` · M15
*Mirror of `GV-P19-V02` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Swing exactly 1.5R (4209.40 + 11.70 = 4221.10): accepted.

Tags: T_SWING, boundary
Context: atr=4 · trend=UP · swings=L4178.90

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4197.20 | 4198.20 | 4196.80 | 4197.15 |
| 3 | 09-16 10:30 | 4196.00 | 4196.50 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4190.60/4190.80; 09-16 10:46:40 4178.70/4178.90

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4190.60
- stop: 4198.40
- R: 7.80
- target(s): 4178.90
- exit: TARGET net 1.50R

#### `GV-P19-V03m` · `GT-ABABY-BEAR-v1.0/SRC-PS-COMPLETED` · M15
*Mirror of `GV-P19-V03` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Swing 4221.09: 1.4987R -> SKIPPED_SRC_RR.

Tags: T_SWING, boundary, insufficient-rr
Context: atr=4 · trend=UP · swings=L4178.91

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4197.20 | 4198.20 | 4196.80 | 4197.15 |
| 3 | 09-16 10:30 | 4196.00 | 4196.50 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4190.60/4190.80

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4190.60
- stop: 4198.40
- R: 7.80

#### `GV-P19-V04m` · `GT-ABABY-BEAR-v1.0/SRC-PS-COMPLETED` · M15
*Mirror of `GV-P19-V04` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> No swing -> SKIPPED_SRC_NO_TARGET.

Tags: T_SWING, no-target
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4197.20 | 4198.20 | 4196.80 | 4197.15 |
| 3 | 09-16 10:30 | 4196.00 | 4196.50 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4190.60/4190.80

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4190.60
- stop: 4198.40
- R: 7.80

#### `GV-P19-V05m` · `GT-ABABY-BEAR-v1.0/SRC-PS-COMPLETED` · M15
*Mirror of `GV-P19-V05` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Stop hit: -1.00R.

Tags: variant, sl-first-ticks
Context: atr=4 · trend=UP · swings=L4178.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4197.20 | 4198.20 | 4196.80 | 4197.15 |
| 3 | 09-16 10:30 | 4196.00 | 4196.50 | 4190.50 | 4190.80 |

Ticks (bid/ask): 09-16 10:45:02 4190.60/4190.80; 09-16 10:46:40 4198.20/4198.40

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4190.60
- stop: 4198.40
- R: 7.80
- target(s): 4178.00
- exit: STOP net -1.00R

## `GT-ABABY-BULL-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `A01` | 4220.00/4220.50/4210.00/4212.00 ; 4209.00/4209.60/4208.00/4209.05 ; 4210.50/4220.00/4210.00/4219.50 | DOWN | 8 | shape ✔ · formed ✔ | — | ATR 8 -> gap_thr = max(0.10, 0.40) = 0.40. L1=4210.00 so H2 <= 4209.60 (exactly) passes; L3 >= H2+0.40 = 4210.00 (exactly) passes. |
| `A02` | 4220.00/4220.50/4210.00/4212.00 ; 4209.00/4209.61/4208.00/4209.05 ; 4210.50/4220.00/4210.00/4219.50 | DOWN | 8 | no shape | H2<=L1-gap, L3>=H2+gap | ATR 8: H2 = 4209.61 breaks the 0.40 gap; and then L3 4210.00 < H2+0.40. |
| `A03` | 4210.00/4210.10/4208.90/4209.00 ; 4208.50/4208.80/4208.20/4208.52 ; 4209.00/4210.20/4208.90/4210.00 | DOWN | 1 | shape ✔ · formed ✔ | — | ATR 1 -> gap_thr = max(0.10, 0.05) = 0.10 (the fixed floor wins). H2 = L1 - 0.10 exactly; L3 = H2 + 0.10 exactly. |
| `B01` | 4210.00/4210.50/4203.50/4204.00 ; 4203.00/4203.30/4201.80/4203.05 ; 4204.00/4209.60/4203.60/4209.20 | DOWN | 4 | shape ✔ · formed ✔ | — | H2 exactly L1 - gap_thr (4203.30; gap_thr = 0.20): passes (L3 kept clear at 4203.60). |
| `B02` | 4210.00/4210.50/4203.50/4204.00 ; 4203.00/4203.31/4201.80/4203.05 ; 4204.00/4209.60/4203.60/4209.20 | DOWN | 4 | no shape | H2<=L1-gap | H2 = 4203.31 (0.01 too high): fails only H2<=L1-gap. |
| `B03` | 4210.00/4210.50/4203.50/4204.00 ; 4202.80/4203.20/4201.80/4202.85 ; 4204.00/4209.50/4203.40/4209.20 | DOWN | 4 | shape ✔ · formed ✔ | — | L3 exactly H2 + gap_thr (H2 4203.20 -> L3 4203.40): passes. |
| `B04` | 4210.00/4210.50/4203.50/4204.00 ; 4202.80/4203.20/4201.80/4202.85 ; 4204.00/4209.50/4203.39/4209.20 | DOWN | 4 | no shape | L3>=H2+gap | L3 = 4203.39: fails only L3>=H2+gap. |
| `B05` | 4210.00/4210.50/4203.50/4204.00 ; 4202.80/4203.20/4201.20/4202.90 ; 4204.00/4209.50/4203.50/4209.20 | DOWN | 4 | shape ✔ · formed ✔ | — | DOJI(C2) exactly B = 0.05R (R 2.00, B 0.10): passes. |
| `B06` | 4210.00/4210.50/4203.50/4204.00 ; 4202.80/4203.20/4201.20/4202.91 ; 4204.00/4209.50/4203.50/4209.20 | DOWN | 4 | no shape | DOJI(C2) | DOJI(C2) with B = 0.11 (R 2.00): fails only DOJI. |
| `N01` | 4210.00/4210.50/4203.50/4204.00 ; 4204.50/4205.00/4203.80/4204.55 ; 4204.00/4209.50/4203.50/4209.20 | DOWN | 4 | no shape | H2<=L1-gap, L3>=H2+gap | C2 overlaps C1 (no gap): fails the first gap clause; L3 clause also fails. |
| `N02` | 4210.00/4210.50/4203.00/4203.50 ; 4203.00/4203.80/4202.00/4203.40 ; 4204.50/4209.50/4204.00/4209.20 | DOWN | 4 | no shape | DOJI(C2), H2<=L1-gap | Ordinary Morning Star (small star that overlaps): abandoned baby requires TRUE gaps on both sides. |
| `NZ1` | 4210.00/4210.50/4205.50/4206.00 ; 4206.00/4210.50/4205.50/4210.00 ; 4210.00/4214.50/4209.50/4214.00 | DOWN | 4 | canonical: no event; variant: no event | — | Bear, bull, bull with no doji and no gaps. |
| `T01` | 4210.00/4210.50/4203.50/4204.00 ; 4202.80/4203.20/4201.80/4202.85 ; 4204.00/4209.50/4203.50/4209.20 | UP | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Abandoned Baby shape after UP: not formed. |
| `T02` | 4210.00/4210.50/4203.50/4204.00 ; 4202.80/4203.20/4201.80/4202.85 ; 4204.00/4209.50/4203.50/4209.20 | RANGE | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Abandoned Baby shape after RANGE: not formed. |
| `T03` | 4210.00/4210.50/4203.50/4204.00 ; 4202.80/4203.20/4201.80/4202.85 ; 4204.00/4209.50/4203.50/4209.20 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Abandoned Baby shape after UNDETERMINED: not formed. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:45:02 4209.20/4209.40; 09-16 10:47:00 4213.10/4213.30; 09-16 10:50:00 4225.00/4225.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.60; R: 7.80; target(s): 4225.00; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:45:02 4209.20/4209.40; 09-16 10:47:00 4205.30/4205.50; 09-16 10:50:00 4201.60/4201.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.60; R: 7.80; target(s): 4225.00; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4199.60 < stop): fill = that tick's bid, not the stop (G9): -49/39R. | 09-16 10:45:02 4209.20/4209.40; 09-16 10:47:00 4199.60/4199.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.60; R: 7.80; target(s): 4225.00; exit: STOP net -49/39 (≈-1.2564)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:45:02 4209.20/4209.40; 09-16 10:46:40 4201.60/4201.80; 09-16 10:48:20 4225.00/4225.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.60; R: 7.80; target(s): 4225.00; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:45:02 4209.20/4209.40; 09-16 10:46:40 4225.00/4225.20; 09-16 10:48:20 4201.60/4201.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.60; R: 7.80; target(s): 4225.00; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:45:02 4209.20/4209.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.60; R: 7.80; target(s): 4225.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:45:02 4209.20/4209.70; 09-16 10:48:20 4225.90/4226.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.70; stop: 4201.60; R: 8.10; target(s): 4225.90; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 11:00:00 4209.20/4209.40; 09-16 11:01:40 4225.00/4225.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.60; R: 7.80; target(s): 4225.00; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 11:00:01 4209.20/4209.40; 09-16 11:01:40 4225.00/4225.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:45:02 4203.10/4203.60; 09-16 10:46:40 4207.60/4208.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4203.60; R: 2.00; target(s): 4207.60; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:45:02 4203.09/4203.59; 09-16 10:46:40 4207.59/4208.09 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4231.40 > target 4225.00): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:45:02 4209.20/4209.40; 09-16 10:47:00 4231.40/4231.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.40; stop: 4201.60; R: 7.80; target(s): 4225.00; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4209.20/4209.40; 09-21 00:30:00 4225.00/4225.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4209.40; stop: 4201.60; R: 7.80; target(s): 4225.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4209.20/4209.40; 09-21 00:30:00 4225.00/4225.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4209.40; stop: 4201.60; R: 7.80; target(s): 4225.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4209.20/4209.40 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P19-R01` · `GT-ABABY-BULL-v1.0/BASE` · M15
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |
| 3 | 09-16 10:30 | 4204.00 | 4209.50 | 4203.50 | 4209.20 |
| 4 | 09-16 10:45 | 4209.20 | 4212.20 | 4207.20 | 4210.20 |
| 5 | 09-16 11:00 | 4210.20 | 4213.20 | 4208.20 | 4211.20 |
| 6 | 09-16 11:15 | 4211.20 | 4212.20 | 4206.20 | 4208.20 |
| 7 | 09-16 11:30 | 4208.20 | 4211.20 | 4205.20 | 4209.20 |
| 8 | 09-16 11:45 | 4210.20 | 4214.20 | 4207.20 | 4212.20 |
| 9 | 09-16 12:00 | 4212.20 | 4218.20 | 4200.20 | 4213.20 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4209.20 | h1: ret=1.00, mfe=3.00, mae=-2.00, end_index=3 | h3: ret=-1.00, mfe=4.00, mae=-3.00, end_index=5 | h5: ret=3.00, mfe=5.00, mae=-4.00, end_index=7 | h10: NULL | h20: NULL

#### `GV-P19-Y01` · `GT-ABABY-BULL-v1.0/BASE` · M15
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |
| 3 | 09-16 10:30 | 4204.00 | 4209.50 | 4203.50 | 4209.20 |

Ticks (bid/ask): 09-16 10:45:02 4209.20/4209.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:45:00Z
- entry: 4209.40
- stop: 4201.60
- R: 7.80
- target(s): 4225.00

### Variant `SRC-PS-COMPLETED`

#### `GV-P19-V01` · `GT-ABABY-BULL-v1.0/SRC-PS-COMPLETED` · M15
> SRC-PS Abandoned Baby: stop L2-0.20 = 4201.60 (equal to the baseline stop by construction: the doji's low is always the lowest). Entry ask 4209.40; R 7.80; T_SWING(1.5): swing 4222.00 = 1.62R -> trade.

Tags: variant-clean-yes, T_SWING
Context: atr=4 · trend=DOWN · swings=H4222.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |
| 3 | 09-16 10:30 | 4204.00 | 4209.50 | 4203.50 | 4209.20 |

Ticks (bid/ask): 09-16 10:45:02 4209.20/4209.40; 09-16 10:46:40 4222.00/4222.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4209.40
- stop: 4201.60
- R: 7.80
- target(s): 4222.00
- exit: TARGET net 21/13 (≈1.6154)R

#### `GV-P19-V02` · `GT-ABABY-BULL-v1.0/SRC-PS-COMPLETED` · M15
> Swing exactly 1.5R (4209.40 + 11.70 = 4221.10): accepted.

Tags: T_SWING, boundary
Context: atr=4 · trend=DOWN · swings=H4221.10

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |
| 3 | 09-16 10:30 | 4204.00 | 4209.50 | 4203.50 | 4209.20 |

Ticks (bid/ask): 09-16 10:45:02 4209.20/4209.40; 09-16 10:46:40 4221.10/4221.30

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4209.40
- stop: 4201.60
- R: 7.80
- target(s): 4221.10
- exit: TARGET net 1.50R

#### `GV-P19-V03` · `GT-ABABY-BULL-v1.0/SRC-PS-COMPLETED` · M15
> Swing 4221.09: 1.4987R -> SKIPPED_SRC_RR.

Tags: T_SWING, boundary, insufficient-rr
Context: atr=4 · trend=DOWN · swings=H4221.09

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |
| 3 | 09-16 10:30 | 4204.00 | 4209.50 | 4203.50 | 4209.20 |

Ticks (bid/ask): 09-16 10:45:02 4209.20/4209.40

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4209.40
- stop: 4201.60
- R: 7.80

#### `GV-P19-V04` · `GT-ABABY-BULL-v1.0/SRC-PS-COMPLETED` · M15
> No swing -> SKIPPED_SRC_NO_TARGET.

Tags: T_SWING, no-target
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |
| 3 | 09-16 10:30 | 4204.00 | 4209.50 | 4203.50 | 4209.20 |

Ticks (bid/ask): 09-16 10:45:02 4209.20/4209.40

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4209.40
- stop: 4201.60
- R: 7.80

#### `GV-P19-V05` · `GT-ABABY-BULL-v1.0/SRC-PS-COMPLETED` · M15
> Stop hit: -1.00R.

Tags: variant, sl-first-ticks
Context: atr=4 · trend=DOWN · swings=H4222.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |
| 3 | 09-16 10:30 | 4204.00 | 4209.50 | 4203.50 | 4209.20 |

Ticks (bid/ask): 09-16 10:45:02 4209.20/4209.40; 09-16 10:46:40 4201.60/4201.80

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4209.40
- stop: 4201.60
- R: 7.80
- target(s): 4222.00
- exit: STOP net -1.00R

