# Super Signals handover — Build 3 Provider Conditional-Alpha + Historical Analogue

Date: 2026-09-20

## Status

Build 3 is **ENGINEERING PROVEN / PRODUCTION VERIFIED as research evidence**. It does **not** prove AIDY trading edge or profitability.

## Source/runtime evidence

- Super Signals PR: #215
- final merged/deployed SHA: `3ae5469e2b4ae83c6de64842aaf714cbd51a38f1`
- Render validation-scope deploy: `dep-dann5mek1f9s7399ndp0` — live
- context contract: `aidy_provider_alpha_analogue_v1`
- replay version: `aidy_historical_time_machine_v6`
- immutable input contract: `aidy_historical_replay_input_v5`
- canonical API gate: **1,149 passed / 137 skipped / 2 warnings**
- secret scan and web quality gates passed

## What Build 3 added

Build 3 reuses the existing Day 13 preregistered provider conditional-alpha machinery. It does not create a second registry.

Current Day 13 evidence remains non-actionable for this exam:
- 0/140 cases have usable pre-trade conditional alpha
- post-entry realized duration conditioning is never promoted to entry-time directional evidence
- missing/underpowered/unapproved evidence remains UNKNOWN

Historical analogue evidence:
- only prior cases with signal_posted_at < target signal are eligible
- the prior result-known timestamp must be <= target signal
- 360 prior analogue rows were attached across the cohort with 0 future-result and 0 future-signal violations
- 72/140 target cases had >=3 sufficiently similar prior cases for a descriptive sample; 68 remained insufficient
- all analogue packets declare selection_bias_possible=true, descriptive_only=true, usable_for_live_edge_claim=false
- 0/140 analogue packets are permitted as live-edge proof

## Historical exam

Frozen exact-PIT cohort: **140 cases**.

- Development: **103/103 decisions, 103/103 scores**. Taken baseline **+$867.48**; Build 3 shadow **+$334.09**; delta **-$533.39**; 18 improved / 45 harmed / 40 unchanged; 7 bounded provider-history retries.
- Validation: **19/19 decisions, 19/19 scores**. Taken baseline **-$39.42**; Build 3 shadow **-$22.35**; delta **+$17.07**; 1 improved / 1 harmed / 17 unchanged; 3 retries.
- Holdout: **18 cases locked; 0 decisions; unopened**.

Safety invariants: 0 input-digest mismatches, 0 research-flag violations, 0 live-money replay rows.

## Interpretation

Build 3 improved development by $79.46 versus Build 2 (-$533.39 vs -$612.85 delta) but remains materially below the provider-taken baseline and is still worse than Build 1's development result. Validation was unchanged from Build 2. The safe evidence plumbing passed; edge did not.

## Exact next step

Start **Build 4 — Probability/EV + Trade Management/Profit Extraction** on a fresh branch. The 18-case holdout remains sealed. Do not start Build 5 until Build 4 has passed its code/test/replay gate and this Memory repository has been updated, merged and re-read.
