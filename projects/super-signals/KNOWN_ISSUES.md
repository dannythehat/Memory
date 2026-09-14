# Super Signals — Confirmed Open Follow-ups / Regression Watchlist

Updated: **2026-09-14**

This file distinguishes **confirmed open follow-ups** from **historical incidents that are not currently proven active**. Do not describe historical incidents as unresolved unless production evidence re-confirms them.

## Confirmed open follow-ups

### 0. Branch topology is a live trap — highest priority

`render.yaml` pins the deploy to `feature/day-10-shared-telegram-sources`. At 2026-09-14:

- that branch is at `8019f66` and **is** production;
- `main` is at `4bb664b` and is **141 commits behind**;
- the branch literally named `production` is at `ade297e` and is **not** deployed.

Any agent or person who reads `main` or `production` as the live system will draw wrong
conclusions about what is running. Two separate risks follow: a "fix" written against `main` may
already exist in production, and a production behaviour may be attributed to code that was never
deployed.

This is a **repository governance follow-up**, not a runtime defect. Resolving it means deciding
deliberately whether to fast-forward `main` to the deployed head, repoint Render, or rename the
misleading `production` branch — none of which should be done casually while real money is being
traded from that branch.

Related and unresolved: `render.yaml` declares `autoDeployTrigger: off` while the previous
`LIVE_STATE.json` recorded `auto_deploy: true`. Confirm against the Render dashboard before
assuming a push does or does not deploy.

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
AIDY's strategic destination is independent Gold/XAUUSD trading intelligence. Own-thesis and
setup generation are **further advanced than this file previously implied** — AIDY's own repo
carries a falsifiable Master Trader contract, decision ledger, paper simulator, management
watcher and episode memory. What remains is forward validation and an explicit graduation gate.
This is roadmap work, not an unresolved production bug.

### 9. Memory drifted materially in one day
Memory recorded the deployed SHA as `278496cc` on 13 September. By 14 September the deployed
branch had advanced **71 commits**, the Alembic head had moved `0078` → `0079`, and the recorded
risk directive ("1% only") no longer matched `provider_risk_policy.py` ("1% per enabled TP/runner
leg"). Two of those are the kind of drift that changes real-money reasoning.

Treat this as evidence that a build day is not complete until Memory is updated in the same pass,
per the `AGENTS.md` completion gate — not as a reason to distrust the source repositories.

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
