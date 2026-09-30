# Execution, timeframe and bar-boundary vectors

Spec Draft 0.2.2 · vector pack GV-0.1. Uses the Hammer BASE strategy as a carrier so the ONLY thing changing between vectors is the mechanic under test.

#### `GV-EX-B01` · `GT-HAMMER-BULL-v1.0/BASE` · **BLOCKED_AMBIGUITY**
> MAX_HOLD = 50 bars: 'close at market after 50 bars of the pattern's own TF'. The spec does not say whether the entry bar counts as bar 1, nor what happens when the 50 bars straddle a scheduled closure. Entry at 10:15:02 on M15 (the 10:15 bar is the entry bar); the daily pause 22:00-23:00 UTC removes four bars.

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-16 10:15:02 4200.20/4200.40

Candidate rulings (no expected value is asserted until the spec settles one):
- Reading A (entry bar = bar 1): the time stop fires at the completion of the 50th bar = 2026-09-16T23:45:00Z (bars 10:15...21:45 = 46 bars, then 23:00, 23:15, 23:30, 23:45).
- Reading B (50 bars AFTER the entry bar): fires at 2026-09-17T00:00:00Z.
- Reading C (wall-clock 50 x 15 min = 12.5 h): fires at 2026-09-16T22:45:02Z - inside the closure, so not executable; must then be the first tick after reopening.

#### `GV-EX-B02` · `GT-HAMMER-BULL-v1.0/BASE` · **BLOCKED_AMBIGUITY**
> Swap: G9 says results are 'minus swap and commission converted to R (from the account spec)' but the spec gives no swap rule: which nights count (rollover at 22:00 UTC?), the triple-swap weekday, whether swap is per lot per night in account currency, and how it converts to R. A trade held from Tue 10:15 to Thu 10:15 crosses two rollovers (and Wed's is normally tripled).

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-16 10:15:02 4200.20/4200.40

Candidate rulings (no expected value is asserted until the spec settles one):
- Cannot be evaluated until the account fixture defines swap_long/swap_short, the rollover time and the triple-swap day.

#### `GV-EX-B03` · `GT-HAMMER-BULL-v1.0/BASE` · **BLOCKED_AMBIGUITY**
> Weekend gap THROUGH the stop at entry: Friday H1 hammer, stop 4193.80, but the first tick after the weekend is bid 4189.50 / ask 4189.70 (entry across a break). The spec says 'any gap through the stop fills at the first price' but a BUY at ask 4189.70 is already BELOW the stop: R = |entry - stop| = 4.10 is positive by formula but the trade is nonsensical (stop above entry).

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 21:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-20 23:00:05 4189.50/4189.70

Candidate rulings (no expected value is asserted until the spec settles one):
- Reading A: skip with a new reason code (e.g. SKIPPED_ENTRY_BEYOND_STOP); nothing is traded.
- Reading B: enter at 4189.70 and stop out at that same price/next tick: a loss of (4189.70-4200.40... ) - the loss is real but R is undefined.
- Reading C (literal): R = |4189.70 - 4193.80| = 4.10 and target = 4189.70 + 8.20 = 4197.90 - a long with the stop above the entry price.

#### `GV-EX-B04` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · **BLOCKED_AMBIGUITY**
> Bars-only resolution for a SHORT: stops and targets for shorts trigger on the ASK, but an OHLC bar has only bid prices. Short: entry bid 4199.60, stop 4206.20, R 6.60. A later bar has high 4206.10 (bid) - 0.10 below the stop - with a recorded spread of 0.20.

Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |

Ticks (bid/ask): 09-16 10:15:02 4199.60/4199.80

Candidate rulings (no expected value is asserted until the spec settles one):
- Reading A: bid-only bars: high 4206.10 < stop 4206.20 -> stop NOT hit.
- Reading B: ask = bar high + the bar's spread 0.20 = 4206.30 >= stop -> stop hit (the calculator used this).
- Reading C: use a fixed assumed spread (which value?).

#### `GV-EX-B05` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · **BLOCKED_AMBIGUITY**
> Does SKIPPED_R_TOO_SMALL apply to SOURCE variants? The rule is written inside the Layer B (baseline) target bullet only, but source variants have their own stops. Spread 3.10 (wide): entry ask 4212.10, SRC-PS stop 4199.80 -> R 12.30, which is below 4 x spread = 12.40. The source target (T_SR zone edge 4262.00) is 4.06R away, so no other rule interferes.

Context: atr=4 · trend=DOWN · zones_entry=[4262.00-4263.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4212.10

Candidate rulings (no expected value is asserted until the spec settles one):
- Reading A (baseline-only rule): the SRC-PS variant takes the trade.
- Reading B (the rule applies to every variant): SKIPPED_R_TOO_SMALL, no trade.

#### `GV-EX-B06` · `GT-HAMMER-BULL-v1.0/BASE` · **BLOCKED_AMBIGUITY**
> RAW MAE sign convention: G8 defines MFE_h as 'best d*(extreme - ref)' and MAE_h as 'worst adverse'. It does not say if MAE is reported negative (min of d*(extreme-ref)), as a positive magnitude, or clamped at 0 when price never trades against the reference. Bars after the hammer never trade below the reference open 4200.20 (lows >= 4199.90 -> adverse excursion -0.30).

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.20 | 4203.00 | 4199.90 | 4202.00 |
| 3 | 09-16 10:30 | 4200.20 | 4203.00 | 4199.90 | 4202.00 |
| 4 | 09-16 10:45 | 4200.20 | 4203.00 | 4199.90 | 4202.00 |
| 5 | 09-16 11:00 | 4200.20 | 4203.00 | 4199.90 | 4202.00 |
| 6 | 09-16 11:15 | 4200.20 | 4203.00 | 4199.90 | 4202.00 |
| 7 | 09-16 11:30 | 4200.20 | 4203.00 | 4199.90 | 4202.00 |

Candidate rulings (no expected value is asserted until the spec settles one):
- Reading A: MAE_1 = -0.30 (negative, min of d*(low - ref)).
- Reading B: MAE_1 = 0.30 (magnitude).
- Reading C: clamped at 0 when the low is above ref (not the case here, low is 0.30 below).

#### `GV-EX-CM-01` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> Commission $7.00 per lot round trip (test account): lots 5/33, commission 7/660 R = 0.0106R. Target hit: +2.00R gross, 1313/660 = +1.9894R net.

Tags: commission
Context: atr=4 · trend=DOWN · account=commission_rt_per_lot=7.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-16 10:15:02 4200.20/4200.40; 09-16 10:16:40 4213.60/4213.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4200.40
- stop: 4193.80
- R: 6.60
- target(s): 4213.60
- exit: TARGET net 1313/660 (≈1.9894)R (gross 2.00R)

#### `GV-EX-CM-02` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> Same commission on a stopped trade: -1.00R gross, -667/660 = -1.0106R net.

Tags: commission
Context: atr=4 · trend=DOWN · account=commission_rt_per_lot=7.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-16 10:15:02 4200.20/4200.40; 09-16 10:16:40 4193.80/4194.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- exit: STOP net -667/660 (≈-1.0106)R (gross -1.00R)

#### `GV-G-ZN-11` · `atzone` · **BLOCKED_AMBIGUITY**
> Dead zones: G4 says a zone is 'dead once a completed bar closes more than 0.10*ATR beyond its far edge' but never says WHICH edge is 'far' (a zone has no side until it is used as support or resistance, and role flips are not modelled). Take zone [4229.80, 4230.80] and a bar that closes at 4231.30 (0.50 above the zone top).

Candidate rulings (no expected value is asserted until the spec settles one):
- Reading A: 'far edge' = the edge farthest from where price came from, i.e. a close above the zone kills it as RESISTANCE and a close below kills it as SUPPORT - the same zone can be dead for one role and alive for the other.
- Reading B: any close more than 0.10*ATR beyond EITHER edge kills the zone for all purposes.
- Reading C: far edge = the top for a resistance zone and the bottom for a support zone, where the role is fixed by which side of the zone price was on when it formed.

#### `GV-TF-D1-01` · `GT-HAMMER-BULL-v1.0/BASE` · D1
> D1 bar (Sunday 23:00 open) completes Monday 22:00; entry after the pause. Baseline: BUY ask 4200.40, stop 4193.80, 2R 4213.60.

Tags: timeframe, bar-boundary, tf-D1
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-13 23:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-14 23:00:05 4200.20/4200.40; 09-14 23:05:05 4213.60/4213.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-14T22:00:00Z
- entry time: 2026-09-14T23:00:05Z
- entry: 4200.40
- stop: 4193.80
- R: 6.60
- target(s): 4213.60
- entry_across_break: True
- exit: TARGET net 2.00R

#### `GV-TF-H1-01` · `GT-HAMMER-BULL-v1.0/BASE` · H1
> H1 bar 10:00 completes 11:00. Baseline: BUY ask 4200.40, stop 4193.80, 2R 4213.60.

Tags: timeframe, bar-boundary, tf-H1
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-16 11:00:02 4200.20/4200.40; 09-16 11:05:02 4213.60/4213.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T11:00:00Z
- entry time: 2026-09-16T11:00:02Z
- entry: 4200.40
- stop: 4193.80
- R: 6.60
- target(s): 4213.60
- exit: TARGET net 2.00R

#### `GV-TF-H4-01` · `GT-HAMMER-BULL-v1.0/BASE` · H4
> H4 bar 19:00 completes at the 22:00 pause start (not 23:00); first tick after the pause 23:00:05 -> entry_across_break. Baseline: BUY ask 4200.40, stop 4193.80, 2R 4213.60.

Tags: timeframe, bar-boundary, tf-H4
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 19:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-16 23:00:05 4200.20/4200.40; 09-16 23:05:05 4213.60/4213.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T22:00:00Z
- entry time: 2026-09-16T23:00:05Z
- entry: 4200.40
- stop: 4193.80
- R: 6.60
- target(s): 4213.60
- entry_across_break: True
- exit: TARGET net 2.00R

#### `GV-TF-M1-01` · `GT-HAMMER-BULL-v1.0/BASE` · M1
> M1 bar 10:00 completes 10:01:00; first tick +2 s. Baseline: BUY ask 4200.40, stop 4193.80, 2R 4213.60.

Tags: timeframe, bar-boundary, tf-M1
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-16 10:01:02 4200.20/4200.40; 09-16 10:06:02 4213.60/4213.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-16T10:01:00Z
- entry time: 2026-09-16T10:01:02Z
- entry: 4200.40
- stop: 4193.80
- R: 6.60
- target(s): 4213.60
- exit: TARGET net 2.00R

#### `GV-TF-MN1-01` · `GT-HAMMER-BULL-v1.0/BASE` · MN1
> September's month bar completes on 30 Sep at the 22:00 pause start; the October bar opens 23:00; first tick 23:00:05. Baseline: BUY ask 4200.40, stop 4193.80, 2R 4213.60.

Tags: timeframe, bar-boundary, tf-MN1
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 08-31 23:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-30 23:00:05 4200.20/4200.40; 09-30 23:05:05 4213.60/4213.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-30T22:00:00Z
- entry time: 2026-09-30T23:00:05Z
- entry: 4200.40
- stop: 4193.80
- R: 6.60
- target(s): 4213.60
- entry_across_break: True
- exit: TARGET net 2.00R

#### `GV-TF-W1-01` · `GT-HAMMER-BULL-v1.0/BASE` · W1
> W1 bar completes at the Friday 22:00 close; the first tick is 5 s after the weekend reopening (Sunday 23:00:05): open_elapsed 5 s, entry_across_break. Wall-clock delay is ~49 h. Baseline: BUY ask 4200.40, stop 4193.80, 2R 4213.60.

Tags: timeframe, bar-boundary, tf-W1
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-06 23:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-13 23:00:05 4200.20/4200.40; 09-13 23:05:05 4213.60/4213.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-11T22:00:00Z
- entry time: 2026-09-13T23:00:05Z
- entry: 4200.40
- stop: 4193.80
- R: 6.60
- target(s): 4213.60
- entry_across_break: True
- exit: TARGET net 2.00R

#### `GV-TF-W1-02` · `GT-HAMMER-BULL-v1.0/BASE` · W1
> Weekly signal, first tick 16 minutes after the weekend reopening: 16 min of OPEN time > 15 -> SKIPPED_STALE_ENTRY.

Tags: timeframe, stale-boundary, tf-W1
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-06 23:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-13 23:16:00 4200.20/4200.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_STALE_ENTRY
- signal time: 2026-09-11T22:00:00Z

#### `GV-TF-W1-03` · `GT-HAMMER-BULL-v1.0/BASE` · W1
> Weekly signal, first tick exactly 15:00 after reopening: accepted.

Tags: timeframe, stale-boundary, tf-W1
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-06 23:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-13 23:15:00 4200.20/4200.40; 09-13 23:30:00 4213.60/4213.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- signal time: 2026-09-11T22:00:00Z
- entry: 4200.40
- exit: TARGET net 2.00R

