# AIDY Expert-Gate Programme — Build 8 H4 Price Structure Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 9 — D1 Context Expert

## What was built

Build 8 adds:

`aidy_gold_h4_price_structure_expert_v1`

This is the fourth timeframe specialist in the 24-build expert-gate programme.

Directional H4 sub-calculators:
- `h4_trend_quality`;
- `h4_swing_structure`;
- `h4_breakout_acceptance`;
- `h4_acceleration`;
- `h4_candle_pressure`;
- `h4_lower_timeframe_conflict`.

Context-only calculators:
- H4 range location;
- Build-4 contradiction diagnostics.

## Slow structural calibration

H4 uses slow path evidence:
- 8 H4 bars = 32 hours;
- 13 H4 bars = 52 hours;
- log-slope / R²;
- persistence;
- path efficiency;
- ATR-normalised displacement;
- confirmed swings;
- breakout acceptance/reclaim;
- 12-hour acceleration context.

## No automatic timeframe dominance

H4 gets:
- no automatic higher-timeframe priority bonus;
- no direct next-15m authority;
- default next-15m weight = 0.

A separate historical evaluator checks incremental value against the lower-timeframe baseline. H4 only becomes eligible for future short-horizon influence if:
- minimum sample size is met; and
- accuracy improves over the baseline.

That eligibility is evidence for a later fusion build only. It does not grant live weight here.

## Lower-timeframe conflict

When a directional H4 view disagrees with M5/M15/H1 consensus, the disagreement is emitted as the separately scoreable `h4_lower_timeframe_conflict` hypothesis.

This lets Aidy learn when slow-timeframe disagreement was useful versus harmful. It is explicitly not an override.

## Acceptance

AIDY PR #211 merged:
`cfe3ab856e3e7c11df99066c9ad99a39391532e6`

Final exact-candidate checks:
- Evidence Semantic Change Gate: PASS — run `35586632949`
- static checks: PASS
- focused workflow suite: 187 passed
- full repository regression: 1439 passed — run `35586632848`

Acceptance coverage included:
- clean H4 uptrend/downtrend;
- chop and positive-but-noisy path handling;
- explicit H4/lower-timeframe conflict;
- conflict scoreability;
- zero timeframe-derived next-15m authority;
- zero default next-15m weight;
- insufficient-sample rejection for incremental value;
- positive incremental-value eligibility after minimum sample;
- missing H4 -> UNKNOWN;
- PIT completed-bar provenance;
- no-future-values;
- chronological freeze;
- separate H4 trust scope;
- dependency/correlation metadata;
- legacy-H4 comparison.

## Production / execution status

No Worker deployment was required because Build 8 is an expert library and is not wired into live gate weighting.

Build 8 does not:
- change Super Signals execution;
- change provider activation;
- change owner 1% risk;
- replace the current live marker brain;
- enable formal-forward authority;
- grant live-money authority.

## Next build

**Build 9 — D1 Context Expert**

D1 is the slowest structural/macro-location context. It must abstain when daily evidence is stale or partial, must not force a 15-minute direction, and historical evaluation must separate context value from direct forecast value.

No Build 10 work begins until Build 9 passes its acceptance gate.
