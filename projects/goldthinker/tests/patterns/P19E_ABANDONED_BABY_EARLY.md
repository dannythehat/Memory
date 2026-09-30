# P19E Abandoned Baby Early — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.3 · vector pack GV-0.2 · **27 vectors** (27 firm)

Strategies covered: `GT-ABABYEARLY-BEAR-v1.0`, `GT-ABABYEARLY-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-ABABYEARLY-BEAR-v1.0`

### Variant `BASE-EARLY`

#### `GV-P19E-BB01` · `GT-ABABYEARLY-BEAR-v1.0/BASE-EARLY` · M15
> bid_open 4210.61 above the line: no trigger.

Tags: boundary, early-trigger
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |
| 2 | 09-16 10:15 | 4211.20 | 4212.20 | 4210.80 | 4211.25 |

Ticks (bid/ask): 09-16 10:30:00 4210.61/4210.81; 09-16 10:31:40 4180.61/4180.81

- canonical: SHAPE_DETECTED
- variant: no event

#### `GV-P19E-BB02` · `GT-ABABYEARLY-BEAR-v1.0/BASE-EARLY` · M15
> bid_open below the line: triggers; SELL at 4210.30 (bid).

Tags: boundary, early-trigger
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |
| 2 | 09-16 10:15 | 4211.20 | 4212.20 | 4210.80 | 4211.25 |

Ticks (bid/ask): 09-16 10:30:00 4210.30/4210.50; 09-16 10:31:40 4180.30/4180.50

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4210.30

#### `GV-P19E-BL04` · `GT-ABABYEARLY-BEAR-v1.0/BASE-EARLY` · M15
> SL/TP ordering: the stop level is reached first, then the target: only the first counts -> -1.00R.

Tags: lifecycle, sl-tp-ordering, early-trigger
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |
| 2 | 09-16 10:15 | 4211.20 | 4212.20 | 4210.80 | 4211.25 |

Ticks (bid/ask): 09-16 10:30:00 4210.60/4210.80; 09-16 10:31:40 4212.20/4212.40; 09-16 10:33:20 4206.80/4207.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4210.60
- stop: 4212.40
- R: 1.80
- target(s): 4207.00
- exit: STOP net -1.00R

#### `GV-P19E-BL05` · `GT-ABABYEARLY-BEAR-v1.0/BASE-EARLY` · M15
> SL/TP ordering: the target is reached first, then the stop level: only the first counts -> +2.00R.

Tags: lifecycle, sl-tp-ordering, early-trigger
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |
| 2 | 09-16 10:15 | 4211.20 | 4212.20 | 4210.80 | 4211.25 |

Ticks (bid/ask): 09-16 10:30:00 4210.60/4210.80; 09-16 10:31:40 4206.80/4207.00; 09-16 10:33:20 4212.20/4212.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4210.60
- stop: 4212.40
- R: 1.80
- target(s): 4207.00
- exit: TARGET net 2.00R

#### `GV-P19E-BL06` · `GT-ABABYEARLY-BEAR-v1.0/BASE-EARLY` · M15
> No ticks after entry; one OHLC bar whose range contains both stop and target: STOP FIRST, with the +2.00R target-first sensitivity reported.

Tags: lifecycle, missing-tick-stop-first, early-trigger
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |
| 2 | 09-16 10:15 | 4211.20 | 4212.20 | 4210.80 | 4211.25 |

Bars after entry (no ticks): 4210.60/4212.70/4206.00/4210.60

Ticks (bid/ask): 09-16 10:30:00 4210.60/4210.80
*No ticks after entry: resolve from the OHLC bar only.*

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4210.60
- stop: 4212.40
- R: 1.80
- target(s): 4207.00
- exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R]

#### `GV-P19E-BT01` · `GT-ABABYEARLY-BEAR-v1.0/BASE-EARLY` · M15
> Trend DOWN: not formed.

Tags: wrong-trend
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |
| 2 | 09-16 10:15 | 4211.20 | 4212.20 | 4210.80 | 4211.25 |

Ticks (bid/ask): 09-16 10:30:00 4210.60/4210.80; 09-16 10:31:40 4180.60/4180.80

- canonical: SHAPE_DETECTED
- variant: no event

#### `GV-P19E-BY01` · `GT-ABABYEARLY-BEAR-v1.0/BASE-EARLY` · M15
> Bear side: C1 bullish LARGE, C2 doji gapped above (L2 4210.80 >= H1+0.20), trend UP, bid_open 4210.60 = L2 - gap_thr exactly. SELL at the BID; stop H2+0.20 = 4212.40; R=1.80; target 4207.00.

Tags: clean-yes, early-trigger
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |
| 2 | 09-16 10:15 | 4211.20 | 4212.20 | 4210.80 | 4211.25 |

Ticks (bid/ask): 09-16 10:30:00 4210.60/4210.80; 09-16 10:31:40 4206.80/4207.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4210.60
- stop: 4212.40
- R: 1.80
- target(s): 4207.00
- exit: TARGET net 2.00R

### Variant `SRC-PS-EARLY`

#### `GV-P19E-V10` · `GT-ABABYEARLY-BEAR-v1.0/SRC-PS-EARLY` · M15
> Source Abandoned Baby early setup, BEAR side: bid_open 4210.60 = L2 - gap_thr; SELL at the bid; stop H2+0.20 = 4212.40; R 1.80; swing low 4207.90 = exactly 1.5R -> +1.50R.

Tags: variant, early-trigger, boundary
Context: atr=4 · trend=UP · swings=L4207.90

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |
| 2 | 09-16 10:15 | 4211.20 | 4212.20 | 4210.80 | 4211.25 |

Ticks (bid/ask): 09-16 10:30:00 4210.60/4210.80; 09-16 10:31:40 4207.70/4207.90

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4210.60
- stop: 4212.40
- R: 1.80
- target(s): 4207.90
- exit: TARGET net 1.50R

#### `GV-P19E-V11` · `GT-ABABYEARLY-BEAR-v1.0/SRC-PS-EARLY` · M15
> Swing low 4207.91 -> 1.494R -> SKIPPED_SRC_RR.

Tags: variant, insufficient-rr
Context: atr=4 · trend=UP · swings=L4207.91

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |
| 2 | 09-16 10:15 | 4211.20 | 4212.20 | 4210.80 | 4211.25 |

Ticks (bid/ask): 09-16 10:30:00 4210.60/4210.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR

## `GT-ABABYEARLY-BULL-v1.0`

### Variant `BASE-EARLY`

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L02` | Stopped at 4201.60. | 09-16 10:30:00 4203.40/4203.60; 09-16 10:31:40 4201.60/4201.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; exit: STOP net -1.00R |
| `L04` | SL/TP ordering: the stop level is reached first, then the target: only the first counts -> -1.00R. | 09-16 10:30:00 4203.40/4203.60; 09-16 10:31:40 4201.60/4201.80; 09-16 10:33:20 4207.60/4207.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4203.60; stop: 4201.60; R: 2.00; target(s): 4207.60; exit: STOP net -1.00R |
| `L05` | SL/TP ordering: the target is reached first, then the stop level: only the first counts -> +2.00R. | 09-16 10:30:00 4203.40/4203.60; 09-16 10:31:40 4207.60/4207.80; 09-16 10:33:20 4201.60/4201.80 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4203.60; stop: 4201.60; R: 2.00; target(s): 4207.60; exit: TARGET net 2.00R |
| `L06` | No ticks after entry; one OHLC bar whose range contains both stop and target: STOP FIRST, with the +2.00R target-first sensitivity reported. | 09-16 10:30:00 4203.40/4203.60 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4203.60; stop: 4201.60; R: 2.00; target(s): 4207.60; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |

#### `GV-P19E-B01` · `GT-ABABYEARLY-BULL-v1.0/BASE-EARLY` · M15
> bid_open 4203.39 just below H2+gap_thr (ask 4203.59 is not used): no trigger.

Tags: boundary, early-trigger, bid-not-ask
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |

Ticks (bid/ask): 09-16 10:30:00 4203.39/4203.59; 09-16 10:31:40 4233.39/4233.59

- canonical: SHAPE_DETECTED
- variant: no event

#### `GV-P19E-B02` · `GT-ABABYEARLY-BULL-v1.0/BASE-EARLY` · M15
> bid_open one tick above the line: triggers.

Tags: boundary, early-trigger
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |

Ticks (bid/ask): 09-16 10:30:00 4203.41/4203.61; 09-16 10:31:40 4233.41/4233.61

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4203.61

#### `GV-P19E-B03` · `GT-ABABYEARLY-BULL-v1.0/BASE-EARLY` · M15
> Spread 0.80: ask 4203.80 is above the line but bid 4203.00 is not: no trigger.

Tags: early-trigger, bid-not-ask, spread
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |

Ticks (bid/ask): 09-16 10:30:00 4203.00/4203.80; 09-16 10:31:40 4233.00/4233.20

- canonical: SHAPE_DETECTED
- variant: no event

#### `GV-P19E-L03` · `GT-ABABYEARLY-BULL-v1.0/BASE-EARLY` · M15
> Selection-bias guard (D-026): the trigger is a trade whether or not the completed Abandoned Baby later forms.

Tags: early-trigger, no-selection-bias
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |

Ticks (bid/ask): 09-16 10:30:00 4203.40/4203.60; 09-16 10:31:40 4203.00/4203.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE

#### `GV-P19E-N01` · `GT-ABABYEARLY-BULL-v1.0/BASE-EARLY` · M15
> C2 not gapped enough (H2 4203.31): no shape.

Tags: clean-no
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4203.00 | 4203.31 | 4201.80 | 4203.05 |

Ticks (bid/ask): 09-16 10:30:00 4203.40/4203.60; 09-16 10:31:40 4233.40/4233.60

- canonical: no event
- failing clause(s): H2<=L1-gap

#### `GV-P19E-N02` · `GT-ABABYEARLY-BULL-v1.0/BASE-EARLY` · M15
> C2 not a doji (B 1.0): no shape.

Tags: clean-no
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.00 | 4203.20 | 4201.80 | 4203.00 |

Ticks (bid/ask): 09-16 10:30:00 4203.40/4203.60; 09-16 10:31:40 4233.40/4233.60

- canonical: no event
- failing clause(s): DOJI(K2)

#### `GV-P19E-R01` · `GT-ABABYEARLY-BULL-v1.0/BASE-EARLY` · M15
> RAW for the Abandoned Baby Early trigger: ref = ask 4203.60; the signal bar is index 2 (the bar containing the trigger tick), horizon_end(h) = 2 + h - 1 -> h1 end index 2, h3 end index 4, h5 end index 6; the bar at index 7 (extreme) is excluded from every horizon shown.

Tags: raw, horizon_end, tick-based, off-by-one
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |
| 3 | 09-16 10:30 | 4203.40 | 4206.00 | 4203.00 | 4205.00 |
| 4 | 09-16 10:45 | 4205.00 | 4208.00 | 4204.50 | 4207.00 |
| 5 | 09-16 11:00 | 4207.00 | 4209.00 | 4200.00 | 4201.00 |
| 6 | 09-16 11:15 | 4201.00 | 4202.00 | 4199.00 | 4200.00 |
| 7 | 09-16 11:30 | 4200.00 | 4203.00 | 4198.00 | 4202.00 |
| 8 | 09-16 11:45 | 4202.00 | 4250.00 | 4150.00 | 4180.00 |

Ticks (bid/ask): 09-16 10:30:00 4203.40/4203.60

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4203.60 | h1: end_index=2, ret=1.40, mfe=2.40, mae=0.60 | h3: end_index=4, ret=-2.60, mfe=5.40, mae=3.60 | h5: end_index=6, ret=-1.60, mfe=5.40, mae=5.60 | h10: NULL | h20: NULL

#### `GV-P19E-T01` · `GT-ABABYEARLY-BULL-v1.0/BASE-EARLY` · M15
> Trend RANGE: shape only.

Tags: wrong-trend
Context: atr=4 · trend=RANGE

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |

Ticks (bid/ask): 09-16 10:30:00 4203.40/4203.60; 09-16 10:31:40 4233.40/4233.60

- canonical: SHAPE_DETECTED
- variant: no event

#### `GV-P19E-W01` · `GT-ABABYEARLY-BULL-v1.0/BASE-EARLY` · H1
> Weekend: C2 (Fri 21:00) completes at the Friday close; the first tick after the reopening has bid 4203.40 = H2 + gap_thr -> trigger; BUY at the ask.

Tags: early-trigger, weekend-entry
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 20:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-18 21:00 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |

Ticks (bid/ask): 09-20 23:00:00 4203.40/4203.60; 09-21 00:30:00 4207.60/4207.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-20T23:00:00Z
- entry: 4203.60
- stop: 4201.60
- R: 2.00
- target(s): 4207.60
- exit: TARGET net 2.00R

#### `GV-P19E-W02` · `GT-ABABYEARLY-BULL-v1.0/BASE-EARLY` · H1
> Weekend gap leaves bid 4203.30 < H2 + gap_thr (4203.40): no trigger.

Tags: early-trigger, weekend-entry
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 20:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-18 21:00 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |

Ticks (bid/ask): 09-20 23:00:00 4203.30/4203.50

- canonical: SHAPE_DETECTED
- variant: no event

#### `GV-P19E-Y01` · `GT-ABABYEARLY-BULL-v1.0/BASE-EARLY` · M15
> Clean YES: C1 bearish LARGE, C2 doji gapped below (H2 4203.20 <= L1-0.20), trend DOWN, bid_open 4203.40 = H2 + gap_thr exactly. BUY at the ask 4203.60; stop L2-0.20 = 4201.60; R=2.00; target 4207.60.

Tags: clean-yes, early-trigger
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |

Ticks (bid/ask): 09-16 10:30:00 4203.40/4203.60; 09-16 10:31:40 4233.40/4233.60

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:30:00Z
- entry: 4203.60
- stop: 4201.60
- R: 2.00
- target(s): 4207.60
- exit: TARGET net 2.00R

### Variant `SRC-PS-EARLY`

#### `GV-P19E-V01` · `GT-ABABYEARLY-BULL-v1.0/SRC-PS-EARLY` · M15
> Source Abandoned Baby early setup: trigger bid_open = H2 + gap_thr; BUY at the ask 4203.60; stop 4201.60 (R 2.00); T_SWING(1.5): swing 4206.60 = exactly 1.5R -> trade, +1.50R.

Tags: variant, early-trigger, boundary
Context: atr=4 · trend=DOWN · swings=H4206.60

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |

Ticks (bid/ask): 09-16 10:30:00 4203.40/4203.60; 09-16 10:31:40 4206.60/4206.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4203.60
- stop: 4201.60
- R: 2.00
- target(s): 4206.60
- exit: TARGET net 1.50R

#### `GV-P19E-V02` · `GT-ABABYEARLY-BULL-v1.0/SRC-PS-EARLY` · M15
> Swing 4206.59 -> 1.495R -> SKIPPED_SRC_RR.

Tags: variant, early-trigger, insufficient-rr
Context: atr=4 · trend=DOWN · swings=H4206.59

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |

Ticks (bid/ask): 09-16 10:30:00 4203.40/4203.60

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR

#### `GV-P19E-V03` · `GT-ABABYEARLY-BULL-v1.0/SRC-PS-EARLY` · M15
> No swing -> NO_TARGET.

Tags: variant, early-trigger, no-target
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |

Ticks (bid/ask): 09-16 10:30:00 4203.40/4203.60

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET

