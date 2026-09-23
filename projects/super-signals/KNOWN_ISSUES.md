# Super Signals — Confirmed Open Follow-ups / Regression Watchlist

Updated: **2026-09-22**

This file distinguishes confirmed active issues from historical incidents. Do not describe historical incidents as unresolved unless fresh production evidence confirms recurrence.

## Confirmed active issues / priorities

### 0.0 BRANCH TOPOLOGY — REPAIRED 2026-09-23. READ BEFORE TOUCHING ANY BRANCH

**Production deploys from `feature/day-10-shared-telegram-sources`** (Render web
service `super-signals-day-8`, `srv-d9qmcgks728c73a555m0`, **autoDeploy = yes**).
Pushing to that branch **IS a deploy**. There is no gap between merging and going live.

Until 2026-09-23 the three refs had drifted badly:

| ref | was | now |
|---|---|---|
| `main` | `1a5488d2` | **`1b35bd16`** |
| `production` | `ade297e7` (9 Sep, 393 behind) | **`1b35bd16`** |
| `feature/day-10-shared-telegram-sources` | `1b35bd16` | `1b35bd16` (untouched) |

**Root cause.** A 9 Sep "stabilisation" pinned `main` and `production` at `ade297e7`
and neither ref ever moved again while all real work continued on the feature branch.
PR #241 ("Hard-isolate AIDY research from live trading") was then authored on 22 Sep
but **built from the 10 Sep base `4bb664bd`**. Against that stale base it deleted
`get_research_engine()`/`get_research_session_factory()` — the `a61e665d` anti-starvation
lane — removed all seven AIDY research runtimes from app startup, and deleted README and
all of `docs/`. **Those removals were stale-base fallout, not a decision.** They never
reached production, because nothing deploys from `main`.

This had happened before: `backup/main-pre-production-consolidation-20260830`,
`backup/main-pre-stabilisation-20260909-bfa4d8b`. Third occurrence.

**Repair executed 2026-09-23** (ChatGPT concurred; owner approved):
backups `backup/{main,production,render-live}-20260923` pushed first, then
`production` fast-forwarded and `main` force-corrected (`--force-with-lease`) to
`1b35bd16`. The Render branch was not touched, so no deploy was triggered. PR #241
remains fully recoverable at `backup/main-20260923`.

**Do NOT replay #241's documentation deletion.** `docs/PRODUCTION_START_HERE.md` is the
canonical topology definition and is now doing the job. Any docs reduction must be a
separate, targeted commit that preserves the production authority/runbook material.

**Remaining steps, in order:** deploy the balance work (below) to the feature branch →
verify health and trading → fast-forward `main`/`production` to the accepted SHA →
only then repoint Render from the feature alias to `production`. Treat that final
repoint as deploy-capable even though the SHA is identical: the web process hosts the
Telegram and background runtimes, so Render's zero-downtime replacement briefly runs two
instances, and idempotency matters more than HTTP downtime.

**Policy from here:** new work targets the live branch until the Render repoint lands;
after it, `main` for PRs, `production` as the promotion ref, Render deploys `production`.

### 0.1 Balance work — VERIFIED ON THE LIVE BRANCH, NOT YET DEPLOYED

Merging commits `98ea5c7c`, `0b02278d`, `8567f3bc`, `63bc1c40` onto
`feature/day-10-shared-telegram-sources` is **clean, zero conflicts**, full
`services/api` suite exits 0. The `a61e665d` research lane survives intact
(15000 ms / 30 s), not #241's 5000 ms / 1 s.

Deploying it changes execution sizing from the broker balance field to the broker
account value: owner demo ~$1,952 → ~$2,054 (+5.2%), and on live member account
35720622 the delta equals floating P&L at sizing time. **Awaiting explicit owner go.**


### 0. THE BALANCE — SETTLED BY OWNER RULING. FIX ON BRANCH, NOT DEPLOYED

**The Vantage account value is the balance. Universally, permanently, for every
surface. Nothing may ever disagree with it.** This is an owner ruling given on
2026-09-22 and it is not open for re-derivation by any future session.

The number is the account value shown on the Vantage account card — balance plus
floating — which read $2,050.64 on 2026-09-22. It is not the broker's
closed-trade `balance` field and it is not any Super Signals derivation.

**Do not repeat these errors.** The four `DEAL_TYPE_BALANCE` adjustments on the
Owner demo account (18 Aug +$509.78, 19 Aug -$439.34, 26 Aug +$308.72 and
-$62.00, net +$317.16) are **real trade results the owner recovered by hand
after MetaAPI failed to place the trades**. They are trading, not top-ups, not
inflation of the record. Any characterisation of them as anything else is wrong.

Six mutually inconsistent balances previously existed, each correct per its own
code: $1,047.71, $1,364.87, $1,437.67, $1,508.57 (what execution sized from),
~$1,828.57 and $2,050.64. Root cause was `displayed_balance()` returning
`OWNER_DEMO_BASELINE_BALANCE + all_time_pnl`, anchored to a hard-coded 1517.23
dated 31 Aug — a value the account never held, which also discarded August.

Fixed on branch `claude/trading-bot-prompt-review-hrxbkw`:

- `8567f3bc` — `displayed_balance()` returns the broker account value unmodified
  for every account; `OWNER_DEMO_BASELINE_BALANCE` deleted; the calendar
  reconstructs backwards from the account value through all balance-changing
  deals (which keeps the four corrections inside the ledger); every caller
  passes the account value, including execution sizing. Nine contract tests in
  `test_universal_balance_contract.py` pin the invariant, seven of which fail
  against the previous code.
- `98ea5c7c` — Telegram publishes the account value and derives its 1% from it.
- `0b02278d` — orphaned broker fills settled (see below).

**Sizing effect when deployed:** execution risks 1% of ~$2,053 instead of 1% of
~$1,508, so position sizes rise about 36%. The 1% itself is unchanged and stays
owner-controlled. 1% is per TP leg by design — owner confirmed, do not "fix" it.

**Orphaned broker fills.** `_persist_filled_not_visible` recorded confirmed
broker fills as `status='error'` and audited
`mt5.pending_broker_fill_requires_settlement`; that settlement was never
implemented, and `owner_manual_close.py` selects `status='open'`, so three
positions stayed live at Vantage for up to four weeks (1845153776, 1867467917,
2002783268) and two more (1792311887, 1878491156) closed at the broker while
still `error` locally, losing -$14.00 and -$36.00 from position reporting.
`app/broker_fill_settlement.py` settles them from ingested broker deals without
contacting the broker, and adds a broker-deal invariant that catches an orphan
from any future code path, logged at ERROR every cycle while one survives.

**Still open:** the 4 Sep restart override excludes the three orphans' realised
P&L from reporting when they close, which would open a fresh balance-vs-report
gap; handle it in the same deploy.

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
