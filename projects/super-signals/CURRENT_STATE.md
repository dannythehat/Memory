# Super Signals — Current State

> **Owner mandate in force since 2026-09-17: read [`OWNER_MANDATE.md`](../../OWNER_MANDATE.md) every session.** It sets the goal (AIDY becomes an evidence-scored decision layer that measurably improves Super Signals' profit) and the one boundary that does not move under it (live-money authority stays OFF until explicitly graduated per class).

Last verified: **2026-09-17**

Authoritative repo: `dannythehat/super-signals`
Authoritative deployed branch: `feature/day-10-shared-telegram-sources`
Verified source/deploy SHA: `d036db3c97531747df590972afd94a4351b0e313`
Render service: `super-signals-day-8` (`srv-d9qmcgks728c73a555m0`)
Verified live deploy: `dep-dalokbnqj5pc73e5af6g`
Deploy status: **live**
Quality gate at deployed SHA: **989 passed, 93 skipped, 0 failed, 2 warnings** (local full-suite baseline; GitHub Actions still credit-exhausted as of this deploy -- PR #184's `api`/`web` checks failed in ~2s each, the same no-runner-executed signature diagnosed earlier this session, not a real failure).

## Decision Ledger outcome scoring — v1 live, first real evidence in (2026-09-17)

PR #184 merged and deployed. `AidyDecisionOutcomeRuntime` scores every AIDY decision against `provider_trade_scores` as the fixed baseline -- an `approve` always equals the baseline (delta=0, never manufactured credit); a `deny`/`conflict_deny`/`hold_no_second_entry` is scored as if the trade was never taken, so a denied trade that really lost reads `confirmed_helped` and one that really won reads `confirmed_hurt`, purely from the sign of an already-computed number.

First production pass, scored against the historical backlog (thin sample, not a verdict):

- **`hold_no_second_entry`** (duplicate/repost within 15 min): 20 helped (+€465) vs 3 hurt (-€69) -- **net +€396**. The strongest early candidate for real authority.
- **`conflict_deny`** (opposite-direction book exposure): 27 hurt (-€579) vs 26 helped (+€527) -- **net -€52, roughly a wash**. Not yet convincing; needs more evidence before trusting it.
- No provider has yet been denied on track record alone (every `approve` so far is either thin evidence or an acceptable record -- nobody has crossed the deny bar yet).

Merged with 1 open position on the book -- the owner explicitly said "just merge it" rather than wait for it to flatten, overriding the standing book-flat-before-merge rule by direct instruction. That rule was crossed once, deliberately, not silently relaxed going forward.

## Current AIDY runtime state — recovered / READY, multi-cycle verified

The 17 September production patch hardened the Super Signals AIDY M1 transport against transient upstream/network failures. `AidyMarketClient.fetch_m1()` now uses bounded retry/backoff for connection/read timeouts, connection errors, protocol failures, HTTP 429 and transient 5xx responses rather than allowing a single transient transport failure to terminate that resolution cycle.

**Important caveat on the startup probe:** `aidy_shadow_runtime.py`'s "Provider Context live probe READY" log fires exactly once per process lifetime (`if context_client is not None and not context_probe_ready`) and never again. One READY line is not evidence of sustained health — do not cite it alone.

Sustained health was instead independently confirmed across multiple systems and cycles (full detail: `handovers/2026-09-17-continuous-health-verification.md`):

- AIDY's own D1 `market_snapshots`: **53 consecutive `complete` snapshots, 0 `partial`**, every ~5 minutes from `2026-09-17T00:02Z` through `04:22Z` — spanning well before and after the deploy.
- Super Signals `shadow_trades`: 83 rows updated since deploy, `aidy_m1_cursor_at` advancing `03:43Z → 04:10Z` across multiple distinct cycles — the resolver is doing real repeated work.
- Full post-deploy log window: zero `pit_context_stale` / `AidyContextTerminalMiss` / `NOT_READY` / tracebacks.
- Live AIDY `/health` at time of writing: `status: ok`, `data_health.status: fresh`, lag 157s.

Render deploy `dep-dalma2gae00c739qlul0` reached **live** at `2026-09-17T04:00:25Z`, superseded by `dep-dalmjj3bc2fs7387mrv0` (a second, unrelated fix, see below) at `04:20Z`, also live.

The earlier `AidyContextTerminalMiss` / stale-context blocker recorded on 16 September is confirmed superseded by this multi-cycle evidence, not by the single startup probe alone.

This recovery does **not** grant AIDY broker/live-money authority.

## Second, unrelated issue found while verifying — partially fixed

`PROVIDER_DAY14_GOVERNANCE_ERROR=RuntimeError` had been repeating since at least 16 September 18:15, unrelated to M1/context. Root cause: `_frozen_boundary()` requires every row in `provider_conditional_hypotheses` to share one `preregistered_at`; production has two legitimate cohorts (15,360 rows from 09-07, 384 from a newly-onboarded shadow source on 09-14) — not a bug in the writer, and the registry will keep growing this way, so the guard can never pass again as written. Fixed: the retry loop now logs the real reason instead of just the exception type (PR #182, deploy `dep-dalmjj3bc2fs7387mrv0`, live and verified). **Not fixed:** whether to freeze one boundary per run or per hypothesis is an anti-hindsight methodology decision left for the owner — changing it changes what counts as in-sample evidence for every provider evaluation. Zero live-money impact either way (`research_only=True` end to end).

## Runtime continuity

Super Signals continuously supervises its application-owned AIDY Provider Lab runtime. Provider Context probing remains armed on the existing research cadence and a one-minute supervisor can restart the Provider Lab task if it exits unexpectedly during the trading week. The existing XAUUSD weekend freeze remains respected.

## Live execution posture

- Trading universe remains Gold/XAUUSD.
- Owner live-risk directive remains **1% only** unless explicitly changed.
- Approved management semantics remain: TP1 + TP2 hit -> move SL to entry; TP3 hit -> move SL to TP2; `move SL to entry` does not mean close the trade.
- Research/shadow/provider-intelligence systems cannot silently change risk, promote/demote live providers or acquire broker authority.

## Product north star

AIDY must progress from passive Provider Intelligence toward an evidence-scored decision layer for Super Signals.

Target flow:

`provider signal -> PIT-safe Gold context -> provider history -> current exposure -> AIDY decision -> action -> outcome -> counterfactual score -> learning`

Target decision classes: `APPROVE`, `DENY`, `HOLD/NO_SECOND_ENTRY`, `CONFLICT_DENY`, `CLOSE_EARLY`, `CONTINUE`.

With Provider Context now production-READY, the next build can proceed with shadow decisions for every eligible trade while existing execution rules remain authoritative until individual decision classes earn separate authority.

## Mandatory Decision Ledger

Every AIDY decision must freeze the facts available at decision time: provider/signal/message identity and ancestry; signal and decision timestamps; exact AIDY context/snapshot IDs and digests; provider evidence then available; open account/exposure state; duplicate/conflict cluster state; decision/reasons/confidence; model/rules version; and resulting action when authority exists. Future outcomes must not be written back into the original decision state.

**v1 merged and live in production** (2026-09-17, PR #183): `aidy_decisions` / `aidy_decision_outcomes` (migration `0088`), `AidyDecisionEngine`, `AidyDecisionRunner`, `AidyDecisionRuntime`, wired into `main.py` startup/shutdown alongside the existing scoring runtime. Deterministic only — duplicate/repost check, opposite-direction book-exposure conflict check, then provider track record from `provider_trade_scoreboard` (min 20 resolved trades; denies only when avg P&L ≤ -$3 **and** win rate ≤ 35% together, never either alone). No model call yet — that is a separate, costed piece not yet switched on. Supersedes the unwired, zero-row Day 16/20 `provider_veto_counterfactual_*` / `provider_management_counterfactual_*` tables rather than building alongside them. Append-only and `research_only=True` / `live_money_execution_allowed=False` are CHECK-constrained and trigger-enforced at the schema level, not documentary. Full detail: `handovers/2026-09-17-decision-ledger-v1.md`.

Merged into `feature/day-10-shared-telegram-sources` (merge commit `acbe35a1`), deployed via Render (`dep-dalnocp5efls73bleqog`, live `2026-09-17T05:38:15Z`), and **verified actually running**: `AidyDecisionRuntime`'s first production pass completed and logged `decided 1241/1241` at `05:43:33Z` — not just deployed-and-idle, confirmed writing real rows to `aidy_decisions`. No new errors introduced; the app's `/health` returned steady 200s throughout.

While building this, found and fixed a real pre-existing bug: `services/api/migrations/env.py` unconditionally called `fileConfig()` on every Alembic migration, which replaces the root logger's handlers process-wide and silently discards pytest's `caplog` capture handler for the rest of that test session — not just for the test that ran the migration, every test afterward. It had never been triggered before because no alembic-invoking test file happened to sort alphabetically before `test_aidy_shadow_runtime_startup.py`; the new `test_aidy_decision_ledger.py` was the first. Fixed by skipping `fileConfig()` when `PYTEST_CURRENT_TEST` is set; real CLI/deploy usage is unaffected.

## Counterfactual learning

Every decision must later be scored against a fixed baseline. Persist factual `decision_delta`: money made/saved or money lost because AIDY intervened. No avoided loss may be claimed unless the baseline path proves it.

## Conditional provider intelligence

A provider is not simply good/bad. AIDY must measure where and how each provider works: BUY vs SELL; session/time and weekday; observable volatility/regime/liquidity; TP progression; initial-call vs management quality; close/BE/SL/cancel instructions; duplicate/edit/repost behaviour; latency/slippage; agreement/conflict; stop/entry geometry; adverse duration and recovery/re-entry; and provider-regime specialisation. Where sample is weak, answer `unknown`.

## Authority graduation

Grant decision authority by class, not wholesale. Likely order: deterministic duplicate rejection; obvious duplicate/conflicting exposure controls; provider/regime denies; early-close management; broader approve/deny/management authority. Every authority class requires prospective evidence, immutable audit trail, explicit enable/disable control, kill switch and owner/live gate. The 1% live-risk directive must not silently change.

## Session rule

Verify live Super Signals branch/Render/Postgres state and current AIDY Worker/repo state before acting. Source/runtime truth overrides Memory if it has advanced. The current verified Super Signals production recovery point is SHA `356dfcf1801f70c786ff7fa2de38ce88d55ec071`, deploy `dep-dalma2gae00c739qlul0`.