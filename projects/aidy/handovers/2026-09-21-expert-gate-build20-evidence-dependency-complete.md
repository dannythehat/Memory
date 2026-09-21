# AIDY Expert-Gate Programme — Build 20 Evidence Dependency & Double-Counting Engine

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 21 — Environment-Aware Gate Selector

## What was built

Build 20 adds `aidy_gold_evidence_dependency_engine_v1`.

It consumes the dependency metadata that earlier expert builds already emit.

Declared roots include:
- `price_action`: structure, momentum, location;
- `macro_information`: event, rates/USD, cross-market, news;
- `liquidity_mechanism`: liquidity;
- `participation_flow`: session participation and futures microstructure;
- `volatility_regime`: volatility;
- `analogue_memory`: analogue;
- `data_quality`: data quality.

## Exact duplicates

Two signals with the same evidence identity and the same vote do not get two votes.

The strongest representative is retained and the duplicate contributes zero incremental weight.

Removing that duplicate leaves the dependency-adjusted research score unchanged.

## Correlated price evidence

M5 structure, M15 structure and momentum can all be telling AIDY about the same price move.

Build 20:
- uses declared family/correlation-group relationships;
- computes rolling correlation from prior signal states only;
- excludes current/future rows;
- uses no realised outcome field;
- dampens high same-parent correlation;
- caps all incremental evidence under one parent root.

Five price-derived votes therefore cannot become five independent votes.

## Independent agreement

Liquidity, macro information and price structure remain distinct roots.

A bounded independent-root bonus exists only when at least three genuinely distinct roots agree. Same-root duplication cannot qualify for the bonus.

## Acceptance

- tested head: `b5cf46b5751cb9a9f7dc565b88bd08dccf3810d4`
- PR #229 merge: `35de6056cbbbdde2309a2185c07914f7df375797`
- AIDY repo handoff: `0fd8728d3686babd88849933cce38d6486da65c2`
- semantic gate: PASS — `35611781415`
- acceptance workflow: PASS — `35611781428`
- focused tests: 144 passed
- dedicated double-counting gate: 5 passed
- full regression: 1607 passed

## Boundaries preserved

Build 20 does not:
- use realised outcomes to estimate current dependency;
- create a live BUY/SELL decision;
- choose which gate is trusted in the current environment;
- change Super Signals execution/provider rules;
- change owner 1% risk;
- create formal-forward or live-money authority.

## Next

**Build 21 — Environment-Aware Gate Selector**

Build 21 will take:
- Build-3 contextual trust;
- sample size/shrinkage;
- calibration;
- recency/drift;
- Build-20 dependency multipliers;

and produce the current high-trust, reduced-trust and unavailable gate set with exact reasons.
