# P09 Inside Bar Breakout — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.2.2 · vector pack GV-0.1 · **80 vectors** (2 dormant, 70 firm, 8 provisional)

Strategies covered: `GT-INSIDE-BEAR-v1.0`, `GT-INSIDE-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-INSIDE-BEAR-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01m` | 4200.00/4202.00/4190.00/4192.00 ; 4196.00/4199.00/4190.00/4195.00 | UP | 4 | no shape | (1 clause) | Inside high equals mother high exactly: not strictly inside -> fails H2<H1 only. |
| `B02m` | 4200.00/4202.00/4190.00/4192.00 ; 4196.00/4202.00/4193.00/4195.00 | UP | 4 | no shape | (1 clause) | Inside low equals mother low exactly -> fails L2>L1 only. |
| `B03m` | 4200.00/4202.00/4190.00/4192.00 ; 4196.00/4201.99/4190.01/4195.00 | UP | 4 | shape ✔ · formed ✔ | — | Inside bar 0.01 inside on both sides -> passes. |
| `B04m` | 4200.00/4202.00/4190.00/4192.00 ; 4196.00/4204.00/4188.00/4195.00 | UP | 4 | no shape | (2 clause) | Second bar is an outside bar: both clauses fail. |
| `NZ1m` | 4200.00/4202.00/4196.00/4197.00 ; 4197.00/4198.00/4193.00/4194.00 | UP | 4 | canonical: no event; variant: no event | — | Second bar is not inside the first (higher high). |
| `S03m` | 4200.00/4202.00/4190.00/4192.00 ; 4196.00/4199.00/4193.00/4195.00 ; 4194.00/4197.00/4191.00/4194.00 ; 4194.00/4196.50/4190.50/4193.00 ; 4193.00/4196.00/4190.10/4192.00 | UP | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED; disposition: EXPIRED_NO_CONFIRMATION | — | Bars 3, 4 and 5 all close inside the mother range: expires with EXPIRED_NO_CONFIRMATION. The base pattern was still FORMED (formation is logged whether or not anything trades). |
| `S05m` | 4200.00/4202.00/4190.00/4192.00 ; 4196.00/4199.00/4193.00/4195.00 ; 4194.00/4197.00/4191.00/4194.00 ; 4194.00/4196.50/4190.50/4193.00 ; 4193.00/4196.00/4190.10/4192.00 ; 4192.00/4192.50/4187.00/4188.00 | UP | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED; disposition: EXPIRED_NO_CONFIRMATION | — | The breakout close arrives on bar 6: too late (window is bars 3-5) -> EXPIRED_NO_CONFIRMATION even though bar 6 breaks out. |
| `S07m` | 4200.00/4202.00/4190.00/4192.00 ; 4196.00/4199.00/4193.00/4195.00 ; 4194.00/4204.00/4193.00/4203.00 | UP | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED | — | Bearish breakout (close 4197 < L1) seen by the BULLISH strategy: no bullish signal. [PROVISIONAL: the spec does not say whether the bull strategy logs a disposition here or whether BASE_PATTERN_FORMED is credited to a side at all - see ambiguity A-09.] |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01m` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:45:02 4188.80/4189.00; 09-16 10:47:00 4182.10/4182.30; 09-16 10:50:00 4161.80/4162.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4202.20; R: 13.40; target(s): 4162.00; exit: TARGET net 2.00R |
| `L02m` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:45:02 4188.80/4189.00; 09-16 10:47:00 4195.50/4195.70; 09-16 10:50:00 4202.00/4202.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4202.20; R: 13.40; target(s): 4162.00; exit: STOP net -1.00R |
| `L03m` | Tick gaps through the stop (bid 4195.80 < stop): fill = that tick's bid, not the stop (G9): -77/67R. | 09-16 10:45:02 4188.80/4189.00; 09-16 10:47:00 4204.00/4204.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4202.20; R: 13.40; target(s): 4162.00; exit: STOP net -77/67 (≈-1.1493)R |
| `L04m` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:45:02 4188.80/4189.00; 09-16 10:46:40 4202.00/4202.20; 09-16 10:48:20 4161.80/4162.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4202.20; R: 13.40; target(s): 4162.00; exit: STOP net -1.00R |
| `L05m` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:45:02 4188.80/4189.00; 09-16 10:46:40 4161.80/4162.00; 09-16 10:48:20 4202.00/4202.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4202.20; R: 13.40; target(s): 4162.00; exit: TARGET net 2.00R |
| `L06m` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:45:02 4188.80/4189.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4202.20; R: 13.40; target(s): 4162.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07m` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:45:02 4188.50/4189.00; 09-16 10:48:20 4160.60/4161.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.50; stop: 4202.20; R: 13.70; target(s): 4161.10; exit: TARGET net 2.00R |
| `L08m` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 11:00:00 4188.80/4189.00; 09-16 11:01:40 4161.80/4162.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4202.20; R: 13.40; target(s): 4162.00; exit: TARGET net 2.00R |
| `L09m` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 11:00:01 4188.80/4189.00; 09-16 11:01:40 4161.80/4162.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10m` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:45:02 4200.20/4200.70; 09-16 10:46:40 4195.70/4196.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.20; R: 2.00; target(s): 4196.20; exit: TARGET net 2.00R |
| `L11m` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:45:02 4200.21/4200.71; 09-16 10:46:40 4195.71/4196.21 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12m` | Tick jumps far past the target (bid 4244.40 > target 4238.00): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:45:02 4188.80/4189.00; 09-16 10:47:00 4155.40/4155.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4188.80; stop: 4202.20; R: 13.40; target(s): 4162.00; exit: TARGET net 2.00R |
| `W01m` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4188.80/4189.00; 09-21 00:30:00 4161.80/4162.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4188.80; stop: 4202.20; R: 13.40; target(s): 4162.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W02m` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4188.80/4189.00; 09-21 00:30:00 4161.80/4162.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4188.80; stop: 4202.20; R: 13.40; target(s): 4162.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W03m` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4188.80/4189.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P09-R01m` · `GT-INSIDE-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P09-R01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 10:15 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 10:30 | 4194.00 | 4195.00 | 4188.00 | 4189.00 |
| 4 | 09-16 10:45 | 4189.00 | 4191.00 | 4186.00 | 4188.00 |
| 5 | 09-16 11:00 | 4188.00 | 4190.00 | 4185.00 | 4187.00 |
| 6 | 09-16 11:15 | 4187.00 | 4192.00 | 4186.00 | 4190.00 |
| 7 | 09-16 11:30 | 4190.00 | 4193.00 | 4187.00 | 4189.00 |
| 8 | 09-16 11:45 | 4188.00 | 4191.00 | 4184.00 | 4186.00 |
| 9 | 09-16 12:00 | 4186.00 | 4198.00 | 4180.00 | 4185.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4189.00 | h1: ret=1.00, mfe=3.00, mae=-2.00, end_index=3 | h3: ret=-1.00, mfe=4.00, mae=-3.00, end_index=5 | h5: ret=3.00, mfe=5.00, mae=-4.00, end_index=7 | h10: NULL | h20: NULL

#### `GV-P09-S01m` · `GT-INSIDE-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P09-S01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Bar 3 closes exactly ON the mother high (4210.00): not outside (close > H1 required) so it stays armed; bar 4 closes 4210.01 -> signal at bar 4 completion (11:00). Stop = L1-0.20 = 4197.80.

Tags: breakout
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 10:15 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 10:30 | 4194.00 | 4195.00 | 4189.50 | 4190.00 |
| 4 | 09-16 10:45 | 4190.00 | 4190.50 | 4188.00 | 4189.99 |

Ticks (bid/ask): 09-16 11:00:02 4189.30/4189.50

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T11:00:00Z
- entry: 4189.30
- stop: 4202.20
- R: 12.90
- target(s): 4163.50

#### `GV-P09-S02m` · `GT-INSIDE-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P09-S02` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Bar 3 pokes above the mother high (H 4211) but CLOSES inside (4209): not a breakout; stays armed. Bar 4 closes at 4211 -> signal at 11:00.

Tags: breakout
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 10:15 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 10:30 | 4194.00 | 4195.00 | 4189.00 | 4191.00 |
| 4 | 09-16 10:45 | 4191.00 | 4191.50 | 4187.00 | 4189.00 |

Ticks (bid/ask): 09-16 11:00:02 4189.30/4189.50

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T11:00:00Z
- stop: 4202.20

#### `GV-P09-S04m` · `GT-INSIDE-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P09-S04` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Breakout close arrives on bar 5 (the last allowed bar): signal at bar 5 completion (11:15).

Tags: breakout
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 10:15 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 10:30 | 4194.00 | 4197.00 | 4191.00 | 4194.00 |
| 4 | 09-16 10:45 | 4194.00 | 4196.50 | 4190.50 | 4193.00 |
| 5 | 09-16 11:00 | 4193.00 | 4194.00 | 4188.00 | 4189.00 |

Ticks (bid/ask): 09-16 11:15:02 4189.30/4189.50

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T11:15:00Z
- stop: 4202.20

#### `GV-P09-S06m` · `GT-INSIDE-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P09-S06` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Bar 3 pokes BOTH sides of the mother range but closes inside: not a breakout; bar 4 closes above -> signal at bar 4.

Tags: breakout
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 10:15 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 10:30 | 4194.00 | 4205.00 | 4188.00 | 4191.00 |
| 4 | 09-16 10:45 | 4191.00 | 4191.50 | 4187.00 | 4189.00 |

Ticks (bid/ask): 09-16 11:00:02 4189.30/4189.50

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T11:00:00Z
- stop: 4202.20

#### `GV-P09-T01m` · `GT-INSIDE-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P09-T01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Inside Bar: no prior-state requirement (trend UP).

Tags: no-prior-state
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 10:15 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 10:30 | 4194.00 | 4195.00 | 4188.00 | 4189.00 |

Ticks (bid/ask): 09-16 10:45:02 4188.80/4189.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE

#### `GV-P09-T02m` · `GT-INSIDE-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P09-T02` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Inside Bar: no prior-state requirement (trend RANGE).

Tags: no-prior-state
Context: atr=4 · trend=RANGE

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 10:15 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 10:30 | 4194.00 | 4195.00 | 4188.00 | 4189.00 |

Ticks (bid/ask): 09-16 10:45:02 4188.80/4189.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE

#### `GV-P09-T03m` · `GT-INSIDE-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P09-T03` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Inside Bar: no prior-state requirement (trend DOWN).

Tags: no-prior-state
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 10:15 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 10:30 | 4194.00 | 4195.00 | 4188.00 | 4189.00 |

Ticks (bid/ask): 09-16 10:45:02 4188.80/4189.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE

#### `GV-P09-Y01m` · `GT-INSIDE-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P09-Y01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 10:15 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 10:30 | 4194.00 | 4195.00 | 4188.00 | 4189.00 |

Ticks (bid/ask): 09-16 10:45:02 4188.80/4189.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:45:00Z
- entry: 4188.80
- stop: 4202.20
- R: 13.40
- target(s): 4162.00

### Variant `SRC-CB`

#### `GV-P09-V01m` · `GT-INSIDE-BEAR-v1.0/SRC-CB` · H4 · **PROVISIONAL**
*Mirror of `GV-P09-V01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> SRC-CB Inside Bar breakout (bull) on H4: TREND UP, mother low 4198.00 within 0.10*ATR of a support zone (provisional level reading, A-15), TF H4 allowed. The last H4 bar (19:00) completes at the 22:00 closure start; the first tick after the pause is 23:00:02 (entry_across_break). Stop L1-0.20 = 4197.80; R 13.40; T_SR(2.0) = 4238.00 = exactly 2.0R.

Tags: variant-clean-yes, tf-H4, closure
Context: atr=4 · trend=DOWN · zones_pre=[4202.10-4202.30] · zones_entry=[4161.00-4162.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 11:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 15:00 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 19:00 | 4194.00 | 4195.00 | 4188.00 | 4189.00 |

Ticks (bid/ask): 09-16 23:00:02 4188.80/4189.00; 09-17 01:00:00 4161.80/4162.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T22:00:00Z
- entry: 4188.80
- stop: 4202.20
- R: 13.40
- target(s): 4162.00
- entry_across_break: True
- exit: TARGET net 2.00R

#### `GV-P09-V02m` · `GT-INSIDE-BEAR-v1.0/SRC-CB` · H4
*Mirror of `GV-P09-V02` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Zone edge 4237.99 -> 1.9993R -> SKIPPED_SRC_RR.

Tags: boundary, insufficient-rr
Context: atr=4 · trend=DOWN · zones_pre=[4202.10-4202.30] · zones_entry=[4161.00-4162.01]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 11:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 15:00 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 19:00 | 4194.00 | 4195.00 | 4188.00 | 4189.00 |

Ticks (bid/ask): 09-16 23:00:02 4188.80/4189.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- signal time: 2026-09-16T22:00:00Z

#### `GV-P09-V03m` · `GT-INSIDE-BEAR-v1.0/SRC-CB` · H4
*Mirror of `GV-P09-V03` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Bullish breakout against a DOWN trend: CB requires breakout WITH the trend (bull needs UP) -> not qualified.

Tags: with-trend, variant-not-qualified
Context: atr=4 · trend=UP · zones_pre=[4202.10-4202.30] · zones_entry=[4161.00-4162.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 11:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 15:00 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 19:00 | 4194.00 | 4195.00 | 4188.00 | 4189.00 |

Ticks (bid/ask): 09-16 23:00:02 4188.80/4189.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event

#### `GV-P09-V04m` · `GT-INSIDE-BEAR-v1.0/SRC-CB` · M15 · **PROVISIONAL**
*Mirror of `GV-P09-V04` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> M15 is not in {H4,D1}: SKIPPED_TF_NOT_ALLOWED. [PROVISIONAL A-12]

Tags: tf-gate
Context: atr=4 · trend=DOWN · zones_pre=[4202.10-4202.30] · zones_entry=[4161.00-4162.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 10:15 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 10:30 | 4194.00 | 4195.00 | 4188.00 | 4189.00 |

Ticks (bid/ask): 09-16 10:45:02 4188.80/4189.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: SKIPPED_TF_NOT_ALLOWED

#### `GV-P09-V05m` · `GT-INSIDE-BEAR-v1.0/SRC-CB` · H1 · **PROVISIONAL**
*Mirror of `GV-P09-V05` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> H1 is not allowed for the CB Inside Bar (only H4, D1), unlike the CB Pin Bar and Engulfing. [PROVISIONAL A-12]

Tags: tf-gate
Context: atr=4 · trend=DOWN · zones_pre=[4202.10-4202.30] · zones_entry=[4161.00-4162.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 11:00 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 12:00 | 4194.00 | 4195.00 | 4188.00 | 4189.00 |

Ticks (bid/ask): 09-16 13:00:02 4188.80/4189.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: SKIPPED_TF_NOT_ALLOWED

#### `GV-P09-V06m` · `GT-INSIDE-BEAR-v1.0/SRC-CB` · H4
*Mirror of `GV-P09-V06` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> No zone above the entry -> SKIPPED_SRC_NO_TARGET.

Tags: T_SR, no-target
Context: atr=4 · trend=DOWN · zones_pre=[4202.10-4202.30]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 11:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 15:00 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 19:00 | 4194.00 | 4195.00 | 4188.00 | 4189.00 |

Ticks (bid/ask): 09-16 23:00:02 4188.80/4189.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- signal time: 2026-09-16T22:00:00Z

### Variant `SRC-PS`

#### `GV-P09-DISm` · `GT-INSIDE-BEAR-v1.0/SRC-PS` · M15
> DISABLED_PENDING_PIP_CONFIRMATION (D-032): the BASE pattern forms exactly as in GV-P09-Y01m (canonical events are still logged), but this source variant depends on PIP_SRC_USD, so it emits NO variant events, opens NO trade and has no ledger. The BASE strategy on the same candle is unaffected.

Tags: disabled-variant
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4202.00 | 4190.00 | 4192.00 |
| 2 | 09-16 10:15 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 3 | 09-16 10:30 | 4194.00 | 4195.00 | 4188.00 | 4189.00 |

Ticks (bid/ask): 09-16 10:45:02 4188.80/4189.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant status: DISABLED_PENDING_PIP_CONFIRMATION
- variant: no event

## `GT-INSIDE-BULL-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4200.00/4210.00/4198.00/4208.00 ; 4204.00/4210.00/4201.00/4205.00 | DOWN | 4 | no shape | H2<H1 | Inside high equals mother high exactly: not strictly inside -> fails H2<H1 only. |
| `B02` | 4200.00/4210.00/4198.00/4208.00 ; 4204.00/4207.00/4198.00/4205.00 | DOWN | 4 | no shape | L2>L1 | Inside low equals mother low exactly -> fails L2>L1 only. |
| `B03` | 4200.00/4210.00/4198.00/4208.00 ; 4204.00/4209.99/4198.01/4205.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Inside bar 0.01 inside on both sides -> passes. |
| `B04` | 4200.00/4210.00/4198.00/4208.00 ; 4204.00/4212.00/4196.00/4205.00 | DOWN | 4 | no shape | H2<H1, L2>L1 | Second bar is an outside bar: both clauses fail. |
| `NZ1` | 4200.00/4204.00/4198.00/4203.00 ; 4203.00/4207.00/4202.00/4206.00 | DOWN | 4 | canonical: no event; variant: no event | — | Second bar is not inside the first (higher high). |
| `S03` | 4200.00/4210.00/4198.00/4208.00 ; 4204.00/4207.00/4201.00/4205.00 ; 4206.00/4209.00/4203.00/4206.00 ; 4206.00/4209.50/4203.50/4207.00 ; 4207.00/4209.90/4204.00/4208.00 | DOWN | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED; disposition: EXPIRED_NO_CONFIRMATION | — | Bars 3, 4 and 5 all close inside the mother range: expires with EXPIRED_NO_CONFIRMATION. The base pattern was still FORMED (formation is logged whether or not anything trades). |
| `S05` | 4200.00/4210.00/4198.00/4208.00 ; 4204.00/4207.00/4201.00/4205.00 ; 4206.00/4209.00/4203.00/4206.00 ; 4206.00/4209.50/4203.50/4207.00 ; 4207.00/4209.90/4204.00/4208.00 ; 4208.00/4213.00/4207.50/4212.00 | DOWN | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED; disposition: EXPIRED_NO_CONFIRMATION | — | The breakout close arrives on bar 6: too late (window is bars 3-5) -> EXPIRED_NO_CONFIRMATION even though bar 6 breaks out. |
| `S07` | 4200.00/4210.00/4198.00/4208.00 ; 4204.00/4207.00/4201.00/4205.00 ; 4206.00/4207.00/4196.00/4197.00 | DOWN | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED | — | Bearish breakout (close 4197 < L1) seen by the BULLISH strategy: no bullish signal. [PROVISIONAL: the spec does not say whether the bull strategy logs a disposition here or whether BASE_PATTERN_FORMED is credited to a side at all - see ambiguity A-09.] |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:45:02 4211.00/4211.20; 09-16 10:47:00 4217.70/4217.90; 09-16 10:50:00 4238.00/4238.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4197.80; R: 13.40; target(s): 4238.00; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:45:02 4211.00/4211.20; 09-16 10:47:00 4204.30/4204.50; 09-16 10:50:00 4197.80/4198.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4197.80; R: 13.40; target(s): 4238.00; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4195.80 < stop): fill = that tick's bid, not the stop (G9): -77/67R. | 09-16 10:45:02 4211.00/4211.20; 09-16 10:47:00 4195.80/4196.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4197.80; R: 13.40; target(s): 4238.00; exit: STOP net -77/67 (≈-1.1493)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:45:02 4211.00/4211.20; 09-16 10:46:40 4197.80/4198.00; 09-16 10:48:20 4238.00/4238.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4197.80; R: 13.40; target(s): 4238.00; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:45:02 4211.00/4211.20; 09-16 10:46:40 4238.00/4238.20; 09-16 10:48:20 4197.80/4198.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4197.80; R: 13.40; target(s): 4238.00; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:45:02 4211.00/4211.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4197.80; R: 13.40; target(s): 4238.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:45:02 4211.00/4211.50; 09-16 10:48:20 4238.90/4239.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.50; stop: 4197.80; R: 13.70; target(s): 4238.90; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 11:00:00 4211.00/4211.20; 09-16 11:01:40 4238.00/4238.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4197.80; R: 13.40; target(s): 4238.00; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 11:00:01 4211.00/4211.20; 09-16 11:01:40 4238.00/4238.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:45:02 4199.30/4199.80; 09-16 10:46:40 4203.80/4204.30 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.80; R: 2.00; target(s): 4203.80; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:45:02 4199.29/4199.79; 09-16 10:46:40 4203.79/4204.29 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4244.40 > target 4238.00): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:45:02 4211.00/4211.20; 09-16 10:47:00 4244.40/4244.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4211.20; stop: 4197.80; R: 13.40; target(s): 4238.00; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4211.00/4211.20; 09-21 00:30:00 4238.00/4238.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4211.20; stop: 4197.80; R: 13.40; target(s): 4238.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4211.00/4211.20; 09-21 00:30:00 4238.00/4238.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4211.20; stop: 4197.80; R: 13.40; target(s): 4238.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4211.00/4211.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P09-R01` · `GT-INSIDE-BULL-v1.0/BASE` · M15
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 10:15 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 10:30 | 4206.00 | 4212.00 | 4205.00 | 4211.00 |
| 4 | 09-16 10:45 | 4211.00 | 4214.00 | 4209.00 | 4212.00 |
| 5 | 09-16 11:00 | 4212.00 | 4215.00 | 4210.00 | 4213.00 |
| 6 | 09-16 11:15 | 4213.00 | 4214.00 | 4208.00 | 4210.00 |
| 7 | 09-16 11:30 | 4210.00 | 4213.00 | 4207.00 | 4211.00 |
| 8 | 09-16 11:45 | 4212.00 | 4216.00 | 4209.00 | 4214.00 |
| 9 | 09-16 12:00 | 4214.00 | 4220.00 | 4202.00 | 4215.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4211.00 | h1: ret=1.00, mfe=3.00, mae=-2.00, end_index=3 | h3: ret=-1.00, mfe=4.00, mae=-3.00, end_index=5 | h5: ret=3.00, mfe=5.00, mae=-4.00, end_index=7 | h10: NULL | h20: NULL

#### `GV-P09-S01` · `GT-INSIDE-BULL-v1.0/BASE` · M15
> Bar 3 closes exactly ON the mother high (4210.00): not outside (close > H1 required) so it stays armed; bar 4 closes 4210.01 -> signal at bar 4 completion (11:00). Stop = L1-0.20 = 4197.80.

Tags: breakout
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 10:15 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 10:30 | 4206.00 | 4210.50 | 4205.00 | 4210.00 |
| 4 | 09-16 10:45 | 4210.00 | 4212.00 | 4209.50 | 4210.01 |

Ticks (bid/ask): 09-16 11:00:02 4210.50/4210.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T11:00:00Z
- entry: 4210.70
- stop: 4197.80
- R: 12.90
- target(s): 4236.50

#### `GV-P09-S02` · `GT-INSIDE-BULL-v1.0/BASE` · M15
> Bar 3 pokes above the mother high (H 4211) but CLOSES inside (4209): not a breakout; stays armed. Bar 4 closes at 4211 -> signal at 11:00.

Tags: breakout
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 10:15 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 10:30 | 4206.00 | 4211.00 | 4205.00 | 4209.00 |
| 4 | 09-16 10:45 | 4209.00 | 4213.00 | 4208.50 | 4211.00 |

Ticks (bid/ask): 09-16 11:00:02 4210.50/4210.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T11:00:00Z
- stop: 4197.80

#### `GV-P09-S04` · `GT-INSIDE-BULL-v1.0/BASE` · M15
> Breakout close arrives on bar 5 (the last allowed bar): signal at bar 5 completion (11:15).

Tags: breakout
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 10:15 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 10:30 | 4206.00 | 4209.00 | 4203.00 | 4206.00 |
| 4 | 09-16 10:45 | 4206.00 | 4209.50 | 4203.50 | 4207.00 |
| 5 | 09-16 11:00 | 4207.00 | 4212.00 | 4206.00 | 4211.00 |

Ticks (bid/ask): 09-16 11:15:02 4210.50/4210.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T11:15:00Z
- stop: 4197.80

#### `GV-P09-S06` · `GT-INSIDE-BULL-v1.0/BASE` · M15
> Bar 3 pokes BOTH sides of the mother range but closes inside: not a breakout; bar 4 closes above -> signal at bar 4.

Tags: breakout
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 10:15 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 10:30 | 4206.00 | 4212.00 | 4195.00 | 4209.00 |
| 4 | 09-16 10:45 | 4209.00 | 4213.00 | 4208.50 | 4211.00 |

Ticks (bid/ask): 09-16 11:00:02 4210.50/4210.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T11:00:00Z
- stop: 4197.80

#### `GV-P09-T01` · `GT-INSIDE-BULL-v1.0/BASE` · M15
> Inside Bar: no prior-state requirement (trend UP).

Tags: no-prior-state
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 10:15 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 10:30 | 4206.00 | 4212.00 | 4205.00 | 4211.00 |

Ticks (bid/ask): 09-16 10:45:02 4211.00/4211.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE

#### `GV-P09-T02` · `GT-INSIDE-BULL-v1.0/BASE` · M15
> Inside Bar: no prior-state requirement (trend RANGE).

Tags: no-prior-state
Context: atr=4 · trend=RANGE

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 10:15 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 10:30 | 4206.00 | 4212.00 | 4205.00 | 4211.00 |

Ticks (bid/ask): 09-16 10:45:02 4211.00/4211.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE

#### `GV-P09-T03` · `GT-INSIDE-BULL-v1.0/BASE` · M15
> Inside Bar: no prior-state requirement (trend DOWN).

Tags: no-prior-state
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 10:15 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 10:30 | 4206.00 | 4212.00 | 4205.00 | 4211.00 |

Ticks (bid/ask): 09-16 10:45:02 4211.00/4211.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE

#### `GV-P09-Y01` · `GT-INSIDE-BULL-v1.0/BASE` · M15
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 10:15 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 10:30 | 4206.00 | 4212.00 | 4205.00 | 4211.00 |

Ticks (bid/ask): 09-16 10:45:02 4211.00/4211.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:45:00Z
- entry: 4211.20
- stop: 4197.80
- R: 13.40
- target(s): 4238.00

### Variant `SRC-CB`

#### `GV-P09-V01` · `GT-INSIDE-BULL-v1.0/SRC-CB` · H4 · **PROVISIONAL**
> SRC-CB Inside Bar breakout (bull) on H4: TREND UP, mother low 4198.00 within 0.10*ATR of a support zone (provisional level reading, A-15), TF H4 allowed. The last H4 bar (19:00) completes at the 22:00 closure start; the first tick after the pause is 23:00:02 (entry_across_break). Stop L1-0.20 = 4197.80; R 13.40; T_SR(2.0) = 4238.00 = exactly 2.0R.

Tags: variant-clean-yes, tf-H4, closure
Context: atr=4 · trend=UP · zones_pre=[4197.70-4197.90] · zones_entry=[4238.00-4239.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 11:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 15:00 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 19:00 | 4206.00 | 4212.00 | 4205.00 | 4211.00 |

Ticks (bid/ask): 09-16 23:00:02 4211.00/4211.20; 09-17 01:00:00 4238.00/4238.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T22:00:00Z
- entry: 4211.20
- stop: 4197.80
- R: 13.40
- target(s): 4238.00
- entry_across_break: True
- exit: TARGET net 2.00R

#### `GV-P09-V02` · `GT-INSIDE-BULL-v1.0/SRC-CB` · H4
> Zone edge 4237.99 -> 1.9993R -> SKIPPED_SRC_RR.

Tags: boundary, insufficient-rr
Context: atr=4 · trend=UP · zones_pre=[4197.70-4197.90] · zones_entry=[4237.99-4239.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 11:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 15:00 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 19:00 | 4206.00 | 4212.00 | 4205.00 | 4211.00 |

Ticks (bid/ask): 09-16 23:00:02 4211.00/4211.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- signal time: 2026-09-16T22:00:00Z

#### `GV-P09-V03` · `GT-INSIDE-BULL-v1.0/SRC-CB` · H4
> Bullish breakout against a DOWN trend: CB requires breakout WITH the trend (bull needs UP) -> not qualified.

Tags: with-trend, variant-not-qualified
Context: atr=4 · trend=DOWN · zones_pre=[4197.70-4197.90] · zones_entry=[4238.00-4239.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 11:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 15:00 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 19:00 | 4206.00 | 4212.00 | 4205.00 | 4211.00 |

Ticks (bid/ask): 09-16 23:00:02 4211.00/4211.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event

#### `GV-P09-V04` · `GT-INSIDE-BULL-v1.0/SRC-CB` · M15 · **PROVISIONAL**
> M15 is not in {H4,D1}: SKIPPED_TF_NOT_ALLOWED. [PROVISIONAL A-12]

Tags: tf-gate
Context: atr=4 · trend=UP · zones_pre=[4197.70-4197.90] · zones_entry=[4238.00-4239.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 10:15 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 10:30 | 4206.00 | 4212.00 | 4205.00 | 4211.00 |

Ticks (bid/ask): 09-16 10:45:02 4211.00/4211.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: SKIPPED_TF_NOT_ALLOWED

#### `GV-P09-V05` · `GT-INSIDE-BULL-v1.0/SRC-CB` · H1 · **PROVISIONAL**
> H1 is not allowed for the CB Inside Bar (only H4, D1), unlike the CB Pin Bar and Engulfing. [PROVISIONAL A-12]

Tags: tf-gate
Context: atr=4 · trend=UP · zones_pre=[4197.70-4197.90] · zones_entry=[4238.00-4239.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 11:00 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 12:00 | 4206.00 | 4212.00 | 4205.00 | 4211.00 |

Ticks (bid/ask): 09-16 13:00:02 4211.00/4211.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: SKIPPED_TF_NOT_ALLOWED

#### `GV-P09-V06` · `GT-INSIDE-BULL-v1.0/SRC-CB` · H4
> No zone above the entry -> SKIPPED_SRC_NO_TARGET.

Tags: T_SR, no-target
Context: atr=4 · trend=UP · zones_pre=[4197.70-4197.90]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 11:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 15:00 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 19:00 | 4206.00 | 4212.00 | 4205.00 | 4211.00 |

Ticks (bid/ask): 09-16 23:00:02 4211.00/4211.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- signal time: 2026-09-16T22:00:00Z

### Variant `SRC-PS`

#### `GV-DORM-P09-01` · `GT-INSIDE-BULL-v1.0/SRC-PS` · H1 · **DORMANT**
> DORMANT. Source Inside Bar breakout on H1: stop = opposite mother side - 3.5 pips x $0.10 = 4197.65; R 13.55; T_SR(1.5): 4232.00 = 1.535R.

Tags: dormant, variant
Context: atr=4 · trend=RANGE · zones_entry=[4232.00-4233.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 11:00 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 12:00 | 4206.00 | 4212.00 | 4205.00 | 4211.00 |

Ticks (bid/ask): 09-16 13:00:02 4211.00/4211.20; 09-16 13:01:40 4232.00/4232.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4211.20
- stop: 4197.65
- R: 13.55
- target(s): 4232.00
- exit: TARGET net 416/271 (≈1.5351)R

#### `GV-DORM-P09-02` · `GT-INSIDE-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> M15 not in {H1,H4,D1,W1,MN1}. [PROVISIONAL A-12]

Tags: dormant, tf-gate
Context: atr=4 · trend=RANGE · zones_entry=[4232.00-4233.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 10:15 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 10:30 | 4206.00 | 4212.00 | 4205.00 | 4211.00 |

Ticks (bid/ask): 09-16 10:45:02 4211.00/4211.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: SKIPPED_TF_NOT_ALLOWED

#### `GV-P09-DIS` · `GT-INSIDE-BULL-v1.0/SRC-PS` · M15
> DISABLED_PENDING_PIP_CONFIRMATION (D-032): the BASE pattern forms exactly as in GV-P09-Y01 (canonical events are still logged), but this source variant depends on PIP_SRC_USD, so it emits NO variant events, opens NO trade and has no ledger. The BASE strategy on the same candle is unaffected.

Tags: disabled-variant
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4210.00 | 4198.00 | 4208.00 |
| 2 | 09-16 10:15 | 4204.00 | 4207.00 | 4201.00 | 4205.00 |
| 3 | 09-16 10:30 | 4206.00 | 4212.00 | 4205.00 | 4211.00 |

Ticks (bid/ask): 09-16 10:45:02 4211.00/4211.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant status: DISABLED_PENDING_PIP_CONFIRMATION
- variant: no event

