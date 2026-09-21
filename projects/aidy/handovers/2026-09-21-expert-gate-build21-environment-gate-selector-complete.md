# AIDY Expert-Gate Programme — Build 21 Environment-Aware Gate Selector

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 22 — AIDY Meta Direction Aggregator & Explanation

## What was built

Build 21 adds `aidy_gold_environment_gate_selector_v1`.

It consumes:
- frozen Build-2 expert packets;
- Build-3 contextual trust envelopes;
- the exact current Build-1 environment;
- Build-20 dependency adjustments;
- optional historical calibration summaries observed before the current cycle.

## Selection logic

For every expected gate, Build 21:
- reads the most specific qualified Build-3 trust scope;
- respects Build-3 hierarchical shrinkage;
- applies sample confidence;
- applies scope backoff when exact context is unavailable;
- applies historical calibration quality;
- applies recent drift state;
- applies Build-20 dependency penalty;
- returns high-trust, reduced-trust or unavailable;
- explains the exact reason.

The selector score is an engineering attention score, not a probability of being correct.

## Safety / learning behavior

Small-N star performers cannot leap to high trust merely because their raw win rate looks perfect.

Weak gates are not deleted. They keep a low observation weight so AIDY can continue scoring them and learn if their usefulness changes.

Unavailable gates get zero authority.

Context-only gates can remain visible to Build 22 but receive zero directional authority.

Current outcome fields are rejected.

## Acceptance

- tested head: `a5f4892909d5eeaffb7143a2d579c0e12eea528d`
- PR #231 merge: `49632b75c773b207f857e23387e4f7ec5428fe52`
- AIDY repo handoff: `9c217699b15e089af78b9f8925d514ea606cb6fd`
- semantic gate: PASS — `35613740343`
- acceptance workflow: PASS — `35613740266`
- focused tests: 84 passed
- dedicated selector gate: 6 passed
- full regression: 1622 passed

## Boundaries preserved

Build 21 does not:
- see the current outcome;
- invent a final Gold direction;
- delete weak gates from learning;
- grant unavailable gates authority;
- change Super Signals execution/provider rules;
- change owner 1% risk;
- create formal-forward or live-money authority.

## Next

**Build 22 — AIDY Meta Direction Aggregator & Explanation**

Build 22 will take the selected gate set and produce one traceable 15-minute research view:
- bullish / bearish / neutral / abstain;
- confidence only when evidence supports calibration;
- supporting gates;
- contradictions;
- environment;
- gate trust and sample N;
- dependency adjustment;
- readable explanation.

Every contribution must remain traceable and context-only gates must never be forced into directional votes.
