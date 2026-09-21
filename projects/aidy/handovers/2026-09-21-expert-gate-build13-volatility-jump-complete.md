# AIDY Expert-Gate Programme — Build 13 Volatility / Jump Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 14 — Session / Participation Expert

## What was built

Build 13 adds:

`aidy_gold_volatility_jump_expert_v1`

This expert is direction-neutral. It changes context and trust, not BUY/SELL direction.

It measures:
- completed-M1 15-minute realised volatility;
- clock-normalised volatility percentile using prior observations from the same UTC 15-minute slot;
- compression, expansion and compression-to-expansion transitions;
- qualified PIT jump-versus-continuous state;
- event-proximate jump state without causal event claims;
- qualified vol-of-vol;
- optional GVZ and IV/RV context only when PIT-qualified;
- a simple M15 ATR/RV band retained as the ablation baseline.

## Unknowns and qualification

Sparse or unqualified GVZ/IV evidence remains UNKNOWN.

Retrospective volatility evidence cannot silently enter PIT context.

GVZ remains explicitly a cross-instrument GLD volatility proxy rather than direct XAUUSD options IV.

## Event-proximate jump

A jump-dominant state near a scheduled event is labelled `event_proximate_jump`.

That label is descriptive only:
- event proximity is used;
- event causation is not asserted;
- volatility context still cannot vote direction.

## Ablation

Build 13 retains the simpler M15 ATR/RV band and provides:

`summarise_volatility_regime_ablation`

The richer regime earns no automatic influence from complexity. It must beat the simple ATR baseline over a sufficient historical sample before later fusion may consider extra weight.

## Acceptance

AIDY PR #216 merged:
`6e9b42eb98c0b624c13273cb76bccd82ac4e1c53`

Final exact-candidate checks:
- Evidence Semantic Change Gate: PASS — run `35593633108`
- static checks: PASS
- focused workflow suite: 249 passed
- full repository regression: 1501 passed — run `35593633054`

Acceptance coverage included:
- direction-neutral contract;
- clock-normalised percentile;
- compression-to-expansion transition;
- continuous expansion versus jump;
- event-proximate jump without causal claim;
- jump outside event window;
- sparse GVZ/IV UNKNOWN handling;
- qualified vol-of-vol;
- retrospective/unqualified external state exclusion;
- simple ATR baseline retention;
- rich-versus-simple ablation;
- insufficient-sample no-promotion;
- PIT completed-bar provenance;
- chronological freeze.

## Production / execution status

No Worker deployment was required because Build 13 is an expert library and is not wired into live gate weighting.

Build 13 does not:
- change Super Signals execution;
- change provider activation;
- change owner 1% risk;
- replace the current live marker brain;
- enable formal-forward authority;
- grant live-money authority.

## Next build

**Build 14 — Session / Participation Expert**

Build 14 will quantify who is likely active and whether current activity is unusual for this time using:
- DST-safe sessions;
- session phase;
- overlap;
- weekday-clock volatility/range baselines;
- historical GC volume/spread baselines where available.

Acceptance requires DST-transition tests, clock-slot baselines, explicit event-time confounding and no hardcoded session-direction rules such as “London bullish.”

No Build 15 work begins until Build 14 passes its acceptance gate.
