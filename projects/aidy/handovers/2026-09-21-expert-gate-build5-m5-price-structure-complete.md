# AIDY Expert-Gate Programme — Build 5 M5 Price Structure Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 6 — M15 Price Structure Expert

## What was built

Build 5 adds:

`aidy_gold_m5_price_structure_expert_v1`

This is the first actual timeframe mini-brain in the 24-build expert-gate programme.

It consumes Build-4 completed-bar mathematics and emits one immutable Build-2 expert packet with:
- M5 trend/path quality;
- confirmed M5 swing structure;
- M5 breakout acceptance/reclaim;
- M5 momentum transition;
- latest completed-candle pressure;
- range location as context-only evidence;
- explicit contradiction diagnostics as context-only evidence.

Each directional calculator remains separately visible and scoreable.

## Correlation / complexity control

The final M5 conclusion uses family-balanced aggregation.

Multiple correlated calculations may all be observed and scored historically, but they do not gain extra current weight merely because several versions of the same underlying evidence agree. Contradictory directional families can force ABSTAIN rather than being silently averaged away.

NEUTRAL, ABSTAIN and UNKNOWN remain explicit outcomes.

## Environment-aware trust

Build 3 conditional trust is attached separately to:
- the M5 expert gate;
- every scoreable directional M5 sub-calculator.

The M5 expert declares its own specialist mini-environment and reduced fallback contexts. Small samples therefore back off through broader history rather than dominating current reasoning.

Historical reliability remains separate from current internal conviction.

## Legacy comparison

The existing M5 direction remains an explicit baseline.

Build 5 includes chronological replay comparison so the new expert can later be measured against the legacy M5 rule. Greater complexity itself is never acceptance evidence and grants no automatic weight.

## PIT / no-lookahead properties

- Build-4 completed-candle rules remain mandatory.
- Partial current candles are excluded.
- Confirmed swings retain their no-lookahead right-wing rule.
- Gate evidence must be observed by the frozen as-of timestamp.
- Later rows cannot alter an already frozen M5 expert packet.
- Historical trust is pre-decision only.
- No outcome field enters the expert decision.
- Research/shadow only.
- AIDY live-money authority remains false.

## Acceptance

AIDY PR #206 merged:
`eaa6f49636ae4ae9f73d6a17db4c9d8f46d8743a`

AIDY repository handoff:
`be2760dd6daa52bdadc655b50d8bb32f02eeef60`

Exact accepted candidate:
`22a31d125f6a74c1caa120d33534976fd089a34d`

Acceptance evidence:
- Evidence Semantic Change Gate: PASS;
- static checks: PASS;
- focused acceptance/regression suite: **148 passed**;
- full repository regression: **1400 passed**;
- acceptance workflow: `35583969491`.

Synthetic/PIT acceptance covered:
- clean M5 uptrend;
- clean M5 downtrend;
- chop/range refusing to masquerade as trend;
- reversal/conflict surfacing;
- missing M5 evidence -> UNKNOWN;
- PIT provenance and future-value exclusion;
- mismatched as-of rejection;
- Build-3 exact-context trust attachment;
- chronological freeze against later rows;
- explicit replay comparison versus the legacy M5 baseline.

No Worker deployment was required because Build 5 is not wired into the current live weighting path.

No Super Signals execution, provider activation, owner 1% risk, broker path or live-money authority changed.

## Next build

**Build 6 — M15 Price Structure Expert**

Build 6 will use the same expert contract but will be independently calibrated for M15. The blueprint specifically requires:
- the M15 8-bar path to be separately identified;
- latest 15-minute momentum to be separately identified;
- M15 swing/breakout features to be separately identified;
- correlation/dependency metadata to remain explicit;
- the legacy M15 baseline to remain available for ablation.

No Build 7 work begins until Build 6 passes its acceptance gate.
