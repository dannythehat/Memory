# AIDY Expert-Gate Programme — Build 17 Futures / Microstructure Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 18 — News / Movement Mechanism Expert

## What was built

Build 17 adds `aidy_gold_futures_microstructure_expert_v1`.

It is a research-only futures/microstructure specialist using genuine historical COMEX GC information:
- exchange trade volume;
- known-side aggressor flow, with unknown aggressor side left UNKNOWN;
- pre-trade BBO spread;
- trade-price/size VWAP;
- anchored/session VWAP and VWAP distance;
- weekday × clock-normalized microstructure state;
- official CME daily open-interest / active-contract / roll state;
- explicit entitlement boundaries;
- no full-depth/order-book-imbalance claim.

## Genuine Phase-A holdout

The final acceptance path used genuine Databento GC TBBO plus the existing historical XAUUSD spot-OHLC research history.

Frozen experiment structure:
- valid weekly episodes: 61;
- normalization: 20;
- development: 10;
- embargo: 1;
- untouched holdout: 30;
- holdout tuning: forbidden;
- purge: required;
- embargo: required.

The microstructure rule catalogue was small and preregistered. Rule selection used development episodes only.

Selected rule:
`override_1p5_0p5`

Untouched holdout result:
- spot-only accuracy: **20.0000%**;
- spot + microstructure accuracy: **23.3333%**;
- incremental accuracy: **+3.3333 percentage points**;
- state: `incremental_value_observed`.

That is enough to satisfy the Build-17 blueprint requirement for genuine retrospective incremental value beyond spot OHLC.

It is **not** a claim of statistical validation or production trading edge.

## Acceptance evidence

Core implementation:
- PR #220 merge: `f6ac451c90ae49f5bbe795af5a25757b65afb8ce`

Genuine holdout:
- PR #223 exact tested head: `ca49a6dd541ec17b09b11b25604722d7ef256b32`
- PR #223 merge: `b1e6e2f491c1cf31fdb30a94a88929e4f092fc18`
- acceptance workflow: `35605952385`
- semantic gate: `35605952419`
- focused suite: 313 passed
- full repository regression: 1565 passed
- quoted Databento research spend: $0.148881077766

Repository handoff:
- AIDY documentation merge: `a350b23cf656f9518ac2407af2253ccd8f687dbb`

## Boundaries preserved

Build 17 does not:
- activate a paid/live Databento subscription;
- claim L2/L3/MBO/MBP10/full-depth information;
- become statistically validated from this one holdout;
- create formal-forward evidence;
- grant a live gate weight;
- change Super Signals execution/provider rules;
- change the owner's 1% risk directive;
- grant live-money authority.

Phase B live/delayed microstructure remains a separate future entitlement/pricing/PIT decision and is not automatically authorized by Phase A passing.

## Next build

**Build 18 — News / Movement Mechanism Expert**

Objective:
explain abnormal Gold movement without inventing causality.

It will reuse the existing movement investigator and scheduled-event evidence and, only where a valid source contract exists, add official/breaking-news evidence with source authority, timestamps, duplicate-story collapse and agreement/disagreement handling.

Acceptance requires:
- scheduled-event fixture;
- credible-news fixture;
- unsupported-narrative fixture;
- UNKNOWN fixture;
- disagreement remains unresolved rather than fabricated;
- news context does not automatically become direction.

No Build 19 work begins until Build 18 passes its acceptance gate.
