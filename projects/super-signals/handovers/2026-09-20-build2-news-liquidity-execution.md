# Super Signals handover — Build 2 News/Event + Liquidity/Execution

Date: 2026-09-20

## Status

Build 2 is **ENGINEERING PROVEN / PRODUCTION VERIFIED as a research evidence layer**. It does **not** prove AIDY trading edge or profitability.

## Source/runtime evidence

- Super Signals PRs: #210, #211, #212, #213
- final merged/deployed SHA: `4bdd56e94bf801a5c22aa9b80168b4f64251b9f1`
- Render service: `super-signals-day-8` / `srv-d9qmcgks728c73a555m0`
- validation-scope deploy: `dep-danmqtajnfac7395g5cg` — live
- context contract: `aidy_event_liquidity_execution_v1`
- replay version: `aidy_historical_time_machine_v5`
- frozen input contract: `aidy_historical_replay_input_v4`
- final canonical API test gate: **1,144 passed / 137 skipped / 2 warnings**
- repository secret scan and web quality gates passed

## What Build 2 added

A deterministic point-in-time event/liquidity/execution evidence packet is supplied to AIDY. It combines the signal geometry, immutable quote/liquidity state, scheduled-event metadata and broker execution calibration available no later than the signal.

Safety/discipline:
- scheduled events are timing/risk evidence, never directional predictions
- realized event outcomes are never supplied
- future quote or calibration evidence is invalid
- broker calibration is usable only when every required sample class reaches the 30-sample floor; otherwise it remains UNKNOWN
- historical broker evidence is filtered by `closed_at <= signal_posted_at`
- strict provider-history validator remains unchanged
- the one replay retry now fails closed by removing provider-history context after a provider-claim validation rejection

Performance hardening:
- the execution calibration source is materialized once per selection query rather than recomputed for every candidate
- once the frozen 140-case input cohort exists, replay batches skip rematerialization and go straight to reasoning/scoring

## Historical exam

Frozen exact-PIT cohort: **140 cases**.

- Development: **103/103 decisions, 103/103 scores**. Taken baseline **+$867.48**; Build 2 AIDY shadow **+$254.63**; delta **-$612.85**; 17 improved / 44 harmed / 42 unchanged; 11 bounded provider-claim retries.
- Validation: **19/19 decisions, 19/19 scores**. Taken baseline **-$39.42**; Build 2 AIDY shadow **-$22.35**; delta **+$17.07**; 1 improved / 1 harmed / 17 unchanged; 3 retries.
- Holdout: **18 cases locked; 0 decisions; unopened**.

Safety invariants: 0 input-digest mismatches, 0 research-flag violations, 0 live-money replay rows.

## Interpretation

Build 2's engineering goal passed: AIDY now receives deterministic, PIT-safe event/liquidity/execution evidence and the historical exam can replay it without hindsight. The trading result is not evidence of edge. Development performance deteriorated versus the taken-trade baseline and versus Build 1's development replay; validation remained only modestly positive. Later modules must improve decision quality without opening the holdout or widening live authority.

## Exact next step

Start **Build 3 — Provider Conditional-Alpha + Historical Analogue**. The codebase already contains the preregistered Day 13 conditional-alpha engine, which is engineering-proven but still waiting for enough forward evidence. Build 3 must reuse that machinery rather than create a second hypothesis registry, and add a PIT-safe historical-analogue surface for AIDY. Build 4 remains locked until Build 3 passes its exam and this Memory repo is closed again.
