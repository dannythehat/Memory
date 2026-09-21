# AIDY expert-gate Build 24 — live forward shadow closeout

Date: 2026-09-21

Status at draft time: **engineering complete; final delayed live score proof running**

## Build

Build 24 — Live Forward Shadow Soak & Permanent Scorecard

This is the final planned numbered build in the 24-build expert-gate programme.

## What was implemented

AIDY now has a prospective-only shadow runtime tied to the existing fresh 15-minute Gold cycle.

Every eligible cycle after the persisted Build-24 activation boundary stores:
- the exact frozen cycle/environment identity;
- all 15 expected expert-gate identities;
- gate packets and sub-calculators;
- pre-outcome conditional trust;
- Build-20 dependency state;
- Build-21 environment-aware selector state;
- Build-22 final AIDY research view;
- the later outcome only after the target window resolves;
- post-outcome gate/subcalculator/meta scores;
- permanent environment-specific scorebook state.

The permanent scorecard exposes mini-environment, N, raw/shrunk reliability, net score, drift, uncertainty, dependency adjustment, calibration/current trust and last score time.

## Live source honesty

The current admitted live PIT stack can genuinely compute the price/structure/location/momentum/liquidity/volatility/session experts.

The current live source contract does not yet connect all accepted research feeds into every fresh cycle. Macro/event, rates/USD/cross-asset, futures/microstructure, news/mechanism and analogue/episode therefore remain explicit UNKNOWN context gates in Build 24. They receive zero invented directional authority.

This is intentional. A missing source is not substituted with retrospective data.

## Prospective / no-hindsight boundary

- activation is written before a Build-24 cycle can qualify;
- cycles decided before activation are excluded rather than backfilled;
- all pre-outcome expert/dependency/selector/meta artifacts bind to the already-admitted snapshot at T;
- the scorecard never feeds back into the private-forward input builder;
- scoring reads only the later existing Gold-cycle outcome;
- frozen packets are not rewritten after the outcome;
- inserts are idempotent under restart/retry.

## Engineering evidence

AIDY PR #238  
Exact tested head: `a0b8710abc3fe4ea569deed868ea6538294169ad`  
Implementation merge: `6644892d12be6ae497f07db2a69119eaa58e0d27`

- semantic gate: run `35623113461` PASS
- Build-24 acceptance: run `35623113260` PASS
- focused/component tests: **103 passed**
- full repository regression: **1664 passed**
- Day-53 feed and safety checks on exact head: PASS

Public live Worker after merge:
- Build-24 shadow version: `aidy_gold_expert_shadow_v1`
- scorecard version: `aidy_gold_expert_scorecard_v1`
- capture: ON
- Twelve Data/public-independent
- Provider Context: fresh
- formal-forward: OFF

## Final live acceptance

PR #239 / run `35623618474` was created specifically to prove the genuine prospective path.

Already passed at draft time:
- migration/schema;
- deploy;
- Worker health/safety;
- first genuine post-activation shadow cycle;
- all 15 expected gate identities present.

The delayed outcome/score step is intentionally still running at draft time. Do not merge this Memory closeout or call Build 24 complete until that step is PASS and its exact realised-cycle evidence is copied below.

## Authority boundary

- research/shadow only;
- AIDY formal-forward authority OFF;
- AIDY live-money execution authority OFF;
- Super Signals execution/provider rules unchanged;
- owner 1% risk unchanged.

Passing Build 24 starts the permanent prospective soak/learning programme. It does not by itself claim profitable predictive edge.

