# Super Signals handover — Build 3 Provider Conditional-Alpha + Historical Analogue

Date: 2026-09-20

## Status

Build 3 is **ENGINEERING PROVEN / PRODUCTION VERIFIED as research evidence**. It does **not** prove AIDY trading edge.

## Source/runtime evidence

- Super Signals PR: #215
- final merged/deployed SHA: `3ae5469e2b4ae83c6de64842aaf714cbd51a38f1`
- final validation-scope Render deploy: `dep-dann5otii2qc73c233qg` — live
- canonical API gate: **1,149 passed / 137 skipped**
- Build 3 context: `aidy_provider_alpha_analogue_v1`
- historical analogue version: `aidy_historical_analogue_v1`
- replay version: `aidy_historical_time_machine_v6`
- immutable input contract: `aidy_historical_replay_input_v5`

## Conditional-alpha discipline

Build 3 reuses the existing Day 13 preregistered engine. It does not create another registry. At the frozen historical timestamps, zero cases have usable pre-trade conditional alpha. Underpowered, threshold-unapproved or realized/post-entry duration-conditioned cells stay non-actionable.

## Historical analogue discipline

A prior case is eligible only when both its signal and resolved result predate the target signal. Across the 140 frozen cases, 360 prior analogue rows were selected with **0 future-result violations**. 72 targets have a descriptive sample of at least three analogues and 68 remain insufficient. All packets keep selection-bias/descriptive-only flags and explicitly prohibit live-edge claims.

## Historical exam

- Development: **103/103 decisions, 103/103 scores**. Taken baseline **+$867.48**; Build 3 shadow **+$334.09**; delta **-$533.39**; 18 improved / 45 harmed / 40 unchanged; 7 bounded provider-claim retries.
- Validation: **19/19 decisions, 19/19 scores**. Taken baseline **-$39.42**; Build 3 shadow **-$22.35**; delta **+$17.07**; 1 improved / 1 harmed / 17 unchanged; 3 retries.
- Holdout: **18 locked / 0 decisions**.

Safety: 0 input-digest mismatches, 0 research-flag violations, 0 live-money replay rows, 0 future analogue-result violations, 0 pre-trade-alpha-usable cases, 0 live-edge-usable analogue cases.

## Interpretation

Build 3 improved development delta by $79.46 versus Build 2 (-$533.39 vs -$612.85), but still materially underperformed taking the provider trades. The small validation slice stayed +$17.07. This is research progress, not edge proof.

## Exact next step

Start **Build 4 — Probability/EV + Trade Management/Profit Extraction**. It must remain research-only/no-live-money, consume only PIT-safe evidence, and pass development then validation before Build 5 can open.
