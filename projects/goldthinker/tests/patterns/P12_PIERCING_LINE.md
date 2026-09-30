# P12 Piercing Line — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.3.1 · vector pack GV-0.2 · **51 vectors** (51 firm)

Strategies covered: `GT-PIERCING-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-PIERCING-BULL-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4210.00/4210.50/4203.50/4204.00 ; 4204.00/4208.50/4203.50/4208.00 | DOWN | 4 | no shape | O2<C1 | O2 equals C1 exactly (4204.00): not strictly below -> fails O2<C1 only. |
| `B02` | 4210.00/4210.50/4203.50/4204.00 ; 4203.99/4208.50/4203.50/4208.00 | DOWN | 4 | shape ✔ · formed ✔ | — | O2 = C1 - 0.01: passes. |
| `B03` | 4210.00/4210.50/4203.50/4204.00 ; 4203.00/4207.50/4202.50/4207.00 | DOWN | 4 | no shape | C2>mid1 | C2 exactly at the midpoint (4207.00): fails C2>mid1 (strict) only. |
| `B04` | 4210.00/4210.50/4203.50/4204.00 ; 4203.00/4207.50/4202.50/4207.01 | DOWN | 4 | shape ✔ · formed ✔ | — | C2 = midpoint + 0.01: passes. |
| `B05` | 4210.00/4210.50/4203.50/4204.00 ; 4203.00/4210.50/4202.50/4210.00 | DOWN | 4 | no shape | C2<O1 | C2 equals O1 exactly (4210.00): fails C2<O1 (strict) only - the Bullish Engulfing side of the split. |
| `B06` | 4210.00/4210.50/4203.50/4204.00 ; 4203.00/4210.00/4202.50/4209.99 | DOWN | 4 | shape ✔ · formed ✔ | — | C2 = O1 - 0.01: passes. |
| `F01` | 4210.00/4210.50/4203.50/4204.00 ; 4203.30/4208.50/4202.50/4208.00 | DOWN | 4 | shape ✔ · formed ✔ | — | gap_thr = max(0.10, 0.05*4)=0.20; L1=4203.50, so gap needs O2 <= 4203.30: exactly 4203.30 -> gap_flag true. |
| `F02` | 4210.00/4210.50/4203.50/4204.00 ; 4203.31/4208.50/4202.50/4208.00 | DOWN | 4 | shape ✔ · formed ✔ | — | O2 = 4203.31: gap_flag false; the pattern still forms (a gap is not required). |
| `LG01` | 4210.00/4210.60/4207.00/4207.60 ; 4207.00/4209.20/4206.50/4209.00 | DOWN | 4 | shape ✔ · formed ✔ | — | LARGE(C1) exactly on B = 2.40 (R=3.6): passes. |
| `LG02` | 4210.00/4210.60/4207.00/4207.61 ; 4207.00/4209.20/4206.50/4209.00 | DOWN | 4 | no shape | LARGE(K1) | LARGE(C1) with B = 2.39: fails LARGE only. |
| `LG03` | 4210.00/4210.20/4207.00/4207.00 ; 4206.50/4209.50/4206.00/4209.00 | DOWN | 4 | shape ✔ · formed ✔ | — | LARGE(C1) exactly on R = 3.20 (B=3.0): passes. |
| `LG04` | 4210.00/4210.19/4207.00/4207.00 ; 4206.50/4209.50/4206.00/4209.00 | DOWN | 4 | no shape | LARGE(K1) | LARGE(C1) with R = 3.19: fails LARGE only. |
| `LG05` | 4210.00/4211.00/4206.00/4207.00 ; 4206.50/4209.50/4206.00/4209.00 | DOWN | 4 | shape ✔ · formed ✔ | — | LARGE(C1) exactly on B/R = 0.60 (B=3, R=5): passes. |
| `LG06` | 4210.00/4211.01/4206.00/4207.00 ; 4206.50/4209.50/4206.00/4209.00 | DOWN | 4 | no shape | LARGE(K1) | LARGE(C1) with B/R just below 0.60 (B=3, R=5.01): fails LARGE only. |
| `N01` | 4204.00/4211.00/4203.50/4210.00 ; 4203.00/4208.50/4202.50/4208.00 | DOWN | 4 | no shape | K1 bear, C2<O1 | C1 bullish (a bullish first candle can never be pierced): fails colour (and mid/O1 relations). |
| `NZ1` | 4200.00/4204.50/4199.50/4204.00 ; 4204.00/4208.50/4203.50/4208.00 | DOWN | 4 | canonical: no event; variant: no event | — | Two bullish candles: nothing to pierce. |
| `T01` | 4210.00/4210.50/4203.50/4204.00 ; 4203.00/4208.50/4202.50/4208.00 | UP | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Piercing shape after UP: not formed. |
| `T02` | 4210.00/4210.50/4203.50/4204.00 ; 4203.00/4208.50/4202.50/4208.00 | RANGE | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Piercing shape after RANGE: not formed. |
| `T03` | 4210.00/4210.50/4203.50/4204.00 ; 4203.00/4208.50/4202.50/4208.00 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Piercing shape after UNDETERMINED: not formed. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:30:02 4208.00/4208.20; 09-16 10:32:00 4210.95/4211.15; 09-16 10:35:00 4220.00/4220.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4208.20; stop: 4202.30; R: 5.90; target(s): 4220.00; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:30:02 4208.00/4208.20; 09-16 10:32:00 4205.05/4205.25; 09-16 10:35:00 4202.30/4202.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4208.20; stop: 4202.30; R: 5.90; target(s): 4220.00; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4200.30 < stop): fill = that tick's bid, not the stop (G9): -79/59R. | 09-16 10:30:02 4208.00/4208.20; 09-16 10:32:00 4200.30/4200.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4208.20; stop: 4202.30; R: 5.90; target(s): 4220.00; exit: STOP net -79/59 (≈-1.3390)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:30:02 4208.00/4208.20; 09-16 10:31:40 4202.30/4202.50; 09-16 10:33:20 4220.00/4220.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4208.20; stop: 4202.30; R: 5.90; target(s): 4220.00; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:30:02 4208.00/4208.20; 09-16 10:31:40 4220.00/4220.20; 09-16 10:33:20 4202.30/4202.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4208.20; stop: 4202.30; R: 5.90; target(s): 4220.00; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:30:02 4208.00/4208.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4208.20; stop: 4202.30; R: 5.90; target(s): 4220.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:30:02 4208.00/4208.50; 09-16 10:33:20 4220.90/4221.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; spread_at_entry: 0.50; entry: 4208.50; stop: 4202.30; R: 6.20; target(s): 4220.90; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:45:00 4208.00/4208.20; 09-16 10:46:40 4220.00/4220.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4208.20; stop: 4202.30; R: 5.90; target(s): 4220.00; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:45:01 4208.00/4208.20; 09-16 10:46:40 4220.00/4220.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:30:02 4203.80/4204.30; 09-16 10:31:40 4208.30/4208.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4204.30; R: 2.00; target(s): 4208.30; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:30:02 4203.79/4204.29; 09-16 10:31:40 4208.29/4208.79 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4226.40 > target 4220.00): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:30:02 4208.00/4208.20; 09-16 10:32:00 4226.40/4226.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4208.20; stop: 4202.30; R: 5.90; target(s): 4220.00; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4208.00/4208.20; 09-21 00:30:00 4220.00/4220.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4208.20; stop: 4202.30; R: 5.90; target(s): 4220.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4208.00/4208.20; 09-21 00:30:00 4220.00/4220.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4208.20; stop: 4202.30; R: 5.90; target(s): 4220.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4208.00/4208.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P12-R01` · `GT-PIERCING-BULL-v1.0/BASE` · M15
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4203.00 | 4208.50 | 4202.50 | 4208.00 |
| 3 | 09-16 10:30 | 4208.00 | 4211.00 | 4206.00 | 4209.00 |
| 4 | 09-16 10:45 | 4209.00 | 4212.00 | 4207.00 | 4210.00 |
| 5 | 09-16 11:00 | 4210.00 | 4211.00 | 4205.00 | 4207.00 |
| 6 | 09-16 11:15 | 4207.00 | 4210.00 | 4204.00 | 4208.00 |
| 7 | 09-16 11:30 | 4209.00 | 4213.00 | 4206.00 | 4211.00 |
| 8 | 09-16 11:45 | 4211.00 | 4217.00 | 4199.00 | 4212.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4208.00 | h1: ret=1.00, mfe=3.00, mae=2.00, end_index=2 | h3: ret=-1.00, mfe=4.00, mae=3.00, end_index=4 | h5: ret=3.00, mfe=5.00, mae=4.00, end_index=6 | h10: NULL | h20: NULL

#### `GV-P12-Y01` · `GT-PIERCING-BULL-v1.0/BASE` · M15
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4203.00 | 4208.50 | 4202.50 | 4208.00 |

Ticks (bid/ask): 09-16 10:30:02 4208.00/4208.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4208.20
- stop: 4202.30
- R: 5.90
- target(s): 4220.00

### Variant `SRC-PS`

#### `GV-P12-S01` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> Signal at 03:15 UTC (Sept, BST): Tokyo 12:15 in ASIA, London 04:15 closed, NY closed -> ASIA_ONLY -> skipped.

Tags: session, asia-only
Context: atr=4 · trend=DOWN · zones_pre=[4202.80-4203.10] · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 02:45 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 03:00 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 09-16 03:15:02 4208.00/4208.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SESSION_FILTER
- signal time: 2026-09-16T03:15:00Z

#### `GV-P12-S02` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> Signal 06:45 UTC = 07:45 London BST: London not open yet (opens 08:00 local) -> still ASIA_ONLY -> skipped.

Tags: session, asia-only
Context: atr=4 · trend=DOWN · zones_pre=[4202.80-4203.10] · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 06:15 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 06:30 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 09-16 06:45:02 4208.00/4208.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SESSION_FILTER
- signal time: 2026-09-16T06:45:00Z

#### `GV-P12-S03` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> Signal 07:00 UTC = 08:00 BST: London opens (start inclusive) -> not ASIA_ONLY -> trade.

Tags: session, asia-only
Context: atr=4 · trend=DOWN · zones_pre=[4202.80-4203.10] · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 06:30 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 06:45 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 09-16 07:00:02 4208.00/4208.20; 09-16 07:01:40 4231.00/4231.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T07:00:00Z
- entry: 4208.20
- stop: 4203.40
- R: 4.80
- target(s): 4231.00
- exit: TARGET net 4.75R

#### `GV-P12-S04` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> After UK clocks change (26 Oct 2026): 07:45 UTC = 07:45 GMT, London not open -> ASIA_ONLY -> skipped (the same UTC time is tradable in September).

Tags: session, asia-only
Context: atr=4 · trend=DOWN · zones_pre=[4202.80-4203.10] · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 10-27 07:15 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 10-27 07:30 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 10-27 07:45:02 4208.00/4208.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SESSION_FILTER
- signal time: 2026-10-27T07:45:00Z

#### `GV-P12-S05` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> 08:00 UTC = 08:00 GMT: London opens -> trade. (Tokyo 17:00 ends the same instant.)

Tags: session, asia-only
Context: atr=4 · trend=DOWN · zones_pre=[4202.80-4203.10] · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 10-27 07:30 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 10-27 07:45 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 10-27 08:00:02 4208.00/4208.20; 10-27 08:01:40 4231.00/4231.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-10-27T08:00:00Z
- entry: 4208.20
- stop: 4203.40
- R: 4.80
- target(s): 4231.00
- exit: TARGET net 4.75R

#### `GV-P12-S06` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> 08:15 UTC in Sept: London (09:15 BST) open, Tokyo (17:15) closed -> not ASIA_ONLY -> trade.

Tags: session, asia-only
Context: atr=4 · trend=DOWN · zones_pre=[4202.80-4203.10] · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 07:45 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 08:00 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 09-16 08:15:02 4208.00/4208.20; 09-16 08:16:40 4231.00/4231.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T08:15:00Z
- entry: 4208.20
- stop: 4203.40
- R: 4.80
- target(s): 4231.00
- exit: TARGET net 4.75R

#### `GV-P12-V01` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> SRC-PS Piercing: AT_SUPPORT holds (lowest low 4203.50 is 0.40 from the zone top 4203.10 = 0.10*ATR exactly); stop = L2-0.20 = 4203.40 (BASE would use min(L1,L2)-0.20 = 4203.30: source stops below C2's low, not C1's); entry ask 4208.20; R = 4.80; target T_SR(2.0) = zone edge 4231.00 = 4.75R -> trade.

Tags: variant-clean-yes, T_SR, stop-differs-from-base, at-support-boundary
Context: atr=4 · trend=DOWN · zones_pre=[4202.80-4203.10] · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 09-16 10:30:02 4208.00/4208.20; 09-16 10:31:40 4231.00/4231.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4208.20
- stop: 4203.40
- R: 4.80
- target(s): 4231.00
- exit: TARGET net 4.75R

#### `GV-P12-V02` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> Zone top 4203.09: distance 0.41 > 0.40 -> not AT_SUPPORT -> variant not qualified (BASE pattern still formed).

Tags: at-support-boundary, variant-not-qualified
Context: atr=4 · trend=DOWN · zones_pre=[4202.80-4203.09] · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 09-16 10:30:02 4208.00/4208.20

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P12-V03` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> Lowest low INSIDE a zone: distance 0 -> AT_SUPPORT.

Tags: at-support
Context: atr=4 · trend=DOWN · zones_pre=[4203.40-4205.00] · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 09-16 10:30:02 4208.00/4208.20; 09-16 10:31:40 4231.00/4231.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4208.20
- stop: 4203.40
- R: 4.80
- target(s): 4231.00
- exit: TARGET net 4.75R

#### `GV-P12-V04` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> No support zone at all: not qualified.

Tags: variant-not-qualified
Context: atr=4 · trend=DOWN · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 09-16 10:30:02 4208.00/4208.20

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P12-V05` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> The only nearby zone is DEAD: not AT_SUPPORT (dead zones are not levels).

Tags: dead-zone, variant-not-qualified
Context: atr=4 · trend=DOWN · zones_pre=[4202.80-4203.10 DEAD] · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 09-16 10:30:02 4208.00/4208.20

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P12-V06` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> Reward exactly 2.0R: zone edge 4217.60, entry 4208.20, R 4.80 -> 9.40/4.80 = 1.958 -> below 2.0 -> SKIPPED_SRC_RR. (minimum 2:1 before entry).

Tags: T_SR, insufficient-rr, boundary
Context: atr=4 · trend=DOWN · zones_pre=[4202.80-4203.10] · zones_entry=[4217.60-4218.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 09-16 10:30:02 4208.00/4208.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4208.20
- stop: 4203.40
- R: 4.80

#### `GV-P12-V07` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> Zone edge 4217.80: 9.60/4.80 = 2.00R exactly -> accepted.

Tags: T_SR, boundary
Context: atr=4 · trend=DOWN · zones_pre=[4202.80-4203.10] · zones_entry=[4217.80-4218.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 09-16 10:30:02 4208.00/4208.20; 09-16 10:31:40 4217.80/4218.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4208.20
- stop: 4203.40
- R: 4.80
- target(s): 4217.80
- exit: TARGET net 2.00R

#### `GV-P12-V08` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> Stopped out at 4203.40.

Tags: variant, sl-first-ticks
Context: atr=4 · trend=DOWN · zones_pre=[4202.80-4203.10] · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 09-16 10:30:02 4208.00/4208.20; 09-16 10:31:40 4203.40/4203.60

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4208.20
- stop: 4203.40
- R: 4.80
- target(s): 4231.00
- exit: STOP net -1.00R

#### `GV-P12-V09` · `GT-PIERCING-BULL-v1.0/SRC-PS` · M15
> No live zone above the entry -> SKIPPED_SRC_NO_TARGET.

Tags: T_SR, no-target
Context: atr=4 · trend=DOWN · zones_pre=[4202.80-4203.10]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4203.90 | 4208.50 | 4203.60 | 4208.00 |

Ticks (bid/ask): 09-16 10:30:02 4208.00/4208.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4208.20
- stop: 4203.40
- R: 4.80

