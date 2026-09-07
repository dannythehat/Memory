# Super Signals — Current State

Last verified: **2026-09-07**

Authoritative repo: `dannythehat/super-signals`
Production branch: `feature/day-10-shared-telegram-sources`
Live production SHA: `367ff4076410e7edfa3095295f3964a57d812d7c`
Render service: `super-signals-day-8`
Live deploy: `dep-daf6dgp7lnhs73fca1rg`
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
- Day 11 — execution-cost and paper ↔ broker calibration — **DEPLOYED / PRODUCTION VERIFIED, but WAITING on a real AIDY M1 evidence blocker. Day 11 is NOT GREEN or complete.**

## Day 10

Migration `0058_provider_aidy_context` creates `provider_signal_context_attachments`, one immutable record per qualifying signal. It freezes the exact provider-profile version and exact AIDY PIT context/snapshot provenance. Database guards reject future provider/AIDY context, duplicate signal attachments, mutable history and any live-money authority.

Day 10 production SHA was `634838b5a559a425a1fe54af5bf7c022763f2743`; Render deploy was `dep-daepomp7lnhs73f213eg`.

## Day 11

PR `#144` was merged from delivery head `92b8b7368ec87073f1be999e42495883509722f0`. The three delivery-head checks (`api`, `web`, Workers) were all successful. Production merge SHA is `367ff4076410e7edfa3095295f3964a57d812d7c`; Render deploy `dep-daf6dgp7lnhs73fca1rg` is live; Alembic is at `0060_provider_day11_reconcile`; `/health` returned 200 repeatedly on the new instance.

The real broker-cost corpus is healthy enough for engineering calibration: 988 broker-position samples, 467 entry-slippage samples and 704 exit-slippage samples. The production cost model reports `ENGINEERING_CALIBRATED`. This evidence is research-only and cannot grant live-money execution authority.

The required five-provider paper ↔ broker reconciliation ran automatically in production against real `broker_deals`. Run `c5fae236-a63f-4340-99e7-7890e08f782a` attempted **56** real signals across the five providers (15 / 6 / 9 / 15 / 11), but produced **0 comparable signals**. Every attempt was excluded because AIDY returned a valid PIT continuity response with at least one missing M1 open time (`aidy_m1_incomplete`). Therefore no genuine paper R/PnL delta or lifecycle-agreement statistic exists yet. The persisted zero median/p95/lifecycle values for zero-sample provider result rows are sentinel values and must not be reported as measurements.

The versioned reconciliation tolerance remains unchanged: minimum 5 comparable signals per provider, minimum 30 total, maximum median absolute R delta 0.35, maximum p95 absolute R delta 1.00, minimum lifecycle agreement 0.80. Because each provider has 0 comparable samples, all five fail closed as `WAITING_INSUFFICIENT_PROVIDER_RECONCILIATION_SAMPLES` with `SHADOW_WAITING`; the overall run is `WAITING_RECONCILIATION`. All 56 persisted run samples are `research_only=true` and `live_money_execution_allowed=false`.

This is a genuine live evidence blocker, not a CI/migration/auth failure. Day 11 must not be called GREEN until complete PIT AIDY M1 replay evidence exists for enough real broker-grounded signals to calculate the reconciliation metrics without fabrication.

## Cross-project boundary

Super Signals owns provider identity, interpretation, Provider Lab research and broker/member execution. AIDY supplies independent point-in-time Gold context and M1 evidence. Day 11 calibration is research-only. Missing AIDY evidence must fail closed and must not alter broker/member execution, sizing, provider status or AIDY authority.

## Exact next step

Restore/provide complete PIT AIDY M1 coverage for the real Day 11 replay windows, then rerun the existing Day 11 acceptance **unchanged** against real `broker_deals`. Do not loosen the tolerance or convert missing evidence into synthetic outcomes. Day 12 must not start until the required real reconciliation metrics exist and Day 11 can be closed with production proof.
