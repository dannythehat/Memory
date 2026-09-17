# Super Signals — Current State

Last verified: **2026-09-17**

Authoritative repo: `dannythehat/super-signals`
Authoritative deployed branch: `feature/day-10-shared-telegram-sources`
Verified source/deploy SHA: `356dfcf1801f70c786ff7fa2de38ce88d55ec071`
Render service: `super-signals-day-8` (`srv-d9qmcgks728c73a555m0`)
Verified live deploy: `dep-dalma2gae00c739qlul0`
Deploy status: **live**
Quality gate at deployed SHA: **989 passed, 93 skipped, 0 failed, 2 warnings**.

## Current AIDY runtime state — recovered / READY

The 17 September production patch hardened the Super Signals AIDY M1 transport against transient upstream/network failures. `AidyMarketClient.fetch_m1()` now uses bounded retry/backoff for connection/read timeouts, connection errors, protocol failures, HTTP 429 and transient 5xx responses rather than allowing a single transient transport failure to terminate that resolution cycle.

Production evidence after deploy:

- Render deploy `dep-dalma2gae00c739qlul0` reached **live** at `2026-09-17T04:00:25Z`.
- New production instance started the `AIDY Provider Lab resolver loop` at `2026-09-17T04:00:26Z`.
- AIDY Provider Context live probe returned `READY` at `2026-09-17T04:00:37Z` with `context_lag_seconds=196`.
- No new AIDY error / `pit_context_stale` event was observed in the checked post-deploy log window.

The earlier `AidyContextTerminalMiss` / stale-context blocker recorded on 16 September is therefore no longer the current verified Super Signals production state.

This recovery does **not** grant AIDY broker/live-money authority.

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

## Counterfactual learning

Every decision must later be scored against a fixed baseline. Persist factual `decision_delta`: money made/saved or money lost because AIDY intervened. No avoided loss may be claimed unless the baseline path proves it.

## Conditional provider intelligence

A provider is not simply good/bad. AIDY must measure where and how each provider works: BUY vs SELL; session/time and weekday; observable volatility/regime/liquidity; TP progression; initial-call vs management quality; close/BE/SL/cancel instructions; duplicate/edit/repost behaviour; latency/slippage; agreement/conflict; stop/entry geometry; adverse duration and recovery/re-entry; and provider-regime specialisation. Where sample is weak, answer `unknown`.

## Authority graduation

Grant decision authority by class, not wholesale. Likely order: deterministic duplicate rejection; obvious duplicate/conflicting exposure controls; provider/regime denies; early-close management; broader approve/deny/management authority. Every authority class requires prospective evidence, immutable audit trail, explicit enable/disable control, kill switch and owner/live gate. The 1% live-risk directive must not silently change.

## Session rule

Verify live Super Signals branch/Render/Postgres state and current AIDY Worker/repo state before acting. Source/runtime truth overrides Memory if it has advanced. The current verified Super Signals production recovery point is SHA `356dfcf1801f70c786ff7fa2de38ce88d55ec071`, deploy `dep-dalma2gae00c739qlul0`.