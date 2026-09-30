# P03 Pin Bar — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.3.2 · vector pack GV-0.2 · **97 vectors** (97 firm)

Strategies covered: `GT-PINBAR-BEAR-v1.0`, `GT-PINBAR-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-PINBAR-BEAR-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01m` | 4200.50/4202.00/4200.00/4200.10 | UP | 4 | shape ✔ · formed ✔ | — | R exactly 2.00 (0.50*ATR): passes. |
| `B02m` | 4200.49/4202.00/4199.99/4200.09 | UP | 4 | shape ✔ · formed ✔ | — | R = 2.01: just inside. |
| `B03m` | 4200.51/4202.00/4200.01/4200.11 | UP | 4 | no shape | (1 clause) | R = 1.99: only the range clause fails. |
| `B04m` | 4203.35/4210.00/4200.00/4200.05 | UP | 4 | shape ✔ · formed ✔ | — | B exactly 0.33*R (R=10: B 3.30, LW 6.65, UW 0.05): passes. |
| `B05m` | 4203.35/4210.00/4200.01/4200.06 | UP | 4 | shape ✔ · formed ✔ | — | B just inside (3.29). |
| `B06m` | 4203.35/4210.00/4199.99/4200.04 | UP | 4 | no shape | (1 clause) | B just outside (3.31 > 0.33*10.01 = 3.3033): only the body clause fails. |
| `B07m` | 4203.40/4210.00/4200.00/4200.40 | UP | 4 | shape ✔ · formed ✔ | — | LW exactly 0.66*R (R=10: LW 6.60, B 3.00, UW 0.40): passes. |
| `B08m` | 4203.39/4210.00/4199.99/4200.39 | UP | 4 | shape ✔ · formed ✔ | — | LW just inside (6.61, R=10.01, limit 6.6066). |
| `B09m` | 4203.41/4210.00/4200.01/4200.41 | UP | 4 | no shape | (1 clause) | LW just outside (6.59, R=9.99, limit 6.5934): only the wick clause fails. |
| `B10m` | 4201.60/4206.00/4200.00/4200.60 | UP | 4 | shape ✔ · formed ✔ | — | Opposite wick exactly 0.10*R (R=6.00, UW 0.60): passes. |
| `B11m` | 4201.60/4206.00/4199.99/4200.60 | UP | 4 | no shape | (1 clause) | Opposite wick 0.61 (limit 0.601): only that clause fails. |
| `B12m` | 4200.70/4208.00/4200.00/4202.00 | UP | 4 | shape ✔ · formed ✔ | — | Close exactly at L+0.75R using a bearish-coloured body (R=8: LW 6.00, B 1.30, UW 0.70): passes (close = bottom of body). |
| `B13m` | 4200.71/4208.00/4200.01/4202.01 | UP | 4 | no shape | (1 clause) | Same but LW 5.99 (R=7.99, line 5.9925): only the close-position clause fails. |
| `N02m` | 4202.01/4208.00/4200.01/4200.71 | UP | 4 | shape ✔ · formed ✔ | — | Bullish body of the same wick geometry passes the close test easily (close at top of body). |
| `N03m` | 4205.50/4206.00/4200.00/4204.50 | UP | 4 | no shape | (3 clause) | Upper-wick pin geometry is the BEARISH pin; for the bullish strategy it fails wick, opposite-wick and close clauses. |
| `NZ1m` | 4200.00/4200.50/4195.50/4196.00 | UP | 4 | canonical: no event; variant: no event | — | Ordinary full-bodied bullish candle: body 4.0 of range 5.0 -> not a pin bar. |
| `T01m` | 4201.50/4206.00/4200.00/4200.50 | DOWN | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Pin Bar has NO prior-state requirement: formed with trend UP (context only). |
| `T02m` | 4201.50/4206.00/4200.00/4200.50 | RANGE | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Pin Bar has NO prior-state requirement: formed with trend RANGE (context only). |
| `T03m` | 4201.50/4206.00/4200.00/4200.50 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Pin Bar has NO prior-state requirement: formed with trend UNDETERMINED (context only). |
| `T04m` | 4201.50/4206.00/4200.00/4200.50 | UP | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Pin Bar has NO prior-state requirement: formed with trend DOWN (context only). |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01m` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:15:02 4200.30/4200.50; 09-16 10:17:00 4197.35/4197.55; 09-16 10:20:00 4188.30/4188.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.30; stop: 4206.20; R: 5.90; target(s): 4188.50; exit: TARGET net 2.00R |
| `L02m` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:15:02 4200.30/4200.50; 09-16 10:17:00 4203.25/4203.45; 09-16 10:20:00 4206.00/4206.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.30; stop: 4206.20; R: 5.90; target(s): 4188.50; exit: STOP net -1.00R |
| `L03m` | Tick gaps through the stop (bid 4191.80 < stop): fill = that tick's bid, not the stop (G9): -79/59R. | 09-16 10:15:02 4200.30/4200.50; 09-16 10:17:00 4208.00/4208.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.30; stop: 4206.20; R: 5.90; target(s): 4188.50; exit: STOP net -79/59 (≈-1.3390)R |
| `L04m` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:15:02 4200.30/4200.50; 09-16 10:16:40 4206.00/4206.20; 09-16 10:18:20 4188.30/4188.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.30; stop: 4206.20; R: 5.90; target(s): 4188.50; exit: STOP net -1.00R |
| `L05m` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:15:02 4200.30/4200.50; 09-16 10:16:40 4188.30/4188.50; 09-16 10:18:20 4206.00/4206.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.30; stop: 4206.20; R: 5.90; target(s): 4188.50; exit: TARGET net 2.00R |
| `L06m` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:15:02 4200.30/4200.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.30; stop: 4206.20; R: 5.90; target(s): 4188.50; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07m` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:15:02 4200.00/4200.50; 09-16 10:18:20 4187.10/4187.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; spread_at_entry: 0.50; entry: 4200.00; stop: 4206.20; R: 6.20; target(s): 4187.60; exit: TARGET net 2.00R |
| `L08m` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:30:00 4200.30/4200.50; 09-16 10:31:40 4188.30/4188.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.30; stop: 4206.20; R: 5.90; target(s): 4188.50; exit: TARGET net 2.00R |
| `L09m` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:30:01 4200.30/4200.50; 09-16 10:31:40 4188.30/4188.50 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10m` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:15:02 4204.20/4204.70; 09-16 10:16:40 4199.70/4200.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4204.20; R: 2.00; target(s): 4200.20; exit: TARGET net 2.00R |
| `L11m` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:15:02 4204.21/4204.71; 09-16 10:16:40 4199.71/4200.21 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12m` | Tick jumps far past the target (bid 4217.90 > target 4211.50): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:15:02 4200.30/4200.50; 09-16 10:17:00 4181.90/4182.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.30; stop: 4206.20; R: 5.90; target(s): 4188.50; exit: TARGET net 2.00R |
| `W01m` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4200.30/4200.50; 09-21 00:30:00 4188.30/4188.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4200.30; stop: 4206.20; R: 5.90; target(s): 4188.50; entry_across_break: True; exit: TARGET net 2.00R |
| `W02m` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4200.30/4200.50; 09-21 00:30:00 4188.30/4188.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4200.30; stop: 4206.20; R: 5.90; target(s): 4188.50; entry_across_break: True; exit: TARGET net 2.00R |
| `W03m` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4200.30/4200.50 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P03-R01m` · `GT-PINBAR-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P03-R01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4201.50 | 4206.00 | 4200.00 | 4200.50 |
| 2 | 09-16 10:15 | 4200.50 | 4202.50 | 4197.50 | 4199.50 |
| 3 | 09-16 10:30 | 4199.50 | 4201.50 | 4196.50 | 4198.50 |
| 4 | 09-16 10:45 | 4198.50 | 4203.50 | 4197.50 | 4201.50 |
| 5 | 09-16 11:00 | 4201.50 | 4204.50 | 4198.50 | 4200.50 |
| 6 | 09-16 11:15 | 4199.50 | 4202.50 | 4195.50 | 4197.50 |
| 7 | 09-16 11:30 | 4197.50 | 4209.50 | 4191.50 | 4196.50 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4200.50 | h1: ret=1.00, mfe=3.00, mae=2.00, end_index=1 | h3: ret=-1.00, mfe=4.00, mae=3.00, end_index=3 | h5: ret=3.00, mfe=5.00, mae=4.00, end_index=5 | h10: NULL | h20: NULL

#### `GV-P03-Y01m` · `GT-PINBAR-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P03-Y01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4201.50 | 4206.00 | 4200.00 | 4200.50 |

Ticks (bid/ask): 09-16 10:15:02 4200.30/4200.50

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:15:00Z
- entry: 4200.30
- stop: 4206.20
- R: 5.90
- target(s): 4188.50

### Variant `SRC-CB`

#### `GV-P03-V01m` · `GT-PINBAR-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P03-V01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> SRC-CB Pin Bar (bull): trend UP (with the trend) AND at support (low 4194.00 is 0.10 above the zone top 4193.90) on H1: qualifies. Entry ask 4199.70; stop L-0.20 = 4193.80; R 5.90; T_SR(2.0) = zone edge 4225.00 = 4.29R -> trade.

Tags: variant-clean-yes, with-trend
Context: atr=4 · trend=DOWN · zones_pre=[4206.10-4206.50] · zones_entry=[4174.00-4175.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4201.50 | 4206.00 | 4200.00 | 4200.50 |

Ticks (bid/ask): 09-16 11:00:02 4200.30/4200.50; 09-16 11:01:40 4174.80/4175.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4200.30
- stop: 4206.20
- R: 5.90
- target(s): 4175.00
- exit: TARGET net 253/59 (≈4.2881)R

#### `GV-P03-V02m` · `GT-PINBAR-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P03-V02` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Same pin bar in a DOWNtrend: the CB rule needs the pin WITH the trend (bull needs UP) -> not qualified (BASE Pin Bar still formed).

Tags: with-trend, variant-not-qualified
Context: atr=4 · trend=UP · zones_pre=[4206.10-4206.50] · zones_entry=[4174.00-4175.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4201.50 | 4206.00 | 4200.00 | 4200.50 |

Ticks (bid/ask): 09-16 11:00:02 4200.30/4200.50

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P03-V03m` · `GT-PINBAR-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P03-V03` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Trend RANGE: not qualified.

Tags: with-trend, variant-not-qualified
Context: atr=4 · trend=RANGE · zones_pre=[4206.10-4206.50] · zones_entry=[4174.00-4175.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4201.50 | 4206.00 | 4200.00 | 4200.50 |

Ticks (bid/ask): 09-16 11:00:02 4200.30/4200.50

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P03-V04m` · `GT-PINBAR-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P03-V04` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Trend UP but no level: not qualified.

Tags: at-level, variant-not-qualified
Context: atr=4 · trend=DOWN · zones_entry=[4174.00-4175.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4201.50 | 4206.00 | 4200.00 | 4200.50 |

Ticks (bid/ask): 09-16 11:00:02 4200.30/4200.50

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P03-V05m` · `GT-PINBAR-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P03-V05` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Zone top 4193.60: distance 0.40 = 0.10*ATR exactly: AT_SUPPORT holds -> qualifies.

Tags: at-level, boundary
Context: atr=4 · trend=DOWN · zones_pre=[4206.40-4206.60] · zones_entry=[4174.00-4175.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4201.50 | 4206.00 | 4200.00 | 4200.50 |

Ticks (bid/ask): 09-16 11:00:02 4200.30/4200.50; 09-16 11:01:40 4174.80/4175.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4200.30
- stop: 4206.20
- R: 5.90
- target(s): 4175.00
- exit: TARGET net 253/59 (≈4.2881)R

#### `GV-P03-V06m` · `GT-PINBAR-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P03-V06` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Zone top 4193.59: distance 0.41 -> not at support.

Tags: at-level, boundary, variant-not-qualified
Context: atr=4 · trend=DOWN · zones_pre=[4206.41-4206.60] · zones_entry=[4174.00-4175.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4201.50 | 4206.00 | 4200.00 | 4200.50 |

Ticks (bid/ask): 09-16 11:00:02 4200.30/4200.50

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P03-V07m` · `GT-PINBAR-BEAR-v1.0/SRC-CB` · M15
*Mirror of `GV-P03-V07` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> M15 is not in {H1,H4,D1}: SKIPPED_TF_NOT_ALLOWED.

Tags: tf-gate
Context: atr=4 · trend=DOWN · zones_pre=[4206.10-4206.50] · zones_entry=[4174.00-4175.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4201.50 | 4206.00 | 4200.00 | 4200.50 |

Ticks (bid/ask): 09-16 10:15:02 4200.30/4200.50

- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

#### `GV-P03-V08m` · `GT-PINBAR-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P03-V08` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Zone edge 4211.50: 11.80/5.90 = 2.00R exactly -> accepted.

Tags: T_SR, boundary
Context: atr=4 · trend=DOWN · zones_pre=[4206.10-4206.50] · zones_entry=[4174.00-4188.50]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4201.50 | 4206.00 | 4200.00 | 4200.50 |

Ticks (bid/ask): 09-16 11:00:02 4200.30/4200.50; 09-16 11:01:40 4188.30/4188.50

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4200.30
- stop: 4206.20
- R: 5.90
- target(s): 4188.50
- exit: TARGET net 2.00R

#### `GV-P03-V09m` · `GT-PINBAR-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P03-V09` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Zone edge 4211.49 -> 1.998R -> SKIPPED_SRC_RR.

Tags: T_SR, boundary, insufficient-rr
Context: atr=4 · trend=DOWN · zones_pre=[4206.10-4206.50] · zones_entry=[4174.00-4188.51]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4201.50 | 4206.00 | 4200.00 | 4200.50 |

Ticks (bid/ask): 09-16 11:00:02 4200.30/4200.50

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4200.30
- stop: 4206.20
- R: 5.90

#### `GV-P03-V10m` · `GT-PINBAR-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P03-V10` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Qualified but no live zone above the entry for T_SR(2.0) -> SKIPPED_SRC_NO_TARGET.

Tags: T_SR, no-target
Context: atr=4 · trend=DOWN · zones_pre=[4206.10-4206.50]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4201.50 | 4206.00 | 4200.00 | 4200.50 |

Ticks (bid/ask): 09-16 11:00:02 4200.30/4200.50

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4200.30
- stop: 4206.20
- R: 5.90

## `GT-PINBAR-BULL-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4199.50/4200.00/4198.00/4199.90 | DOWN | 4 | shape ✔ · formed ✔ | — | R exactly 2.00 (0.50*ATR): passes. |
| `B02` | 4199.51/4200.01/4198.00/4199.91 | DOWN | 4 | shape ✔ · formed ✔ | — | R = 2.01: just inside. |
| `B03` | 4199.49/4199.99/4198.00/4199.89 | DOWN | 4 | no shape | R>=0.50ATR | R = 1.99: only the range clause fails. |
| `B04` | 4196.65/4200.00/4190.00/4199.95 | DOWN | 4 | shape ✔ · formed ✔ | — | B exactly 0.33*R (R=10: B 3.30, LW 6.65, UW 0.05): passes. |
| `B05` | 4196.65/4199.99/4190.00/4199.94 | DOWN | 4 | shape ✔ · formed ✔ | — | B just inside (3.29). |
| `B06` | 4196.65/4200.01/4190.00/4199.96 | DOWN | 4 | no shape | B<=0.33R | B just outside (3.31 > 0.33*10.01 = 3.3033): only the body clause fails. |
| `B07` | 4196.60/4200.00/4190.00/4199.60 | DOWN | 4 | shape ✔ · formed ✔ | — | LW exactly 0.66*R (R=10: LW 6.60, B 3.00, UW 0.40): passes. |
| `B08` | 4196.61/4200.01/4190.00/4199.61 | DOWN | 4 | shape ✔ · formed ✔ | — | LW just inside (6.61, R=10.01, limit 6.6066). |
| `B09` | 4196.59/4199.99/4190.00/4199.59 | DOWN | 4 | no shape | LW>=0.66R | LW just outside (6.59, R=9.99, limit 6.5934): only the wick clause fails. |
| `B10` | 4198.40/4200.00/4194.00/4199.40 | DOWN | 4 | shape ✔ · formed ✔ | — | Opposite wick exactly 0.10*R (R=6.00, UW 0.60): passes. |
| `B11` | 4198.40/4200.01/4194.00/4199.40 | DOWN | 4 | no shape | UW<=0.10R | Opposite wick 0.61 (limit 0.601): only that clause fails. |
| `B12` | 4199.30/4200.00/4192.00/4198.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Close exactly at L+0.75R using a bearish-coloured body (R=8: LW 6.00, B 1.30, UW 0.70): passes (close = bottom of body). |
| `B13` | 4199.29/4199.99/4192.00/4197.99 | DOWN | 4 | no shape | C>=L+0.75R | Same but LW 5.99 (R=7.99, line 5.9925): only the close-position clause fails. |
| `N02` | 4197.99/4199.99/4192.00/4199.29 | DOWN | 4 | shape ✔ · formed ✔ | — | Bullish body of the same wick geometry passes the close test easily (close at top of body). |
| `N03` | 4194.50/4200.00/4194.00/4195.50 | DOWN | 4 | no shape | LW>=0.66R, UW<=0.10R, C>=L+0.75R | Upper-wick pin geometry is the BEARISH pin; for the bullish strategy it fails wick, opposite-wick and close clauses. |
| `NZ1` | 4200.00/4204.50/4199.50/4204.00 | DOWN | 4 | canonical: no event; variant: no event | — | Ordinary full-bodied bullish candle: body 4.0 of range 5.0 -> not a pin bar. |
| `T01` | 4198.50/4200.00/4194.00/4199.50 | UP | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Pin Bar has NO prior-state requirement: formed with trend UP (context only). |
| `T02` | 4198.50/4200.00/4194.00/4199.50 | RANGE | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Pin Bar has NO prior-state requirement: formed with trend RANGE (context only). |
| `T03` | 4198.50/4200.00/4194.00/4199.50 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Pin Bar has NO prior-state requirement: formed with trend UNDETERMINED (context only). |
| `T04` | 4198.50/4200.00/4194.00/4199.50 | DOWN | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL | — | Pin Bar has NO prior-state requirement: formed with trend DOWN (context only). |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:15:02 4199.50/4199.70; 09-16 10:17:00 4202.45/4202.65; 09-16 10:20:00 4211.50/4211.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.70; stop: 4193.80; R: 5.90; target(s): 4211.50; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:15:02 4199.50/4199.70; 09-16 10:17:00 4196.55/4196.75; 09-16 10:20:00 4193.80/4194.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.70; stop: 4193.80; R: 5.90; target(s): 4211.50; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4191.80 < stop): fill = that tick's bid, not the stop (G9): -79/59R. | 09-16 10:15:02 4199.50/4199.70; 09-16 10:17:00 4191.80/4192.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.70; stop: 4193.80; R: 5.90; target(s): 4211.50; exit: STOP net -79/59 (≈-1.3390)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:15:02 4199.50/4199.70; 09-16 10:16:40 4193.80/4194.00; 09-16 10:18:20 4211.50/4211.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.70; stop: 4193.80; R: 5.90; target(s): 4211.50; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:15:02 4199.50/4199.70; 09-16 10:16:40 4211.50/4211.70; 09-16 10:18:20 4193.80/4194.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.70; stop: 4193.80; R: 5.90; target(s): 4211.50; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:15:02 4199.50/4199.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.70; stop: 4193.80; R: 5.90; target(s): 4211.50; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:15:02 4199.50/4200.00; 09-16 10:18:20 4212.40/4212.90 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; spread_at_entry: 0.50; entry: 4200.00; stop: 4193.80; R: 6.20; target(s): 4212.40; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:30:00 4199.50/4199.70; 09-16 10:31:40 4211.50/4211.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.70; stop: 4193.80; R: 5.90; target(s): 4211.50; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:30:01 4199.50/4199.70; 09-16 10:31:40 4211.50/4211.70 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:15:02 4195.30/4195.80; 09-16 10:16:40 4199.80/4200.30 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4195.80; R: 2.00; target(s): 4199.80; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:15:02 4195.29/4195.79; 09-16 10:16:40 4199.79/4200.29 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4217.90 > target 4211.50): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:15:02 4199.50/4199.70; 09-16 10:17:00 4217.90/4218.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.70; stop: 4193.80; R: 5.90; target(s): 4211.50; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4199.50/4199.70; 09-21 00:30:00 4211.50/4211.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4199.70; stop: 4193.80; R: 5.90; target(s): 4211.50; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4199.50/4199.70; 09-21 00:30:00 4211.50/4211.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4199.70; stop: 4193.80; R: 5.90; target(s): 4211.50; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4199.50/4199.70 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P03-R01` · `GT-PINBAR-BULL-v1.0/BASE` · M15
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4198.50 | 4200.00 | 4194.00 | 4199.50 |
| 2 | 09-16 10:15 | 4199.50 | 4202.50 | 4197.50 | 4200.50 |
| 3 | 09-16 10:30 | 4200.50 | 4203.50 | 4198.50 | 4201.50 |
| 4 | 09-16 10:45 | 4201.50 | 4202.50 | 4196.50 | 4198.50 |
| 5 | 09-16 11:00 | 4198.50 | 4201.50 | 4195.50 | 4199.50 |
| 6 | 09-16 11:15 | 4200.50 | 4204.50 | 4197.50 | 4202.50 |
| 7 | 09-16 11:30 | 4202.50 | 4208.50 | 4190.50 | 4203.50 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4199.50 | h1: ret=1.00, mfe=3.00, mae=2.00, end_index=1 | h3: ret=-1.00, mfe=4.00, mae=3.00, end_index=3 | h5: ret=3.00, mfe=5.00, mae=4.00, end_index=5 | h10: NULL | h20: NULL

#### `GV-P03-Y01` · `GT-PINBAR-BULL-v1.0/BASE` · M15
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4198.50 | 4200.00 | 4194.00 | 4199.50 |

Ticks (bid/ask): 09-16 10:15:02 4199.50/4199.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:15:00Z
- entry: 4199.70
- stop: 4193.80
- R: 5.90
- target(s): 4211.50

### Variant `SRC-CB`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `QF1` | 4198.50/4200.00/4194.00/4199.50 | RANGE | 4 | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: no event; disposition: NOT_QUALIFIED; qualification_failures: TF_NOT_ALLOWED, WITH_TREND, AT_LEVEL | — | A-12: every failed static gate is kept. M15 is not an allowed TF, the trend is not UP and there is no support level: all three failures are recorded (in gate order), no VARIANT_QUALIFIED, disposition NOT_QUALIFIED. The BASE pin bar still forms. |

#### `GV-P03-V01` · `GT-PINBAR-BULL-v1.0/SRC-CB` · H1
> SRC-CB Pin Bar (bull): trend UP (with the trend) AND at support (low 4194.00 is 0.10 above the zone top 4193.90) on H1: qualifies. Entry ask 4199.70; stop L-0.20 = 4193.80; R 5.90; T_SR(2.0) = zone edge 4225.00 = 4.29R -> trade.

Tags: variant-clean-yes, with-trend
Context: atr=4 · trend=UP · zones_pre=[4193.50-4193.90] · zones_entry=[4225.00-4226.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4198.50 | 4200.00 | 4194.00 | 4199.50 |

Ticks (bid/ask): 09-16 11:00:02 4199.50/4199.70; 09-16 11:01:40 4225.00/4225.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4199.70
- stop: 4193.80
- R: 5.90
- target(s): 4225.00
- exit: TARGET net 253/59 (≈4.2881)R

#### `GV-P03-V02` · `GT-PINBAR-BULL-v1.0/SRC-CB` · H1
> Same pin bar in a DOWNtrend: the CB rule needs the pin WITH the trend (bull needs UP) -> not qualified (BASE Pin Bar still formed).

Tags: with-trend, variant-not-qualified
Context: atr=4 · trend=DOWN · zones_pre=[4193.50-4193.90] · zones_entry=[4225.00-4226.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4198.50 | 4200.00 | 4194.00 | 4199.50 |

Ticks (bid/ask): 09-16 11:00:02 4199.50/4199.70

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P03-V03` · `GT-PINBAR-BULL-v1.0/SRC-CB` · H1
> Trend RANGE: not qualified.

Tags: with-trend, variant-not-qualified
Context: atr=4 · trend=RANGE · zones_pre=[4193.50-4193.90] · zones_entry=[4225.00-4226.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4198.50 | 4200.00 | 4194.00 | 4199.50 |

Ticks (bid/ask): 09-16 11:00:02 4199.50/4199.70

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P03-V04` · `GT-PINBAR-BULL-v1.0/SRC-CB` · H1
> Trend UP but no level: not qualified.

Tags: at-level, variant-not-qualified
Context: atr=4 · trend=UP · zones_entry=[4225.00-4226.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4198.50 | 4200.00 | 4194.00 | 4199.50 |

Ticks (bid/ask): 09-16 11:00:02 4199.50/4199.70

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P03-V05` · `GT-PINBAR-BULL-v1.0/SRC-CB` · H1
> Zone top 4193.60: distance 0.40 = 0.10*ATR exactly: AT_SUPPORT holds -> qualifies.

Tags: at-level, boundary
Context: atr=4 · trend=UP · zones_pre=[4193.40-4193.60] · zones_entry=[4225.00-4226.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4198.50 | 4200.00 | 4194.00 | 4199.50 |

Ticks (bid/ask): 09-16 11:00:02 4199.50/4199.70; 09-16 11:01:40 4225.00/4225.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4199.70
- stop: 4193.80
- R: 5.90
- target(s): 4225.00
- exit: TARGET net 253/59 (≈4.2881)R

#### `GV-P03-V06` · `GT-PINBAR-BULL-v1.0/SRC-CB` · H1
> Zone top 4193.59: distance 0.41 -> not at support.

Tags: at-level, boundary, variant-not-qualified
Context: atr=4 · trend=UP · zones_pre=[4193.40-4193.59] · zones_entry=[4225.00-4226.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4198.50 | 4200.00 | 4194.00 | 4199.50 |

Ticks (bid/ask): 09-16 11:00:02 4199.50/4199.70

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P03-V07` · `GT-PINBAR-BULL-v1.0/SRC-CB` · M15
> M15 is not in {H1,H4,D1}: SKIPPED_TF_NOT_ALLOWED.

Tags: tf-gate
Context: atr=4 · trend=UP · zones_pre=[4193.50-4193.90] · zones_entry=[4225.00-4226.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4198.50 | 4200.00 | 4194.00 | 4199.50 |

Ticks (bid/ask): 09-16 10:15:02 4199.50/4199.70

- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

#### `GV-P03-V08` · `GT-PINBAR-BULL-v1.0/SRC-CB` · H1
> Zone edge 4211.50: 11.80/5.90 = 2.00R exactly -> accepted.

Tags: T_SR, boundary
Context: atr=4 · trend=UP · zones_pre=[4193.50-4193.90] · zones_entry=[4211.50-4226.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4198.50 | 4200.00 | 4194.00 | 4199.50 |

Ticks (bid/ask): 09-16 11:00:02 4199.50/4199.70; 09-16 11:01:40 4211.50/4211.70

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4199.70
- stop: 4193.80
- R: 5.90
- target(s): 4211.50
- exit: TARGET net 2.00R

#### `GV-P03-V09` · `GT-PINBAR-BULL-v1.0/SRC-CB` · H1
> Zone edge 4211.49 -> 1.998R -> SKIPPED_SRC_RR.

Tags: T_SR, boundary, insufficient-rr
Context: atr=4 · trend=UP · zones_pre=[4193.50-4193.90] · zones_entry=[4211.49-4226.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4198.50 | 4200.00 | 4194.00 | 4199.50 |

Ticks (bid/ask): 09-16 11:00:02 4199.50/4199.70

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4199.70
- stop: 4193.80
- R: 5.90

#### `GV-P03-V10` · `GT-PINBAR-BULL-v1.0/SRC-CB` · H1
> Qualified but no live zone above the entry for T_SR(2.0) -> SKIPPED_SRC_NO_TARGET.

Tags: T_SR, no-target
Context: atr=4 · trend=UP · zones_pre=[4193.50-4193.90]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4198.50 | 4200.00 | 4194.00 | 4199.50 |

Ticks (bid/ask): 09-16 11:00:02 4199.50/4199.70

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4199.70
- stop: 4193.80
- R: 5.90

### Variant `SRC-PS`

#### `GV-DORM-P03-01` · `GT-PINBAR-BULL-v1.0/SRC-PS` · M15
> SRC-PS Pin Bar: needs AT_SUPPORT (no trend condition). Stop = wick tip - 12.5 pips x $0.10 = 4192.75; entry ask 4199.70; R 6.95; T_SWING(2.0): swing high 4214.00 = 2.06R.

Tags: variant, pip-variant
Context: atr=4 · trend=RANGE · zones_pre=[4193.50-4193.90] · swings=H4214.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4198.50 | 4200.00 | 4194.00 | 4199.50 |

Ticks (bid/ask): 09-16 10:15:02 4199.50/4199.70; 09-16 10:16:40 4214.00/4214.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4199.70
- stop: 4192.75
- R: 6.95
- target(s): 4214.00
- exit: TARGET net 286/139 (≈2.0576)R

#### `GV-DORM-P03-02` · `GT-PINBAR-BULL-v1.0/SRC-PS` · M15
> No support: not qualified.

Tags: variant-not-qualified, pip-variant
Context: atr=4 · trend=RANGE · swings=H4214.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4198.50 | 4200.00 | 4194.00 | 4199.50 |

Ticks (bid/ask): 09-16 10:15:02 4199.50/4199.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event

