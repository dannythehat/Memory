# GoldThinker — Candle Specification v1 (Wave 1) — DRAFT 0.3.2

Status: **DRAFT 0.3.2, 2026-09-30.** Research specification; nothing is coded from it yet. Author: Claude; reviewer:
ChatGPT. Draft 0.3 applies the reviewer rulings on the 29 findings of the golden-vector pack GV-0.1 plus one new
finding (A-30, executable-price quantisation); the ruling table is in section 4. Under the working rule of
2026-09-30 (`DECISIONS.md` D-035) Claude and ChatGPT settle candlestick, mathematical, execution and testing rules
between them; the owner's original requirements stay marked OWNER and anything involving real money is the owner's.
Golden vectors GV-0.2 (`tests/`) are the acceptance test for this draft.

Wave 1 = the 22 patterns marked FULL in `MASTER_CANDLE_LIST.md`, plus two "early setup" companions
(Kicker, Abandoned Baby) added in 0.2: 24 pattern families, 32 direction-specific versions.
The other 19 patterns (10 PARTIAL, 9 NONE) and the ~30 extra TA-Lib patterns are Wave 2+.

**Standard this document must meet:** two independent programs fed the same OHLC (and tick) data must
produce exactly the same yes/no for every rule below. **[SPEC]** = a number or rule added by this spec that
no source gives. **[INTERP]** = a source was ambiguous and this spec picked a reading. Every threshold has
a constant name so a change is a version bump, never a silent edit.

---

## 1. Global definitions (GLOBALS v1.1)

### G-N Notation (new in 0.3, ruling A-02)

- `K1 ... K5` are the CANDLES of a formation (K1 the first). `O1, H1, L1, C1` are the numeric open/high/low/close of
  K1, and so on. In prose "K2 is bullish" speaks about the candle; in a formula `O2<=C1` means the open of K2 is at
  most the CLOSE of K1. `Kb` is the breakout candle of P09 and `Cb` its close.
- Numbers: prices are held as integer broker ticks (`price / tick_size`). ATR, ratios, zone widths and every
  threshold comparison use exact decimal/rational arithmetic and are NEVER rounded before a comparison (ruling
  A-22). Only executable order prices are quantised (G13).

### G0 Conventions, bars and indices

- Prices are USD per ounce. Store `price_distance_usd`, never "pips".
- **Source-pip conversion (confirmed in 0.3.2, D-040):** the sources quote gold "pips". `PIP_SRC_USD = 0.10`
  **[CONFIRMED FROM THE SOURCES]**: Pro-Scalper's own gold pip page defines "1 pip = $0.10 price move" (0.01 lot =
  $0.10 per pip, 1.0 lot = $10.00 per pip), and the same site's Bullish Engulfing page pairs "a $6-12 per ounce swing
  in a single hour" on H1 with "50-150 pips" of follow-through (= $5-15 at $0.10); the explicit definition is the
  strongest evidence. It is the sources' convention, not Vantage's. It is used ONLY inside
  source-normalized variants (`SRC-*`) to convert a source's distance to dollars (`pips x PIP_SRC_USD`). **No canonical
  (BASE) pattern identity may depend on it.** The ten `SRC-PS` variants that use it (P01, P02, P03, P04, P05, P06,
  P07, P09, P10, P11) are **ENABLED** (the state `DISABLED_PENDING_PIP_CONFIRMATION` is retired). No source page gives a
  worked entry/stop/target price example with pips, so the check is the definition plus the internal consistency
  above; the value stays a named constant and any change is a new rule version (D-011).
- Time is UTC internally. Timeframes (TF): M1, M5, M15, M30, H1, H4, D1, W1, MN1, built from the tick
  stream on the Vantage broker calendar [TO CONFIRM from the demo account: server timezone/DST, day boundary, week
  start, month boundary, daily rollover/pause window]. No empty bars for closed intervals.
- **Two price series per bar (0.3, ruling A-26).** Candle DETECTION uses the BID bars (the chart). Every bar also
  stores ASK OHLC built from the same ticks, used for short-side stop/target checks when tick order is missing (G9).
  An ask is never synthesised from a bid bar plus a spread.
- **Bar completion:** a bar is complete at the EARLIER of (a) the open time of the next bar in the broker calendar,
  and (b) the start of a scheduled market closure that covers the rest of the bar. Duration arithmetic
  (`open + TF length`) is never used. Bars are half-open: a tick at exactly a bar's completion instant belongs to the
  NEXT bar.
- `open_elapsed(a,b)` = time from a to b **excluding scheduled market closures** (feed outages while the market is
  open DO count).
- Indices and times for one detection:
  - `i0` = first bar of the geometric formation; `formation_end_bar` (`f`) = last bar of the geometry;
  - **`signal_time`** (per variant) = the exact UTC timestamp at which that variant's signal became knowable:
    close-confirmed patterns -> `complete_time` of the confirming bar; opening-tick setups (P14E, P19E) -> the time
    of that first tick; `STOP_ENTRY` variants -> the time of the tick that reaches the trigger;
  - `signal_bar` (`s`) = the bar identified by `signal_time`: for close-confirmed signals the bar that completes at
    `signal_time`; for tick-based signals the bar containing the tick;
  - `entry_eligible_time` = `signal_time` for every entry. `STOP_ENTRY` arms at `arm_time` = `complete_time(f)` and
    fills at the trigger tick, which is `signal_time`.
  - RAW (Layer A) uses only the BASE variant's `signal_time`/`signal_bar`; no BASE signal means no RAW record (G8).
- Candle maths for candle k: `R=H-L`, `B=|C-O|`, `UW=H-max(O,C)`, `LW=min(O,C)-L`. Bull: `C>O`. Bear: `C<O`.
  A candle with `R=0` never takes part in any pattern.
- **Data integrity:** a pattern is evaluated only if all its candles and its ATR/swing/zone look-back bars exist with
  no unexplained gap (scheduled closures are allowed and tagged `across_break`); else `NOT_EVALUATED_DATA_GAP`.

### G0b Event model (rewritten in 0.3 - this feeds the hub)

Every candle passes through separate, individually logged events:

1. `SHAPE_DETECTED` - the canonical geometry matched (no prior-state requirement). It carries `side` = BULL, BEAR or
   **NEUTRAL** where the geometry itself has no direction (P08 outside geometry, P09 inside geometry; ruling A-08:
   a K2 doji still logs the geometry but forms no directional pattern). Example: a hammer-shaped candle after an
   UPTREND logs the shape with `pattern_qualified=false`, `candidate=HANGING_MAN`.
2. `BASE_PATTERN_FORMED` - canonical shape AND the canonical prior state (and, for P08, the K2 direction) hold. **This
   is the hub's "Formed" count.** Logged whether or not anything is ever traded, once per detection, never once per
   variant. **P09's formation is `side=NEUTRAL` at K2 (an `INSIDE_BAR` exists) and stays counted even if it later
   expires** (ruling A-09).
3. `VARIANT_QUALIFIED` - every static gate of the variant holds at formation. Every shape evaluated against a variant
   keeps ALL failed gates in `qualification_failures[]` (ruling A-12): `PRIOR_STATE`, `DIRECTION`, `TF_NOT_ALLOWED`,
   `WITH_TREND`, `AT_LEVEL`, `IDENTITY_DELTA`, `RSI`, `SIZE_FILTER`, `WICKS_ENGULFED`, `BODY_CLOSE_FLAG`, `TRIGGER_NOT_MET`. If the list is
   not empty there is no `VARIANT_QUALIFIED` and the disposition is `NOT_QUALIFIED`. A variant may qualify WITHOUT
   `BASE_PATTERN_FORMED` (`base_formed=false`); the BASE variant qualifies exactly when the base pattern forms
   (its failure code is `PRIOR_STATE`, or `DIRECTION` for P08).
4. `SIGNAL` - the variant's confirmation/trigger happened and `signal_time` is set. Simple patterns: signal = the
   completion of the formation. Session and news filters use the session/news at `signal_time`, so their skips are
   recorded here. Waiting states are dispositions, not failures: `PENDING_CONFIRMATION`, `PENDING_BREAKOUT`.
5. `TRADE` - the variant actually entered (or its early trigger fired).
6. Non-trade dispositions, always with a reason code: `NOT_QUALIFIED`, `EXPIRED_NO_CONFIRMATION`, `EXPIRED`,
   `INVALIDATED_BEFORE_ENTRY`, `NOT_TRIGGERED_OTHER_SIDE` (P09: the breakout closed on the other side),
   `NO_SIGNAL_AMBIGUOUS_BOTH_SIDES` (P22), `SKIPPED_STALE_ENTRY`, `SKIPPED_ENTRY_AT_OR_BEYOND_STOP`,
   `SKIPPED_R_TOO_SMALL`, `SKIPPED_SRC_RR`, `SKIPPED_SRC_NO_TARGET`, `SKIPPED_TARGET_ALREADY_PASSED`,
   `SKIPPED_SESSION_FILTER`, `SKIPPED_NEWS`, `SKIPPED_ROLLOVER`, `NOT_EVALUATED_DATA_GAP`, `NOT_EVALUATED_WARMUP`.
   (`DISABLED_PENDING_PIP_CONFIRMATION` is retired in 0.3.2; `SKIPPED_TF_NOT_ALLOWED` is retired: the TF gate is the failure code
   `TF_NOT_ALLOWED`.) A closed trade whose costs are incomplete is tagged `PENDING_COST_SPEC` (G9).

**Hub counters - two levels so nothing is double counted:**

- **Canonical counters**, stored ONCE per `pattern x side x timeframe x version` (`side` may be NEUTRAL): `shapes`,
  `base_formed`. P08: shapes NEUTRAL, formed per direction. P09: shapes and formed NEUTRAL.
- **Variant counters**, stored per `pattern x side x timeframe x variant x version`: `qualified`, `signals`,
  `trades`, each skip/expiry reason, open and closed trades, P&L. A variant card shows `base_formed` by lookup and it
  is never summed across variants. Early-setup patterns (P14E, P19E) are their own identities. Counts are never
  derived from trades.

### G1 ATR

`ATR = atr_pre` = simple mean of True Range over the 14 completed candles ending at `i0-1`
(`TR = max(H-L, |H-Cprev|, |L-Cprev|)`), an exact rational. Needs 15 completed bars before `i0` else
`NOT_EVALUATED_WARMUP`. The candidate pattern never influences its own ATR.

### G2 Size classes

- `LARGE(k)`: `B>=0.60*ATR` AND `R>=0.80*ATR` AND `B/R>=0.60`. **[SPEC]**
- `SMALL(k)`: `B<=0.25*ATR` AND `R<=0.60*ATR`. **[SPEC]**
- `DOJI(k)`: `B<=0.05*R`.
- `MIN_RANGE_SINGLE`: single-candle patterns also need `R>=0.50*ATR`. **[SPEC]**

### G3 Swings and trend

- Swing high at bar j: `H[j]` strictly greater than the highs of the 2 bars before and 2 bars after; swing low
  mirrors. Confirmed when bar j+2 is complete.
- **200-bar window (ruling A-24):** a swing belongs to the lookback when its CENTRE bar j lies among the last 200
  completed bars. Its two left neighbours may lie just outside the window if they exist; no unconfirmed right-hand
  bars are ever used.
- `TREND(at i0-1)`: uses only swings confirmed by then, own TF. Last two swing highs (SH1 older, SH2 newer) and lows
  (SL1, SL2). **UP** if `SH2>=SH1+0.10*ATR` AND `SL2>=SL1+0.10*ATR`; **DOWN** if `SH2<=SH1-0.10*ATR` AND
  `SL2<=SL1-0.10*ATR`; else **RANGE**; fewer than two of each: **UNDETERMINED**.
- `TREND_HTF`: same on the higher TF (M1->M15, M5->H1, M15->H1, M30->H4, H1->H4, H4->D1, D1->W1, W1->MN1).
  Context only; never required by any rule in v1.

### G4 Support / resistance zones

**Two separate zone sets:** `zones_prepattern` (computed at `i0-1`, used only for `AT_SUPPORT`/`AT_RESISTANCE`) and
`zones_at_entry` (computed once at entry, used only for targets; see G10). They use the same procedure with a
different completed-bar cut-off, and both use the pattern's `atr_pre`.

- Collect the confirmed swing prices of the lookback (G3); sort ascending; cluster greedily (a cluster starts at the
  lowest unassigned price `p0` and takes every price `<= p0 + 0.25*ATR`). A cluster is a **zone** if it has >= 2 pivots
  with at least one pair >= 3 bars apart. Centre = median (**for an even count, the arithmetic mean of the two middle
  prices, ruling A-23**); zone = centre +- `0.125*ATR`. Highs and lows are pooled. **Automatic role reversal merely because price crossed a zone is not modelled; a zone's role can change only when a later confirmed contributing pivot establishes the opposite role.**
- **Zone role and death (ruling A-01, revised by Claude in 0.3):** a zone's ROLE is the type of its most recent
  contributing pivot (a swing low -> SUPPORT, a swing high -> RESISTANCE); the zone may still be used for either
  `AT_*` flag or as a target (pivots are pooled). A SUPPORT zone is DEAD once a completed candle AFTER that latest
  pivot closes more than `0.10*ATR` BELOW its bottom; a RESISTANCE zone once a completed candle after it closes more
  than `0.10*ATR` ABOVE its top. Bars before the latest contributing pivot are never scanned, so a later pivot that
  re-joins the cluster revives the zone; the same `atr_pre` of that evaluation is used. Dead zones are ignored by
  `AT_*` flags and by every target rule. **Same-candle pivots (D-038 addendum):** if the latest contributing candle is
  both a swing high and a swing low and both pivots join the same zone, neither is "latest": `role = AMBIGUOUS`, and the zone
  is excluded from `AT_*` flags and from every structural target (treated like a dead zone; no death scan applies) until a
  later single-type confirmed pivot establishes its role. (The reviewer's first ruling - dead after a close beyond EITHER edge - was
  replaced because it kills every support zone the moment price bounces upward from it; see section 4.)
- `AT_SUPPORT` (bullish): distance from the pattern's lowest low to the nearest LIVE zone (0 if inside)
  `<= 0.10*ATR`; `AT_RESISTANCE` (bearish): same with the highest high. Fibonacci and round numbers are context flags
  only (`ROUND_50`: extreme within `0.10*ATR` of a multiple of $50).

### G5 Gap

`gap_thr = max($0.10, 0.05*ATR)`. Bullish gap between bars a<b: `L_b >= H_a + gap_thr`; bearish:
`H_b <= L_a - gap_thr`. Gaps across a closed interval are allowed and tagged `across_break`.

### G6 Sessions and news (source variants only; always recorded)

- ASIA = 09:00-17:00 `Asia/Tokyo`; LONDON = 08:00-17:00 `Europe/London`; NY = 08:00-17:00 `America/New_York` (DST
  automatic). **Intervals are half-open `[start, end)` (ruling A-06): 08:00 belongs to London, exactly 17:00 does
  not.** `ASIA_ONLY` = in ASIA and in neither LONDON nor NY. The session of a signal is the session at its
  `signal_time`. **[SPEC]**
- `economic_events(time_utc, currency, impact, name)`. `F_NEWS_HIGH`: blocked T-30 to T+15 min around any high-impact
  USD event. `F_NEWS_MAJOR`: NFP, CPI, FOMC decision, FOMC press conference, blocked T-60 to T+30 min. **Endpoints are
  inclusive (ruling A-07).** **[SPEC]** Blocked signals are still detected and logged.
  **Source and coverage (D-054):** the calendar is the free Forex Factory / FairEconomy weekly XML feed (title, currency, date, time,
  impact High/Medium/Low). Its clock is decided from official release times (NFP/CPI 08:30 ET, FOMC decision 14:00 ET, press
  conference 14:30 ET) and refused if none fits. `impact=High` feeds `F_NEWS_HIGH`; the MAJOR kinds come from a fixed title table
  (`news/feed.py`; Core CPI is grouped with CPI; "FOMC Member ... Speaks" is not an FOMC decision). A filter is applied only where
  the stored calendar COVERS its window; without coverage the variant is `NOT_EVALUATED_NEWS_COVERAGE` (no evaluation, no research
  clock), never "no news". **Point in time:** the calendar used for a signal is the latest accepted download fetched at or before the signal (every download is kept immutable); an untimed high-impact USD event (HIGH filter) or untimed NFP/CPI/FOMC item (MAJOR filter) on the window's day also gives `NOT_EVALUATED_NEWS_COVERAGE`.

### G7 Indicators (filters and context only)

`RSI14` = Wilder RSI on closes at the completion of the last pattern candle; needs 100 bars of warm-up. **Fixed sequence (D-054):** the RSI is computed from exactly the 100 completed closes immediately before the pattern's first bar plus the pattern's own closes through its last candle (never from older history), so its value cannot change when older data is later added.

### G8 Measurement layers

**Layer A - RAW (candle prices only, no trading assumptions).** `d=+1` bullish, `-1` bearish. **RAW is generated once
per canonical BASE signal only.** A signal that exists only in a source variant produces NO RAW record
(`VARIANT_FORWARD_BEHAVIOUR` is a separate future metric).
- Reference `ref`: close-based signal -> open of the bar after `signal_bar`; tick-based BASE signal (P14E/P19E) ->
  the trigger tick's executable price (ask for `d=+1`, bid for `d=-1`). `ref_time` = the open of that bar / the
  trigger tick time.
- **Horizon end:** for `h in {1,3,5,10,20}`: close-based `horizon_end(h) = s + h`; tick-based `horizon_end(h) = s + h - 1`
  (the signal bar itself is bar 1). `ret_h`, `MFE_h` and `MAE_h` use the bars from the first bar after `ref` up to and
  including `horizon_end(h)`.
- `ret_h = d*(close[horizon_end(h)] - ref)` (USD and ATR units). **Non-negative magnitudes (ruling A-27):**
  `MFE_h = max(0, max over bars of d*(fav_extreme - ref))` and `MAE_h = max(0, -min over bars of d*(adv_extreme - ref))`
  where the favourable extreme is the bar high for `d=+1` (low for `d=-1`) and the adverse extreme the bar low (high).
  `dir_ok_h = ret_h>0`. A data gap in the window gives `NULL`.
- **`mfe_before_mae_h` (defined in 0.3, needs ticks):** using BID ticks from `ref_time` to the completion of
  `horizon_end(h)`, find the first tick at which the running favourable extreme reaches `MFE_h` and the first tick at
  which the running adverse extreme reaches `MAE_h`. `TRUE` if the MFE tick is strictly earlier, `FALSE` if the MAE
  tick is earlier, `NULL` if `MFE_h = 0`, `MAE_h = 0`, or the ticks do not cover the window.

**Layer B - BASELINE (identical mechanics for every pattern).**
- **Entry:** first executable tick with `time >= entry_eligible_time`. BUY at ask, SELL at bid. If
  `open_elapsed(entry_eligible_time, first_tick) > 15 minutes` -> `SKIPPED_STALE_ENTRY`. Scheduled closures do not
  count, so a weekly candle completing at the Friday close can enter at Monday's first tick (tagged
  `entry_across_break`). **[SPEC]**
- **Entry validity (ruling A-25, applies to EVERY variant):** after the stop is quantised (G13), a long whose actual
  fill is `<= stop` (short: `>= stop`) is not traded: `SKIPPED_ENTRY_AT_OR_BEYOND_STOP`. `R = |entry_fill - stop|`
  is only formed for a valid entry.
- **Stop:** beyond the pattern extreme: bullish `pattern_low - G_BUFFER`; bearish `pattern_high + G_BUFFER`;
  `pattern_low/high` = lowest low / highest high over all candles of the geometry (not any confirmation candle);
  `G_BUFFER = max($0.20, 0.05*ATR)`, then quantised (G13). **[SPEC]**
- **Target:** fixed `2R`, `R=|entry_fill-stop|`. No partials. No RSI/MACD/DXY/news/session/level filter.
  **`SKIPPED_R_TOO_SMALL` if `R < max(4*spread_at_entry, 0.10*ATR)` - BASELINE ONLY (ruling A-11);** source-normalized
  plans are not screened by this guard so their own tightness shows up in the costs. **[SPEC]**
- **Time stop (ruling A-13):** `MAX_HOLD = 50`. The candle containing the entry tick is bar 0 and does not count.
  Count the next 50 completed broker bars of the pattern's own TF that actually exist (closures create no bars). Exit
  at the first executable tick at or after the completion of bar 50 (`exit_reason=TIME`, BUY closes at bid, SELL at
  ask); if that completion is immediately followed by a scheduled closure the exit is the first tick after the
  reopening, tagged `exit_across_break`. High-TF trades mature very slowly (`INSUFFICIENT_DATA` for long); accepted.
- **Sizing:** `1R = 1% of REF_EQUITY`, `REF_EQUITY=$10,000` **[SPEC]**. `loss_per_lot = (R / tick_size) * tick_value`;
  `lots = risk_usd / loss_per_lot`. The virtual ledger keeps the unrounded value. The Vantage demo mirror rounds down to
  the lot step and records `requested_risk` and `actual_demo_risk`; below the minimum lot -> `MIRROR_SKIPPED_MIN_LOT`.
  The virtual trade and the mirror use the SAME quantised stop and target levels (G13).

**Layer C - SOURCE-NORMALIZED PLAN (it is not an "exact" reproduction).** It follows a source's confirmation, entry,
stop, targets, partials and filters as closely as can be made deterministic; every departure is written in field 26
`source_deviation_notes`. Ids: `<ID>/SRC-PS`, `/SRC-CB`, `/SRC-SH`. A variant restates its prior state only when it
changes it; otherwise the base prior state is INHERITED (ruling A-05).
- Where a source names two targets but no split, v1 uses the first target only (second recorded as OPEN).
- Where a source names a structural target but no minimum ratio, `G_MIN_REWARD_DEFAULT = 1.5R`. **[SPEC]**

### G9 Fills, ordering and costs

- Long: stop at first tick with `bid <= stop`, fill = that tick's bid; target at first tick with `bid >= target`,
  fill = target price. Short: stop at `ask >= stop`, fill = that ask; target at `ask <= target`, fill = target price.
  Gaps through a stop fill at the first tick price; a favourable gap through a target earns the target price only.
- Tick order decides stop vs target. **If ticks are missing (ruling A-26)** and stored BID/ASK bars exist, use the
  relevant side: long stop/target on BID low/high, short stop/target on ASK high/low. If a bar proves both the stop and
  the target could have been hit, score **STOP FIRST**, tag `resolution=CONSERVATIVE_STOP_FIRST` and report a
  target-first sensitivity figure. A short with no ASK bar cannot be resolved from bars (`NEEDS_ASK_BARS`). Never delete.
- **Costs (ruling A-14):** result in R = `(exit-entry)*d/R` minus commission and swap converted to R (`cost_usd / 100`).
  The account/instrument specification must hold: `swap_mode`, `swap_long`, `swap_short` (account currency per lot per
  night), `rollover_time` (broker calendar), triple-swap weekday and multiplier, and the effective date. A swap charge
  applies at EVERY broker rollover instant crossed while the position is open (times the multiplier on the triple
  day). A closed trade that crossed at least one rollover while the swap specification is missing is stored with
  `PENDING_COST_SPEC`: the trade is recorded, its net R is left empty, and it is excluded from survival statistics
  until backfilled. A trade that crossed no rollover needs no swap.

### G10 Entry mechanics, targets and validity

- `NEXT_TICK`: as Layer B at `entry_eligible_time`.
- `CONFIRM_CLOSE`: the confirmation test runs on the immediately following completed bar unless the pattern says
  otherwise (max extension `G_CONFIRM_MAX=3` bars **[SPEC]**); success -> entry at the first executable tick after
  that bar completes; failure -> `EXPIRED_NO_CONFIRMATION`; while waiting -> `PENDING_CONFIRMATION`.
- `STOP_ENTRY(trigger)`: armed at `arm_time`; the fill tick is `signal_time`; long fills when ask `>= trigger`, short
  when bid `<= trigger`. **The window is defined by bar membership (ruling A-18):** the order lives through the next
  THREE completed broker bars after `arm_time`; a tick that belongs to bar 4 (including one stamped exactly at bar 3's
  completion instant) is too late -> `EXPIRED`. Cancelled if price first reaches the (quantised) stop level ->
  `INVALIDATED_BEFORE_ENTRY`. **[SPEC]**
- `OPEN_TRIGGER`: fires on the first executable tick of the bar after the geometry if a stated opening condition holds.
  The condition is tested on the BID (chart) opening price `bid_open`, never the ask; the order then executes BUY at
  ask / SELL at bid. Used only by the EARLY_SETUP patterns (P14E, P19E). Every trigger counts as a trade, whether or
  not the completed pattern later forms.
- **`T_SR(minR)`:** target = near edge of the NEAREST live zone beyond the entry in the trade direction, compared
  after quantisation (G13). If `< minR` -> `SKIPPED_SRC_RR`. No zone -> `SKIPPED_SRC_NO_TARGET`. The rule never steps
  over a nearer obstacle. **A live zone that straddles or contains the entry is the nearest obstacle; its near edge is
  at or behind the entry, so the result is `SKIPPED_TARGET_ALREADY_PASSED` (ruling A-04).**
- **`T_SWING(minR)`:** BUY targets the nearest confirmed swing HIGH above the entry; SELL the nearest swing LOW below
  it (ruling A-16). Same nearest-only and minimum-R behaviour.
- **Entry snapshot:** targets that use zones or swings (`T_SR`, `T_SWING`, TP2 anchors) are computed ONCE, immediately
  before the entry, from zones/swings confirmed by `entry_eligible_time` (`zones_at_entry`), stored on the trade and
  frozen. A trade with no valid target is skipped with its reason code and never re-evaluated.
- **Target validity and precedence (ruling A-19):** every target must be strictly beyond the ACTUAL entry price. If
  not -> `SKIPPED_TARGET_ALREADY_PASSED`, checked BEFORE any `SKIPPED_SRC_RR` test.
- Conservative pullback entries named in sources (50% retrace etc.) are deferred to v1.1.

### G11 Identity, versions, overlaps, experiment size

- Ids: `GT-<PATTERN>-<BULL|BEAR>-v1.0`; variants `.../BASE`, `.../SRC-PS`, etc. Any rule or constant change creates a
  new version and a new sample; old results stay attached to the old version.
- Overlapping identities are allowed and all logged (ruling A-21). Two ids: **`formation_cluster_id`** groups
  detections with the same TF, direction and `formation_end_bar`; **`signal_cluster_id`** groups strategies whose
  SIGNAL has the same TF, direction and `signal_bar` (so Kicker Early and the completed Kicker share a signal cluster
  but not a formation cluster). Results are never pooled across TFs, variants or versions.
- Size: about 32 sides x 9 TFs = 288 baseline strategies plus about 41 source-variant sides x up to 9 TFs = at most
  about 369 more: **up to about 657 strategies** (the ten pip-dependent variants are enabled since 0.3.2). Survivors must clear the
  untouched validation stage before any real money.

### G12 Context recorded for every detection (never required unless a variant says so)

`trend_state`, `trend_state_htf`, `at_support`/`at_resistance` and distance to nearest zone, `rsi14`, `atr_pre`, spread
at signal, session flags, `news_flags`, `round_50`, `across_break`, weekday and hour, size ratios of the pattern
candles, `formation_cluster_id`, `signal_cluster_id`, `qualification_failures`.

### G13 Executable-price quantisation (new in 0.3, ruling A-30)

Internal arithmetic is exact. Every price that becomes an ORDER LEVEL is then quantised to `tick_size`
deterministically, and the virtual trade and the Vantage mirror use the same quantised level:

- **Stops** round AWAY from the entry (long: down, short: up).
- **Fixed-R, Fibonacci and measured-move targets** round in the PROFIT direction (long: up, short: down).
- **Structural targets** (zone edges) round TOWARD the entry (long: down, short: up) so the target never lies beyond
  the obstacle it claims to respect. Swing pivots are already on the tick grid.
- **Stop-entry triggers** round in the trigger direction (long: up, short: down).
- Minimum-R, target-validity and stop-validity tests use the quantised levels.

---

## 2. Test-vector requirement

Golden test vectors GV-0.2 (`tests/`, drafted by Claude, reviewed by ChatGPT) are the acceptance test for this draft: small OHLC/tick
sequences with the expected yes/no and expected entry/stop/target, so an implementation can be checked.
Worked examples below are illustrative only.

---

## 3. Wave-1 pattern specifications

Fields 1-25 are the agreed schema; field 26 is new in 0.2. "G" points to section 1. Every "FINAL ACCEPTED
RULE" reads **PROPOSED v1.0** until approved. In every pattern, `shape` = geometry only, `pattern` = shape
plus the stated prior state (G0b).

### P01 HAMMER (bullish) — `GT-HAMMER-BULL-v1.0`

1. GT-HAMMER-BULL-v1.0 (BASE, SRC-PS)  2. Hammer  3. bullish  4. 1
5. **Shape `HAMMER_SHAPE` (K1):** `R>=0.50*ATR` AND `LW>=2.0*B` AND `UW<=0.10*R` AND `min(O,C)>=L+0.65*R`.
6. **Prior state (pattern = shape + this):** `TREND(i0-1)=DOWN`. Same shape after `UP` is logged as a
   Hanging Man candidate.
7. Formation = signal = completion of K1.
8. Baseline per G8; SRC-PS fails if confirmation fails/expires.
9-11. **Baseline:** BUY, stop `L1-G_BUFFER`, 2R.
12. **SRC-PS entry:** CONFIRM_CLOSE BUY.  13. **Stop:** `L1 - 17.5*PIP_SRC_USD` (source "15-20 pips").
14. **Target:** single `2R` (source "2:1 minimum"). No partials.
15. **Confirmation:** K2 bullish AND `C2>H1`. **[INTERP]**  16. **Expiry:** K2 only.
17. **Filters:** prior state relaxed to `DOWN OR AT_SUPPORT`.
18. Context: G12; wick and body ratios.  19. Session/news: none stated.  20. Gap: none.
21. **Aliases:** subset of Pin Bar (bull); overlaps Dragonfly when the body is tiny.
22. **Example:** `O=4200.00 H=4200.50 L=4194.00 C=4200.20`, ATR 4.0: `R=6.5>=2.0`, `B=0.20`, `LW=6.0>=0.4`,
    `UW=0.30<=0.65`, `min(O,C)=4200.00>=4194+4.225=4198.225` -> shape YES; pattern YES if trend DOWN.
23. **Sources:** master row 1; PS `/hammer-candlestick` (source 9); TV, SA, SH, CB.
24. **Open:** "upper third" vs "upper 40%" in the source (this spec: 35%); `MIN_RANGE_SINGLE` and ratios [SPEC].
25. PROPOSED v1.0 = fields 5+6+7.
26. **SRC-PS is ENABLED** (uses `PIP_SRC_USD = 0.10`, confirmed in 0.3.2, G0). **Source deviation notes:** "initial bullish momentum" replaced by a close test; "15-20 pips" converted at an
    confirmed $0.10/pip (D-040); "downtrend or known support" implemented with the G3/G4 definitions.

### P02 SHOOTING STAR (bearish) — `GT-SHOOTINGSTAR-BEAR-v1.0`

1. GT-SHOOTINGSTAR-BEAR-v1.0 (BASE, SRC-PS)  2. Shooting Star  3. bearish  4. 1
5. **Shape:** `R>=0.50*ATR` AND `UW>=2.0*B` AND `LW<=0.10*R` AND `max(O,C)<=H-0.65*R`.
6. **Prior state:** `TREND(i0-1)=UP` (same shape after DOWN = Inverted Hammer candidate).  7. As P01.
8-11. **Baseline:** SELL at bid; stop `H1+G_BUFFER`; 2R.
12. **SRC-PS entry:** CONFIRM_CLOSE SELL.  13. **Stop:** `H1 + 20*PIP_SRC_USD` (source "15-25 pips").
14. **Target:** `T_SWING(1.5)` (nearest confirmed swing low below entry; skip if under 1.5R). Second target
    ("rally origin") OPEN.
15. **Confirmation:** K2 bearish AND `C2<min(O1,C1)`. **[INTERP]**  16. K2 only.
17. **Filters:** skip `ASIA_ONLY` (source: reduced size or skipped) **[INTERP]**; prior state
    `UP OR AT_RESISTANCE`.
18-20. G12; none; none.  21. Subset of Pin Bar (bear); overlaps Gravestone.
22. Red body preferred by source, not required.
23. Master row 4; PS `/shooting-star` (source 10); TV, SH, CB.  24. Open: second target; size reduction.
25. PROPOSED v1.0.
26. **SRC-PS is ENABLED** (uses `PIP_SRC_USD = 0.10`, confirmed in 0.3.2, G0). **Deviation notes:** open-based confirmation replaced by a close test; "reduced size" replaced by skip;
    rally-origin target dropped; pips converted at $0.10.

### P03 PIN BAR (bullish, bearish) — `GT-PINBAR-BULL-v1.0`, `GT-PINBAR-BEAR-v1.0`

1. IDs as given; variants BASE, SRC-PS, SRC-CB.  2. Pin Bar  3. both  4. 1
5. **Shape = pattern:** `R>=0.50*ATR`, `B<=0.33*R`, dominant wick `>=0.66*R`, opposite wick `<=0.10*R`.
   Bullish: dominant wick is the lower one and `C>=L+0.75*R`. Bearish: upper one and `C<=H-0.75*R`.
6. **Prior state:** none (context recorded).  7. Formation = signal = K1 completion.
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
26. **SRC-PS is ENABLED** (uses `PIP_SRC_USD = 0.10`, confirmed in 0.3.2, G0). **Deviation notes:** PS conservative 50%-retrace entry deferred; "body inside prior candle" dropped from
    identity; CB "8/21 MA, Fibonacci" location not used (S/R zones only); second targets dropped.

### P04 DRAGONFLY DOJI (bullish) — `GT-DRAGONFLY-BULL-v1.0`

1. GT-DRAGONFLY-BULL-v1.0 (BASE, SRC-PS)  2. Dragonfly Doji  3. bullish  4. 1
5. **Shape:** `DOJI` AND `UW<=0.05*R` AND `LW>=0.80*R` (implied by the first two) AND `R>=0.50*ATR`.
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. Formation = signal = K1 completion.
8-11. **Baseline:** BUY, stop `L1-G_BUFFER`, 2R.
12. **SRC-PS entry:** CONFIRM_CLOSE BUY.  13. **Stop:** `L1 - 10*PIP_SRC_USD` (source 5-15 pips).
14. **Target:** `T_SR(1.5)`.
15. **Confirmation:** K2 bullish AND `C2>max(O1,C1)`; fails if K2 is bearish or a doji.  16. K2 only.
17. **Filters:** `AT_SUPPORT`; skip `ASIA_ONLY`; `F_NEWS_MAJOR`.
18-20. G12; as 17; none.  21. Subset of Bull Pin Bar; overlaps Hammer.
22. Exact `O=C=H` not required (too strict).  23. Master row 8; PS `/dragonfly-doji`; SH, CB.
24. Open: 5% tolerances [SPEC].  25. PROPOSED v1.0.
26. **SRC-PS is ENABLED** (uses `PIP_SRC_USD = 0.10`, confirmed in 0.3.2, G0). **Deviation notes:** pips at $0.10; "buy limit at the level" alternative dropped; H4/D1 emphasis recorded only.

### P05 GRAVESTONE DOJI (bearish) — `GT-GRAVESTONE-BEAR-v1.0`

1. GT-GRAVESTONE-BEAR-v1.0 (BASE, SRC-PS)  2. Gravestone Doji  3. bearish  4. 1
5. **Shape:** `DOJI` AND `LW<=0.05*R` AND `UW>=0.80*R` AND `R>=0.50*ATR`.
6. **Prior state:** `TREND(i0-1)=UP`.  7. As P04.
8-11. **Baseline:** SELL, stop `H1+G_BUFFER`, 2R.
12. **SRC-PS entry:** CONFIRM_CLOSE SELL.  13. **Stop:** `H1 + 10*PIP_SRC_USD`.  14. **Target:** `T_SR(1.5)`.
15. **Confirmation:** K2 closes below `min(O1,C1)`; fails if it closes above.  16. K2 only.
17. **Filters:** `AT_RESISTANCE`. No session/TF rule in the source.  18-20. G12; none; none.
21. Subset of Bear Pin Bar; overlaps Shooting Star.  22. Differs from Shooting Star only by near-zero body.
23. Master row 9; PS `/gravestone-doji`; SH, CB.  24. Open: tolerances [SPEC].  25. PROPOSED v1.0.
26. **SRC-PS is ENABLED** (uses `PIP_SRC_USD = 0.10`, confirmed in 0.3.2, G0). **Deviation notes:** pips at $0.10; sell-limit alternative dropped.

### P06 BULLISH ENGULFING — `GT-ENGULF-BULL-v1.0`

1. GT-ENGULF-BULL-v1.0 (BASE, SRC-PS, SRC-CB, SRC-SH)  2. Bullish Engulfing  3. bullish  4. 2
5. **Shape:** K1 bear, K2 bull, `O2<=C1`, `C2>=O1`, `B2>B1`, `B1>0.05*R1`. Flags: `B2>=2*B1`; wicks also
   engulfed (`L2<=L1`, `H2>=H1`).
6. **Prior state:** `TREND(i0-1)=DOWN`. The same shape in an UP trend is logged as
   `candidate=ENGULF_CONTINUATION` (continuation reading deferred).  7. Formation = signal = K2 completion.
8-11. **Baseline:** BUY, stop `min(L1,L2)-G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK.  13. **Stop:** `min(L1,L2) - 20*PIP_SRC_USD`.
14. **Target:** `T_SR(1.5)`; second target (3R) OPEN.
15-16. None; none.
17. **Filters:** SRC-PS prior state `DOWN OR AT_SUPPORT`. SRC-CB: `TREND=DOWN` AND `AT_SUPPORT`, TF in
    {H1,H4,D1}, NEXT_TICK, stop `min(L1,L2)-G_BUFFER`, target `T_SR(2.0)`. SRC-SH: shape tightened to wicks
    engulfed AND `RSI14(C2)<30`; NEXT_TICK; stop/target = BASELINE (source gives none). The base prior state (`TREND=DOWN`) is INHERITED (ruling A-05).
18. Context: size ratio, wick flag, RSI14.  19. Session/news: SRC-PS none.  20. Gap: none.
21. Aliases: Outside Bar when wicks are engulfed too. Piercing Line is disjoint (`C2<O1` there).
22. **Example:** K1 `O=4210 H=4211 L=4203 C=4204`; K2 `O=4203.5 H=4212.5 L=4203 C=4212`: `O2<=4204`,
    `C2>=4210`, `B2=8.5>B1=6` -> YES.
23. Master row 13; PS `/bullish-engulfing` (source 7); SH (source 4); CB (source 15); TV, SA.
24. **Open:** SH's own text asks for both "enter at the close" and "third candle confirms".
25. PROPOSED v1.0.
26. **SRC-PS is ENABLED** (uses `PIP_SRC_USD = 0.10`, confirmed in 0.3.2, G0). **Deviation notes:** PS "or at support" alternative implemented as `AT_SUPPORT`; PS second target dropped;
    SH third-candle confirmation not used (entry-at-close reading); CB moving-average/Fibonacci locations not
    used; continuation reading deferred.

### P07 BEARISH ENGULFING — `GT-ENGULF-BEAR-v1.0`

1. GT-ENGULF-BEAR-v1.0 (BASE, SRC-PS, SRC-CB)  2. Bearish Engulfing  3. bearish  4. 2
5. **Shape:** K1 bull, K2 bear, `O2>=C1`, `C2<=O1`, `B2>B1`, `B1>0.05*R1`.
6. **Prior state:** `TREND(i0-1)=UP` (else `ENGULF_CONTINUATION` candidate).  7. As P06.
8-11. **Baseline:** SELL, stop `max(H1,H2)+G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK.  13. **Stop:** `max(H1,H2) + 20*PIP_SRC_USD`.
14. **Target:** `T_SR(1.5)`; second target (~3R) OPEN.  15-16. None; none.
17. **Filters:** SRC-PS prior state `UP OR AT_RESISTANCE`; skip `ASIA_ONLY`. SRC-CB mirrors P06.
18-20. G12; as 17; none.  21. Outside Bar when wicks are engulfed too.  22. As P06.
23. Master row 14; PS `/bearish-engulfing` (source 8); CB.  24. Open: DXY unavailable.  25. PROPOSED v1.0.
26. **SRC-PS is ENABLED** (uses `PIP_SRC_USD = 0.10`, confirmed in 0.3.2, G0). **Deviation notes:** DXY correlation and RSI-divergence filters not enforced (no feed; recorded as
    unavailable); Fibonacci-extension location recorded only; pips at $0.10.

### P08 OUTSIDE BAR (bullish, bearish) — `GT-OUTSIDE-BULL-v1.0`, `GT-OUTSIDE-BEAR-v1.0`

1. IDs as given (BASE, SRC-PS)  2. Outside Bar  3. both  4. 2
5. **Shape (side NEUTRAL, `OUTSIDE_BAR_SHAPE`):** `H2>H1` AND `L2<L1` (strict). **Formation:** the shape AND the K2
   direction: bullish if `C2>O2`, bearish if `C2<O2`; `C2=O2` logs the shape but forms no directional pattern
   (ruling A-08). Flag: `R2>=1.5*ATR`.
6. **Prior state:** none.  7. Formation = signal = K2 completion.
8-11. **Baseline:** bullish BUY, stop `L2-G_BUFFER`; bearish SELL, stop `H2+G_BUFFER`; 2R.
12. **SRC-PS entry:** NEXT_TICK.  13. **Stop:** `L2-G_BUFFER` / `H2+G_BUFFER` (source gives no buffer) **[INTERP]**.
14. **Target:** `T_SR(1.5)`.  15-16. None; none.
17. **Filters:** SRC-PS requires `R2>=1.5*ATR` (`SIZE_FILTER`). At the signal it skips (ruling A-03): K2 containing a
    high-impact USD event (`SKIPPED_NEWS`; K2 only, not K1), and - on intraday TFs M1..H4 only - a K2 whose nominal
    period overlaps the broker's scheduled daily rollover pause (`SKIPPED_ROLLOVER`; the window is a calendar
    parameter). D1/W1/MN1 are exempt because every such bar contains the pause by construction.
18-20. G12; as 17; none.  21. Alias: Engulfing (Outside Bar is stricter).
22. The size filter is a flag in BASE, a requirement in SRC-PS.
23. Master row 15; PS `/outside-bar`.  24. Open: news delay replaced by skip.  25. PROPOSED v1.0.
26. **Deviation notes:** "wait 1-2 candles after a news spike" replaced by skipping the occurrence.

### P09 INSIDE BAR BREAKOUT (bullish, bearish) — `GT-INSIDE-BULL-v1.0`, `GT-INSIDE-BEAR-v1.0`

1. IDs as given (BASE, SRC-PS, SRC-CB)  2. Inside Bar (breakout)  3. both  4. 2 + breakout bar
5. **Shape / formation (side NEUTRAL, ruling A-09):** mother K1, inside K2 with `H2<H1` AND `L2>L1` (strict). This is
   `SHAPE_DETECTED` and `BASE_PATTERN_FORMED` with `side=NEUTRAL` (an `INSIDE_BAR` exists) and is counted once, even if
   nothing follows. Compression `R2/R1` recorded.
   **Signal candle `Kb`:** first candle among the next three (`b=3,4,5`) whose CLOSE is outside the mother range:
   `Cb>H1` bullish, `Cb<L1` bearish. While the window is open the disposition is `PENDING_BREAKOUT`; a close outside on
   the OTHER side than the strategy's -> `NOT_TRIGGERED_OTHER_SIDE`; none within 3 candles -> `EXPIRED_NO_CONFIRMATION`
   for both strategies. The eventual signal belongs to the BULL or BEAR strategy.
6. **Prior state:** none.  7. `formation_end_bar`=K2; `signal_bar`=`Kb`; `signal_time` = completion of `Kb`.
8-11. **Baseline:** entry NEXT_TICK after `Kb`; stop = opposite side of the mother `L1-G_BUFFER` /
    `H1+G_BUFFER` (`pattern_low/high` = mother range); 2R.
12. **SRC-PS entry:** NEXT_TICK after `Kb` (source says both "buy stop above" and "wait for a close outside";
    the close reading is adopted) **[INTERP]**.
13. **Stop:** opposite mother side `+-3.5*PIP_SRC_USD` (source 2-5 pips).  14. **Target:** `T_SR(1.5)`.
15. Confirmation: the breakout close.  16. Expiry: 3 bars after K2.
17. **Filters:** SRC-PS: TF in {H1,H4,D1,W1,MN1}; skip `ASIA_ONLY`; `F_NEWS_MAJOR`. SRC-CB: breakout WITH the
    trend (bull needs `TREND=UP`, bear `TREND=DOWN`), mother bar at a level (ruling A-15: bull -> the mother LOW at
    support `AT_SUPPORT(L1)`, bear -> the mother HIGH at resistance `AT_RESISTANCE(H1)`), TF in {H4,D1}; stop opposite
    mother side `+-G_BUFFER`; target `T_SR(2.0)`.
18-20. Context: nested-bar count, compression; as 17; none.  21. Aliases: none.
22. A bar that pokes outside the mother range but closes inside is not a breakout; it stays armed until
    expiry (and may be a Sweep & Reclaim, P22).
23. Master row 16; PS `/inside-bar`; CB; TV, SH.  24. Open: order-based vs close-based entry.  25. PROPOSED v1.0.
26. **SRC-PS is ENABLED** (uses `PIP_SRC_USD = 0.10`, confirmed in 0.3.2, G0). **Deviation notes:** buy-stop entry replaced by close-based entry; source pips at $0.10; news window uses
    `F_NEWS_MAJOR`.

### P10 TWEEZER TOP (bearish) — `GT-TWEEZERTOP-BEAR-v1.0`

1. GT-TWEEZERTOP-BEAR-v1.0 (BASE, SRC-PS)  2. Tweezer Top  3. bearish  4. 2
5. **Shape:** K1 bull, K2 bear, `|H1-H2|<=tol`, **`tol=max(3*tick_size, 0.05*ATR)`** (canonical, no pip
   dependency). Flags (ruling A-10, mirrored with P11): K1 closes in its highest 25%, K2 in its lowest 25%.
6. **Prior state:** `TREND(i0-1)=UP`.  7. Formation = K2 completion; signal = the trigger break for SRC-PS,
   K2 completion for BASE.
8-11. **Baseline:** SELL, stop `max(H1,H2)+G_BUFFER`, 2R.
12. **SRC-PS entry:** `STOP_ENTRY(trigger=L2)` SELL **[INTERP]** (source also allows "open of the third
    candle").
13. **Stop:** `max(H1,H2) + 3*PIP_SRC_USD`.  14. **Target:** `T_SR(1.5)` (source: nearest support).
15. Confirmation: the trigger break.  16. Expiry: 3 bars after K2.
17. **Filters:** `AT_RESISTANCE`; skip `ASIA_ONLY`. **SRC-PS identity delta:** `tol_src=max(3*PIP_SRC_USD,
    0.05*ATR)`.
18-20. G12; as 17; none.  21. Bearish Engulfing / Dark Cloud can share a bar.
22. The canonical tolerance grows with ATR.  23. Master row 19; PS `/tweezer-top`; CB, SH.
24. Open: 3-bar trigger expiry [SPEC].  25. PROPOSED v1.0.
26. **SRC-PS is ENABLED** (uses `PIP_SRC_USD = 0.10`, confirmed in 0.3.2, G0). **Deviation notes:** the source's wider pip tolerance applies only inside SRC-PS; entry reading is a trigger
    break; "small pullback" entry deferred.

### P11 TWEEZER BOTTOM (bullish) — `GT-TWEEZERBOTTOM-BULL-v1.0`

1. GT-TWEEZERBOTTOM-BULL-v1.0 (BASE, SRC-PS)  2. Tweezer Bottom  3. bullish  4. 2
5. **Shape:** K1 bear, K2 bull, `|L1-L2|<=tol` (`tol` as P10). Flags: K1 closes in its lowest 25%, K2 in its
   highest 25%.
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. As P10.
8-11. **Baseline:** BUY, stop `min(L1,L2)-G_BUFFER`, 2R.
12. **SRC-PS entry:** `STOP_ENTRY(trigger=H2)` BUY.  13. **Stop:** `min(L1,L2) - 3*PIP_SRC_USD`.
14. **Target:** `T_SWING(1.5)`.  15. Trigger break.  16. 3 bars.
17. **Filters:** `AT_SUPPORT`. Volume divergence (source) not usable - recorded only. SRC-PS identity delta as P10.
18-20. G12; none; none.  21. Bullish Engulfing can share a bar.  22. As P10.
23. Master row 20; PS `/tweezer-bottom`.  24. As P10.  25. PROPOSED v1.0.
26. **SRC-PS is ENABLED** (uses `PIP_SRC_USD = 0.10`, confirmed in 0.3.2, G0). **Deviation notes:** as P10; volume confirmation dropped.

### P12 PIERCING LINE (bullish) — `GT-PIERCING-BULL-v1.0`

1. GT-PIERCING-BULL-v1.0 (BASE, SRC-PS)  2. Piercing Line  3. bullish  4. 2
5. **Shape:** K1 bear AND `LARGE(K1)`; K2 bull; `O2<C1`; `C2>(O1+C1)/2`; **`C2<O1`** (strict, so it cannot
   also be a Bullish Engulfing, which needs `C2>=O1`). Flags: `O2<=L1-gap_thr` (`gap_flag`); penetration
   tier (50-60 / 75 / 90+ %).
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. Formation = signal = K2 completion.
8-11. **Baseline:** BUY, stop `min(L1,L2)-G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK.  13. **Stop:** `L2 - G_BUFFER` (source: below K2's low, not K1's).
14. **Target:** `T_SR(2.0)` (source: minimum 1:2 before entry); second target OPEN.  15-16. None; none.
17. **Filters:** `AT_SUPPORT`; skip signals wholly inside `ASIA_ONLY`.
18-20. Context: penetration %, `gap_flag`; as 17; gap not required (a strict classical-gap variant would be a
    separately named version).
21. Disjoint from Bullish Engulfing.  22. Source says a gap down strengthens - recorded, not required.
23. Master row 21; PS `/piercing-line`; SA, SH.  24. Open: "opens below K1 close" is barely a gap on gold.
25. PROPOSED v1.0.
26. **Deviation notes:** second target dropped; the "at level" location requirement uses G4 zones only.

### P13 DARK CLOUD COVER (bearish) — `GT-DARKCLOUD-BEAR-v1.0`

1. GT-DARKCLOUD-BEAR-v1.0 (BASE, SRC-PS)  2. Dark Cloud Cover  3. bearish  4. 2
5. **Shape:** K1 bull AND `LARGE(K1)`; K2 bear; `O2>C1`; `C2<(O1+C1)/2`; **`C2>O1`** (strict; a Bearish
   Engulfing needs `C2<=O1`).
6. **Prior state:** `TREND(i0-1)=UP`.  7. Formation = signal = K2 completion.
8-11. **Baseline:** SELL, stop `max(H1,H2)+G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK.  13. **Stop:** `H2 + G_BUFFER`.  14. **Target:** `T_SR(1.5)`; source's "scale
    out half, trail the rest" OPEN (trail not defined).
15-16. None; none.  17. **Filters:** `AT_RESISTANCE`.  18-20. G12; none; source says "gap required" but
    defines it as `O2>C1`, which is the rule.
21. Disjoint from Bearish Engulfing.  22. Mirror of P12.
23. Master row 22; PS `/dark-cloud-cover`; SH.  24. Open: trailing. The differences from P12 (no 2R minimum, no Asia skip) are
    DELIBERATE: the Pro-Scalper pages differ (ruling A-20).  25. PROPOSED v1.0.
26. **Deviation notes:** scale-out/trailing dropped; single target.

### P14 KICKER, completed pattern (bullish, bearish) — `GT-KICKER-BULL-v1.0`, `GT-KICKER-BEAR-v1.0`

1. IDs as given (BASE, SRC-PS-COMPLETED)  2. Kicker (completed)  3. both  4. 2
5. **Shape (fixed in 0.2):** bullish: K1 bear `LARGE`; K2 bull `LARGE`; **`O2>=O1`** (K2 opens at or above
   K1's open, so K2's body does not overlap K1's body); `C2>=H2-0.10*R2`. Bearish: K1 bull `LARGE`; K2 bear
   `LARGE`; `O2<=O1`; `C2<=L2+0.10*R2`. Flags: `bull_gap_flag = O2>=O1+gap_thr` (bullish
   Kicker), `bear_gap_flag = O2<=O1-gap_thr` (bearish Kicker).
6. **Prior state:** bullish `TREND=DOWN`; bearish `TREND=UP`.  7. Formation = signal = K2 completion.
8-11. **Baseline:** entry NEXT_TICK; stop `min(L1,L2)-G_BUFFER` / `max(H1,H2)+G_BUFFER`; 2R.
12. **SRC-PS-COMPLETED entry:** NEXT_TICK after K2 completes.  13. **Stop:** beyond K1's far extreme:
    `L1-G_BUFFER` (bull) / `H1+G_BUFFER` (bear).  14. **Target:** `T_SWING(1.5)`.
15-16. None; none.  17. **Filters:** TF in {H1,H4,D1,W1,MN1} (source: M15 and below "almost never worth
    trading").
18-20. G12; as 17; the identity forces a gap-like open away from K1's close through `LARGE(K1)` and
    `O2>=O1`.
21. Aliases: none.  22. Rare on gold; the system reports `UNKNOWN`, not a win rate, until enough trades.
23. Master row 23; PS `/kicker-pattern`.  24. Open: the source's "approximately equal open" tolerance was
    removed because it contradicted "bodies do not overlap".  25. PROPOSED v1.0.
26. **Deviation notes:** the source's entry "at the open of the second candle" is NOT used here (needs
    unknown K2 information); it lives in the separate EARLY_SETUP pattern P14E.

### P14E KICKER EARLY SETUP (bullish, bearish) — `GT-KICKEREARLY-BULL-v1.0`, `GT-KICKEREARLY-BEAR-v1.0`

New in 0.2. A different pattern with its own counts: it is what the source's entry actually is.

1. IDs as given (BASE-EARLY, SRC-PS-EARLY)  2. Kicker early setup  3. both  4. 1 + opening tick
5. **`SHAPE_DETECTED` = K1 geometry:** K1 bear `LARGE` (bullish) / K1 bull `LARGE` (bearish), logged when K1
   completes. **`BASE_PATTERN_FORMED` = the trigger (0.2.1):** the prior state holds (`TREND(i0-1)=DOWN` bullish,
   `UP` bearish) AND the BID opening price of the next bar satisfies: bullish `bid_open >= O1`; bearish
   `bid_open <= O1`. Then the order executes BUY at the ask / SELL at the bid of that first tick (G10
   `OPEN_TRIGGER`). Nothing about K2's later body or close is required or checked.
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
5. **Shape:** K1 bear `LARGE`; K2 `SMALL` AND `B2<=0.40*B1` AND `O2<=C1+0.10*ATR`; K3 bull `LARGE` AND
   `C3>(O1+C1)/2`.
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. Formation = signal = K3 completion.
8-11. **Baseline:** BUY, stop `min(L1,L2,L3)-G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK after K3.  13. **Stop:** `min(L1,L2)-G_BUFFER` (source offers tight-below-K2 or
    wide-below-K1; the lower of the two lows is used) **[INTERP]**.
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
5. **Shape:** K1 bull `LARGE`; K2 `SMALL` AND `B2<=0.40*B1` AND `O2>=C1-0.10*ATR`; K3 bear `LARGE` AND
   `C3<(O1+C1)/2`.
6. **Prior state:** `TREND(i0-1)=UP`.  7. Formation = signal = K3 completion.
8-11. **Baseline:** SELL, stop `max(H1,H2,H3)+G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK after K3.  13. **Stop:** `max(H1,H2) + G_BUFFER` (ruling A-17: symmetric with the Morning
    Star; the source allows above K2's high or above K1's high for more room, the higher of the two is used) **[INTERP]**.
14. **Targets:** TP1 = `L1`, close **60%**; TP2 = near edge of the nearest live zone below TP1. Both must be
    beyond the actual entry, else `SKIPPED_TARGET_ALREADY_PASSED`.
15-16. None; none.  17. Filters: none required.  18-20. G12; none; gap not required.
21. Abandoned Baby subset.  22. Source H1 example: 30-80 pips (at $0.10 = $3-8).
23. Master row 27; PS `/evening-star` (source 6); TV, SH, CB, GPFX.  24. Open: none beyond [SPEC].
25. PROPOSED v1.0.
26. **Deviation notes:** stop reading; TP2 as nearest zone (source: "next major support", whereas the Morning Star
    source says "next swing high": the TP2 wording difference is kept, ruling A-17).

### P17 THREE WHITE SOLDIERS (bullish) — `GT-3WHITESOLDIERS-BULL-v1.0`

1. GT-3WHITESOLDIERS-BULL-v1.0 (BASE, SRC-PS)  2. Three White Soldiers  3. bullish  4. 3
5. **Shape = pattern:** for k=1..3: bull, `B_k>=0.40*ATR`, `B_k>=0.60*R_k`, `UW_k<=0.25*R_k`; for k=2,3:
   `O_{k-1}<=O_k<=C_{k-1}` and `C_k>C_{k-1}`; `max(B1,B2,B3)<=2.0*min(B1,B2,B3)`. All thresholds [SPEC].
6. **Prior state:** none (sources call it a continuation, classical texts a reversal; both recorded via
   `trend_state`).  7. Formation = K3 completion; signal = K3 (BASE) or the trigger break (SRC-PS).
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
5. **Shape:** bullish: K1 bear `LARGE`; K2 `DOJI` with `H2<=L1-gap_thr`; K3 bull `LARGE` with
   `L3>=H2+gap_thr`. Bearish: K1 bull `LARGE`; K2 `DOJI` with `L2>=H1+gap_thr`; K3 bear `LARGE` with
   `H3<=L2-gap_thr`. True gaps only.
6. **Prior state:** bullish `TREND=DOWN`; bearish `TREND=UP`.  7. Formation = signal = K3 completion.
8-11. **Baseline:** NEXT_TICK after K3; stop = pattern extreme over all three bars (`min(L1..L3)-G_BUFFER`
    bullish / `max(H1..H3)+G_BUFFER` bearish); 2R.
12. **SRC-PS-COMPLETED entry:** NEXT_TICK after K3 completes.  13. **Stop:** `L2-G_BUFFER` (bull) /
    `H2+G_BUFFER` (bear) (source: below the doji's low).  14. **Target:** `T_SWING(1.5)`.
15-16. None; none.  17. Filters: none enforced (RSI, DXY, Fibonacci recorded).
18-20. G12; none; gaps required (that is the identity).  21. Subset of Morning/Evening Star.
22. Source: about 2-4 signals a year on D1 gold; the system reports `UNKNOWN`, not a win rate.
23. Master row 31; PS `/abandoned-baby`.  24. Open: none.  25. PROPOSED v1.0.
26. **Deviation notes:** the source's entry "on the open of the third candle" is in P19E, not here.

### P19E ABANDONED BABY EARLY SETUP (bullish, bearish) — `GT-ABABYEARLY-BULL-v1.0`, `GT-ABABYEARLY-BEAR-v1.0`

New in 0.2, same reasoning as P14E.

1. IDs as given (BASE-EARLY, SRC-PS-EARLY)  2. Abandoned Baby early setup  3. both  4. 2 + opening tick
5. **`SHAPE_DETECTED`** = K1 and K2 geometry: bullish K1 bear `LARGE`, K2 `DOJI` with `H2<=L1-gap_thr`;
   bearish K1 bull `LARGE`, K2 `DOJI` with `L2>=H1+gap_thr`. **`BASE_PATTERN_FORMED` = the trigger (0.2.1):** the
   prior state holds (`TREND(i0-1)=DOWN` bullish / `UP` bearish) AND the BID opening price of K3 satisfies:
   bullish `bid_open >= H2+gap_thr`; bearish `bid_open <= L2-gap_thr`. Then BUY at the ask / SELL at the bid of that
   first tick. K3's size, close and colour are not checked.
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
5. **Shape:** K1 bull `LARGE`; k=2,3,4: bear AND `H_k<=H1` AND `L_k>=L1` AND `B_k<=0.5*B1`; K5 bull `LARGE`
   AND `C5>C1`. Flag: all K2-K4 closes within K1's body (`O1<=C_k<=C1`).
6. **Prior state:** `TREND(i0-1)=UP`.  7. Formation = signal = K5 completion.
8-11. **Baseline:** BUY, stop `min(L1..L5)-G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK after K5.  13. **Stop:** `min(L2,L3,L4)-G_BUFFER`.
14. **Target:** TP1 = `P + 1.272*(H1-L1)`, `P=min(L2..L4)` **[INTERP]** (source names the 1.272 extension but
    not its anchor); TP2 (1.618) OPEN; must be beyond entry and give `>=2R` else `SKIPPED_SRC_RR`.
15-16. None; none.  17. Filters: none enforced (volume decline unusable).  18-20. G12; none; none.
21. None.
22. **Source re-check (2026-09-30):** the Rising page states the middle candles' highs must not exceed K1's
    high and lows must not break K1's low, and "none should close outside the range of the first candle". So
    full high-low containment (this spec) is the source's rule.
23. Master row 38; PS `/rising-three-methods`; INV.  24. Open: Fibonacci anchor.  25. PROPOSED v1.0.
26. **Deviation notes:** Fibonacci anchor invented; TP2 dropped.

### P21 FALLING THREE METHODS (bearish) — `GT-FALLING3-BEAR-v1.0`

1. GT-FALLING3-BEAR-v1.0 (BASE, SRC-PS)  2. Falling Three Methods  3. bearish  4. 5
5. **Shape:** K1 bear `LARGE`; k=2,3,4: bull AND `H_k<=H1` AND `L_k>=L1` AND `B_k<=0.5*B1`; K5 bear `LARGE`
   AND `C5<C1`. Flag: K2-K4 closes within K1's body (`C1<=C_k<=O1`).
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. Formation = signal = K5 completion.
8-11. **Baseline:** SELL, stop `max(H1..H5)+G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK after K5.  13. **Stop:** `max(H2,H3,H4)+G_BUFFER`.
14. **Target:** TP1 = `P - 1.272*(H1-L1)`, `P=max(H2..H4)` **[INTERP]**; must be beyond entry and `>=2R`.
15-16. None; none.
17. **Filters:** **SRC-PS additionally requires the body-close flag** (the Falling page says "none should
    close above the first candle's open, and none should drop below the first candle's close", read here as
    closes); the Rising page does not state the mirror rule.
18-20. G12; none; none.  21. None.
22. **Source re-check:** Falling page also requires full high-low containment ("must remain within the
    high-to-low range of the first large bearish candle"), which is the canonical shape rule.
23. Master row 39; PS `/falling-three-methods`.  24. The Rising/Falling close-rule asymmetry is DELIBERATE: the source texts differ (ruling A-28).
25. PROPOSED v1.0.  26. **Deviation notes:** as P20; close-rule reading.

### P22 INSIDE BAR SAME-BAR SWEEP & RECLAIM (bullish, bearish) — `GT-IBSR-BULL-v1.0`, `GT-IBSR-BEAR-v1.0`

Renamed in 0.2 (was "Inside Bar False Breakout"): it is one specific, objective subtype. A multi-bar false
break (bar 3 closes outside, bar 4 reverses back inside) is not covered and is listed for Wave 1b if the
source supports it.

1. IDs as given (BASE, SRC-CB)  2. Inside Bar Same-Bar Sweep & Reclaim  3. both  4. inside bar + 1..3
5. **Shape:** mother K1, inside K2 (`H2<H1`, `L2>L1`). Then bar `Ck`, `k in {3,4,5}`, is the FIRST bar after K2
   that pierces the mother range (every bar between K2 and `Ck` has `H<=H1` and `L>=L1`). `Ck` pierces exactly
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

### Draft 0.2.2 -> 0.3 rulings (golden-vector findings A-01 ... A-30, reviewer + Claude, 2026-09-30)

| ID | Ruling in Draft 0.3 | Where |
|---|---|---|
| A-01 zone death | Reviewer ruled: dead after a close > 0.10*ATR beyond EITHER edge. **Claude replaced this (ruling E):** role = type of the latest contributing pivot; SUPPORT dies on a close below its bottom, RESISTANCE on a close above its top, scan after that pivot only. Reason: 'either edge' kills every support zone the instant price bounces away from it (shown by the end-to-end vector GV-E2E-02). **Accepted by the reviewer (D-038, RESEARCH APPROVED).** Addendum: a same-candle high+low pivot pair in the latest position gives role AMBIGUOUS (excluded until a later single-type pivot) | G4 |
| A-02 notation | Candles are `K1..K5`; `O1,H1,L1,C1` are numeric fields; `C2close` retired | G-N, all patterns |
| A-03 P08 filters | News/rollover apply to K2 only. **Claude refinement:** the rollover test applies to intraday TFs (M1-H4) only, because every D1/W1/MN1 bar contains the pause by construction. New code `SKIPPED_ROLLOVER` | P08 |
| A-04 straddling zone | Nearest obstacle; near edge at/behind entry -> `SKIPPED_TARGET_ALREADY_PASSED` | G10 |
| A-05 SRC-SH | Base prior state inherited unless a variant replaces it | G8 Layer C, P06 |
| A-06 sessions | Half-open `[start,end)` | G6 |
| A-07 news | Inclusive endpoints | G6 |
| A-08 outside bar | Neutral `OUTSIDE_BAR_SHAPE`; directional pattern only if K2 has a direction | G0b, P08 |
| A-09 inside bar | Neutral `INSIDE_BAR` formation at K2, counted even if expired; `PENDING_BREAKOUT`; **added** `NOT_TRIGGERED_OTHER_SIDE` for the opposite-side breakout | G0b, P09 |
| A-10 tweezer flags | Mirrored 25% flags on both tweezers | P10, P11 |
| A-11 R_TOO_SMALL | Baseline only | G8 |
| A-12 non-qualification | `qualification_failures[]` keeps every failed gate; disposition `NOT_QUALIFIED`; `SKIPPED_TF_NOT_ALLOWED` retired into failure code `TF_NOT_ALLOWED` | G0b |
| A-13 MAX_HOLD | Entry bar = bar 0; next 50 existing completed bars; exit at first tick after bar 50, `exit_across_break` if a closure follows | G8 |
| A-14 swap | Account-spec fields; charge at every rollover crossed; `PENDING_COST_SPEC` when the spec is missing and a rollover was crossed | G9 |
| A-15 inside bar CB level | Bull: mother low at support; bear: mother high at resistance | P09 |
| A-16 T_SWING | BUY: swing highs above entry; SELL: swing lows below | G10 |
| A-17 stars | Symmetric stop (`max(H1,H2)+buffer`); TP2 source wordings kept (swing high vs zone), because the two sources genuinely differ | P16 |
| A-18 stop-entry window | Bar membership; a tick belonging to bar 4 is too late | G10 |
| A-19 precedence | `SKIPPED_TARGET_ALREADY_PASSED` before `SKIPPED_SRC_RR` | G10 |
| A-20 Piercing vs Dark Cloud | Asymmetry kept (sources differ) | P12, P13 |
| A-21 clusters | `formation_cluster_id` and `signal_cluster_id` | G11 |
| A-22 numerics | Integer ticks; exact rationals; no rounding before comparisons | G-N |
| A-23 even median | Mean of the two middle prices | G4 |
| A-24 window edge | Pivot centre inside the 200-bar lookback; left neighbours may lie outside | G3 |
| A-25 entry beyond stop | `SKIPPED_ENTRY_AT_OR_BEYOND_STOP` for every variant | G8 |
| A-26 bars-only | Store BID and ASK bars from ticks; shorts use ASK bars; else `NEEDS_ASK_BARS` | G0, G9 |
| A-27 MAE | Non-negative magnitudes; `mfe_before_mae_h` defined | G8 |
| A-28 Rising/Falling | Asymmetry kept (source text differs) | P20, P21 |
| A-29 P22 code | `NO_SIGNAL_AMBIGUOUS_BOTH_SIDES` in the code list | G0b |
| **A-30 quantisation** | Exact internally; executable levels quantised to tick size: stops away from entry, fixed-R/Fibonacci/measured targets in the profit direction, structural targets toward the entry, triggers in the trigger direction; virtual trade and Vantage mirror share the levels | G13 |

### Still open

1. **Rollover/pause window, swap table, tick size/value, contract specification and server calendar** come from the real Vantage
   demo account (fixtures are used until then).
2. ~~`PIP_SRC_USD`~~ **confirmed 0.10 in 0.3.2 (D-040)**; the ten SRC-PS variants are enabled.
3. **Validation-stage pass/fail rule:** `VALIDATION_RULES.md` v0.3 (D-041, approved) and `tests/validation/`.
4. **Portfolio Simulation rules:** `PORTFOLIO_RULES.md` v0.2 (D-042, approved) and `tests/portfolio/`.
5. **Not enforced in v1:** DXY, volume, RSI/MACD divergence, Fibonacci-location requirements, weekly-trend checks,
   trailing stops, second targets where the split is not given. **Deferred to v1.1:** pullback entries, continuation
   reading of engulfing, strict-gap Piercing/Dark Cloud, automatic role-reversal of zones, multi-bar inside-bar false break.
6. **Multiple testing:** up to about 657 strategies; the untouched validation stage is mandatory.

## 5. Change log

- 0.1 (2026-09-30): first full draft.
- 0.2 (2026-09-30): applies the review above; adds P14E and P19E; renames P22; adds the event model, field 26 and
  the nearest-only target rule.
- 0.2.1 (2026-09-30): applies the six second-pass fixes (section 4); `MAX_HOLD=50` recorded as reviewer-approved.
- 0.2.2 (2026-09-30): applies four third-pass fixes (RAW once per BASE signal, explicit `horizon_end(h)`, bearish
  Kicker gap flag, pip confirmed from source examples).
- 0.3 (2026-09-30): applies the reviewer rulings on golden-vector pack GV-0.1 (A-01..A-29) plus A-30 executable-price
  quantisation; new notation (K1..K5); new event-model codes; pairs of patterns that differ in their sources stay different.
- 0.3.1 (2026-09-30): reviewer accepted Claude's zone-death rule (D-038); wording on role changes made precise (roles change only via a later confirmed pivot); same-candle high/low pivot pair -> role AMBIGUOUS (vector GV-G-ZN-13). Ambiguity phase closed.
- 0.3.2 (2026-09-30): `PIP_SRC_USD = 0.10` confirmed from the sources' own definition and internal consistency (D-040); the ten pip-dependent SRC-PS variants are enabled; `DISABLED_PENDING_PIP_CONFIRMATION` retired.
