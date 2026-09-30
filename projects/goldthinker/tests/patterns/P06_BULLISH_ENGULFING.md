# P06 Bullish Engulfing — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.2.2 · vector pack GV-0.1 · **52 vectors** (1 blocked_ambiguity, 1 dormant, 49 firm, 1 provisional)

Strategies covered: `GT-ENGULF-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-ENGULF-BULL-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4210.00/4211.00/4203.00/4204.00 ; 4204.00/4212.50/4203.00/4212.00 | DOWN | 4 | shape ✔ · formed ✔ | — | O2 exactly equal to C1 (4204.00) with C2 = 4212: passes (O2<=C1). |
| `B02` | 4210.00/4211.00/4203.00/4204.00 ; 4204.01/4212.50/4203.00/4212.00 | DOWN | 4 | no shape | O2<=C1 | O2 = C1 + 0.01: only O2<=C1 fails. |
| `B03` | 4210.00/4211.00/4203.00/4204.00 ; 4203.50/4210.50/4203.00/4210.00 | DOWN | 4 | shape ✔ · formed ✔ | — | C2 exactly equal to O1 (4210.00): passes (C2>=O1). |
| `B04` | 4210.00/4211.00/4203.00/4204.00 ; 4203.50/4210.50/4203.00/4209.99 | DOWN | 4 | no shape | C2>=O1 | C2 = O1 - 0.01: only C2>=O1 fails (this is the Piercing-Line side of the boundary). |
| `B05` | 4210.00/4211.00/4203.00/4204.00 ; 4204.00/4210.50/4203.50/4210.00 | DOWN | 4 | no shape | B2>B1 | B2 exactly equal to B1 (6.00; O2=C1, C2=O1): fails only B2>B1 (strict) - three boundaries touch at once. |
| `B06` | 4210.00/4211.00/4203.00/4204.00 ; 4204.00/4210.50/4203.50/4210.01 | DOWN | 4 | shape ✔ · formed ✔ | — | B2 = B1 + 0.01 (O2=C1, C2=4210.01): passes. |
| `B07` | 4204.40/4208.00/4200.00/4204.00 ; 4203.50/4206.00/4203.00/4205.00 | DOWN | 4 | no shape | B1>0.05R1 | B1 exactly 0.05*R1 (R1=8, B1=0.40): fails B1>0.05R1 (strict). |
| `B08` | 4204.41/4208.00/4200.00/4204.00 ; 4203.50/4206.00/4203.00/4205.00 | DOWN | 4 | shape ✔ · formed ✔ | — | B1 = 0.41 (just above 0.05*R1): passes. |
| `F01` | 4210.00/4211.00/4203.00/4204.00 ; 4203.50/4216.00/4203.00/4216.00 | DOWN | 4 | shape ✔ · formed ✔ | — | B2 = 12.5 >= 2*B1 = 12 -> size2x flag true. |
| `F02` | 4210.00/4211.00/4203.00/4204.00 ; 4204.00/4216.00/4203.00/4216.00 | DOWN | 4 | shape ✔ · formed ✔ | — | B2 = 12.00 exactly 2*B1 -> flag true (>=). |
| `F03` | 4210.00/4211.00/4203.00/4204.00 ; 4204.00/4215.99/4203.00/4215.99 | DOWN | 4 | shape ✔ · formed ✔ | — | B2 = 11.99 < 12 -> flag false; the pattern still forms. |
| `F04` | 4210.00/4211.00/4203.00/4204.00 ; 4203.50/4210.80/4203.50/4210.50 | DOWN | 4 | shape ✔ · formed ✔ | — | L2 = L1 + 0.50 (wick not engulfed on the low side): wicks_engulfed false; body still engulfs. |
| `N01` | 4204.00/4211.00/4203.00/4210.00 ; 4203.50/4212.50/4203.00/4212.00 | DOWN | 4 | no shape | C1 bear | C1 is BULLISH (4204->4210) with a bigger bullish C2: fails colour clause only. |
| `N02` | 4210.00/4211.00/4203.00/4204.00 ; 4212.00/4212.50/4203.00/4203.50 | DOWN | 4 | no shape | C2 bull, O2<=C1, C2>=O1 | C2 is BEARISH: fails colour, C2>=O1 and B2>B1 as well. |
| `N03` | 4204.00/4206.00/4202.00/4204.00 ; 4203.50/4212.50/4203.00/4212.00 | DOWN | 4 | no shape | C1 bear, B1>0.05R1 | C1 doji (O=C): not bearish, body 0. |
| `NZ1` | 4200.00/4204.50/4199.50/4204.00 ; 4204.00/4208.50/4203.50/4208.00 | DOWN | 4 | canonical: no event; variant: no event | — | Two consecutive bullish candles: C1 is not bearish -> no engulfing. |
| `T01` | 4210.00/4211.00/4203.00/4204.00 ; 4203.50/4212.50/4203.00/4212.00 | UP | 4 | canonical: SHAPE_DETECTED; candidate: ENGULF_CONTINUATION; variant: no event | — | Engulfing shape after trend UP: not formed (logged as candidate ENGULF_CONTINUATION; reading deferred to v1.1). |
| `T02` | 4210.00/4211.00/4203.00/4204.00 ; 4203.50/4212.50/4203.00/4212.00 | RANGE | 4 | canonical: SHAPE_DETECTED; candidate: None; variant: no event | — | Engulfing shape after trend RANGE: not formed. |
| `T03` | 4210.00/4211.00/4203.00/4204.00 ; 4203.50/4212.50/4203.00/4212.00 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; candidate: None; variant: no event | — | Engulfing shape after trend UNDETERMINED: not formed. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:30:02 4212.00/4212.20; 09-16 10:32:00 4216.70/4216.90; 09-16 10:35:00 4231.00/4231.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4212.20; stop: 4202.80; R: 9.40; target(s): 4231.00; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:30:02 4212.00/4212.20; 09-16 10:32:00 4207.30/4207.50; 09-16 10:35:00 4202.80/4203.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4212.20; stop: 4202.80; R: 9.40; target(s): 4231.00; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4200.80 < stop): fill = that tick's bid, not the stop (G9): -57/47R. | 09-16 10:30:02 4212.00/4212.20; 09-16 10:32:00 4200.80/4201.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4212.20; stop: 4202.80; R: 9.40; target(s): 4231.00; exit: STOP net -57/47 (≈-1.2128)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:30:02 4212.00/4212.20; 09-16 10:31:40 4202.80/4203.00; 09-16 10:33:20 4231.00/4231.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4212.20; stop: 4202.80; R: 9.40; target(s): 4231.00; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:30:02 4212.00/4212.20; 09-16 10:31:40 4231.00/4231.20; 09-16 10:33:20 4202.80/4203.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4212.20; stop: 4202.80; R: 9.40; target(s): 4231.00; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:30:02 4212.00/4212.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4212.20; stop: 4202.80; R: 9.40; target(s): 4231.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:30:02 4212.00/4212.50; 09-16 10:33:20 4231.90/4232.40 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4212.50; stop: 4202.80; R: 9.70; target(s): 4231.90; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:45:00 4212.00/4212.20; 09-16 10:46:40 4231.00/4231.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4212.20; stop: 4202.80; R: 9.40; target(s): 4231.00; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:45:01 4212.00/4212.20; 09-16 10:46:40 4231.00/4231.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:30:02 4204.30/4204.80; 09-16 10:31:40 4208.80/4209.30 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4204.80; R: 2.00; target(s): 4208.80; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:30:02 4204.29/4204.79; 09-16 10:31:40 4208.79/4209.29 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4237.40 > target 4231.00): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:30:02 4212.00/4212.20; 09-16 10:32:00 4237.40/4237.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4212.20; stop: 4202.80; R: 9.40; target(s): 4231.00; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4212.00/4212.20; 09-21 00:30:00 4231.00/4231.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4212.20; stop: 4202.80; R: 9.40; target(s): 4231.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4212.00/4212.20; 09-21 00:30:00 4231.00/4231.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4212.20; stop: 4202.80; R: 9.40; target(s): 4231.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4212.00/4212.20 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P06-R01` · `GT-ENGULF-BULL-v1.0/BASE` · M15
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:15 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |
| 3 | 09-16 10:30 | 4212.00 | 4215.00 | 4210.00 | 4213.00 |
| 4 | 09-16 10:45 | 4213.00 | 4216.00 | 4211.00 | 4214.00 |
| 5 | 09-16 11:00 | 4214.00 | 4215.00 | 4209.00 | 4211.00 |
| 6 | 09-16 11:15 | 4211.00 | 4214.00 | 4208.00 | 4212.00 |
| 7 | 09-16 11:30 | 4213.00 | 4217.00 | 4210.00 | 4215.00 |
| 8 | 09-16 11:45 | 4215.00 | 4221.00 | 4203.00 | 4216.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4212.00 | h1: ret=1.00, mfe=3.00, mae=-2.00, end_index=2 | h3: ret=-1.00, mfe=4.00, mae=-3.00, end_index=4 | h5: ret=3.00, mfe=5.00, mae=-4.00, end_index=6 | h10: NULL | h20: NULL

#### `GV-P06-Y00` · `GT-ENGULF-BULL-v1.0/BASE` · M15
> Spec example. B2=8.5>B1=6 (not 2x: 8.5<12). Wicks engulfed: L2=4203<=L1=4203 and H2=4212.5>=H1=4211 -> flag true. Stop = min(L1,L2)-0.20 = 4202.80; entry ask 4212.20; R=9.40; 2R target 4231.00.

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:15 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 10:30:02 4212.00/4212.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- flags: size2x=False, wicks_engulfed=True
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4212.20
- stop: 4202.80
- R: 9.40
- target(s): 4231.00

#### `GV-P06-Y01` · `GT-ENGULF-BULL-v1.0/BASE` · M15
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:15 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 10:30:02 4212.00/4212.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4212.20
- stop: 4202.80
- R: 9.40
- target(s): 4231.00

### Variant `SRC-CB`

#### `GV-P06-V01` · `GT-ENGULF-BULL-v1.0/SRC-CB` · H1
> SRC-CB Bullish Engulfing: TREND DOWN AND AT_SUPPORT (lowest low 4203.00 vs zone top 4202.60 = 0.40 = 0.10*ATR exactly) on H1. Stop min(L1,L2)-0.20 = 4202.80; entry ask 4212.20; R 9.40; T_SR(2.0): 4231.00 = 2.00R exactly -> trade.

Tags: variant-clean-yes, boundary
Context: atr=4 · trend=DOWN · zones_pre=[4202.50-4202.60] · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 11:00 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 12:00:02 4212.00/4212.20; 09-16 12:01:40 4231.00/4231.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4212.20
- stop: 4202.80
- R: 9.40
- target(s): 4231.00
- exit: TARGET net 2.00R

#### `GV-P06-V02` · `GT-ENGULF-BULL-v1.0/SRC-CB` · H1
> Trend RANGE with support: SRC-CB needs TREND=DOWN AND AT_SUPPORT (both) -> not qualified; BASE also not formed.

Tags: variant-not-qualified
Context: atr=4 · trend=RANGE · zones_pre=[4202.50-4202.60] · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 11:00 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 12:00:02 4212.00/4212.20

- variant: no event

#### `GV-P06-V03` · `GT-ENGULF-BULL-v1.0/SRC-CB` · H1
> Trend DOWN but no support: BASE formed, CB variant not qualified.

Tags: variant-not-qualified
Context: atr=4 · trend=DOWN · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 11:00 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 12:00:02 4212.00/4212.20

- variant: no event

#### `GV-P06-V04` · `GT-ENGULF-BULL-v1.0/SRC-CB` · H1
> Zone edge 4230.99: 1.9989R -> SKIPPED_SRC_RR.

Tags: T_SR, boundary, insufficient-rr
Context: atr=4 · trend=DOWN · zones_pre=[4202.50-4202.60] · zones_entry=[4230.99-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 11:00 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 12:00:02 4212.00/4212.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4212.20
- stop: 4202.80
- R: 9.40

#### `GV-P06-V05` · `GT-ENGULF-BULL-v1.0/SRC-CB` · M5 · **PROVISIONAL**
> M5 not allowed -> SKIPPED_TF_NOT_ALLOWED. [PROVISIONAL A-12]

Tags: tf-gate
Context: atr=4 · trend=DOWN · zones_pre=[4202.50-4202.60] · zones_entry=[4231.00-4232.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:05 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 10:10:02 4212.00/4212.20

- variant: no event
- disposition: SKIPPED_TF_NOT_ALLOWED

#### `GV-P06-V06` · `GT-ENGULF-BULL-v1.0/SRC-CB` · H1
> No zone above the entry -> SKIPPED_SRC_NO_TARGET.

Tags: T_SR, no-target
Context: atr=4 · trend=DOWN · zones_pre=[4202.50-4202.60]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 11:00 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 12:00:02 4212.00/4212.20

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4212.20
- stop: 4202.80
- R: 9.40

### Variant `SRC-PS`

#### `GV-DORM-P06-01` · `GT-ENGULF-BULL-v1.0/SRC-PS` · M15 · **DORMANT**
> DORMANT. Source-only qualification: trend RANGE (BASE not formed) but the lowest low 4203.00 is 0.30 from support -> 'DOWN OR AT_SUPPORT' holds. Stop = min(L1,L2) - 20 pips x $0.10 = 4201.00; R 11.20; T_SR(1.5): 4229.00 = 1.5R exactly.

Tags: dormant, source-only-qualification
Context: atr=4 · trend=RANGE · zones_pre=[4202.50-4202.70] · zones_entry=[4229.00-4230.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:15 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 10:30:02 4212.00/4212.20; 09-16 10:31:40 4229.00/4229.20

- canonical: SHAPE_DETECTED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4212.20
- stop: 4201.00
- R: 11.20
- target(s): 4229.00
- exit: TARGET net 1.50R

#### `GV-P06-DIS` · `GT-ENGULF-BULL-v1.0/SRC-PS` · M15
> DISABLED_PENDING_PIP_CONFIRMATION (D-032): the BASE pattern forms exactly as in GV-P06-Y01 (canonical events are still logged), but this source variant depends on PIP_SRC_USD, so it emits NO variant events, opens NO trade and has no ledger. The BASE strategy on the same candle is unaffected.

Tags: disabled-variant
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:15 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 10:30:02 4212.00/4212.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant status: DISABLED_PENDING_PIP_CONFIRMATION
- variant: no event

### Variant `SRC-SH`

#### `GV-P06-H01` · `GT-ENGULF-BULL-v1.0/SRC-SH` · M15
> SRC-SH: wicks engulfed (L2 4203 <= L1 4203, H2 4212.5 >= H1 4211) AND RSI14 = 25 < 30 -> qualifies; entry/stop/target = BASELINE (2R): entry ask 4212.20, stop 4202.80, target 4231.00.

Tags: variant-clean-yes, rsi
Context: atr=4 · trend=DOWN · rsi=25 · history_bars=500

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:15 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 10:30:02 4212.00/4212.20; 09-16 10:31:40 4231.00/4231.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4212.20
- stop: 4202.80
- R: 9.40
- target(s): 4231.00
- exit: TARGET net 2.00R

#### `GV-P06-H02` · `GT-ENGULF-BULL-v1.0/SRC-SH` · M15
> RSI exactly 30: the test is strictly < 30 -> not qualified.

Tags: rsi, boundary, variant-not-qualified
Context: atr=4 · trend=DOWN · rsi=30 · history_bars=500

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:15 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 10:30:02 4212.00/4212.20

- variant: no event

#### `GV-P06-H03` · `GT-ENGULF-BULL-v1.0/SRC-SH` · M15
> RSI 29.99: qualifies.

Tags: rsi, boundary
Context: atr=4 · trend=DOWN · rsi=29.99 · history_bars=500

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:15 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 10:30:02 4212.00/4212.20; 09-16 10:31:40 4231.00/4231.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4212.20
- stop: 4202.80
- R: 9.40
- target(s): 4231.00
- exit: TARGET net 2.00R

#### `GV-P06-H04` · `GT-ENGULF-BULL-v1.0/SRC-SH` · M15
> Body engulfs but L2 (4203.50) > L1 (4203.00): wicks not engulfed -> SH variant not qualified although BASE formed.

Tags: variant-not-qualified, wicks
Context: atr=4 · trend=DOWN · rsi=25 · history_bars=500

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:15 | 4203.50 | 4210.80 | 4203.50 | 4210.50 |

Ticks (bid/ask): 09-16 10:30:02 4210.50/4210.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- flags: wicks_engulfed=False
- variant: no event

#### `GV-P06-H05` · `GT-ENGULF-BULL-v1.0/SRC-SH` · M15
> Only 99 completed bars of history: RSI14 needs 100 -> NOT_EVALUATED_WARMUP (no events).

Tags: rsi, warmup
Context: atr=4 · trend=DOWN · rsi=25 · history_bars=99

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:15 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 10:30:02 4212.00/4212.20

- variant: no event
- disposition: NOT_EVALUATED_WARMUP

#### `GV-P06-H06` · `GT-ENGULF-BULL-v1.0/SRC-SH` · M15
> Exactly 100 bars of history: enough -> evaluated (RSI 25) and trades.

Tags: rsi, warmup, boundary
Context: atr=4 · trend=DOWN · rsi=25 · history_bars=100

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:15 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 10:30:02 4212.00/4212.20; 09-16 10:31:40 4231.00/4231.20

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4212.20
- stop: 4202.80
- R: 9.40
- target(s): 4231.00
- exit: TARGET net 2.00R

#### `GV-P06-H07` · `GT-ENGULF-BULL-v1.0/SRC-SH` · **BLOCKED_AMBIGUITY**
> SRC-SH's field says 'shape tightened to wicks engulfed AND RSI14(C2)<30' but does not say whether the base prior state (TREND = DOWN) still applies. Here trend is RANGE, wicks are engulfed and RSI is 25.

Context: atr=4 · trend=RANGE · rsi=25 · history_bars=500

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:15 | 4203.50 | 4212.50 | 4203.00 | 4212.00 |

Ticks (bid/ask): 09-16 10:30:02 4212.00/4212.20

Candidate rulings (no expected value is asserted until the spec settles one):
- Reading A (prior state inherited): trend RANGE -> BASE not formed -> variant not qualified.
- Reading B (prior state replaced by the RSI test): qualifies -> trade.

