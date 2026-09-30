# P22 Inside Bar Sweep Reclaim — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.3 · vector pack GV-0.2 · **80 vectors** (80 firm)

Strategies covered: `GT-IBSR-BEAR-v1.0`, `GT-IBSR-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-IBSR-BEAR-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4200.01/4191.00/4194.00 | UP | 4 | shape ✔ · formed ✔ | — | Pierce by exactly one tick (L3 = 4199.99): qualifies. |
| `B02m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4200.00/4191.00/4194.00 ; 4193.00/4200.50/4191.00/4194.00 | UP | 4 | shape ✔ · formed ✔ | — | Bar 3 low equals the mother low (no pierce): the bar is skipped; bar 4 is the first piercing bar and forms the signal (formation_end_bar index 3). |
| `B03m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4200.50/4191.00/4200.00 | UP | 4 | shape ✔ · formed ✔ | — | Close exactly on the mother low (4200.00): 'closes back inside [L1,H1]' is inclusive -> qualifies. |
| `B04m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4200.50/4191.00/4200.01 | UP | 4 | no shape | — | Close 0.01 below the mother low: it CLOSED outside -> that is a breakout (P09), not a sweep. No P22 signal. |
| `B05m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4200.50/4184.50/4194.00 | UP | 4 | no shape | — | Bar 3 pierces BOTH sides (H 4215.50 > H1 and L 4199.50 < L1): NO_SIGNAL_AMBIGUOUS_BOTH_SIDES. |
| `B06m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4196.50/4191.00/4194.00 ; 4194.00/4196.40/4191.00/4194.00 ; 4193.00/4200.50/4191.00/4194.00 | UP | 4 | shape ✔ · formed ✔ | — | Sweep on bar 5 (the last allowed bar; two quiet inside-range bars before it): qualifies. |
| `B07m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4196.50/4191.00/4194.00 ; 4194.00/4196.40/4191.00/4194.00 ; 4194.00/4196.30/4191.00/4194.00 ; 4193.00/4200.50/4191.00/4194.00 | UP | 4 | no shape | — | The only sweep is on bar 6: outside the bar 3-5 window -> no signal. |
| `B08m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4205.00/4191.00/4202.00 ; 4193.00/4200.50/4191.00/4194.00 | UP | 4 | no shape | — | Bar 3 pierces and closes OUTSIDE (a breakout): it is the FIRST piercing bar, so the later sweep on bar 4 does not count. |
| `B09m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4185.00/4191.00 ; 4193.00/4200.50/4191.00/4194.00 | UP | 4 | no shape | — | Inside bar touches the mother high exactly (H2 = H1): not strictly inside -> no P22. |
| `B10m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4196.00/4184.00/4191.00 | UP | 4 | no shape | — | Bar 3 pierces the OTHER side (high) and closes back inside... but the BULL strategy needs the LOW pierced, so no bullish signal here. |
| `B11` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4209.00/4199.50/4206.00 | DOWN | 4 | no shape | — | The BEAR strategy on a low sweep: no signal (sells need the HIGH pierced). |
| `NZ1m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4196.50/4191.00/4194.00 ; 4194.00/4196.40/4191.00/4194.00 ; 4194.00/4196.30/4191.00/4194.00 | UP | 4 | canonical: no event; variant: no event | — | Inside bar followed by three bars that never pierce the mother range: no sweep. |
| `T01m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4200.50/4191.00/4194.00 | DOWN | 4 | shape ✔ · formed ✔ | — | BASE Sweep & Reclaim has no prior state: formed with trend UP. |
| `T02m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4200.50/4191.00/4194.00 | RANGE | 4 | shape ✔ · formed ✔ | — | BASE Sweep & Reclaim has no prior state: formed with trend RANGE. |
| `T03m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4200.50/4191.00/4194.00 | UNDETERMINED | 4 | shape ✔ · formed ✔ | — | BASE Sweep & Reclaim has no prior state: formed with trend UNDETERMINED. |
| `T04m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4200.50/4191.00/4194.00 | UP | 4 | shape ✔ · formed ✔ | — | BASE Sweep & Reclaim has no prior state: formed with trend DOWN. |
| `Y00m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4200.50/4191.00/4194.00 | UP | 4 | shape ✔ · formed ✔ | — | Bullish sweep: bar 3 pierces the mother low by 0.50 (4199.50 < 4200.00), closes back inside (4206), first piercing bar -> signal at bar 3 completion. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01m` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:45:02 4193.80/4194.00; 09-16 10:47:00 4190.35/4190.55; 09-16 10:50:00 4179.80/4180.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4193.80; stop: 4200.70; R: 6.90; target(s): 4180.00; exit: TARGET net 2.00R |
| `L02m` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:45:02 4193.80/4194.00; 09-16 10:47:00 4197.25/4197.45; 09-16 10:50:00 4200.50/4200.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4193.80; stop: 4200.70; R: 6.90; target(s): 4180.00; exit: STOP net -1.00R |
| `L03m` | Tick gaps through the stop (bid 4197.30 < stop): fill = that tick's bid, not the stop (G9): -89/69R. | 09-16 10:45:02 4193.80/4194.00; 09-16 10:47:00 4202.50/4202.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4193.80; stop: 4200.70; R: 6.90; target(s): 4180.00; exit: STOP net -89/69 (≈-1.2899)R |
| `L04m` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:45:02 4193.80/4194.00; 09-16 10:46:40 4200.50/4200.70; 09-16 10:48:20 4179.80/4180.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4193.80; stop: 4200.70; R: 6.90; target(s): 4180.00; exit: STOP net -1.00R |
| `L05m` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:45:02 4193.80/4194.00; 09-16 10:46:40 4179.80/4180.00; 09-16 10:48:20 4200.50/4200.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4193.80; stop: 4200.70; R: 6.90; target(s): 4180.00; exit: TARGET net 2.00R |
| `L06m` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:45:02 4193.80/4194.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4193.80; stop: 4200.70; R: 6.90; target(s): 4180.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07m` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:45:02 4193.50/4194.00; 09-16 10:48:20 4178.60/4179.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; spread_at_entry: 0.50; entry: 4193.50; stop: 4200.70; R: 7.20; target(s): 4179.10; exit: TARGET net 2.00R |
| `L08m` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 11:00:00 4193.80/4194.00; 09-16 11:01:40 4179.80/4180.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4193.80; stop: 4200.70; R: 6.90; target(s): 4180.00; exit: TARGET net 2.00R |
| `L09m` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 11:00:01 4193.80/4194.00; 09-16 11:01:40 4179.80/4180.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10m` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:45:02 4198.70/4199.20; 09-16 10:46:40 4194.20/4194.70 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4198.70; R: 2.00; target(s): 4194.70; exit: TARGET net 2.00R |
| `L11m` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:45:02 4198.71/4199.21; 09-16 10:46:40 4194.21/4194.71 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12m` | Tick jumps far past the target (bid 4226.40 > target 4220.00): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:45:02 4193.80/4194.00; 09-16 10:47:00 4173.40/4173.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4193.80; stop: 4200.70; R: 6.90; target(s): 4180.00; exit: TARGET net 2.00R |
| `W01m` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4193.80/4194.00; 09-21 00:30:00 4179.80/4180.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4193.80; stop: 4200.70; R: 6.90; target(s): 4180.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W02m` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4193.80/4194.00; 09-21 00:30:00 4179.80/4180.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4193.80; stop: 4200.70; R: 6.90; target(s): 4180.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W03m` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4193.80/4194.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P22-R01m` · `GT-IBSR-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P22-R01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4188.00 | 4200.00 | 4185.00 | 4196.00 |
| 2 | 09-16 10:15 | 4194.00 | 4197.00 | 4190.00 | 4191.00 |
| 3 | 09-16 10:30 | 4193.00 | 4200.50 | 4191.00 | 4194.00 |
| 4 | 09-16 10:45 | 4194.00 | 4196.00 | 4191.00 | 4193.00 |
| 5 | 09-16 11:00 | 4193.00 | 4195.00 | 4190.00 | 4192.00 |
| 6 | 09-16 11:15 | 4192.00 | 4197.00 | 4191.00 | 4195.00 |
| 7 | 09-16 11:30 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 8 | 09-16 11:45 | 4193.00 | 4196.00 | 4189.00 | 4191.00 |
| 9 | 09-16 12:00 | 4191.00 | 4203.00 | 4185.00 | 4190.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4194.00 | h1: ret=1.00, mfe=3.00, mae=2.00, end_index=3 | h3: ret=-1.00, mfe=4.00, mae=3.00, end_index=5 | h5: ret=3.00, mfe=5.00, mae=4.00, end_index=7 | h10: NULL | h20: NULL

#### `GV-P22-Y01m` · `GT-IBSR-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P22-Y01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4188.00 | 4200.00 | 4185.00 | 4196.00 |
| 2 | 09-16 10:15 | 4194.00 | 4197.00 | 4190.00 | 4191.00 |
| 3 | 09-16 10:30 | 4193.00 | 4200.50 | 4191.00 | 4194.00 |

Ticks (bid/ask): 09-16 10:45:02 4193.80/4194.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:45:00Z
- entry: 4193.80
- stop: 4200.70
- R: 6.90
- target(s): 4180.00

### Variant `SRC-CB`

#### `GV-P22-V01m` · `GT-IBSR-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P22-V01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> SRC-CB Sweep & Reclaim (bull): TREND DOWN satisfies 'TREND=DOWN OR AT_SUPPORT'; H1 allowed. Stop = sweep low - 0.20 = 4199.30; entry ask 4206.20; R 6.90; T_SR(2.0) = zone edge 4220.00 = 2.0R exactly -> trade.

Tags: variant-clean-yes, boundary
Context: atr=4 · trend=UP · zones_entry=[4179.00-4180.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4188.00 | 4200.00 | 4185.00 | 4196.00 |
| 2 | 09-16 11:00 | 4194.00 | 4197.00 | 4190.00 | 4191.00 |
| 3 | 09-16 12:00 | 4193.00 | 4200.50 | 4191.00 | 4194.00 |

Ticks (bid/ask): 09-16 13:00:02 4193.80/4194.00; 09-16 13:01:40 4179.80/4180.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4193.80
- stop: 4200.70
- R: 6.90
- target(s): 4180.00
- exit: TARGET net 2.00R

#### `GV-P22-V02m` · `GT-IBSR-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P22-V02` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Trend UP but the sweep low (4199.50) is INSIDE a support zone: 'OR AT_SUPPORT' -> qualifies.

Tags: or-condition
Context: atr=4 · trend=DOWN · zones_pre=[4200.40-4201.50] · zones_entry=[4179.00-4180.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4188.00 | 4200.00 | 4185.00 | 4196.00 |
| 2 | 09-16 11:00 | 4194.00 | 4197.00 | 4190.00 | 4191.00 |
| 3 | 09-16 12:00 | 4193.00 | 4200.50 | 4191.00 | 4194.00 |

Ticks (bid/ask): 09-16 13:00:02 4193.80/4194.00; 09-16 13:01:40 4179.80/4180.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4193.80
- stop: 4200.70
- R: 6.90
- target(s): 4180.00
- exit: TARGET net 2.00R

#### `GV-P22-V03m` · `GT-IBSR-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P22-V03` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Trend UP and no support: neither branch true -> not qualified (BASE formed).

Tags: or-condition, variant-not-qualified
Context: atr=4 · trend=DOWN · zones_entry=[4179.00-4180.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4188.00 | 4200.00 | 4185.00 | 4196.00 |
| 2 | 09-16 11:00 | 4194.00 | 4197.00 | 4190.00 | 4191.00 |
| 3 | 09-16 12:00 | 4193.00 | 4200.50 | 4191.00 | 4194.00 |

Ticks (bid/ask): 09-16 13:00:02 4193.80/4194.00

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P22-V04m` · `GT-IBSR-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P22-V04` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Zone edge 4219.99 -> 1.9986R -> SKIPPED_SRC_RR.

Tags: T_SR, boundary, insufficient-rr
Context: atr=4 · trend=UP · zones_entry=[4179.00-4180.01]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4188.00 | 4200.00 | 4185.00 | 4196.00 |
| 2 | 09-16 11:00 | 4194.00 | 4197.00 | 4190.00 | 4191.00 |
| 3 | 09-16 12:00 | 4193.00 | 4200.50 | 4191.00 | 4194.00 |

Ticks (bid/ask): 09-16 13:00:02 4193.80/4194.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4193.80
- stop: 4200.70
- R: 6.90

#### `GV-P22-V05m` · `GT-IBSR-BEAR-v1.0/SRC-CB` · M30
*Mirror of `GV-P22-V05` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> M30 not allowed -> SKIPPED_TF_NOT_ALLOWED.

Tags: tf-gate
Context: atr=4 · trend=UP · zones_entry=[4179.00-4180.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4188.00 | 4200.00 | 4185.00 | 4196.00 |
| 2 | 09-16 10:30 | 4194.00 | 4197.00 | 4190.00 | 4191.00 |
| 3 | 09-16 11:00 | 4193.00 | 4200.50 | 4191.00 | 4194.00 |

Ticks (bid/ask): 09-16 11:30:02 4193.80/4194.00

- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

#### `GV-P22-V06m` · `GT-IBSR-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P22-V06` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> No zone above the entry -> SKIPPED_SRC_NO_TARGET.

Tags: T_SR, no-target
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4188.00 | 4200.00 | 4185.00 | 4196.00 |
| 2 | 09-16 11:00 | 4194.00 | 4197.00 | 4190.00 | 4191.00 |
| 3 | 09-16 12:00 | 4193.00 | 4200.50 | 4191.00 | 4194.00 |

Ticks (bid/ask): 09-16 13:00:02 4193.80/4194.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4193.80
- stop: 4200.70
- R: 6.90

## `GT-IBSR-BULL-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4209.00/4199.99/4206.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Pierce by exactly one tick (L3 = 4199.99): qualifies. |
| `B02` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4209.00/4200.00/4206.00 ; 4207.00/4209.00/4199.50/4206.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Bar 3 low equals the mother low (no pierce): the bar is skipped; bar 4 is the first piercing bar and forms the signal (formation_end_bar index 3). |
| `B03` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4209.00/4199.50/4200.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Close exactly on the mother low (4200.00): 'closes back inside [L1,H1]' is inclusive -> qualifies. |
| `B04` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4209.00/4199.50/4199.99 | DOWN | 4 | no shape | — | Close 0.01 below the mother low: it CLOSED outside -> that is a breakout (P09), not a sweep. No P22 signal. |
| `B05` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4215.50/4199.50/4206.00 | DOWN | 4 | no shape | — | Bar 3 pierces BOTH sides (H 4215.50 > H1 and L 4199.50 < L1): NO_SIGNAL_AMBIGUOUS_BOTH_SIDES. |
| `B06` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4209.00/4203.50/4206.00 ; 4206.00/4209.00/4203.60/4206.00 ; 4207.00/4209.00/4199.50/4206.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Sweep on bar 5 (the last allowed bar; two quiet inside-range bars before it): qualifies. |
| `B07` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4209.00/4203.50/4206.00 ; 4206.00/4209.00/4203.60/4206.00 ; 4206.00/4209.00/4203.70/4206.00 ; 4207.00/4209.00/4199.50/4206.00 | DOWN | 4 | no shape | — | The only sweep is on bar 6: outside the bar 3-5 window -> no signal. |
| `B08` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4209.00/4195.00/4198.00 ; 4207.00/4209.00/4199.50/4206.00 | DOWN | 4 | no shape | — | Bar 3 pierces and closes OUTSIDE (a breakout): it is the FIRST piercing bar, so the later sweep on bar 4 does not count. |
| `B09` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4215.00/4203.00/4209.00 ; 4207.00/4209.00/4199.50/4206.00 | DOWN | 4 | no shape | — | Inside bar touches the mother high exactly (H2 = H1): not strictly inside -> no P22. |
| `B10` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4216.00/4204.00/4209.00 | DOWN | 4 | no shape | — | Bar 3 pierces the OTHER side (high) and closes back inside... but the BULL strategy needs the LOW pierced, so no bullish signal here. |
| `B11m` | 4188.00/4200.00/4185.00/4196.00 ; 4194.00/4197.00/4190.00/4191.00 ; 4193.00/4200.50/4191.00/4194.00 | UP | 4 | no shape | — | The BEAR strategy on a low sweep: no signal (sells need the HIGH pierced). |
| `NZ1` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4209.00/4203.50/4206.00 ; 4206.00/4209.00/4203.60/4206.00 ; 4206.00/4209.00/4203.70/4206.00 | DOWN | 4 | canonical: no event; variant: no event | — | Inside bar followed by three bars that never pierce the mother range: no sweep. |
| `T01` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4209.00/4199.50/4206.00 | UP | 4 | shape ✔ · formed ✔ | — | BASE Sweep & Reclaim has no prior state: formed with trend UP. |
| `T02` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4209.00/4199.50/4206.00 | RANGE | 4 | shape ✔ · formed ✔ | — | BASE Sweep & Reclaim has no prior state: formed with trend RANGE. |
| `T03` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4209.00/4199.50/4206.00 | UNDETERMINED | 4 | shape ✔ · formed ✔ | — | BASE Sweep & Reclaim has no prior state: formed with trend UNDETERMINED. |
| `T04` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4209.00/4199.50/4206.00 | DOWN | 4 | shape ✔ · formed ✔ | — | BASE Sweep & Reclaim has no prior state: formed with trend DOWN. |
| `Y00` | 4212.00/4215.00/4200.00/4204.00 ; 4206.00/4210.00/4203.00/4209.00 ; 4207.00/4209.00/4199.50/4206.00 | DOWN | 4 | shape ✔ · formed ✔ | — | Bullish sweep: bar 3 pierces the mother low by 0.50 (4199.50 < 4200.00), closes back inside (4206), first piercing bar -> signal at bar 3 completion. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:45:02 4206.00/4206.20; 09-16 10:47:00 4209.45/4209.65; 09-16 10:50:00 4220.00/4220.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4206.20; stop: 4199.30; R: 6.90; target(s): 4220.00; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:45:02 4206.00/4206.20; 09-16 10:47:00 4202.55/4202.75; 09-16 10:50:00 4199.30/4199.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4206.20; stop: 4199.30; R: 6.90; target(s): 4220.00; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4197.30 < stop): fill = that tick's bid, not the stop (G9): -89/69R. | 09-16 10:45:02 4206.00/4206.20; 09-16 10:47:00 4197.30/4197.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4206.20; stop: 4199.30; R: 6.90; target(s): 4220.00; exit: STOP net -89/69 (≈-1.2899)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:45:02 4206.00/4206.20; 09-16 10:46:40 4199.30/4199.50; 09-16 10:48:20 4220.00/4220.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4206.20; stop: 4199.30; R: 6.90; target(s): 4220.00; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:45:02 4206.00/4206.20; 09-16 10:46:40 4220.00/4220.20; 09-16 10:48:20 4199.30/4199.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4206.20; stop: 4199.30; R: 6.90; target(s): 4220.00; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:45:02 4206.00/4206.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4206.20; stop: 4199.30; R: 6.90; target(s): 4220.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:45:02 4206.00/4206.50; 09-16 10:48:20 4220.90/4221.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; spread_at_entry: 0.50; entry: 4206.50; stop: 4199.30; R: 7.20; target(s): 4220.90; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 11:00:00 4206.00/4206.20; 09-16 11:01:40 4220.00/4220.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4206.20; stop: 4199.30; R: 6.90; target(s): 4220.00; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 11:00:01 4206.00/4206.20; 09-16 11:01:40 4220.00/4220.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:45:02 4200.80/4201.30; 09-16 10:46:40 4205.30/4205.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4201.30; R: 2.00; target(s): 4205.30; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:45:02 4200.79/4201.29; 09-16 10:46:40 4205.29/4205.79 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4226.40 > target 4220.00): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:45:02 4206.00/4206.20; 09-16 10:47:00 4226.40/4226.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4206.20; stop: 4199.30; R: 6.90; target(s): 4220.00; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4206.00/4206.20; 09-21 00:30:00 4220.00/4220.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4206.20; stop: 4199.30; R: 6.90; target(s): 4220.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4206.00/4206.20; 09-21 00:30:00 4220.00/4220.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4206.20; stop: 4199.30; R: 6.90; target(s): 4220.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4206.00/4206.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P22-R01` · `GT-IBSR-BULL-v1.0/BASE` · M15
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4212.00 | 4215.00 | 4200.00 | 4204.00 |
| 2 | 09-16 10:15 | 4206.00 | 4210.00 | 4203.00 | 4209.00 |
| 3 | 09-16 10:30 | 4207.00 | 4209.00 | 4199.50 | 4206.00 |
| 4 | 09-16 10:45 | 4206.00 | 4209.00 | 4204.00 | 4207.00 |
| 5 | 09-16 11:00 | 4207.00 | 4210.00 | 4205.00 | 4208.00 |
| 6 | 09-16 11:15 | 4208.00 | 4209.00 | 4203.00 | 4205.00 |
| 7 | 09-16 11:30 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 8 | 09-16 11:45 | 4207.00 | 4211.00 | 4204.00 | 4209.00 |
| 9 | 09-16 12:00 | 4209.00 | 4215.00 | 4197.00 | 4210.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4206.00 | h1: ret=1.00, mfe=3.00, mae=2.00, end_index=3 | h3: ret=-1.00, mfe=4.00, mae=3.00, end_index=5 | h5: ret=3.00, mfe=5.00, mae=4.00, end_index=7 | h10: NULL | h20: NULL

#### `GV-P22-Y01` · `GT-IBSR-BULL-v1.0/BASE` · M15
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4212.00 | 4215.00 | 4200.00 | 4204.00 |
| 2 | 09-16 10:15 | 4206.00 | 4210.00 | 4203.00 | 4209.00 |
| 3 | 09-16 10:30 | 4207.00 | 4209.00 | 4199.50 | 4206.00 |

Ticks (bid/ask): 09-16 10:45:02 4206.00/4206.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:45:00Z
- entry: 4206.20
- stop: 4199.30
- R: 6.90
- target(s): 4220.00

### Variant `SRC-CB`

#### `GV-P22-V01` · `GT-IBSR-BULL-v1.0/SRC-CB` · H1
> SRC-CB Sweep & Reclaim (bull): TREND DOWN satisfies 'TREND=DOWN OR AT_SUPPORT'; H1 allowed. Stop = sweep low - 0.20 = 4199.30; entry ask 4206.20; R 6.90; T_SR(2.0) = zone edge 4220.00 = 2.0R exactly -> trade.

Tags: variant-clean-yes, boundary
Context: atr=4 · trend=DOWN · zones_entry=[4220.00-4221.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4212.00 | 4215.00 | 4200.00 | 4204.00 |
| 2 | 09-16 11:00 | 4206.00 | 4210.00 | 4203.00 | 4209.00 |
| 3 | 09-16 12:00 | 4207.00 | 4209.00 | 4199.50 | 4206.00 |

Ticks (bid/ask): 09-16 13:00:02 4206.00/4206.20; 09-16 13:01:40 4220.00/4220.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4206.20
- stop: 4199.30
- R: 6.90
- target(s): 4220.00
- exit: TARGET net 2.00R

#### `GV-P22-V02` · `GT-IBSR-BULL-v1.0/SRC-CB` · H1
> Trend UP but the sweep low (4199.50) is INSIDE a support zone: 'OR AT_SUPPORT' -> qualifies.

Tags: or-condition
Context: atr=4 · trend=UP · zones_pre=[4198.50-4199.60] · zones_entry=[4220.00-4221.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4212.00 | 4215.00 | 4200.00 | 4204.00 |
| 2 | 09-16 11:00 | 4206.00 | 4210.00 | 4203.00 | 4209.00 |
| 3 | 09-16 12:00 | 4207.00 | 4209.00 | 4199.50 | 4206.00 |

Ticks (bid/ask): 09-16 13:00:02 4206.00/4206.20; 09-16 13:01:40 4220.00/4220.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4206.20
- stop: 4199.30
- R: 6.90
- target(s): 4220.00
- exit: TARGET net 2.00R

#### `GV-P22-V03` · `GT-IBSR-BULL-v1.0/SRC-CB` · H1
> Trend UP and no support: neither branch true -> not qualified (BASE formed).

Tags: or-condition, variant-not-qualified
Context: atr=4 · trend=UP · zones_entry=[4220.00-4221.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4212.00 | 4215.00 | 4200.00 | 4204.00 |
| 2 | 09-16 11:00 | 4206.00 | 4210.00 | 4203.00 | 4209.00 |
| 3 | 09-16 12:00 | 4207.00 | 4209.00 | 4199.50 | 4206.00 |

Ticks (bid/ask): 09-16 13:00:02 4206.00/4206.20

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P22-V04` · `GT-IBSR-BULL-v1.0/SRC-CB` · H1
> Zone edge 4219.99 -> 1.9986R -> SKIPPED_SRC_RR.

Tags: T_SR, boundary, insufficient-rr
Context: atr=4 · trend=DOWN · zones_entry=[4219.99-4221.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4212.00 | 4215.00 | 4200.00 | 4204.00 |
| 2 | 09-16 11:00 | 4206.00 | 4210.00 | 4203.00 | 4209.00 |
| 3 | 09-16 12:00 | 4207.00 | 4209.00 | 4199.50 | 4206.00 |

Ticks (bid/ask): 09-16 13:00:02 4206.00/4206.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4206.20
- stop: 4199.30
- R: 6.90

#### `GV-P22-V05` · `GT-IBSR-BULL-v1.0/SRC-CB` · M30
> M30 not allowed -> SKIPPED_TF_NOT_ALLOWED.

Tags: tf-gate
Context: atr=4 · trend=DOWN · zones_entry=[4220.00-4221.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4212.00 | 4215.00 | 4200.00 | 4204.00 |
| 2 | 09-16 10:30 | 4206.00 | 4210.00 | 4203.00 | 4209.00 |
| 3 | 09-16 11:00 | 4207.00 | 4209.00 | 4199.50 | 4206.00 |

Ticks (bid/ask): 09-16 11:30:02 4206.00/4206.20

- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

#### `GV-P22-V06` · `GT-IBSR-BULL-v1.0/SRC-CB` · H1
> No zone above the entry -> SKIPPED_SRC_NO_TARGET.

Tags: T_SR, no-target
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4212.00 | 4215.00 | 4200.00 | 4204.00 |
| 2 | 09-16 11:00 | 4206.00 | 4210.00 | 4203.00 | 4209.00 |
| 3 | 09-16 12:00 | 4207.00 | 4209.00 | 4199.50 | 4206.00 |

Ticks (bid/ask): 09-16 13:00:02 4206.00/4206.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4206.20
- stop: 4199.30
- R: 6.90

