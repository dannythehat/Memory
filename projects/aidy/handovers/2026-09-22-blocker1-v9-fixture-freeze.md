# AIDY Blocker 1 — v9 Executable Fixture Freeze Handover

Date: 2026-09-22
Status: MATHEMATICS FROZEN / T1 FIXTURE FROZEN / IMPLEMENTATION NOT STARTED

## What changed

This session completed the fixture-validation work left open by v8. The aggregation mathematics in BLOCKER1_AGGREGATION_PREREGISTRATION.md was not changed.

The real AIDY builders were executed from audited production source SHA:

47ffe131b9a8d2180c8d78ba3c1dc1b9253b9e4a

Execution was isolated on AIDY draft audit PR #243. Nothing from the audit branch was merged or deployed.

The v8 deterministic source state was not sufficient for T1 because every Liquidity/Reclaim directional calculator voted neutral, which made liquidity_mechanism signed strength exactly zero under the frozen replacement mathematics. v9 therefore adds an explicit PIT-safe OHLC scenario around the genuine prior-day-low reference. The real Liquidity/Reclaim builder detected the event itself and emitted bullish scoreable reclaim calculators. No vote was hand-edited.

## Frozen executable state

- 15 expert packets: 10 computed + 5 explicit UNKNOWN.
- 70 learned sub-calculator subjects from the computed experts.
- 75 packet sub-calculators when the five explicit UNKNOWN runtime-availability sentinels are included.
- 8,280 historical commitment rows.
- 510 production-shaped Build-3 scoped trust rows.
- 5,000 resolved outcome-history rows.
- 180 dependency-history cycles.
- Every commitment has decision_time_utc.
- Every commitment has gate/packet/version linkage and scope keys.
- correct is derived and asserted as int(predicted_class == realised_direction); it is not an independent construction knob.
- History admission is strict PIT: resolved_at_utc < decision_time_utc.
- The validator rejected an intermediate fixture whose latest outcome resolved exactly at the decision timestamp. That history was moved back one cycle before freezing.
- The injected prior-day-low reference is 3648.03.

## Dual-path execution

The same frozen state was run through both paths.

### Existing production path

Build 20 -> Build 21 -> Build 22:

- direction: ABSTAIN
- reason: insufficient_directional_authority
- directional_total: 0.049046

This value was executed, not estimated.

### Frozen replacement mathematics

- direction: BULLISH
- reason: bullish_independent_family_evidence
- meta_balance: 1.000000000
- qualifying independent root families: price_action and liquidity_mechanism.

This proves engineering reachability of the frozen aggregation design. It is not an empirical claim that AIDY has predictive edge.

## Frozen digest

Combined fixture digest:

0c9034382593506c409c9efcfbfa9e4782410d298efb7c90e06baf571f2d7274

AIDY audit artifact commit: de56823
Successful executable freeze run: 35697543554

## Authoritative Memory artifacts

- projects/aidy/fixtures/blocker1_t1_v9_fixture.json
- projects/aidy/fixtures/blocker1_t1_v9_execution.json
- projects/aidy/fixtures/blocker1_t1_v9_fixture_validator.py
- projects/aidy/BLOCKER1_AGGREGATION_PREREGISTRATION.md

v7's eight-ID fixture remains withdrawn. v8's real-builder discovery remains useful evidence but is superseded by v9 for the frozen T1 acceptance source state.

## Known issue deliberately NOT fixed

KNOWN_ISSUES.md 0.05 remains active: Liquidity/Reclaim can still raise when usable M1 exists but no reference/event produces a known neutral directional calculator. v9 avoids that state by constructing a genuine reclaim event; it does not change the expert or gate contract.

## Production safety

No production code changed.
No production config changed.
No formal-forward state changed.
No live-money path changed.
No untouched holdout was used or changed.
AIDY remains research/shadow only for this decision layer.

## Next work

1. Write T1-T18 against the frozen v9 fixture and digest.
2. Confirm T1 fails the current Build-20 -> 21 -> 22 production path for the recorded reason/value.
3. Implement the already-frozen aggregation mathematics exactly, with no threshold or formula changes.
4. Run focused tests and full regression.
5. Continue the independently agreed repair order: environment-cardinality fix, calibration producers, PIT-safe H4/D1 rebuild, sub-evidence/abstain semantics, maintenance-window classification, append-only health monitoring, baselines, Build-23 rerun, then unchanged multi-regime soak.

Do not wire new paid data or promote live authority before those gates are complete.
