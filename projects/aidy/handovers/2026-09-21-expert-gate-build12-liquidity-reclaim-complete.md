# AIDY Expert-Gate Programme — Build 12 Liquidity / Reclaim Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 13 — Volatility / Jump Expert

## What was built

Build 12 adds `aidy_gold_liquidity_reclaim_expert_v1`.

It evaluates named high/low references from Build 11 using completed M1 OHLC and measures:
- level identity;
- penetration depth in USD and bps;
- reclaim speed in completed M1 bars;
- confirmation closes;
- retest and retest-hold;
- reclaim-candle rejection geometry;
- nearest competing-level distance;
- session, session phase and volatility context.

Only confirmed or retest-held reclaims can emit a directional proxy vote. No-sweep, unconfirmed penetration and failed reclaim cases remain neutral.

## Proxy / order-flow boundary

Every event is explicitly labelled:
- `proxy_not_order_flow=true`;
- `hidden_order_flow_claimed=false`.

Explanations state that OHLC sweep/reclaim logic is a price-action proxy and not genuine order flow.

Retrospective genuine GC-flow research is stored separately with:
- `used_in_ohlc_proxy_calculation=false`;
- `used_in_expert_conclusion=false`;
- `separate_from_ohlc_proxy=true`.

## Acceptance

AIDY PR #215 merged:
`68c793281811351ece20c3f66dc8af3413bdd8fe`

Final exact-candidate checks:
- Evidence Semantic Change Gate: PASS — run `35592648326`
- static checks: PASS
- focused workflow suite: 235 passed
- full repository regression: 1487 passed — run `35592648321`

Acceptance coverage included:
- high sweep/reclaim/retest;
- low sweep/reclaim;
- no-sweep neutral;
- failed reclaim neutral;
- penetration depth;
- reclaim speed;
- confirmation closes;
- retest/retest-hold;
- rejection geometry;
- competing-level distance;
- session/volatility trust-scope separation;
- fake-order-flow language protection;
- retrospective genuine GC-flow separation;
- gapped M1 fail-closed;
- PIT completed-bar provenance;
- chronological freeze.

## Production / execution status

No Worker deployment was required because Build 12 is an expert library and is not wired into live gate weighting.

Build 12 does not:
- change Super Signals execution;
- change provider activation;
- change owner 1% risk;
- replace the current live marker brain;
- enable formal-forward authority;
- grant live-money authority.

## Next build

**Build 13 — Volatility / Jump Expert**

Build 13 will classify:
- clock-normalised volatility percentile;
- compression/expansion transitions;
- continuous versus jump state;
- vol-of-vol;
- optional IV/RV relation when qualified.

It must remain direction-neutral, distinguish event-driven jumps from normal expansion when evidence supports that distinction, keep sparse GVZ/IV evidence UNKNOWN, and compare simple ATR bands against the richer regime model in ablation.

No Build 14 work begins until Build 13 passes its acceptance gate.
