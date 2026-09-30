# P13 Dark Cloud Cover — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.2.2 · vector pack GV-0.1 · **45 vectors** (45 firm)

Strategies covered: `GT-DARKCLOUD-BEAR-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-DARKCLOUD-BEAR-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4190.00/4196.50/4189.50/4196.00 ; 4196.00/4196.50/4191.50/4192.00 | UP | 4 | no shape | (1 clause) | O2 equals C1 exactly (4204.00): not strictly below -> fails O2<C1 only. |
| `B02` | 4190.00/4196.50/4189.50/4196.00 ; 4196.01/4196.50/4191.50/4192.00 | UP | 4 | shape ✔ · formed ✔ | — | O2 = C1 - 0.01: passes. |
| `B03` | 4190.00/4196.50/4189.50/4196.00 ; 4197.00/4197.50/4192.50/4193.00 | UP | 4 | no shape | (1 clause) | C2 exactly at the midpoint (4207.00): fails C2>mid1 (strict) only. |
| `B04` | 4190.00/4196.50/4189.50/4196.00 ; 4197.00/4197.50/4192.50/4192.99 | UP | 4 | shape ✔ · formed ✔ | — | C2 = midpoint + 0.01: passes. |
| `B05` | 4190.00/4196.50/4189.50/4196.00 ; 4197.00/4197.50/4189.50/4190.00 | UP | 4 | no shape | (1 clause) | C2 equals O1 exactly (4210.00): fails C2<O1 (strict) only - the Bullish Engulfing side of the split. |
| `B06` | 4190.00/4196.50/4189.50/4196.00 ; 4197.00/4197.50/4190.00/4190.01 | UP | 4 | shape ✔ · formed ✔ | — | C2 = O1 - 0.01: passes. |
| `F01` | 4190.00/4196.50/4189.50/4196.00 ; 4196.70/4197.50/4191.50/4192.00 | UP | 4 | shape ✔ · formed ✔ | — | gap_thr = max(0.10, 0.05*4)=0.20; L1=4203.50, so gap needs O2 <= 4203.30: exactly 4203.30 -> gap_flag true. |
| `F02` | 4190.00/4196.50/4189.50/4196.00 ; 4196.69/4197.50/4191.50/4192.00 | UP | 4 | shape ✔ · formed ✔ | — | O2 = 4203.31: gap_flag false; the pattern still forms (a gap is not required). |
| `LG01` | 4190.00/4193.00/4189.40/4192.40 ; 4193.00/4193.50/4190.80/4191.00 | UP | 4 | shape ✔ · formed ✔ | — | LARGE(C1) exactly on B = 2.40 (R=3.6): passes. |
| `LG02` | 4190.00/4193.00/4189.40/4192.39 ; 4193.00/4193.50/4190.80/4191.00 | UP | 4 | no shape | (1 clause) | LARGE(C1) with B = 2.39: fails LARGE only. |
| `LG03` | 4190.00/4193.00/4189.80/4193.00 ; 4193.50/4194.00/4190.50/4191.00 | UP | 4 | shape ✔ · formed ✔ | — | LARGE(C1) exactly on R = 3.20 (B=3.0): passes. |
| `LG04` | 4190.00/4193.00/4189.81/4193.00 ; 4193.50/4194.00/4190.50/4191.00 | UP | 4 | no shape | (1 clause) | LARGE(C1) with R = 3.19: fails LARGE only. |
| `LG05` | 4190.00/4194.00/4189.00/4193.00 ; 4193.50/4194.00/4190.50/4191.00 | UP | 4 | shape ✔ · formed ✔ | — | LARGE(C1) exactly on B/R = 0.60 (B=3, R=5): passes. |
| `LG06` | 4190.00/4194.00/4188.99/4193.00 ; 4193.50/4194.00/4190.50/4191.00 | UP | 4 | no shape | (1 clause) | LARGE(C1) with B/R just below 0.60 (B=3, R=5.01): fails LARGE only. |
| `N01` | 4196.00/4196.50/4189.00/4190.00 ; 4197.00/4197.50/4191.50/4192.00 | UP | 4 | no shape | (2 clause) | C1 bullish (a bullish first candle can never be pierced): fails colour (and mid/O1 relations). |
| `NZ1` | 4200.00/4200.50/4195.50/4196.00 ; 4196.00/4196.50/4191.50/4192.00 | UP | 4 | canonical: no event; variant: no event | — | Two bullish candles: nothing to pierce. |
| `T01` | 4190.00/4196.50/4189.50/4196.00 ; 4197.00/4197.50/4191.50/4192.00 | DOWN | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Piercing shape after UP: not formed. |
| `T02` | 4190.00/4196.50/4189.50/4196.00 ; 4197.00/4197.50/4191.50/4192.00 | RANGE | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Piercing shape after RANGE: not formed. |
| `T03` | 4190.00/4196.50/4189.50/4196.00 ; 4197.00/4197.50/4191.50/4192.00 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Piercing shape after UNDETERMINED: not formed. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:30:02 4191.80/4192.00; 09-16 10:32:00 4188.85/4189.05; 09-16 10:35:00 4179.80/4180.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4191.80; stop: 4197.70; R: 5.90; target(s): 4180.00; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:30:02 4191.80/4192.00; 09-16 10:32:00 4194.75/4194.95; 09-16 10:35:00 4197.50/4197.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4191.80; stop: 4197.70; R: 5.90; target(s): 4180.00; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4200.30 < stop): fill = that tick's bid, not the stop (G9): -79/59R. | 09-16 10:30:02 4191.80/4192.00; 09-16 10:32:00 4199.50/4199.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4191.80; stop: 4197.70; R: 5.90; target(s): 4180.00; exit: STOP net -79/59 (≈-1.3390)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:30:02 4191.80/4192.00; 09-16 10:31:40 4197.50/4197.70; 09-16 10:33:20 4179.80/4180.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4191.80; stop: 4197.70; R: 5.90; target(s): 4180.00; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:30:02 4191.80/4192.00; 09-16 10:31:40 4179.80/4180.00; 09-16 10:33:20 4197.50/4197.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4191.80; stop: 4197.70; R: 5.90; target(s): 4180.00; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:30:02 4191.80/4192.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4191.80; stop: 4197.70; R: 5.90; target(s): 4180.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:30:02 4191.50/4192.00; 09-16 10:33:20 4178.60/4179.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4191.50; stop: 4197.70; R: 6.20; target(s): 4179.10; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:45:00 4191.80/4192.00; 09-16 10:46:40 4179.80/4180.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4191.80; stop: 4197.70; R: 5.90; target(s): 4180.00; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:45:01 4191.80/4192.00; 09-16 10:46:40 4179.80/4180.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:30:02 4195.70/4196.20; 09-16 10:31:40 4191.20/4191.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4195.70; R: 2.00; target(s): 4191.70; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:30:02 4195.71/4196.21; 09-16 10:31:40 4191.21/4191.71 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4226.40 > target 4220.00): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:30:02 4191.80/4192.00; 09-16 10:32:00 4173.40/4173.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4191.80; stop: 4197.70; R: 5.90; target(s): 4180.00; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4191.80/4192.00; 09-21 00:30:00 4179.80/4180.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4191.80; stop: 4197.70; R: 5.90; target(s): 4180.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4191.80/4192.00; 09-21 00:30:00 4179.80/4180.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4191.80; stop: 4197.70; R: 5.90; target(s): 4180.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4191.80/4192.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P13-R01` · `GT-DARKCLOUD-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P12-R01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4197.00 | 4197.50 | 4191.50 | 4192.00 |
| 3 | 09-16 10:30 | 4192.00 | 4194.00 | 4189.00 | 4191.00 |
| 4 | 09-16 10:45 | 4191.00 | 4193.00 | 4188.00 | 4190.00 |
| 5 | 09-16 11:00 | 4190.00 | 4195.00 | 4189.00 | 4193.00 |
| 6 | 09-16 11:15 | 4193.00 | 4196.00 | 4190.00 | 4192.00 |
| 7 | 09-16 11:30 | 4191.00 | 4194.00 | 4187.00 | 4189.00 |
| 8 | 09-16 11:45 | 4189.00 | 4201.00 | 4183.00 | 4188.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4192.00 | h1: ret=1.00, mfe=3.00, mae=-2.00, end_index=2 | h3: ret=-1.00, mfe=4.00, mae=-3.00, end_index=4 | h5: ret=3.00, mfe=5.00, mae=-4.00, end_index=6 | h10: NULL | h20: NULL

#### `GV-P13-Y01` · `GT-DARKCLOUD-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P12-Y01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4197.00 | 4197.50 | 4191.50 | 4192.00 |

Ticks (bid/ask): 09-16 10:30:02 4191.80/4192.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4191.80
- stop: 4197.70
- R: 5.90
- target(s): 4180.00

### Variant `SRC-PS`

#### `GV-P13-V01` · `GT-DARKCLOUD-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P12-V01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> SRC-PS Piercing: AT_SUPPORT holds (lowest low 4203.50 is 0.40 from the zone top 4203.10 = 0.10*ATR exactly); stop = L2-0.20 = 4203.40 (BASE would use min(L1,L2)-0.20 = 4203.30: source stops below C2's low, not C1's); entry ask 4208.20; R = 4.80; target T_SR(2.0) = zone edge 4231.00 = 4.75R -> trade.

Tags: variant-clean-yes, T_SR, stop-differs-from-base, at-support-boundary
Context: atr=4 · trend=UP · zones_pre=[4196.90-4197.20] · zones_entry=[4168.00-4169.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4196.10 | 4196.40 | 4191.50 | 4192.00 |

Ticks (bid/ask): 09-16 10:30:02 4191.80/4192.00; 09-16 10:31:40 4168.80/4169.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4191.80
- stop: 4196.60
- R: 4.80
- target(s): 4169.00
- exit: TARGET net 4.75R

#### `GV-P13-V02` · `GT-DARKCLOUD-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P12-V02` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Zone top 4203.09: distance 0.41 > 0.40 -> not AT_SUPPORT -> variant not qualified (BASE pattern still formed).

Tags: at-support-boundary, variant-not-qualified
Context: atr=4 · trend=UP · zones_pre=[4196.91-4197.20] · zones_entry=[4168.00-4169.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4196.10 | 4196.40 | 4191.50 | 4192.00 |

Ticks (bid/ask): 09-16 10:30:02 4191.80/4192.00

- variant: no event

#### `GV-P13-V03` · `GT-DARKCLOUD-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P12-V03` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Lowest low INSIDE a zone: distance 0 -> AT_SUPPORT.

Tags: at-support
Context: atr=4 · trend=UP · zones_pre=[4195.00-4196.60] · zones_entry=[4168.00-4169.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4196.10 | 4196.40 | 4191.50 | 4192.00 |

Ticks (bid/ask): 09-16 10:30:02 4191.80/4192.00; 09-16 10:31:40 4168.80/4169.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4191.80
- stop: 4196.60
- R: 4.80
- target(s): 4169.00
- exit: TARGET net 4.75R

#### `GV-P13-V04` · `GT-DARKCLOUD-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P12-V04` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> No support zone at all: not qualified.

Tags: variant-not-qualified
Context: atr=4 · trend=UP · zones_entry=[4168.00-4169.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4196.10 | 4196.40 | 4191.50 | 4192.00 |

Ticks (bid/ask): 09-16 10:30:02 4191.80/4192.00

- variant: no event

#### `GV-P13-V05` · `GT-DARKCLOUD-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P12-V05` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> The only nearby zone is DEAD: not AT_SUPPORT (dead zones are not levels).

Tags: dead-zone, variant-not-qualified
Context: atr=4 · trend=UP · zones_pre=[4196.90-4197.20 DEAD] · zones_entry=[4168.00-4169.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4196.10 | 4196.40 | 4191.50 | 4192.00 |

Ticks (bid/ask): 09-16 10:30:02 4191.80/4192.00

- variant: no event

#### `GV-P13-V08` · `GT-DARKCLOUD-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P12-V08` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Stopped out at 4203.40.

Tags: variant, sl-first-ticks
Context: atr=4 · trend=UP · zones_pre=[4196.90-4197.20] · zones_entry=[4168.00-4169.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4196.10 | 4196.40 | 4191.50 | 4192.00 |

Ticks (bid/ask): 09-16 10:30:02 4191.80/4192.00; 09-16 10:31:40 4196.40/4196.60

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4191.80
- stop: 4196.60
- R: 4.80
- target(s): 4169.00
- exit: STOP net -1.00R

#### `GV-P13-V09` · `GT-DARKCLOUD-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-P12-V09` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> No live zone above the entry -> SKIPPED_SRC_NO_TARGET.

Tags: T_SR, no-target
Context: atr=4 · trend=UP · zones_pre=[4196.90-4197.20]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4196.10 | 4196.40 | 4191.50 | 4192.00 |

Ticks (bid/ask): 09-16 10:30:02 4191.80/4192.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4191.80
- stop: 4196.60
- R: 4.80

#### `GV-P13-V20` · `GT-DARKCLOUD-BEAR-v1.0/SRC-PS` · M15
> SRC-PS Dark Cloud Cover: minimum reward is 1.5R (T_SR(1.5)), unlike Piercing Line's 2.0R. Entry (SELL at the bid) 4191.80, stop H2+0.20 = 4196.60, R 4.80; zone top 4184.60 is exactly 1.5R away -> accepted.

Tags: T_SR, boundary, asymmetry
Context: atr=4 · trend=UP · zones_pre=[4196.90-4197.20] · zones_entry=[4183.00-4184.60]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4196.10 | 4196.40 | 4191.50 | 4192.00 |

Ticks (bid/ask): 09-16 10:30:02 4191.80/4192.00; 09-16 10:31:40 4184.40/4184.60

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4191.80
- stop: 4196.60
- R: 4.80
- target(s): 4184.60
- exit: TARGET net 1.50R

#### `GV-P13-V21` · `GT-DARKCLOUD-BEAR-v1.0/SRC-PS` · M15
> Zone top 4184.61 -> 7.19/4.80 = 1.498R -> SKIPPED_SRC_RR.

Tags: T_SR, boundary, insufficient-rr, asymmetry
Context: atr=4 · trend=UP · zones_pre=[4196.90-4197.20] · zones_entry=[4183.00-4184.61]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4196.10 | 4196.40 | 4191.50 | 4192.00 |

Ticks (bid/ask): 09-16 10:30:02 4191.80/4192.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4191.80
- stop: 4196.60
- R: 4.80

