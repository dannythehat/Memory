# Super Signals Day 11 — LIVE EVIDENCE BLOCKER

Date: 2026-09-07
Status: **WAITING — not GREEN / not complete**

## What reached production

- Delivery PR: `#144`.
- Delivery head: `92b8b7368ec87073f1be999e42495883509722f0`.
- Delivery-head checks: `api`, `web`, Workers — all successful.
- Production merge SHA: `367ff4076410e7edfa3095295f3964a57d812d7c`.
- Render deploy: `dep-daf6dgp7lnhs73fca1rg` — live.
- Alembic head: `0060_provider_day11_reconcile`.
- New-instance `/health`: 200.

The Day 11 implementation is research-only. It does not call MetaAPI, mutate broker positions, change member risk/sizing, change provider routing/status or grant AIDY/live-money authority.

## Real broker-cost evidence

Production contains real broker calibration evidence. The demo cost model is `ENGINEERING_CALIBRATED` from:

- 988 broker-position samples;
- 467 entry-slippage samples;
- 704 exit-slippage samples;
- entry adverse p50 = 0 points;
- entry adverse p95 = 1.088 points;
- exit adverse p50 = 0 points;
- exit adverse p95 = 0 points.

This proves the broker-cost side clears its 30-sample engineering floor. It does **not** substitute for paper ↔ broker reconciliation.

## Real five-provider reconciliation

Production run: `c5fae236-a63f-4340-99e7-7890e08f782a`
Evidence digest: `0c802cf5f792b3095c6ad7e6f4e8ff3aff0d9d4c324ee3a3d4d1ac1e42ec0449`
Run status: `WAITING_RECONCILIATION`

The run selected and attempted **56 real broker-grounded signals** across all five established providers:

- Provider 1: 15 attempted / 0 comparable;
- Provider 2: 6 attempted / 0 comparable;
- Provider 3: 9 attempted / 0 comparable;
- Provider 4: 15 attempted / 0 comparable;
- Provider 5: 11 attempted / 0 comparable.

Every attempted signal was excluded as `aidy_m1_incomplete:<missing_open_time>`. The AIDY client received valid PIT continuity payloads, but each replay window contained at least one declared missing expected M1 open time. This is a real data-coverage blocker, not missing credentials or a fabricated test failure.

Because there are **0 comparable signals**, no genuine median/p95 paper-vs-broker R/PnL delta and no genuine lifecycle agreement rate can be calculated for any provider. The zero values stored on the zero-sample provider-result rows are sentinel defaults and must never be presented as measured deltas.

## Fail-closed proof

Tolerance version `provider_day11_v1` remains unchanged:

- minimum comparable signals/provider: 5;
- minimum comparable signals total: 30;
- maximum median absolute R delta: 0.35;
- maximum p95 absolute R delta: 1.00;
- minimum lifecycle agreement rate: 0.80.

All five providers have 0 comparable samples, so all five correctly remain:

`WAITING_INSUFFICIENT_PROVIDER_RECONCILIATION_SAMPLES` → `SHADOW_WAITING`.

All 56 persisted acceptance sample rows are `research_only=true` and `live_money_execution_allowed=false`.

## Hard blocker

Day 11 cannot be closed GREEN because the required real paper ↔ broker metrics do not exist while AIDY M1 continuity is incomplete for every selected replay window. Loosening the tolerance, treating sentinel zeros as results, backfilling synthetic bars or substituting broker-only PnL would violate the acceptance rules.

## Exact next step

Restore/provide complete PIT AIDY M1 coverage for enough of the selected real replay windows, then rerun the existing Day 11 acceptance **unchanged** against real `broker_deals`. Only when real comparable samples exist should the median/p95 R/PnL deltas and lifecycle agreement be evaluated against the current tolerance. Do not start Day 12 until Day 11 has real reconciliation evidence and can be closed with production proof.
