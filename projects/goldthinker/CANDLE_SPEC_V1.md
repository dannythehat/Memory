# GoldThinker — Candle Specification v1 (Wave 1) — DRAFT FOR REVIEW

Status: **DRAFT 0.1, 2026-09-30. NOT approved. Nothing is to be coded from this until the owner and the
independent reviewer (ChatGPT) have gone through it line by line.** Author: Claude.

Wave 1 = the 22 patterns marked FULL in `MASTER_CANDLE_LIST.md` (28 direction-specific versions).
The other 19 patterns (10 PARTIAL, 9 NONE) and the ~30 extra TA-Lib patterns are Wave 2+.

**Standard this document must meet:** two independent programs fed the same OHLC (and tick) data must
produce exactly the same yes/no for every rule below. Where this draft had to choose a number the
sources do not give, the item is tagged **[SPEC]** (added by this spec, not from a source) and listed in
section 4 for the reviewer. Where a source is ambiguous and this draft picked an interpretation it is
tagged **[INTERP]**. Every threshold has a constant name so a change is a version bump, never a silent edit.

---

## 1. Global definitions (GLOBALS v1.0)

### G0 Conventions

- Prices are USD per ounce as quoted by the broker. Store `price_distance_usd`, never "pips".
- **Source-pip conversion:** the research sources quote gold "pips". Their numbers only make sense at
  `PIP_SRC_USD = 0.10` **[ASSUMPTION, to be confirmed against the demo account spec]**. Source-plan
  distances are converted as `pips x PIP_SRC_USD`. The original phrase stays in the notes; it never
  drives execution. Changing the constant re-versions every source variant.
- Time is UTC internally. A bar is identified by its open time; it is **complete** at
  `open_time + timeframe duration`. A pattern is **knowable** only when its last bar is complete.
- Timeframes (TF): M1, M5, M15, M30, H1, H4, D1, W1, MN1. Bars are built from the tick stream
  (bid prices, like an MT5 chart), aligned to the Vantage server-time boundaries reported by the demo
  account [TO CONFIRM from the account spec]. No empty bars are created for closed-market intervals.
- Bar indexing: bars of one TF are numbered chronologically. A pattern with n bars is C1..Cn; `p` is
  the index of Cn; `i0` is the index of C1. `t0` = completion time of Cn (= known-at time).
- Candle maths for bar k: `R=H-L`, `B=|C-O|`, `UW=H-max(O,C)`, `LW=min(O,C)-L`. Bull: `C>O`. Bear: `C<O`.
  A bar with `R=0` never takes part in any pattern.
- **Data integrity:** a pattern is evaluated only if all bars in it, and all bars in the ATR/swing/zone
  look-back windows, exist with no unexplained gap (gaps explained by the instrument's published closed
  intervals are allowed and tagged `across_break`). Otherwise `NOT_EVALUATED_DATA_GAP` is logged.

### G1 ATR

`ATR = atr_pre` = simple mean of True Range over the 14 completed bars ending at bar `i0-1`
(`TR = max(H-L, |H-Cprev|, |L-Cprev|)`). Needs at least 15 completed bars before `i0` (else
`NOT_EVALUATED_WARMUP`). The candidate pattern never influences its own ATR.

### G2 Size classes

- `LARGE(k)`: `B>=0.60*ATR` AND `R>=0.80*ATR` AND `B/R>=0.60`. **[SPEC]**
- `SMALL(k)`: `B<=0.25*ATR` AND `R<=0.60*ATR`. **[SPEC]**
- `DOJI(k)`: `B<=0.05*R`.
- `MIN_RANGE_SINGLE`: single-candle patterns also need `R>=0.50*ATR`. **[SPEC]**

### G3 Swings and trend

- Swing high at bar j: `H[j]` strictly greater than the highs of the 2 bars before and the 2 bars after.
  Swing low: mirror with lows. A swing is **confirmed** when bar j+2 is complete.
- `TREND(at i0-1)` uses only swings confirmed by then, from the last 200 bars, on the pattern's own TF.
  Take the last two swing highs (SH1 older, SH2 newer) and last two swing lows (SL1, SL2).
  **UP** if `SH2>=SH1+0.10*ATR` AND `SL2>=SL1+0.10*ATR`. **DOWN** if `SH2<=SH1-0.10*ATR` AND
  `SL2<=SL1-0.10*ATR`. Otherwise **RANGE**. Fewer than two of each: **UNDETERMINED**.
  (Trend flips late by design: it needs confirmed swings.)
- `TREND_HTF`: same rule on the higher TF (M1->M15, M5->H1, M15->H1, M30->H4, H1->H4, H4->D1, D1->W1,
  W1->MN1, MN1->none). **Context only. Never required by any rule in v1.**

### G4 Support / resistance zones

At `i0-1`, over the last 200 completed bars, collect confirmed swing prices. Sort ascending; build
clusters greedily: a cluster starts at the lowest unassigned price `p0` and takes every price
`<= p0+0.25*ATR`. A cluster is a **zone** if it has >=2 pivots and at least one pair of them is >=3 bars
apart. Centre = median price; zone = centre +- `0.125*ATR`.
`AT_SUPPORT` (bullish patterns): distance from the pattern's lowest low to the nearest zone
(0 if inside) `<=0.10*ATR`. `AT_RESISTANCE` (bearish): same with the pattern's highest high.
A zone is dead once a completed bar closes more than `0.10*ATR` beyond its far edge. Role flips are not
modelled in v1. Fibonacci levels and round numbers are **context flags only** in v1
(`ROUND_50`: pattern extreme within `0.10*ATR` of a multiple of $50).

### G5 Gap

`gap_thr = max($0.10, 0.05*ATR)`. Bullish gap between bars a<b: `L_b >= H_a + gap_thr`; bearish:
`H_b <= L_a - gap_thr`. A gap across a closed-market interval is allowed but tagged `across_break`.

### G6 Sessions and news (used by source variants only; always recorded)

- Sessions from local clocks so DST is automatic: ASIA = 09:00-17:00 `Asia/Tokyo`; LONDON = 08:00-17:00
  `Europe/London`; NY = 08:00-17:00 `America/New_York`. `ASIA_ONLY` = in ASIA and in neither LONDON nor NY.
  The session of a signal is the session at its `t0` (for confirmed variants, at the confirmation bar's
  completion). **[SPEC]** (sources give different UTC windows)
- News table `economic_events(time_utc, currency, impact, name)`. `F_NEWS_HIGH`: blocked from T-30 min to
  T+15 min of any high-impact USD event. `F_NEWS_MAJOR`: NFP, CPI, FOMC decision, FOMC press conference
  blocked from T-60 min to T+30 min. **[SPEC]**
- A blocked signal is still detected and logged: `signal_detected=true, trade_eligible=false, reason=...`.

### G7 Indicators (only for filters and context)

`RSI14` = Wilder RSI on closes at the completion of the last pattern bar, needs 100 bars of warm-up.

### G8 Measurement layers (every detection gets all applicable layers)

**Layer A - RAW (no trading assumptions, candle prices only).** Direction `d=+1` for bullish signals,
`-1` for bearish (for Inside Bar / Outside Bar / Inside Bar False Break, `d` is set by the pattern's own
direction rule). Reference price `ref` = open of bar `p+1`. For `h in {1,3,5,10,20}` bars after the
signal (own TF): `ret_h = d*(close[p+h]-ref)` in USD and in ATR units; `MFE_h` = best `d*(extreme-ref)`
(bar high for d=+1, low for d=-1) over those bars; `MAE_h` = worst adverse; `dir_ok_h = ret_h>0`.
If tick data exist also store `mfe_before_mae_h`. A data gap inside the window gives `NULL/DATA_GAP`.

**Layer B - BASELINE (identical mechanics for every pattern).**
- **Entry:** first executable tick with `time >= t0`. BUY fills at ask, SELL at bid. If that tick arrives
  more than 15 minutes after `t0` -> `SKIPPED_STALE_ENTRY` (avoids entering across weekends/rollover).
  **[SPEC]**
- **Stop:** beyond the pattern extreme: bullish = `pattern_low - G_BUFFER`; bearish =
  `pattern_high + G_BUFFER`, where `pattern_low/high` are the lowest low / highest high over all bars of
  the pattern (excluding any confirmation bar) and `G_BUFFER = max($0.20, 0.05*ATR)`. **[SPEC]**
- **Target:** fixed `2R`, `R = |entry_fill - stop|`. No partial exits. No RSI/MACD/DXY/news/session/level
  filters. Skip with `SKIPPED_R_TOO_SMALL` if `R < max(4*spread_at_entry, 0.10*ATR)`. **[SPEC]**
- **Time stop:** if neither stop nor target is hit within `MAX_HOLD = 50` bars of the pattern's TF, close
  at market (`exit_reason=TIME`). **[SPEC]** (so monthly-TF trades are not open for years)
- **Sizing:** `1R = 1% of REF_EQUITY`, `REF_EQUITY = $10,000` **[SPEC]**; lots =
  `risk_usd / (R*contract_size)`, fractional lots allowed in the virtual trade.

**Layer C - SOURCE plan.** Each variant reproduces its source's own confirmation, entry, stop, targets,
partials and filters exactly as written in section 3. Variant ids: `<PATTERN-ID>/SRC-PS`, `/SRC-CB`,
`/SRC-SH` (PS = Pro-Scalper, CB = Candlestick Trading Bible, SH = Shankar notes).
Rule: **where a source names two targets but no split, v1 uses the first target only** and records the
second as OPEN. **Where a source names a structural target but no minimum ratio, v1 requires
`>=1.5R` available** (`G_MIN_REWARD_DEFAULT`), else `SKIPPED_SRC_RR`. **[SPEC]**

### G9 Fills, ordering and costs

- Long: stop triggers at the first tick with `bid <= stop`, fill = that tick's bid. Target: first tick
  with `bid >= target`, fill = target price. Short: stop when `ask >= stop`, fill = that tick's ask;
  target when `ask <= target`, fill = target price. Gap-through-stop fills at the first tick price.
- Tick order decides which of stop/target came first. If tick data are missing:
  score **STOP FIRST**, tag `resolution=CONSERVATIVE_STOP_FIRST`, and also report a target-first
  sensitivity figure. Ambiguous trades are never deleted.
- Result in R = `(exit-entry)*d/R` minus swap and commission converted to R. Swap/commission come from
  the account spec at the time. Spread is already inside the fills.

### G10 Entry mechanics used by source variants

- `NEXT_TICK`: as in Layer B, at `t0`.
- `CONFIRM_CLOSE`: a confirmation test is evaluated on the **immediately following completed bar**
  (`p+1`) unless the pattern says otherwise; on success entry = first executable tick after that bar
  completes. On failure: `EXPIRED_NO_CONFIRMATION`. Maximum allowed extension where a source permits
  later confirmation: 3 further bars (`G_CONFIRM_MAX=3`). **[SPEC]** Confirmations that a source words as
  "opens with momentum" are replaced by a close-based test (**[INTERP]**).
- `STOP_ENTRY(trigger)`: armed at `t0`; long fills when ask `>= trigger`, short when bid `<= trigger`,
  within the next 3 completed bars; cancelled if price first reaches the stop level
  (`INVALIDATED_BEFORE_ENTRY`); else `EXPIRED`. **[SPEC]**
- `OPEN_TRIGGER`: fires on the first executable tick of bar `p+1` if a stated opening condition holds.
- Targets: `T_SR(k)` = near edge of the nearest live zone (G4) beyond the entry whose distance is
  `>=k*R`; `T_SWING(k)` = nearest confirmed swing pivot beyond entry with distance `>=k*R`;
  none found -> `SKIPPED_SRC_NO_TARGET`. Conservative pullback entries named in the sources
  (50% retrace etc.) are **deferred to v1.1**, not part of Wave 1.

### G11 Identity, versions, overlaps

- Ids: `GT-<PATTERN>-<BULL|BEAR>-v1.0`, variants `.../BASE`, `.../SRC-PS` etc. Changing any rule or
  constant creates a new version with a new sample; old results stay attached to the old version.
- Overlapping identities are allowed and all logged. Detections completing on the same bar, same TF and
  same direction share a `cluster_id` so correlated results are shown as correlated.
- Every result belongs to one `(pattern-side x TF x variant x version)` and is **never pooled** across
  TFs or variants. Size of the experiment: about 28 sides x 9 TFs = 252 baseline strategies plus about
  37 source-variant sides x up to 9 TFs = at most about 333 more, so up to about 585 strategies. Survivors
  must clear the untouched validation stage before any real money.

### G12 Context recorded for every detection (never required unless a variant says so)

`trend_state`, `trend_state_htf`, `at_support`/`at_resistance` and distance to nearest zone, `rsi14`,
`atr_pre`, spread at signal, session flags, `news_flags`, `round_50`, `across_break`, weekday and hour,
size ratios of the pattern bars, `cluster_id`.

---

## 2. Test-vector requirement

Before any code: for each pattern the reviewer supplies (or approves) **golden test vectors** - small OHLC
sequences with the expected yes/no and expected entry/stop/target - so an implementation can be checked
against them. Worked examples below are illustrative only and are themselves part of the review.

---

## 3. Wave-1 pattern specifications

Field numbering follows the agreed 25-field schema. "G" references point to section 1. Every
"FINAL ACCEPTED RULE" reads **PROPOSED v1.0** until approved.

### P01 HAMMER (bullish) — `GT-HAMMER-BULL-v1.0`

1. **ID/version:** GT-HAMMER-BULL-v1.0 (BASE, SRC-PS)
2. **Name:** Hammer  3. **Side:** bullish  4. **Candles:** 1
5. **Geometry (C1):** `R>=0.50*ATR` AND `LW>=2.0*B` AND `UW<=0.10*R` AND `min(O,C)>=L+0.65*R`.
6. **Prior state:** `TREND(i0-1)=DOWN`.
7. **Knowable:** completion of C1.
8. **Invalidation:** baseline - G8 skip rules. SRC-PS - confirmation fails/expires.
9-11. **Baseline:** entry NEXT_TICK BUY; stop `L1-G_BUFFER`; target 2R.
12. **SRC-PS entry:** after confirmation (CONFIRM_CLOSE) BUY at first executable tick.
13. **SRC-PS stop:** `L1 - 17.5*PIP_SRC_USD` (source "15-20 pip buffer", midpoint).
14. **SRC-PS targets:** single target `2R` (source "2:1 minimum"). No partials.
15. **Confirmation:** C2 is bullish AND `C2close > H1`. **[INTERP]** (source: "next candle shows initial
    bullish momentum"; other sources say "closes above the hammer high").
16. **Expiry:** C2 only.
17. **Source filters:** prior state relaxed to `DOWN OR AT_SUPPORT`. Nothing else.
18. **Context recorded:** G12; upper wick ratio; body position.
19. **Session/news:** SRC-PS none stated (record only).
20. **Gap:** none.
21. **Aliases:** subset of Pin Bar (bull) and overlaps Dragonfly when body is tiny. Hanging Man has the same
    shape after an uptrend (not Wave 1).
22. **Edge cases:** `B=0` allowed (then also a dragonfly candidate). Example: `O=4200.00 H=4200.50
    L=4194.00 C=4200.20`, ATR 4.0: `R=6.5>=2.0`, `B=0.20`, `LW=6.0>=0.4`, `UW=0.30<=0.65`,
    `min(O,C)=4200.00>=4194+4.225=4198.225` -> YES (if trend DOWN).
23. **Sources:** master row 1; PS `/hammer-candlestick` (source 9); TV, SA, SH, CB.
24. **Open disagreements:** body "upper third" vs "upper 40%" (this spec: upper 35%); `MIN_RANGE_SINGLE`
    and `2.0/0.10` thresholds are [SPEC]; confirmation wording.
25. **FINAL ACCEPTED RULE:** PROPOSED v1.0 = fields 5+6+7.

### P02 SHOOTING STAR (bearish) — `GT-SHOOTINGSTAR-BEAR-v1.0`

1. GT-SHOOTINGSTAR-BEAR-v1.0 (BASE, SRC-PS)  2. Shooting Star  3. bearish  4. 1
5. **Geometry:** `R>=0.50*ATR` AND `UW>=2.0*B` AND `LW<=0.10*R` AND `max(O,C)<=H-0.65*R`.
6. **Prior state:** `TREND(i0-1)=UP`.  7. Knowable at C1 completion.
8. Baseline skips per G8; SRC-PS confirmation fails/expires.
9-11. **Baseline:** SELL at bid; stop `H1+G_BUFFER`; target 2R.
12. **SRC-PS entry:** CONFIRM_CLOSE, SELL at first executable tick.
13. **Stop:** `H1 + 20*PIP_SRC_USD` (source "15-25 pips").
14. **Targets:** `T_SWING(1.5)` = nearest confirmed swing low below entry with reward `>=1.5R`; source's second
    target ("rally origin") is OPEN; no partials (split not given).
15. **Confirmation:** C2 bearish AND `C2close < min(O1,C1)` (source: "next candle opens bearishly OR closes
    bearish below the star body" - close version adopted). **[INTERP]**
16. **Expiry:** C2 only.
17. **Filters:** `F_SESSION`: skip if `ASIA_ONLY` (source: reduced size or skipped). **[INTERP]**
    Prior state relaxed to `UP OR AT_RESISTANCE`.
18-20. Context per G12; none; none.
21. **Aliases:** subset of Pin Bar (bear); overlaps Gravestone when body tiny.
22. **Edge case:** red body preferred by source but not required.
23. Master row 4; PS `/shooting-star` (source 10); TV, SH, CB.
24. **Open:** second target; "reduced sizing" replaced by skip.
25. PROPOSED v1.0.

### P03 PIN BAR (bullish and bearish) — `GT-PINBAR-BULL-v1.0`, `GT-PINBAR-BEAR-v1.0`

1. IDs as given; variants BASE, SRC-PS, SRC-CB.  2. Pin Bar  3. both  4. 1
5. **Geometry:** `R>=0.50*ATR`, `B<=0.33*R`, dominant wick `>=0.66*R`, opposite wick `<=0.10*R`.
   Bullish = dominant wick is the lower one and `C>=L+0.75*R`. Bearish = dominant wick is the upper one and
   `C<=H-0.75*R`.
6. **Prior state:** none (context recorded). This is a deliberate difference from Hammer/Shooting Star.
7. Knowable at C1 completion.
8. Baseline per G8; variants per their own filters.
9-11. **Baseline:** bullish BUY, stop `L1-G_BUFFER`; bearish SELL, stop `H1+G_BUFFER`; target 2R.
12. **SRC-PS entry:** NEXT_TICK (aggressive). **SRC-CB entry:** NEXT_TICK ("immediately after the pin bar
    closes").
13. **SRC-PS stop:** wick tip `+-12.5*PIP_SRC_USD` (source 10-15 pips). **SRC-CB stop:** wick tip `+-G_BUFFER`
    (source: "beyond the tail", no number). **[INTERP]**
14. **Targets:** SRC-PS `T_SWING(2.0)` (source: at least 1:2); second target (measured move = pin range) OPEN.
    SRC-CB `T_SR(2.0)` (source: next level, minimum 2:1).
15-16. **Confirmation:** none, none.
17. **Filters:** SRC-PS requires `AT_SUPPORT` (bull) / `AT_RESISTANCE` (bear) and skips `ASIA_ONLY`.
    SRC-CB requires pin direction WITH the trend (bull needs `TREND=UP`, bear needs `TREND=DOWN`) AND
    `AT_SUPPORT/AT_RESISTANCE`; runs only on TF in {H1, H4, D1}.
18. Context: wick ratios, distance to zone.
19. Session/news: SRC-PS `ASIA_ONLY` skip; nothing else.
20. Gap: none.
21. **Aliases:** bull pin bar contains Hammer / Dragonfly cases; bear contains Shooting Star / Gravestone.
    "Body inside prior candle's range" (PS) is not part of identity.
22. **Edge case:** `B=0` allowed; same candle may qualify as Hammer, Dragonfly and Pin Bar simultaneously
    (three detections, one `cluster_id`).
23. Master row 5; PS `/pin-bar` (source 12); CB source 15.
24. **Open:** CB says pin bars on 5-minute "lose money"; this spec still runs them (owner chose all TFs).
    `T_SWING` vs `T_SR` choice differs between sources.
25. PROPOSED v1.0.

### P04 DRAGONFLY DOJI (bullish) — `GT-DRAGONFLY-BULL-v1.0`

1. GT-DRAGONFLY-BULL-v1.0 (BASE, SRC-PS)  2. Dragonfly Doji  3. bullish  4. 1
5. **Geometry:** `DOJI` (`B<=0.05R`) AND `UW<=0.05*R` AND `LW>=0.80*R` (implied by the first two: `LW>=0.90R`)
   AND `R>=0.50*ATR`.
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. Knowable at C1 completion.
8. Baseline per G8; SRC-PS confirmation fails if C2 is bearish or a doji.
9-11. **Baseline:** BUY, stop `L1-G_BUFFER`, 2R.
12. **SRC-PS entry:** CONFIRM_CLOSE BUY.  13. **Stop:** `L1 - 10*PIP_SRC_USD` (source 5-15 pips).
14. **Target:** `T_SR(1.5)` (source: minimum 1:1.5; 1:2-1:3 at major support). No partials.
15. **Confirmation:** C2 bullish AND `C2close > max(O1,C1)`.  16. Expiry: C2 only.
17. **Filters:** `AT_SUPPORT` required; skip `ASIA_ONLY`; `F_NEWS_MAJOR`.
18-20. Context per G12; session/news as in 17; no gap.
21. Aliases: subset of Bull Pin Bar; overlaps Hammer.
22. Edge: exact `O=C=H` is not required (too strict); the 5% tolerances are [SPEC].
23. Master row 8; PS `/dragonfly-doji`; SH, CB.
24. Open: source "H4/D1 far more meaningful" recorded, not restricted.
25. PROPOSED v1.0.

### P05 GRAVESTONE DOJI (bearish) — `GT-GRAVESTONE-BEAR-v1.0`

1. GT-GRAVESTONE-BEAR-v1.0 (BASE, SRC-PS)  2. Gravestone Doji  3. bearish  4. 1
5. **Geometry:** `DOJI` AND `LW<=0.05*R` AND `UW>=0.80*R` AND `R>=0.50*ATR`.
6. **Prior state:** `TREND(i0-1)=UP`.  7. At C1 completion.
8. As P04.
9-11. **Baseline:** SELL, stop `H1+G_BUFFER`, 2R.
12. **SRC-PS entry:** CONFIRM_CLOSE SELL (source: enter at the open following the confirmation close).
13. **Stop:** `H1 + 10*PIP_SRC_USD`.  14. **Target:** `T_SR(1.5)`; no partials.
15. **Confirmation:** C2 closes below `min(O1,C1)`; fails if C2 closes above it.  16. C2 only.
17. **Filters:** `AT_RESISTANCE` required. No session or timeframe rule in the source.
18-20. Context per G12; none; none.
21. Aliases: subset of Bear Pin Bar; overlaps Shooting Star.
22. Edge: differs from Shooting Star only by near-zero body.
23. Master row 9; PS `/gravestone-doji`; SH, CB.
24. Open: none beyond [SPEC] tolerances.
25. PROPOSED v1.0.

### P06 BULLISH ENGULFING — `GT-ENGULF-BULL-v1.0`

1. GT-ENGULF-BULL-v1.0 (BASE, SRC-PS, SRC-CB, SRC-SH)  2. Bullish Engulfing  3. bullish  4. 2
5. **Geometry:** C1 bear, C2 bull, `O2<=C1`, `C2>=O1`, `B2>B1`, `B1>0.05*R1` (C1 not a doji).
   Quality flags (recorded, not required): `B2>=2*B1`; wicks also engulfed (`L2<=L1` and `H2>=H1`).
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. At C2 completion.
8. Baseline per G8. SRC-SH: fails if RSI condition false.
9-11. **Baseline:** BUY, stop `min(L1,L2)-G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK (engulfing close).  13. **Stop:** `min(L1,L2) - 20*PIP_SRC_USD`.
14. **Targets:** `T_SR(1.5)`; second target (3R) OPEN (no split given).
15-16. Confirmation: none, none.
17. **Filters:** SRC-PS prior state relaxed to `DOWN OR AT_SUPPORT`. **SRC-CB:** requires `TREND=DOWN`... the
    book also allows engulfing WITH the trend as continuation - **not modelled in v1** - plus `AT_SUPPORT`,
    TF in {H1,H4,D1}, entry NEXT_TICK, stop `min(L1,L2)-G_BUFFER`, target `T_SR(2.0)`.
    **SRC-SH:** identity tightened to wicks engulfed (`L2<=L1`, `H2>=H1`) AND `RSI14(C2)<30`; entry
    NEXT_TICK; stop/target = BASELINE (source gives none).
18. Context: size ratio, wick engulf flag, RSI14.  19. Session/news: SRC-PS none.
20. Gap: none.  21. Aliases: Outside Bar (when wicks engulfed too).  Piercing Line is disjoint
    (`C2<=O1` there is not enough to be engulfing).
22. **Edge cases:** SH's own text asks for both "enter at the close of the engulfing candle" and "third
    candle confirms" - v1 uses only the entry-at-close reading. Example: C1 `O=4210 C=4204 R1=7 (H4211 L4203)`;
    C2 `O=4203.5 C=4212 H4212.5 L4203`: `O2=4203.5<=4204`, `C2=4212>=4210`, `B2=8.5>B1=6` -> YES.
23. Master row 13; PS `/bullish-engulfing` (source 7); SH (source 4); CB (source 15); TV, SA.
24. **Open:** trend-context vs at-support alternative; SH internal conflict; DXY/Fibonacci not enforced.
25. PROPOSED v1.0.

### P07 BEARISH ENGULFING — `GT-ENGULF-BEAR-v1.0`

1. GT-ENGULF-BEAR-v1.0 (BASE, SRC-PS, SRC-CB)  2. Bearish Engulfing  3. bearish  4. 2
5. **Geometry:** C1 bull, C2 bear, `O2>=C1`, `C2<=O1`, `B2>B1`, `B1>0.05*R1`.
6. **Prior state:** `TREND(i0-1)=UP`.  7. At C2 completion.
8. Baseline per G8.
9-11. **Baseline:** SELL, stop `max(H1,H2)+G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK.  13. **Stop:** `max(H1,H2) + 20*PIP_SRC_USD`.
14. **Targets:** `T_SR(1.5)`; second target (candle height projected, ~3R) OPEN.
15-16. None, none.
17. **Filters:** SRC-PS: prior state `UP OR AT_RESISTANCE`; skip `ASIA_ONLY`. DXY and RSI-divergence rules in
    the source are **not enforced** (no DXY feed in v1; recorded as unavailable). SRC-CB mirrors P06 SRC-CB.
18-20. Context per G12; session as in 17; no gap.
21. Aliases: Outside Bar when wicks also engulfed.
22. Edge: same as P06.
23. Master row 14; PS `/bearish-engulfing` (source 8); CB.
24. Open: DXY filter unavailable; Fibonacci-extension location recorded only.
25. PROPOSED v1.0.

### P08 OUTSIDE BAR (bullish and bearish) — `GT-OUTSIDE-BULL-v1.0`, `GT-OUTSIDE-BEAR-v1.0`

1. IDs as given (BASE, SRC-PS)  2. Outside Bar  3. both  4. 2
5. **Geometry:** `H2>H1` AND `L2<L1` (strict). Direction: bullish if `C2>O2`, bearish if `C2<O2`; `C2=O2` gives
   no signal. Quality flag: `R2>=1.5*ATR` (recorded).
6. **Prior state:** none.  7. At C2 completion.
8. Baseline per G8; SRC-PS see 17.
9-11. **Baseline:** bullish BUY, stop `L2-G_BUFFER`; bearish SELL, stop `H2+G_BUFFER`; 2R.
12. **SRC-PS entry:** NEXT_TICK.  13. **Stop:** `L2-G_BUFFER` / `H2+G_BUFFER` (source gives no buffer). **[INTERP]**
14. **Target:** `T_SR(1.5)` (source: next level, 1:1.5 to 1:2 minimum).
15-16. None; none (the close direction is the built-in confirmation).
17. **Filters:** SRC-PS requires `R2>=1.5*ATR`; skips signals whose bar contained a high-impact USD event
    (source: wait 1-2 candles after news spikes) **[INTERP]**; skips bars overlapping the daily rollover pause.
18-20. Context per G12; as in 17; none.
21. Aliases: Engulfing (Outside Bar is stricter).
22. Edge: the size filter is a quality flag in BASE, a requirement in SRC-PS (source treats it as a filter).
23. Master row 15; PS `/outside-bar`.
24. Open: news delay replaced by skip.
25. PROPOSED v1.0.

### P09 INSIDE BAR BREAKOUT (bullish and bearish) — `GT-INSIDE-BULL-v1.0`, `GT-INSIDE-BEAR-v1.0`

1. IDs as given (BASE, SRC-PS, SRC-CB)  2. Inside Bar (breakout)  3. both  4. 2 + breakout bar
5. **Geometry:** mother C1, inside C2 with `H2<H1` AND `L2>L1` (strict). **Signal bar** `Cb`: the first bar
   among the next three (`b=3,4,5`) whose CLOSE is outside the mother range: `Cb>H1` = bullish, `Cb<L1` =
   bearish. No signal if none within 3 bars (`EXPIRED`). Compression `R2/R1` recorded (30-50% = strong).
6. **Prior state:** none.  7. **Knowable at completion of `Cb`.**
8. Baseline per G8.
9-11. **Baseline:** entry NEXT_TICK after `Cb`; stop = opposite side of mother, `L1-G_BUFFER` (bull) /
    `H1+G_BUFFER` (bear); target 2R. (`pattern_low/high` here = the mother range.)
12. **SRC-PS entry:** NEXT_TICK after `Cb` (the source both says "buy stop 2-5 pips above" and "wait for a
    close outside"; the close-based reading is adopted). **[INTERP]**
13. **Stop:** opposite side of mother `+-3.5*PIP_SRC_USD` (source 2-5 pips).
14. **Target:** `T_SR(1.5)` (source: at least 1:1.5, ideally 1:2).
15. **Confirmation:** the breakout close itself.  16. Expiry: 3 bars after C2.
17. **Filters:** SRC-PS: TF in {H1,H4,D1,W1,MN1}; skip `ASIA_ONLY`; `F_NEWS_MAJOR`. **SRC-CB:** breakout WITH
    the trend (bull needs `TREND=UP`, bear needs `TREND=DOWN`), AND the mother bar `AT_SUPPORT/AT_RESISTANCE`,
    TF in {H4,D1}; stop opposite side of mother `+-G_BUFFER`; target `T_SR(2.0)`.
18-20. Context: nested inside bars count, compression ratio; as in 17; none.
21. Aliases: none (Harami not modelled as a separate Wave-1 pattern).
22. **Edge cases:** a bar that pokes outside the mother range but closes inside is NOT a breakout: it stays
    armed until expiry (and may be an Inside Bar False Break, P22).
23. Master row 16; PS `/inside-bar`; CB; TV, SH.
24. **Open:** entry-order vs close-based reading; TF limits differ by source.
25. PROPOSED v1.0.

### P10 TWEEZER TOP (bearish) — `GT-TWEEZERTOP-BEAR-v1.0`

1. GT-TWEEZERTOP-BEAR-v1.0 (BASE, SRC-PS)  2. Tweezer Top  3. bearish  4. 2
5. **Geometry:** C1 bull, C2 bear, `|H1-H2|<=tol` with `tol=max(3*PIP_SRC_USD, 0.05*ATR)`.
   Quality flag: `C2close<=(O1+C1)/2`.
6. **Prior state:** `TREND(i0-1)=UP`.  7. At C2 completion.
8. Baseline per G8; SRC-PS: entry expires.
9-11. **Baseline:** SELL, stop `max(H1,H2)+G_BUFFER`, 2R.
12. **SRC-PS entry:** `STOP_ENTRY(trigger = L2)` SELL (source: "below the low of the second candle").
    **[INTERP]** (source also allows "open of the third candle").
13. **Stop:** `max(H1,H2) + 3*PIP_SRC_USD`.  14. **Target:** `T_SR(1.5)` (source: nearest support; ratio not given).
15. **Confirmation:** the trigger break.  16. Expiry: 3 bars after C2.
17. **Filters:** `AT_RESISTANCE` required; skip `ASIA_ONLY`.
18-20. Context per G12; as in 17; none.
21. Aliases: Bearish Engulfing / Dark Cloud can share a bar.
22. Edge: the tolerance is in dollars, not source pips, and grows with ATR.
23. Master row 19; PS `/tweezer-top`; CB, SH (weak).
24. Open: `tol`, 3-bar trigger expiry, and the trigger-break entry are [SPEC]/[INTERP].
25. PROPOSED v1.0.

### P11 TWEEZER BOTTOM (bullish) — `GT-TWEEZERBOTTOM-BULL-v1.0`

1. GT-TWEEZERBOTTOM-BULL-v1.0 (BASE, SRC-PS)  2. Tweezer Bottom  3. bullish  4. 2
5. **Geometry:** C1 bear, C2 bull, `|L1-L2|<=tol` (`tol` as P10). Quality flags: C1 closes in its lowest 25%,
   C2 closes in its highest 25%.
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. At C2 completion.
8-11. **Baseline:** BUY, stop `min(L1,L2)-G_BUFFER`, 2R.
12. **SRC-PS entry:** `STOP_ENTRY(trigger = H2)` BUY.  13. **Stop:** `min(L1,L2) - 3*PIP_SRC_USD`.
14. **Target:** `T_SWING(1.5)` (source: prior swing high above).
15. Confirmation: the trigger break.  16. Expiry: 3 bars.
17. **Filters:** `AT_SUPPORT` required. Source's volume-divergence confirmation is not usable (tick volume only)
    - recorded only.
18-20. Context per G12; none; none.
21. Aliases: Bullish Engulfing can share a bar.  22. As P10.
23. Master row 20; PS `/tweezer-bottom`.  24. As P10.  25. PROPOSED v1.0.

### P12 PIERCING LINE (bullish) — `GT-PIERCING-BULL-v1.0`

1. GT-PIERCING-BULL-v1.0 (BASE, SRC-PS)  2. Piercing Line  3. bullish  4. 2
5. **Geometry:** C1 bear AND `LARGE(C1)`; C2 bull; `O2<C1`; `C2>(O1+C1)/2`; `C2<=O1` (so it does not engulf).
   Quality flags: `O2<=L1-gap_thr` (true gap, `gap_flag`); penetration tier (50-60 / 75 / 90+ %).
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. At C2 completion.
8-11. **Baseline:** BUY, stop `L2-G_BUFFER`? No - baseline uses the pattern extreme `min(L1,L2)-G_BUFFER`; 2R.
12. **SRC-PS entry:** NEXT_TICK after C2.  13. **Stop:** `L2 - G_BUFFER` (source: below C2's low, not C1's).
14. **Target:** `T_SR(2.0)` (source: minimum 1:2 required before entry); second target (measured move) OPEN.
15-16. None; none.
17. **Filters:** `AT_SUPPORT` required; skip signals wholly inside `ASIA_ONLY`.
18-20. Context: penetration %, `gap_flag`; as in 17. **Gap:** not required. A strict classical-gap variant
    would be a separately named version.
21. Aliases: disjoint from Bullish Engulfing by the `C2<=O1` clause.
22. Edge: source says "gap down strengthens" - recorded, not required.
23. Master row 21; PS `/piercing-line`; SA, SH.
24. Open: "opens below C1 close" is barely a gap on gold - this is the source's own rule.
25. PROPOSED v1.0.

### P13 DARK CLOUD COVER (bearish) — `GT-DARKCLOUD-BEAR-v1.0`

1. GT-DARKCLOUD-BEAR-v1.0 (BASE, SRC-PS)  2. Dark Cloud Cover  3. bearish  4. 2
5. **Geometry:** C1 bull AND `LARGE(C1)`; C2 bear; `O2>C1`; `C2<(O1+C1)/2`; `C2>=O1`.
6. **Prior state:** `TREND(i0-1)=UP`.  7. At C2 completion.
8-11. **Baseline:** SELL, stop `max(H1,H2)+G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK.  13. **Stop:** `H2 + G_BUFFER` (source: above C2's high).
14. **Target:** `T_SR(1.5)`; source's "scale out half, trail the rest" is OPEN (trail not defined).
15-16. None; none.  17. **Filters:** `AT_RESISTANCE` required.
18-20. Context per G12; none; **Gap:** source says "gap required" but defines it as `O2>C1` - that is the rule.
21. Aliases: disjoint from Bearish Engulfing (`C2>=O1`).  22. As P12 mirrored.
23. Master row 22; PS `/dark-cloud-cover`; SH.  24. Open: trailing.  25. PROPOSED v1.0.

### P14 KICKER (bullish and bearish) — `GT-KICKER-BULL-v1.0`, `GT-KICKER-BEAR-v1.0`

1. IDs as given (BASE, SRC-PS)  2. Kicker  3. both  4. 2
5. **Geometry (bullish):** C1 bear AND `LARGE(C1)`; C2 bull AND `LARGE(C2)`; `O2>=O1-0.10*ATR`;
   `C2>=H2-0.10*R2`. **Bearish:** C1 bull LARGE; C2 bear LARGE; `O2<=O1+0.10*ATR`; `C2<=L2+0.10*R2`.
   (C2 opens at or beyond C1's open, so its body does not overlap C1's body.)
6. **Prior state:** bullish `TREND=DOWN`; bearish `TREND=UP`.  7. At C2 completion.
8-11. **Baseline:** BUY/SELL after C2; stop `min(L1,L2)-G_BUFFER` (bull) / `max(H1,H2)+G_BUFFER` (bear); 2R.
12. **SRC-PS entry:** `OPEN_TRIGGER` at the first executable tick of C2: bullish fires if
    `ask >= O1-0.10*ATR` while C1 is bear-LARGE and `TREND=DOWN` (mirror for bearish). This needs only C1 and
    the opening tick, so it has no look-ahead. **[INTERP]** (source: "enter at the open of the second candle")
13. **Stop:** beyond C1's far extreme: bullish `L1-G_BUFFER`; bearish `H1+G_BUFFER`.
14. **Target:** `T_SWING(1.5)` (source: prior swing).
15-16. None; none.
17. **Filters:** TF in {H1,H4,D1,W1,MN1} (source: M15 and below "almost never worth trading").
18-20. Context: `across_break` and `gap_flag` are recorded; **Gap:** identity needs no separate gap test because
    `LARGE(C1)` plus `O2>=O1-0.10*ATR` already forces C2's open away from C1's close.
21. Aliases: none.  22. Edge: with `OPEN_TRIGGER` the SRC-PS trade can exist where the completed pattern never
    forms (C2 reverses). Both facts are recorded.
23. Master row 23; PS `/kicker-pattern`.  24. Open: the whole entry reading is [INTERP].  25. PROPOSED v1.0.

### P15 MORNING STAR (bullish) — `GT-MORNINGSTAR-BULL-v1.0`

1. GT-MORNINGSTAR-BULL-v1.0 (BASE, SRC-PS)  2. Morning Star  3. bullish  4. 3
5. **Geometry:** C1 bear `LARGE`; C2 `SMALL` (any colour) AND `B2<=0.40*B1` AND `O2<=C1+0.10*ATR`;
   C3 bull `LARGE` AND `C3>(O1+C1)/2`.
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. At C3 completion.
8-11. **Baseline:** BUY, stop `min(L1,L2,L3)-G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK after C3.  13. **Stop:** `min(L1,L2)-G_BUFFER` (source offers tight-below-C2
    or wide-below-C1; the lower of the two lows is used so the stop is never inside the pattern). **[INTERP]**
14. **Targets:** TP1 = `H1`, close **60%**; TP2 = nearest confirmed swing high above TP1 (remaining 40%; if none,
    the remainder runs to stop/time stop). Stop not moved.
15-16. None; none.  17. **Filters:** none required. RSI<30 and support/Fibonacci location recorded only.
18-20. Context per G12 plus star gap flag (`max(O2,C2)<C1`); none; gap not required.
21. Aliases: Abandoned Baby is a subset variant with true gaps.
22. Edge: the star-opening rule `O2<=C1+0.10*ATR` is symmetrical with Evening Star and comes from SH/PS-evening
    wording (PS morning star gives no position rule). [SPEC]
23. Master row 25; PS `/morning-star`; TV, SH, SA, CB, GPFX.  24. Open: star position rule.
25. PROPOSED v1.0.

### P16 EVENING STAR (bearish) — `GT-EVENINGSTAR-BEAR-v1.0`

1. GT-EVENINGSTAR-BEAR-v1.0 (BASE, SRC-PS)  2. Evening Star  3. bearish  4. 3
5. **Geometry:** C1 bull `LARGE`; C2 `SMALL` AND `B2<=0.40*B1` AND `O2>=C1-0.10*ATR`; C3 bear `LARGE` AND
   `C3<(O1+C1)/2`.
6. **Prior state:** `TREND(i0-1)=UP`.  7. At C3 completion.
8-11. **Baseline:** SELL, stop `max(H1,H2,H3)+G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK after C3 (source: "at market on the open following C3's close").
13. **Stop:** `H2 + G_BUFFER` (source: just above C2's high).
14. **Targets:** TP1 = `L1`, close **60%**; TP2 = near edge of the nearest live zone below TP1 (`T_SR` with no
    minimum). Stop not moved.
15-16. None; none.  17. **Filters:** none required.  18-20. Context per G12; none; gap not required.
21. Aliases: Abandoned Baby subset.  22. Example is the source's own (H1: 30-80 pips).
23. Master row 27; PS `/evening-star` (source 6); TV, SH, CB, GPFX.  24. Open: none beyond [SPEC].
25. PROPOSED v1.0.

### P17 THREE WHITE SOLDIERS (bullish) — `GT-3WHITESOLDIERS-BULL-v1.0`

1. GT-3WHITESOLDIERS-BULL-v1.0 (BASE, SRC-PS)  2. Three White Soldiers  3. bullish  4. 3
5. **Geometry:** for k=1..3: bull, `B_k>=0.40*ATR`, `B_k>=0.60*R_k`, `UW_k<=0.25*R_k`; for k=2,3:
   `O_{k-1}<=O_k<=C_{k-1}` (opens inside the prior body) and `C_k>C_{k-1}`; and
   `max(B1,B2,B3)<=2.0*min(B1,B2,B3)` (similar size). All thresholds [SPEC]; the sources give none.
6. **Prior state:** none. The sources call it a continuation after a breakout/support hold; classical texts call
   it a reversal after a decline. Both are recorded via `trend_state`; neither is required.
7. At C3 completion.
8-11. **Baseline:** BUY, stop `min(L1..L3)-G_BUFFER`, 2R.
12. **SRC-PS entry:** `STOP_ENTRY(trigger = H3)` BUY (breakout above C3's high). **[INTERP]**
13. **Stop:** `L3 - G_BUFFER` (source: below C3's low for pullback entry; breakout-entry stop is undefined).
    **[INTERP]**
14. **Target:** measured move `H3 + (max(H1..H3)-min(L1..L3))`; source's 50% scale-out is OPEN (only one target
    named).
15-16. Confirmation: the trigger break; expiry 3 bars.
17. **Filters:** none enforced. RSI>75-80 caution, "resistance within 50 pips ($5)" and bull/bear-market context
    are recorded only.
18-20. Context per G12; none; none.
21. Aliases: Marubozu-like bodies possible.
22. Edge: a run of 15-20 prior candles is "weakest" per source - recorded as `bars_since_swing_low`.
23. Master row 29; PS `/three-white-soldiers`; SH.  24. Open: numeric similarity; continuation vs reversal.
25. PROPOSED v1.0.

### P18 THREE BLACK CROWS (bearish) — `GT-3BLACKCROWS-BEAR-v1.0`

1. GT-3BLACKCROWS-BEAR-v1.0 (BASE, SRC-PS)  2. Three Black Crows  3. bearish  4. 3
5. **Geometry:** mirror of P17: bear, `B_k>=0.40*ATR`, `B_k>=0.60*R_k`, `LW_k<=0.25*R_k`; for k=2,3
   `C_{k-1}<=O_k<=O_{k-1}` and `C_k<C_{k-1}`; similar-size clause.
6. Prior state: none (recorded).  7. At C3 completion.
8-11. **Baseline:** SELL, stop `max(H1..H3)+G_BUFFER`, 2R.
12. **SRC-PS entry:** `STOP_ENTRY(trigger = L3)` SELL (breakdown entry). **[INTERP]** (retracement entry
    is deferred to v1.1).
13. **Stop:** `H3 + G_BUFFER`. **[INTERP]**
14. **Target:** measured move `L3 - pattern height`; then next support OPEN.
15-16. Trigger break; 3 bars.
17. **Filters:** none enforced. Weekly-trend check, DXY, and "avoid RSI<25" are recorded only.
18-20. Context per G12; none; none.
21. Aliases: as P17.  22. As P17.
23. Master row 30; PS `/three-black-crows`; SH.  24. Open: as P17.  25. PROPOSED v1.0.

### P19 ABANDONED BABY (bullish and bearish) — `GT-ABABY-BULL-v1.0`, `GT-ABABY-BEAR-v1.0`

1. IDs as given (BASE, SRC-PS)  2. Abandoned Baby  3. both  4. 3
5. **Geometry (bullish):** C1 bear `LARGE`; C2 `DOJI` with `H2<=L1-gap_thr`; C3 bull `LARGE` with
   `L3>=H2+gap_thr`. **Bearish:** C1 bull `LARGE`; C2 `DOJI` with `L2>=H1+gap_thr`; C3 bear `LARGE` with
   `H3<=L2-gap_thr`. True gaps only; no touching or overlap.
6. **Prior state:** bullish `TREND=DOWN`; bearish `TREND=UP`.  7. At C3 completion.
8-11. **Baseline:** entry NEXT_TICK after C3; stop `L2-G_BUFFER` (bull) / `H2+G_BUFFER` (bear); 2R.
    (`pattern_low/high` = the whole three-bar pattern.)
12. **SRC-PS entry:** `OPEN_TRIGGER` at the first executable tick of C3: bullish if
    `ask >= H2+gap_thr` (bear mirror) while C1 is bear-LARGE and C2 is a gapped doji. **[INTERP]** (source:
    "buy on the open of the third candle").
13. **Stop:** `L2 - G_BUFFER` (source: below the doji's low).  14. **Target:** `T_SWING(1.5)` (source: prior swing).
15-16. None; none.
17. **Filters:** none enforced (RSI, DXY, Fibonacci recorded only).
18-20. Context per G12; none; gaps required (that is the identity).
21. Aliases: subset of Morning/Evening Star.
22. **Edge:** the source expects about 2-4 signals a year on D1 gold; sample size will be tiny and the
    system must report `UNKNOWN`, not a win rate.
23. Master row 31; PS `/abandoned-baby`.  24. Open: entry reading.  25. PROPOSED v1.0.

### P20 RISING THREE METHODS (bullish) — `GT-RISING3-BULL-v1.0`

1. GT-RISING3-BULL-v1.0 (BASE, SRC-PS)  2. Rising Three Methods  3. bullish  4. 5
5. **Geometry:** C1 bull `LARGE`; for k=2,3,4: bear AND `H_k<=H1` AND `L_k>=L1` AND `B_k<=0.5*B1`;
   C5 bull `LARGE` AND `C5>C1`.
6. **Prior state:** `TREND(i0-1)=UP`.  7. At C5 completion.
8-11. **Baseline:** BUY, stop `min(L1..L5)-G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK after C5.  13. **Stop:** `min(L2,L3,L4) - G_BUFFER` (source: below the lowest wick
    of C2-C4, not C1).
14. **Target:** TP1 = `P + 1.272*(H1-L1)` where `P=min(L2..L4)` **[INTERP]** (source names the 1.272 extension
    but not its anchor); TP2 (1.618) OPEN. Require reward to TP1 `>=2R` (source: minimum 1:2) else
    `SKIPPED_SRC_RR`.
15-16. None; none.  17. **Filters:** none enforced (volume decline not usable).
18-20. Context per G12; none; none.
21. Aliases: none.  22. Edge: strict containment (`H<=H1`, `L>=L1`) is the source's own rule.
23. Master row 38; PS `/rising-three-methods`; INV.  24. Open: Fibonacci anchor.  25. PROPOSED v1.0.

### P21 FALLING THREE METHODS (bearish) — `GT-FALLING3-BEAR-v1.0`

1. GT-FALLING3-BEAR-v1.0 (BASE, SRC-PS)  2. Falling Three Methods  3. bearish  4. 5
5. **Geometry:** C1 bear `LARGE`; for k=2,3,4: bull AND `H_k<=H1` AND `L_k>=L1` AND `B_k<=0.5*B1`;
   C5 bear `LARGE` AND `C5<C1`.
6. **Prior state:** `TREND(i0-1)=DOWN`.  7. At C5 completion.
8-11. **Baseline:** SELL, stop `max(H1..H5)+G_BUFFER`, 2R.
12. **SRC-PS entry:** NEXT_TICK after C5.  13. **Stop:** `max(H2,H3,H4) + G_BUFFER`.
14. **Target:** TP1 = `P - 1.272*(H1-L1)` with `P=max(H2..H4)` **[INTERP]**; TP2 OPEN; reward `>=2R` required.
15-16. None; none.  17. Filters: none enforced (DXY recorded only).  18-20. As P20.
21. Aliases: none.  22. As P20.
23. Master row 39; PS `/falling-three-methods`.  24. Open: as P20.  25. PROPOSED v1.0.

### P22 INSIDE BAR FALSE BREAKOUT (bullish and bearish) — `GT-IBFB-BULL-v1.0`, `GT-IBFB-BEAR-v1.0`

1. IDs as given (BASE, SRC-CB)  2. Inside Bar False Breakout  3. both  4. inside bar + 1..3
5. **Geometry:** mother C1, inside C2 (`H2<H1`, `L2>L1`). Then bar `Ck`, `k in {3,4,5}`, is the **first** bar after C2
   that pierces the mother range: every bar between C2 and `Ck` has `H<=H1` and `L>=L1`. `Ck` pierces exactly
   ONE side by at least 1 tick and closes back inside `[L1,H1]`. **Bearish** (sell) = pierces above (`H_k>=H1+tick`)
   and closes inside; **bullish** (buy) = pierces below (`L_k<=L1-tick`) and closes inside. If `Ck` pierces both
   sides, `NO_SIGNAL_AMBIGUOUS_BOTH_SIDES`.
6. **Prior state:** none in identity.  7. **Knowable at completion of `Ck`.**
8-11. **Baseline:** NEXT_TICK after `Ck`; stop beyond the break bar's extreme: bearish `H_k+G_BUFFER`, bullish
    `L_k-G_BUFFER`; 2R.
12. **SRC-CB entry:** NEXT_TICK after `Ck` ("after the close of the break bar").  13. **Stop:** as baseline.
14. **Target:** `T_SR(2.0)` (source: next level, minimum 2:1).
15-16. None; expiry as in 5.
17. **Filters:** bearish needs `TREND=UP` OR `AT_RESISTANCE`; bullish needs `TREND=DOWN` OR `AT_SUPPORT`;
    TF in {H1,H4,D1}.
18-20. Context per G12; none; none.
21. Aliases: excludes Inside Bar Breakout (P09) because that fires on a CLOSE outside the range.
22. **Edge:** the source says false breakouts "don't happen every time" and are stop-hunts by large players -
    an explanation, not a rule.  Example (bearish): mother `H=4210 L=4200`; inside `H=4207 L=4203`; next bar
    `H=4210.5 L=4204 C=4208` -> pierces `4210+tick`, closes inside -> sell signal.
23. Master row 41; CB (source 15).  24. Open: none beyond [SPEC].  25. PROPOSED v1.0.

---

## 4. Items the reviewer must decide (everything tagged [SPEC] or [INTERP])

1. **Constants invented by this spec:** `LARGE`/`SMALL` thresholds, `MIN_RANGE_SINGLE`, `G_BUFFER`,
   `REF_EQUITY`, `MAX_HOLD=50`, 15-minute stale-entry rule, `MIN_R` guard, `G_CONFIRM_MAX=3`,
   `STOP_ENTRY` 3-bar expiry, `G_MIN_REWARD_DEFAULT=1.5R`, three-soldiers similarity ratio, kicker tolerance
   `0.10*ATR`, session and news windows, `PIP_SRC_USD=0.10`.
2. **Interpretations of ambiguous source wording:** every confirmation rule; kicker/abandoned-baby
   `OPEN_TRIGGER`; tweezer trigger break; inside-bar close vs stop-entry; Fibonacci extension anchors;
   which stop the morning/evening star sources mean.
3. **Not enforced in v1 (source asks for it, we cannot yet supply it):** DXY correlation, volume, RSI/MACD
   divergence, Fibonacci-location requirements, weekly-trend checks, trailing stops, second targets where the
   split is not given.
4. **Deferred to v1.1:** conservative pullback entries (50% retrace etc.); trend-continuation reading of
   engulfing; strict-gap variants of Piercing/Dark Cloud; role-flipped support/resistance.
5. **Whether `PIP_SRC_USD=0.10` is right** - to be confirmed against real source examples and the demo
   account specification.
6. **Score handling:** ambiguous stop/target trades scored STOP FIRST with a target-first sensitivity figure
   (agreed in review), never deleted.
7. **Multiple testing:** up to about 585 strategies; Month-3 gates alone do not control false passes; the
   untouched validation stage is mandatory.

## 5. Change log

- 0.1 (2026-09-30): first full draft of Wave 1 from `MASTER_CANDLE_LIST.md` and the review round with ChatGPT.
