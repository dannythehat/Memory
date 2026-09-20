# Super Signals — Build 4 Handover

Date: 2026-09-20  
Module: **Probability/EV + Trade Management/Profit Extraction**  
Status: **ENGINEERING_PROVEN_PRODUCTION_VERIFIED_NO_EDGE_CLAIM**

## Source and production

- Authoritative repo: `dannythehat/super-signals`
- Authoritative branch: `feature/day-10-shared-telegram-sources`
- Merged implementation: PR #216
- Final deployed SHA: `1c6853e814d59f57c6b55f41361c23c98ffde791`
- Render service: `super-signals-day-8` / `srv-d9qmcgks728c73a555m0`
- Validation-scope deploy: `dep-dannhpugekts739i8660`
- Deploy state: **live**
- Canonical Docker gate: **1,154 passed / 137 skipped / 2 warnings**
- Web quality gate: passed
- Repository secret scan: passed

## Build 4 contract

- Context: `aidy_probability_ev_management_v1`
- Historical replay: `aidy_historical_time_machine_v7`
- Immutable replay input: `aidy_historical_replay_input_v6`
- Frozen predecessor contract: `aidy_historical_replay_input_v5`
- Build 4 derives from the exact frozen Build 3 cases rather than rematerializing from mutable raw source tables.

The deployed probability surface uses already-resolved prior historical analogues only. It reports descriptive positive-outcome probability, uncertainty and empirical prior realised-R evidence where the minimum sample is present. It is explicitly selection-bias flagged and is never a calibrated current TP-hit forecast. Reward:risk and break-even geometry are signal-derived. Execution-cost R is only exposed when the existing engineering calibration is available.

## Management authority

Build 4 did **not** widen trading authority.

- `research_only=true`
- `live_money_execution_allowed=false`
- AIDY paper management allowed: **false**
- AIDY live management allowed: **false**
- Research posture: `provider_baseline_only_until_forward_efficacy_is_proven`
- Existing broker-confirmed profit-protection ladder remains canonical.
- AIDY must not duplicate or override that ladder.

## Frozen cohort

Exact cohort remains **140**:

- Development: **103**
- Validation: **19**
- Holdout: **18 locked**

Cross-contract audit versus Build 3 input v5:

- Same source decisions: **140/140**
- Partition mismatches: **0**
- Frozen-source provenance violations: **0**
- Previous-contract provenance violations: **0**
- PIT assertion violations: **0**

## Probability / EV evidence audit

Across 140 cases:

- Descriptive empirical analogue probability/EV available: **72**
- Insufficient prior outcomes: **68**
- Selected analogue rows: **360**
- Future analogue result violations: **0**
- Future analogue signal violations: **0**
- Live-edge-claim violations: **0**
- Entry-override violations: **0**

These values are research evidence only.

## Development exam

Completed **103/103 decisions + 103/103 scores**.

- Provider-taken baseline: **+$867.48**
- Build 4 AIDY shadow: **+$554.52**
- Delta versus taken provider trades: **-$312.96**
- Improved: **13**
- Harmed: **33**
- Unchanged: **57**

Build 3 development delta was **-$533.39**, so Build 4 improves the development delta by **+$220.43**. This is meaningful engineering progress, but Build 4 still underperforms the provider baseline by **$312.96** and therefore does **not** prove trading edge.

## Validation exam

Completed **19/19 decisions + 19/19 scores**.

- Provider-taken baseline: **-$39.42**
- Build 4 AIDY shadow: **-$21.38**
- Delta: **+$18.05**
- Improved: **1**
- Harmed: **1**
- Unchanged: **17**

The validation slice is small and remains insufficient for a profitability claim.

## Final safety audit

- Holdout decisions: **0**
- Holdout scores: **0**
- Input digest mismatches: **0**
- Research/live-money flag violations: **0**
- Live-money replay rows: **0**
- Future analogue-result violations: **0**
- Future analogue-signal violations: **0**
- Live-management violations: **0**
- Paper-management violations: **0**
- Live-edge-claim violations: **0**
- Entry-override violations: **0**
- Holdout-open flag: **false**

## Interpretation

Build 4 passes engineering, production and PIT/safety acceptance. It materially improves the development replay versus Build 3, while keeping authority unchanged. It does **not** beat the provider-taken development baseline and must not be described as proving AIDY profitability or edge.

The 18-case holdout remains sealed.

## Next gate

**Build 5 — Failure Attribution/UNKNOWN + AIDY self-critique/judging**

Do not start Build 5 until this Memory branch is validated, merged and re-read from `main`.
