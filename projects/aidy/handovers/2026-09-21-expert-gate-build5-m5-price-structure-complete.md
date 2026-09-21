# AIDY Expert-Gate Programme — Build 5 M5 Price Structure Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 6 — M15 Price Structure Expert

## What was built

Build 5 adds:

`aidy_gold_m5_price_structure_expert_v1`

It is the first actual timeframe expert mini-brain in the 24-build expert-gate programme.

Directional sub-calculators:
- `m5_trend_path`;
- `m5_swing_structure`;
- `m5_breakout_acceptance`;
- `m5_momentum_transition`;
- `m5_candle_pressure`.

Context-only calculators:
- M5 range location;
- Build-4 contradiction diagnostics.

The expert consumes Build-4 completed-bar mathematics, emits the standard Build-2 expert packet, declares its own repeatable M5 mini-environment, and attaches Build-3 conditional trust to the gate and its calculators.

## Important design properties

- Correlated calculations are visible and individually scoreable, but the current conclusion is family-balanced so calculator count alone cannot manufacture conviction.
- Historical reliability remains separate from current internal conviction.
- Weak evidence can remain NEUTRAL.
- Conflicting directional families can ABSTAIN.
- Missing evidence remains UNKNOWN.
- The legacy M5 direction is retained as an explicit baseline for ablation/comparison.
- Added sophistication receives no automatic weight.
- Only completed candles are admitted through Build 4.
- Future values remain excluded.
- Research/shadow and live-money-disabled boundaries remain intact.

## Acceptance

AIDY PR #206 merged:
`eaa6f49636ae4ae9f73d6a17db4c9d8f46d8743a`

AIDY repository handoff:
`be2760dd6daa52bdadc655b50d8bb32f02eeef60`

Final exact-candidate checks:
- Evidence Semantic Change Gate: PASS — run `35583969559`
- static checks: PASS
- focused workflow suite: 148 passed
- full repository regression: 1400 passed — run `35583969491`

Acceptance coverage included:
- clean M5 uptrend;
- clean M5 downtrend;
- chop/range not promoted to trend;
- reversal/conflict surfacing;
- missing M5 evidence -> UNKNOWN;
- PIT completed-bar provenance;
- no-future-values;
- as-of mismatch rejection;
- Build-3 exact mini-environment trust attachment;
- chronological freeze unaffected by later rows;
- legacy-M5 baseline comparison;
- explicit no-complexity bonus.

## Production / execution status

No Worker deployment was required for Build 5 because this expert library is not yet wired into the live gate-weighting path.

Build 5 does not:
- change Super Signals execution;
- change provider activation;
- change owner 1% risk;
- replace the current live marker brain;
- enable formal-forward authority;
- grant live-money authority.

## Next build

**Build 6 — M15 Price Structure Expert**

Build 6 uses the same expert contract, but M15 is calibrated independently rather than copying M5 thresholds. Acceptance requires separate identification of the M15 8-bar path, latest 15-minute momentum, swing/breakout evidence, correlation/dependency metadata, and retention of the legacy M15 baseline for ablation.

No Build 7 work begins until Build 6 passes its acceptance gate.
