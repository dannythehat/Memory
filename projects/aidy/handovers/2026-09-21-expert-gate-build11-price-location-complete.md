# AIDY Expert-Gate Programme — Build 11 Price Location Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 12 — Liquidity / Reclaim Expert

## What was built

Build 11 adds `aidy_gold_price_location_expert_v1`, a context-only location brain.

It combines frozen cycle-start references with completed-bar structure:
- prior-day high/low/close;
- Asia overnight range;
- active-session high/low;
- 15m/30m/60m opening ranges;
- confirmed M15/H1 swings;
- recent M5/M15 20/50-bar extrema;
- deterministic $10/$50 round numbers.

Every reference carries exact:
- level;
- side of current price;
- USD distance;
- bps distance;
- ATR-normalised distance.

## Nearest versus important

Build 11 deliberately separates:
- **geometric nearest**: the closest measured level by exact USD distance;
- **structural priority**: the highest-priority structural level using an exposed tier/reason policy.

The closest level therefore cannot silently become the “most important” level.

## Confluence and conflict

References within 0.25 ATR are grouped into confluence clusters.

If relevant nearby levels exist on both sides of price within 0.50 ATR, the expert records explicit bracketing conflict instead of pretending location has a clean directional implication.

## Directional safety

The gate is context-only.

Location alone:
- cannot emit bullish/bearish;
- has no internal directional conviction;
- cannot claim reaction edge;
- requires a separately defined and tested reaction rule before it may affect direction.

## Acceptance

AIDY PR #214 merged:
`8b3400ecb569b6b0990c899f0b15440f73f4eb73`

Final exact-candidate checks:
- Evidence Semantic Change Gate: PASS — run `35591189620`
- static checks: PASS
- focused workflow suite: 223 passed
- full repository regression: 1475 passed — run `35591189552`

Acceptance coverage included:
- exact nearest-level arithmetic;
- separate structural priority;
- multi-category confluence;
- two-sided nearby-level conflict;
- descriptive-only round numbers;
- ATR-normalised distance;
- missing mid -> context UNKNOWN;
- PIT/no-future;
- chronological freeze;
- Build-3 context-specific trust.

## Production / execution status

No Worker deployment was required because Build 11 is an expert library and is not wired into live gate weighting.

Build 11 does not:
- change Super Signals execution;
- change provider activation;
- change owner 1% risk;
- replace the current live marker brain;
- enable formal-forward authority;
- grant live-money authority.

## Next build

**Build 12 — Liquidity / Reclaim Expert**

Build 12 will make sweep/reclaim reasoning measurable using level identity, penetration depth, reclaim speed, confirmation closes, retest, rejection geometry, competing-level distance and session/volatility context.

OHLC sweep logic must remain explicitly labelled as a proxy and must never be described as genuine order flow.

No Build 13 work begins until Build 12 passes its acceptance gate.
