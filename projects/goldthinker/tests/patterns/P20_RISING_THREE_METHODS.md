# P20 Rising Three Methods — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.2.2 · vector pack GV-0.1 · **39 vectors** (38 firm, 1 provisional)

Strategies covered: `GT-RISING3-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-RISING3-BULL-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4200.00/4212.00/4199.00/4211.00 ; 4210.00/4212.00/4206.00/4207.00 ; 4208.00/4208.50/4204.50/4205.50 ; 4206.00/4206.50/4203.00/4204.00 ; 4205.00/4216.00/4204.50/4215.50 | UP | 4 | shape ✔ · formed ✔ | — | Middle bar high exactly H1 (4212.00): passes (H<=H1). |
| `B02` | 4200.00/4212.00/4199.00/4211.00 ; 4210.00/4212.01/4206.00/4207.00 ; 4208.00/4208.50/4204.50/4205.50 ; 4206.00/4206.50/4203.00/4204.00 ; 4205.00/4216.00/4204.50/4215.50 | UP | 4 | no shape | bar2 H<=H1 | Middle bar high 4212.01: fails only that clause. |
| `B03` | 4200.00/4212.00/4199.00/4211.00 ; 4210.00/4210.50/4206.00/4207.00 ; 4208.00/4208.50/4204.50/4205.50 ; 4206.00/4206.50/4199.00/4204.00 ; 4205.00/4216.00/4204.50/4215.50 | UP | 4 | shape ✔ · formed ✔ | — | Middle bar low exactly L1 (4199.00): passes. |
| `B04` | 4200.00/4212.00/4199.00/4211.00 ; 4210.00/4210.50/4206.00/4207.00 ; 4208.00/4208.50/4204.50/4205.50 ; 4206.00/4206.50/4198.99/4204.00 ; 4205.00/4216.00/4204.50/4215.50 | UP | 4 | no shape | bar4 L>=L1 | Middle bar low 4198.99: fails only that clause. |
| `B05` | 4200.00/4212.00/4199.00/4211.00 ; 4210.00/4210.50/4206.00/4207.00 ; 4210.00/4210.20/4204.00/4204.50 ; 4206.00/4206.50/4203.00/4204.00 ; 4205.00/4216.00/4204.50/4215.50 | UP | 4 | shape ✔ · formed ✔ | — | Middle body exactly 0.5*B1 (5.50): passes. |
| `B06` | 4200.00/4212.00/4199.00/4211.00 ; 4210.00/4210.50/4206.00/4207.00 ; 4210.01/4210.20/4204.00/4204.50 ; 4206.00/4206.50/4203.00/4204.00 ; 4205.00/4216.00/4204.50/4215.50 | UP | 4 | no shape | bar3 B<=0.5B1 | Middle body 5.51: fails only that clause. |
| `B07` | 4200.00/4212.00/4199.00/4211.00 ; 4210.00/4210.50/4206.00/4207.00 ; 4208.00/4208.50/4204.50/4205.50 ; 4206.00/4206.50/4203.00/4204.00 ; 4205.00/4211.60/4204.50/4211.00 | UP | 4 | no shape | C5>C1 | C5 closes exactly at C1's close (4211.00): fails only C5>C1 (strict). |
| `B08` | 4200.00/4212.00/4199.00/4211.00 ; 4210.00/4210.50/4206.00/4207.00 ; 4208.00/4208.50/4204.50/4205.50 ; 4206.00/4206.50/4203.00/4204.00 ; 4205.00/4211.60/4204.50/4211.01 | UP | 4 | shape ✔ · formed ✔ | — | C5 closes 0.01 above C1's close: passes. |
| `F01` | 4200.00/4212.00/4199.00/4211.00 ; 4210.00/4210.50/4206.00/4207.00 ; 4208.00/4208.50/4204.50/4205.50 ; 4206.00/4206.50/4203.00/4204.00 ; 4205.00/4216.00/4204.50/4215.50 | UP | 4 | shape ✔ · formed ✔ | — | All middle closes (4207, 4205.5, 4204) lie within C1's body [4200, 4211]: flag true. |
| `F02` | 4200.00/4212.00/4199.00/4211.00 ; 4211.50/4211.60/4208.00/4211.01 ; 4208.00/4208.50/4204.50/4205.50 ; 4206.00/4206.50/4203.00/4204.00 ; 4205.00/4216.00/4204.50/4215.50 | UP | 4 | shape ✔ · formed ✔ | — | Middle close 4211.01 is above C1's close 4211.00: flag false, pattern still forms (canonical rule uses full high-low containment). |
| `N01` | 4200.00/4212.00/4199.00/4211.00 ; 4210.00/4210.50/4206.00/4207.00 ; 4205.50/4208.50/4204.50/4208.00 ; 4206.00/4206.50/4203.00/4204.00 ; 4205.00/4216.00/4204.50/4215.50 | UP | 4 | no shape | bar3 bear | A bullish middle candle (bar 3) breaks the alternation: fails colour. |
| `N02` | 4200.00/4212.00/4199.00/4211.00 ; 4210.00/4210.50/4206.00/4207.00 ; 4208.00/4208.50/4204.50/4205.50 ; 4206.00/4206.50/4203.00/4204.00 ; 4205.00/4211.60/4204.50/4207.00 | UP | 4 | no shape | LARGE(C5), C5>C1 | C5 is not LARGE: fails LARGE(C5) (and C5>C1). |
| `NZ1` | 4200.00/4204.50/4199.50/4204.00 ; 4204.00/4208.50/4203.50/4208.00 ; 4208.00/4212.50/4207.50/4212.00 ; 4212.00/4216.50/4211.50/4216.00 ; 4216.00/4220.50/4215.50/4220.00 | UP | 4 | canonical: no event; variant: no event | — | Five bullish candles: the middle three must be bearish and contained. |
| `T01` | 4200.00/4212.00/4199.00/4211.00 ; 4210.00/4210.50/4206.00/4207.00 ; 4208.00/4208.50/4204.50/4205.50 ; 4206.00/4206.50/4203.00/4204.00 ; 4205.00/4216.00/4204.50/4215.50 | DOWN | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Rising Three Methods shape after DOWN: not formed. |
| `T02` | 4200.00/4212.00/4199.00/4211.00 ; 4210.00/4210.50/4206.00/4207.00 ; 4208.00/4208.50/4204.50/4205.50 ; 4206.00/4206.50/4203.00/4204.00 ; 4205.00/4216.00/4204.50/4215.50 | RANGE | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Rising Three Methods shape after RANGE: not formed. |
| `T03` | 4200.00/4212.00/4199.00/4211.00 ; 4210.00/4210.50/4206.00/4207.00 ; 4208.00/4208.50/4204.50/4205.50 ; 4206.00/4206.50/4203.00/4204.00 ; 4205.00/4216.00/4204.50/4215.50 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Rising Three Methods shape after UNDETERMINED: not formed. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 11:15:02 4215.50/4215.70; 09-16 11:17:00 4223.95/4224.15; 09-16 11:20:00 4249.50/4249.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4215.70; stop: 4198.80; R: 16.90; target(s): 4249.50; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 11:15:02 4215.50/4215.70; 09-16 11:17:00 4207.05/4207.25; 09-16 11:20:00 4198.80/4199.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4215.70; stop: 4198.80; R: 16.90; target(s): 4249.50; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4196.80 < stop): fill = that tick's bid, not the stop (G9): -189/169R. | 09-16 11:15:02 4215.50/4215.70; 09-16 11:17:00 4196.80/4197.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4215.70; stop: 4198.80; R: 16.90; target(s): 4249.50; exit: STOP net -189/169 (≈-1.1183)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 11:15:02 4215.50/4215.70; 09-16 11:16:40 4198.80/4199.00; 09-16 11:18:20 4249.50/4249.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4215.70; stop: 4198.80; R: 16.90; target(s): 4249.50; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 11:15:02 4215.50/4215.70; 09-16 11:16:40 4249.50/4249.70; 09-16 11:18:20 4198.80/4199.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4215.70; stop: 4198.80; R: 16.90; target(s): 4249.50; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 11:15:02 4215.50/4215.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4215.70; stop: 4198.80; R: 16.90; target(s): 4249.50; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 11:15:02 4215.50/4216.00; 09-16 11:18:20 4250.40/4250.90 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4216.00; stop: 4198.80; R: 17.20; target(s): 4250.40; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 11:30:00 4215.50/4215.70; 09-16 11:31:40 4249.50/4249.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4215.70; stop: 4198.80; R: 16.90; target(s): 4249.50; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 11:30:01 4215.50/4215.70; 09-16 11:31:40 4249.50/4249.70 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 11:15:02 4200.30/4200.80; 09-16 11:16:40 4204.80/4205.30 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.80; R: 2.00; target(s): 4204.80; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 11:15:02 4200.29/4200.79; 09-16 11:16:40 4204.79/4205.29 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4255.90 > target 4249.50): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 11:15:02 4215.50/4215.70; 09-16 11:17:00 4255.90/4256.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4215.70; stop: 4198.80; R: 16.90; target(s): 4249.50; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4215.50/4215.70; 09-21 00:30:00 4249.50/4249.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4215.70; stop: 4198.80; R: 16.90; target(s): 4249.50; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4215.50/4215.70; 09-21 00:30:00 4249.50/4249.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4215.70; stop: 4198.80; R: 16.90; target(s): 4249.50; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4215.50/4215.70 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P20-R01` · `GT-RISING3-BULL-v1.0/BASE` · M15
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4212.00 | 4199.00 | 4211.00 |
| 2 | 09-16 10:15 | 4210.00 | 4210.50 | 4206.00 | 4207.00 |
| 3 | 09-16 10:30 | 4208.00 | 4208.50 | 4204.50 | 4205.50 |
| 4 | 09-16 10:45 | 4206.00 | 4206.50 | 4203.00 | 4204.00 |
| 5 | 09-16 11:00 | 4205.00 | 4216.00 | 4204.50 | 4215.50 |
| 6 | 09-16 11:15 | 4215.50 | 4218.50 | 4213.50 | 4216.50 |
| 7 | 09-16 11:30 | 4216.50 | 4219.50 | 4214.50 | 4217.50 |
| 8 | 09-16 11:45 | 4217.50 | 4218.50 | 4212.50 | 4214.50 |
| 9 | 09-16 12:00 | 4214.50 | 4217.50 | 4211.50 | 4215.50 |
| 10 | 09-16 12:15 | 4216.50 | 4220.50 | 4213.50 | 4218.50 |
| 11 | 09-16 12:30 | 4218.50 | 4224.50 | 4206.50 | 4219.50 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4215.50 | h1: ret=1.00, mfe=3.00, mae=-2.00, end_index=5 | h3: ret=-1.00, mfe=4.00, mae=-3.00, end_index=7 | h5: ret=3.00, mfe=5.00, mae=-4.00, end_index=9 | h10: NULL | h20: NULL

#### `GV-P20-V00` · `GT-RISING3-BULL-v1.0/BASE` · M15
> BASE on the tall-C1 carrier: stop = min(L1..L5) - 0.20 = 4198.80 (far).

Tags: base-vs-source
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4230.00 | 4199.00 | 4229.00 |
| 2 | 09-16 10:15 | 4228.00 | 4229.00 | 4222.00 | 4223.00 |
| 3 | 09-16 10:30 | 4224.00 | 4225.00 | 4219.00 | 4220.00 |
| 4 | 09-16 10:45 | 4221.00 | 4222.00 | 4218.00 | 4219.00 |
| 5 | 09-16 11:00 | 4219.00 | 4230.00 | 4218.50 | 4229.50 |

Ticks (bid/ask): 09-16 11:15:02 4230.00/4230.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4230.20
- stop: 4198.80

#### `GV-P20-Y01` · `GT-RISING3-BULL-v1.0/BASE` · M15
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4212.00 | 4199.00 | 4211.00 |
| 2 | 09-16 10:15 | 4210.00 | 4210.50 | 4206.00 | 4207.00 |
| 3 | 09-16 10:30 | 4208.00 | 4208.50 | 4204.50 | 4205.50 |
| 4 | 09-16 10:45 | 4206.00 | 4206.50 | 4203.00 | 4204.00 |
| 5 | 09-16 11:00 | 4205.00 | 4216.00 | 4204.50 | 4215.50 |

Ticks (bid/ask): 09-16 11:15:02 4215.50/4215.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T11:15:00Z
- entry: 4215.70
- stop: 4198.80
- R: 16.90
- target(s): 4249.50

### Variant `SRC-PS`

#### `GV-P20-V01` · `GT-RISING3-BULL-v1.0/SRC-PS` · M15
> SRC-PS Rising Three: stop = min(L2,L3,L4) - 0.20 = 4217.80; TP1 = P + 1.272*(H1-L1) with P = min(L2..L4) = 4218.00 -> 4218.00 + 1.272*31.00 = 4257.432; entry ask 4231.01; R 13.21; reward 26.422 vs 2R = 26.42 -> passes by 0.002 (just inside).

Tags: variant, fib-target, boundary
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4230.00 | 4199.00 | 4229.00 |
| 2 | 09-16 10:15 | 4228.00 | 4229.00 | 4222.00 | 4223.00 |
| 3 | 09-16 10:30 | 4224.00 | 4225.00 | 4219.00 | 4220.00 |
| 4 | 09-16 10:45 | 4221.00 | 4222.00 | 4218.00 | 4219.00 |
| 5 | 09-16 11:00 | 4219.00 | 4230.00 | 4218.50 | 4229.50 |

Ticks (bid/ask): 09-16 11:15:02 4230.81/4231.01; 09-16 11:16:40 4257.44/4257.64

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4231.01
- stop: 4217.80
- R: 13.21
- target(s): 4257.432
- exit: TARGET net 13211/6605 (≈2.0002)R

#### `GV-P20-V02` · `GT-RISING3-BULL-v1.0/SRC-PS` · M15
> Entry ask 4231.02: R 13.22, 2R = 26.44 > 26.412 available -> SKIPPED_SRC_RR (just outside).

Tags: fib-target, boundary, insufficient-rr
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4230.00 | 4199.00 | 4229.00 |
| 2 | 09-16 10:15 | 4228.00 | 4229.00 | 4222.00 | 4223.00 |
| 3 | 09-16 10:30 | 4224.00 | 4225.00 | 4219.00 | 4220.00 |
| 4 | 09-16 10:45 | 4221.00 | 4222.00 | 4218.00 | 4219.00 |
| 5 | 09-16 11:00 | 4219.00 | 4230.00 | 4218.50 | 4229.50 |

Ticks (bid/ask): 09-16 11:15:02 4230.82/4231.02

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR

#### `GV-P20-V03` · `GT-RISING3-BULL-v1.0/SRC-PS` · M15
> Original textbook bars: TP1 = 4203.00 + 1.272*13 = 4219.536 is only 3.84 above the entry 4215.70 (0.30R) -> SKIPPED_SRC_RR.

Tags: fib-target, insufficient-rr
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4212.00 | 4199.00 | 4211.00 |
| 2 | 09-16 10:15 | 4210.00 | 4210.50 | 4206.00 | 4207.00 |
| 3 | 09-16 10:30 | 4208.00 | 4208.50 | 4204.50 | 4205.50 |
| 4 | 09-16 10:45 | 4206.00 | 4206.50 | 4203.00 | 4204.00 |
| 5 | 09-16 11:00 | 4205.00 | 4216.00 | 4204.50 | 4215.50 |

Ticks (bid/ask): 09-16 11:15:02 4215.50/4215.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR

#### `GV-P20-V04` · `GT-RISING3-BULL-v1.0/SRC-PS` · M15 · **PROVISIONAL**
> Entry ask 4220.00 is ABOVE TP1 4219.536: target behind the entry -> SKIPPED_TARGET_ALREADY_PASSED (checked before the 2R test). [PROVISIONAL precedence, A-19]

Tags: fib-target, target-already-passed
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4212.00 | 4199.00 | 4211.00 |
| 2 | 09-16 10:15 | 4210.00 | 4210.50 | 4206.00 | 4207.00 |
| 3 | 09-16 10:30 | 4208.00 | 4208.50 | 4204.50 | 4205.50 |
| 4 | 09-16 10:45 | 4206.00 | 4206.50 | 4203.00 | 4204.00 |
| 5 | 09-16 11:00 | 4205.00 | 4216.00 | 4204.50 | 4215.50 |

Ticks (bid/ask): 09-16 11:15:02 4219.80/4220.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_TARGET_ALREADY_PASSED

#### `GV-P20-V05` · `GT-RISING3-BULL-v1.0/SRC-PS` · M15
> A middle bar closes above C1's close (4229.50 > 4229.00): body-close flag false. The RISING source variant does NOT require the flag -> trades.

Tags: asymmetry, close-rule
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4230.00 | 4199.00 | 4229.00 |
| 2 | 09-16 10:15 | 4229.90 | 4230.00 | 4222.00 | 4229.50 |
| 3 | 09-16 10:30 | 4224.00 | 4225.00 | 4219.00 | 4220.00 |
| 4 | 09-16 10:45 | 4221.00 | 4222.00 | 4218.00 | 4219.00 |
| 5 | 09-16 11:00 | 4219.00 | 4230.00 | 4218.50 | 4229.50 |

Ticks (bid/ask): 09-16 11:15:02 4230.81/4231.01

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- flags: closes_in_body=False
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4231.01
- stop: 4217.80
- R: 13.21
- target(s): 4257.432

