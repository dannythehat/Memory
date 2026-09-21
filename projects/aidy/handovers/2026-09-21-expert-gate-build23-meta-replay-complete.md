# AIDY Expert-Gate Programme — Build 23 Chronological Replay, Ablation & Untouched Holdout

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 24 — Live Forward Shadow Soak & Permanent Scorecard

## What was built

Build 23 adds the `aidy_gold_meta_replay_*_v1` contracts.

It provides:
- immutable versioned replay cases;
- explicit separation of pre-outcome decision state and later evaluation-only outcome;
- chronological development, validation and untouched holdout windows;
- purge and embargo;
- frozen variant policy;
- legacy-vs-full comparison;
- every gate alone;
- full-minus-each-gate;
- dependency-on vs dependency-off;
- directional accuracy by class;
- +2/+1/-1/-2 impact score;
- Brier where confidence actually exists;
- coverage and abstention;
- environment-specific performance;
- time stability;
- incremental contribution;
- sample N.

## Anti-overfitting rules

Recommendations come from validation only.

Development cannot promote a gate merely because it looks good in-sample.

Holdout cannot tune thresholds, promote/prune gates or change recommendations.

A deliberately flashy development-only gate is rejected in the acceptance harness when it fails validation.

## Evidence boundary

The acceptance dataset is an explicitly labeled synthetic adversarial fixture.

It proves the replay/ablation/holdout machinery behaves correctly. It does **not** prove AIDY already has real-market predictive edge.

That prospective proof is Build 24.

## Acceptance

- PR #235 implementation merge: `12d5f0f17b6678a426890fd8bcd643d3984d1d27`
- corrective PR #237 tested head: `0c5e2f2a072e20e1671db13ac90f3ccce88cf11f`
- verified main: `5c370ac4182b96a8fb2d06be7927d8de141914a1`
- AIDY repo handoff: `0d71792813a12b62f70e2999058b7ba7780e1943`
- semantic gate: PASS — `35619195958`
- acceptance workflow: PASS — `35619195819`
- focused replay tests: 54 passed
- dedicated adversarial replay tests: 6 passed
- full regression: 1652 passed

## Boundaries preserved

Build 23 does not:
- claim real-market edge from the synthetic fixture;
- use holdout for tuning;
- use future values for prediction;
- create formal-forward authority;
- create live-money authority;
- change Super Signals execution/provider rules;
- change owner 1% risk.

## Next

**Build 24 — Live Forward Shadow Soak & Permanent Scorecard**

This is the final planned build. It will persist each fresh eligible cycle's:
- environment;
- all gate packets;
- sub-calculator outputs;
- pre-outcome selector/trust state;
- final AIDY research view;
- later resolved outcome;
- score updates.

That is where AIDY begins accumulating the real prospective evidence needed for serious market study.
