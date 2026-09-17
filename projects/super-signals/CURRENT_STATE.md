# Super Signals — Current State

> **Owner mandate in force since 2026-09-17: read [`OWNER_MANDATE.md`](../../OWNER_MANDATE.md) every session.** It sets the goal (AIDY becomes an evidence-scored decision layer that measurably improves Super Signals' profit) and the one boundary that does not move under it (live-money authority stays OFF until explicitly graduated per class).

Last verified: **2026-09-17**

Authoritative repo: `dannythehat/super-signals`
Authoritative deployed branch: `feature/day-10-shared-telegram-sources`
Verified source/deploy SHA: `e4ed35bf148a25f257c232e5204ea36e2008c715`
Render service: `super-signals-day-8` (`srv-d9qmcgks728c73a555m0`)
Verified live deploy: `dep-dalr3deq1p3s73a0o9v0`
Deploy status: **live**
Quality gate at deployed SHA: **989 passed, 93 skipped, 0 failed, 2 warnings** (local full-suite baseline; GitHub Actions remains credit-exhausted, same no-runner-executed signature diagnosed earlier this session, not a real failure).

## AIDY blind Gold learning exam — in build, research-only (2026-09-17)

Owner explicitly redirected testing away from re-running already-proven Claude decision-ledger checks. New objective: measure whether AIDY actually understands Gold/provider-market relationships and becomes measurably smarter on later unseen data.

AIDY repo PR #135 (`feature/blind-gold-learning-exam-20260917`), latest branch commit recorded here `3492beaf064780469367a28564bef3739aec18e9`, now contains a governed chronological blind scorer plus a PIT-safe bridge from immutable AIDY episode memory and score-eligible forward outcomes. It counts only learning cards available before each episode, excludes same-episode future learning, scores direction/Brier/difficulty where AIDY genuinely emitted the needed ex-ante fields, and reports `insufficient_evidence`, `memory_accumulating`, `learning_candidate`, `learning_observed`, or regression. Memory growth alone can never be labelled learning.

The exam now extracts frozen contemporaneous market context already preserved in episode memory (`regime_state`/`setup_state`): market structure, volatility, liquidity/spread state, session and event state where present. Difficulty is assigned from those frozen features only. Missing context stays unknown and is surfaced through a context-coverage report rather than retrospectively invented. Provider identity/context is likewise not fabricated when absent; provider-conditioned learning needs a PIT-safe join.

**Do not claim AIDY is smarter yet.** PR #135 is open/research-only and the real production/D1 blind scorecard still has to be run with adequate chronological unseen samples. If later batches do not improve, the result must remain memory accumulation/regression. Full handover: `handovers/2026-09-17-aidy-blind-gold-learning-exam.md`.

Safety unchanged: no broker authority, no execution-rule change, 1% live-risk directive unchanged.

## AIDY visibility layer — v1 live, both repos (2026-09-17)

Investigated build item #4 (hypothesis registry) before building it and found it already exists: `provider_conditional_hypotheses`/`_runs`/`_results` (Day 13) -- 15,744 hypotheses preregistered with real Benjamini-Hochberg significance testing and out-of-sample gating, just barely fed (42 of 15,744 ever tested, 0 significant). A "needs more live evidence" problem, not a "needs code" problem -- building a second registry would have duplicated real, more rigorous work. Built the visibility layer instead, at the owner's direction ("keep building, get AIDY ready for launch").

- **Backend** (`dannythehat/super-signals` PR #186): `GET /admin/aidy/overview`, owner/trading_admin gated (`activity.view` permission, same as the existing Day 35 control centre). Returns decision totals, per-class breakdown with net delta and resolution mix, top/bottom cohort standouts (min 15 resolved trades), hypothesis registry status. Read-only, no writes, no broker/OpenAI calls.
- **Frontend** (`dannythehat/super-signals-website` PR #4): **https://smartsignals.site/admin-aidy** (not `/admin/aidy`). Same auth pattern as the existing `/complimentary` page.

## Provider coverage — v1 live, both repos (2026-09-17)

Owner asked directly, looking at the new visibility dashboard: *"Why is the skills so low? We have 38 traders no? Why isn't Aidy studying them all?"* Investigated with real production SQL rather than guessing. Finding: AIDY was already deciding on **41 of 63** connected sources (46 have any trade history at all). The dashboard looked thin because its cohort-standouts table requires 15+ resolved trades in one specific side+session+weekday slice (70 possible slices per provider) — almost nothing clears that yet, hiding ~36 of the 41 actively-decided providers. This was a **dashboard display-threshold gap, not a real coverage gap** in what AIDY processes.

Fixed same-session in both repos:
- **Backend** (`dannythehat/super-signals` PR #187, merged `e4ed35bf148a25f257c232e5204ea36e2008c715`): coverage totals + a full blended (non-cohort-sliced) per-provider table added to `GET /admin/aidy/overview`.
- **Frontend** (`dannythehat/super-signals-website` PR #5, merged `9aec4e4f354b60ec80536cbe8120133b8373ba25`): new coverage stat row + "every provider AIDY has decided on" table at **https://smartsignals.site/admin-aidy**. Same PR also fixed a real mobile layout bug the owner caught via phone screenshots ("Bit shit isn't it") — tables were cut off mid-column; now stack as cards below 640px, verified with an actual Playwright screenshot at a 390px viewport, not just a `curl` 200 check.

Real spread confirmed across named providers: net P&L from **-$1,351.26** (TRADE GLOBAL, 36.6% win rate) to **+$1,605.31** (GOLDHUNTER, 78.6% win rate) — AIDY is genuinely differentiating providers, not producing flat output. Full detail: `LIVE_STATE.json` → `provider_coverage_v1`.

## Book-flat-before-merge rule dropped (2026-09-17)

Danny: *"Merge it.. nobody cares about open positions."* Routine research merges are no longer held on open-position count. Execution/risk-sizing changes still require scrutiny. Full detail: `OWNER_MANDATE.md`.

## Scoreboard cohort dimensions — v1 live (2026-09-17)

PR #185 merged/deployed. `provider_trade_scoreboard_by_cohort` splits provider performance by source, side, session and weekday (Europe/Sofia). Cohort evidence is not yet wired into live AIDY decisions.

## Decision Ledger outcome scoring — v1 live (2026-09-17)

PR #184 merged/deployed. `AidyDecisionOutcomeRuntime` scores decisions against `provider_trade_scores` fixed baseline. `approve` gets delta 0; denied/held trades are scored counterfactually from already-computed baseline outcomes. Early historical evidence showed duplicate/repost holds promising while conflict-deny was not convincing. Treat this as thin historical evidence, not authority.

## Current AIDY runtime state — recovered / READY, multi-cycle verified

17 September production patch hardened Super Signals AIDY M1 transport with bounded retry/backoff. Sustained health was independently confirmed across multiple systems/cycles; do not cite the one-time startup READY probe alone. Full detail: `handovers/2026-09-17-continuous-health-verification.md`.

## Day 14 governance issue

`PROVIDER_DAY14_GOVERNANCE_ERROR` root cause is a preregistration-boundary methodology mismatch as registry cohorts grow. Logging was fixed; methodology choice remains unresolved. Zero live-money impact (`research_only=True`).

## Live execution posture

- Gold/XAUUSD only.
- **1% only** live-risk directive unless owner explicitly changes it.
- TP1 + TP2 -> SL to entry; TP3 -> SL to TP2; move SL to entry != close.
- Research/provider intelligence cannot silently change risk, promote/demote live providers or acquire broker authority.
- AIDY live-money authority OFF.
- XAUUSD weekend freeze unchanged.

## Product north star

`provider signal -> PIT-safe Gold context -> provider history -> current exposure -> AIDY decision -> action -> outcome -> counterfactual score -> learning`

AIDY must become measurably better on forward unseen evidence, not merely accumulate more data.