# P21 Falling Three Methods — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.3 · vector pack GV-0.2 · **38 vectors** (38 firm)

Strategies covered: `GT-FALLING3-BEAR-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-FALLING3-BEAR-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4200.00/4201.00/4188.00/4189.00 ; 4190.00/4194.00/4188.00/4193.00 ; 4192.00/4195.50/4191.50/4194.50 ; 4194.00/4197.00/4193.50/4196.00 ; 4195.00/4195.50/4184.00/4184.50 | DOWN | 4 | shape ✔ · formed ✔ | — | Middle bar high exactly H1 (4212.00): passes (H<=H1). |
| `B02` | 4200.00/4201.00/4188.00/4189.00 ; 4190.00/4194.00/4187.99/4193.00 ; 4192.00/4195.50/4191.50/4194.50 ; 4194.00/4197.00/4193.50/4196.00 ; 4195.00/4195.50/4184.00/4184.50 | DOWN | 4 | no shape | (1 clause) | Middle bar high 4212.01: fails only that clause. |
| `B03` | 4200.00/4201.00/4188.00/4189.00 ; 4190.00/4194.00/4189.50/4193.00 ; 4192.00/4195.50/4191.50/4194.50 ; 4194.00/4201.00/4193.50/4196.00 ; 4195.00/4195.50/4184.00/4184.50 | DOWN | 4 | shape ✔ · formed ✔ | — | Middle bar low exactly L1 (4199.00): passes. |
| `B04` | 4200.00/4201.00/4188.00/4189.00 ; 4190.00/4194.00/4189.50/4193.00 ; 4192.00/4195.50/4191.50/4194.50 ; 4194.00/4201.01/4193.50/4196.00 ; 4195.00/4195.50/4184.00/4184.50 | DOWN | 4 | no shape | (1 clause) | Middle bar low 4198.99: fails only that clause. |
| `B05` | 4200.00/4201.00/4188.00/4189.00 ; 4190.00/4194.00/4189.50/4193.00 ; 4190.00/4196.00/4189.80/4195.50 ; 4194.00/4197.00/4193.50/4196.00 ; 4195.00/4195.50/4184.00/4184.50 | DOWN | 4 | shape ✔ · formed ✔ | — | Middle body exactly 0.5*B1 (5.50): passes. |
| `B06` | 4200.00/4201.00/4188.00/4189.00 ; 4190.00/4194.00/4189.50/4193.00 ; 4189.99/4196.00/4189.80/4195.50 ; 4194.00/4197.00/4193.50/4196.00 ; 4195.00/4195.50/4184.00/4184.50 | DOWN | 4 | no shape | (1 clause) | Middle body 5.51: fails only that clause. |
| `B07` | 4200.00/4201.00/4188.00/4189.00 ; 4190.00/4194.00/4189.50/4193.00 ; 4192.00/4195.50/4191.50/4194.50 ; 4194.00/4197.00/4193.50/4196.00 ; 4195.00/4195.50/4188.40/4189.00 | DOWN | 4 | no shape | (1 clause) | C5 closes exactly at C1's close (4211.00): fails only C5>C1 (strict). |
| `B08` | 4200.00/4201.00/4188.00/4189.00 ; 4190.00/4194.00/4189.50/4193.00 ; 4192.00/4195.50/4191.50/4194.50 ; 4194.00/4197.00/4193.50/4196.00 ; 4195.00/4195.50/4188.40/4188.99 | DOWN | 4 | shape ✔ · formed ✔ | — | C5 closes 0.01 above C1's close: passes. |
| `F01` | 4200.00/4201.00/4188.00/4189.00 ; 4190.00/4194.00/4189.50/4193.00 ; 4192.00/4195.50/4191.50/4194.50 ; 4194.00/4197.00/4193.50/4196.00 ; 4195.00/4195.50/4184.00/4184.50 | DOWN | 4 | shape ✔ · formed ✔ | — | All middle closes (4207, 4205.5, 4204) lie within C1's body [4200, 4211]: flag true. |
| `F02` | 4200.00/4201.00/4188.00/4189.00 ; 4188.50/4192.00/4188.40/4188.99 ; 4192.00/4195.50/4191.50/4194.50 ; 4194.00/4197.00/4193.50/4196.00 ; 4195.00/4195.50/4184.00/4184.50 | DOWN | 4 | shape ✔ · formed ✔ | — | Middle close 4211.01 is above C1's close 4211.00: flag false, pattern still forms (canonical rule uses full high-low containment). |
| `N01` | 4200.00/4201.00/4188.00/4189.00 ; 4190.00/4194.00/4189.50/4193.00 ; 4194.50/4195.50/4191.50/4192.00 ; 4194.00/4197.00/4193.50/4196.00 ; 4195.00/4195.50/4184.00/4184.50 | DOWN | 4 | no shape | (1 clause) | A bullish middle candle (bar 3) breaks the alternation: fails colour. |
| `N02` | 4200.00/4201.00/4188.00/4189.00 ; 4190.00/4194.00/4189.50/4193.00 ; 4192.00/4195.50/4191.50/4194.50 ; 4194.00/4197.00/4193.50/4196.00 ; 4195.00/4195.50/4188.40/4193.00 | DOWN | 4 | no shape | (2 clause) | C5 is not LARGE: fails LARGE(C5) (and C5>C1). |
| `NZ1` | 4200.00/4200.50/4195.50/4196.00 ; 4196.00/4196.50/4191.50/4192.00 ; 4192.00/4192.50/4187.50/4188.00 ; 4188.00/4188.50/4183.50/4184.00 ; 4184.00/4184.50/4179.50/4180.00 | DOWN | 4 | canonical: no event; variant: no event | — | Five bullish candles: the middle three must be bearish and contained. |
| `T01` | 4200.00/4201.00/4188.00/4189.00 ; 4190.00/4194.00/4189.50/4193.00 ; 4192.00/4195.50/4191.50/4194.50 ; 4194.00/4197.00/4193.50/4196.00 ; 4195.00/4195.50/4184.00/4184.50 | UP | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Rising Three Methods shape after DOWN: not formed. |
| `T02` | 4200.00/4201.00/4188.00/4189.00 ; 4190.00/4194.00/4189.50/4193.00 ; 4192.00/4195.50/4191.50/4194.50 ; 4194.00/4197.00/4193.50/4196.00 ; 4195.00/4195.50/4184.00/4184.50 | RANGE | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Rising Three Methods shape after RANGE: not formed. |
| `T03` | 4200.00/4201.00/4188.00/4189.00 ; 4190.00/4194.00/4189.50/4193.00 ; 4192.00/4195.50/4191.50/4194.50 ; 4194.00/4197.00/4193.50/4196.00 ; 4195.00/4195.50/4184.00/4184.50 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Rising Three Methods shape after UNDETERMINED: not formed. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 11:15:02 4184.30/4184.50; 09-16 11:17:00 4175.85/4176.05; 09-16 11:20:00 4150.30/4150.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4184.30; stop: 4201.20; R: 16.90; target(s): 4150.50; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 11:15:02 4184.30/4184.50; 09-16 11:17:00 4192.75/4192.95; 09-16 11:20:00 4201.00/4201.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4184.30; stop: 4201.20; R: 16.90; target(s): 4150.50; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4196.80 < stop): fill = that tick's bid, not the stop (G9): -189/169R. | 09-16 11:15:02 4184.30/4184.50; 09-16 11:17:00 4203.00/4203.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4184.30; stop: 4201.20; R: 16.90; target(s): 4150.50; exit: STOP net -189/169 (≈-1.1183)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 11:15:02 4184.30/4184.50; 09-16 11:16:40 4201.00/4201.20; 09-16 11:18:20 4150.30/4150.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4184.30; stop: 4201.20; R: 16.90; target(s): 4150.50; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 11:15:02 4184.30/4184.50; 09-16 11:16:40 4150.30/4150.50; 09-16 11:18:20 4201.00/4201.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4184.30; stop: 4201.20; R: 16.90; target(s): 4150.50; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 11:15:02 4184.30/4184.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4184.30; stop: 4201.20; R: 16.90; target(s): 4150.50; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 11:15:02 4184.00/4184.50; 09-16 11:18:20 4149.10/4149.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; spread_at_entry: 0.50; entry: 4184.00; stop: 4201.20; R: 17.20; target(s): 4149.60; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 11:30:00 4184.30/4184.50; 09-16 11:31:40 4150.30/4150.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4184.30; stop: 4201.20; R: 16.90; target(s): 4150.50; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 11:30:01 4184.30/4184.50; 09-16 11:31:40 4150.30/4150.50 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 11:15:02 4199.20/4199.70; 09-16 11:16:40 4194.70/4195.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.20; R: 2.00; target(s): 4195.20; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 11:15:02 4199.21/4199.71; 09-16 11:16:40 4194.71/4195.21 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4255.90 > target 4249.50): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 11:15:02 4184.30/4184.50; 09-16 11:17:00 4143.90/4144.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4184.30; stop: 4201.20; R: 16.90; target(s): 4150.50; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4184.30/4184.50; 09-21 00:30:00 4150.30/4150.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4184.30; stop: 4201.20; R: 16.90; target(s): 4150.50; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4184.30/4184.50; 09-21 00:30:00 4150.30/4150.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4184.30; stop: 4201.20; R: 16.90; target(s): 4150.50; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4184.30/4184.50 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P21-R01` · `GT-FALLING3-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P20-R01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4201.00 | 4188.00 | 4189.00 |
| 2 | 09-16 10:15 | 4190.00 | 4194.00 | 4189.50 | 4193.00 |
| 3 | 09-16 10:30 | 4192.00 | 4195.50 | 4191.50 | 4194.50 |
| 4 | 09-16 10:45 | 4194.00 | 4197.00 | 4193.50 | 4196.00 |
| 5 | 09-16 11:00 | 4195.00 | 4195.50 | 4184.00 | 4184.50 |
| 6 | 09-16 11:15 | 4184.50 | 4186.50 | 4181.50 | 4183.50 |
| 7 | 09-16 11:30 | 4183.50 | 4185.50 | 4180.50 | 4182.50 |
| 8 | 09-16 11:45 | 4182.50 | 4187.50 | 4181.50 | 4185.50 |
| 9 | 09-16 12:00 | 4185.50 | 4188.50 | 4182.50 | 4184.50 |
| 10 | 09-16 12:15 | 4183.50 | 4186.50 | 4179.50 | 4181.50 |
| 11 | 09-16 12:30 | 4181.50 | 4193.50 | 4175.50 | 4180.50 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4184.50 | h1: ret=1.00, mfe=3.00, mae=2.00, end_index=5 | h3: ret=-1.00, mfe=4.00, mae=3.00, end_index=7 | h5: ret=3.00, mfe=5.00, mae=4.00, end_index=9 | h10: NULL | h20: NULL

#### `GV-P21-Y01` · `GT-FALLING3-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P20-Y01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4201.00 | 4188.00 | 4189.00 |
| 2 | 09-16 10:15 | 4190.00 | 4194.00 | 4189.50 | 4193.00 |
| 3 | 09-16 10:30 | 4192.00 | 4195.50 | 4191.50 | 4194.50 |
| 4 | 09-16 10:45 | 4194.00 | 4197.00 | 4193.50 | 4196.00 |
| 5 | 09-16 11:00 | 4195.00 | 4195.50 | 4184.00 | 4184.50 |

Ticks (bid/ask): 09-16 11:15:02 4184.30/4184.50

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T11:15:00Z
- entry: 4184.30
- stop: 4201.20
- R: 16.90
- target(s): 4150.50

### Variant `SRC-PS`

#### `GV-P21-V01` · `GT-FALLING3-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P20-V01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> SRC-PS Rising Three: stop = min(L2,L3,L4) - 0.20 = 4217.80; TP1 = P + 1.272*(H1-L1) with P = min(L2..L4) = 4218.00 -> 4218.00 + 1.272*31.00 = 4257.432, quantised in the PROFIT direction (up) to 4257.44 (A-30); entry ask 4231.01; R 13.21; reward 26.43 vs 2R = 26.42 -> passes (just inside).

Tags: variant, fib-target, boundary
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4201.00 | 4170.00 | 4171.00 |
| 2 | 09-16 10:15 | 4172.00 | 4178.00 | 4171.00 | 4177.00 |
| 3 | 09-16 10:30 | 4176.00 | 4181.00 | 4175.00 | 4180.00 |
| 4 | 09-16 10:45 | 4179.00 | 4182.00 | 4178.00 | 4181.00 |
| 5 | 09-16 11:00 | 4181.00 | 4181.50 | 4170.00 | 4170.50 |

Ticks (bid/ask): 09-16 11:15:02 4168.99/4169.19; 09-16 11:16:40 4142.36/4142.56

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4168.99
- stop: 4182.20
- R: 13.21
- target(s): 4142.56
- exit: TARGET net 2643/1321 (≈2.0008)R

#### `GV-P21-V02` · `GT-FALLING3-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P20-V02` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Entry ask 4231.02: R 13.22, 2R = 26.44 > 26.42 available (target 4257.44) -> SKIPPED_SRC_RR (just outside).

Tags: fib-target, boundary, insufficient-rr
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4201.00 | 4170.00 | 4171.00 |
| 2 | 09-16 10:15 | 4172.00 | 4178.00 | 4171.00 | 4177.00 |
| 3 | 09-16 10:30 | 4176.00 | 4181.00 | 4175.00 | 4180.00 |
| 4 | 09-16 10:45 | 4179.00 | 4182.00 | 4178.00 | 4181.00 |
| 5 | 09-16 11:00 | 4181.00 | 4181.50 | 4170.00 | 4170.50 |

Ticks (bid/ask): 09-16 11:15:02 4168.98/4169.18

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR

#### `GV-P21-V03` · `GT-FALLING3-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P20-V03` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Original textbook bars: TP1 = 4203.00 + 1.272*13 = 4219.536 is only 3.84 above the entry 4215.70 (0.30R) -> SKIPPED_SRC_RR.

Tags: fib-target, insufficient-rr
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4201.00 | 4188.00 | 4189.00 |
| 2 | 09-16 10:15 | 4190.00 | 4194.00 | 4189.50 | 4193.00 |
| 3 | 09-16 10:30 | 4192.00 | 4195.50 | 4191.50 | 4194.50 |
| 4 | 09-16 10:45 | 4194.00 | 4197.00 | 4193.50 | 4196.00 |
| 5 | 09-16 11:00 | 4195.00 | 4195.50 | 4184.00 | 4184.50 |

Ticks (bid/ask): 09-16 11:15:02 4184.30/4184.50

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR

#### `GV-P21-V04` · `GT-FALLING3-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P20-V04` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Entry ask 4220.00 is ABOVE TP1 4219.536: target behind the entry -> SKIPPED_TARGET_ALREADY_PASSED (checked before the 2R test).

Tags: fib-target, target-already-passed
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4201.00 | 4188.00 | 4189.00 |
| 2 | 09-16 10:15 | 4190.00 | 4194.00 | 4189.50 | 4193.00 |
| 3 | 09-16 10:30 | 4192.00 | 4195.50 | 4191.50 | 4194.50 |
| 4 | 09-16 10:45 | 4194.00 | 4197.00 | 4193.50 | 4196.00 |
| 5 | 09-16 11:00 | 4195.00 | 4195.50 | 4184.00 | 4184.50 |

Ticks (bid/ask): 09-16 11:15:02 4180.00/4180.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_TARGET_ALREADY_PASSED

#### `GV-P21-V05` · `GT-FALLING3-BEAR-v1.0/SRC-PS` · M15
> Mirror image of GV-P20-V05: shape valid and formed (canonical uses high-low containment) but a middle close lies beyond C1's close, so the body-close flag is false. The FALLING source variant REQUIRES the flag (P21 field 17) -> not qualified. The RISING variant did not require it: a deliberate asymmetry in the spec (open item 2 in section 4).

Tags: asymmetry, close-rule, variant-not-qualified
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4201.00 | 4170.00 | 4171.00 |
| 2 | 09-16 10:15 | 4170.10 | 4178.00 | 4170.00 | 4170.50 |
| 3 | 09-16 10:30 | 4176.00 | 4181.00 | 4175.00 | 4180.00 |
| 4 | 09-16 10:45 | 4179.00 | 4182.00 | 4178.00 | 4181.00 |
| 5 | 09-16 11:00 | 4181.00 | 4181.50 | 4170.00 | 4170.50 |

Ticks (bid/ask): 09-16 11:15:02 4170.80/4171.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- flags: closes_in_body=False
- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: BODY_CLOSE_FLAG

