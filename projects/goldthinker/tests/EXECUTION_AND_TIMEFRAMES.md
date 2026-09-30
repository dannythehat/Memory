# Execution, timeframe and bar-boundary vectors

Spec Draft 0.3 · vector pack GV-0.2. Uses the Hammer BASE strategy as a carrier so the ONLY thing changing between vectors is the mechanic under test.

#### `GV-EX-B01` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> MAX_HOLD (A-13). Entry tick 10:15:02 -> the 10:15 candle is bar 0 (not counted). The next 50 EXISTING M15 bars are 10:30 ... 21:45 (46 bars), then the 22:00-23:00 pause creates no bars, then 23:00, 23:15, 23:30, 23:45: bar 50 completes at 00:00. The tick at 23:59:59 does not exit; the first tick at 00:00:00 closes at the BID 4203.20: +2.80/6.60 = 14/33 R.

Tags: max-hold, time-stop
Context: atr=4 · trend=DOWN · account=swap_long=0.00, swap_short=0.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-16 10:15:02 4200.20/4200.40; 09-16 23:59:59 4202.00/4202.20; 09-17 00:00:00 4203.20/4203.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- time_stop_at: 2026-09-17T00:00:00Z
- exit: TIME net 14/33 (≈0.4242)R (gross 14/33 (≈0.4242)R)

#### `GV-EX-B01b` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> Same rule when bar 50 completes exactly at a scheduled closure: entry bar starts 09:15 (signal candle 09:00), so bar 50 is the 21:45 candle completing at 22:00 = the pause start. The exit is the first tick after reopening (23:00:03, bid 4202.60): +2.20/6.60 = 1/3 R, tagged exit_across_break.

Tags: max-hold, time-stop, closure
Context: atr=4 · trend=DOWN · account=swap_long=0.00, swap_short=0.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 09:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-16 09:15:02 4200.20/4200.40; 09-16 12:00:00 4201.00/4201.20; 09-16 23:00:03 4202.60/4202.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- time_stop_at: 2026-09-16T22:00:00Z
- exit: TIME net 1/3 (≈0.3333)R

#### `GV-EX-B01bm` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · M15
*Mirror of `GV-EX-B01b` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Same rule when bar 50 completes exactly at a scheduled closure: entry bar starts 09:15 (signal candle 09:00), so bar 50 is the 21:45 candle completing at 22:00 = the pause start. The exit is the first tick after reopening (23:00:03, bid 4202.60): +2.20/6.60 = 1/3 R, tagged exit_across_break.

Tags: max-hold, time-stop, closure
Context: atr=4 · trend=UP · account=swap_long=0.00, swap_short=0.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 09:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |

Ticks (bid/ask): 09-16 09:15:02 4199.60/4199.80; 09-16 12:00:00 4198.80/4199.00; 09-16 23:00:03 4197.20/4197.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- time_stop_at: 2026-09-16T22:00:00Z
- exit: TIME net 1/3 (≈0.3333)R

#### `GV-EX-B01m` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · M15
*Mirror of `GV-EX-B01` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> MAX_HOLD (A-13). Entry tick 10:15:02 -> the 10:15 candle is bar 0 (not counted). The next 50 EXISTING M15 bars are 10:30 ... 21:45 (46 bars), then the 22:00-23:00 pause creates no bars, then 23:00, 23:15, 23:30, 23:45: bar 50 completes at 00:00. The tick at 23:59:59 does not exit; the first tick at 00:00:00 closes at the BID 4203.20: +2.80/6.60 = 14/33 R.

Tags: max-hold, time-stop
Context: atr=4 · trend=UP · account=swap_long=0.00, swap_short=0.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |

Ticks (bid/ask): 09-16 10:15:02 4199.60/4199.80; 09-16 23:59:59 4197.80/4198.00; 09-17 00:00:00 4196.60/4196.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- time_stop_at: 2026-09-17T00:00:00Z
- exit: TIME net 14/33 (≈0.4242)R (gross 14/33 (≈0.4242)R)

#### `GV-EX-B02` · `GT-HAMMER-BULL-v1.0/BASE` · H1
> Swap (A-14, test fixture swap_long = -5.00 per lot per night, rollover 22:00 UTC, triple on Wednesday). H1 long entered Tue 10:00:02, exit Thu 10:00 (the 50-bar time stop would fall on Thu 15:00), crosses the Tue 22:00 rollover (x1) and the Wed 22:00 rollover (x3): weight 4. lots 5/33 -> swap $-5 x 4 x 5/33 = -100/33 -> -1/33 R. Net = 2 - 1/33 = 65/33.

Tags: swap
Context: atr=4 · trend=DOWN · account=swap_long=-5.00, swap_short=2.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-15 09:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-15 10:00:02 4200.20/4200.40; 09-17 10:00:00 4213.60/4213.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- exit: TARGET net 65/33 (≈1.9697)R (gross 2.00R) (swap -1/33 (≈-0.0303)R)

#### `GV-EX-B02b` · `GT-HAMMER-BULL-v1.0/BASE` · H1
> Same trade with NO swap specification in the account: two rollovers were crossed, so the trade is recorded but its net result is PENDING_COST_SPEC (excluded from survival statistics until backfilled).

Tags: swap, pending-cost-spec
Context: atr=4 · trend=DOWN · account=swap_long=None, swap_short=None

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-15 09:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-15 10:00:02 4200.20/4200.40; 09-17 10:00:00 4213.60/4213.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- exit: TARGET (gross 2.00R)

#### `GV-EX-B02c` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> A trade that crosses NO rollover needs no swap specification, so it is not pending even when the account has none.

Tags: swap, no-rollover
Context: atr=4 · trend=DOWN · account=swap_long=None, swap_short=None

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-16 10:15:02 4200.20/4200.40; 09-16 10:30:00 4213.60/4213.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- exit: TARGET net 2.00R

#### `GV-EX-B02d` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · H1
> Short with swap_short = +2.00 (a credit): the same two rollovers (weight 4). lots = 100/640 = 5/32; swap = +2 x 4 x 5/32 = +5/4 USD = +1/80 R; net = 2 + 1/80 = 161/80.

Tags: swap, credit
Context: atr=4 · trend=UP · account=swap_long=-5.00, swap_short=2.00

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-15 09:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |

Ticks (bid/ask): 09-15 10:00:02 4199.80/4200.00; 09-17 10:00:00 4186.80/4187.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4199.80
- stop: 4206.20
- R: 6.40
- target(s): 4187.00
- exit: TARGET net 161/80 (≈2.0125)R (gross 2.00R) (swap 1/80 (≈0.0125)R)

#### `GV-EX-B03` · `GT-HAMMER-BULL-v1.0/BASE` · H1
> Weekend gap through the stop: the Friday H1 hammer has stop 4193.80 but the first tick after reopening is 4189.50/4189.70. A BUY at the ask 4189.70 is already below the stop -> SKIPPED_ENTRY_AT_OR_BEYOND_STOP (ruling A-25). No R is formed.

Tags: entry-beyond-stop, weekend-gap
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 21:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-20 23:00:05 4189.50/4189.70

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_ENTRY_AT_OR_BEYOND_STOP
- entry: 4189.70
- stop: 4193.80

#### `GV-EX-B03b` · `GT-HAMMER-BULL-v1.0/BASE` · H1
> Ask exactly equal to the stop (4193.80): at-or-beyond -> skipped.

Tags: entry-beyond-stop, weekend-gap
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 21:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-20 23:00:05 4193.60/4193.80

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_ENTRY_AT_OR_BEYOND_STOP
- entry: 4193.80
- stop: 4193.80

#### `GV-EX-B03bm` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · H1
*Mirror of `GV-EX-B03b` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Ask exactly equal to the stop (4193.80): at-or-beyond -> skipped.

Tags: entry-beyond-stop, weekend-gap
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 21:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |

Ticks (bid/ask): 09-20 23:00:05 4206.20/4206.40

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_ENTRY_AT_OR_BEYOND_STOP
- entry: 4206.20
- stop: 4206.20

#### `GV-EX-B03c` · `GT-HAMMER-BULL-v1.0/BASE` · H1
> Ask one tick above the stop: a valid entry with R = 0.01. The BASELINE guard then rejects it: SKIPPED_R_TOO_SMALL (R < max(4 x spread, 0.10 x ATR)).

Tags: entry-beyond-stop, weekend-gap
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 21:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |

Ticks (bid/ask): 09-20 23:00:05 4193.61/4193.81

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_R_TOO_SMALL
- R: 0.01

#### `GV-EX-B03cm` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · H1
*Mirror of `GV-EX-B03c` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Ask one tick above the stop: a valid entry with R = 0.01. The BASELINE guard then rejects it: SKIPPED_R_TOO_SMALL (R < max(4 x spread, 0.10 x ATR)).

Tags: entry-beyond-stop, weekend-gap
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 21:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |

Ticks (bid/ask): 09-20 23:00:05 4206.19/4206.39

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_R_TOO_SMALL
- R: 0.01

#### `GV-EX-B03m` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · H1
*Mirror of `GV-EX-B03` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Weekend gap through the stop: the Friday H1 hammer has stop 4193.80 but the first tick after reopening is 4189.50/4189.70. A BUY at the ask 4189.70 is already below the stop -> SKIPPED_ENTRY_AT_OR_BEYOND_STOP (ruling A-25). No R is formed.

Tags: entry-beyond-stop, weekend-gap
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-18 21:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |

Ticks (bid/ask): 09-20 23:00:05 4210.30/4210.50

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL
- disposition: SKIPPED_ENTRY_AT_OR_BEYOND_STOP
- entry: 4210.30
- stop: 4206.20

#### `GV-EX-B04` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · M15
> Bars-only fallback for a SHORT (A-26): the BID high is 4206.10 (below the 4206.20 stop) but the stored ASK high is 4206.30, which is what a short stop trades on -> stopped at 4206.20, -1.00R. The ask bar is stored, never synthesised from bid + a spread.

Tags: bars-only, ask-bars
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |

Bars after entry (no ticks): 4199.60/4206.10/4195.00/4199.60

Ticks (bid/ask): 09-16 10:15:02 4199.60/4199.80
*No ticks after entry: resolve from the OHLC bar only.*

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4199.60
- stop: 4206.20
- R: 6.60
- target(s): 4186.40
- exit: STOP net -1.00R [BARS]

#### `GV-EX-B04b` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · M15
> A short whose only bar data is BID OHLC cannot be resolved from bars: NEEDS_ASK_BARS (backfill from ticks).

Tags: bars-only, ask-bars
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |

Bars after entry (no ticks): 4199.60/4206.10/4195.00/4199.60

Ticks (bid/ask): 09-16 10:15:02 4199.60/4199.80
*No ticks after entry: resolve from the OHLC bar only.*

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- exit: NEEDS_ASK_BARS [NEEDS_ASK_BARS]

#### `GV-EX-B04c` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · M15
> The ASK bar proves both the stop (ask high 4206.30 >= 4206.20) and the target (ask low 4186.20 <= 4186.40) were reachable: STOP FIRST, target-first sensitivity +2.00R.

Tags: bars-only, ask-bars, missing-tick-stop-first
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |

Bars after entry (no ticks): 4199.60/4206.10/4186.00/4199.60

Ticks (bid/ask): 09-16 10:15:02 4199.60/4199.80
*No ticks after entry: resolve from the OHLC bar only.*

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4199.60
- stop: 4206.20
- R: 6.60
- target(s): 4186.40
- exit: STOP net -1.00R [CONSERVATIVE_STOP_FIRST] [target-first sensitivity 2.00R]

#### `GV-EX-B05` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · M15
> Ruling A-11: the R_TOO_SMALL guard is BASELINE ONLY. The source-normalized Outside Bar fills at 4199.81, one tick above its stop (R 0.01, far below 4 x spread): it is still traded (the enormous size, 100 lots, exposes how tight the source plan is; universal validity checks still apply).

Tags: r-too-small, baseline-only
Context: atr=4 · trend=DOWN · zones_entry=[4224.00-4225.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4199.61/4199.81

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4199.81
- stop: 4199.80
- R: 0.01
- target(s): 4224.00
- lots: 100

#### `GV-EX-B05b` · `GT-OUTSIDE-BULL-v1.0/SRC-PS` · M15
> Spread 3.10: R 12.30 < 4 x spread 12.40, but the source variant is not screened by the baseline guard -> trade taken (its own costs will show the damage).

Tags: r-too-small, baseline-only
Context: atr=4 · trend=DOWN · zones_entry=[4262.00-4263.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4208.00 | 4202.00 | 4206.00 |
| 2 | 09-16 10:15 | 4204.00 | 4210.00 | 4200.00 | 4209.00 |

Ticks (bid/ask): 09-16 10:30:02 4209.00/4212.10

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4212.10
- stop: 4199.80
- R: 12.30
- target(s): 4262.00

#### `GV-EX-B05bm` · `GT-OUTSIDE-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-EX-B05b` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Spread 3.10: R 12.30 < 4 x spread 12.40, but the source variant is not screened by the baseline guard -> trade taken (its own costs will show the damage).

Tags: r-too-small, baseline-only
Context: atr=4 · trend=UP · zones_entry=[4137.00-4138.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |

Ticks (bid/ask): 09-16 10:30:02 4187.90/4191.00

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4187.90
- stop: 4200.20
- R: 12.30
- target(s): 4138.00

#### `GV-EX-B05m` · `GT-OUTSIDE-BEAR-v1.0/SRC-PS` · M15
*Mirror of `GV-EX-B05` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Ruling A-11: the R_TOO_SMALL guard is BASELINE ONLY. The source-normalized Outside Bar fills at 4199.81, one tick above its stop (R 0.01, far below 4 x spread): it is still traded (the enormous size, 100 lots, exposes how tight the source plan is; universal validity checks still apply).

Tags: r-too-small, baseline-only
Context: atr=4 · trend=UP · zones_entry=[4175.00-4176.00]

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4198.00 | 4192.00 | 4194.00 |
| 2 | 09-16 10:15 | 4196.00 | 4200.00 | 4190.00 | 4191.00 |

Ticks (bid/ask): 09-16 10:30:02 4200.19/4200.39

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- variant: VARIANT_QUALIFIED, SIGNAL, TRADE
- entry: 4200.19
- stop: 4200.20
- R: 0.01
- target(s): 4176.00
- lots: 100

#### `GV-EX-B06` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> RAW MAE convention (A-27): MFE and MAE are NON-NEGATIVE magnitudes. Bars after the signal have lows 0.30 below the reference open 4200.20 -> MAE = 0.30 (not -0.30).

Tags: raw, mae-sign
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

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4200.20 | h1: ret=1.80, mfe=2.80, mae=0.30 | h3: ret=1.80, mfe=2.80, mae=0.30 | h5: ret=1.80, mfe=2.80, mae=0.30 | h10: NULL | h20: NULL

#### `GV-EX-B06b` · `GT-HAMMER-BULL-v1.0/BASE` · M15
> Price never trades below the reference: MAE = 0.00 (clamped, never negative).

Tags: raw, mae-sign
Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4200.50 | 4194.00 | 4200.20 |
| 2 | 09-16 10:15 | 4200.20 | 4203.00 | 4200.20 | 4202.00 |
| 3 | 09-16 10:30 | 4200.20 | 4203.00 | 4200.20 | 4202.00 |
| 4 | 09-16 10:45 | 4200.20 | 4203.00 | 4200.20 | 4202.00 |
| 5 | 09-16 11:00 | 4200.20 | 4203.00 | 4200.20 | 4202.00 |
| 6 | 09-16 11:15 | 4200.20 | 4203.00 | 4200.20 | 4202.00 |
| 7 | 09-16 11:30 | 4200.20 | 4203.00 | 4200.20 | 4202.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — h1: ret=1.80, mfe=2.80, mae=0.00 | h5: mae=0.00

#### `GV-EX-B06bm` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · M15
*Mirror of `GV-EX-B06b` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> Price never trades below the reference: MAE = 0.00 (clamped, never negative).

Tags: raw, mae-sign
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |
| 2 | 09-16 10:15 | 4199.80 | 4199.80 | 4197.00 | 4198.00 |
| 3 | 09-16 10:30 | 4199.80 | 4199.80 | 4197.00 | 4198.00 |
| 4 | 09-16 10:45 | 4199.80 | 4199.80 | 4197.00 | 4198.00 |
| 5 | 09-16 11:00 | 4199.80 | 4199.80 | 4197.00 | 4198.00 |
| 6 | 09-16 11:15 | 4199.80 | 4199.80 | 4197.00 | 4198.00 |
| 7 | 09-16 11:30 | 4199.80 | 4199.80 | 4197.00 | 4198.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — h1: ret=1.80, mfe=2.80, mae=0.00 | h5: mae=0.00

#### `GV-EX-B06m` · `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` · M15
*Mirror of `GV-EX-B06` (prices reflected around 8400; buy/sell, highs/lows and trend swapped).*
> RAW MAE convention (A-27): MFE and MAE are NON-NEGATIVE magnitudes. Bars after the signal have lows 0.30 below the reference open 4200.20 -> MAE = 0.30 (not -0.30).

Tags: raw, mae-sign
Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.00 | 4206.00 | 4199.50 | 4199.80 |
| 2 | 09-16 10:15 | 4199.80 | 4200.10 | 4197.00 | 4198.00 |
| 3 | 09-16 10:30 | 4199.80 | 4200.10 | 4197.00 | 4198.00 |
| 4 | 09-16 10:45 | 4199.80 | 4200.10 | 4197.00 | 4198.00 |
| 5 | 09-16 11:00 | 4199.80 | 4200.10 | 4197.00 | 4198.00 |
| 6 | 09-16 11:15 | 4199.80 | 4200.10 | 4197.00 | 4198.00 |
| 7 | 09-16 11:30 | 4199.80 | 4200.10 | 4197.00 | 4198.00 |

- canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED
- RAW — ref=4199.80 | h1: ret=1.80, mfe=2.80, mae=0.30 | h3: ret=1.80, mfe=2.80, mae=0.30 | h5: ret=1.80, mfe=2.80, mae=0.30 | h10: NULL | h20: NULL

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

