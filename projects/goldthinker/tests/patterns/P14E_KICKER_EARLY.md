# P14E Kicker Early — golden test vectors

Spec: `CANDLE_SPEC_V1.md` Draft 0.3 · vector pack GV-0.2 · **33 vectors** (33 firm)

Strategies covered: `GT-KICKEREARLY-BEAR-v1.0`, `GT-KICKEREARLY-BULL-v1.0`

Read `README.md` first (conventions: ATR is injected as 4.00 unless stated, test account, exact decimal arithmetic, statuses). All numbers are USD/oz. Bars are **bid** OHLC; ticks list bid/ask. Prices in expectations are exact.

## `GT-KICKEREARLY-BEAR-v1.0`

### Variant `BASE-EARLY`

#### `GV-P14E-BB01` · `GT-KICKEREARLY-BEAR-v1.0/BASE-EARLY` · M15
> bid_open 4204.01 > O1: no trigger. The ask (4204.21) is irrelevant.

Tags: boundary, early-trigger
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |

Ticks (bid/ask): 09-16 10:15:00 4204.01/4204.21; 09-16 10:16:40 4174.01/4174.21

- canonical: SHAPE_DETECTED
- variant: no event

#### `GV-P14E-BB02` · `GT-KICKEREARLY-BEAR-v1.0/BASE-EARLY` · M15
> bid_open 4203.80 < O1 -> triggers: SELL at the bid 4203.80 even though the ask equals O1.

Tags: boundary, early-trigger, bid-not-ask
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |

Ticks (bid/ask): 09-16 10:15:00 4203.80/4204.00; 09-16 10:16:40 4173.80/4174.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4203.80

#### `GV-P14E-BL04` · `GT-KICKEREARLY-BEAR-v1.0/BASE-EARLY` · M15
> SL/TP ordering: the stop level is reached first, then the target: only the first counts -> -1.00R.

Tags: lifecycle, sl-tp-ordering, early-trigger
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |

Ticks (bid/ask): 09-16 10:15:00 4204.00/4204.20; 09-16 10:16:40 4210.50/4210.70; 09-16 10:18:20 4190.40/4190.60

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4204.00
- stop: 4210.70
- R: 6.70
- target(s): 4190.60
- exit: STOP net -1.00R

#### `GV-P14E-BL05` · `GT-KICKEREARLY-BEAR-v1.0/BASE-EARLY` · M15
> SL/TP ordering: the target is reached first, then the stop level: only the first counts -> +2.00R.

Tags: lifecycle, sl-tp-ordering, early-trigger
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |

Ticks (bid/ask): 09-16 10:15:00 4204.00/4204.20; 09-16 10:16:40 4190.40/4190.60; 09-16 10:18:20 4210.50/4210.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4204.00
- stop: 4210.70
- R: 6.70
- target(s): 4190.60
- exit: TARGET net 2.00R

#### `GV-P14E-BL06` · `GT-KICKEREARLY-BEAR-v1.0/BASE-EARLY` · M15
> No ticks after entry; one OHLC bar whose range contains both stop and target: STOP FIRST, with the +2.00R target-first sensitivity reported.

Tags: lifecycle, missing-tick-stop-first, early-trigger
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |

Bars after entry (no ticks): 4204.00/4211.00/4189.60/4204.00

Ticks (bid/ask): 09-16 10:15:00 4204.00/4204.20
*No ticks after entry: resolve from the OHLC bar only.*

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4204.00
- stop: 4210.70
- R: 6.70
- target(s): 4190.60
- exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R]

#### `GV-P14E-BT01` · `GT-KICKEREARLY-BEAR-v1.0/BASE-EARLY` · M15
> Trend DOWN: bearish early setup needs UP -> shape only.

Tags: wrong-trend
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |

Ticks (bid/ask): 09-16 10:15:00 4204.00/4204.20; 09-16 10:16:40 4174.00/4174.20

- canonical: SHAPE_DETECTED
- variant: no event

#### `GV-P14E-BY01` · `GT-KICKEREARLY-BEAR-v1.0/BASE-EARLY` · M15
> Bear early setup: C1 bullish LARGE (O1=4204.00), trend UP, bid_open 4204.00 <= O1. SELL at the BID 4204.00; stop H1+0.20 = 4210.70; R=6.70; target 4190.60.

Tags: clean-yes, early-trigger
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |

Ticks (bid/ask): 09-16 10:15:00 4204.00/4204.20; 09-16 10:16:40 4190.40/4190.60

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:15:00Z
- entry: 4204.00
- stop: 4210.70
- R: 6.70
- target(s): 4190.60
- exit: TARGET net 2.00R

### Variant `SRC-PS-EARLY`

#### `GV-P14E-V10` · `GT-KICKEREARLY-BEAR-v1.0/SRC-PS-EARLY` · H1
> Source Kicker early setup, BEAR side, H1: C1 bullish LARGE, trend UP, bid_open 4204.00 <= O1 -> SELL at the BID 4204.00; stop H1+0.20 = 4210.70; T_SWING(1.5): swing low 4193.95 is exactly 1.5R below -> +1.50R.

Tags: variant, early-trigger, boundary
Context: atr=4 · trend=UP · swings=L4193.95

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |

Ticks (bid/ask): 09-16 11:00:00 4204.00/4204.20; 09-16 11:01:40 4193.75/4193.95

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4204.00
- stop: 4210.70
- R: 6.70
- target(s): 4193.95
- exit: TARGET net 1.50R

#### `GV-P14E-V11` · `GT-KICKEREARLY-BEAR-v1.0/SRC-PS-EARLY` · H1
> Swing low 4193.96 -> 1.4985R -> SKIPPED_SRC_RR.

Tags: variant, insufficient-rr
Context: atr=4 · trend=UP · swings=L4193.96

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |

Ticks (bid/ask): 09-16 11:00:00 4204.00/4204.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR

#### `GV-P14E-V12` · `GT-KICKEREARLY-BEAR-v1.0/SRC-PS-EARLY` · M15
> M15 not allowed for the source variant.

Tags: variant, tf-gate
Context: atr=4 · trend=UP · swings=L4193.65

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |

Ticks (bid/ask): 09-16 10:15:00 4204.00/4204.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

## `GT-KICKEREARLY-BULL-v1.0`

### Variant `BASE-EARLY`

#### Trade lifecycle (BASE: entry at the first executable tick, stop beyond the pattern extreme, fixed 2R)

| ID | scenario | ticks (bid/ask) | expected |
|---|---|---|---|
| `L02` | Same trade, stopped: bid reaches 4203.30. | 09-16 10:15:00 4210.00/4210.20; 09-16 10:16:40 4203.30/4203.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4210.20; exit: STOP net -1.00R |
| `L04` | SL/TP ordering: the stop level is reached first, then the target: only the first counts -> -1.00R. | 09-16 10:15:00 4210.00/4210.20; 09-16 10:16:40 4203.30/4203.50; 09-16 10:18:20 4224.00/4224.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4210.20; stop: 4203.30; R: 6.90; target(s): 4224.00; exit: STOP net -1.00R |
| `L05` | SL/TP ordering: the target is reached first, then the stop level: only the first counts -> +2.00R. | 09-16 10:15:00 4210.00/4210.20; 09-16 10:16:40 4224.00/4224.20; 09-16 10:18:20 4203.30/4203.50 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4210.20; stop: 4203.30; R: 6.90; target(s): 4224.00; exit: TARGET net 2.00R |
| `L06` | No ticks after entry; one OHLC bar whose range contains both stop and target: STOP FIRST, with the +2.00R target-first sensitivity reported. | 09-16 10:15:00 4210.00/4210.20 | variant: VARIANT_QUALIFIED, SIGNAL, TRADE; entry: 4210.20; stop: 4203.30; R: 6.90; target(s): 4224.00; exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R] |

#### `GV-P14E-B01` · `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` · M15
> bid_open one tick above O1: triggers.

Tags: boundary, early-trigger
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-16 10:15:00 4210.01/4210.21; 09-16 10:16:40 4240.01/4240.21

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4210.21

#### `GV-P14E-B02` · `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` · M15
> bid_open 4209.99 < O1 (4210.00) but the ASK 4210.19 is above O1: must NOT trigger - detection tests the bid/chart price, not the ask (0.2.1 fix 3). SHAPE_DETECTED only; no trade.

Tags: boundary, early-trigger, bid-not-ask
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-16 10:15:00 4209.99/4210.19; 09-16 10:16:40 4239.99/4240.19

- canonical: SHAPE_DETECTED
- variant: no event
- disposition: NOT_QUALIFIED

#### `GV-P14E-B03` · `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` · M15
> Wide spread 1.00: bid 4209.60 below O1, ask 4210.60 above it: still no trigger.

Tags: early-trigger, bid-not-ask, spread
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-16 10:15:00 4209.60/4210.60; 09-16 10:16:40 4239.60/4239.80

- canonical: SHAPE_DETECTED
- variant: no event

#### `GV-P14E-B04` · `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` · M15
> Opens well above O1: triggers; entry at the ask; R measured from the actual fill.

Tags: early-trigger
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-16 10:15:00 4212.00/4212.20; 09-16 10:16:40 4242.00/4242.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4212.20
- stop: 4203.30
- R: 8.90
- target(s): 4230.00

#### `GV-P14E-L03` · `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` · M15
> Selection-bias guard (D-026): the trigger counts as a trade whether or not the completed Kicker later forms; here C2 turns out small (would not be a Kicker) and the trade is still taken and just stays open.

Tags: early-trigger, no-selection-bias
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-16 10:15:00 4210.00/4210.20; 09-16 10:16:40 4207.00/4207.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE

#### `GV-P14E-N01` · `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` · M15
> C1 not LARGE (B=2.0, R=2.5): no shape.

Tags: clean-no
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4206.00 | 4206.30 | 4203.80 | 4204.00 |

Ticks (bid/ask): 09-16 10:15:00 4210.00/4210.20; 09-16 10:16:40 4240.00/4240.20

- canonical: no event
- failing clause(s): LARGE(K1)

#### `GV-P14E-N02` · `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` · M15
> C1 bullish: the bullish early setup needs a bearish C1.

Tags: clean-no
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4204.00 | 4210.50 | 4203.50 | 4210.00 |

Ticks (bid/ask): 09-16 10:15:00 4210.00/4210.20; 09-16 10:16:40 4240.00/4240.20

- canonical: no event
- failing clause(s): K1 bear

#### `GV-P14E-QF1` · `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` · M15
> Early Kicker whose opening BID 4209.99 is below O1: the shape exists (K1) but the trigger is not met -> failure TRIGGER_NOT_MET.

Tags: qualification-failures, early-trigger
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-16 10:15:00 4209.99/4210.19

- canonical: SHAPE_DETECTED
- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TRIGGER_NOT_MET

#### `GV-P14E-R01` · `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` · M15
> RAW for a TICK-based signal (Kicker Early): ref = the trigger tick's ASK 4210.20; the signal bar is the bar containing the tick (index 1) and counts as bar 1, so horizon_end(h) = s + h - 1: h1 uses close[1] (4212.00 -> +1.80), h3 uses close[3], h5 uses close[5] (the last bar, index 6, has an extreme range 4190-4230 and must NOT be in h5). A close-based reading (s + h) would give h1 = close[2].

Tags: raw, horizon_end, tick-based, off-by-one
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4210.00 | 4213.00 | 4208.00 | 4212.00 |
| 3 | 09-16 10:30 | 4212.00 | 4216.00 | 4211.00 | 4215.00 |
| 4 | 09-16 10:45 | 4215.00 | 4217.00 | 4209.50 | 4210.50 |
| 5 | 09-16 11:00 | 4210.50 | 4212.00 | 4206.00 | 4207.00 |
| 6 | 09-16 11:15 | 4207.00 | 4209.00 | 4203.00 | 4204.00 |
| 7 | 09-16 11:30 | 4204.00 | 4230.00 | 4190.00 | 4200.00 |

Ticks (bid/ask): 09-16 10:15:00 4210.00/4210.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4210.20 | h1: end_index=1, ret=1.80, mfe=2.80, mae=2.20 | h3: end_index=3, ret=0.30, mfe=6.80, mae=2.20 | h5: end_index=5, ret=-6.20, mfe=6.80, mae=7.20 | h10: NULL | h20: NULL

#### `GV-P14E-T01` · `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` · M15
> Trigger condition true but trend RANGE: SHAPE only.

Tags: wrong-trend, early-trigger
Context: atr=4 · trend=RANGE

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-16 10:15:00 4210.00/4210.20; 09-16 10:16:40 4240.00/4240.20

- canonical: SHAPE_DETECTED
- variant: no event

#### `GV-P14E-T02` · `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` · M15
> Trend UP: not formed.

Tags: wrong-trend, early-trigger
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-16 10:15:00 4210.00/4210.20; 09-16 10:16:40 4240.00/4240.20

- canonical: SHAPE_DETECTED
- variant: no event

#### `GV-P14E-W01` · `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` · H1
> Weekend: the H1 C1 bar (Fri 21:00) completes at the Friday 22:00 close. The early trigger tests the FIRST executable tick after the reopening (Sun 23:00:00): the market gaps up to bid 4212.00 >= O1 4210.00 -> triggers; BUY at the ask 4212.20 (a bigger R because of the gap). No stale rule applies: the trigger tick IS the first tick.

Tags: early-trigger, weekend-entry, gap
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 21:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-20 23:00:00 4212.00/4212.20; 09-21 00:30:00 4230.00/4230.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-20T23:00:00Z
- entry: 4212.20
- stop: 4203.30
- R: 8.90
- target(s): 4230.00
- exit: TARGET net 2.00R

#### `GV-P14E-W02` · `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` · H1
> Weekend gap DOWN: first tick after reopening bid 4205.00 < O1 4210.00 -> no trigger (the pattern is not chased later).

Tags: early-trigger, weekend-entry, gap
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 21:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-20 23:00:00 4205.00/4205.20

- canonical: SHAPE_DETECTED
- variant: no event

#### `GV-P14E-Y01` · `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` · M15
> Clean YES: C1 bearish LARGE, trend DOWN, bid_open 4210.00 = O1 exactly. BUY at the ask 4210.20 (executes at ask, detects on bid). Stop L1-0.20 = 4203.30, R=6.90, 2R target 4224.00.

Tags: clean-yes, early-trigger
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-16 10:15:00 4210.00/4210.20; 09-16 10:16:40 4240.00/4240.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:15:00Z
- entry: 4210.20
- stop: 4203.30
- R: 6.90
- target(s): 4224.00
- exit: TARGET net 2.00R

### Variant `SRC-PS-EARLY`

#### `GV-P14E-V01` · `GT-KICKEREARLY-BULL-v1.0/SRC-PS-EARLY` · H1
> Source Kicker early setup on H1: bid_open = O1 -> trigger; BUY at the ask 4210.20; stop 4203.30; T_SWING(1.5): swing high 4220.55 = exactly 1.5R (10.35/6.90) -> trade, hit: +1.50R.

Tags: variant, early-trigger, boundary
Context: atr=4 · trend=DOWN · swings=H4220.55

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-16 11:00:00 4210.00/4210.20; 09-16 11:01:40 4220.55/4220.75

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T11:00:00Z
- entry: 4210.20
- stop: 4203.30
- R: 6.90
- target(s): 4220.55
- exit: TARGET net 1.50R

#### `GV-P14E-V02` · `GT-KICKEREARLY-BULL-v1.0/SRC-PS-EARLY` · H1
> Swing 4220.54 -> 1.4986R: SKIPPED_SRC_RR. The early trigger fired (the base event is still counted) but the source plan does not trade.

Tags: variant, early-trigger, insufficient-rr
Context: atr=4 · trend=DOWN · swings=H4220.54

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-16 11:00:00 4210.00/4210.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_RR

#### `GV-P14E-V03` · `GT-KICKEREARLY-BULL-v1.0/SRC-PS-EARLY` · M15
> M15 is not an allowed timeframe for the source variant: SKIPPED_TF_NOT_ALLOWED although the base early pattern formed.

Tags: variant, tf-gate
Context: atr=4 · trend=DOWN · swings=H4220.55

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-16 10:15:00 4210.00/4210.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: no event
- disposition: NOT_QUALIFIED
- qualification_failures: TF_NOT_ALLOWED

#### `GV-P14E-V04` · `GT-KICKEREARLY-BULL-v1.0/SRC-PS-EARLY` · H1
> No swing -> SKIPPED_SRC_NO_TARGET.

Tags: variant, early-trigger, no-target
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-16 11:00:00 4210.00/4210.20

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_SRC_NO_TARGET

#### `GV-P14E-V05` · `GT-KICKEREARLY-BULL-v1.0/SRC-PS-EARLY` · H1
> bid_open 4209.99 < O1: no trigger (bid test) even though the ask is above O1.

Tags: variant, early-trigger, bid-not-ask
Context: atr=4 · trend=DOWN · swings=H4220.55

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |

Ticks (bid/ask): 09-16 11:00:00 4209.99/4210.19

- canonical: SHAPE_DETECTED
- variant: no event

