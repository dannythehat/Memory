# AIDY Expert-Gate Programme — Build 19 Analogue / Episode Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 20 — Evidence Dependency & Double-Counting Engine

## What was built

Build 19 adds `aidy_gold_analogue_episode_expert_v1`.

It does not replace AIDY's existing memory stack. It composes:
- historical analogue retrieval v1;
- independent-episode retrieval v2;
- structural-epoch retrieval v3;
- semantic analogue qualification;
- Gold movement episode memory and learning cards.

Build 19 adds:
- exact PIT gate-state snapshots;
- environment-state similarity;
- immutable input-digest binding;
- outcome-blind re-ranking of already independent historical episodes;
- supporting analogue and counterexample groups;
- continuation/retrace distributions read only after selection;
- chronological holdout guardrails.

## Critical no-hindsight result

Changing only a historical case's future return from strongly positive to strongly negative leaves:
- selected source case identity unchanged;
- state similarity unchanged.

Only the post-selection classification changes from continuation to retrace.

That is the required boundary.

## Duplicate episodes

The existing v2 overlapping 240-minute episode logic remains authoritative. Build 19 consumes those independent representatives rather than allowing multiple snapshots from one underlying move to inflate evidence.

## Counterexamples

Build 19 deliberately preserves both:
- continuation/supporting analogues;
- retrace/counterexample analogues.

It never selects only the examples that support the current direction.

## Acceptance

- tested head: `87a793066af3ac0cb9855399416c0a01f55aa02d`
- PR #227 merge: `aba5ebc275646b31ec8132af3fed7179c1b5046f`
- repo handoff: `439780074aee6ec2a84ca30d5a399a1f8c4bc76e`
- semantic gate: PASS — `35610105748`
- acceptance workflow: PASS — `35610105516`
- focused tests: 115 passed
- dedicated chronological/counterexample gate: 5 passed
- full regression: 1591 passed

## Boundaries preserved

Build 19 does not:
- use future outcomes in similarity;
- tune on holdout;
- count overlapping cases as independent episodes;
- turn analogue history into automatic BUY/SELL authority;
- change Super Signals execution/provider rules;
- change owner 1% risk;
- create formal-forward or live-money authority.

## Next

**Build 20 — Evidence Dependency & Double-Counting Engine**

Objective: stop the same underlying Gold evidence from voting multiple times.

Acceptance must prove:
- exact duplicates do not double weight;
- highly correlated M5/M15/momentum inputs are damped;
- independent liquidity + macro + structure agreement remains distinct;
- removing one duplicate does not radically change the final score.
