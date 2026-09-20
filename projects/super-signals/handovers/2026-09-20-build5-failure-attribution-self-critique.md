# Super Signals — Build 5 Handover

Date: 2026-09-20  
Module: **Failure Attribution / UNKNOWN + AIDY self-critique**  
Status: **ENGINEERING_PROVEN_PRODUCTION_VERIFIED_NO_EDGE_CLAIM**

## Source and production

- Authoritative repo: `dannythehat/super-signals`
- Authoritative branch: `feature/day-10-shared-telegram-sources`
- Build 5 initial PR: **#219**
- Build 5 final-calibration PR: **#220**
- Final deployed SHA: `dc642161e59d94c1e6fdb595bc578d070e53ec9c`
- Render deploy: `dep-dant4068bjmc73ar4960`
- Deploy state: **live**
- Canonical Docker gate: **1,165 passed / 137 skipped / 2 warnings**
- Web quality gate: passed
- Repository secret scan: passed

## What Build 5 does

Build 5 turns AIDY's earlier resolved shadow decisions into point-in-time descriptive self-feedback. It can identify whether AIDY's own previous filtering/reduction helped or harmed, while requiring every prior result to have been known before the target signal.

It also separates genuine UNKNOWN from generic caution. Hard missing/broken evidence forces `need_more_evidence`. Ordinary uncertainty does not automatically justify avoiding or reducing a coherent trade.

The final calibration makes the reduce discipline deterministic. A reduced shadow size is allowed only when the current trade has at least one approved concrete reason:
- equal-weight mean target reward below 1R;
- clear multi-timeframe counter-trend;
- high-impact scheduled event within 60 minutes.

Prior self-feedback can discipline AIDY but cannot itself create a current-trade reduce reason, directional edge, entry override or live authority.

## Failed Build 5 v1 iteration — preserved

The first Build 5 implementation correctly diagnosed over-reduction but prompt guidance alone did not fix it.

Development v1:
- baseline: **+$867.48**
- AIDY shadow: **+$460.01**
- delta: **-$407.47**
- reductions: **79/103**

This was worse than Build 4 (-$312.96). The failure was preserved and used as **development-only** evidence for the deterministic final calibration. Validation and holdout were not used to choose that rule.

## Final contracts

- self-critique context: `aidy_failure_self_critique_v2`
- replay: `aidy_historical_time_machine_v9`
- input: `aidy_historical_replay_input_v8`
- frozen predecessor: `aidy_historical_replay_input_v7`

## Frozen cohort

Exact cohort: **140**
- Development: **103**
- Validation: **19**
- Holdout: **18 locked**

Cross-contract audit:
- same source decisions: **140/140**
- partition drift: **0**
- future self-feedback cutoff violations: **0**
- input digest mismatches: **0**

## Final development exam

Completed **103/103 decisions + 103/103 scores**.

- Provider-taken baseline: **+$867.48**
- Build 5 AIDY shadow: **+$807.07**
- Delta: **-$60.42**
- Improved: **6**
- Harmed: **15**
- Unchanged: **82**
- Actions: **74 take / 28 reduce / 1 reject**
- Deterministic unjustified-reduce corrections to TAKE: **42**

Build 4 development delta was -$312.96, so Build 5 improves development delta by **+$252.54**. It still does not beat the provider baseline.

## Validation exam

Completed **19/19 decisions + 19/19 scores**.

- Provider-taken baseline: **-$39.42**
- Build 5 AIDY shadow: **-$41.38**
- Delta: **-$1.96**
- Improved: **0**
- Harmed: **1**
- Unchanged: **18**
- Actions: **12 take / 6 reduce / 1 need_more_evidence**
- Unjustified-reduce corrections to TAKE: **5**
- Hard UNKNOWN correction to need_more_evidence: **1**

Build 4 validation delta was +$18.05. Build 5 validation is therefore **$20.01 worse** than Build 4. This is evidence that the strong development improvement did not fully generalise.

Do **not** tune Build 5 again using this now-observed validation slice.

## Self-critique evidence

Across the 140 frozen inputs:
- over-reduction of profitable trades: **56**
- prior filtering added value: **11**
- mixed/neutral: **5**
- insufficient prior self-feedback: **68**
- hard UNKNOWN required: **1**
- evidence usable: **139**
- reduce gate open: **58**
- reduce gate closed: **82**

These are descriptive research diagnostics only.

## Final safety audit

- Holdout decisions: **0**
- Holdout scores: **0**
- Partition drift: **0**
- Input digest mismatches: **0**
- Future self-feedback cutoff violations: **0**
- Research flag violations: **0**
- Live-money replay rows: **0**
- Live-management violations: **0**
- Holdout-open flag: **false**

AIDY remains research-only. No live-money, paper-management or live-management authority was granted.

## Interpretation

Build 5 passes engineering, production and PIT/safety acceptance. It substantially corrects the development over-reduction problem, but validation does not confirm edge. The five-build sequence is complete.

## What happens next

There is **no automatic Build 6**.

Freeze this exact deployed Build 5 implementation. The next step is the **proper final exam on the untouched 18-case holdout**. Do not modify/tune the model against validation before that exam, and do not open the holdout until the owner explicitly starts the proper test.
