# GoldThinker — Candle Specification v1 (Wave 1) — DRAFT 0.2.2 FOR REVIEW

Status: **DRAFT 0.2.2, 2026-09-30. NOT approved. Nothing is to be coded from this until the owner and the
independent reviewer (ChatGPT) have approved it and golden test vectors exist.** Author: Claude.
Draft 0.2 answered ChatGPT's review of Draft 0.1. Draft 0.2.1 is a small revision answering ChatGPT's
second-pass review (six fixes, section 4). Draft 0.2.2 fixes four small points from ChatGPT's third pass. Nothing else
changed.

Wave 1 = the 22 patterns marked FULL in `MASTER_CANDLE_LIST.md`, plus two "early setup" companions
(Kicker, Abandoned Baby) added in 0.2: 24 pattern families, 32 direction-specific versions.
The other 19 patterns (10 PARTIAL, 9 NONE) and the ~30 extra TA-Lib patterns are Wave 2+.

**Standard this document must meet:** two independent programs fed the same OHLC (and tick) data must
produce exactly the same yes/no for every rule below. **[SPEC]** = a number or rule added by this spec that
no source gives. **[INTERP]** = a source was ambiguous and this spec picked a reading. Every threshold has
a constant name so a change is a version bump, never a silent edit.

---

## 1. Global definitions (GLOBALS v1.0)

### G0 Conventions, bars and indices

- Prices are USD per ounce. Store `price_distance_usd`, never "pips".
- **Source-pip conversion:** the sources quote gold "pips". Their numbers only make sense at
  `PIP_SRC_USD = 0.10` **[ASSUMPTION, unconfirmed]**. It is used ONLY inside source-normalized variants
  (`SRC-*`) to convert a source's distance to dollars (`pips x PIP_SRC_USD`). **No canonical (BASE)
  pattern identity may depend on it.** (Vantage may define one gold pip as $0.01, so the assumption can be wrong.)
  **Disabled until confirmed (0.2.1):** every variant whose rules use `PIP_SRC_USD` carries the status
  `DISABLED_PENDING_PIP_CONFIRMATION`: it is not evaluated, opens no trades and has no ledger, and the hub shows it
  as disabled. The variants are `SRC-PS` of P01, P02, P03, P04, P05, P06, P07, P09, P10, P11. BASE strategies and
  every other variant run regardless. Enabling one needs `PIP_SRC_USD` confirmed and logged as a decision.
  **How it is confirmed (0.2.2):** by deriving it from explicit worked examples in the source pages where both the
  stated pip distance and the actual XAUUSD price move are given. The broker's own pip convention (what Vantage
  calls a pip) is useful context but is NOT evidence of what the source author meant; the two may differ, and
  the source-normalized strategies must follow the author.
- Time is UTC internally. Timeframes (TF): M1, M5, M15, M30, H1, H4, D1, W1, MN1, built from the tick
  stream (bid prices, like an MT5 chart) on the Vantage broker calendar [TO CONFIRM from the demo account:
  server timezone/DST, day boundary, week start, month boundary]. No empty bars for closed intervals.
- **Bar completion (fixed in 0.2):** a bar is complete at the EARLIER of (a) the open time of the next bar
  in the broker calendar, and (b) the start of a scheduled market closure that covers the rest of the bar.
  Example: the last H1 bar before the weekend completes at the scheduled Friday close, not on Monday.
  Duration arithmetic (`open + TF length`) is never used (months, DST and broker days break it).
- `open_elapsed(a,b)` = time from a to b **excluding scheduled market closures** (feed outages while the
  market is open DO count).
- Indices and times for one detection (fixed in 0.2, extended in 0.2.1):
  - `i0` = first bar of the geometric formation; `formation_end_bar` (`f`) = last bar of the geometry;
  - **`signal_time`** (per variant) = the exact UTC timestamp at which that variant's signal became knowable:
    close-confirmed patterns -> `complete_time` of the bar whose completion confirms it; opening-tick setups
    (P14E, P19E) -> the time of that first tick; `STOP_ENTRY` variants -> the time of the tick that reaches the
    trigger;
  - `signal_bar` (`s`) = the bar identified by `signal_time`: for close-confirmed signals the bar that completes
    at `signal_time` (equals `f` for simple patterns; the breakout/confirmation bar for state-machine patterns);
    for tick-based signals the bar containing the tick;
  - `entry_eligible_time` = `signal_time` for every entry. `STOP_ENTRY` is the one case with an earlier step:
    the order is armed at `arm_time` = `complete_time(f)` and fills at the trigger tick, which is `signal_time`.
  - RAW (Layer A) uses only the BASE variant's `signal_time`/`signal_bar`; no BASE signal means no RAW record (G8).
- Candle maths for bar k: `R=H-L`, `B=|C-O|`, `UW=H-max(O,C)`, `LW=min(O,C)-L`. Bull: `C>O`. Bear: `C<O`.
  A bar with `R=0` never takes part in any pattern.
- **Data integrity:** a pattern is evaluated only if all its bars and its ATR/swing/zone look-back bars exist
  with no unexplained gap (scheduled closures are allowed and tagged `across_break`); else
  `NOT_EVALUATED_DATA_GAP`.

### G0b Event model (0.2, rewritten in 0.2.1 to be variant-aware - this feeds the hub)

Every candle passes through separate, individually logged events:

1. `SHAPE_DETECTED` - the canonical geometry matched (no prior-state requirement). Example: a hammer-shaped
   candle after an UPTREND is logged as `HAMMER_SHAPE`, `pattern_qualified=false`, `candidate=HANGING_MAN`.
   Patterns with no prior-state requirement have shape = pattern.
2. `BASE_PATTERN_FORMED` - canonical shape AND the canonical prior state hold ("the pattern exists"). **This is
   the hub's "Formed" count.** Logged whether or not anything is ever traded, and **once per detection, never
   once per variant.**
3. `VARIANT_QUALIFIED` - a variant's own static conditions hold at formation: its context and location rules
   (e.g. SRC-PS Hammer accepts `DOWN OR AT_SUPPORT`, SRC-CB needs the trend or a level), its allowed TFs, and any
   identity delta (e.g. the wider SRC-PS Tweezer tolerance). A variant may qualify **without**
   `BASE_PATTERN_FORMED` (recorded `base_formed=false`); the BASE variant qualifies exactly when the base pattern
   forms. A variant with an identity delta evaluates its own geometry at the same bar.
4. `SIGNAL` - the variant's confirmation/trigger happened and `signal_time` is set (a hammer confirmed by the
   next bar, an inside bar broken out within 3 bars, a `STOP_ENTRY` trigger reached). Simple patterns: signal =
   the completion of the formation. Session and news filters are evaluated with the session/news at
   `signal_time`, so their skips are recorded at this stage.
5. `TRADE` - the variant actually entered (or its early trigger fired).
6. Non-trade dispositions, always with a reason code: `EXPIRED_NO_CONFIRMATION`, `INVALIDATED_BEFORE_ENTRY`,
   `SKIPPED_STALE_ENTRY`, `SKIPPED_R_TOO_SMALL`, `SKIPPED_SRC_RR`, `SKIPPED_SRC_NO_TARGET`,
   `SKIPPED_TARGET_ALREADY_PASSED`, `SKIPPED_SESSION_FILTER`, `SKIPPED_NEWS`, `SKIPPED_TF_NOT_ALLOWED`,
   `NOT_EVALUATED_DATA_GAP`, `NOT_EVALUATED_WARMUP`, `DISABLED_PENDING_PIP_CONFIRMATION`.

**Hub counters (0.2.1) - two levels so nothing is double counted:**

- **Canonical counters**, stored ONCE per `pattern x side x timeframe x version`: `shapes`, `base_formed`.
- **Variant counters**, stored per `pattern x side x timeframe x variant x version`: `qualified`, `signals`,
  `trades`, each skip/expiry reason, open and closed trades, P&L.
- A variant card shows `base_formed` by looking it up in the canonical counters; `base_formed` is never summed
  across variants. Early-setup patterns (P14E, P19E) are their own pattern identities with their own canonical
  counters. Counts are never derived from trades.

### G1 ATR

`ATR = atr_pre` = simple mean of True Range over the 14 completed bars ending at bar `i0-1`
(`TR = max(H-L, |H-Cprev|, |L-Cprev|)`). Needs 15 completed bars before `i0` else `NOT_EVALUATED_WARMUP`.
The candidate pattern never influences its own ATR.

### G2 Size classes

- `LARGE(k)`: `B>=0.60*ATR` AND `R>=0.80*ATR` AND `B/R>=0.60`. **[SPEC]**
- `SMALL(k)`: `B<=0.25*ATR` AND `R<=0.60*ATR`. **[SPEC]**
- `DOJI(k)`: `B<=0.05*R`.
- `MIN_RANGE_SINGLE`: single-candle patterns also need `R>=0.50*ATR`. **[SPEC]**

### G3 Swings and trend

- Swing high at bar j: `H[j]` strictly greater than the highs of the 2 bars before and 2 bars after; swing
  low mirrors. Confirmed when bar j+2 is complete.
- `TREND(at i0-1)`: uses only swings confirmed by then, last 200 bars, own TF. Last two swing highs (SH1
  older, SH2 newer) and lows (SL1, SL2). **UP** if `SH2>=SH1+0.10*ATR` AND `SL2>=SL1+0.10*ATR`; **DOWN** if
  `SH2<=SH1-0.10*ATR` AND `SL2<=SL1-0.10*ATR`; else **RANGE**; fewer than two of each: **UNDETERMINED**.
- `TREND_HTF`: same on the higher TF (M1->M15, M5->H1, M15->H1, M30->H4, H1->H4, H4->D1, D1->W1, W1->MN1).
  Context only; never required by any rule in v1.

### G4 Support / resistance zones

**Two separate zone sets (0.2.1):** `zones_prepattern` (computed at `i0-1`, used only for the `AT_SUPPORT` /
`AT_RESISTANCE` flags and filters) and `zones_at_entry` (computed once at entry, used only for targets; see G10).
The next paragraph defines the computation for both; they differ only in the completed-bar cut-off.

At `i0-1`, over the last 200 completed bars, collect confirmed swing prices; sort ascending; cluster
greedily (a cluster starts at the lowest unassigned price `p0` and takes every price `<=p0+0.25*ATR`).
A cluster is a **zone** if it has >=2 pivots with at least one pair >=3 bars apart. Centre = median;
zone = centre +- `0.125*ATR`. `AT_SUPPORT` (bullish): distance from the pattern's lowest low to the nearest
zone (0 if inside) `<=0.10*ATR`; `AT_RESISTANCE` (bearish): same with the highest high. A zone is dead once
a completed bar closes more than `0.10*ATR` beyond its far edge. Role flips not modelled in v1. Fibonacci
and round numbers are context flags only (`ROUND_50`: extreme within `0.10*ATR` of a multiple of $50).

### G5 Gap

`gap_thr = max($0.10, 0.05*ATR)`. Bullish gap between bars a<b: `L_b >= H_a + gap_thr`; bearish:
`H_b <= L_a - gap_thr`. Gaps across a closed interval are allowed and tagged `across_break`.

### G6 Sessions and news (source variants only; always recorded)

- ASIA = 09:00-17:00 `Asia/Tokyo`; LONDON = 08:00-17:00 `Europe/London`; NY = 08:00-17:00
  `America/New_York` (DST automatic). `ASIA_ONLY` = in ASIA and in neither LONDON nor NY. The session of a
  signal is the session at its `signal_time`.
  **[SPEC]**
- `economic_events(time_utc, currency, impact, name)`. `F_NEWS_HIGH`: blocked T-30 to T+15 min around any
  high-impact USD event. `F_NEWS_MAJOR`: NFP, CPI, FOMC decision, FOMC press conference, blocked T-60 to
  T+30 min. **[SPEC]** Blocked signals are still detected and logged.

### G7 Indicators (filters and context only)

`RSI14` = Wilder RSI on closes at the completion of the last pattern bar; needs 100 bars of warm-up.

### G8 Measurement layers

**Layer A - RAW (candle prices only, no trading assumptions).** Direction `d=+1` bullish, `-1` bearish (for
Inside Bar and Outside Bar, `d` comes from the pattern's own direction rule). **RAW is generated once per
canonical BASE signal only (0.2.2).** A signal that exists only in a source variant (no BASE signal, e.g. a
source Hammer at support without the canonical downtrend) produces NO RAW record. Forward behaviour after
variant-specific signals, if ever wanted, is a separate metric `VARIANT_FORWARD_BEHAVIOUR`, never Layer A.
- Reference price `ref`: close-based signal -> open of the bar after `signal_bar`; tick-based BASE signal
  (P14E/P19E) -> the trigger tick's executable price (ask for `d=+1`, bid for `d=-1`).
- **Horizon end (0.2.2):** for `h in {1,3,5,10,20}`: close-based signal `horizon_end(h) = s + h`; tick-based
  opening signal `horizon_end(h) = s + h - 1` (the signal bar itself is bar 1). All of `ret_h`, `MFE_h` and
  `MAE_h` use the bars from the first bar after the reference up to and including `horizon_end(h)`
  (close-based: bars `s+1 .. s+h`; tick-based: bars `s .. s+h-1`).
- `ret_h = d*(close[horizon_end(h)] - ref)` (USD and ATR units); `MFE_h` = best `d*(extreme-ref)` over those bars
  (bar high for `d=+1`, low for `d=-1`); `MAE_h` = worst adverse; `dir_ok_h = ret_h>0`; with ticks also
  `mfe_before_mae_h`. A data gap in the window gives `NULL`.

**Layer B - BASELINE (identical mechanics for every pattern).**
- **Entry:** first executable tick with `time >= entry_eligible_time` (= `signal_time`). BUY at ask, SELL at bid. If
  `open_elapsed(entry_eligible_time, first_tick) > 15 minutes` -> `SKIPPED_STALE_ENTRY`. Scheduled
  closures do not count, so a weekly candle completing at the Friday close can enter at Monday's first tick
  (tagged `entry_across_break`, and any gap through the stop fills at the first price). **[SPEC]**
- **Stop:** beyond the pattern extreme: bullish `pattern_low - G_BUFFER`; bearish `pattern_high +
  G_BUFFER`; `pattern_low/high` = lowest low / highest high over all bars of the geometry (not any
  confirmation bar); `G_BUFFER = max($0.20, 0.05*ATR)`. **[SPEC]**
- **Target:** fixed `2R`, `R=|entry_fill-stop|`. No partials. No RSI/MACD/DXY/news/session/level filter.
  `SKIPPED_R_TOO_SMALL` if `R < max(4*spread_at_entry, 0.10*ATR)`. **[SPEC]**
- **Time stop:** `MAX_HOLD = 50` bars of the pattern's own TF, then close at market (`exit_reason=TIME`).
  **[SPEC]** Approved by the reviewer for v1 (2026-09-30); owner confirmation pending. Correction to 0.1: this keeps horizons comparable in bars; it does NOT keep high-TF trades short
  (50 monthly bars is over four years). W1/MN1 experiments will mature very slowly and will show
  `INSUFFICIENT_DATA` for a long time; that is accepted. (Alternatives - per-TF limits or no time stop for
  high TFs - are not used in v1.)
- **Sizing (fixed in 0.2):** `1R = 1% of REF_EQUITY`, `REF_EQUITY=$10,000` **[SPEC]**.
  `loss_per_lot = (R / tick_size) * tick_value`; `lots = risk_usd / loss_per_lot` using the broker's actual
  tick size and tick value (USD) from the account spec. The independent virtual ledger keeps the unrounded
  value. The Vantage demo mirror rounds down to the lot step and records `requested_risk` and
  `actual_demo_risk`; below the minimum lot -> `MIRROR_SKIPPED_MIN_LOT` (the virtual trade still counts).

**Layer C - SOURCE-NORMALIZED PLAN (renamed in 0.2; it is not an "exact" reproduction).** It follows a
source's confirmation, entry, stop, targets, partials and filters as closely as can be made deterministic,
and every departure is written in the variant's `source_deviation_notes` (field 26). Ids: `<ID>/SRC-PS`,
`/SRC-CB`, `/SRC-SH` (PS Pro-Scalper, CB Candlestick Trading Bible, SH Shankar notes).
- Where a source names two targets but no split, v1 uses the first target only (second recorded as OPEN).
- Where a source names a structural target but no minimum ratio, `G_MIN_REWARD_DEFAULT = 1.5R`. **[SPEC]**

### G9 Fills, ordering and costs

- Long: stop at first tick with `bid <= stop`, fill = that tick's bid; target at first tick with
  `bid >= target`, fill = target price. Short: stop at `ask >= stop`, fill = that ask; target at
  `ask <= target`, fill = target price. Gaps through a stop fill at the first tick price.
- Tick order decides stop vs target. If ticks are missing: score **STOP FIRST**, tag
  `resolution=CONSERVATIVE_STOP_FIRST`, and report a target-first sensitivity figure. Never delete.
- Result in R = `(exit-entry)*d/R` minus swap and commission converted to R (from the account spec).

### G10 Entry mechanics, targets and validity

- `NEXT_TICK`: as Layer B at `entry_eligible_time`.
- `CONFIRM_CLOSE`: the confirmation test runs on the immediately following completed bar unless the pattern
  says otherwise (max extension `G_CONFIRM_MAX=3` bars **[SPEC]**); success -> entry at the first
  executable tick after that bar completes; failure -> `EXPIRED_NO_CONFIRMATION`. "Opens with momentum"
  wording is replaced by a close-based test **[INTERP]**.
- `STOP_ENTRY(trigger)`: armed at `arm_time` (`complete_time(f)`); the fill tick is `signal_time` = `entry_eligible_time`; long fills when ask `>= trigger`, short when bid
  `<= trigger`, within the next 3 completed bars; cancelled if price first reaches the stop level
  (`INVALIDATED_BEFORE_ENTRY`); else `EXPIRED`. **[SPEC]**
- `OPEN_TRIGGER`: fires on the first executable tick of the bar after the geometry if a stated opening condition
  holds. **The condition is tested on the BID (chart) opening price `bid_open` - the same price a candle chart
  would show - never on the ask; the order then executes BUY at ask / SELL at bid (0.2.1: removes an
  ask-based bias in the bullish trigger).** **Used only by the EARLY_SETUP patterns (P14E, P19E). Every trigger counts as a trade, whether or not the
  completed pattern later forms.**
- **`T_SR(minR)` (fixed in 0.2):** target = near edge of the NEAREST live zone beyond the entry in the trade
  direction. Compute available `R` to it. If `< minR` -> `SKIPPED_SRC_RR`. No zone -> `SKIPPED_SRC_NO_TARGET`.
  The rule never steps over a nearer obstacle to reach a bigger target.
- **`T_SWING(minR)`:** same with the nearest confirmed swing pivot beyond the entry.
- **Entry snapshot (0.2.1):** targets that use zones or swings (`T_SR`, `T_SWING`, and TP2 anchors) are computed
  ONCE, immediately before the entry, using only zones/swings that were confirmed by `entry_eligible_time`
  (`zones_at_entry` = the G4 procedure over the last 200 bars completed by that time; swings confirmed by then).
  The result is stored on the trade (`target_snapshot`) and frozen: later bars never move a target. A trade
  with no valid target under the variant's rule is skipped with its reason code and never re-evaluated.
- **Target validity (new in 0.2):** every target must be strictly beyond the ACTUAL entry price in the trade
  direction. If not -> `SKIPPED_TARGET_ALREADY_PASSED` (the whole occurrence for that variant is skipped; no
  retrospective profit is invented).
- Conservative pullback entries named in sources (50% retrace etc.) are **deferred to v1.1**.

### G11 Identity, versions, overlaps, experiment size

- Ids: `GT-<PATTERN>-<BULL|BEAR>-v1.0`; variants `.../BASE`, `.../SRC-PS`, etc. Any rule or constant change
  creates a new version and a new sample; old results stay attached to the old version.
- Overlapping identities are allowed and all logged; detections completing on the same bar, same TF and
  same direction share a `cluster_id`. Results are never pooled across TFs, variants or versions.
- Size: about 32 sides x 9 TFs = 288 baseline strategies plus about 41 source-variant sides x up to 9 TFs =
  at most about 369 more: **up to about 657 strategies.** Variants disabled by `DISABLED_PENDING_PIP_CONFIRMATION`
  (G0) are inside this maximum until enabled. Survivors must clear the untouched validation
  stage before any real money.

### G12 Context recorded for every detection (never required unless a variant says so)

`trend_state`, `trend_state_htf`, `at_support`/`at_resistance` and distance to nearest zone, `rsi14`,
`atr_pre`, spread at signal, session flags, `news_flags`, `round_50`, `across_break`, weekday and hour, size
ratios of the pattern bars, `cluster_id`.

---

## 2. Test-vector requirement

After Draft 0.2.2 is reviewed, **golden test vectors** are written (drafted by Claude, checked by the reviewer): small OHLC/tick
sequences with the expected yes/no and expected entry/stop/target, so an implementation can be checked.
Worked examples below are illustrative only.

---

## 3. Wave-1 pattern specifications

Fields 1-25 are the agreed schema; field 26 is new in 0.2. "G" points to section 1. Every "FINAL ACCEPTED
RULE" reads **PROPOSED v1.0** until approved. In every pattern, `shape` = geometry only, `pattern` = shape
plus the stated prior state (G0b).

### P01 HAMMER (bullish) — `GT-HAMMER-BULL-v1.0`

1. GT-HAMMER-BULL-v1.0 (BASE, SRC-PS)  2. Hammer  3. bullish  4. 1
5. **Shape `HAMMER_SHAPE` (C1):** `R>=0.50*ATR` AND `LW>=2.0*B` AND `UW<=0.10*R` AND `min(O,C)>=L+0.65*R`.
6. **Prior state (pattern = shape + this):** `TREND(i0-1)=DOWN`. Same shape after `UP` is logged as a
   Hanging Man candidate.
7. Formation = signal = completion of C1.
8. Baseline per G8; SRC-PS fails if confirmation fails/expires.
9-11. **Baseline:** BUY, stop `L1-G_BUFFER`, 2R.
12. **SRC-PS entry:** CONFIRM_CLOSE BUY.  13. **Stop:** `L1 - 17.5*PIP_SRC_USD` (source "15-20 pips").
14. **Target:** single `2R` (source "2:1 minimum"). No partials.
15. **Confirmation:** C2 bullish AND `C2close>H1`. **[INTERP]**  16. **Expiry:** C2 only.
17. **Filters:** prior state relaxed to `DOWN OR AT_SUPPORT`.
18. Context: G12; wick and body ratios.  19. Session/news: none stated.  20. Gap: none.
21. **Aliases:** subset of Pin Bar (bull); overlaps Dragonfly when the body is tiny.
22. **Example:** `O=4200.00 H=4200.50 L=4194.00 C=4200.20`, ATR 4.0: `R=6.5>=2.0`, `B=0.20`, `LW=6.0>=0.4`,
    `UW=0.30<=0.65`, `min(O,C)=4200.00>=4194+4.225=4198.225` -> shape YES; pattern YES if trend DOWN.
23. **Sources:** master row 1; PS `/hammer-candlestick` (source 9); TV, SA, SH, CB.
24. **Open:** "upper third" vs "upper 40%" in the source (this spec: 35%); `MIN_RANGE_SINGLE` and ratios [SPEC].
25. PROPOSED v1.0 = fields 5+6+7.
26. **SRC-PS is `DISABLED_PENDING_PIP_CONFIRMATION`** (uses `PIP_SRC_USD`, G0). **Source deviation notes:** "initial bullish momentum" replaced by a close test; "15-20 pips" converted at an
    assumed $0.10/pip; "downtrend or known support" implemented with the G3/G4 definitions.

### P02 SHOOTING STAR (bearish) — `GT-SHOOTINGSTAR-BEAR-v1.0`

1. GT-SHOOTINGSTAR-BEAR-v1.0 (BASE, SRC-PS)  2. Shooting Star  3. bearish  4. 1
5. **Shape:** `R>=0.50*ATR` AND `UW>=2.0*B` AND `LW<=0.10*R` AND `max(O,C)<=H-0.65*R`.
6. **Prior state:** `TREND(i0-1)=UP` (same shape after DOWN = Inverted Hammer candidate).  7. As P01.
8-11. **Baseline:** SELL at bid; stop `H1+G_BUFFER`; 2R.
12. **SRC-PS entry:** CONFIRM_CLOSE SELL.  13. **Stop:** `H1 + 20*PIP_SRC_USD` (source "15-25 pips").
14. **Target:** `T_SWING(1.5)` (nearest confirmed swing low below entry; skip if under 1.5R). Second target
    ("rally origin") OPEN.
15. **Confirmation:** C2 bearish AND `C2close<min(O1,C1)`. **[INTERP]**  16. C2 only.
17. **Filters:** skip `ASIA_ONLY` (source: reduced size or skipped) **[INTERP]**; prior state
    `UP OR AT_RESISTANCE`.
18-20. G12; none; none.  21. Subset of Pin Bar (bear); overlaps Gravestone.
22. Red body preferred by source, not required.
23. Master row 4; PS `/shooting-star` (source 10); TV, SH, CB.  24. Open: second target; size reduction.
25. PROPOSED v1.0.
26. **SRC-PS is `DISABLED_PENDING_PIP_CONFIRMATION`** (uses `PIP_SRC_USD`, G0). **Deviation notes:** open-based confirmation replaced by a close test; "reduced size" replaced by skip;
    rally-origin target dropped; pips converted at $0.10.

### P03 PIN BAR (bullish, bearish) — `GT-PINBAR-BULL-v1.0`, `GT-PINBAR-BEAR-v1.0`

1. IDs as given; variants BASE, SRC-PS, SRC-CB.  2. Pin Bar  3. both  4. 1
5. **Shape = pattern:** `R>=0.50*ATR`, `B<=0.33*R`, dominant wick `>=0.66*R`, opposite wick `<=0.10*R`.
   Bullish: dominant wick is the lower one and `C>=L+0.75*R`. Bearish: upper one and `C<=H-0.75*R`.
6. **Prior state:** none (context recorded).  7. Formation = signal = C1 completion.
8-11. **Baseline:** bullish BUY, stop `L1-G_BUFFER`; bearish SELL, stop `H1+G_BUFFER`; 2R.
12. **Entry:** SRC-PS and SRC-CB both NEXT_TICK.
13. **Stop:** SRC-PS: wick tip `+-12.5*PIP_SRC_USD` (source 10-15 pips). SRC-CB: wick tip `+-G_BUFFER`
    (source "beyond the tail", no number) **[INTERP]**.
14. **Target:** SRC-PS `T_SWING(2.0)`; second target (measured move) OPEN. SRC-CB `T_SR(2.0)`.
15-16. None; none.
17. **Filters:** SRC-PS requires `AT_SUPPORT`/`AT_RESISTANCE` and skips `ASIA_ONLY`. SRC-CB requires the pin
    to be WITH the trend (bull needs `TREND=UP`, bear `TREND=DOWN`) AND at a level; TF in {H1,H4,D1}.
18. Context: wick ratios, zone distance.  19. Session/news: as in 17.  20. Gap: none.
21. Aliases: bullish contains Hammer/Dragonfly cases; bearish contains Shooting Star/Gravestone.
22. `B=0` allowed; one candle may be Hammer, Dragonfly and Pin Bar at once (three detections, one cluster).
23. Master row 5; PS `/pin-bar` (source 12); CB (source 15).
24. Open: CB says 5-minute pin bars "lose money"; this spec still runs them (owner chose all TFs).
25. PROPOSED v1.0.
26. **SRC-PS is `DISABLED_PENDING_PIP_CONFIRMATION`** (uses `PIP_SRC_USD`, G0). **Deviation notes:** PS conservative 50%-retrace entry deferred; "body inside prior candle" dropped from
    identity; CB "8/21 MA, Fibonacci" location not used (S/R zones only); second targets dropped.

### P04 DRAGONFLY DOJI (bullish) — `GT-DRAGONFLY-BULL-v1.0`

1. GT-DRAGONFLY-BULL-v1.0 (BASE, SRC-PS)  2. Dragonfly Doji  3. bullish  4. 1
5. **Shape:** `DOJI` AND `UW<=0.05*R` AND `LW>=0.80*R` (implied by the first two) AND `R>=0.50*ATR`.
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. Formation = signal = C1 completion.
8-11. **Baseline:** BUY, stop `L1-G_BUFFER`, 2R.
12. **SRC-PS entry:** CONFIRM_CLOSE BUY.  13. **Stop:** `L1 - 10*PIP_SRC_USD` (source 5-15 pips).
14. **Target:** `T_SR(1.5)`.
15. **Confirmation:** C2 bullish AND `C2close>max(O1,C1)`; fails if C2 is bearish or a doji.  16. C2 only.
17. **Filters:** `AT_SUPPORT`; skip `ASIA_ONLY`; `F_NEWS_MAJOR`.
18-20. G12; as 17; none.  21. Subset of Bull Pin Bar; overlaps Hammer.
22. Exact `O=C=H` not required (too strict).  23. Master row 8; PS `/dragonfly-doji`; SH, CB.
24. Open: 5% tolerances [SPEC].  25. PROPOSED v1.0.
26. **SRC-PS is `DISABLED_PENDING_PIP_CONFIRMATION`** (uses `PIP_SRC_USD`, G0). **Deviation notes:** pips at $0.10; "buy limit at the level" alternative dropped; H4/D1 emphasis recorded only.

### P05 GRAVESTONE DOJI (bearish) — `GT-GRAVESTONE-BEAR-v1.0`

1. GT-GRAVESTONE-BEAR-v1.0 (BASE, SRC-PS)  2. Gravestone Doji  3. bearish  4. 1
5. **Shape:** `DOJI` AND `LW<=0.05*R` AND `UW>=0.80*R` AND `R>=0.50*ATR`.
6. **Prior state:** `TREND(i0-1)=UP`.  7. As P04.
8-11. **Baseline:** SELL, stop `H1+G_BUFFER`, 2R.
12. **SRC-PS entry:** CONFIRM_CLOSE SELL.  13. **Stop:** `H1 + 10*PIP_SRC_USD`.  14. **Target:** `T_SR(1.5)`.
15. **Confirmation:** C2 closes below `min(O1,C1)`; fails if it closes above.  16. C2 only.
17. **Filters:** `AT_RESISTANCE`. No session/TF rule in the source.  18-20. G12; none; none.
21. Subset of Bear Pin Bar; overlaps Shooting Star.  22. Differs from Shooting Star only by near-zero body.
23. Master row 9; PS `/gravestone-doji`; SH, CB.  24. Open: tolerances [SPEC].  25. PROPOSED v1.0.
26. **SRC-PS is `DISABLED_PENDING_PIP_CONFIRMATION`** (uses `PIP_SRC_USD`, G0). **Deviation notes:** pips at $0.10; sell-limit alternative dropped.

### P06 BULLISH ENGULFING — `GT-ENGULF-BULL-v1.0`

1. GT-ENGULF-BULL-v1.0 (BASE, SRC-PS, SRC-CB, SRC-SH)  2. Bullish Engulfing  3. bullish  4. 2
5. **Shape:** C1 bear, C2 bull, `O2<=C1`, `C2>=O1`, `B2>B1`, `B1>0.05*R1`. Flags: `B2>=2*B1`; wicks also
   engulfed (`L2<=L1`, `H2>=H1`).
6. **Prior state:** `TREND(i0-1)=DOWN`. The same shape in an UP trend is logged as
   `candidate=ENGULF_CONTINUATION` (continuation reading deferred).  7. Formation = signal = C2 completion.
8-11. **Baseline:** BUY, stop `min(L1,L2)-G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK.  13. **Stop:** `min(L1,L2) - 20*PIP_SRC_USD`.
14. **Target:** `T_SR(1.5)`; second target (3R) OPEN.
15-16. None; none.
17. **Filters:** SRC-PS prior state `DOWN OR AT_SUPPORT`. SRC-CB: `TREND=DOWN` AND `AT_SUPPORT`, TF in
    {H1,H4,D1}, NEXT_TICK, stop `min(L1,L2)-G_BUFFER`, target `T_SR(2.0)`. SRC-SH: shape tightened to wicks
    engulfed AND `RSI14(C2)<30`; NEXT_TICK; stop/target = BASELINE (source gives none).
18. Context: size ratio, wick flag, RSI14.  19. Session/news: SRC-PS none.  20. Gap: none.
21. Aliases: Outside Bar when wicks are engulfed too. Piercing Line is disjoint (`C2<O1` there).
22. **Example:** C1 `O=4210 H=4211 L=4203 C=4204`; C2 `O=4203.5 H=4212.5 L=4203 C=4212`: `O2<=4204`,
    `C2>=4210`, `B2=8.5>B1=6` -> YES.
23. Master row 13; PS `/bullish-engulfing` (source 7); SH (source 4); CB (source 15); TV, SA.
24. **Open:** SH's own text asks for both "enter at the close" and "third candle confirms".
25. PROPOSED v1.0.
26. **SRC-PS is `DISABLED_PENDING_PIP_CONFIRMATION`** (uses `PIP_SRC_USD`, G0). **Deviation notes:** PS "or at support" alternative implemented as `AT_SUPPORT`; PS second target dropped;
    SH third-candle confirmation not used (entry-at-close reading); CB moving-average/Fibonacci locations not
    used; continuation reading deferred.

### P07 BEARISH ENGULFING — `GT-ENGULF-BEAR-v1.0`

1. GT-ENGULF-BEAR-v1.0 (BASE, SRC-PS, SRC-CB)  2. Bearish Engulfing  3. bearish  4. 2
5. **Shape:** C1 bull, C2 bear, `O2>=C1`, `C2<=O1`, `B2>B1`, `B1>0.05*R1`.
6. **Prior state:** `TREND(i0-1)=UP` (else `ENGULF_CONTINUATION` candidate).  7. As P06.
8-11. **Baseline:** SELL, stop `max(H1,H2)+G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK.  13. **Stop:** `max(H1,H2) + 20*PIP_SRC_USD`.
14. **Target:** `T_SR(1.5)`; second target (~3R) OPEN.  15-16. None; none.
17. **Filters:** SRC-PS prior state `UP OR AT_RESISTANCE`; skip `ASIA_ONLY`. SRC-CB mirrors P06.
18-20. G12; as 17; none.  21. Outside Bar when wicks are engulfed too.  22. As P06.
23. Master row 14; PS `/bearish-engulfing` (source 8); CB.  24. Open: DXY unavailable.  25. PROPOSED v1.0.
26. **SRC-PS is `DISABLED_PENDING_PIP_CONFIRMATION`** (uses `PIP_SRC_USD`, G0). **Deviation notes:** DXY correlation and RSI-divergence filters not enforced (no feed; recorded as
    unavailable); Fibonacci-extension location recorded only; pips at $0.10.

### P08 OUTSIDE BAR (bullish, bearish) — `GT-OUTSIDE-BULL-v1.0`, `GT-OUTSIDE-BEAR-v1.0`

1. IDs as given (BASE, SRC-PS)  2. Outside Bar  3. both  4. 2
5. **Shape = pattern:** `H2>H1` AND `L2<L1` (strict). Direction: bullish if `C2>O2`, bearish if `C2<O2`;
   `C2=O2` gives no signal. Flag: `R2>=1.5*ATR`.
6. **Prior state:** none.  7. Formation = signal = C2 completion.
8-11. **Baseline:** bullish BUY, stop `L2-G_BUFFER`; bearish SELL, stop `H2+G_BUFFER`; 2R.
12. **SRC-PS entry:** NEXT_TICK.  13. **Stop:** `L2-G_BUFFER` / `H2+G_BUFFER` (source gives no buffer) **[INTERP]**.
14. **Target:** `T_SR(1.5)`.  15-16. None; none.
17. **Filters:** SRC-PS requires `R2>=1.5*ATR`; skips bars containing a high-impact USD event and bars
    overlapping the daily rollover pause.
18-20. G12; as 17; none.  21. Alias: Engulfing (Outside Bar is stricter).
22. The size filter is a flag in BASE, a requirement in SRC-PS.
23. Master row 15; PS `/outside-bar`.  24. Open: news delay replaced by skip.  25. PROPOSED v1.0.
26. **Deviation notes:** "wait 1-2 candles after a news spike" replaced by skipping the occurrence.

### P09 INSIDE BAR BREAKOUT (bullish, bearish) — `GT-INSIDE-BULL-v1.0`, `GT-INSIDE-BEAR-v1.0`

1. IDs as given (BASE, SRC-PS, SRC-CB)  2. Inside Bar (breakout)  3. both  4. 2 + breakout bar
5. **Shape / formation:** mother C1, inside C2 with `H2<H1` AND `L2>L1` (strict). This is `BASE_PATTERN_FORMED`
   (the "inside bar exists"). Compression `R2/R1` recorded.
   **Signal bar `Cb`:** first bar among the next three (`b=3,4,5`) whose CLOSE is outside the mother range:
   `Cb>H1` bullish, `Cb<L1` bearish. None within 3 bars -> `EXPIRED_NO_CONFIRMATION`.
6. **Prior state:** none.  7. `formation_end_bar`=C2; `signal_bar`=`Cb`; `signal_time` = completion of `Cb`.
8-11. **Baseline:** entry NEXT_TICK after `Cb`; stop = opposite side of the mother `L1-G_BUFFER` /
    `H1+G_BUFFER` (`pattern_low/high` = mother range); 2R.
12. **SRC-PS entry:** NEXT_TICK after `Cb` (source says both "buy stop above" and "wait for a close outside";
    the close reading is adopted) **[INTERP]**.
13. **Stop:** opposite mother side `+-3.5*PIP_SRC_USD` (source 2-5 pips).  14. **Target:** `T_SR(1.5)`.
15. Confirmation: the breakout close.  16. Expiry: 3 bars after C2.
17. **Filters:** SRC-PS: TF in {H1,H4,D1,W1,MN1}; skip `ASIA_ONLY`; `F_NEWS_MAJOR`. SRC-CB: breakout WITH the
    trend (bull needs `TREND=UP`, bear `TREND=DOWN`), mother bar at a level, TF in {H4,D1}; stop opposite
    mother side `+-G_BUFFER`; target `T_SR(2.0)`.
18-20. Context: nested-bar count, compression; as 17; none.  21. Aliases: none.
22. A bar that pokes outside the mother range but closes inside is not a breakout; it stays armed until
    expiry (and may be a Sweep & Reclaim, P22).
23. Master row 16; PS `/inside-bar`; CB; TV, SH.  24. Open: order-based vs close-based entry.  25. PROPOSED v1.0.
26. **SRC-PS is `DISABLED_PENDING_PIP_CONFIRMATION`** (uses `PIP_SRC_USD`, G0). **Deviation notes:** buy-stop entry replaced by close-based entry; source pips at $0.10; news window uses
    `F_NEWS_MAJOR`.

### P10 TWEEZER TOP (bearish) — `GT-TWEEZERTOP-BEAR-v1.0`

1. GT-TWEEZERTOP-BEAR-v1.0 (BASE, SRC-PS)  2. Tweezer Top  3. bearish  4. 2
5. **Shape:** C1 bull, C2 bear, `|H1-H2|<=tol`, **`tol=max(3*tick_size, 0.05*ATR)`** (canonical, no pip
   dependency). Flag: `C2close<=(O1+C1)/2`.
6. **Prior state:** `TREND(i0-1)=UP`.  7. Formation = C2 completion; signal = the trigger break for SRC-PS,
   C2 completion for BASE.
8-11. **Baseline:** SELL, stop `max(H1,H2)+G_BUFFER`, 2R.
12. **SRC-PS entry:** `STOP_ENTRY(trigger=L2)` SELL **[INTERP]** (source also allows "open of the third
    candle").
13. **Stop:** `max(H1,H2) + 3*PIP_SRC_USD`.  14. **Target:** `T_SR(1.5)` (source: nearest support).
15. Confirmation: the trigger break.  16. Expiry: 3 bars after C2.
17. **Filters:** `AT_RESISTANCE`; skip `ASIA_ONLY`. **SRC-PS identity delta:** `tol_src=max(3*PIP_SRC_USD,
    0.05*ATR)`.
18-20. G12; as 17; none.  21. Bearish Engulfing / Dark Cloud can share a bar.
22. The canonical tolerance grows with ATR.  23. Master row 19; PS `/tweezer-top`; CB, SH.
24. Open: 3-bar trigger expiry [SPEC].  25. PROPOSED v1.0.
26. **SRC-PS is `DISABLED_PENDING_PIP_CONFIRMATION`** (uses `PIP_SRC_USD`, G0). **Deviation notes:** the source's wider pip tolerance applies only inside SRC-PS; entry reading is a trigger
    break; "small pullback" entry deferred.

### P11 TWEEZER BOTTOM (bullish) — `GT-TWEEZERBOTTOM-BULL-v1.0`

1. GT-TWEEZERBOTTOM-BULL-v1.0 (BASE, SRC-PS)  2. Tweezer Bottom  3. bullish  4. 2
5. **Shape:** C1 bear, C2 bull, `|L1-L2|<=tol` (`tol` as P10). Flags: C1 closes in its lowest 25%, C2 in its
   highest 25%.
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. As P10.
8-11. **Baseline:** BUY, stop `min(L1,L2)-G_BUFFER`, 2R.
12. **SRC-PS entry:** `STOP_ENTRY(trigger=H2)` BUY.  13. **Stop:** `min(L1,L2) - 3*PIP_SRC_USD`.
14. **Target:** `T_SWING(1.5)`.  15. Trigger break.  16. 3 bars.
17. **Filters:** `AT_SUPPORT`. Volume divergence (source) not usable - recorded only. SRC-PS identity delta as P10.
18-20. G12; none; none.  21. Bullish Engulfing can share a bar.  22. As P10.
23. Master row 20; PS `/tweezer-bottom`.  24. As P10.  25. PROPOSED v1.0.
26. **SRC-PS is `DISABLED_PENDING_PIP_CONFIRMATION`** (uses `PIP_SRC_USD`, G0). **Deviation notes:** as P10; volume confirmation dropped.

### P12 PIERCING LINE (bullish) — `GT-PIERCING-BULL-v1.0`

1. GT-PIERCING-BULL-v1.0 (BASE, SRC-PS)  2. Piercing Line  3. bullish  4. 2
5. **Shape:** C1 bear AND `LARGE(C1)`; C2 bull; `O2<C1`; `C2>(O1+C1)/2`; **`C2<O1`** (strict, so it cannot
   also be a Bullish Engulfing, which needs `C2>=O1`). Flags: `O2<=L1-gap_thr` (`gap_flag`); penetration
   tier (50-60 / 75 / 90+ %).
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. Formation = signal = C2 completion.
8-11. **Baseline:** BUY, stop `min(L1,L2)-G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK.  13. **Stop:** `L2 - G_BUFFER` (source: below C2's low, not C1's).
14. **Target:** `T_SR(2.0)` (source: minimum 1:2 before entry); second target OPEN.  15-16. None; none.
17. **Filters:** `AT_SUPPORT`; skip signals wholly inside `ASIA_ONLY`.
18-20. Context: penetration %, `gap_flag`; as 17; gap not required (a strict classical-gap variant would be a
    separately named version).
21. Disjoint from Bullish Engulfing.  22. Source says a gap down strengthens - recorded, not required.
23. Master row 21; PS `/piercing-line`; SA, SH.  24. Open: "opens below C1 close" is barely a gap on gold.
25. PROPOSED v1.0.
26. **Deviation notes:** second target dropped; the "at level" location requirement uses G4 zones only.

### P13 DARK CLOUD COVER (bearish) — `GT-DARKCLOUD-BEAR-v1.0`

1. GT-DARKCLOUD-BEAR-v1.0 (BASE, SRC-PS)  2. Dark Cloud Cover  3. bearish  4. 2
5. **Shape:** C1 bull AND `LARGE(C1)`; C2 bear; `O2>C1`; `C2<(O1+C1)/2`; **`C2>O1`** (strict; a Bearish
   Engulfing needs `C2<=O1`).
6. **Prior state:** `TREND(i0-1)=UP`.  7. Formation = signal = C2 completion.
8-11. **Baseline:** SELL, stop `max(H1,H2)+G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK.  13. **Stop:** `H2 + G_BUFFER`.  14. **Target:** `T_SR(1.5)`; source's "scale
    out half, trail the rest" OPEN (trail not defined).
15-16. None; none.  17. **Filters:** `AT_RESISTANCE`.  18-20. G12; none; source says "gap required" but
    defines it as `O2>C1`, which is the rule.
21. Disjoint from Bearish Engulfing.  22. Mirror of P12.
23. Master row 22; PS `/dark-cloud-cover`; SH.  24. Open: trailing.  25. PROPOSED v1.0.
26. **Deviation notes:** scale-out/trailing dropped; single target.

### P14 KICKER, completed pattern (bullish, bearish) — `GT-KICKER-BULL-v1.0`, `GT-KICKER-BEAR-v1.0`

1. IDs as given (BASE, SRC-PS-COMPLETED)  2. Kicker (completed)  3. both  4. 2
5. **Shape (fixed in 0.2):** bullish: C1 bear `LARGE`; C2 bull `LARGE`; **`O2>=O1`** (C2 opens at or above
   C1's open, so C2's body does not overlap C1's body); `C2>=H2-0.10*R2`. Bearish: C1 bull `LARGE`; C2 bear
   `LARGE`; `O2<=O1`; `C2<=L2+0.10*R2`. Flags: `bull_gap_flag = O2>=O1+gap_thr` (bullish
   Kicker), `bear_gap_flag = O2<=O1-gap_thr` (bearish Kicker).
6. **Prior state:** bullish `TREND=DOWN`; bearish `TREND=UP`.  7. Formation = signal = C2 completion.
8-11. **Baseline:** entry NEXT_TICK; stop `min(L1,L2)-G_BUFFER` / `max(H1,H2)+G_BUFFER`; 2R.
12. **SRC-PS-COMPLETED entry:** NEXT_TICK after C2 completes.  13. **Stop:** beyond C1's far extreme:
    `L1-G_BUFFER` (bull) / `H1+G_BUFFER` (bear).  14. **Target:** `T_SWING(1.5)`.
15-16. None; none.  17. **Filters:** TF in {H1,H4,D1,W1,MN1} (source: M15 and below "almost never worth
    trading").
18-20. G12; as 17; the identity forces a gap-like open away from C1's close through `LARGE(C1)` and
    `O2>=O1`.
21. Aliases: none.  22. Rare on gold; the system reports `UNKNOWN`, not a win rate, until enough trades.
23. Master row 23; PS `/kicker-pattern`.  24. Open: the source's "approximately equal open" tolerance was
    removed because it contradicted "bodies do not overlap".  25. PROPOSED v1.0.
26. **Deviation notes:** the source's entry "at the open of the second candle" is NOT used here (needs
    unknown C2 information); it lives in the separate EARLY_SETUP pattern P14E.

### P14E KICKER EARLY SETUP (bullish, bearish) — `GT-KICKEREARLY-BULL-v1.0`, `GT-KICKEREARLY-BEAR-v1.0`

New in 0.2. A different pattern with its own counts: it is what the source's entry actually is.

1. IDs as given (BASE-EARLY, SRC-PS-EARLY)  2. Kicker early setup  3. both  4. 1 + opening tick
5. **`SHAPE_DETECTED` = C1 geometry:** C1 bear `LARGE` (bullish) / C1 bull `LARGE` (bearish), logged when C1
   completes. **`BASE_PATTERN_FORMED` = the trigger (0.2.1):** the prior state holds (`TREND(i0-1)=DOWN` bullish,
   `UP` bearish) AND the BID opening price of the next bar satisfies: bullish `bid_open >= O1`; bearish
   `bid_open <= O1`. Then the order executes BUY at the ask / SELL at the bid of that first tick (G10
   `OPEN_TRIGGER`). Nothing about C2's later body or close is required or checked.
6. **Prior state:** as P14.  7. Formation = signal = that first tick (`signal_time` = its timestamp).
8. **Every trigger is a trade.** Trades are counted whether or not P14 later completes. The completed-pattern
   outcome is stored as a label on the trade (`completed_kicker_yes/no`) and is **never** used to include or
   exclude trades.
9-11. **Baseline (BASE-EARLY):** entry at the trigger tick; stop `L1-G_BUFFER` (bull) / `H1+G_BUFFER` (bear);
    2R.
12-14. **SRC-PS-EARLY:** entry at the trigger tick; stop as P14 field 13; target `T_SWING(1.5)`.
15-16. None; none.  17. TF in {H1,H4,D1,W1,MN1}.  18-20. G12; none; none.
21. Overlaps P14 (the completed version is a later, narrower event).
22. **Purpose:** avoids selection bias - we do not enter early and then keep only the trades where the pattern
    completed.
23. As P14.  24. Open: none.  25. PROPOSED v1.0.
26. **Deviation notes:** none beyond pips at $0.10.

### P15 MORNING STAR (bullish) — `GT-MORNINGSTAR-BULL-v1.0`

1. GT-MORNINGSTAR-BULL-v1.0 (BASE, SRC-PS)  2. Morning Star  3. bullish  4. 3
5. **Shape:** C1 bear `LARGE`; C2 `SMALL` AND `B2<=0.40*B1` AND `O2<=C1+0.10*ATR`; C3 bull `LARGE` AND
   `C3>(O1+C1)/2`.
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. Formation = signal = C3 completion.
8-11. **Baseline:** BUY, stop `min(L1,L2,L3)-G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK after C3.  13. **Stop:** `min(L1,L2)-G_BUFFER` (source offers tight-below-C2 or
    wide-below-C1; the lower of the two lows is used) **[INTERP]**.
14. **Targets:** TP1 = `H1`, close **60%**; TP2 = nearest confirmed swing high above TP1 for the remaining
    40% (none -> the remainder runs to stop/time stop). Stop not moved. **Both targets must be beyond the
    actual entry; if TP1 is not, `SKIPPED_TARGET_ALREADY_PASSED`.**
15-16. None; none.  17. Filters: none required (RSI<30, support/Fibonacci recorded only).
18-20. G12 plus `star_gap` (`max(O2,C2)<C1`); none; gap not required.
21. Abandoned Baby is the true-gap subset.  22. The star-opening rule mirrors Evening Star (from SH/PS-evening
    wording) [SPEC].
23. Master row 25; PS `/morning-star`; TV, SH, SA, CB, GPFX.  24. Open: star position rule.
25. PROPOSED v1.0.
26. **Deviation notes:** stop choice reading; TP2 anchor; RSI/support not enforced.

### P16 EVENING STAR (bearish) — `GT-EVENINGSTAR-BEAR-v1.0`

1. GT-EVENINGSTAR-BEAR-v1.0 (BASE, SRC-PS)  2. Evening Star  3. bearish  4. 3
5. **Shape:** C1 bull `LARGE`; C2 `SMALL` AND `B2<=0.40*B1` AND `O2>=C1-0.10*ATR`; C3 bear `LARGE` AND
   `C3<(O1+C1)/2`.
6. **Prior state:** `TREND(i0-1)=UP`.  7. Formation = signal = C3 completion.
8-11. **Baseline:** SELL, stop `max(H1,H2,H3)+G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK after C3.  13. **Stop:** `H2 + G_BUFFER`.
14. **Targets:** TP1 = `L1`, close **60%**; TP2 = near edge of the nearest live zone below TP1. Both must be
    beyond the actual entry, else `SKIPPED_TARGET_ALREADY_PASSED`.
15-16. None; none.  17. Filters: none required.  18-20. G12; none; gap not required.
21. Abandoned Baby subset.  22. Source H1 example: 30-80 pips (at $0.10 = $3-8).
23. Master row 27; PS `/evening-star` (source 6); TV, SH, CB, GPFX.  24. Open: none beyond [SPEC].
25. PROPOSED v1.0.
26. **Deviation notes:** stop reading; TP2 as nearest zone (source: "next major support").

### P17 THREE WHITE SOLDIERS (bullish) — `GT-3WHITESOLDIERS-BULL-v1.0`

1. GT-3WHITESOLDIERS-BULL-v1.0 (BASE, SRC-PS)  2. Three White Soldiers  3. bullish  4. 3
5. **Shape = pattern:** for k=1..3: bull, `B_k>=0.40*ATR`, `B_k>=0.60*R_k`, `UW_k<=0.25*R_k`; for k=2,3:
   `O_{k-1}<=O_k<=C_{k-1}` and `C_k>C_{k-1}`; `max(B1,B2,B3)<=2.0*min(B1,B2,B3)`. All thresholds [SPEC].
6. **Prior state:** none (sources call it a continuation, classical texts a reversal; both recorded via
   `trend_state`).  7. Formation = C3 completion; signal = C3 (BASE) or the trigger break (SRC-PS).
8-11. **Baseline:** BUY, stop `min(L1..L3)-G_BUFFER`, 2R.
12. **SRC-PS entry:** `STOP_ENTRY(trigger=H3)` BUY **[INTERP]**.  13. **Stop:** `L3-G_BUFFER` **[INTERP]**.
14. **Target:** measured move `H3 + (max(H1..H3)-min(L1..L3))` (must be beyond entry); 50% scale-out OPEN.
15-16. Trigger break; 3 bars.  17. Filters: none enforced (RSI 75-80, "resistance within 50 pips",
    bull/bear-market context recorded).
18-20. G12; none; none.  21. Marubozu-like bodies possible.
22. Runs of 15-20 prior candles are "weakest" per the source - recorded as `bars_since_swing_low`.
23. Master row 29; PS `/three-white-soldiers`; SH.  24. Open: similarity ratio; continuation vs reversal.
25. PROPOSED v1.0.
26. **Deviation notes:** breakout-entry stop and target readings; pullback entry deferred.

### P18 THREE BLACK CROWS (bearish) — `GT-3BLACKCROWS-BEAR-v1.0`

1. GT-3BLACKCROWS-BEAR-v1.0 (BASE, SRC-PS)  2. Three Black Crows  3. bearish  4. 3
5. **Shape = pattern:** mirror of P17: bear, `B_k>=0.40*ATR`, `B_k>=0.60*R_k`, `LW_k<=0.25*R_k`; k=2,3:
   `C_{k-1}<=O_k<=O_{k-1}` and `C_k<C_{k-1}`; similar-size clause.
6. **Prior state:** none.  7. As P17.
8-11. **Baseline:** SELL, stop `max(H1..H3)+G_BUFFER`, 2R.
12. **SRC-PS entry:** `STOP_ENTRY(trigger=L3)` SELL (breakdown; retracement entry deferred) **[INTERP]**.
13. **Stop:** `H3+G_BUFFER` **[INTERP]**.  14. **Target:** `L3 - pattern height` (must be beyond entry); then next
    support OPEN.
15-16. Trigger break; 3 bars.  17. Filters: none enforced (weekly trend, DXY, RSI<25 recorded).
18-20. G12; none; none.  21-22. As P17.  23. Master row 30; PS `/three-black-crows`; SH.
24. Open: as P17.  25. PROPOSED v1.0.  26. **Deviation notes:** as P17.

### P19 ABANDONED BABY, completed pattern (bullish, bearish) — `GT-ABABY-BULL-v1.0`, `GT-ABABY-BEAR-v1.0`

1. IDs as given (BASE, SRC-PS-COMPLETED)  2. Abandoned Baby (completed)  3. both  4. 3
5. **Shape:** bullish: C1 bear `LARGE`; C2 `DOJI` with `H2<=L1-gap_thr`; C3 bull `LARGE` with
   `L3>=H2+gap_thr`. Bearish: C1 bull `LARGE`; C2 `DOJI` with `L2>=H1+gap_thr`; C3 bear `LARGE` with
   `H3<=L2-gap_thr`. True gaps only.
6. **Prior state:** bullish `TREND=DOWN`; bearish `TREND=UP`.  7. Formation = signal = C3 completion.
8-11. **Baseline:** NEXT_TICK after C3; stop = pattern extreme over all three bars (`min(L1..L3)-G_BUFFER`
    bullish / `max(H1..H3)+G_BUFFER` bearish); 2R.
12. **SRC-PS-COMPLETED entry:** NEXT_TICK after C3 completes.  13. **Stop:** `L2-G_BUFFER` (bull) /
    `H2+G_BUFFER` (bear) (source: below the doji's low).  14. **Target:** `T_SWING(1.5)`.
15-16. None; none.  17. Filters: none enforced (RSI, DXY, Fibonacci recorded).
18-20. G12; none; gaps required (that is the identity).  21. Subset of Morning/Evening Star.
22. Source: about 2-4 signals a year on D1 gold; the system reports `UNKNOWN`, not a win rate.
23. Master row 31; PS `/abandoned-baby`.  24. Open: none.  25. PROPOSED v1.0.
26. **Deviation notes:** the source's entry "on the open of the third candle" is in P19E, not here.

### P19E ABANDONED BABY EARLY SETUP (bullish, bearish) — `GT-ABABYEARLY-BULL-v1.0`, `GT-ABABYEARLY-BEAR-v1.0`

New in 0.2, same reasoning as P14E.

1. IDs as given (BASE-EARLY, SRC-PS-EARLY)  2. Abandoned Baby early setup  3. both  4. 2 + opening tick
5. **`SHAPE_DETECTED`** = C1 and C2 geometry: bullish C1 bear `LARGE`, C2 `DOJI` with `H2<=L1-gap_thr`;
   bearish C1 bull `LARGE`, C2 `DOJI` with `L2>=H1+gap_thr`. **`BASE_PATTERN_FORMED` = the trigger (0.2.1):** the
   prior state holds (`TREND(i0-1)=DOWN` bullish / `UP` bearish) AND the BID opening price of C3 satisfies:
   bullish `bid_open >= H2+gap_thr`; bearish `bid_open <= L2-gap_thr`. Then BUY at the ask / SELL at the bid of that
   first tick. C3's size, close and colour are not checked.
6. **Prior state:** as P19.  7. Formation = signal = that first tick (`signal_time` = its timestamp).
8. **Every trigger is a trade**, counted whether or not P19 later completes; `completed_abandoned_baby`
   is stored as a label and never used to include/exclude.
9-11. **Baseline (BASE-EARLY):** entry at the trigger tick; stop `L2-G_BUFFER` / `H2+G_BUFFER`; 2R.
12-14. **SRC-PS-EARLY:** entry at the trigger tick; stop `L2-G_BUFFER` (bull) / `H2+G_BUFFER` (bear); target
    `T_SWING(1.5)`.
15-16. None; none.  17-20. As P19.  21. Overlaps P19.  22. As P14E.  23. As P19.
24. Open: none.  25. PROPOSED v1.0.  26. **Deviation notes:** none beyond pips at $0.10.

### P20 RISING THREE METHODS (bullish) — `GT-RISING3-BULL-v1.0`

1. GT-RISING3-BULL-v1.0 (BASE, SRC-PS)  2. Rising Three Methods  3. bullish  4. 5
5. **Shape:** C1 bull `LARGE`; k=2,3,4: bear AND `H_k<=H1` AND `L_k>=L1` AND `B_k<=0.5*B1`; C5 bull `LARGE`
   AND `C5>C1`. Flag: all C2-C4 closes within C1's body (`O1<=C_k<=C1`).
6. **Prior state:** `TREND(i0-1)=UP`.  7. Formation = signal = C5 completion.
8-11. **Baseline:** BUY, stop `min(L1..L5)-G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK after C5.  13. **Stop:** `min(L2,L3,L4)-G_BUFFER`.
14. **Target:** TP1 = `P + 1.272*(H1-L1)`, `P=min(L2..L4)` **[INTERP]** (source names the 1.272 extension but
    not its anchor); TP2 (1.618) OPEN; must be beyond entry and give `>=2R` else `SKIPPED_SRC_RR`.
15-16. None; none.  17. Filters: none enforced (volume decline unusable).  18-20. G12; none; none.
21. None.
22. **Source re-check (2026-09-30):** the Rising page states the middle candles' highs must not exceed C1's
    high and lows must not break C1's low, and "none should close outside the range of the first candle". So
    full high-low containment (this spec) is the source's rule.
23. Master row 38; PS `/rising-three-methods`; INV.  24. Open: Fibonacci anchor.  25. PROPOSED v1.0.
26. **Deviation notes:** Fibonacci anchor invented; TP2 dropped.

### P21 FALLING THREE METHODS (bearish) — `GT-FALLING3-BEAR-v1.0`

1. GT-FALLING3-BEAR-v1.0 (BASE, SRC-PS)  2. Falling Three Methods  3. bearish  4. 5
5. **Shape:** C1 bear `LARGE`; k=2,3,4: bull AND `H_k<=H1` AND `L_k>=L1` AND `B_k<=0.5*B1`; C5 bear `LARGE`
   AND `C5<C1`. Flag: C2-C4 closes within C1's body (`C1<=C_k<=O1`).
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. Formation = signal = C5 completion.
8-11. **Baseline:** SELL, stop `max(H1..H5)+G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK after C5.  13. **Stop:** `max(H2,H3,H4)+G_BUFFER`.
14. **Target:** TP1 = `P - 1.272*(H1-L1)`, `P=max(H2..H4)` **[INTERP]**; must be beyond entry and `>=2R`.
15-16. None; none.
17. **Filters:** **SRC-PS additionally requires the body-close flag** (the Falling page says "none should
    close above the first candle's open, and none should drop below the first candle's close", read here as
    closes); the Rising page does not state the mirror rule.
18-20. G12; none; none.  21. None.
22. **Source re-check:** Falling page also requires full high-low containment ("must remain within the
    high-to-low range of the first large bearish candle"), which is the canonical shape rule.
23. Master row 39; PS `/falling-three-methods`.  24. Open: Rising/Falling asymmetry on the close rule.
25. PROPOSED v1.0.  26. **Deviation notes:** as P20; close-rule reading.

### P22 INSIDE BAR SAME-BAR SWEEP & RECLAIM (bullish, bearish) — `GT-IBSR-BULL-v1.0`, `GT-IBSR-BEAR-v1.0`

Renamed in 0.2 (was "Inside Bar False Breakout"): it is one specific, objective subtype. A multi-bar false
break (bar 3 closes outside, bar 4 reverses back inside) is not covered and is listed for Wave 1b if the
source supports it.

1. IDs as given (BASE, SRC-CB)  2. Inside Bar Same-Bar Sweep & Reclaim  3. both  4. inside bar + 1..3
5. **Shape:** mother C1, inside C2 (`H2<H1`, `L2>L1`). Then bar `Ck`, `k in {3,4,5}`, is the FIRST bar after C2
   that pierces the mother range (every bar between C2 and `Ck` has `H<=H1` and `L>=L1`). `Ck` pierces exactly
   ONE side by at least 1 tick and closes back inside `[L1,H1]`. **Bearish** (sell): `H_k>=H1+tick` and closes
   inside. **Bullish** (buy): `L_k<=L1-tick` and closes inside. Both sides pierced ->
   `NO_SIGNAL_AMBIGUOUS_BOTH_SIDES`.
6. **Prior state:** none in the shape.  7. `formation_end_bar`=`signal_bar`=`Ck`.
8-11. **Baseline:** NEXT_TICK after `Ck`; stop beyond the sweep extreme: bearish `H_k+G_BUFFER`, bullish
    `L_k-G_BUFFER`; 2R.
12. **SRC-CB entry:** NEXT_TICK after `Ck`.  13. **Stop:** as baseline.  14. **Target:** `T_SR(2.0)`.
15-16. None; expiry as in 5.
17. **Filters:** bearish needs `TREND=UP` OR `AT_RESISTANCE`; bullish needs `TREND=DOWN` OR `AT_SUPPORT`;
    TF in {H1,H4,D1}.
18-20. G12; none; none.  21. Excludes P09 (which fires on a CLOSE outside the range).
22. **Example (bearish):** mother `H=4210 L=4200`; inside `H=4207 L=4203`; next bar `H=4210.5 L=4204 C=4208`:
    pierces `4210+tick`, closes inside -> sell signal.
23. Master row 41; CB (source 15, pages 148-157).
24. **Open:** whether the book's "false breakout" includes the multi-bar case (its wording: price "breaks out
    from the inside bar pattern and then quickly reverses to close within the range of the mother bar").
25. PROPOSED v1.0.
26. **Deviation notes:** narrowed to the same-bar case; "quickly reverses" not extended to later bars.

---

## 4. Review log and open items

### Draft 0.1 -> 0.2 changes (ChatGPT review findings and self-review)

| Finding | Status | Fix |
|---|---|---|
| A. Bar completion used `open + TF length` | Fixed | G0: complete at next broker bar or scheduled closure start |
| B. 15-min stale rule rejects W1/MN1 | Fixed | G8: counts `open_elapsed` only |
| C. `p` breaks for state-machine patterns | Fixed | G0: `i0`, `formation_end_bar`, `signal_bar`, `known_at_time`, `entry_eligible_time`; RAW uses bar after `signal_bar` |
| 2. Formation vs signal vs trade | Fixed | G0b event model; hub counters |
| 14. Shape vs pattern | Fixed | `SHAPE_DETECTED` and `PATTERN_FORMED`; candidates logged (Hanging Man, continuation engulfing) |
| 3. Kicker/Baby early-entry selection bias | Fixed | Completed patterns P14/P19 plus EARLY_SETUP patterns P14E/P19E; all triggers count |
| 4. Tweezer tolerance used source pip | Fixed | Canonical `max(3*tick_size, 0.05*ATR)`; source pips only in SRC-PS |
| 5. Piercing/Dark Cloud equal-value overlap | Fixed | `C2<O1` / `C2>O1` |
| 6. Kicker tolerance contradicted "no overlap" | Fixed | `O2>=O1` / `O2<=O1`; tolerance removed |
| 7. Layer C called "exact" | Fixed | Renamed SOURCE-NORMALIZED; field 26 `source_deviation_notes` |
| 8. `T_SR/T_SWING` stepped over nearer obstacles | Fixed | Nearest-only, then skip if under minR |
| 9. `MAX_HOLD` rationale wrong | Corrected; decision open | Rationale fixed; alternatives listed below |
| 10. Sizing used `contract_size` | Fixed | tick_size/tick_value/lot step; mirror records requested vs actual risk |
| 11. Target could be behind the entry | Fixed | Target validity rule, `SKIPPED_TARGET_ALREADY_PASSED` |
| 12. Rising/Falling containment | Checked against the source | Full high-low containment confirmed on both pages; Falling adds a close rule (see P21) |
| 13. False Breakout only one subtype | Fixed | Renamed to Same-Bar Sweep & Reclaim; multi-bar version deferred |
| Self: garbled text in P12/P06/P19 fields | Fixed | Cleaned |
| Hub decisions missing from the log | Already logged | D-022 to D-024 were added after ChatGPT's copy was made |

### Draft 0.2 -> 0.2.1 changes (ChatGPT second-pass review)

| # | Finding | Fix |
|---|---|---|
| 1 | Event model ignored that variants can qualify from the shape by their own context rules | G0b: SHAPE_DETECTED -> BASE_PATTERN_FORMED -> VARIANT_QUALIFIED -> SIGNAL -> TRADE |
| 2 | No exact signal timestamp | G0: `signal_time`; `signal_bar`, `entry_eligible_time`, `arm_time` derive from it |
| 3 | Early Kicker/Baby trigger tested the ask (bullish) - biased | G10, P14E, P19E: tests on BID chart open (`bid_open`), executes at ask/bid |
| 4 | Formed count could be multiplied by variants | G0b: canonical counters once per pattern x side x TF x version; variant counters separate |
| 5 | Targets could drift with later zones/swings | G10 entry snapshot frozen at `entry_eligible_time`; G4 `zones_prepattern` vs `zones_at_entry` |
| 6 | Pip assumption unconfirmed | G0: variants using `PIP_SRC_USD` are `DISABLED_PENDING_PIP_CONFIRMATION`; BASE runs regardless |
| - | `MAX_HOLD` | Kept at 50 bars; reviewer-approved, owner confirmation pending |

### Draft 0.2.1 -> 0.2.2 changes (ChatGPT third-pass review)

| # | Finding | Fix |
|---|---|---|
| 1 | RAW claimed variant-independence but a source-only variant signal has no BASE `signal_time` | G8: RAW once per canonical BASE signal only; source-only signals get none; `VARIANT_FORWARD_BEHAVIOUR` reserved as a separate future metric |
| 2 | Tick-based RAW horizon: text said `close[s+h-1]`, formula said `close[s+h]` | G8: explicit `horizon_end(h)`: `s+h` close-based, `s+h-1` tick-based; all metrics use it (must be in the golden tests) |
| 3 | Bearish Kicker gap flag not written | P14: `bull_gap_flag` and `bear_gap_flag` |
| 4 | Pip confirmation wording could adopt the broker's pip instead of the author's | G0: `PIP_SRC_USD` derived from the sources' worked examples; broker convention is context only |

### Still open for the reviewer / owner

1. **`MAX_HOLD` = 50 bars:** approved by the reviewer; owner to confirm (W1/MN1 samples will be very slow).
2. **Rising/Falling asymmetry:** does the Rising page really lack the close rule the Falling page states?
   (Read from the fetched text; worth a manual look at the page.)
3. **Constants invented by this spec [SPEC]** and **readings [INTERP]** - see the tags; every one needs approval.
4. **Not enforced in v1:** DXY, volume, RSI/MACD divergence, Fibonacci-location requirements, weekly-trend
   checks, trailing stops, second targets where the split is not given.
5. **Deferred to v1.1:** conservative pullback entries; continuation reading of engulfing; strict-gap variants
   of Piercing/Dark Cloud; role-flipped support/resistance; multi-bar inside-bar false break.
6. **`PIP_SRC_USD=0.10`** to be confirmed from the sources' own worked examples (G0); until then the affected SRC-PS variants stay disabled.
7. **Multiple testing:** up to about 657 strategies; the untouched validation stage is mandatory. The exact
   validation pass/fail rule (day-block bootstrap, multiple-testing control) is to be written before validation
   starts.
8. **Portfolio Simulation rules** (sizing, exposure cap) are undefined; until they are, the hub's top figure is
   "Total Experimental P&L", not a balance (see `DECISIONS.md`).

## 5. Change log

- 0.1 (2026-09-30): first full draft.
- 0.2 (2026-09-30): applies the review above; adds P14E and P19E; renames P22; adds the event model, field 26 and
  the nearest-only target rule.
- 0.2.1 (2026-09-30): applies the six second-pass fixes (section 4); `MAX_HOLD=50` recorded as reviewer-approved.
- 0.2.2 (2026-09-30): applies four third-pass fixes (RAW once per BASE signal, explicit `horizon_end(h)`, bearish
  Kicker gap flag, pip confirmed from source examples).
