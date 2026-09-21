# AIDY Expert-Gate Programme — Build 1 Environment Contract v3

**Date:** 2026-09-21  
**Status:** PRODUCTION VERIFIED  
**Next:** Build 2 — Expert Gate Contract v1

## What was built

Build 1 replaced the long-term environment spine with `aidy_gold_cycle_environment_v3`.

It adds:
- a canonical 34-dimension Gold environment registry;
- a compact shared `envcore_` identity;
- separate factor families for time/participation, structure, movement, location, liquidity, volatility, events, cross-market, regime and data quality;
- exact facts retained separately for audit;
- explicit 15-minute UTC clock buckets;
- weekend/pre/post-weekend and market-calendar state;
- explicit data-quality state;
- fail-closed rejection of labelled future/outcome fields;
- explicit UNKNOWN handling;
- removal of the old monolithic `full_environment` score scope.

Build 1 deliberately does **not** change the intelligence inside M5/M15/H1/H4/D1 gates yet.

## Why it matters

AIDY can now know the Gold environment first without making every cycle a near-unique combination. Later gates can attach smaller specialist mini-environments and build enough comparable history to learn which expert is useful under which conditions.

## Engineering acceptance

- semantic-change gate: PASS
- static checks: PASS
- focused market-data tests: PASS
- full repository regression: PASS, 1346 tests
- AIDY repo handoff merged

## Production proof

AIDY implementation commits:
- `2b42c3484254a7fd50508f8a2e201d6d652c353e`
- `968909df73eada5bc9603ea45894395b54ca2c9b`
- `3cab838f7f7308bbcd8827220ff68a64ea3352b9`
- final AIDY documentation/handoff: `847342903da2cc988ce61eb4ebb43ff96b420924`

Deploy run:
`35576676324`

Worker version:
`a20dcfe9-cd46-40c2-aef5-5d6c524cc6c1`

Live cycle proof:
- window: `2026-09-21T08:15:00+00:00`
- decision frozen: `2026-09-21T08:10:56.620000+00:00`
- environment version: `aidy_gold_cycle_environment_v3`
- schema: `aidy_gold_environment_contract_schema_v1`
- registered dimensions: 34
- `envcore_` key: present
- monolithic full-environment key: false
- legacy `full_environment` scopes: 0
- toolbox considered/trace/coverage: 34 / 34 / 34
- missing readable states: 0
- missing score contexts: 0
- future values used: 0
- live-money authority: 0
- formal-forward: OFF
- minute capture cron: present

## Next build

**Build 2 — Expert Gate Contract v1**

It will define the standard contract every mini-brain must use: identity/version, frozen global environment, specialist mini-environment, evidence references, sub-calculator outputs, direction or context-only/ABSTAIN/UNKNOWN, internal conviction, contradictions, readable explanation, scoreability, dependency family and no-hindsight attestation.

No Build 3 work should begin until Build 2 passes its own acceptance gate.
