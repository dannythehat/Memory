# Super Signals — Confirmed Open Follow-ups / Regression Watchlist

Updated: **2026-09-13**

This file distinguishes **confirmed open follow-ups** from **historical incidents that are not currently proven active**. Do not describe historical incidents as unresolved unless production evidence re-confirms them.

## Confirmed open follow-ups

### 1. Forward statistical evidence is still sparse
AIDY Provider Intelligence B-F is engineering/prod verified, but broad provider ranking/profitability/promotion claims are not statistically validated yet. Use `WAITING-FOR-FORWARD-EVIDENCE` where sample floors are not met.

### 2. Settlement efficiency cleanup
Four historical August `broker_filled_position_not_visible` rows previously kept the fast settlement/history path active. Preserve audit evidence, but quarantine these stale rows from the fast path after bounded retry/repair handling.

This is an **efficiency/hygiene follow-up**, not evidence that live settlement is currently failing.

### 3. Protection polling efficiency
The protection path can read broker positions/orders even when there are no protection plans. Reorder the path so it returns before broker reads when no plans exist.

This is an **API-efficiency improvement**, not a known trade-management failure.

### 4. Redundant MetaAPI Gold-price read
The UI Gold quote already uses free Gold feeds. Dashboard broker-state collection still contains a redundant MetaAPI XAU price read that should be removed where it is not required for execution logic.

This is an **API-efficiency improvement**, not a pricing-display failure.

### 5. Usage telemetry
Exact OpenAI token/cost telemetry and consolidated MetaAPI request telemetry are not yet persisted. This is an observability improvement.

### 6. Weekend edited-message edge
Original weekend messages are blocked and the automatic runtime is frozen. A narrow edge remains where a pre-weekend message edited during closure could potentially be recovered after reopen unless `edited_at` is also freeze-gated.

This is a **specific edge-case hardening item**. The main weekend freeze is already fixed and production verified.

### 7. AIDY Data Hub
The owner-facing AIDY Data Hub has not yet been built. B-F current views are ready to support it. This is the next planned product build, not a production defect.

### 8. Independent AIDY trader capability
AIDY's strategic destination is independent Gold/XAUUSD trading intelligence, but own-thesis/setup generation and forward validation are future capability work. This is roadmap work, not an unresolved production bug.

## Historical regression watchlist — not currently proven active

The following are previous incident classes and should only be called active/unresolved if fresh production evidence confirms recurrence:

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

These remain useful regression checks, but **Memory must not imply they are still broken merely because they happened historically**.
