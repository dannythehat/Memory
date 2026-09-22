# Super Signals — Confirmed Open Follow-ups / Regression Watchlist

Updated: **2026-09-22**

This file distinguishes confirmed active issues from historical incidents. Do not describe historical incidents as unresolved unless fresh production evidence confirms recurrence.

## Confirmed active issues / priorities

### 0. Balance reporting had six different answers; orphaned broker fills — FIX ON BRANCH, NOT DEPLOYED

Independent reconciliation on 2026-09-22 against the production database.

**The ledger.** $1,000.00 start (6 Aug) + $47.71 realised trading across 1,448 closed
trades + $317.16 of four manual `DEAL_TYPE_BALANCE` corrections = **$1,364.87**, which
ties to the broker end-of-day balance to the cent on 29 of 30 trading days. The four
corrections (18, 19, 26 Aug) were deliberate owner fixes and belong in the record.
Trading alone: August +$52.17, September -$4.46. 14 Sep lost -$308.32 in one day.

**Six conflicting figures existed**, each correct per its own code:
$1,047.71 (trading only) · $1,364.87 (broker balance) · $1,437.67 (with overrides and
reviewed-provider cash) · $1,508.57 (`displayed_balance()`, used for execution sizing)
· ~$1,828.57 (dashboard calendar) · $2,050.64 (Telegram / Vantage card).

Causes, in order of size:
1. `paper_run_epoch.py:24` hard-codes `PAPER_RUN_BASELINE_BALANCE = 1517.23` dated
   31 Aug — a value the account never held, which also discards all of August.
2. +$320.00 of `reviewed_provider_result_*` outcomes with `broker_deal_count = 0`
   (39 rows 11 Sep, 3 rows 10 Sep) counted as profit with no broker trade behind them.
   **Unresolved — owner has not yet said whether these are corrections or estimates.**
3. Telegram and the dashboard publish equity, which carried $685.77 of unbanked
   floating profit. Fixed on branch in `98ea5c7c`: the published 1% is derived from the
   account value (the company paper balance), and a stale snapshot suppresses it.

**Orphaned broker fills (root cause of the floating).**
`pending_reconciliation_canonical._persist_filled_not_visible` records a confirmed
broker fill as `status='error'` with `close_reason='broker_filled_position_not_visible'`
and audits `mt5.pending_broker_fill_requires_settlement`. That settlement was never
implemented, and `owner_manual_close.py:172,196` select `p.status='open'`, so the
position became unreachable by every code path. Three positions stayed live at Vantage
for up to four weeks (1845153776, 1867467917, 2002783268); two more (1792311887,
1878491156) closed at the broker while still `error` locally, losing -$14.00 and
-$36.00 from position-level reporting.

Fixed on branch in `0b02278d`: `app/broker_fill_settlement.py` settles stranded fills
from ingested broker deals (never contacts the broker), plus a broker-deal invariant
that catches an orphan from any future code path, run each reconciler cycle and logged
at ERROR while any survives. On first run it adopts the three live positions to `open`
— which makes them closeable from the owner UI with no broker call.

**Still open:** the $320 question above; retiring the $1,517.23 / 31 Aug origin so every
surface reads one number; and the 4 Sep restart override, which will exclude the three
orphans' realised P&L from reporting when they close, creating a fresh balance-vs-report
gap unless handled at the same time.


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
