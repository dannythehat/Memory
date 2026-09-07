# Super Signals — Current State

Last verified: **2026-09-07**

Authoritative repo: `dannythehat/super-signals`
Production branch: `feature/day-10-shared-telegram-sources`
Live production SHA: `d48a81744af6dda5e644b929d713d3d1ec95c6d3`
Render service: `super-signals-day-8`
Live deploy: `dep-daf8spc9v7es73bpqd30`
Alembic head: `0061_provider_day12_fingerprint`

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
- Day 12 — fingerprint core + hierarchical statistics harness — **ENGINEERING GREEN / PRODUCTION VERIFIED; statistical authority WAITING-FOR-FORWARD-EVIDENCE.**

## Day 11

Day 11 closed under PR `#146`, production SHA `9896c78962f06ec5e89403fa55514178c7cbc4a7`, Render deploy `dep-daf8ci942hec73cvss3g`. The frozen 82-trade paper ↔ broker run produced 23 comparable trades under unchanged gates, so no provider received paper-trust authority. Providers that were not M1-reconcilable remain excluded rather than guessed. This partial fail-closed disposition is complete and remains unchanged by Day 12.

## Day 12 — fingerprint core + hierarchical statistics harness

PR `#147` passed `api`, `web` and Workers checks at delivery head `5eb27148bdbd1512e01269746578d86fb2a3d519`. It merged as `d48a81744af6dda5e644b929d713d3d1ec95c6d3`; Render deploy `dep-daf8spc9v7es73bpqd30` is live; new-instance `/health` repeatedly returned 200; Alembic is at `0061_provider_day12_fingerprint`.

Day 12 is intentionally limited to the **40 shadow discovery providers** and does not mix in the five testing/real calibration providers. Only closed paper outcomes that are `score_eligible` and have `provider_profile_pit_status='resolved'` can enter fingerprint evidence. Broker deals, MetaAPI/live execution and AIDY/D1 writes are outside this harness.

The model surfaces provider, provider×direction, provider×session and provider×direction×session fingerprints for TP hit rates, stop/break-even rates, duration, MAE and MFE. Raw rates are descriptive only. The primary statistic is a deterministic empirical-Bayes hierarchical partial-pooling posterior with 95% intervals. The pre-registered minimum forward N is **30 per evaluable cell**; statistical status is structurally locked to `WAITING-FOR-FORWARD-EVIDENCE` until a later explicitly authorised statistical-validation step.

Production run `92c29d7a-fd65-41ad-bacc-fa082666d870` recorded:

- model: `provider_day12_v1`;
- engineering status: `ENGINEERING_PROVEN`;
- statistical status: `WAITING-FOR-FORWARD-EVIDENCE`;
- shadow provider count: **40**;
- eligible forward trades: **0**;
- fingerprint cells: **0**;
- minimum forward N: **30**;
- evidence digest: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`;
- `research_only=true`;
- `live_money_execution_allowed=false`.

Zero evidence creates zero cells: the harness does not manufacture 0/0 statistics. This is the correct production state because the existing closed shadow outcomes are not currently eligible under the forward/PIT fairness gates. Day 12 engineering is therefore GREEN / production verified while its statistical authority correctly remains WAITING.

The Day 12 deployment made **no AIDY/D1 writes**, preserving the Cloudflare D1 free-tier write boundary after the earlier 93% daily-write warning.

## Cross-project boundary

Super Signals owns provider identity, Provider Lab research and broker/member execution. AIDY supplies bounded independent market/context evidence only. Day 12 is a dormant research harness and cannot mutate broker/member execution, provider live status, sizing or AIDY authority.

## Exact next step

Day 12 needs no further engineering closure work. Accumulate genuinely forward, PIT-resolved, score-eligible shadow evidence; statistical authority remains `WAITING-FOR-FORWARD-EVIDENCE`. **Day 13 is NOT STARTED and requires separate owner instruction.**
