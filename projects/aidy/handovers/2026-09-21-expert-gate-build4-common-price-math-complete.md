# AIDY Expert-Gate Programme — Build 4 Common Price Expert Mathematics

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 5 — M5 Price Structure Expert

## What was built

Build 4 adds:

`aidy_gold_price_expert_math_v1`

It is the shared factual mathematics layer for future M5/M15/H1/H4/D1 expert gates.

Primitive families:
- multi-lookback returns;
- log-price OLS slope and R² trend quality;
- close-step persistence;
- path efficiency;
- ATR(14) and realised-volatility normalisation;
- recent-vs-prior acceleration/deceleration;
- confirmed wing-2 swing highs/lows;
- HH/HL/LH/LL swing-sequence structure;
- close-based structure breaks;
- breakout lifecycle: penetration, close acceptance, hold, retest-hold and reclaim;
- 20/50-bar range location;
- latest completed candle body/wick/close-location geometry;
- explicit contradiction diagnostics;
- unique primitive manifest to prevent duplicate feature counting.

## PIT / no-lookahead properties

- Only completed bars at the frozen as-of timestamp are used.
- The current partial candle is excluded.
- A swing pivot is unavailable until the required right-hand confirmation bars have completed.
- No historical outcome enters the calculations.
- The library emits no directional gate vote.
- Research-only and live-money-disabled boundaries remain intact.

## Acceptance

AIDY PR #205 merged:
`b3fdabe25b58ea816f282b7cfc29ab22485d4257`

Final exact-candidate checks:
- Evidence Semantic Change Gate: PASS
- static checks: PASS
- focused workflow suite: 122 passed
- full repository regression: 1390 passed

Synthetic acceptance covered:
- clean uptrend;
- clean downtrend;
- range/chop;
- reversal;
- exact persistence/path-efficiency arithmetic;
- volatility normalisation;
- exact candle geometry;
- no-lookahead swing confirmation;
- partial-bar exclusion;
- accepted breakout;
- rejected/reclaimed breakout;
- factual range position;
- contradiction diagnostics;
- duplicate primitive rejection;
- deterministic packet digest;
- explicit unknown state for missing timeframes.

No Worker deployment was required because Build 4 is a shared library and is not yet wired into live expert-gate weighting.

## What Build 4 does not do

It does not yet:
- decide whether M5/M15/H1/H4/D1 is bullish or bearish;
- attach a mini-environment to one timeframe expert;
- apply Build-3 historical trust to a live expert;
- replace the legacy marker brain;
- change Super Signals execution or owner 1% risk;
- grant live-money authority.

## Next build

**Build 5 — M5 Price Structure Expert**

Build 5 will be the first real timeframe mini-brain. It will consume the Build-4 primitives, define M5-specific environment dimensions, convert relevant primitives into versioned sub-calculator opinions, surface contradictions, emit one auditable M5 gate conclusion through the Build-2 contract, and attach Build-3 environment-specific trust.

No Build 6 work begins until Build 5 passes its acceptance gate.
