# AIDY Expert-Gate Programme — Build 6 M15 Price Structure Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 7 — H1 Price Structure Expert

## What was built

Build 6 adds:

`aidy_gold_m15_price_structure_expert_v1`

It is the second timeframe specialist in the 24-build expert-gate programme and is independently calibrated for M15 rather than inheriting M5 thresholds.

Directional M15 sub-calculators:
- `m15_8_bar_path`;
- `m15_swing_structure`;
- `m15_breakout_acceptance`;
- `m15_latest_15m_momentum`;
- `m15_candle_pressure`.

Context-only calculators:
- M15 range location;
- Build-4 contradiction diagnostics.

## M15-specific calibration

The expert uses:
- a 60-minute target horizon;
- an explicit 8-bar / 120-minute M15 path;
- 8-bar return;
- 8-bar log-price slope and R²;
- path efficiency;
- close-step persistence;
- ATR/RV-normalised 8-bar displacement;
- latest completed 15-minute return normalised to M15 ATR;
- completed-candle body and close-location confirmation;
- M15-specific swing/breakout thresholds.

The implementation records `copied_m5_thresholds=false`.

## Correlation and dependency control

Each calculator has an explicit dependency family and correlation group.

Overlapping structure or latest-bar evidence remains separately visible and scoreable for learning, but family-balanced aggregation prevents duplicated evidence from manufacturing current conviction.

Historical reliability remains separate from current internal conviction.

## PIT / no-lookahead properties

- Only completed bars enter Build-4 mathematics.
- The frozen decision is unchanged by later rows.
- Future values remain excluded.
- Missing M15 evidence remains UNKNOWN.
- Contradictory evidence can force ABSTAIN.
- NEUTRAL remains explicit.
- The legacy M15 direction is retained as an ablation baseline.
- Added complexity receives no automatic weight.

## Acceptance

AIDY PR #209 merged:
`102b75170fc5f9b64b02ea5223b1c61182b802d5`

Final exact-candidate checks:
- Evidence Semantic Change Gate: PASS — run `35585078753`
- static checks: PASS
- focused workflow suite: 159 passed
- full repository regression: 1411 passed — run `35585078717`

Acceptance coverage included:
- clean M15 uptrend;
- clean M15 downtrend;
- chop not promoted to trend;
- reversal/conflict surfacing;
- explicit 8-bar path evidence;
- explicit latest 15-minute momentum evidence;
- missing M15 -> UNKNOWN;
- PIT completed-bar provenance;
- no-future-values;
- as-of mismatch rejection;
- Build-3 trust attachment;
- chronological freeze;
- dependency/correlation metadata;
- legacy-M15 comparison.

## Production / execution status

No Worker deployment was required because Build 6 is an expert library and is not yet wired into live gate weighting.

Build 6 does not:
- change Super Signals execution;
- change provider activation;
- change owner 1% risk;
- replace the current live marker brain;
- enable formal-forward authority;
- grant live-money authority.

## Next build

**Build 7 — H1 Price Structure Expert**

Build 7 focuses on genuine hourly trend quality, swing structure, acceleration and breakout acceptance. A positive first-to-last hourly move must not be enough to label H1 strongly bullish when the internal path is choppy or poorly persistent. H1 explanations must expose slope, quality, swings, location and contradictions, and H1 conditional trust must remain separate from M15.

No Build 8 work begins until Build 7 passes its acceptance gate.
