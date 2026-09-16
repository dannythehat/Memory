# Super Signals — Confirmed Open Follow-ups / Regression Watchlist

Updated: **2026-09-16**

This file distinguishes confirmed active issues from historical incidents. Do not describe historical incidents as unresolved unless fresh production evidence confirms recurrence.

## Confirmed active issues / priorities

### 1. Upstream AIDY Provider Context is NOT_READY — ACTIVE / RED

Super Signals itself is live on SHA `d3f3f8898ff85c3235875bd298d51066f0f5a82e` and now continuously supervises its AIDY Provider Lab runtime, but upstream AIDY Provider Context remains stale.

Production logs continue to show:

`AIDY Provider Context live probe NOT_READY error=AidyContextTerminalMiss`

Current AIDY market capture is fresh, but Super Signals still receives `pit_context_stale` for current joins. Do not describe AIDY as healthy until a current provider signal successfully receives current AIDY context.

### 2. GitHub Actions credits unavailable for approximately one week

The owner has confirmed GitHub Actions credits are exhausted temporarily. AIDY required checks are failing before normal runner work and showed 0 ms runner execution.

Do not make production runtime continuity depend on Actions and do not repeatedly rerun unavailable jobs. Use trusted external exact-SHA validation for urgent recovery while preserving normal protection intent.

### 3. AIDY Decision Ledger / counterfactual engine not yet built end-to-end

The next central build is now decision intelligence, not simply a dashboard.

Once AIDY context is healthy, Super Signals must capture one shadow AIDY decision for every eligible trade and later score it against a fixed baseline so the owner can measure factual money made/saved or lost because AIDY intervened.

### 4. Duplicate/conflict exposure control is a priority

AIDY/Super Signals still need a canonical exposure-cluster layer that can identify an already represented idea, edit/repost, materially equivalent same-direction risk addition, opposite exposure or genuinely independent trade.

This capability should be among the first AIDY decision classes evaluated for authority because it addresses duplicate/conflicting risk directly.

### 5. Conditional provider intelligence still needs prospective evidence

Existing Provider Intelligence foundations are useful, but AIDY must answer provider questions by direction, session/time, regime/volatility/liquidity conditions, management quality, TP progression, latency, agreement/conflict and other exact cohorts rather than rely on one provider-wide win rate.

Where sample floors are not met, use `unknown` / `WAITING-FOR-FORWARD-EVIDENCE`.

### 6. AIDY question/hypothesis registry not yet implemented

Research questions need durable IDs, exact cohorts, metrics, minimum samples, current samples, uncertainty, supporting trades/decisions and observational-versus-decision eligibility. Retrospective findings must not silently become live rules.

### 7. Settlement efficiency cleanup

Four historical August `broker_filled_position_not_visible` rows previously kept the fast settlement/history path active. Preserve audit evidence, but quarantine these stale rows from the fast path after bounded retry/repair handling.

This is an efficiency/hygiene follow-up, not evidence that live settlement is currently failing.

### 8. Protection polling efficiency

The protection path can read broker positions/orders even when there are no protection plans. Reorder the path so it returns before broker reads when no plans exist.

### 9. Redundant MetaAPI Gold-price read

The UI Gold quote already uses free Gold feeds. Dashboard broker-state collection still contains a redundant MetaAPI XAU price read that should be removed where it is not required for execution logic.

### 10. Usage telemetry

Exact OpenAI token/cost telemetry and consolidated MetaAPI request telemetry are not yet persisted.

### 11. Weekend edited-message edge

Original weekend messages are blocked and the automatic runtime is frozen. A narrow edge remains where a pre-weekend message edited during closure could potentially be recovered after reopen unless `edited_at` is also freeze-gated.

### 12. AIDY Data Hub

The owner-facing Data Hub remains useful but is now a supporting visibility surface, not the central next milestone. It should expose stored Decision Ledger/counterfactual/provider-intelligence state without creating new external-call loops on page refresh.

## Historical regression watchlist — not currently proven active

Only call these active if fresh production evidence confirms recurrence:

- missed new trades;
- duplicate handling from edited Telegram posts;
- missed `move SL`, BE, take-loss or cancel instructions;
- hidden/open trades not visible in the app;
- provider-specific grammar/interpretation failures;
- notification delays;
- slow stats refresh;
- login persistence/account-page issues;
- calendar trade-visibility issues;
- balance/equity presentation issues.
