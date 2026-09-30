# P08 Outside Bar — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.2.2 · vector pack GV-0.1 · **91 vectors** (3 blocked_ambiguity, 88 firm)

Strategies covered: `GT-OUTSIDE-BEAR-v1.0`, `GT-OUTSIDE-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-OUTSIDE-BEAR-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01m` | 4195.00/4198.00/4192.00/4194.00 ; 4196.00/4200.00/4192.00/4193.00 | UP | 4 | no shape | (1 clause) | H2 = H1 exactly (4208.00): not strictly greater -> fails H2>H1 only. |
| `B02m` | 4195.00/4198.00/4192.00/4194.00 ; 4196.00/4200.00/4191.99/4193.00 | UP | 4 | shape ✔ · formed ✔ | — | H2 = H1 + 0.01: passes. |
| `B03m` | 4195.00/4198.00/4192.00/4194.00 ; 4196.00/4198.00/4190.00/4191.00 | UP | 4 | no shape | (1 clause) | L2 = L1 exactly (4202.00): fails L2<L1 only. |
| `B04m` | 4195.00/4198.00/4192.00/4194.00 ; 4196.00/4198.01/4190.00/4191.00 | UP | 4 | shape ✔ · formed ✔ | — | L2 = L1 - 0.01: passes. |
| `B05m` | 4195.00/4198.00/4192.00/4194.00 ; 4194.00/4200.00/4190.00/4194.00 | UP | 4 | no shape | (1 clause) | C2 = O2 (doji close): shape geometry holds but direction is undefined -> no bullish (and no bearish) signal. |
| `B06m` | 4195.00/4198.00/4192.00/4194.00 ; 4191.00/4200.00/4190.00/4196.00 | UP | 4 | no shape | (1 clause) | Bearish outside bar seen by the BULL strategy: geometry passes, direction clause fails. |
| `F01m` | 4195.00/4198.00/4192.00/4194.00 ; 4197.00/4199.00/4191.00/4192.00 | UP | 4 | shape ✔ · formed ✔ | — | R2 = 8.00 >= 6.00: flag big true. |
| `F02m` | 4195.00/4197.00/4193.00/4194.00 ; 4196.00/4198.00/4192.00/4193.00 | UP | 4 | shape ✔ · formed ✔ | — | R2 = 6.00 exactly = 1.5*ATR: flag true (>=). |
| `F03m` | 4195.00/4197.00/4193.00/4194.00 ; 4196.00/4197.99/4192.01/4193.00 | UP | 4 | shape ✔ · formed ✔ | — | R2 = 5.98 < 6.00: flag false; pattern still forms. |
| `N01m` | 4195.00/4198.00/4192.00/4194.00 ; 4196.00/4197.00/4193.00/4194.00 | UP | 4 | no shape | (2 clause) | Inside bar (not outside): both range clauses fail. |
| `NZ1m` | 4200.00/4202.00/4196.00/4197.00 ; 4198.00/4201.00/4197.00/4200.00 | UP | 4 | canonical: no event; variant: no event | — | Second bar sits inside the first: not an outside bar. |
| `T01m` | 4195.00/4198.00/4192.00/4194.00 ; 4196.00/4200.00/4190.00/4191.00 | DOWN | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Outside Bar has no prior-state requirement: formed with trend UP. |
| `T02m` | 4195.00/4198.00/4192.00/4194.00 ; 4196.00/4200.00/4190.00/4191.00 | RANGE | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Outside Bar has no prior-state requirement: formed with trend RANGE. |
| `T03m` | 4195.00/4198.00/4192.00/4194.00 ; 4196.00/4200.00/4190.00/4191.00 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Outside Bar has no prior-state requirement: formed with trend UNDETERMINED. |
| `T04m` | 4195.00/4198.00/4192.00/4194.00 ; 4196.00/4200.00/4190.00/4191.00 | UP | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Outside Bar has no prior-state requirement: formed with trend DOWN. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01m` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:30:02 4190.80/4191.00; 09-16 10:32:00 4186.10/4186.30; 09-16 10:35:00 4171.80/4172.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.80; stop: 4200.20; R: 9.40; target(s): 4172.00; exit: TARGET net 2.00R |
| `L02m` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:30:02 4190.80/4191.00; 09-16 10:32:00 4195.50/4195.70; 09-16 10:35:00 4200.00/4200.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.80; stop: 4200.20; R: 9.40; target(s): 4172.00; exit: STOP net -1.00R |
| `L03m` | Tick gaps through the stop (bid 4197.80 < stop): fill = that tick's bid, not the stop (G9): -57/47R. | 09-16 10:30:02 4190.80/4191.00; 09-16 10:32:00 4202.00/4202.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.80; stop: 4200.20; R: 9.40; target(s): 4172.00; exit: STOP net -57/47 (≈-1.2128)R |
| `L04m` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:30:02 4190.80/4191.00; 09-16 10:31:40 4200.00/4200.20; 09-16 10:33:20 4171.80/4172.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.80; stop: 4200.20; R: 9.40; target(s): 4172.00; exit: STOP net -1.00R |
| `L05m` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:30:02 4190.80/4191.00; 09-16 10:31:40 4171.80/4172.00; 09-16 10:33:20 4200.00/4200.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.80; stop: 4200.20; R: 9.40; target(s): 4172.00; exit: TARGET net 2.00R |
| `L06m` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:30:02 4190.80/4191.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.80; stop: 4200.20; R: 9.40; target(s): 4172.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07m` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:30:02 4190.50/4191.00; 09-16 10:33:20 4170.60/4171.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.50; stop: 4200.20; R: 9.70; target(s): 4171.10; exit: TARGET net 2.00R |
| `L08m` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:45:00 4190.80/4191.00; 09-16 10:46:40 4171.80/4172.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.80; stop: 4200.20; R: 9.40; target(s): 4172.00; exit: TARGET net 2.00R |
| `L09m` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:45:01 4190.80/4191.00; 09-16 10:46:40 4171.80/4172.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10m` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:30:02 4198.20/4198.70; 09-16 10:31:40 4193.70/4194.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4198.20; R: 2.00; target(s): 4194.20; exit: TARGET net 2.00R |
| `L11m` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:30:02 4198.21/4198.71; 09-16 10:31:40 4193.71/4194.21 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12m` | Tick jumps far past the target (bid 4234.40 > target 4228.00): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:30:02 4190.80/4191.00; 09-16 10:32:00 4165.40/4165.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4190.80; stop: 4200.20; R: 9.40; target(s): 4172.00; exit: TARGET net 2.00R |
| `W01m` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4190.80/4191.00; 09-21 00:30:00 4171.80/4172.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4190.80; stop: 4200.20; R: 9.40; target(s): 4172.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W02m` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4190.80/4191.00; 09-21 00:30:00 4171.80/4172.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4190.80; stop: 4200.20; R: 9.40; target(s): 4172.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W03m` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4190.80/4191.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P08-R01m` · `GT-OUTSIDE-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P08-R01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |
| 3 | 09-16 10:30 | 4191.00 | 4193.00 | 4188.00 | 4190.00 |
| 4 | 09-16 10:45 | 4190.00 | 4192.00 | 4187.00 | 4189.00 |
| 5 | 09-16 11:00 | 4189.00 | 4194.00 | 4188.00 | 4192.00 |
| 6 | 09-16 11:15 | 4192.00 | 4195.00 | 4189.00 | 4191.00 |
| 7 | 09-16 11:30 | 4190.00 | 4193.00 | 4186.00 | 4188.00 |
| 8 | 09-16 11:45 | 4188.00 | 4200.00 | 4182.00 | 4187.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4191.00 | h1: ret=1.00, mfe=3.00, mae=-2.00, end_index=2 | h3: ret=-1.00, mfe=4.00, mae=-3.00, end_index=4 | h5: ret=3.00, mfe=5.00, mae=-4.00, end_index=6 | h10: NULL | h20: NULL

#### `GV-P08-Y01m` · `GT-OUTSIDE-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P08-Y01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |

Ticks (bid/ask): 09-16 10:30:02 4190.80/4191.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4190.80
- stop: 4200.20
- R: 9.40
- target(s): 4172.00

### Variant `SRC-PS`

#### `GV-P08-V01m` · `GT-OUTSIDE-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P08-V01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> SRC-PS Outside Bar: R2 = 10 >= 1.5*ATR (6.0) so it qualifies; entry at the ask 4209.20; stop L2-0.20 = 4199.80 (R 9.40); target T_SR(1.5) = near edge of the nearest live zone above the entry (4224.00): 14.80 = 1.57R >= 1.5R -> trade. Target hit: +1.5745R (not 2R).

Tags: variant-clean-yes, T_SR
Context: atr=4 · trend=UP · zones_entry=[4175.00-4176.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |

Ticks (bid/ask): 09-16 10:30:02 4190.80/4191.00; 09-16 10:31:40 4175.80/4176.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4190.80
- stop: 4200.20
- R: 9.40
- target(s): 4176.00
- exit: TARGET net 74/47 (≈1.5745)R

#### `GV-P08-V02m` · `GT-OUTSIDE-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P08-V02` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Same trade stopped out at 4199.80: -1.00R.

Tags: variant, sl-first-ticks
Context: atr=4 · trend=UP · zones_entry=[4175.00-4176.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |

Ticks (bid/ask): 09-16 10:30:02 4190.80/4191.00; 09-16 10:31:40 4200.00/4200.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4190.80
- stop: 4200.20
- R: 9.40
- target(s): 4176.00
- exit: STOP net -1.00R

#### `GV-P08-V03m` · `GT-OUTSIDE-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P08-V03` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Reward exactly 1.5R (zone edge 4223.30, entry 4209.20, R 9.40 -> 14.10 = 1.5R): accepted (skip only if BELOW minR).

Tags: T_SR, boundary
Context: atr=4 · trend=UP · zones_entry=[4175.00-4176.70]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |

Ticks (bid/ask): 09-16 10:30:02 4190.80/4191.00; 09-16 10:31:40 4176.50/4176.70

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4190.80
- stop: 4200.20
- R: 9.40
- target(s): 4176.70
- exit: TARGET net 1.50R

#### `GV-P08-V04m` · `GT-OUTSIDE-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P08-V04` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Zone edge 4223.29: 14.09/9.40 = 1.4989R < 1.5 -> SKIPPED_SRC_RR (signal happened, no trade).

Tags: T_SR, boundary, insufficient-rr
Context: atr=4 · trend=UP · zones_entry=[4175.00-4176.71]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |

Ticks (bid/ask): 09-16 10:30:02 4190.80/4191.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4190.80
- stop: 4200.20
- R: 9.40

#### `GV-P08-V05m` · `GT-OUTSIDE-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P08-V05` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> No zone at all -> SKIPPED_SRC_NO_TARGET.

Tags: T_SR, no-target
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |

Ticks (bid/ask): 09-16 10:30:02 4190.80/4191.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4190.80
- stop: 4200.20
- R: 9.40

#### `GV-P08-V06m` · `GT-OUTSIDE-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P08-V06` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Only zones BELOW the entry for a BUY -> nothing beyond the entry -> SKIPPED_SRC_NO_TARGET.

Tags: T_SR, no-target
Context: atr=4 · trend=UP · zones_entry=[4209.00-4210.00], [4219.00-4220.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |

Ticks (bid/ask): 09-16 10:30:02 4190.80/4191.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4190.80
- stop: 4200.20
- R: 9.40

#### `GV-P08-V07m` · `GT-OUTSIDE-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P08-V07` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Nearest zone (4215.00) gives only 0.62R; a farther zone (4235.00 = 2.75R) would qualify but the rule NEVER steps over a nearer obstacle -> SKIPPED_SRC_RR.

Tags: T_SR, nearest-only, insufficient-rr
Context: atr=4 · trend=UP · zones_entry=[4184.00-4185.00], [4164.00-4165.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |

Ticks (bid/ask): 09-16 10:30:02 4190.80/4191.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4190.80
- stop: 4200.20
- R: 9.40

#### `GV-P08-V08m` · `GT-OUTSIDE-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P08-V08` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> The nearest zone is DEAD (a bar closed beyond it) so it is ignored; the next live zone (4230.00) is the target: 20.80/9.40 = 2.21R.

Tags: T_SR, dead-zone
Context: atr=4 · trend=UP · zones_entry=[4175.00-4176.00 DEAD], [4169.00-4170.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |

Ticks (bid/ask): 09-16 10:30:02 4190.80/4191.00; 09-16 10:31:40 4169.80/4170.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4190.80
- stop: 4200.20
- R: 9.40
- target(s): 4170.00
- exit: TARGET net 104/47 (≈2.2128)R

#### `GV-P08-V10m` · `GT-OUTSIDE-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P08-V10` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> R2 = 5.98 < 1.5*ATR = 6.00: BASE Outside Bar exists, but SRC-PS does not qualify (variant identity needs R2>=1.5*ATR): no variant events.

Tags: variant-not-qualified
Context: atr=4 · trend=UP · zones_entry=[4175.00-4176.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4197.99 | 4192.01 | 4193.00 |

Ticks (bid/ask): 09-16 10:30:02 4192.80/4193.00

- variant: no event

#### `GV-P08-V11m` · `GT-OUTSIDE-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P08-V11` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> A high-impact USD event at 10:20 lies inside C2's bar (10:15-10:30): SRC-PS skips it -> SKIPPED_NEWS (signal happened, no trade).

Tags: news
Context: atr=4 · trend=UP · zones_entry=[4175.00-4176.00] · news=CPI high USD 10:20:00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |

Ticks (bid/ask): 09-16 10:30:02 4190.80/4191.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_NEWS

#### `GV-P08-V12m` · `GT-OUTSIDE-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P08-V12` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Same but MEDIUM impact: not a high-impact event -> trade taken.

Tags: news
Context: atr=4 · trend=UP · zones_entry=[4175.00-4176.00] · news=CPI medium USD 10:20:00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |

Ticks (bid/ask): 09-16 10:30:02 4190.80/4191.00; 09-16 10:31:40 4175.80/4176.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4190.80
- stop: 4200.20
- R: 9.40
- target(s): 4176.00
- exit: TARGET net 74/47 (≈1.5745)R

#### `GV-P08-V13m` · `GT-OUTSIDE-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P08-V13` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> High-impact but EUR event: only USD events count -> trade taken.

Tags: news
Context: atr=4 · trend=UP · zones_entry=[4175.00-4176.00] · news=CPI high EUR 10:20:00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |

Ticks (bid/ask): 09-16 10:30:02 4190.80/4191.00; 09-16 10:31:40 4175.80/4176.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4190.80
- stop: 4200.20
- R: 9.40
- target(s): 4176.00
- exit: TARGET net 74/47 (≈1.5745)R

## `GT-OUTSIDE-BULL-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4205.00/4208.00/4202.00/4206.00 ; 4204.00/4208.00/4200.00/4207.00 | DOWN | 4 | no shape | H2>H1 | H2 = H1 exactly (4208.00): not strictly greater -> fails H2>H1 only. |
| `B02` | 4205.00/4208.00/4202.00/4206.00 ; 4204.00/4208.01/4200.00/4207.00 | DOWN | 4 | shape ✔ · formed ✔ | — | H2 = H1 + 0.01: passes. |
| `B03` | 4205.00/4208.00/4202.00/4206.00 ; 4204.00/4210.00/4202.00/4209.00 | DOWN | 4 | no shape | L2<L1 | L2 = L1 exactly (4202.00): fails L2<L1 only. |
| `B04` | 4205.00/4208.00/4202.00/4206.00 ; 4204.00/4210.00/4201.99/4209.00 | DOWN | 4 | shape ✔ · formed ✔ | — | L2 = L1 - 0.01: passes. |
| `B05` | 4205.00/4208.00/4202.00/4206.00 ; 4206.00/4210.00/4200.00/4206.00 | DOWN | 4 | no shape | direction=BULL | C2 = O2 (doji close): shape geometry holds but direction is undefined -> no bullish (and no bearish) signal. |
| `B06` | 4205.00/4208.00/4202.00/4206.00 ; 4209.00/4210.00/4200.00/4204.00 | DOWN | 4 | no shape | direction=BULL | Bearish outside bar seen by the BULL strategy: geometry passes, direction clause fails. |
| `F01` | 4205.00/4208.00/4202.00/4206.00 ; 4203.00/4209.00/4201.00/4208.00 | DOWN | 4 | shape ✔ · formed ✔ | — | R2 = 8.00 >= 6.00: flag big true. |
| `F02` | 4205.00/4207.00/4203.00/4206.00 ; 4204.00/4208.00/4202.00/4207.00 | DOWN | 4 | shape ✔ · formed ✔ | — | R2 = 6.00 exactly = 1.5*ATR: flag true (>=). |
| `F03` | 4205.00/4207.00/4203.00/4206.00 ; 4204.00/4207.99/4202.01/4207.00 | DOWN | 4 | shape ✔ · formed ✔ | — | R2 = 5.98 < 6.00: flag false; pattern still forms. |
| `N01` | 4205.00/4208.00/4202.00/4206.00 ; 4204.00/4207.00/4203.00/4206.00 | DOWN | 4 | no shape | H2>H1, L2<L1 | Inside bar (not outside): both range clauses fail. |
| `NZ1` | 4200.00/4204.00/4198.00/4203.00 ; 4202.00/4203.00/4199.00/4200.00 | DOWN | 4 | canonical: no event; variant: no event | — | Second bar sits inside the first: not an outside bar. |
| `T01` | 4205.00/4208.00/4202.00/4206.00 ; 4204.00/4210.00/4200.00/4209.00 | UP | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Outside Bar has no prior-state requirement: formed with trend UP. |
| `T02` | 4205.00/4208.00/4202.00/4206.00 ; 4204.00/4210.00/4200.00/4209.00 | RANGE | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Outside Bar has no prior-state requirement: formed with trend RANGE. |
| `T03` | 4205.00/4208.00/4202.00/4206.00 ; 4204.00/4210.00/4200.00/4209.00 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Outside Bar has no prior-state requirement: formed with trend UNDETERMINED. |
| `T04` | 4205.00/4208.00/4202.00/4206.00 ; 4204.00/4210.00/4200.00/4209.00 | DOWN | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Outside Bar has no prior-state requirement: formed with trend DOWN. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:30:02 4209.00/4209.20; 09-16 10:32:00 4213.70/4213.90; 09-16 10:35:00 4228.00/4228.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.20; stop: 4199.80; R: 9.40; target(s): 4228.00; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:30:02 4209.00/4209.20; 09-16 10:32:00 4204.30/4204.50; 09-16 10:35:00 4199.80/4200.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.20; stop: 4199.80; R: 9.40; target(s): 4228.00; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4197.80 < stop): fill = that tick's bid, not the stop (G9): -57/47R. | 09-16 10:30:02 4209.00/4209.20; 09-16 10:32:00 4197.80/4198.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.20; stop: 4199.80; R: 9.40; target(s): 4228.00; exit: STOP net -57/47 (≈-1.2128)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:30:02 4209.00/4209.20; 09-16 10:31:40 4199.80/4200.00; 09-16 10:33:20 4228.00/4228.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.20; stop: 4199.80; R: 9.40; target(s): 4228.00; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:30:02 4209.00/4209.20; 09-16 10:31:40 4228.00/4228.20; 09-16 10:33:20 4199.80/4200.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.20; stop: 4199.80; R: 9.40; target(s): 4228.00; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:30:02 4209.00/4209.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.20; stop: 4199.80; R: 9.40; target(s): 4228.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:30:02 4209.00/4209.50; 09-16 10:33:20 4228.90/4229.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.50; stop: 4199.80; R: 9.70; target(s): 4228.90; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:45:00 4209.00/4209.20; 09-16 10:46:40 4228.00/4228.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.20; stop: 4199.80; R: 9.40; target(s): 4228.00; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:45:01 4209.00/4209.20; 09-16 10:46:40 4228.00/4228.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:30:02 4201.30/4201.80; 09-16 10:31:40 4205.80/4206.30 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4201.80; R: 2.00; target(s): 4205.80; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:30:02 4201.29/4201.79; 09-16 10:31:40 4205.79/4206.29 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4234.40 > target 4228.00): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:30:02 4209.00/4209.20; 09-16 10:32:00 4234.40/4234.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4209.20; stop: 4199.80; R: 9.40; target(s): 4228.00; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4209.00/4209.20; 09-21 00:30:00 4228.00/4228.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4209.20; stop: 4199.80; R: 9.40; target(s): 4228.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4209.00/4209.20; 09-21 00:30:00 4228.00/4228.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4209.20; stop: 4199.80; R: 9.40; target(s): 4228.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4209.00/4209.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P08-R01` · `GT-OUTSIDE-BULL-v1.0/BASE` · M15
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |
| 3 | 09-16 10:30 | 4209.00 | 4212.00 | 4207.00 | 4210.00 |
| 4 | 09-16 10:45 | 4210.00 | 4213.00 | 4208.00 | 4211.00 |
| 5 | 09-16 11:00 | 4211.00 | 4212.00 | 4206.00 | 4208.00 |
| 6 | 09-16 11:15 | 4208.00 | 4211.00 | 4205.00 | 4209.00 |
| 7 | 09-16 11:30 | 4210.00 | 4214.00 | 4207.00 | 4212.00 |
| 8 | 09-16 11:45 | 4212.00 | 4218.00 | 4200.00 | 4213.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4209.00 | h1: ret=1.00, mfe=3.00, mae=-2.00, end_index=2 | h3: ret=-1.00, mfe=4.00, mae=-3.00, end_index=4 | h5: ret=3.00, mfe=5.00, mae=-4.00, end_index=6 | h10: NULL | h20: NULL

#### `GV-P08-Y01` · `GT-OUTSIDE-BULL-v1.0/BASE` · M15
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4209.20
- stop: 4199.80
- R: 9.40
- target(s): 4228.00

### Variant `SRC-PS`

#### `GV-P08-V01` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · M15
> SRC-PS Outside Bar: R2 = 10 >= 1.5*ATR (6.0) so it qualifies; entry at the ask 4209.20; stop L2-0.20 = 4199.80 (R 9.40); target T_SR(1.5) = near edge of the nearest live zone above the entry (4224.00): 14.80 = 1.57R >= 1.5R -> trade. Target hit: +1.5745R (not 2R).

Tags: variant-clean-yes, T_SR
Context: atr=4 · trend=DOWN · zones_entry=[4224.00-4225.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20; 09-16 10:31:40 4224.00/4224.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4209.20
- stop: 4199.80
- R: 9.40
- target(s): 4224.00
- exit: TARGET net 74/47 (≈1.5745)R

#### `GV-P08-V02` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · M15
> Same trade stopped out at 4199.80: -1.00R.

Tags: variant, sl-first-ticks
Context: atr=4 · trend=DOWN · zones_entry=[4224.00-4225.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20; 09-16 10:31:40 4199.80/4200.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4209.20
- stop: 4199.80
- R: 9.40
- target(s): 4224.00
- exit: STOP net -1.00R

#### `GV-P08-V03` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · M15
> Reward exactly 1.5R (zone edge 4223.30, entry 4209.20, R 9.40 -> 14.10 = 1.5R): accepted (skip only if BELOW minR).

Tags: T_SR, boundary
Context: atr=4 · trend=DOWN · zones_entry=[4223.30-4225.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20; 09-16 10:31:40 4223.30/4223.50

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4209.20
- stop: 4199.80
- R: 9.40
- target(s): 4223.30
- exit: TARGET net 1.50R

#### `GV-P08-V04` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · M15
> Zone edge 4223.29: 14.09/9.40 = 1.4989R < 1.5 -> SKIPPED_SRC_RR (signal happened, no trade).

Tags: T_SR, boundary, insufficient-rr
Context: atr=4 · trend=DOWN · zones_entry=[4223.29-4225.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4209.20
- stop: 4199.80
- R: 9.40

#### `GV-P08-V05` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · M15
> No zone at all -> SKIPPED_SRC_NO_TARGET.

Tags: T_SR, no-target
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4209.20
- stop: 4199.80
- R: 9.40

#### `GV-P08-V06` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · M15
> Only zones BELOW the entry for a BUY -> nothing beyond the entry -> SKIPPED_SRC_NO_TARGET.

Tags: T_SR, no-target
Context: atr=4 · trend=DOWN · zones_entry=[4190.00-4191.00], [4180.00-4181.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4209.20
- stop: 4199.80
- R: 9.40

#### `GV-P08-V07` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · M15
> Nearest zone (4215.00) gives only 0.62R; a farther zone (4235.00 = 2.75R) would qualify but the rule NEVER steps over a nearer obstacle -> SKIPPED_SRC_RR.

Tags: T_SR, nearest-only, insufficient-rr
Context: atr=4 · trend=DOWN · zones_entry=[4215.00-4216.00], [4235.00-4236.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4209.20
- stop: 4199.80
- R: 9.40

#### `GV-P08-V08` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · M15
> The nearest zone is DEAD (a bar closed beyond it) so it is ignored; the next live zone (4230.00) is the target: 20.80/9.40 = 2.21R.

Tags: T_SR, dead-zone
Context: atr=4 · trend=DOWN · zones_entry=[4224.00-4225.00 DEAD], [4230.00-4231.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20; 09-16 10:31:40 4230.00/4230.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4209.20
- stop: 4199.80
- R: 9.40
- target(s): 4230.00
- exit: TARGET net 104/47 (≈2.2128)R

#### `GV-P08-V09` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · **BLOCKED_AMBIGUITY**
> A live zone STRADDLES the entry (4208.00-4212.00, entry 4209.20): its near edge (4208.00) is behind the entry. G10 says 'nearest live zone beyond the entry' and 'never steps over a nearer obstacle', but does not say whether a zone containing the entry is 'beyond'.

Context: atr=4 · trend=DOWN · zones_entry=[4208.00-4212.00], [4230.00-4231.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20

Candidate rulings (no expected value is asserted until the spec settles one):
- Reading A: the straddling zone is ignored; the target is 4230.00 (2.21R) -> trade.
- Reading B: the straddling zone is the nearest obstacle and its near edge is behind the entry -> SKIPPED_TARGET_ALREADY_PASSED.

#### `GV-P08-V10` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · M15
> R2 = 5.98 < 1.5*ATR = 6.00: BASE Outside Bar exists, but SRC-PS does not qualify (variant identity needs R2>=1.5*ATR): no variant events.

Tags: variant-not-qualified
Context: atr=4 · trend=DOWN · zones_entry=[4224.00-4225.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4207.99 | 4202.01 | 4207.00 |

Ticks (bid/ask): 09-16 10:30:02 4207.00/4207.20

- variant: no event

#### `GV-P08-V11` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · M15
> A high-impact USD event at 10:20 lies inside C2's bar (10:15-10:30): SRC-PS skips it -> SKIPPED_NEWS (signal happened, no trade).

Tags: news
Context: atr=4 · trend=DOWN · zones_entry=[4224.00-4225.00] · news=CPI high USD 10:20:00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_NEWS

#### `GV-P08-V12` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · M15
> Same but MEDIUM impact: not a high-impact event -> trade taken.

Tags: news
Context: atr=4 · trend=DOWN · zones_entry=[4224.00-4225.00] · news=CPI medium USD 10:20:00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20; 09-16 10:31:40 4224.00/4224.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4209.20
- stop: 4199.80
- R: 9.40
- target(s): 4224.00
- exit: TARGET net 74/47 (≈1.5745)R

#### `GV-P08-V13` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · M15
> High-impact but EUR event: only USD events count -> trade taken.

Tags: news
Context: atr=4 · trend=DOWN · zones_entry=[4224.00-4225.00] · news=CPI high EUR 10:20:00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20; 09-16 10:31:40 4224.00/4224.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4209.20
- stop: 4199.80
- R: 9.40
- target(s): 4224.00
- exit: TARGET net 74/47 (≈1.5745)R

#### `GV-P08-V14` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · **BLOCKED_AMBIGUITY**
> A high-impact USD event at 10:05 lies inside C1's bar (10:00-10:15), not C2's. The spec says SRC-PS 'skips bars containing a high-impact USD event' without saying whether that means C2 only, C1 or C2, or the whole formation.

Context: atr=4 · trend=DOWN · zones_entry=[4224.00-4225.00] · news=CPI high USD 10:05:00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20

Candidate rulings (no expected value is asserted until the spec settles one):
- Reading A: only the signal bar C2 is checked -> trade taken.
- Reading B: any geometry bar (C1 or C2) -> SKIPPED_NEWS.

#### `GV-P08-V15` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · **BLOCKED_AMBIGUITY**
> SRC-PS also 'skips bars overlapping the daily rollover pause' but the daily rollover pause is not defined anywhere in the globals (times, timezone, duration).

Context: atr=4 · trend=DOWN · zones_entry=[4224.00-4225.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4209.20

Candidate rulings (no expected value is asserted until the spec settles one):
- Cannot be evaluated until the rollover window is defined (start, end, timezone, whether it follows broker time).

