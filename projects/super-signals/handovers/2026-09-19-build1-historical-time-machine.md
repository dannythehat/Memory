# Super Signals handover — Build 1 Historical Time Machine

Date: 2026-09-19

## Status

Build 1 is **ENGINEERING PROVEN / PRODUCTION VERIFIED as research infrastructure**. It is **not** a trading-edge or profitability validation.

## Source/runtime evidence

- Super Signals PR: #209 — Build 1: finish Historical Time Machine acceptance gate
- merged/deployed SHA: `8ddbc40050e13fb26f04304d2e2de7a364c2efdc`
- Render service: `super-signals-day-8` / `srv-d9qmcgks728c73a555m0`
- validation-scope deploy: `dep-dan4cg3m8hqs73a0gtb0` — live
- replay version: `aidy_historical_time_machine_v4`
- frozen input contract: `aidy_historical_replay_input_v3`
- Docker acceptance gate: compileall + full API pytest suite before runtime image can go live

## Historical exam

Frozen exact-PIT cohort: 140 cases.

- Development: 103/103 decisions, 103/103 scores. Baseline +$867.48; AIDY shadow +$403.65; delta -$463.83; 19 improved / 46 harmed / 38 unchanged; 11 bounded provider-claim retries.
- Validation: 19/19 decisions, 19/19 scores. Baseline -$39.42; AIDY shadow -$21.38; delta +$18.05; 1 improved / 1 harmed / 17 unchanged; 3 bounded provider-claim retries.
- Holdout: 18 cases locked; 0 decisions; not opened.

Safety invariants: 0 input-digest mismatches, 0 research-flag violations, 0 live-money replay rows. Provider-identity leakage remains removed from replay model context and strict provider-history anti-drift validation remains unchanged.

## Interpretation

The Time Machine itself passed. The current AIDY shadow policy did not establish generalisable edge: development was materially worse than the taken-trade baseline and the small validation slice was only modestly better. Do not describe Build 1 as proving AIDY is profitable or smarter. The point of the Time Machine is precisely to expose this before authority is widened.

## Exact next step

Start **Build 2 — News/Event + Liquidity/Execution** on its own branch/PR. Do not start Build 3 until Build 2 has passed its own exam, been merged/verified, and this Memory repository has been updated, validated, merged and re-read.
