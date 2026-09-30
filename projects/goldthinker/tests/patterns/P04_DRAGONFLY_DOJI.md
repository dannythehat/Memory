# P04 Dragonfly Doji — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.3 · vector pack GV-0.2 · **39 vectors** (7 dormant, 32 firm)

Strategies covered: `GT-DRAGONFLY-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-DRAGONFLY-BULL-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4199.40/4200.00/4190.00/4199.90 | DOWN | 4 | shape ✔ · formed ✔ | — | B exactly 0.05*R (R=10: B 0.50, UW 0.10, LW 9.40): passes. |
| `B02` | 4199.40/4199.99/4190.00/4199.89 | DOWN | 4 | shape ✔ · formed ✔ | — | B just inside (0.49). |
| `B03` | 4199.40/4200.01/4190.00/4199.91 | DOWN | 4 | no shape | DOJI:B<=0.05R | B just outside (0.51 > 0.05*10.01): only the doji clause fails. |
| `B04` | 4199.20/4200.00/4190.00/4199.50 | DOWN | 4 | shape ✔ · formed ✔ | — | UW exactly 0.05*R (R=10: UW 0.50, B 0.30): passes. |
| `B05` | 4199.20/4199.99/4190.00/4199.50 | DOWN | 4 | shape ✔ · formed ✔ | — | UW just inside (0.49). |
| `B06` | 4199.20/4200.01/4190.00/4199.50 | DOWN | 4 | no shape | UW<=0.05R | UW just outside (0.51 > 0.5005): only the UW clause fails. |
| `B07` | 4199.82/4200.00/4198.00/4199.91 | DOWN | 4 | shape ✔ · formed ✔ | — | R exactly 2.00: passes. |
| `B08` | 4199.81/4199.99/4198.00/4199.90 | DOWN | 4 | no shape | R>=0.50ATR | R = 1.99: only the range clause fails. |
| `N02` | 4194.10/4200.00/4194.00/4194.20 | DOWN | 4 | no shape | UW<=0.05R, LW>=0.80R | Long UPPER wick (gravestone shape): fails UW and LW clauses for the dragonfly. |
| `N03` | 4194.50/4200.00/4194.00/4199.50 | DOWN | 4 | no shape | DOJI:B<=0.05R, UW<=0.05R, LW>=0.80R | Full-body candle: fails doji. |
| `N04` | 4199.00/4200.00/4190.00/4199.50 | DOWN | 4 | shape ✔ · formed ✔ | — | Property: the LW>=0.80R clause is IMPLIED by DOJI and UW<=0.05R (LW >= 0.90R), so it can never fail alone. Here everything passes with LW = 0.90R exactly (R=10, B 0.50, UW 0.50, LW 9.00). |
| `T01` | 4199.80/4200.00/4194.00/4199.90 | UP | 4 | canonical: SHAPE_DETECTED; candidate: None; variant: no event | — | Dragonfly shape after trend UP: not formed (needs DOWN). |
| `T02` | 4199.80/4200.00/4194.00/4199.90 | RANGE | 4 | canonical: SHAPE_DETECTED; candidate: None; variant: no event | — | Dragonfly shape after trend RANGE: not formed (needs DOWN). |
| `T03` | 4199.80/4200.00/4194.00/4199.90 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; candidate: None; variant: no event | — | Dragonfly shape after trend UNDETERMINED: not formed (needs DOWN). |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:15:02 4199.90/4200.10; 09-16 10:17:00 4203.05/4203.25; 09-16 10:20:00 4212.70/4212.90 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.10; stop: 4193.80; R: 6.30; target(s): 4212.70; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:15:02 4199.90/4200.10; 09-16 10:17:00 4196.75/4196.95; 09-16 10:20:00 4193.80/4194.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.10; stop: 4193.80; R: 6.30; target(s): 4212.70; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4191.80 < stop): fill = that tick's bid, not the stop (G9): -83/63R. | 09-16 10:15:02 4199.90/4200.10; 09-16 10:17:00 4191.80/4192.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.10; stop: 4193.80; R: 6.30; target(s): 4212.70; exit: STOP net -83/63 (≈-1.3175)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:15:02 4199.90/4200.10; 09-16 10:16:40 4193.80/4194.00; 09-16 10:18:20 4212.70/4212.90 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.10; stop: 4193.80; R: 6.30; target(s): 4212.70; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:15:02 4199.90/4200.10; 09-16 10:16:40 4212.70/4212.90; 09-16 10:18:20 4193.80/4194.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.10; stop: 4193.80; R: 6.30; target(s): 4212.70; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:15:02 4199.90/4200.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.10; stop: 4193.80; R: 6.30; target(s): 4212.70; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:15:02 4199.90/4200.40; 09-16 10:18:20 4213.60/4214.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; spread_at_entry: 0.50; entry: 4200.40; stop: 4193.80; R: 6.60; target(s): 4213.60; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:30:00 4199.90/4200.10; 09-16 10:31:40 4212.70/4212.90 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.10; stop: 4193.80; R: 6.30; target(s): 4212.70; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:30:01 4199.90/4200.10; 09-16 10:31:40 4212.70/4212.90 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:15:02 4195.30/4195.80; 09-16 10:16:40 4199.80/4200.30 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4195.80; R: 2.00; target(s): 4199.80; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:15:02 4195.29/4195.79; 09-16 10:16:40 4199.79/4200.29 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4219.10 > target 4212.70): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:15:02 4199.90/4200.10; 09-16 10:17:00 4219.10/4219.30 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4200.10; stop: 4193.80; R: 6.30; target(s): 4212.70; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4199.90/4200.10; 09-21 00:30:00 4212.70/4212.90 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4200.10; stop: 4193.80; R: 6.30; target(s): 4212.70; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4199.90/4200.10; 09-21 00:30:00 4212.70/4212.90 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4200.10; stop: 4193.80; R: 6.30; target(s): 4212.70; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4199.90/4200.10 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P04-R01` · `GT-DRAGONFLY-BULL-v1.0/BASE` · M15
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4199.80 | 4200.00 | 4194.00 | 4199.90 |
| 2 | 09-16 10:15 | 4199.90 | 4202.90 | 4197.90 | 4200.90 |
| 3 | 09-16 10:30 | 4200.90 | 4203.90 | 4198.90 | 4201.90 |
| 4 | 09-16 10:45 | 4201.90 | 4202.90 | 4196.90 | 4198.90 |
| 5 | 09-16 11:00 | 4198.90 | 4201.90 | 4195.90 | 4199.90 |
| 6 | 09-16 11:15 | 4200.90 | 4204.90 | 4197.90 | 4202.90 |
| 7 | 09-16 11:30 | 4202.90 | 4208.90 | 4190.90 | 4203.90 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4199.90 | h1: ret=1.00, mfe=3.00, mae=2.00, end_index=1 | h3: ret=-1.00, mfe=4.00, mae=3.00, end_index=3 | h5: ret=3.00, mfe=5.00, mae=4.00, end_index=5 | h10: NULL | h20: NULL

#### `GV-P04-Y01` · `GT-DRAGONFLY-BULL-v1.0/BASE` · M15
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4199.80 | 4200.00 | 4194.00 | 4199.90 |

Ticks (bid/ask): 09-16 10:15:02 4199.90/4200.10

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:15:00Z
- entry: 4200.10
- stop: 4193.80
- R: 6.30
- target(s): 4212.70

### Variant `SRC-PS`

#### `GV-DORM-P04-01` · `GT-DRAGONFLY-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> DORMANT. Source Dragonfly: C2 bullish closing above max(O1,C1) = 4199.90; at support; stop L1 - 10 pips x $0.10 = 4193.00; entry ask 4201.20; R 8.20; T_SR(1.5) zone edge 4214.00 = 1.56R.

Tags: dormant, confirmation
Context: atr=4 · trend=DOWN · zones_pre=[4193.60-4193.90] · zones_entry=[4214.00-4215.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4199.80 | 4200.00 | 4194.00 | 4199.90 |
| 2 | 09-16 10:15 | 4200.00 | 4202.00 | 4199.80 | 4201.00 |

Ticks (bid/ask): 09-16 10:30:02 4201.00/4201.20; 09-16 10:31:40 4214.00/4214.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4201.20
- stop: 4193.00
- R: 8.20
- target(s): 4214.00
- exit: TARGET net 64/41 (≈1.5610)R

#### `GV-DORM-P04-02` · `GT-DRAGONFLY-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> C2 is a doji (close = open): 'fails if C2 is bearish or a doji' -> expired.

Tags: dormant, confirmation, expiry
Context: atr=4 · trend=DOWN · zones_pre=[4193.60-4193.90] · zones_entry=[4214.00-4215.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4199.80 | 4200.00 | 4194.00 | 4199.90 |
| 2 | 09-16 10:15 | 4200.00 | 4201.00 | 4199.50 | 4200.00 |

Ticks (bid/ask): 09-16 10:30:02 4201.00/4201.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED
- disposition: EXPIRED_NO_CONFIRMATION

#### `GV-DORM-P04-03` · `GT-DRAGONFLY-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> NFP exactly at the signal time (T): inside the MAJOR window T-60..T+30 -> SKIPPED_NEWS.

Tags: dormant, news
Context: atr=4 · trend=DOWN · zones_pre=[4193.60-4193.90] · zones_entry=[4214.00-4215.00] · news=NFP high USD 10:30:00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4199.80 | 4200.00 | 4194.00 | 4199.90 |
| 2 | 09-16 10:15 | 4200.00 | 4202.00 | 4199.80 | 4201.00 |

Ticks (bid/ask): 09-16 10:30:02 4201.00/4201.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_NEWS
- signal time: 2026-09-16T10:30:00Z

#### `GV-DORM-P04-04` · `GT-DRAGONFLY-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> NFP at 10:00: signal 10:30 is exactly T+30: window end inclusive -> blocked.

Tags: dormant, news
Context: atr=4 · trend=DOWN · zones_pre=[4193.60-4193.90] · zones_entry=[4214.00-4215.00] · news=NFP high USD 10:00:00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4199.80 | 4200.00 | 4194.00 | 4199.90 |
| 2 | 09-16 10:15 | 4200.00 | 4202.00 | 4199.80 | 4201.00 |

Ticks (bid/ask): 09-16 10:30:02 4201.00/4201.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_NEWS
- signal time: 2026-09-16T10:30:00Z

#### `GV-DORM-P04-05` · `GT-DRAGONFLY-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> NFP at 09:59:59: signal 10:30:00 is T+30:01 -> outside -> trade.

Tags: dormant, news
Context: atr=4 · trend=DOWN · zones_pre=[4193.60-4193.90] · zones_entry=[4214.00-4215.00] · news=NFP high USD 09:59:59

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4199.80 | 4200.00 | 4194.00 | 4199.90 |
| 2 | 09-16 10:15 | 4200.00 | 4202.00 | 4199.80 | 4201.00 |

Ticks (bid/ask): 09-16 10:30:02 4201.00/4201.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE

#### `GV-DORM-P04-06` · `GT-DRAGONFLY-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> NFP at 11:30: signal 10:30 is T-60 exactly -> inside the window start (inclusive).

Tags: dormant, news
Context: atr=4 · trend=DOWN · zones_pre=[4193.60-4193.90] · zones_entry=[4214.00-4215.00] · news=NFP high USD 11:30:00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4199.80 | 4200.00 | 4194.00 | 4199.90 |
| 2 | 09-16 10:15 | 4200.00 | 4202.00 | 4199.80 | 4201.00 |

Ticks (bid/ask): 09-16 10:30:02 4201.00/4201.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_NEWS
- signal time: 2026-09-16T10:30:00Z

#### `GV-DORM-P04-07` · `GT-DRAGONFLY-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> NFP at 11:30:01: signal is T-60:01 -> outside -> trade.

Tags: dormant, news
Context: atr=4 · trend=DOWN · zones_pre=[4193.60-4193.90] · zones_entry=[4214.00-4215.00] · news=NFP high USD 11:30:01

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4199.80 | 4200.00 | 4194.00 | 4199.90 |
| 2 | 09-16 10:15 | 4200.00 | 4202.00 | 4199.80 | 4201.00 |

Ticks (bid/ask): 09-16 10:30:02 4201.00/4201.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE

#### `GV-P04-DIS` · `GT-DRAGONFLY-BULL-v1.0/SRC-PS` · M15
> DISABLED_PENDING_PIP_CONFIRMATION (D-032): the BASE pattern forms exactly as in GV-P04-Y01 (canonical events are still logged), but this source variant depends on PIP_SRC_USD, so it emits NO variant events, opens NO trade and has no ledger. The BASE strategy on the same candle is unaffected.

Tags: disabled-variant
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4199.80 | 4200.00 | 4194.00 | 4199.90 |

Ticks (bid/ask): 09-16 10:15:02 4199.90/4200.10

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant status: DISABLED_PENDING_PIP_CONFIRMATION
- variant: no event

