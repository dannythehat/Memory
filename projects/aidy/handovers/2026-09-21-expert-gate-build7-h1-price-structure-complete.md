# AIDY Expert-Gate Programme — Build 7 H1 Price Structure Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 8 — H4 Price Structure Expert

## What was built

Build 7 adds:

`aidy_gold_h1_price_structure_expert_v1`

This is the third timeframe specialist in the 24-build expert-gate programme.

Directional H1 sub-calculators:
- `h1_trend_quality`;
- `h1_swing_structure`;
- `h1_breakout_acceptance`;
- `h1_acceleration`;
- `h1_candle_pressure`.

Context-only calculators:
- H1 range location;
- Build-4 contradiction diagnostics.

## H1-specific intelligence

The H1 trend-quality specialist uses:
- 8-hour and 13-hour return;
- 8-hour and 13-hour log-slope / R²;
- close-step persistence;
- path efficiency;
- ATR-normalised displacement.

A directional trend vote requires minimum quality across R², efficiency, persistence and directional quality.

A dedicated H1 trend-quality guard blocks the classic false signal where first-to-last return is positive or negative but the internal hourly path is noisy. If a same-direction conclusion forms while the H1 quality gate fails, the expert downgrades to ABSTAIN rather than treating endpoint direction as a strong trend.

## Explanations

Every H1 packet explicitly surfaces:
- slope;
- quality;
- swings and breakout state;
- range/location;
- contradiction diagnostics.

## Learning separation

H1 uses its own gate ID, mini-environment, conditional trust scopes and scorebook path. H1 historical trust therefore does not borrow M15 history.

Dependency families and correlation groups keep overlapping evidence separately learnable without giving duplicated evidence extra current weight.

## Acceptance

AIDY PR #210 merged:
`a03cd568884549e760b2c6abc43d60127a4fbd23`

Final exact-candidate checks:
- Evidence Semantic Change Gate: PASS — run `35585909232`
- static checks: PASS
- focused workflow suite: 172 passed
- full repository regression: 1424 passed — run `35585909198`

Acceptance coverage included:
- clean H1 uptrend;
- clean H1 downtrend;
- ordinary chop;
- explicit positive-first-to-last but choppy path;
- reversal/conflict surfacing;
- missing H1 -> UNKNOWN;
- PIT completed-bar provenance;
- no-future-values;
- chronological freeze;
- separate H1 trust scope;
- dependency/correlation metadata;
- explicit explanation fields;
- legacy-H1 comparison.

## Production / execution status

No Worker deployment was required because Build 7 is an expert library and is not yet wired into live gate weighting.

Build 7 does not:
- change Super Signals execution;
- change provider activation;
- change owner 1% risk;
- replace the current live marker brain;
- enable formal-forward authority;
- grant live-money authority.

## Next build

**Build 8 — H4 Price Structure Expert**

Build 8 is a slow structural expert. H4 cannot dominate a next-15m forecast merely because it is a higher timeframe. It must prove incremental conditional value, and conflict with M5/M15/H1 must remain explicit and scoreable.

No Build 9 work begins until Build 8 passes its acceptance gate.
