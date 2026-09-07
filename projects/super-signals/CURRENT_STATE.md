# Super Signals — Current State

Last verified: **2026-09-07**

Authoritative repo: `dannythehat/super-signals`
Production branch: `feature/day-10-shared-telegram-sources`
Live production SHA: `3b8ac88c5b248c6d9f2fb0718b2062b58d5e77cd`
Render service: `super-signals-day-8`
Live deploy: `dep-dafbjhks728c738nrdu0`
Alembic head: `0063_provider_day14_governance`

## Provider populations

- 40 shadow discovery providers — research only, broker-isolated.
- 5 testing providers — current real execution population.
- 14 paused.
- 4 revoked.

Never mix the 40 shadow discovery providers with the 5 real/testing providers.

## Provider Intelligence sequence

- Day 7 — immutable provider identity/style/behaviour history — GREEN / PRODUCTION VERIFIED.
- Day 8 — forward-only provider learning boundary + legacy closure — GREEN / PRODUCTION VERIFIED.
- Day 9 — canonical AIDY point-in-time context join — GREEN / PRODUCTION VERIFIED.
- Day 10 — immutable per-signal provider + AIDY context attachment — GREEN / PRODUCTION VERIFIED.
- Day 11 — execution-cost and paper ↔ broker calibration — COMPLETE / PRODUCTION VERIFIED as a partial fail-closed provider disposition; not universal reconciliation GREEN.
- Day 12 — fingerprint core + hierarchical statistics harness — ENGINEERING GREEN / PRODUCTION VERIFIED; statistical authority WAITING-FOR-FORWARD-EVIDENCE.
- Day 13 — conditional fingerprints + preregistration + BH FDR + effect-size gates + shrunken conditional posteriors — ENGINEERING GREEN / PRODUCTION VERIFIED; statistical authority WAITING-FOR-FORWARD-EVIDENCE.
- Day 14 — evidence-backed promotion/demotion/re-test governance using the existing `provider_research_profiles` state machine — **ENGINEERING GREEN / PRODUCTION VERIFIED; provider promotion authority remains fail-closed.**

## Day 14 — research governance

PR `#150` delivered the Day 14 governance harness. Final delivery head `d4eee9db9c07db7f9713fbd480d47fb6bd7e8c94` passed `api`, `web` and Workers checks and merged as `3b8ac88c5b248c6d9f2fb0718b2062b58d5e77cd`. Render deploy `dep-dafbjhks728c738nrdu0` is live and production Alembic is `0063_provider_day14_governance`.

Day 14 deliberately reuses the existing research states rather than creating a competing provider state machine:

`learning → shadow → qualified`

`qualified` means **paper-research eligibility only**. It does not change `sources.status`, broker routing, sizing, MetaAPI authority or live-money eligibility. Demotion/re-test logic is also research-only. The Provider Lab scanner now preserves governance-owned `shadow`, `qualified` and `rejected` states instead of silently resetting them to `learning` on later scans.

Builder governance policy `provider_day14_policy_v1` is persisted with:

- minimum post-preregistration OOS N: **30**;
- minimum tested fingerprint cells: **1**;
- confidence level: **95%**;
- OOS window: `since_day13_preregistration`;
- policy approval: `PROPOSED_UNAPPROVED`;
- human live gate required: **true**;
- `research_only=true`;
- `live_money_execution_allowed=false`.

These are builder recommendations only. No owner threshold approval has been inferred from the instruction to build Day 14.

Production Day 13 refresh `d5012961-b09d-4be3-b1ae-db2486a20e11` retained the original frozen OOS boundary `2026-09-07T10:50:52.042190Z` and still had **0 eligible OOS trades / 0 tested hypotheses / 0 BH rejections / 0 candidates / 0 authoritative discoveries**. Statistical status therefore remains `WAITING-FOR-FORWARD-EVIDENCE` and threshold status remains `PROPOSED_UNAPPROVED`.

Production Day 14 run `29ccf16a-3da4-41dc-8e09-dfb7ab99be01` completed with:

- model: `provider_day14_v1`;
- policy: `provider_day14_policy_v1`;
- engineering: `ENGINEERING_PROVEN`;
- governance status: `WAITING-FOR-OWNER-THRESHOLD-APPROVAL`;
- providers: **40**;
- **39 HOLD** (`learning`, insufficient OOS);
- **1 RETEST** (`duplicate_review`, insufficient OOS);
- promotions: **0**;
- demotions: **0**;
- research-state transitions: **0**;
- paper-qualified providers: **0**;
- authoritative live transitions: **0**;
- evidence digest: `0e4d697bb2c9629dfee6667c4d102f5b92fb8d780ff53e4216272932a7cce8b6`;
- all 40 result rows are research-only, live-money false and authoritative-live-transition false.

The production source roster remained unchanged at 40 shadow / 5 testing / 14 paused / 4 revoked, and the 40 shadow research states remained 39 `learning` / 1 `duplicate_review` after the run.

## Safety / runtime note

Day 14 made no AIDY/D1 write and no broker/member execution change. The new instance repeatedly returned `/health` 200 after cutover. A pre-existing fail-safe shadow fallback evaluator error (`legacy provider profile state cannot be score eligible`) was observed both before and after Day 14 deployment; it predates PR #150 and did not alter the Day 14 governance run or source states. Treat it as a separate existing operational issue, not as Day 14 evidence or authority.

## Cross-project boundary

Super Signals owns provider identity, Provider Lab research and broker/member execution. AIDY supplies bounded independent market/context evidence only. Day 14 consumes Super Signals' frozen Day 13 research evidence and does not write to AIDY/D1 or acquire execution authority.

## Exact next step

Day 14 needs no further engineering closure work. Keep policy `provider_day14_policy_v1` fail-closed until there is explicit owner approval of its governance thresholds and sufficient genuinely post-Day-13-preregistration OOS evidence. **Day 15 is NOT STARTED and requires separate owner instruction.**
