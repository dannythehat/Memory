# AIDY Handover — 2026-09-22 — Independent 24-Build Adversarial Audit

## Finished state

Source repo: `dannythehat/Aidy-Gold-Signals`
Branch: `main`
Verified SHA: `47ffe131b9a8d2180c8d78ba3c1dc1b9253b9e4a`
Memory SHA at audit start: `4a26d811728a585dfe9395c49268783f95ad1214`
Status: **RED** — Builds 1-24 are BUILT and ENGINEERING PROVEN, but the live decision layer is **non-functional**. AIDY cannot currently produce a directional view under any achievable amount of learning.

Audit type: independent adversarial audit requested by the owner. Read-only. No production, code, config, holdout or Super Signals change was made.

## What changed

Nothing in production. This handover records **audit findings only**, so the next session does not restart from "Builds 1-24 complete / all green".

## Findings — blocking

### 1. Meta-direction abstention is arithmetic, not judgement — RED

`gold_meta_direction.py:298` abstains when `directional_total < MIN_DIRECTIONAL_WEIGHT` (0.30).

Measured across all 41 live cycles: `directional_total` max **0.016939**, typical **0.002-0.009**. Short of the threshold by 18x-150x on every cycle.

Cause is a units mismatch. `gold_environment_gate_selector.py:472` computes:

    authority = shrunk_accuracy * sample_confidence * scope * calibration * recency * dependency

The dependency term is Build 20's **evidence-redundancy ratio**, not a confidence. Build 20 correctly collapses **91 raw signal-units into 4.0 effective units** (0.044 system-wide) because M5/M15/momentum genuinely describe one move. Build 21 then multiplies that ratio into a confidence chain and Build 22 **sums** the results against an **absolute** constant.

Live per-gate dependency multipliers: h1 0.2168, h4 0.1817, liquidity 0.0500, m5 0.0225, m15 0.0220, momentum 0.0207.

Ceiling analysis: with perfect trust (accuracy 1.0, N infinite, `mini_exact` scope, strong calibration) and all six directional gates agreeing, the sum of dependency multipliers is **0.5137**. Under realistic mature conditions (accuracy 0.65, N=180, `gate_global` scope, calibration unwired) it is **0.179 — still below 0.30**. In practice only 2-3 gates conclude directionally per cycle, giving ~0.05-0.10.

**AIDY will still abstain at N=10,000.** The 39/39 (now 41/41) abstention is not correctly-calibrated caution; it is a dead end that resembles caution, which is why it passed acceptance.

### 2. Environment-conditional learning never runs — RED

**41 cycles produced 41 distinct `environment_key` values.**

Cause: `gold_environment_contract.py:75-86` includes `utc_clock_bucket_15m` and `utc_weekday` in `GLOBAL_CORE_DIMENSIONS`. With a 15-minute cadence the clock bucket changes every cycle, so the core key is effectively a timestamp fingerprint.

Live scope depth (`aidy_gold_expert_context_scores`, gate subjects):

| scope | rows | max N | minimum | ever met |
|---|---|---|---|---|
| `global_core` | 570 | 1 | 6 | never |
| `mini_exact` | 300 | 3 | 12 | never |
| best reduced context | 99 | 6-7 | ~8 | never |
| `gate_global` | 15 | 23 | 1 | always |

Every directional gate in every live cycle resolves to `context_label: gate_global`, `scope multiplier 0.70`. **100% fallback to the environment-blind global average.** The central premise of the programme — "in THIS environment, which expert is reliable" — is not operating. AIDY currently learns exactly one number per gate.

### 3. Two calibration subsystems are dead code in production — RED

`gold_expert_shadow.py:720` passes `calibration_rows=()` and `:726` passes `meta_calibration_rows=()` — both hardcoded empty in the live bundle.

Consequences:
- Build 21 calibration state is permanently `unknown`, multiplier permanently **0.85**: a haircut on every gate forever that no learning can lift.
- Build 22 `calibrated_confidence` is permanently `None`, `confidence_state` permanently `withheld_unavailable`. The `META_CALIBRATION_MIN_N = 30` path has never executed.
- Circular: meta-calibration requires resolved non-abstain views, which finding 1 prevents.

### 4. The two best gates contribute exactly zero — RED

`gold_environment_gate_selector.py:491` grants `directional_authority_weight` only when the conclusion is `bullish`, `bearish` or `neutral`. A gate-level `abstain` receives **0**.

Measured over 41 cycles: H1 concludes `abstain` **29/41**; H4 **33/41**. So the only two gates performing above chance are silent 71% and 80% of the time, while M5 (31.82%, the worst gate) commits 25/41 and dominates what little directional weight exists. Intended selection is inverted.

H4 has concluded **bearish 0 times in 41 cycles** (33 abstain, 8 bullish) against a 58%-bearish tape. See finding 5 for the mechanical cause.

### 5. D1 and H4 experts are structurally starved — RED (data)

Price experts read only `source = 'twelve_data_session_aggregate_v1'` over a 45-day window (`private_forward_context.py:310`). Verified admitted depth in live D1 `market_candles`:

- H1: **156** bars — workable
- H4: **42** bars (~7 trading days) — too thin for swing geometry
- D1 Context: **10** bars (2026-09-01 to 2026-09-20) — **cannot compute daily structure at all**

Confirmed HH/HL/LH/LL, confirmed swings, prior-day range position and daily ATR are not derivable from 10 daily observations. Build 9 output is not daily context. This is also the mechanical cause of H4's degenerate never-bearish behaviour in finding 4, and it means H4's "57% on N=7" is not evidence of skill.

**Cheap fix available:** D1 already holds **40,771 M1 bars back to 2026-08-12** (essentially complete coverage for ~29 trading days), while the daily aggregate series only begins 2026-09-01. Rebuilding H4/D1 aggregates from existing M1 would take D1 from 10 to ~28 bars and H4 from 42 to ~170 with **zero new data cost and no new vendor**. Higher value than wiring any of the five UNKNOWN gates.

## Findings — non-blocking but material

### 6. Zero-market-minute bucket misclassified — ~60 lost minutes every trading day

`twelve_data_market.py:216,229`:

    ratio = Decimal(len(in_session)) / Decimal(len(expected)) if expected else Decimal(0)
    "admissible": bool(expected) and ratio >= threshold,

A bucket containing **no market minutes** is classified as inadmissible/missing rather than not-applicable.

This is the traced root cause of the 135.2-minute gap, and **it was not an outage**: capture ran uninterrupted every 5 minutes throughout. Evidence from `market_snapshots`:

- 20:57 last `complete` (session `new_york`)
- 21:02-21:57 `partial`, session `off_hours` — genuine CME daily maintenance break (`17:00-18:00 America/New_York` per the adapter manifest)
- 22:02 quotes resume (22:01 bar, lag 74s) but status stays `partial`
- 22:32 and 22:57 the sole blocker is `"1h": {admissible: false, expected_market_minutes: 0, coverage_ratio: "0.000000"}` for bucket 21:00-22:00
- 23:02 `complete`, because the H1 bucket finally rolled to 22:00-23:00

So the gap = 60 min genuine closure + 60 min waiting for the H1 bucket to roll past the break + cadence. Fail-closed behaviour was safe; the classification is wrong. Recurs every Monday-Thursday: ~4 lost cycles/day, ~1,000/year, systematically concentrated at the post-reopen hour.

### 7. Nothing is watching the live loop

- **No scheduled workflows exist.** Only `ops-aidy-live-recovery-20260913.yml` contains a cron, and it is a one-off ops recovery. Every watchdog (`aidy-capture-freshness-watchdog`, `aidy-d1-row-budget-alert`, `aidy-archive-outbox-watchdog`) triggers only on `workflow_dispatch` or on a push editing its own file.
- **Health telemetry keeps no history.** `aidy_gold_expert_shadow_sync_health` is a singleton (`PRIMARY KEY CHECK (singleton_id = 1)`); every sync overwrites the single row.

The 135-minute gap therefore could not be detected or diagnosed from health telemetry and had to be reconstructed from `market_snapshots`. If the learning loop stops, nothing reports it and no record of degradation survives.

### 8. No baselines recorded anywhere

In the 38-outcome resolved sample: 22 bearish / 11 bullish / 5 neutral. Always answering "bearish" scores **57.9%**. The legacy simple view (36.11%) and M5 (31.82%) are both below random 3-class (33%) and far below the majority-class baseline. Nothing in the codebase computes a baseline, so accuracy figures in Memory and the scorecard are currently uninterpretable.

### 9. Hindsight blacklist misses this codebase's own field names

`FORBIDDEN_HINDSIGHT_KEYS` covers `outcome`, `pnl`, `mfe`, `future_return` but **not** `realised_direction`, `realised_return_bps`, `return_bps`, `score`, `correct`, `impact_class` — the actual column names in `aidy_gold_expert_outcome_ledger`. Real PIT protection comes from the SQL `resolved_at_utc < as_of` filters, which are correct; the blacklist provides false reassurance.

### 10. Scoring and target-label weaknesses

- `gate_scoreable` is True only for `bullish`/`bearish`; neutral and abstain are correctly unscored. Sample N is counted correctly.
- Abstain carries **no cost**. A gate abstaining 80% of the time can accumulate a flattering record on few commits and eventually earn high trust while contributing nothing. No coverage or opportunity-cost term exists.
- `LARGE_MOVE_BPS = 5` / `CYCLE_NEUTRAL_BAND_BPS = 2` are **not volatility-normalised**, so the same label means different things in Asian chop versus an NY event. Verified split is 66% `large` / 34% `normal`, so the impact scale does function, but `large` spans 5-29 bps and lumps noise with genuine moves.

## Verified as sound

These were attacked and held up:

- **PIT window discipline — excellent.** 0/41 windows start before their decision. Each 15-minute window starts 4.2-4.8 min after decision. Windows are adjacent but disjoint.
- **Serial dependence is mild.** Run-structure test on 38 realised directions: **21 runs observed vs ~22.4 expected** under independence. The overlapping-window concern is not the dominant statistical problem; regime-level marginal bias (58% bearish in one session) is.
- **Data revisions handled correctly.** `_decision_candles` admits bars with `first_observed_at <= cutoff` ordered by `revision_index`, so later vendor revisions cannot retroactively alter frozen history. Matches manifest `vendor_revisions_overwrite_prior_evidence: false`.
- **Explainability — excellent and verified.** `aidy_gold_expert_gate_snapshots` = **630 rows = exactly 42 cycles x 15 gates**, plus **3,742** sub-calculator snapshots, plus per-cycle dependency/selector/meta-view/trust JSON and digests. Any past decision is reconstructible to individual sub-calculator votes.
- **Build 19 analogue design is correct.** Similarity computed first, outcomes read strictly post-selection, with guards that raise if outcome values touched selection.
- **Build 2 gate contract is substantive**, not superficial. `_validate_conclusion` enforces real invariants.
- **Legacy MetaAPI boundary is enforced at the data layer**, not only in docs: `market_candles` still holds legacy `metaapi` rows (1 D1, 27 H1, 7 H4) but the aggregate source filter excludes them.
- **AIDY/Super Signals isolation is clean.** No gold expert module reads broker, MetaAPI, MT5 or follower state. Manifest asserts `super_signals_dependency_allowed: false`. Only matches were inert toolbox registry declarations and an unrelated local variable named `follower_total`.
- **Cycle yield is 1:1.** 41 cycle views after activation produced 41 shadow cycles — no post-activation loss.
- **Full regression suite passes**: 1,665 tests locally at the audited SHA.

## Test-suite caveat

The 1,665 passing tests prove **software correctness, not reachability**. `tests/test_gold_meta_direction.py:104` defaults to `n=100, correct=75` with 1-2 gates in a single dependency family, giving a dependency multiplier near 1.0 and authority ~0.3-0.5, so a direction is produced and asserted. Production has N<=23, ~40% accuracy and 91 mutually damped signals, giving ~0.003. **No test asserts that a non-abstain direction is reachable under the live 15-gate / 91-signal dependency graph.** That missing assertion is why findings 1-4 reached production behind green acceptance.

Any Build 23 replay/ablation result that reported non-abstain behaviour exercised a code path production cannot reach, and should be treated as suspect until re-run after finding 1 is fixed.

## Memory discrepancies found and repaired in this commit

Per `AGENTS.md` authority ordering, verified runtime beat Memory in three places:

1. `LIVE_STATE.json.live_worker.deployed_source_sha` was `76cbedc410dbb4f298687bdccff754f444048036` — verified to be the *"Build 3: Conditional Trust & Score Engine v3"* commit of 2026-09-21T11:58, **34 commits behind** the audited HEAD, and containing **none** of `gold_evidence_dependency.py`, `gold_environment_gate_selector.py`, `gold_meta_direction.py`, `gold_meta_replay.py`, `gold_expert_shadow.py`. Production is nonetheless demonstrably running Build 24 (42 shadow cycles in D1; worker `aidy-signals-test` modified 2026-09-22T04:08:28Z). This was **stale metadata, not old code in production**, but it would have sent a future session to the wrong commit.
2. `LIVE_STATE.json.data_health` claimed `degraded / stale_provider_context` with `latest_scheduled_success_utc 2026-09-16T18:22` inside a file whose `verified_at_utc` was 2026-09-22T03:42. Live D1 shows 266 captures since 2026-09-21T06:00 and latest capture 2026-09-22T04:22:35Z.
3. `KNOWN_ISSUES.md` was dated 2026-09-16 and its items 1-2 (Provider Context stale; GitHub Actions credits exhausted) were contradicted by `CURRENT_STATE.md`'s own record of passing Actions runs on 2026-09-21/22.

`CURRENT_STATE.md` was otherwise **honest**: it recorded the 39/39 abstention plainly, labelled the gate stats "small-N and not promotion evidence", and logged the 135-minute gap rather than hiding it. Its one substantive error was classification: it framed the abstention as an expected early-life state ("directional authority remains insufficient") when it is a permanent arithmetic condition.

## Evidence

- Audited source SHA: `47ffe131b9a8d2180c8d78ba3c1dc1b9253b9e4a` (verified against owner-stated HEAD)
- Memory SHA at audit start: `4a26d811728a585dfe9395c49268783f95ad1214` (verified)
- Live D1: `aidy-ops-test` `3588d82a-d686-4430-872d-d4c0e62c3d5d`, read-only queries
- Local full regression at audited SHA: **1,665 passed**
- Live worker: `aidy-signals-test`, modified `2026-09-22T04:08:28Z`
- Shadow sync health at audit: `ok`, `2026-09-22T04:20:13Z`, `latest_meta_direction: abstain`
- Cycles examined: 42 (`aidy_gold_expert_shadow_cycles`), 38 resolved outcomes
- Traced cycle: `2026-09-22T03:55:37.460000+00:00` (environment -> gates -> dependency -> selector -> meta view -> outcome -> scoring)

## Safety state

Unchanged and re-verified. No AIDY live-money execution. No formal-forward authority. No direct MT5 execution from AIDY. Owner live risk remains 1%. No Super Signals risk, provider or behaviour change. No historical data deleted, no historical outcome rewritten, no UNKNOWN converted to synthetic evidence, no holdout touched. Audit was read-only.

## Unresolved

- Findings 1-5 are unfixed and block any directional output.
- Five research gates remain explicit UNKNOWN: macro/event, rates/USD/cross-asset, futures/microstructure, news/mechanism, analogue/episode. `aidy_memory_episodes` is **empty (0 rows)**, so Build 19 has no episode store.
- Build 4 mathematics and Build 23 ablations were **not** audited line-by-line; a second pass is warranted.
- R2/BigQuery/queue internals not audited.
- Statistical validity is impossible at present sample size regardless of fixes: 42 cycles in a single overnight regime.

## Exact next step

Fix in this order. Do not wire new data sources first.

1. **Re-denominate the aggregator** (finding 1). Preferred: treat dependency as an **effective-independent-family count** gate (require k independent families) rather than folding a redundancy ratio into the confidence product. Alternative: compare a normalised share `signed / sum(|authority|)` plus a separate minimum-evidence gate. **Pre-register the new threshold before looking at outcomes.**
2. **Add a reachability test** asserting a non-abstain direction is achievable under the live 15-gate / 91-signal graph with realistic accumulated trust. This is the guard whose absence allowed findings 1-4.
3. **Fix the environment key** (finding 2): remove `utc_clock_bucket_15m` and `utc_weekday` from `GLOBAL_CORE_DIMENSIONS`; keep them as factor dimensions for reduced contexts. `session` and `session_phase` already carry time-of-day at learnable granularity.
4. **Wire both calibration paths** (finding 3).
5. **Backfill H4/D1 aggregates from the existing 40,771 M1 bars** (finding 5) — free, no new vendor, fixes two experts.
6. **Fix the zero-market-minute bucket classification** (finding 6) and the gate-level `abstain` weight handling (finding 4).
7. **Add a cron'd watchdog and an append-only health history table** (finding 7).
8. **Add majority-class, persistence and random baselines to the scorecard** (finding 8).
9. **Soak 2-4 weeks changing nothing**, to obtain a genuine multi-regime sample.
10. **Re-run Build 23** ablations on reachable code paths, then wire Macro/Event (122 `market_event_observations` rows already live, existing PIT vintage machinery, zero cost) and start the Build 19 episode **writer** so analogues accumulate.

Do **not** connect the Databento futures feed yet: +3.33pp on 30 holdout episodes is not distinguishable from noise and would be the only paid dependency in the stack.
