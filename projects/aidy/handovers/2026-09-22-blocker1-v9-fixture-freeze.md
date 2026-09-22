# AIDY Blocker 1 v9 — Executable Fixture Freeze Handover

Date: 2026-09-22  
Status: **FIXTURE FROZEN / PRODUCTION AGGREGATOR NOT YET IMPLEMENTED**  
AIDY production source validated: `47ffe131b9a8d2180c8d78ba3c1dc1b9253b9e4a`  
Memory predecessor: v8 `9b3e37a86965d5978450789bea0e878112d90590`

## What v9 closes

v8 proved that the earlier T1 fixture was invalid because it used synthetic contributor identities. v9 completes the fixture-only work without changing the already-approved aggregation mathematics.

The frozen fixture now:

- runs the real connected expert builders;
- includes all **15 gate packets** (10 computed + 5 explicit UNKNOWN);
- records **70 real connected sub-calculator identities**;
- uses the production window shape: M1 decision window plus 45-day aggregate history;
- uses the session-aware Gold calendar and completed-bar PIT timestamps;
- stores explicit `decision_time_utc` for historical commitments;
- derives `correct = int(predicted_class == realised_direction)`;
- contains PIT outcome prehistory for class-baseline calculation;
- contains sub-calculator histories and production-shaped gate-level trust/scopes;
- contains dependency history for the real subject identities;
- reloads the frozen fixture bytes before executing either decision path;
- executes the current Build 20→21→22 path and the frozen replacement path from the same state.

## Real liquidity event

The fixture does not inject a liquidity vote. The unmodified real Liquidity/Reclaim builder sees a genuine OHLC proxy event:

- reference: prior-day low;
- state: `reclaim_retest_hold`;
- penetration: **1.507663 bps**;
- reclaim speed: **same_bar**;
- confirming closes: **20**;
- retest held: **true**;
- gate conclusion: **bullish**.

The same fixture gives bullish M5/H1 price-structure evidence, so the reachability test has two genuinely separate root-family routes.

## CI execution proof

AIDY evidence branch: `probe/blocker1-v9-fixture-20260922`  
Evidence branch head: `e4d3a92475189c5d844060d3e7d1b41effe9c8b1`  
PR: #244 (test-only; do not merge)  
CI run: `35704609730` — PASS

Exact output:

- fixture SHA-256: `5d99b3db701df696c5325b1146af5942319db70e05e1c8a2fe130f3e23281960`
- combined manifest digest: `cf9e44df2965ebbe2b8cbc4e1c21d2e6682dfe978466feb5f3686978bc70e1cd`
- packets: **15**
- connected subjects: **70**
- old path: **ABSTAIN**, reason `insufficient_directional_authority`, `directional_total=0.152785`
- replacement path: **BULLISH**, reason `bullish_family_evidence`, `meta_balance=1.000000`, qualifying families **2**
- `price_action`: signed/strength `0.331592`
- `liquidity_mechanism`: signed/strength `0.373330`

Positive subject reliability checks:

- `m5_price_structure_expert:m5_candle_pressure`: N=168, reliability `0.439855`
- `h4_price_structure_expert:h4_acceleration`: N=132, reliability `0.223329`
- `liquidity_reclaim_expert:liquidity_prior_day_low`: N=162, reliability `0.373330`

## Frozen digest components

- subject IDs digest: `2e827dd5d0df0b218d122542e9ddd364beb5fed34be232dad33d4df3f94278b9`
- outcome history digest: `b7ca63589314deb00cc78c11900bcb66a2f6d902c868b74960e3e664aad389ed`
- gate trust history digest: `3f1d9d149ec164ce6738ab9cd4c6c1a28705d243e46533284990ab57e5760125`
- subject history digest: `ce306f1d56c230ce6a4d2ec06a89c7ea89a7ada1e06308331235d34c347de9e0`
- dependency history digest: `697fa6afe0ccb4a86fff0d9266994d80b40343d1891e8a914753ac7090d7f992`
- environment digest: `78047e25f6d159e56e7085eabc4056c27dda758a5f74fe44944efd4e3f804449`
- current packet digests digest: `9c1a716480b4ce9bf0b64c0531deb1a96407aa205de45af7b376fab3cb7cfd33`

## Memory files

- `projects/aidy/BLOCKER1_AGGREGATION_PREREGISTRATION.md`
- `projects/aidy/fixtures/blocker1_v9_validation_manifest.json`
- `projects/aidy/fixtures/blocker1_v9_fixture_probe.py`
- `projects/aidy/fixtures/blocker1_v9_full_fixture.py`
- `projects/aidy/CURRENT_STATE.md`
- `projects/aidy/LIVE_STATE.json`
- `projects/aidy/KNOWN_ISSUES.md`
- `projects/aidy/DECISIONS.jsonl`

The generated full fixture is ~8.6 MB and remains on the isolated AIDY evidence branch, addressed by its SHA-256 above. Memory stores the exact reproduction harness and validation manifest.

## Safety / authority

No production AIDY code was changed. No deployment was made. No config, holdout, Super Signals execution rule, owner risk, formal-forward authority or live-money authority changed. Formal-forward and live-money authority remain OFF. Owner 1% risk remains unchanged.

The latent Liquidity/Reclaim empty-reference neutral-contract defect discovered in v8 remains open; v9 does not hide or fix it.

## Next engineering step

Implement the already-frozen Blocker-1 aggregation replacement in AIDY production code **without changing the frozen constants or equations**. Promote the v9 reachability assertion into the production test suite. Then rerun Build 23 / prospective shadow acceptance against the repaired decision layer before any promotion or live-money reasoning.
