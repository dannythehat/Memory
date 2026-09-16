# Super Signals — Current State

Last verified: **2026-09-16**

Authoritative repo: `dannythehat/super-signals`
Authoritative deployed branch: `feature/day-10-shared-telegram-sources`
Verified source/deploy SHA: `d3f3f8898ff85c3235875bd298d51066f0f5a82e`
Render service: `super-signals-day-8` (`srv-d9qmcgks728c73a555m0`)
Verified live deploy: `dep-dalblphm57gc73d7cta0`
Deploy status: **live**
Quality gate at deployed SHA: **989 passed, 93 skipped, 0 failed, 2 warnings**.

## Current AIDY runtime state

Super Signals now continuously supervises its application-owned AIDY Provider Lab runtime.

The production reliability patch at the deployed SHA does two things:

- keeps AIDY Provider Context probing armed on the existing research cadence instead of stopping after one successful probe;
- runs a one-minute supervisor that can restart the Provider Lab task if that task exits unexpectedly during the trading week.

The existing XAUUSD weekend freeze is still respected.

This reliability layer does **not** grant AIDY broker/live-money authority.

## Current AIDY blocker

The Super Signals side is alive, but upstream AIDY Provider Context is still unhealthy.

Production logs after the current deploy continue to report:

`AIDY Provider Context live probe NOT_READY error=AidyContextTerminalMiss`

The upstream AIDY Worker has fresh market capture but stale Provider Context. Current provider signals have therefore been recorded with `pit_context_stale` instead of current AIDY context.

The AIDY recovery is open as PR #133 in `dannythehat/Aidy-Gold-Signals`, head:

`06ffdc8dc87c8aba8e521b237e181121fbd82cfd`

That exact head passed external Render acceptance: 17/17 focused and 1270/1270 full repository tests, plus Ruff/compile.

Do not call AIDY healthy or fully integrated until a current provider signal successfully receives current AIDY context in production.

## GitHub Actions constraint

The owner has confirmed GitHub Actions credits are exhausted for approximately one week. Recent required AIDY checks showed 0 ms runner execution.

Do not make runtime continuity dependent on GitHub Actions and do not burn time repeatedly rerunning unavailable CI. During this temporary outage use trusted external exact-SHA acceptance where necessary while preserving protection intent.

## Live execution posture

- Trading universe remains Gold/XAUUSD.
- Owner live-risk directive remains **1% only** unless explicitly changed.
- Approved management semantics remain: TP1 + TP2 hit -> move SL to entry; TP3 hit -> move SL to TP2; `move SL to entry` does not mean close the trade.
- Research/shadow/provider-intelligence systems cannot silently change risk, promote/demote live providers or acquire broker authority.

## Product north star — sharpened 16 September

AIDY must now progress from passive Provider Intelligence toward an evidence-scored decision layer for Super Signals.

Target flow:

`provider signal -> PIT-safe Gold context -> provider history -> current exposure -> AIDY decision -> action -> outcome -> counterfactual score -> learning`

Target decision classes:

- `APPROVE`
- `DENY`
- `HOLD/NO_SECOND_ENTRY`
- `CONFLICT_DENY`
- `CLOSE_EARLY`
- `CONTINUE`

The immediate rollout is **shadow decisions for every eligible trade once Provider Context is healthy**. Existing execution rules remain authoritative until individual decision classes earn separate authority.

## Mandatory Decision Ledger

Every AIDY decision must freeze the facts available at decision time:

- provider/signal/message identity and ancestry
- signal and decision timestamps
- exact AIDY context/snapshot IDs and digests
- provider evidence then available
- open account/exposure state
- duplicate/conflict cluster state
- decision/reasons/confidence
- model/rules version
- resulting action when authority exists

Future outcomes must not be written back into the original decision state.

## Counterfactual learning

Every decision must later be scored against a fixed baseline.

Examples:

- deny -> compare with following the provider normally
- close early -> compare AIDY close with original provider-management outcome
- approve -> score realised P&L, MFE/MAE, TP progression and management quality

Persist factual `decision_delta`: money made/saved or money lost because AIDY intervened.

No avoided loss may be claimed unless the baseline path proves it.

## Conditional provider intelligence

A provider is not simply good/bad. AIDY must measure where and how each provider works:

- BUY vs SELL
- session/time of day and weekday
- observable volatility/regime/liquidity conditions
- TP progression and small-profit/runner style
- initial-call quality vs management quality
- effect of provider close/BE/SL/cancel instructions
- duplicate/edit/repost behaviour
- latency/slippage sensitivity
- provider agreement/conflict
- stop/entry geometry
- adverse duration and recovery/re-entry behaviour
- provider-regime specialisation

Where the sample is weak, answer `unknown`.

## Hypothesis/question registry

Create a persistent research-question registry containing stable question ID, exact cohort/filter, required factual features, metric, minimum sample, current sample size, answer/status, uncertainty, last calculation, supporting trade/decision IDs and observational-versus-decision eligibility.

Retrospective patterns do not automatically become live rules. Freeze the rule definition and test it prospectively.

## Duplicate/conflict control — priority

Build canonical exposure clusters using symbol, direction, entry/stop vicinity, provider, message ancestry, timestamp, current broker exposure and cross-provider agreement/conflict.

AIDY must know whether a new trade is already represented, merely an edit/repost, a same-direction equivalent risk addition, opposite exposure or genuinely independent.

If evidence cannot justify choosing between conflicting exposures, fail safely and flag the situation rather than invent certainty.

## Authority graduation

Grant decision authority by class, not wholesale.

Likely order:

1. deterministic duplicate rejection
2. obvious duplicate/conflicting exposure controls
3. provider/regime denies
4. early-close management
5. broader approve/deny/management authority

Every authority class requires prospective evidence, immutable audit trail, explicit enable/disable control, kill switch and owner/live gate. The 1% live-risk directive must not silently change.

## Data Hub role

The AIDY Data Hub remains useful, but it is now a supporting owner/admin surface rather than the central next milestone. It should expose stored Decision Ledger evidence, counterfactual decision delta, provider conditional intelligence, hypothesis state, duplicate/conflict state, AIDY thesis and system health without invoking OpenAI/MetaAPI just because the page refreshes.

## Session rule

Read the 16 September handover first, then verify the live Super Signals branch/Render/Postgres state and the current AIDY Worker/repo state. Source/runtime truth overrides Memory if it has advanced.