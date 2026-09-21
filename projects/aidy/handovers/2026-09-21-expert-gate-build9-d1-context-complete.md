# AIDY Expert-Gate Programme — Build 9 D1 Context Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 10 — Momentum / Impulse Expert

## What was built

Build 9 adds:

`aidy_gold_d1_context_expert_v1`

D1 is deliberately context-only.

It can describe:
- daily trend;
- daily structure;
- macro-location;
- breakout state;
- data freshness and completeness.

It cannot:
- emit a BUY/SELL conclusion;
- force a 15-minute direction;
- receive default short-horizon weight;
- grant live-money authority.

## Freshness and completeness

Daily context is withheld when:
- the latest completed D1 evidence is older than 72 hours;
- required daily trend/location inputs are materially incomplete;
- D1 evidence is missing.

Confirmed daily swing structure is treated separately from core context completeness. This means a valid daily trend/location context can still be used before enough pivot history exists for confirmed swing/breakout structure. Those unavailable components remain UNKNOWN rather than invalidating the whole D1 context layer.

## Context value versus direct forecast value

Build 9 explicitly evaluates:
1. whether adding D1 context improves another forecast; and
2. whether D1 direction itself would have been correct.

These are separate metrics. Direct D1 directional accuracy never grants direct 15-minute authority.

## Acceptance

AIDY PR #212 merged:
`e0fe9a8e0e91bfeacbade687a70746ad51165586`

Final exact-candidate checks:
- Evidence Semantic Change Gate: PASS — run `35587798686`
- static checks: PASS
- focused workflow suite: 199 passed
- full repository regression: 1451 passed — run `35587798625`

Acceptance coverage included:
- fresh complete D1 context;
- stale D1 -> ABSTAIN;
- partial D1 -> ABSTAIN;
- missing D1 -> ABSTAIN;
- strong D1 trend cannot force a 15m direction;
- context-value metric separate from direct forecast metric;
- minimum-sample requirement for context-value proof;
- PIT completed-bar provenance;
- no-future-values;
- chronological freeze;
- Build-3 conditional trust;
- context-only dependency metadata.

## Production / execution status

No Worker deployment was required because Build 9 is a context library and is not wired into live gate weighting.

Build 9 does not:
- change Super Signals execution;
- change provider activation;
- change owner 1% risk;
- replace the current live marker brain;
- enable formal-forward authority;
- grant live-money authority.

## Next build

**Build 10 — Momentum / Impulse Expert**

Build 10 distinguishes continuation-quality momentum from noisy direction using:
- 1/5/15/30/60m returns;
- volatility-normalised returns;
- acceleration;
- persistence;
- path efficiency;
- impulse versus drift;
- exhaustion;
- multi-horizon agreement.

Acceptance requires proving that one large candle does not automatically equal persistent momentum, testing regime/clock normalisation, and tagging correlated price-expert influence for later penalty.

No Build 11 work begins until Build 10 passes its acceptance gate.
