# AIDY Expert-Gate Programme — Build 2 Expert Gate Contract v1

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 3 — Conditional Trust & Score Engine v3

## What was built

Build 2 adds the standard expert-gate packet contract:

`aidy_gold_expert_gate_contract_v1`

Every later mini-brain must now produce the same auditable structure:
- gate identity/version/mode/dependency family;
- exact as-of and target horizon;
- verified frozen Environment v3 reference;
- full shared environment dimensions plus a smaller specialist mini-environment;
- timestamped evidence inputs with source, path, state, value and provenance;
- versioned sub-calculator outputs with role, state, vote, strength, scoreability and evidence refs;
- explicit bullish/bearish/neutral/context-only/abstain/unknown conclusions;
- current internal conviction separate from historical reliability;
- structured contradictions;
- structured readable explanation with source refs;
- no-hindsight attestation;
- research-only=true;
- live-money authority=false;
- immutable packet/evidence/calculator/mini-environment digests.

## Fail-closed rules

The contract rejects:
- future-dated evidence;
- labelled future/outcome fields;
- unknown evidence masquerading as a known calculation;
- context-only gates emitting bullish/bearish conclusions;
- directional conclusions without a matching scoreable sub-calculator;
- explanation text that does not cite a real evidence input or calculator;
- mutated packet/evidence/calculator/mini-environment digests.

Missing evidence can remain UNKNOWN. Known but conflicting evidence can ABSTAIN. Context experts are not forced into fake directional opinions.

## Acceptance

AIDY PR #202 merged:
`95f1bbfbfe845ca95c6c766b16d87c42468da4f6`

Final exact-head acceptance:
- Evidence Semantic Change Gate: PASS
- static checks: PASS
- focused workflow tests: 108 passed
- full repository regression: 1360 passed
- acceptance workflow: `35578111443`

No production Worker deploy was required because Build 2 is a foundation contract library and does not yet alter live gate reasoning, scoring or weighting.

## What Build 2 does not do

It does not yet:
- make H1/M15/etc smarter;
- assign historical reliability percentages;
- change live AIDY weights;
- change current Super Signals execution;
- change owner 1% risk;
- grant live-money authority.

Those happen only in later accepted builds.

## Next build

**Build 3 — Conditional Trust & Score Engine v3**

Build 3 will attach environment-specific history to each gate and scoreable sub-calculator, preserve +2/+1/0/-1/-2 outcomes, shrink small samples toward broader priors, and back off from exact mini-environment -> reduced context -> gate global when history is thin.

No Build 4 work begins until Build 3 passes its acceptance gate.
