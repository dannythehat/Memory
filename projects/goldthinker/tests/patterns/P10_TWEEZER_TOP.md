# P10 Tweezer Top — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.2.2 · vector pack GV-0.1 · **37 vectors** (1 dormant, 36 firm)

Strategies covered: `GT-TWEEZERTOP-BEAR-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-TWEEZERTOP-BEAR-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `A01` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4200.60/4194.50/4195.00 | UP | 8 | shape ✔ · formed ✔ | — | ATR 8 -> tol 0.40. Difference 0.40 passes. |
| `A02` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4200.59/4194.50/4195.00 | UP | 8 | no shape | (1 clause) | ATR 8: difference 0.41 fails. |
| `A03` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4200.95/4194.50/4195.00 | UP | 1 | shape ✔ · formed ✔ | — | ATR 1 -> tol = max(0.03, 0.05) = 0.05. Difference 0.05 passes. |
| `A04` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4200.94/4194.50/4195.00 | UP | 1 | no shape | (1 clause) | ATR 1: difference 0.06 fails. |
| `A05` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4200.97/4194.50/4195.00 | UP | 0.5 | shape ✔ · formed ✔ | — | ATR 0.5 -> 0.05*ATR = 0.025 < 3 ticks 0.03, so tol = 0.03. Difference 0.03 passes. |
| `A06` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4200.96/4194.50/4195.00 | UP | 0.5 | no shape | (1 clause) | ATR 0.5: difference 0.04 fails (the 3-tick floor is 0.03). |
| `B01` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4200.80/4194.50/4195.00 | UP | 4 | shape ✔ · formed ✔ | — | ATR 4 -> tol = max(3*tick 0.03, 0.05*4 = 0.20) = 0.20. |L1-L2| = 0.20 (L2 above L1): passes. |
| `B02` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4200.81/4194.50/4195.00 | UP | 4 | shape ✔ · formed ✔ | — | |L1-L2| = 0.19. |
| `B03` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4200.79/4194.50/4195.00 | UP | 4 | no shape | (1 clause) | |L1-L2| = 0.21 -> only the tolerance clause fails. |
| `B04` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4201.20/4194.50/4195.00 | UP | 4 | shape ✔ · formed ✔ | — | L2 BELOW L1 by exactly 0.20 (4198.80): passes (absolute difference). |
| `B05` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4201.21/4194.50/4195.00 | UP | 4 | no shape | (1 clause) | L2 below L1 by 0.21: fails. |
| `B06` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4201.00/4194.50/4195.00 | UP | 4 | shape ✔ · formed ✔ | — | Equal lows (difference 0): passes. |
| `N01` | 4200.00/4201.00/4194.00/4195.00 ; 4200.50/4200.90/4194.50/4195.00 | UP | 4 | no shape | (1 clause) | C1 bullish: fails colour. |
| `N02` | 4195.00/4201.00/4194.00/4200.00 ; 4195.00/4200.90/4194.50/4200.50 | UP | 4 | no shape | (1 clause) | C2 bearish: fails colour. |
| `NZ1` | 4200.00/4200.50/4195.50/4196.00 ; 4196.00/4196.50/4191.50/4192.00 | UP | 4 | canonical: no event; variant: no event | — | Two bullish candles: C1 must be bearish. |
| `T01` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4200.90/4194.50/4195.00 | DOWN | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Tweezer shape after UP: not formed. |
| `T02` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4200.90/4194.50/4195.00 | RANGE | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Tweezer shape after RANGE: not formed. |
| `T03` | 4195.00/4201.00/4194.00/4200.00 ; 4200.50/4200.90/4194.50/4195.00 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; variant: no event | — | Tweezer shape after UNDETERMINED: not formed. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:30:02 4194.80/4195.00; 09-16 10:32:00 4191.60/4191.80; 09-16 10:35:00 4181.80/4182.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4194.80; stop: 4201.20; R: 6.40; target(s): 4182.00; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:30:02 4194.80/4195.00; 09-16 10:32:00 4198.00/4198.20; 09-16 10:35:00 4201.00/4201.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4194.80; stop: 4201.20; R: 6.40; target(s): 4182.00; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4196.80 < stop): fill = that tick's bid, not the stop (G9): -1.3125R. | 09-16 10:30:02 4194.80/4195.00; 09-16 10:32:00 4203.00/4203.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4194.80; stop: 4201.20; R: 6.40; target(s): 4182.00; exit: STOP net -1.3125R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:30:02 4194.80/4195.00; 09-16 10:31:40 4201.00/4201.20; 09-16 10:33:20 4181.80/4182.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4194.80; stop: 4201.20; R: 6.40; target(s): 4182.00; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:30:02 4194.80/4195.00; 09-16 10:31:40 4181.80/4182.00; 09-16 10:33:20 4201.00/4201.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4194.80; stop: 4201.20; R: 6.40; target(s): 4182.00; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:30:02 4194.80/4195.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4194.80; stop: 4201.20; R: 6.40; target(s): 4182.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:30:02 4194.50/4195.00; 09-16 10:33:20 4180.60/4181.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4194.50; stop: 4201.20; R: 6.70; target(s): 4181.10; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:45:00 4194.80/4195.00; 09-16 10:46:40 4181.80/4182.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4194.80; stop: 4201.20; R: 6.40; target(s): 4182.00; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:45:01 4194.80/4195.00; 09-16 10:46:40 4181.80/4182.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:30:02 4199.20/4199.70; 09-16 10:31:40 4194.70/4195.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4199.20; R: 2.00; target(s): 4195.20; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:30:02 4199.21/4199.71; 09-16 10:31:40 4194.71/4195.21 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4224.40 > target 4218.00): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:30:02 4194.80/4195.00; 09-16 10:32:00 4175.40/4175.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4194.80; stop: 4201.20; R: 6.40; target(s): 4182.00; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4194.80/4195.00; 09-21 00:30:00 4181.80/4182.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4194.80; stop: 4201.20; R: 6.40; target(s): 4182.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4194.80/4195.00; 09-21 00:30:00 4181.80/4182.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4194.80; stop: 4201.20; R: 6.40; target(s): 4182.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4194.80/4195.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P10-R01` · `GT-TWEEZERTOP-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P11-R01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4201.00 | 4194.00 | 4200.00 |
| 2 | 09-16 10:15 | 4200.50 | 4200.90 | 4194.50 | 4195.00 |
| 3 | 09-16 10:30 | 4195.00 | 4197.00 | 4192.00 | 4194.00 |
| 4 | 09-16 10:45 | 4194.00 | 4196.00 | 4191.00 | 4193.00 |
| 5 | 09-16 11:00 | 4193.00 | 4198.00 | 4192.00 | 4196.00 |
| 6 | 09-16 11:15 | 4196.00 | 4199.00 | 4193.00 | 4195.00 |
| 7 | 09-16 11:30 | 4194.00 | 4197.00 | 4190.00 | 4192.00 |
| 8 | 09-16 11:45 | 4192.00 | 4204.00 | 4186.00 | 4191.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4195.00 | h1: ret=1.00, mfe=3.00, mae=-2.00, end_index=2 | h3: ret=-1.00, mfe=4.00, mae=-3.00, end_index=4 | h5: ret=3.00, mfe=5.00, mae=-4.00, end_index=6 | h10: NULL | h20: NULL

#### `GV-P10-Y01` · `GT-TWEEZERTOP-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P11-Y01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4201.00 | 4194.00 | 4200.00 |
| 2 | 09-16 10:15 | 4200.50 | 4200.90 | 4194.50 | 4195.00 |

Ticks (bid/ask): 09-16 10:30:02 4194.80/4195.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4194.80
- stop: 4201.20
- R: 6.40
- target(s): 4182.00

### Variant `SRC-PS`

#### `GV-DORM-P10-01` · `GT-TWEEZERTOP-BEAR-v1.0/SRC-PS` · M15 · **DORMANT**
> DORMANT. Identity delta: highs differ by 0.25. Canonical tolerance max(0.03, 0.05*4) = 0.20 -> NO canonical shape; SRC-PS tolerance max(3 pips x $0.10 = 0.30, 0.20) = 0.30 -> the source variant qualifies with base_formed=false. STOP_ENTRY sell trigger L2 = 4198.50 (bid <= trigger); stop max(H1,H2) + 3 pips x $0.10 = 4206.30; R 7.80; T_SR(1.5) 4186.50 = 1.54R.

Tags: dormant, source-only-qualification, stop-entry
Context: atr=4 · trend=UP · zones_pre=[4206.20-4206.60] · zones_entry=[4185.00-4186.50]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.00 | 4205.00 |
| 2 | 09-16 10:15 | 4205.50 | 4205.75 | 4198.50 | 4199.50 |

Ticks (bid/ask): 09-16 10:40:00 4198.50/4198.70; 09-16 10:50:00 4186.30/4186.50

- canonical: no event
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- trigger: 4198.50
- signal time: 2026-09-16T10:40:00Z
- entry: 4198.50
- stop: 4206.30
- R: 7.80
- target(s): 4186.50
- exit: TARGET net 20/13 (≈1.5385)R

#### `GV-P10-DIS` · `GT-TWEEZERTOP-BEAR-v1.0/SRC-PS` · M15
> DISABLED_PENDING_PIP_CONFIRMATION (D-032): the BASE pattern forms exactly as in GV-P10-Y01 (canonical events are still logged), but this source variant depends on PIP_SRC_USD, so it emits NO variant events, opens NO trade and has no ledger. The BASE strategy on the same candle is unaffected.

Tags: disabled-variant
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4201.00 | 4194.00 | 4200.00 |
| 2 | 09-16 10:15 | 4200.50 | 4200.90 | 4194.50 | 4195.00 |

Ticks (bid/ask): 09-16 10:30:02 4194.80/4195.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant status: DISABLED_PENDING_PIP_CONFIRMATION
- variant: no event

