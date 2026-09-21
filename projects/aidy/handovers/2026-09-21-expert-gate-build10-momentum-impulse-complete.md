# AIDY Expert-Gate Programme — Build 10 Momentum / Impulse Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 11 — Price Location Expert

## What was built

Build 10 adds:

`aidy_gold_momentum_impulse_expert_v1`

The expert uses exact completed M1 history to distinguish genuine continuation momentum from noisy or concentrated movement.

It measures:
- 1/5/15/30/60-minute returns;
- realised-volatility-normalised movement;
- path persistence;
- path efficiency;
- recent-vs-prior 5-minute acceleration/deceleration;
- multi-horizon agreement;
- continuation impulse versus persistent drift versus noisy/unconfirmed movement;
- single-bar concentration and exhaustion risk.

## One-large-candle protection

A large final M1 candle cannot become sustained momentum by itself.

If the move is concentrated in one bar while persistence is weak:
- the impulse/drift classifier stays noisy/unconfirmed;
- an exhaustion/reversal hypothesis can be emitted;
- same-direction continuation cannot be promoted merely because raw returns across several horizons now point the same way.

## Regime and clock normalisation

Momentum reliability is conditioned on:
- volatility state;
- session;
- session phase;
- 15-minute UTC clock bucket;
- recent five-minute distribution/range state.

Build-3 trust scopes therefore learn separately across different volatility/clock environments.

## Correlation control

All price-derived momentum calculators carry:
- an explicit correlation group;
- `later_penalty_tag=correlated_price_expert_input`.

This records overlap with the earlier price-structure experts so a later fusion build can penalise shared evidence instead of double-counting it.

## Data quality / PIT safety

Build 10 requires:
- 61 contiguous completed M1 bars;
- no gaps across the required path;
- completed-bar provenance;
- frozen as-of alignment with the global environment.

Missing, insufficient or gapped M1 evidence fails closed to UNKNOWN.

## Acceptance

AIDY PR #213 merged:
`50b692c4ecf2f775a2f445bf69ea1578b0fd5bae`

Final exact-candidate checks:
- Evidence Semantic Change Gate: PASS — run `35588709979`
- static checks: PASS
- focused workflow suite: 211 passed
- full repository regression: 1463 passed — run `35588709994`

Acceptance coverage included:
- clean bullish continuation impulse;
- clean bearish continuation impulse;
- one large final candle does not equal persistent momentum;
- choppy/noisy direction rejection;
- gapped M1 fails closed;
- insufficient M1 fails closed;
- volatility-regime trust-scope separation;
- clock-bucket trust-scope separation;
- price-expert correlation tagging;
- PIT completed-bar provenance;
- chronological freeze;
- Build-3 conditional trust.

## Production / execution status

No Worker deployment was required because Build 10 is an expert library and is not yet wired into live gate weighting.

Build 10 does not:
- change Super Signals execution;
- change provider activation;
- change owner 1% risk;
- replace the current live marker brain;
- enable formal-forward authority;
- grant live-money authority.

## Next build

**Build 11 — Price Location Expert**

Build 11 answers where Gold is, not merely where it is moving.

It will use:
- prior-day references;
- Asia references;
- active-session references;
- opening ranges;
- confirmed swings;
- recent extrema;
- round numbers;
- ATR-normalised distance.

Acceptance requires exact nearest-level calculations, auditable reference priority, explicit confluence/conflict representation, and no directional vote unless a separately tested location-reaction rule exists.

No Build 12 work begins until Build 11 passes its acceptance gate.
