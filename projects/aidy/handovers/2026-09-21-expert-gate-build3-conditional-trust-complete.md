# AIDY Expert-Gate Programme — Build 3 Conditional Trust & Score Engine v3

**Date:** 2026-09-21  
**Status:** PRODUCTION VERIFIED  
**Next:** Build 4 — Common Price Expert Mathematics

## What was built

Build 3 adds:

`aidy_gold_expert_conditional_trust_v3`

It gives every future expert gate and every scoreable sub-calculator separate historical trust by environment.

Core behavior:
- +2 / +1 / 0 / -1 / -2 outcome scoring;
- exact mini-environment scorebooks;
- gate-declared reduced mini-environment scorebooks;
- global-core fallback;
- gate-global fallback;
- neutral prior when no qualified history exists;
- deterministic hierarchical shrinkage toward broader history;
- minimum sample requirements before a specific context can override broader evidence;
- separate directional accuracy and impact score;
- bounded recent-window stats alongside long-term stats;
- Wilson 95% accuracy intervals;
- explicit sample-confidence/uncertainty state;
- strict resolved-before-as-of filtering so current/future outcomes cannot influence the current decision;
- stable/idempotent outcome result identities;
- immutable result digests;
- trust envelope separate from the frozen Build-2 gate packet and its internal conviction.

The generic engine never guesses a gate's reduced mini-environment. Each later expert must explicitly define which dimensions are used at each fallback level.

## Why this matters

Raw percentages are dangerous. 8 wins from 10 observations must not automatically outrank 137 wins from 200 observations.

Build 3 lets AIDY answer a more useful question:

> How reliable has this exact gate or calculator been under conditions like these, and how much evidence do I actually have?

Small samples borrow heavily from broader history. As sample size grows, the local environment is allowed to own more of the estimate.

## D1 persistence

Migration:

`0026_gold_expert_conditional_trust.sql`

Production tables:
- `aidy_gold_expert_outcome_ledger`
- `aidy_gold_expert_context_scores`

The raw ledger preserves reconstruction and recent-window calculations. The context score table supports fast future pre-decision lookup.

## Acceptance

AIDY implementation merge:
`76cbedc410dbb4f298687bdccff754f444048036`

AIDY repo handoff:
`538ebac3fe8799550bce99d1b65a517834081e13`

Engineering:
- Evidence Semantic Change Gate: PASS
- static checks: PASS
- focused workflow suite: 122 passed
- full repository regression: 1374 passed

Production:
- deploy run: `35580744094`
- Worker version: `bb0a1553-5b85-44aa-8ca7-6cba85fad081`
- D1 migration applied: PASS
- outcome ledger table present: PASS
- context score table present: PASS
- capture cron present: PASS
- environment v3 audit: PASS
- 34/34 toolbox trace/coverage remained intact
- future-values used: 0
- live-money authority: 0

## What Build 3 does not do

It does not yet:
- replace the current M5/M15/H1/H4/D1 logic;
- assign live expert-gate weights, because those expert gates are not built yet;
- alter the existing legacy marker-weighting runtime;
- change Super Signals execution;
- change owner 1% risk;
- grant live-money authority.

## Next build

**Build 4 — Common Price Expert Mathematics**

Build 4 creates the shared deterministic math used by the price/timeframe experts:
- multi-lookback returns;
- OLS/log-price slope;
- R²/trend quality;
- close-step persistence;
- path efficiency;
- ATR/RV-normalised movement;
- acceleration/deceleration;
- confirmed swing sequences;
- structure breaks;
- breakout/acceptance/retest/reclaim;
- range position;
- wick/body/close geometry;
- contradiction flags.

No Build 5 work begins until Build 4 passes its own acceptance gate.
