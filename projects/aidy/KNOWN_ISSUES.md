# AIDY — Known Issues / Deferred Work

Updated: **2026-09-22**

Only keep unresolved or deliberately deferred items here. Verify source/runtime before acting because Memory can become stale.

## Current

### 0. Expert-gate decision layer cannot produce a direction — ACTIVE / RED, BLOCKING

Found by independent adversarial audit on 2026-09-22 at verified SHA `47ffe131b9a8d2180c8d78ba3c1dc1b9253b9e4a`. Full detail, line references and fix order: `projects/aidy/handovers/2026-09-22-independent-24-build-audit.md`.

Five blocking defects. All are engineering/wiring defects, not flaws in the architecture:

- **0a. Aggregator threshold unreachable.** `MIN_DIRECTIONAL_WEIGHT` 0.30 vs measured live `directional_total` max **0.016939** (typical 0.002-0.009). Build 20's redundancy ratio (91 raw signal-units to 4.0 effective) is multiplied into Build 21's confidence product and summed by Build 22 against an absolute constant — a units mismatch. Realistic mature ceiling **0.179**. Abstention is permanent at any N.
- **0b. Environment key explodes.** 41 cycles produced 41 distinct `environment_key` values; `utc_clock_bucket_15m` and `utc_weekday` are in `GLOBAL_CORE_DIMENSIONS`. `global_core` max N=1 over 570 rows. **Zero contextual scopes ever qualify**: independent verification counted **196 `gate_global` selections and 50 `neutral_prior` selections** among the directional gates (the latter in early cycles before any history existed). Corrects an earlier overstatement of "100% fallback to gate_global" — the substance is unchanged: AIDY is learning broad gate-global performance, not "what works in this environment", which is the core idea the programme was built for.
- **0c. Calibration subsystems dead.** `calibration_rows=()` and `meta_calibration_rows=()` hardcoded empty in the live bundle. Build 21 calibration multiplier stuck at 0.85 forever; Build 22 `calibrated_confidence` permanently `None`. Circular: meta-calibration needs non-abstain history that 0a prevents.
- **0d. Best gates contribute zero.** Gate-level `abstain` gets no directional weight. H1 abstains 29/41, H4 33/41; M5 (worst, 31.82%) commits 25/41 and dominates. H4 has concluded bearish 0/41.
- **0e. D1/H4 starved.** Verified admitted depth D1 **10 bars**, H4 **42 bars**. Daily structure is not derivable from 10 observations; this is the mechanical cause of 0d's H4 asymmetry. **40,771 M1 bars from 2026-08-12 already exist** — backfilling aggregates fixes both experts at zero data cost and is higher value than wiring any UNKNOWN gate.

Do not wire new data sources before these are fixed. Do not read the 41/41 abstention as calibrated caution.

### 0.1 No reachability test — process gap that allowed 0a-0d to ship — ACTIVE

The 1,665-test suite proves software correctness, not reachability. `tests/test_gold_meta_direction.py` defaults to `n=100, correct=75` with 1-2 gates in a single dependency family (dependency multiplier ~1.0, authority ~0.3-0.5); production runs N<=23, ~40% accuracy and 91 mutually damped signals (~0.003). **No test asserts a non-abstain direction is reachable under the live 15-gate / 91-signal graph.** Add that assertion as part of fixing 0a. Treat any Build 23 ablation that reported non-abstain behaviour as suspect until re-run.

### 0.2 Cycle loss from zero-market-minute bucket — ACTIVE, ~1,000 cycles/year

`twelve_data_market.py:216,229` classifies a bucket with **no market minutes** as inadmissible rather than not-applicable. Traced root cause of the 135.2-minute gap of 2026-09-21, which was **not an outage** — capture ran every 5 minutes throughout. The H1 bucket 21:00-22:00 UTC (CME daily maintenance break) reports `expected_market_minutes: 0`, `coverage_ratio: "0.000000"`, `admissible: false`, forcing `capture_status: partial` until the bucket rolls at 23:02. Recurs every Monday-Thursday, ~4 lost cycles/day, concentrated at the post-reopen hour. Fail-closed behaviour is safe; the classification is wrong.

### 0.3 No automated monitoring of the learning loop — ACTIVE

No scheduled workflows exist (only `ops-aidy-live-recovery-20260913.yml` has a cron, a one-off ops recovery). Every watchdog triggers only on `workflow_dispatch` or a push editing its own file. `aidy_gold_expert_shadow_sync_health` is a singleton row that each sync overwrites, so no health history survives. The 135-minute gap had to be reconstructed from `market_snapshots` because telemetry could not show it. The loop can stop learning with no alert and no record.

### 0.4 No baselines; outcome labels not volatility-normalised — ACTIVE

Nothing computes a baseline, so recorded accuracy figures are uninterpretable. On the 38-outcome resolved sample (22 bearish / 11 bullish / 5 neutral) always answering "bearish" scores **57.9%**; legacy 36.11% and M5 31.82% are below both random 3-class (33%) and majority-class. Add majority-class, persistence and random baselines to the scorecard before any promotion reasoning. Separately, `LARGE_MOVE_BPS = 5` and `CYCLE_NEUTRAL_BAND_BPS = 2` are fixed rather than volatility-normalised, so a label means different things in Asian chop versus an NY event. Abstain also carries no cost, so chronic abstainers can earn trust while contributing nothing.

### 0.5 Hindsight blacklist omits this codebase's own outcome fields — ACTIVE, low severity

`FORBIDDEN_HINDSIGHT_KEYS` covers `outcome`, `pnl`, `mfe`, `future_return` but not `realised_direction`, `realised_return_bps`, `return_bps`, `score`, `correct`, `impact_class` — the actual `aidy_gold_expert_outcome_ledger` columns. Real PIT protection is the SQL `resolved_at_utc < as_of` filtering, which was verified correct; the blacklist gives false reassurance and would not catch the most likely accidental leak here.

### 1. Provider Context stale / GitHub Actions credits exhausted — RESOLVED-STALE as of 2026-09-22

The two items previously recorded here (Provider Context stale since 2026-09-15, and GitHub Actions credits exhausted) are **contradicted by later verified evidence** and are retained only as history:

- Live D1 shows market capture healthy: 266 captures since 2026-09-21T06:00, latest `2026-09-22T04:22:35Z`, shadow sync health `ok` at `2026-09-22T04:20:13Z`.
- `CURRENT_STATE.md` records passing GitHub Actions runs on 2026-09-21/22 (acceptance `35623113260`, rollout `35630952162`, D1 diagnostic `35630952252`), so the Actions outage ended.

The verification lesson below is still worth keeping. Original record follows.

#### Historical record — Provider Context stale while market capture is fresh (as recorded 2026-09-16)

The Worker is capturing fresh Twelve Data on direct Cron, but the latest accepted Provider Context snapshot is still from `2026-09-15T20:57:36.761999+00:00` (still true as of 2026-09-16T18:10Z re-check). Current Super Signals joins therefore fail closed with `pit_context_stale` / `AidyContextTerminalMiss`.

Open AIDY PR #133, head `01c6a955c5c7c513a6db86f70cdc2e7d146ea246` (was `06ffdc8d`, updated 2026-09-16 -- see correction below). Independently re-verified locally, outside GitHub Actions entirely: compile clean, 33/33 focused tests, 1270/1270 full suite, ruff clean. Both safety claims checked directly in the diff, not just trusted from the PR body: `live_money_execution_allowed` is hardcoded `False` unconditionally, and `forward_live_observer.py` keeps its own separate, unmodified `capture_status != "complete"` gate -- it never calls the loosened snapshot function this PR touches.

**Correction to what was recorded here before:** the prior "17/17, ruff:pass" figures were accurate for an earlier SHA (`327ad76e`) cited inside the PR body, not for the actual open head at the time (`06ffdc8d`). Re-running against the exact open head found ruff genuinely failing (`UP035`, deprecated `typing.Mapping` import) -- unrelated to the Actions outage, a real bug the prior verification pass did not catch because it checked the wrong commit. Fixed as an import-only change and re-verified. **Lesson for future verification: diff the PR body's cited SHA against `pull_request.head.sha` before trusting any acceptance numbers it quotes.**

The PR is now blocked purely by GitHub's required-status-checks rule (`merge_pull_request` returns `405: 2 of 2 required status checks are failing` -- no other rule cited: no missing review, no other violation). **Claude cannot clear this or deploy the result** -- see the tooling gap below. Two manual actions only the owner can take are recorded in `LIVE_STATE.json -> provider_context_recovery.tooling_gap_blocking_claude`.

#### Historical record — GitHub Actions unavailable due to exhausted credits (as recorded 2026-09-16; ended by 2026-09-21)

The owner reports GitHub Actions credits are exhausted for approximately one week. Independently confirmed 2026-09-16 across 3 separate workflow runs on 2 different branches, hours apart: every run completes in 2-3 seconds with `conclusion=failure` and a 404 on log download (no runner ever executed). Not this-PR-specific.

**Claude has no way around this in the current environment**, and this is a capability gap worth recording precisely so no future session wastes time rediscovering it:
- **No ruleset/branch-protection tool.** This session's GitHub MCP server exposes PRs, checks, files, merges -- nothing for reading or editing repository rules. No `gh` CLI, no raw API access (both explicitly withheld). A direct `merge_pull_request` attempt confirmed there is no admin-bypass path through the merge API with this token either.
- **No Cloudflare deploy path.** No `CLOUDFLARE_API_TOKEN`/`CLOUDFLARE_ACCOUNT_ID` in this sandbox's environment. The Cloudflare MCP tools available are read-only for Workers (get/list/get_worker_code) -- no deploy/put tool. `aidy-signals-test` has no visible native Cloudflare git integration (unlike Super Signals on Render, which deploys independently of GitHub Actions), so the only deploy path is `uv run pywrangler deploy` inside the same GitHub Actions workflow that is down.

Do not repeatedly rerun unavailable CI -- confirmed dead across multiple attempts already. The owner needs to either bypass the 2 required checks for this one merge (restoring the rule once Actions capacity returns) and then deploy himself (wait for Actions, or run `wrangler deploy` locally against the merged `main`, preserving the `* * * * *` cron exactly as the dead workflow would have asserted it), or wait out the outage.

### 3. Formal-forward/live-money authority remains OFF

Do not treat new Decision Ledger, shadow decisions or provider intelligence as live-money authority. Decision classes must be separately graduated through prospective evidence and explicit owner/live gates.

### 4. Decision intelligence not yet implemented end-to-end

The new central roadmap requires:

- immutable AIDY Decision Ledger;
- counterfactual scoring and factual decision delta;
- conditional provider intelligence;
- persistent hypothesis/question registry;
- duplicate/conflict exposure engine;
- prospective shadow decisions for every eligible trade after Provider Context recovery.

This is the next major product build after restoring current context health.

### 5. Provider-market credential hygiene

Any bearer/token rotation or remediation must be synchronized with Super Signals and performed in a controlled window with rollback. Never expose credential values in Memory, logs or chat.

### 6. Historical secret-remediation caution

Deleting a file in a later commit does not erase Git history. Any history rewrite must be deliberate and must not casually rewrite protected production history.

## Rule

Do not call AIDY fully healthy until current Provider Context is production verified and a current Super Signals provider signal successfully receives current AIDY context.