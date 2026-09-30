# Ambiguity & inconsistency log for the golden vectors

Found while writing `golden_vectors.json` against `CANDLE_SPEC_V1.md` Draft 0.2.2. **The spec has NOT been edited** (owner/reviewer rule: do not change the spec to make a test pass unless the test exposes a genuine ambiguity or contradiction, and then flag it for review). Each item lists the readings, the vectors that depend on it, and a recommended ruling. `BLOCKED` vectors assert nothing until a ruling is logged; `PROVISIONAL` vectors state the assumption used.

Counts: **4 high**, **13 medium**, **12 low**. HIGH = a wrong guess changes trades or makes a rule impossible to implement; MEDIUM = changes events, counters or which trades are skipped; LOW = editorial or an edge case.

| ID | severity | where | vectors |
|---|---|---|---|
| A-01 | HIGH | G4 zone death | GV-G-ZN-11 (blocked) |
| A-02 | LOW | Notation (all patterns) | all pattern packs |
| A-03 | MEDIUM | P08 SRC-PS field 17 | GV-P08-V11 (assumes C2), GV-P08-V14 (blocked), GV-P08-V15 (blocked) |
| A-04 | MEDIUM | G10 T_SR / T_SWING | GV-P08-V09 (blocked) |
| A-05 | MEDIUM | P06 SRC-SH field 17 | GV-P06-H07 (blocked) |
| A-06 | MEDIUM | G6 sessions | GV-G-SS-03, GV-P12-S03, GV-P12-S05 |
| A-07 | MEDIUM | G6 news windows | GV-G-NW-03, GV-DORM-P04-04, GV-DORM-P04-06 |
| A-08 | LOW | P08 events | GV-P08-B05, GV-P08-B06 |
| A-09 | MEDIUM | P09 / hub counters | GV-P09-S07 (provisional), GV-OV-09 |
| A-10 | LOW | P10 vs P11 flags | GV-P11-F01, GV-P11-F02 (no P10 mirror) |
| A-11 | MEDIUM | G8 Layer B / C | GV-EX-B05 (blocked) |
| A-12 | MEDIUM | G0b event model | all vectors marked PROVISIONAL with a TF gate (9 for A-12) |
| A-13 | HIGH | G8 MAX_HOLD | GV-EX-B01 (blocked) |
| A-14 | HIGH | G9 swap | GV-EX-B02 (blocked) |
| A-15 | MEDIUM | P09 SRC-CB field 17 | GV-P09-V01 (provisional) |
| A-16 | LOW | G10 T_SWING | GV-P14-V05 (provisional) |
| A-17 | MEDIUM | P15 vs P16 SRC-PS | GV-P16-V07 (provisional: literal spec) |
| A-18 | LOW | G10 STOP_ENTRY | GV-P17-V04 (provisional) |
| A-19 | LOW | P20/P21 targets | GV-P20-V04 (provisional) |
| A-20 | MEDIUM | P12 vs P13 SRC-PS | GV-P13-V20, GV-P13-V21 (hand-written, literal spec) |
| A-21 | LOW | G11 clustering | GV-OV-11 (provisional) |
| A-22 | MEDIUM | G0 numerics | GV-G-ATR-03 (provisional) |
| A-23 | LOW | G4 clusters | GV-G-ZN-04 (provisional) |
| A-24 | LOW | G3/G4 window | GV-G-SW-04 avoids the edge |
| A-25 | HIGH | G8 weekend / gap entries | GV-EX-B03 (blocked) |
| A-26 | MEDIUM | G9 bars-only fallback | GV-EX-B04 (blocked) |
| A-27 | LOW | G8 Layer A RAW | GV-EX-B06 (blocked) |
| A-28 | LOW | P20/P21 | GV-P20-V05, GV-P21-V05 |
| A-29 | LOW | P22 | GV-P22-B05 |

## A-01 — G4 zone death (HIGH)

Dead zones: 'a zone is dead once a completed bar closes more than 0.10*ATR beyond its FAR edge'. A zone has no side until it is used, role flips are not modelled, so 'far' is undefined. Changes which zones survive, so it changes targets and AT_SUPPORT/AT_RESISTANCE.

Readings:
- A: dead per role (a close above kills it as resistance, below kills it as support).
- B: dead for all uses after a close more than 0.10*ATR beyond EITHER edge.
- C: role fixed by the side price was on when the zone formed.

Vectors: GV-G-ZN-11 (blocked)

Recommendation: Adopt B for v1 (simplest, no role state) and log it as a decision.

## A-02 — Notation (all patterns) (LOW)

`C1`, `C2`, `C3` mean both the candle (`C1 bear`, `LARGE(C1)`) and its close (`O2<=C1`, `C3>(O1+C1)/2`). Readable from context but error-prone for a coder.

Readings:
- Vectors follow the contextual reading (candle for colour/size clauses, close inside inequalities).

Vectors: all pattern packs

Recommendation: Rename candles K1..K5 or closes `close1`..

## A-03 — P08 SRC-PS field 17 (MEDIUM)

'Skips bars containing a high-impact USD event and bars overlapping the daily rollover pause': it does not say WHICH bars (C2 only? C1 or C2? the whole formation?) and the daily rollover pause (start, end, timezone) is not defined anywhere.

Readings:
- News: A) C2 only; B) any geometry bar.
- Rollover: cannot be evaluated.

Vectors: GV-P08-V11 (assumes C2), GV-P08-V14 (blocked), GV-P08-V15 (blocked)

Recommendation: State the bar rule and add the pause window to the calendar section.

## A-04 — G10 T_SR / T_SWING (MEDIUM)

A live zone that STRADDLES the entry price: its near edge is behind the entry. 'Nearest live zone beyond the entry' and 'never steps over a nearer obstacle' do not say whether such a zone is 'beyond'.

Readings:
- A: ignored (target = next zone).
- B: it is the nearest obstacle and its near edge is behind the entry -> SKIPPED_TARGET_ALREADY_PASSED.

Vectors: GV-P08-V09 (blocked)

Recommendation: B is consistent with the nearest-only rule; state it.

## A-05 — P06 SRC-SH field 17 (MEDIUM)

SRC-SH is 'shape tightened to wicks engulfed AND RSI14(C2)<30'. Does the base prior state (TREND = DOWN) still apply?

Readings:
- A: inherited (calculator's reading).
- B: replaced by the RSI test.

Vectors: GV-P06-H07 (blocked)

Recommendation: Say which; A matches how other variants restate prior state only when they change it.

## A-06 — G6 sessions (MEDIUM)

Session boundaries: start inclusive / end exclusive? Only the vectors flagged PROVISIONAL depend on it.

Readings:
- A: [start, end) (assumed).
- B: [start, end].

Vectors: GV-G-SS-03, GV-P12-S03, GV-P12-S05

Recommendation: Adopt [start, end).

## A-07 — G6 news windows (MEDIUM)

Blocked window inclusive at both ends? (T-30..T+15, T-60..T+30).

Readings:
- A: inclusive both ends (assumed).
- B: exclusive at one or both ends.

Vectors: GV-G-NW-03, GV-DORM-P04-04, GV-DORM-P04-06

Recommendation: Adopt inclusive (conservative: blocks more).

## A-08 — P08 events (LOW)

Outside Bar direction comes from C2's colour, so the SHAPE_DETECTED event is direction-specific. A geometric outside bar with C2 = O2 has no side. The vectors log shape per side and none for the doji-close case.

Readings:
- A: shape is per side (assumed).
- B: geometry-only shape event without side.

Vectors: GV-P08-B05, GV-P08-B06

Recommendation: Keep A.

## A-09 — P09 / hub counters (MEDIUM)

Inside Bar BASE_PATTERN_FORMED occurs at C2, before the direction is known, but counters are per side. Also undefined: what the bull strategy logs when the breakout goes the OTHER way, and the 'still waiting' state while bars 3-5 are pending.

Readings:
- A: count formation under the side that breaks out (at the breakout).
- B: count it under a side-less key at C2.
- C: count it for both sides.

Vectors: GV-P09-S07 (provisional), GV-OV-09

Recommendation: A is the cleanest for per-side hub cards; needs a PENDING state for the window.

## A-10 — P10 vs P11 flags (LOW)

Tweezer Top records `C2close<=(O1+C1)/2`; Tweezer Bottom records 'C1 in its lowest 25%, C2 in its highest 25%'. Mirror patterns with different flags.

Readings:
- Give both the same flag set.

Vectors: GV-P11-F01, GV-P11-F02 (no P10 mirror)

Recommendation: Align the flags.

## A-11 — G8 Layer B / C (MEDIUM)

SKIPPED_R_TOO_SMALL (R < max(4*spread, 0.10*ATR)) is written in the baseline target bullet only. Does it apply to source variants?

Readings:
- A: baseline only.
- B: every variant.

Vectors: GV-EX-B05 (blocked)

Recommendation: Decide; B is safer for costs.

## A-12 — G0b event model (MEDIUM)

Where non-qualification is logged: the timeframe gate has a reason code (SKIPPED_TF_NOT_ALLOWED) but trend/location failures have none, and the spec does not say whether the TF skip precedes VARIANT_QUALIFIED. The vectors record TF skips when the base shape exists, with no VARIANT_QUALIFIED, and treat all other variant non-qualification as silent.

Readings:
- A: as vectors (assumed).
- B: every non-qualification gets a coded disposition.

Vectors: all vectors marked PROVISIONAL with a TF gate (9 for A-12)

Recommendation: State the rule; B gives the hub more diagnostics.

## A-13 — G8 MAX_HOLD (HIGH)

'MAX_HOLD = 50 bars ... then close at market': does the entry bar count as bar 1, and what if the 50 bars straddle a scheduled closure (bars that do not exist)? The three readings give different exit times.

Readings:
- A: entry bar = bar 1.
- B: 50 bars after the entry bar.
- C: wall-clock 50 x TF.

Vectors: GV-EX-B01 (blocked)

Recommendation: Adopt B, counting only bars that exist.

## A-14 — G9 swap (HIGH)

Results are 'minus swap and commission converted to R (from the account spec)' but the spec gives no swap rule: rollover time, nights counted, triple-swap day, units, conversion.

Readings:
- Undefined.

Vectors: GV-EX-B02 (blocked)

Recommendation: Add swap fields and a rollover rule to the account fixture; ask Vantage for the swap table.

## A-15 — P09 SRC-CB field 17 (MEDIUM)

'Mother bar at a level' does not say which extreme is compared with the zones (mother low for a bullish breakout? mother high?).

Readings:
- A: bull -> mother LOW at support, bear -> mother HIGH at resistance (assumed, G4's AT_SUPPORT uses the pattern's lowest low).
- B: the extreme in the breakout direction.

Vectors: GV-P09-V01 (provisional)

Recommendation: Adopt A.

## A-16 — G10 T_SWING (LOW)

'Nearest confirmed swing pivot beyond the entry': for a BUY, do swing LOWS above the entry count? Other rules speak of 'swing high above'/'swing low below'.

Readings:
- A: same-side type only (assumed).
- B: any pivot.

Vectors: GV-P14-V05 (provisional)

Recommendation: Adopt A.

## A-17 — P15 vs P16 SRC-PS (MEDIUM)

The two source variants are not mirrors: stop = min(L1,L2)-buffer (P15) vs H2+buffer only (P16, mirror would be max(H1,H2)+buffer); TP2 = nearest swing HIGH above TP1 (P15) vs near edge of the nearest ZONE below TP1 (P16).

Readings:
- Intentional (different source wording) or an oversight.

Vectors: GV-P16-V07 (provisional: literal spec)

Recommendation: Confirm against the Pro-Scalper pages; if unintended, mirror P15.

## A-18 — G10 STOP_ENTRY (LOW)

A tick at exactly the instant the third bar completes: inside the window or not?

Readings:
- A: inside (assumed).
- B: outside.

Vectors: GV-P17-V04 (provisional)

Recommendation: Adopt A (window is closed at the right).

## A-19 — P20/P21 targets (LOW)

If the fib target is behind the entry, both SKIPPED_TARGET_ALREADY_PASSED and SKIPPED_SRC_RR apply. Precedence?

Readings:
- A: already-passed first (assumed).
- B: SRC_RR.

Vectors: GV-P20-V04 (provisional)

Recommendation: Adopt A (more specific).

## A-20 — P12 vs P13 SRC-PS (MEDIUM)

Not mirrors: minimum reward 2.0R (Piercing) vs 1.5R (Dark Cloud); the Asia-only skip is on Piercing only.

Readings:
- Intentional (source differences) or an oversight.

Vectors: GV-P13-V20, GV-P13-V21 (hand-written, literal spec)

Recommendation: Confirm against the sources.

## A-21 — G11 clustering (LOW)

Which bar an EARLY setup 'completes on' for cluster purposes (formation_end = C1, signal at the next bar's open), and whether shapes, formed detections or signals cluster.

Readings:
- A: formed detections by formation_end_bar (assumed).

Vectors: GV-OV-11 (provisional)

Recommendation: State the clustering key.

## A-22 — G0 numerics (MEDIUM)

No numeric-precision or rounding rule. ATR = sum/14 is non-terminating (57/14 in GV-G-ATR-03), and boundary comparisons (e.g. 0.60*ATR) can flip with binary floating point.

Readings:
- Require exact decimal/rational arithmetic (or fixed-point ticks) and state ATR rounding.

Vectors: GV-G-ATR-03 (provisional)

Recommendation: Mandate decimal arithmetic in prices (integer ticks); keep ATR exact or round half-up to a stated scale.

## A-23 — G4 clusters (LOW)

Median of an EVEN number of pivots is not defined.

Readings:
- A: mean of the two middle prices (assumed).

Vectors: GV-G-ZN-04 (provisional)

Recommendation: State it.

## A-24 — G3/G4 window (LOW)

'Last 200 completed bars': can a pivot near the window start use neighbour bars that lie just outside the window?

Readings:
- Ambiguous only at the window edge.

Vectors: GV-G-SW-04 avoids the edge

Recommendation: State it.

## A-25 — G8 weekend / gap entries (HIGH)

A gap can put the entry price already BEYOND the stop (BUY at an ask below the stop). |entry - stop| is positive, so R and the 2R target come out as nonsense.

Readings:
- A: skip with a new code (e.g. SKIPPED_ENTRY_BEYOND_STOP).
- B: enter and stop out at once.
- C: literal formula.

Vectors: GV-EX-B03 (blocked)

Recommendation: Adopt A and add the code.

## A-26 — G9 bars-only fallback (MEDIUM)

Short stops/targets trigger on the ASK but an OHLC bar has bid prices only. Which spread turns a bar into an ask?

Readings:
- A: bid bars only.
- B: the bar's recorded spread (calculator).
- C: a fixed assumed spread.

Vectors: GV-EX-B04 (blocked)

Recommendation: Adopt B and require a per-bar spread in the data model.

## A-27 — G8 Layer A RAW (LOW)

MAE sign convention: negative min(d*(extreme-ref)), positive magnitude, or clamped at 0?

Readings:
- Three readings.

Vectors: GV-EX-B06 (blocked)

Recommendation: Adopt negative (same sign convention as ret).

## A-28 — P20/P21 (LOW)

Rising SRC-PS does not require the body-close flag but Falling SRC-PS does (already open item 2 in section 4 of the spec). Both are literal in the vectors.

Readings:
- Intentional (page wording) or an oversight.

Vectors: GV-P20-V05, GV-P21-V05

Recommendation: Check the Rising page once more.

## A-29 — P22 (LOW)

`NO_SIGNAL_AMBIGUOUS_BOTH_SIDES` is used in P22 but is not in the G0b list of reason codes.

Readings:
- Add it (or map to an existing code).

Vectors: GV-P22-B05

Recommendation: Add to the list.

## Observations (not ambiguities)

- **O-1** No ACTIVE variant can qualify without its BASE pattern: every variant with a relaxed prior state or wider tolerance is a pip-dependent SRC-PS variant, which is disabled by D-032. The `VARIANT_QUALIFIED` with `base_formed=false` path therefore appears only in DORMANT vectors (GV-DORM-*). If D-032 is lifted the dormant vectors become active.
- **O-2** The early setups (Kicker Early, Abandoned Baby Early) test the BID for both directions, so the bear side is not the price mirror of the bull side (a mirror of a bid test is an ask test). Their bear vectors are hand-written, not mirrored.
- **O-3** The Dragonfly/Gravestone clause `LW >= 0.80*R` is implied by `DOJI` and `UW <= 0.05*R` (LW >= 0.90R) and can never fail alone (GV-P04-N04).
- **O-4** For Abandoned Baby (completed and early) the SRC-PS stop equals the BASE stop by construction (the doji's low is always the lowest low); the source and baseline stops cannot differ.
- **O-5** G2 size-class boundaries (LARGE/SMALL/DOJI) are tested once globally (GV-G-CLS-*) and again as single-clause probes inside patterns that use them (Piercing, Dark Cloud, Kicker, stars, Rising/Falling).
