# AIDY Expert-Gate Programme — Build 15 Macro / Event Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 16 — Rates / USD / Cross-Asset Expert

## What was built

Build 15 adds `aidy_gold_macro_event_expert_v1`.

It is a Gold-specific, context-only macro/event specialist layered on the already accepted official event intelligence stack.

It adds:
- strict as-of schedule visibility;
- pre-event Gold features with no future-actual access;
- first-print surprise from PIT-known consensus plus revision-index-0 actual only;
- later revisions retained separately;
- standardized surprise only when enough independent same-unit PIT history exists;
- Gold-learned event tiers from independent Gold episodes;
- event clustering within 30 and 60 minutes;
- completed-M1 post-release Gold confirmation;
- historical conditional Gold response by event class and surprise direction;
- matched no-news controls;
- event-versus-no-news comparison;
- Build-3 conditional trust.

## Timing boundary

Actuals are invisible until their own `first_observed_at`.

A release scheduled at 12:30:00 cannot expose an actual first observed at 12:30:03 to a 12:30:00 or 12:30:02 cycle.

This is directly acceptance-tested.

## First print versus revision

Only revision index 0 defines the first-print surprise.

Later revisions:
- remain visible as revisions once observed;
- do not replace the first-print surprise;
- stay separate from the original event print.

## Gold event tiers

Event tiers come from the preregistered Day-29 independent Gold-episode study.

Build 15 does not use:
- vendor high-impact labels;
- trade P/L;
- win rate;
- provider outcomes.

Sparse event classes remain unclassified.

## Standardized surprise

Raw surprise is standardized only when:
- event class matches;
- unit matches;
- historical rows are PIT-reconstructable;
- rows were first observed before the current as-of;
- independent episode identities are unique;
- at least the minimum historical sample exists.

Otherwise standardized surprise remains UNKNOWN.

## Post-release confirmation

Post-release confirmation uses only completed M1 Gold bars available as of the frozen cycle.

It can describe:
- forming;
- muted;
- Gold up;
- Gold down.

This remains context, not an automatic trading direction.

## No-news control

Build 15 requires an independent matched no-news control before comparing historical event movement with ordinary background movement.

Insufficient control history returns UNKNOWN.

## Acceptance

AIDY PR #218 merged:
`ce9ff0a8f021c062aba05440b112c5f8cf2e0518`

Final exact-candidate checks:
- Evidence Semantic Change Gate: PASS — run `35596090199`
- static checks: PASS
- focused workflow suite: 276 passed
- full repository regression: 1528 passed — run `35596090200`

Acceptance coverage included:
- context-only / zero direct macro-direction rule;
- pre-event actual leakage blocked;
- actual enters only after first-observed timestamp;
- first-print/revision separation;
- standardized surprise from PIT history only;
- independent Gold event tiering;
- no vendor importance label;
- event cluster measurement;
- completed-bar post-release confirmation;
- independent conditional response;
- matched no-news control;
- insufficient no-news UNKNOWN;
- PIT chronological freeze;
- future historical rows excluded;
- unknown-at-as-of schedules rejected.

## Production / execution status

No Worker deployment was required because Build 15 is an expert library and is not wired into live gate weighting.

Build 15 does not:
- change Super Signals execution;
- change provider activation;
- change owner 1% risk;
- replace the current live marker brain;
- enable formal-forward authority;
- grant live-money authority.

## Next build

**Build 16 — Rates / USD / Cross-Asset Expert**

Build 16 will model Gold's opportunity-cost and risk mechanisms using:
- broad USD;
- DGS2;
- DGS10;
- DFII10;
- T10YIE;
- policy-path research;
- SI / ES / VIX / EURUSD / USDJPY when qualified.

It will add:
- multi-horizon changes;
- rolling Gold beta/correlation;
- relationship-stability state;
- divergence state;
- cross-asset breadth/agreement.

Acceptance requires that changing sign relationships are representable, stale daily series cannot masquerade as intraday reaction, same-mechanism series are dependency-tagged, and no permanent Gold-vs-USD/rates sign is hardcoded.

No Build 17 work begins until Build 16 passes its acceptance gate.
