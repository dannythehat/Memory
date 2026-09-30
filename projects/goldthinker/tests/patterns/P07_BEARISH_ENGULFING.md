# P07 Bearish Engulfing — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.3.2 · vector pack GV-0.2 · **45 vectors** (45 firm)

Strategies covered: `GT-ENGULF-BEAR-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-ENGULF-BEAR-v1.0`

### Variant `BASE`

#### Compact vectors (detection / boundary / context) — bars are O/H/L/C, one candle per `;`

| ID | bars | trend | ATR | result | failing clause | note |
|---|---|---|---|---|---|---|
| `B01` | 4190.00/4197.00/4189.00/4196.00 ; 4196.00/4197.00/4187.50/4188.00 | UP | 4 | shape ✔ · formed ✔ | — | O2 exactly equal to C1 (4204.00) with C2 = 4212: passes (O2<=C1). |
| `B02` | 4190.00/4197.00/4189.00/4196.00 ; 4195.99/4197.00/4187.50/4188.00 | UP | 4 | no shape | (1 clause) | O2 = C1 + 0.01: only O2<=C1 fails. |
| `B03` | 4190.00/4197.00/4189.00/4196.00 ; 4196.50/4197.00/4189.50/4190.00 | UP | 4 | shape ✔ · formed ✔ | — | C2 exactly equal to O1 (4210.00): passes (C2>=O1). |
| `B04` | 4190.00/4197.00/4189.00/4196.00 ; 4196.50/4197.00/4189.50/4190.01 | UP | 4 | no shape | (1 clause) | C2 = O1 - 0.01: only C2>=O1 fails (this is the Piercing-Line side of the boundary). |
| `B05` | 4190.00/4197.00/4189.00/4196.00 ; 4196.00/4196.50/4189.50/4190.00 | UP | 4 | no shape | (1 clause) | B2 exactly equal to B1 (6.00; O2=C1, C2=O1): fails only B2>B1 (strict) - three boundaries touch at once. |
| `B06` | 4190.00/4197.00/4189.00/4196.00 ; 4196.00/4196.50/4189.50/4189.99 | UP | 4 | shape ✔ · formed ✔ | — | B2 = B1 + 0.01 (O2=C1, C2=4210.01): passes. |
| `B07` | 4195.60/4200.00/4192.00/4196.00 ; 4196.50/4197.00/4194.00/4195.00 | UP | 4 | no shape | (1 clause) | B1 exactly 0.05*R1 (R1=8, B1=0.40): fails B1>0.05R1 (strict). |
| `B08` | 4195.59/4200.00/4192.00/4196.00 ; 4196.50/4197.00/4194.00/4195.00 | UP | 4 | shape ✔ · formed ✔ | — | B1 = 0.41 (just above 0.05*R1): passes. |
| `F01` | 4190.00/4197.00/4189.00/4196.00 ; 4196.50/4197.00/4184.00/4184.00 | UP | 4 | shape ✔ · formed ✔ | — | B2 = 12.5 >= 2*B1 = 12 -> size2x flag true. |
| `F02` | 4190.00/4197.00/4189.00/4196.00 ; 4196.00/4197.00/4184.00/4184.00 | UP | 4 | shape ✔ · formed ✔ | — | B2 = 12.00 exactly 2*B1 -> flag true (>=). |
| `F03` | 4190.00/4197.00/4189.00/4196.00 ; 4196.00/4197.00/4184.01/4184.01 | UP | 4 | shape ✔ · formed ✔ | — | B2 = 11.99 < 12 -> flag false; the pattern still forms. |
| `F04` | 4190.00/4197.00/4189.00/4196.00 ; 4196.50/4196.50/4189.20/4189.50 | UP | 4 | shape ✔ · formed ✔ | — | L2 = L1 + 0.50 (wick not engulfed on the low side): wicks_engulfed false; body still engulfs. |
| `N01` | 4196.00/4197.00/4189.00/4190.00 ; 4196.50/4197.00/4187.50/4188.00 | UP | 4 | no shape | (1 clause) | C1 is BULLISH (4204->4210) with a bigger bullish C2: fails colour clause only. |
| `N02` | 4190.00/4197.00/4189.00/4196.00 ; 4188.00/4197.00/4187.50/4196.50 | UP | 4 | no shape | (3 clause) | C2 is BEARISH: fails colour, C2>=O1 and B2>B1 as well. |
| `N03` | 4196.00/4198.00/4194.00/4196.00 ; 4196.50/4197.00/4187.50/4188.00 | UP | 4 | no shape | (2 clause) | C1 doji (O=C): not bearish, body 0. |
| `NZ1` | 4200.00/4200.50/4195.50/4196.00 ; 4196.00/4196.50/4191.50/4192.00 | UP | 4 | canonical: no event; variant: no event | — | Two consecutive bullish candles: C1 is not bearish -> no engulfing. |
| `T01` | 4190.00/4197.00/4189.00/4196.00 ; 4196.50/4197.00/4187.50/4188.00 | DOWN | 4 | canonical: SHAPE_DETECTED; candidate: ENGULF_CONTINUATION; variant: no event | — | Engulfing shape after trend UP: not formed (logged as candidate ENGULF_CONTINUATION; reading deferred to v1.1). |
| `T02` | 4190.00/4197.00/4189.00/4196.00 ; 4196.50/4197.00/4187.50/4188.00 | RANGE | 4 | canonical: SHAPE_DETECTED; candidate: None; variant: no event | — | Engulfing shape after trend RANGE: not formed. |
| `T03` | 4190.00/4197.00/4189.00/4196.00 ; 4196.50/4197.00/4187.50/4188.00 | UNDETERMINED | 4 | canonical: SHAPE_DETECTED; candidate: None; variant: no event | — | Engulfing shape after trend UNDETERMINED: not formed. |

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L01` | Target reached by tick order: exit at target price, +2.00R (spread already in entry/R). | 09-16 10:30:02 4187.80/4188.00; 09-16 10:32:00 4183.10/4183.30; 09-16 10:35:00 4168.80/4169.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4187.80; stop: 4197.20; R: 9.40; target(s): 4169.00; exit: TARGET net 2.00R |
| `L02` | Stop reached first by tick order: exit at the tick bid = stop, -1.00R. | 09-16 10:30:02 4187.80/4188.00; 09-16 10:32:00 4192.50/4192.70; 09-16 10:35:00 4197.00/4197.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4187.80; stop: 4197.20; R: 9.40; target(s): 4169.00; exit: STOP net -1.00R |
| `L03` | Tick gaps through the stop (bid 4200.80 < stop): fill = that tick's bid, not the stop (G9): -57/47R. | 09-16 10:30:02 4187.80/4188.00; 09-16 10:32:00 4199.00/4199.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4187.80; stop: 4197.20; R: 9.40; target(s): 4169.00; exit: STOP net -57/47 (≈-1.2128)R |
| `L04` | Ticks reach the stop first then the target: only the first counts (stop). | 09-16 10:30:02 4187.80/4188.00; 09-16 10:31:40 4197.00/4197.20; 09-16 10:33:20 4168.80/4169.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4187.80; stop: 4197.20; R: 9.40; target(s): 4169.00; exit: STOP net -1.00R |
| `L05` | Ticks reach the target first then the stop: only the first counts (target). | 09-16 10:30:02 4187.80/4188.00; 09-16 10:31:40 4168.80/4169.00; 09-16 10:33:20 4197.00/4197.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4187.80; stop: 4197.20; R: 9.40; target(s): 4169.00; exit: TARGET net 2.00R |
| `L06` | No ticks after entry, only one OHLC bar whose range contains both stop and target: scored STOP FIRST (G9) and the target-first figure +2.00R is reported. | 09-16 10:30:02 4187.80/4188.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4187.80; stop: 4197.20; R: 9.40; target(s): 4169.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |
| `L07` | Spread 0.50: BUY fills at the ask (bid+0.50), so entry, R and target all move; result still +2.00R. | 09-16 10:30:02 4187.50/4188.00; 09-16 10:33:20 4167.60/4168.10 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; spread_at_entry: 0.50; entry: 4187.50; stop: 4197.20; R: 9.70; target(s): 4168.10; exit: TARGET net 2.00R |
| `L08` | First tick exactly 15:00 after signal_time: open_elapsed = 15 min is NOT greater than 15 min, so the trade is taken. | 09-16 10:45:00 4187.80/4188.00; 09-16 10:46:40 4168.80/4169.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4187.80; stop: 4197.20; R: 9.40; target(s): 4169.00; exit: TARGET net 2.00R |
| `L09` | First tick 15:01 after signal_time: open_elapsed > 15 min -> SKIPPED_STALE_ENTRY (no trade). | 09-16 10:45:01 4187.80/4188.00; 09-16 10:46:40 4168.80/4169.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY |
| `L10` | R = 4 x spread exactly (2.00): threshold is 'R < max(4*spread, 0.10*ATR)', so equal is accepted. | 09-16 10:30:02 4195.20/4195.70; 09-16 10:31:40 4190.70/4191.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4195.20; R: 2.00; target(s): 4191.20; exit: TARGET net 2.00R |
| `L11` | R one tick below 4 x spread -> SKIPPED_R_TOO_SMALL (no trade). | 09-16 10:30:02 4195.21/4195.71; 09-16 10:31:40 4190.71/4191.21 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_R_TOO_SMALL; R: 1.99 |
| `L12` | Tick jumps far past the target (bid 4237.40 > target 4231.00): fill = the TARGET price, no windfall for a favourable gap (G9): exactly +2.00R. | 09-16 10:30:02 4187.80/4188.00; 09-16 10:32:00 4162.40/4162.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4187.80; stop: 4197.20; R: 9.40; target(s): 4169.00; exit: TARGET net 2.00R |
| `W01` | H1 bar completes at the Friday 22:00 UTC scheduled close (not Monday). First tick after the weekend, 5 s after reopening: open_elapsed = 5 s -> trade taken, tagged entry_across_break. | 09-20 23:00:05 4187.80/4188.00; 09-21 00:30:00 4168.80/4169.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry time: 2026-09-20T23:00:05Z; entry: 4187.80; stop: 4197.20; R: 9.40; target(s): 4169.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W02` | First tick exactly 15:00 of OPEN time after reopening: not greater than 15 min -> trade taken. | 09-20 23:15:00 4187.80/4188.00; 09-21 00:30:00 4168.80/4169.00 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; signal time: 2026-09-18T22:00:00Z; entry: 4187.80; stop: 4197.20; R: 9.40; target(s): 4169.00; entry_across_break: True; exit: TARGET net 2.00R |
| `W03` | First tick 15:01 of open time after reopening -> SKIPPED_STALE_ENTRY. Wall-clock since Friday is ~49 h, but only open time counts. | 09-20 23:15:01 4187.80/4188.00 | variant: VARIANT_QUALIFIED, SIGNAL; disposition: SKIPPED_STALE_ENTRY; signal time: 2026-09-18T22:00:00Z |

#### `GV-P07-R01` · `GT-ENGULF-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P06-R01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> RAW (Layer A): ref = open of the bar after the signal bar; horizon h uses close[s+h] and bars s+1..s+h. Only 6 bars follow, so h10/h20 are NULL (data gap rule). Bar 6 has extreme high/low to expose an off-by-one in h5.

Tags: raw, horizon_end
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.00 | 4196.00 |
| 2 | 09-16 10:15 | 4196.50 | 4197.00 | 4187.50 | 4188.00 |
| 3 | 09-16 10:30 | 4188.00 | 4190.00 | 4185.00 | 4187.00 |
| 4 | 09-16 10:45 | 4187.00 | 4189.00 | 4184.00 | 4186.00 |
| 5 | 09-16 11:00 | 4186.00 | 4191.00 | 4185.00 | 4189.00 |
| 6 | 09-16 11:15 | 4189.00 | 4192.00 | 4186.00 | 4188.00 |
| 7 | 09-16 11:30 | 4187.00 | 4190.00 | 4183.00 | 4185.00 |
| 8 | 09-16 11:45 | 4185.00 | 4197.00 | 4179.00 | 4184.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4188.00 | h1: ret=1.00, mfe=3.00, mae=2.00, end_index=2 | h3: ret=-1.00, mfe=4.00, mae=3.00, end_index=4 | h5: ret=3.00, mfe=5.00, mae=4.00, end_index=6 | h10: NULL | h20: NULL

#### `GV-P07-Y00` · `GT-ENGULF-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P06-Y00` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Spec example. B2=8.5>B1=6 (not 2x: 8.5<12). Wicks engulfed: L2=4203<=L1=4203 and H2=4212.5>=H1=4211 -> flag true. Stop = min(L1,L2)-0.20 = 4202.80; entry ask 4212.20; R=9.40; 2R target 4231.00.

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.00 | 4196.00 |
| 2 | 09-16 10:15 | 4196.50 | 4197.00 | 4187.50 | 4188.00 |

Ticks (bid/ask): 09-16 10:30:02 4187.80/4188.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- flags: size2x=False, wicks_engulfed=True
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4187.80
- stop: 4197.20
- R: 9.40
- target(s): 4169.00

#### `GV-P07-Y01` · `GT-ENGULF-BEAR-v1.0/BASE` · M15
*Mirror of `GV-P06-Y01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Clean YES: canonical shape and base pattern formed; BASE variant qualifies, signals at bar completion and trades at the first tick (BUY at ask, 2R).

Tags: clean-yes
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.00 | 4196.00 |
| 2 | 09-16 10:15 | 4196.50 | 4197.00 | 4187.50 | 4188.00 |

Ticks (bid/ask): 09-16 10:30:02 4187.80/4188.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4187.80
- stop: 4197.20
- R: 9.40
- target(s): 4169.00

### Variant `SRC-CB`

#### `GV-P07-V01` · `GT-ENGULF-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P06-V01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> SRC-CB Bullish Engulfing: TREND DOWN AND AT_SUPPORT (lowest low 4203.00 vs zone top 4202.60 = 0.40 = 0.10*ATR exactly) on H1. Stop min(L1,L2)-0.20 = 4202.80; entry ask 4212.20; R 9.40; T_SR(2.0): 4231.00 = 2.00R exactly -> trade.

Tags: variant-clean-yes, boundary
Context: atr=4 · trend=UP · zones_pre=[4197.40-4197.50] · zones_entry=[4168.00-4169.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.00 | 4196.00 |
| 2 | 09-16 11:00 | 4196.50 | 4197.00 | 4187.50 | 4188.00 |

Ticks (bid/ask): 09-16 12:00:02 4187.80/4188.00; 09-16 12:01:40 4168.80/4169.00

- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4187.80
- stop: 4197.20
- R: 9.40
- target(s): 4169.00
- exit: TARGET net 2.00R

#### `GV-P07-V02` · `GT-ENGULF-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P06-V02` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Trend RANGE with support: SRC-CB needs TREND=DOWN AND AT_SUPPORT (both) -> not qualified; BASE also not formed.

Tags: variant-not-qualified
Context: atr=4 · trend=RANGE · zones_pre=[4197.40-4197.50] · zones_entry=[4168.00-4169.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.00 | 4196.00 |
| 2 | 09-16 11:00 | 4196.50 | 4197.00 | 4187.50 | 4188.00 |

Ticks (bid/ask): 09-16 12:00:02 4187.80/4188.00

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P07-V03` · `GT-ENGULF-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P06-V03` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Trend DOWN but no support: BASE formed, CB variant not qualified.

Tags: variant-not-qualified
Context: atr=4 · trend=UP · zones_entry=[4168.00-4169.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.00 | 4196.00 |
| 2 | 09-16 11:00 | 4196.50 | 4197.00 | 4187.50 | 4188.00 |

Ticks (bid/ask): 09-16 12:00:02 4187.80/4188.00

- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P07-V04` · `GT-ENGULF-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P06-V04` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Zone edge 4230.99: 1.9989R -> SKIPPED_SRC_RR.

Tags: T_SR, boundary, insufficient-rr
Context: atr=4 · trend=UP · zones_pre=[4197.40-4197.50] · zones_entry=[4168.00-4169.01]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.00 | 4196.00 |
| 2 | 09-16 11:00 | 4196.50 | 4197.00 | 4187.50 | 4188.00 |

Ticks (bid/ask): 09-16 12:00:02 4187.80/4188.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR
- entry: 4187.80
- stop: 4197.20
- R: 9.40

#### `GV-P07-V05` · `GT-ENGULF-BEAR-v1.0/SRC-CB` · M5
*Mirror of `GV-P06-V05` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> M5 not allowed -> SKIPPED_TF_NOT_ALLOWED.

Tags: tf-gate
Context: atr=4 · trend=UP · zones_pre=[4197.40-4197.50] · zones_entry=[4168.00-4169.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.00 | 4196.00 |
| 2 | 09-16 10:05 | 4196.50 | 4197.00 | 4187.50 | 4188.00 |

Ticks (bid/ask): 09-16 10:10:02 4187.80/4188.00

- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

#### `GV-P07-V06` · `GT-ENGULF-BEAR-v1.0/SRC-CB` · H1
*Mirror of `GV-P06-V06` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> No zone above the entry -> SKIPPED_SRC_NO_TARGET.

Tags: T_SR, no-target
Context: atr=4 · trend=UP · zones_pre=[4197.40-4197.50]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.00 | 4196.00 |
| 2 | 09-16 11:00 | 4196.50 | 4197.00 | 4187.50 | 4188.00 |

Ticks (bid/ask): 09-16 12:00:02 4187.80/4188.00

- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET
- entry: 4187.80
- stop: 4197.20
- R: 9.40

### Variant `SRC-PS`

#### `GV-DORM-P07-01` · `GT-ENGULF-BEAR-v1.0/SRC-PS` · M15
> Bearish source-only qualification: RANGE trend, highest high 4197.00 is 0.30 below resistance. SELL at the bid; stop max(H1,H2) + 20 pips x $0.10 = 4199.00; R 11.00; T_SR(1.5) nearest zone top 4171.00 = 1.545R.

Tags: source-only-qualification, pip-variant
Context: atr=4 · trend=RANGE · zones_pre=[4197.30-4197.50] · zones_entry=[4170.00-4171.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.00 | 4196.00 |
| 2 | 09-16 10:15 | 4196.50 | 4197.00 | 4187.50 | 4188.00 |

Ticks (bid/ask): 09-16 10:30:02 4188.00/4188.20; 09-16 10:31:40 4170.80/4171.00

- canonical: SHAPE_DETECTED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4188.00
- stop: 4199.00
- R: 11.00
- target(s): 4171.00
- exit: TARGET net 17/11 (≈1.5455)R

#### `GV-DORM-P07-02` · `GT-ENGULF-BEAR-v1.0/SRC-PS` · M15
> Signal 03:00 UTC (ASIA_ONLY): skipped.

Tags: session, pip-variant
Context: atr=4 · trend=RANGE · zones_pre=[4197.30-4197.50] · zones_entry=[4170.00-4171.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 02:30 | 4190.00 | 4197.00 | 4189.00 | 4196.00 |
| 2 | 09-16 02:45 | 4196.50 | 4197.00 | 4187.50 | 4188.00 |

Ticks (bid/ask): 09-16 03:00:02 4188.00/4188.20

- canonical: SHAPE_DETECTED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SESSION_FILTER
- signal time: 2026-09-16T03:00:00Z

