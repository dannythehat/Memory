# Super Signals Day 14 — RESEARCH GOVERNANCE

Date: 2026-09-07
Status: **ENGINEERING GREEN / PRODUCTION VERIFIED — governance remains fail-closed pending owner threshold approval and forward evidence**

## Production proof

- Delivery PR: `#150`.
- Final delivery head: `d4eee9db9c07db7f9713fbd480d47fb6bd7e8c94`.
- Final head checks: `api` success, `web` success, Workers success.
- Workers build ID: `171ff85d-bab0-4995-8494-6bad9ed11548`.
- Workers version: `1f2e575a-bf80-408c-9869-f5445348f748`.
- Production merge SHA: `3b8ac88c5b248c6d9f2fb0718b2062b58d5e77cd`.
- Render deploy: `dep-dafbjhks728c738nrdu0` — `live`.
- Migration: `0063_provider_day14_governance`.
- New Render instance `srv-d9qmcgks728c73a555m0-8xcpk` repeatedly returned `/health` 200 after cutover.
- Production Day 14 run: `29ccf16a-3da4-41dc-8e09-dfb7ab99be01`.
- Evidence digest: `0e4d697bb2c9629dfee6667c4d102f5b92fb8d780ff53e4216272932a7cce8b6`.

## What Day 14 built

Day 14 implements evidence-backed provider research governance for the 40 shadow discovery providers only. It uses the existing `provider_research_profiles` state model instead of creating a parallel rollout state machine:

`learning → shadow → qualified`

`qualified` means **paper-research eligibility only**. It has no authority over `sources.status`, broker/member routing, position sizing, MetaAPI or real-money execution. A separate explicit human live gate remains mandatory outside this subsystem.

The research scanner was also made compatible with governance: later scans preserve governance-owned `shadow`, `qualified` and `rejected` states instead of overwriting them back to `learning` while refreshing language/style/duplicate evidence.

## Governance policy

Migration `0063_provider_day14_governance` persists policy `provider_day14_policy_v1` with builder recommendations:

- minimum OOS N: **30**;
- minimum tested fingerprint cells: **1**;
- confidence level: **0.95**;
- OOS window: `since_day13_preregistration`;
- approval status: `PROPOSED_UNAPPROVED`;
- owner-approved timestamp: `null`;
- human live gate required: `true`;
- `research_only=true`;
- `live_money_execution_allowed=false`.

No owner approval is inferred from the instruction to build/complete Day 14. Until explicit approval is recorded, promotion is fail-closed.

## Evidence input

Day 14 consumes the refreshed Day 13 research evidence abstraction, not broker truth. The Day 13 refresh used by the production run was:

- run: `d5012961-b09d-4be3-b1ae-db2486a20e11`;
- code SHA: `3b8ac88c5b248c6d9f2fb0718b2062b58d5e77cd`;
- completed: `2026-09-07T13:20:55.329761Z`;
- frozen OOS boundary preserved: `2026-09-07T10:50:52.042190Z`;
- eligible OOS trades: **0**;
- tested hypotheses: **0**;
- BH rejections: **0**;
- builder-gate candidates: **0**;
- authoritative discoveries: **0**;
- engineering: `ENGINEERING_PROVEN`;
- statistical status: `WAITING-FOR-FORWARD-EVIDENCE`;
- threshold status: `PROPOSED_UNAPPROVED`;
- evidence digest: `8b6873c76b2c1cee5a37866a2048d967865be189ec26e526a0673b88ed61a7ea`.

Existing pre-preregistration history is not recycled to manufacture Day 14 evidence.

## Real production Day 14 result

Run `29ccf16a-3da4-41dc-8e09-dfb7ab99be01` completed at `2026-09-07T13:21:00.927675Z` with:

- model: `provider_day14_v1`;
- policy: `provider_day14_policy_v1`;
- policy approval: `PROPOSED_UNAPPROVED`;
- engineering: `ENGINEERING_PROVEN`;
- deterministic governance simulation acceptance: **passed**;
- governance status: `WAITING-FOR-OWNER-THRESHOLD-APPROVAL`;
- shadow providers: **40**;
- HOLD: **39**;
- RETEST: **1**;
- PROMOTE: **0**;
- DEMOTE: **0**;
- research-state transitions: **0**;
- paper-qualified: **0**;
- authoritative live transitions: **0**;
- `research_only=true`;
- `live_money_execution_allowed=false`.

The 40 persisted result rows were verified:

- 40/40 `research_only=true`;
- 40/40 `live_money_execution_allowed=false`;
- 40/40 `authoritative_live_transition=false`;
- 0 research-state transitions;
- 0 paper-qualified rows.

Disposition:

- 39 `learning` providers → `HOLD`, evidence state `INSUFFICIENT_OOS`;
- 1 `duplicate_review` provider → `RETEST`, evidence state `INSUFFICIENT_OOS`.

Source status remained unchanged at 40 shadow / 5 testing / 14 paused / 4 revoked. Shadow research states remained 39 learning / 1 duplicate_review.

## Safety boundaries

- 40 shadow providers only; five testing/real providers excluded from this governance population.
- No `broker_deals` input.
- No MetaAPI call.
- No source execution-status mutation.
- No routing or sizing mutation.
- No AIDY/D1 write.
- No automatic live activation.
- `qualified` is paper-research only.
- Human live gate remains outside Day 14 and mandatory.
- Day 13 preregistration/OOS boundary remains authoritative.

## Runtime note

One outgoing Day 13 instance attempted to restart after the shared database had advanced to migration `0063` and could not recognize that newer revision; it was the superseded instance and stopped serving during cutover. The live Day 14 instance continued returning health 200s.

A separate pre-existing shadow fallback evaluator error, `legacy provider profile state cannot be score eligible`, was observed repeatedly before PR #150 and also after cutover. It fails safely and did not change the Day 14 governance run, source statuses or research states. It is not Day 14 evidence and was not introduced by Day 14.

## Acceptance interpretation

**Day 14 engineering is GREEN and production verified.**

This is **not** a provider-promotion GREEN and **not** live-money approval. Promotion remains deliberately closed because there are no eligible Day 13 OOS trades and the Day 14 governance policy is still `PROPOSED_UNAPPROVED`.

## Exact next step

No further Day 14 engineering closure work is required. Preserve the Day 13 frozen OOS boundary and the Day 14 fail-closed governance policy. Do not approve thresholds implicitly. Day 15 is **NOT STARTED** and requires separate owner instruction.
