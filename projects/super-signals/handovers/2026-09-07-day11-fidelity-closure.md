# Super Signals Day 11 — PAPER RECONCILIATION FIDELITY CLOSURE

Date: 2026-09-07
Status: **COMPLETE / PRODUCTION VERIFIED as a partial fail-closed disposition — NOT universal reconciliation GREEN**

## Production proof

- Super Signals PR: `#146` — `Day 11 closure: paper reconciliation fidelity`.
- Delivery head: `f0c50724dd8f1ce0d28b03b7e7de01ad8898de61`.
- Delivery-head checks: `api` success, `web` success, Workers success.
- Production merge SHA: `9896c78962f06ec5e89403fa55514178c7cbc4a7`.
- Render deploy: `dep-daf8ci942hec73cvss3g` — `live`.
- Production reconciliation run: `00ddf1dc-5bcf-48b4-bab1-7f03d0c6cb88`.
- Run evidence digest: `f4b2f814cb8c845e2390c3e218ffc4006eb2a8a71a59ff63a397d0ef7a909c6c`.
- Frozen corpus: 82 attempted / 23 comparable.
- All 82 persisted samples: `research_only=true`, `live_money_execution_allowed=false`.

## Fidelity closure implemented

Fidelity mode: `canonical_allocation_keyed_leg_m1`.

- Live execution and calibration replay use one shared pure entry/target allocation helper.
- Paper legs and broker legs are matched by deterministic `(entry_index,tp_index)` keys.
- Paper reconstruction is completed before broker truth is read; broker outcomes never resolve the paper side.
- Broker lifecycle truth recognises final per-position moved/breakeven stops, while R remains measured against the original signal stop.
- Calibration reads retry only HTTP 500/503 with a fixed 3-attempt exponential backoff.
- No tolerance/sample floor was loosened and no ambiguous M1 path was guessed.

## Calibration isolation

The widened AIDY corpus was already loaded under AIDY merge `b17bf78d7c7197aea4864a4ecd340deaf5d8c344`: 82/82 windows complete and 17,054 isolated Twelve M1 bars.

Closure preserved `source_kind=calibration_backfill`, `source_provider=twelve_data`, `pit_eligible=false`, `research_only=true`, `live_money_execution_allowed=false`. The closure rerun performed no new D1 backfill/write, which also avoided additional D1 row-write usage after the account reached 93% of the daily free-tier write cap.

## Unchanged acceptance contract

Tolerance version `provider_day11_v1` remains exactly:

- minimum comparable/provider: 5;
- minimum comparable total: 30;
- maximum median |R delta|: 0.35;
- maximum p95 |R delta|: 1.00;
- minimum lifecycle agreement: 0.80.

The production run remains `WAITING_RECONCILIATION` because total comparable is 23/30. That fail-closed runtime status is correct and is not rewritten merely because the Day 11 characterization milestone is closed.

## Provider verdicts

- **FXTradingVision — NOT trusted for paper.** 31 attempted / 10 comparable; median |RΔ| `0.02468508`; p95 |RΔ| `1.23040298`; lifecycle `90%`. Residual: p95 exceeds the unchanged 1.00 cap by `0.23040298R`.
- **GTMO VIP — not M1-reconcilable / excluded.** 11 attempted / 0 comparable. Exclusions: 8 signal-minute ambiguities; 3 calibration HTTP 500 responses persisted after bounded retry. Zero stored metric fields are sentinels, not measurements.
- **SureShot GOLD — not M1-reconcilable / excluded.** 6 attempted / 5 comparable; median |RΔ| `0`; p95 |RΔ| `2.4`; lifecycle `80%`. Signal `914f83ee-d880-4c29-bb3b-f42fe82e5724` remains an independent M1 path/order disagreement; broker truth was not used to change the paper result.
- **TIG’s Asia Trades — NOT trusted for paper yet.** 25 attempted / 8 comparable; median |RΔ| `0.06008850`; p95 |RΔ| `1.00000000`; lifecycle `100%`. Provider-level numeric thresholds pass, but the unchanged global floor remains 23/30, so no paper-trust authority is granted.
- **United Kings — not M1-reconcilable / excluded.** 9 attempted / 0 comparable. Exclusions: 4 signal-minute ambiguities, 3 management-bar ambiguities, 2 deterministic paper/broker leg-key mismatches. Zero stored metric fields are sentinels, not measurements.

Trusted for paper after this frozen run: **none**.

## Full exclusion matrix

| Provider | Attempted | Comparable | Non-comparable evidence |
| --- | ---: | ---: | --- |
| FXTradingVision | 31 | 10 | 19 management-bar ambiguous; 1 management-exit price unobserved; 1 signal-minute ambiguous |
| GTMO VIP | 11 | 0 | 8 signal-minute ambiguous; 3 persistent HTTP 500 after bounded retry |
| SureShot GOLD | 6 | 5 | 1 management-bar ambiguous; comparable set also contains the documented independent path/order divergence |
| TIG’s Asia Trades | 25 | 8 | 11 management-bar ambiguous; 3 persistent HTTP 503 after bounded retry; 2 paper/broker leg-key mismatch; 1 signal-minute ambiguous |
| United Kings | 9 | 0 | 4 signal-minute ambiguous; 3 management-bar ambiguous; 2 paper/broker leg-key mismatch |

## Exact Memory entry

> **Day 11 = COMPLETE as a provider-by-provider, fail-closed characterization milestone: trusted where it reconciles, documented/excluded where it cannot; this is NOT a universal reconciliation GREEN.** Production SHA `9896c78962f06ec5e89403fa55514178c7cbc4a7`, Render deploy `dep-daf8ci942hec73cvss3g`, reconciliation run `00ddf1dc-5bcf-48b4-bab1-7f03d0c6cb88`, evidence digest `f4b2f814cb8c845e2390c3e218ffc4006eb2a8a71a59ff63a397d0ef7a909c6c`. The frozen run attempted 82 and produced 23 comparable under the unchanged `provider_day11_v1` gates (5/provider, 30 total, median <=0.35R, p95 <=1.00R, lifecycle >=80%). Fidelity mode is `canonical_allocation_keyed_leg_m1`; paper is independently reconstructed before broker comparison; calibration remains retrospective Twelve-only, `source_kind=calibration_backfill`, `pit_eligible=false`, `research_only=true`, `live_money_execution_allowed=false`. Provider disposition: FXTradingVision NOT trusted (10 comparable; median 0.02468508R; p95 1.23040298R; lifecycle 90% — p95 fails); GTMO excluded/not M1-reconcilable (0/11; 8 signal-minute ambiguities + 3 persistent 500s after bounded retry); SureShot excluded/not M1-reconcilable (5/6; median 0; p95 2.4R; lifecycle 80%; genuine independent M1 path/order divergence retained for `914f83ee-d880-4c29-bb3b-f42fe82e5724`); TIG NOT trusted yet (8/25; median 0.06008850R; p95 1.00000000R; lifecycle 100%; local metrics pass but unchanged global floor is only 23/30); United Kings excluded/not M1-reconcilable (0/9; 4 signal-minute ambiguities + 3 management-bar ambiguities + 2 keyed-leg mismatches). **Trusted for paper after this frozen run: none.** No broker outcome was used to resolve paper, no tolerance/sample floor was loosened, no Day 12 work was started.

## Exact next step

No further Day 11 closure work is required. Keep paper trust fail-closed under the unchanged gates and leave documented M1-unreconcilable providers excluded from paper-based evaluation. Day 12 is **NOT STARTED** and requires a separate explicit owner instruction.
