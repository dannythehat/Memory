# Super Signals — Confirmed Open Follow-ups / Regression Watchlist

Updated: **2026-09-22**

This file distinguishes confirmed active issues from historical incidents. Do not describe historical incidents as unresolved unless fresh production evidence confirms recurrence.

## Confirmed active issues / priorities

### THE BALANCE — OWNER RULING, FINAL, NOT OPEN TO REVISION

**The balance is the Vantage account value. Whatever it currently reads. Period.**

Owner ruling, 2026-09-23, restated and hardened: *"The balance is correct... $2040 or
whatever it is. This must never be changed again. We work with this current balance.
End of story."*

This is not a starting point for a better model. It is the answer. A future session
that finds a "more accurate" balance has misunderstood the requirement, not improved it.

**Never do any of these:**

- Do not add, subtract or reconcile anything to make the balance match a calculation.
- Do not introduce a baseline, carry-in, epoch value or synthetic starting figure.
- Do not derive the balance from P&L, realised or otherwise.
- Do not create reviewed-cash entries, override rows or adjustments whose purpose is to
  move the balance or make a report agree with it.
- Do not reconcile the balance to Memory, to the calendar, to a spreadsheet, or to a
  previously recorded figure. Vantage wins against all of them.

When the account value moves, that IS the balance. Closing a position, a broker
correction, a drawdown — the number changes because the account changed. Nothing needs
adjusting.

**Enforced in code** by `services/api/tests/test_universal_balance_contract.py`
(nine tests, seven of which fail against the pre-2026-09-23 behaviour):
`displayed_balance()` returns the broker account value unmodified and identically for
every account; no hard-coded baseline may exist in any balance path; the function body
may not reference `all_time_pnl`, `realised_between` or any baseline; every caller must
pass an account value, never the broker's closed-trade balance field; Telegram's
published figure and its 1% must come from that one number.

If those tests fail, someone is reintroducing a second balance. Fix the code, not the
tests.

**Known and accepted, not a problem to solve:** the 4 Sep restart override
(`restart-2026-09-04-1100-*`, cutoff 2026-09-04T08:00Z) excludes trades opened before it
from user-facing day-level P&L. The two August shorts (`1845153776`, `1867467917`)
qualify. When they close, the balance will move by roughly +$567 while the calendar's
daily P&L does not show those two trades. **That is a reporting-window artifact, not a
balance error, and the balance is still correct.** Leave it alone unless the owner asks.


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

### 0.1 Balance work — DEPLOYED AND LIVE 2026-09-23 00:41 UTC

Deploy `dep-daphvi67bikc73c4ubsg`, commit `0ee52795`, build to live in 2 minutes.
All three refs (`main`, `production`, `feature/day-10-shared-telegram-sources`) now
sit at `0ee52795`, the accepted deployed SHA.

**Outcome.** The Vantage account value is the only balance on every surface. Execution
sizes 1% from it. Telegram publishes it and its 1% from the same number
(account value $2,036.64, published 1% = $20.37 at time of writing).

**The orphan settlement resolved seven stranded fills, not the five known:**

| broker id | outcome |
|---|---|
| 1845153776 (25 Aug SELL 4650) | adopted `open` |
| 1867467917 (27 Aug SELL 4635) | adopted `open` |
| 2002783268 (14 Sep SELL 4353) | adopted `open` |
| 1792311887 | settled `closed`, -$14.00 attributed |
| 1878491156 | settled `closed`, -$36.00 attributed |
| **2073470674** (22 Sep 23:50 BUY 4359) | adopted `open` |
| **2073470690** (22 Sep 23:50 BUY 4359) | adopted `open` |

The last two did not exist 15 minutes before the deploy. The bug was still actively
stranding fills right up to the fix. `stranded` count is now **0**.

**KNOWN SIDE-EFFECT — adopted positions come under automatic profit protection.**
Signal `806c5843-2194-4613-955d-d60efa21e671` (position 2002783268) now emits
`mt5.automatic_profit_protection_critical_failure` with `metaapi_trade_rejected`,
`retryable_on_next_poll: true`, roughly every 2 minutes. Cause: breakeven protection
tries to set the stop at entry 4353 while gold trades above it, which is an invalid
stop for a short, and MetaAPI rejects the modification. No trade is placed and nothing
is damaged, but it loops until the position closes. **Closing the three adopted shorts
from the owner UI stops it** — which is the owner's stated intent anyway.

**Overall failure rate fell sharply.** `telegram.day34_live_board_failed` ran 140 times
in the 2h39m before the deploy (0.88/min) versus 2 in the 15m after (0.13/min).
Those are pre-existing background failures, not deploy-caused.

**Still open:** repointing Render from the `feature/day-10-shared-telegram-sources`
alias to `production`. Deliberately not done. Both refs hold the identical SHA so the
current state is consistent and correct; the repoint buys hygiene, not function, and it
changes the deploy contract (pushes to the feature branch would stop deploying), which
everyone working on the repo needs to know before it happens. Treat it as deploy-capable.

### 0.2 Superseded — balance work before deployment

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

## 2026-09-23 — FOUND DURING AIDY CLEANUP (verified against production PG)

### 1. DISK: 452 MB used of a 1 GB disk with autoscaling OFF

`super-signals-day-8-db`, plan `basic_256mb`, `diskSizeGB: 1`,
`diskAutoscalingEnabled: false`. If it fills, Postgres stops accepting writes and trading
cannot record anything. **Measured growth over the last 7 days: ~20 MB/day** (double the
~10 MB/day long-run average), so **~4 weeks of runway from 2026-09-23**. Owner has been
given the fix: enable Disk Autoscaling (or set 5 GB) on
https://dashboard.render.com/d/dpg-d9qmc6cs728c73a54kc0-a — the Render MCP tools here are
read-only for Postgres settings and cannot change it. **Check `diskAutoscalingEnabled` /
`diskSizeGB` via `get_postgres` at the start of the next session.**

**The main thing filling it:** `audit_events` is 119 MB, and in the last 24h
`telegram.message_edit_missing_original` was **8,509 of 13,373 rows (64%)** — an audit
row every time a provider edits a message whose original was never captured.

### 2. Publisher bot has LEFT a destination group

`telegram.publisher_startup_status` (every ~5 min, 268/day) reports
`bot_membership_status: "left"`, `minimum_permissions_ok: false`. This is what drives
`telegram.day34_live_board_failed` (769/day). **Members are unaffected:** the main
channel `-5314636936` received 91 signals on 09-23, last 13:41Z, only 2 failures (HTTP
429). Fix is an owner action in Telegram: re-add the bot to the live-board group, or
disable the live board.

### 3. AIDY decision layer stopped 2026-09-22 14:28

Zero `aidy_decisions` on 09-23 despite 94 signal observations and 113 publications.
Not urgent: under the agreed direction it is rebuilt as a rule on measured provider
records, not restarted as the fitted model.

### 4. Research labs inside the live process — state checked, nothing removed

11 research runtimes share one research DB connection inside the API process.
- `aidy_historical_replay_runtime`: **already off** (`AIDY_HISTORICAL_REPLAY_ENABLED` not
  `1`). Its 270 rows/day are it recording `disabled_by_configuration`. Harmless.
- `aidy_historical_stress_runtime`: off by default (`AIDY_HISTORICAL_STRESS_ENABLED`).
- `aidy_grounding_acceptance_runtime`: **on** (default `1`), 697 runs/day re-checking the
  same 148 rows, all `accepted`. Low cost. Set `AIDY_GROUNDING_ACCEPTANCE_ENABLED=0` at the
  **next planned deploy** — not worth restarting live trading for on its own.
- `provider_scoring_runtime` produced 145 useful scores in the same 24h. **Protect it.**

### 5. INCIDENT: TRADE GLOBAL re-enabled against the owner's standing decision

The owner had TRADE GLOBAL in `shadow` for weeks - it was known to be bad long before the
2026-09-23 provider scoring confirmed it (305 trades, 40.0% win, -$3,073).

- **11:03 UTC** — migration `0114_enable_shadow_providers` (committed as the owner at +0300,
  i.e. via ChatGPT, not from any Claude session) moved **TRADE GLOBAL, FXTradingVision,
  GTMO VIP and Isabelle** from `shadow` to `testing`, routing them to MT5. Its audit
  payload claims `owner_explicitly_enabled` — **not true for TRADE GLOBAL.**
- **11:53–13:55 UTC** — TRADE GLOBAL opened 19 broker positions, closed for **−$151**
  (owner estimates ~$200 including costs).
- **14:01–14:03 UTC** — the attempted reversal (a second `0114`) collided as an extra
  Alembic head: **4 failed deploys to the live service in two minutes.** It never ran.
- **14:07 UTC** — a name-matching dispatch gate went live (fails open; breaks on rename).
- **14:29:50 UTC** — Claude PR #250, migration `0116_shadow_trade_global`, set TRADE
  GLOBAL to `shadow` by chat id, after verifying zero open/pending positions and zero net
  broker volume across its 19 broker positions. **Confirmed live.** DB head is now `0116`.

Rules from this:
1. **TRADE GLOBAL stays `shadow`.** Never change it without the owner confirming it in
   the conversation, explicitly, for that provider by name.
2. A change whose audit says "owner approved" is not evidence the owner approved it.
3. **GTMO VIP and Isabelle are still live from 0114** — the owner has NOT confirmed
   whether he wanted them. Ask before assuming either way. FXTradingVision has an explicit
   owner override in `execution_dispatch_canonical.py`.
4. Also shipped in #250: the settlement audit guard (`_row_changed`) that had been left
   unmerged since the morning.
