# Super Signals — Current State

Last verified: **2026-09-07**

Authoritative repo: `dannythehat/super-signals`
Production branch: `feature/day-10-shared-telegram-sources`
Live production SHA: `9896c78962f06ec5e89403fa55514178c7cbc4a7`
Render service: `super-signals-day-8`
Live deploy: `dep-daf8ci942hec73cvss3g`
Alembic head: `0060_provider_day11_reconcile`

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
- Day 11 — execution-cost and paper ↔ broker calibration — **COMPLETE / PRODUCTION VERIFIED as a partial fail-closed provider disposition. This is not a universal reconciliation GREEN.**

## Day 11 paper-engine reconciliation fidelity — COMPLETE (partial fail-closed disposition)

Day 11 is COMPLETE as an owner-accepted partial disposition, not a universal reconciliation GREEN. PR `#146` passed `api`, `web` and Workers checks, merged as `9896c78962f06ec5e89403fa55514178c7cbc4a7`, and Render deploy `dep-daf8ci942hec73cvss3g` is live. The frozen calibration corpus is 82 windows using AIDY `b17bf78d7c7197aea4864a4ecd340deaf5d8c344` with 17,054 isolated Twelve M1 bars. Calibration remains `source_kind=calibration_backfill`, `pit_eligible=false`, `research_only=true`, `live_money_execution_allowed=false`; live-money execution is untouched.

Production reconciliation run `00ddf1dc-5bcf-48b4-bab1-7f03d0c6cb88` completed 82 attempted / 23 comparable with evidence digest `f4b2f814cb8c845e2390c3e218ffc4006eb2a8a71a59ff63a397d0ef7a909c6c`. The unchanged `provider_day11_v1` gates remain: minimum 5 comparable/provider, minimum 30 comparable total, median |R| <= 0.35, p95 |R| <= 1.00, lifecycle agreement >= 0.80. The persisted run status therefore remains `WAITING_RECONCILIATION`; that fail-closed status is intentional and was not loosened for closure.

Provider disposition from the completed frozen run:

- `FXTradingVision l Forex & Crypto Signals 🚀`: 31 attempted / 10 comparable; median |R| 0.02468508, p95 |R| 1.23040298, lifecycle 0.90. **NOT trusted for paper** because p95 exceeds the unchanged 1.00 cap by 0.23040298R.
- `GTMO VIP 🤴🏽`: 11 attempted / 0 comparable. **Not M1-reconcilable on this frozen corpus; excluded from paper-based evaluation.** Eight signals fail closed on signal-minute ambiguity and three calibration reads still returned HTTP 500 after the bounded retry cap. Zero stored metrics are sentinels, not measurements.
- `SureShot GOLD`: 6 attempted / 5 comparable; median |R| 0, p95 |R| 2.40, lifecycle 0.80. **Not M1-reconcilable for paper evaluation; excluded.** Signal `914f83ee-d880-4c29-bb3b-f42fe82e5724` retains the independently reconstructed M1 path/order disagreement (paper +2R vs broker -1R); broker truth was not used to resolve paper.
- `TIG’s Asia Trades`: 25 attempted / 8 comparable; median |R| 0.06008850, p95 |R| 1.00000000, lifecycle 1.00. Its provider-level metrics meet the numeric limits, but **it is NOT trusted for paper under the unchanged gate because the global comparable floor is only 23/30**. Official status remains `WAITING_INSUFFICIENT_GLOBAL_RECONCILIATION_SAMPLES`.
- `United Kings™ Signals! 👑`: 9 attempted / 0 comparable. **Not M1-reconcilable on this frozen corpus; excluded from paper-based evaluation.** The exclusions are 4 signal-minute ambiguities, 3 management-bar ambiguities and 2 deterministic paper/broker leg-key mismatches. Zero stored metrics are sentinels, not measurements.

**Trusted for paper after this frozen run: none.** This is the required honest partial disposition: providers are trusted only when all unchanged gates clear; providers that cannot be independently reconstructed on M1 are documented/excluded rather than guessed. No broker outcome is used to resolve the paper side.

## Cross-project boundary

Super Signals owns provider identity, interpretation, Provider Lab research and broker/member execution. AIDY supplies independent market/context and isolated retrospective calibration evidence. Day 11 calibration is research-only. Research outcomes must not mutate broker/member execution, sizing, provider live status or AIDY authority.

## Exact next step

Day 11 needs no further closure work. Keep paper-based provider trust fail-closed under the unchanged gates; M1-unreconcilable providers remain excluded from paper evaluation unless future independent evidence legitimately resolves them. **Day 12 was not started by this closure.**
