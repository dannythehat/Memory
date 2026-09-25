# Super Signals — Telegram settlement day-boundary bug + broker-fill reconciliation gap — 2026-09-25

## Owner request
Owner asked to check Telegram messages for whether stop-loss hits are correctly reported, and to audit that the system never silently misses telling members when a SL is hit. This surfaced two separate real production bugs, both fixed and deployed same session.

## Bug 1 — Settlement day-boundary bug (real messages deleted every night)

### Root cause
Commit `5de252ff` (24 Sep, pushed as a same-day hotfix for a one-time replay incident) compared every broker settlement's `occurred_at` against "today" (`date_trunc('day', timezone('Europe/Sofia', now()))`), recomputed on every run, instead of a fixed incident window. Effect, every night as soon as the Sofia calendar day rolled over:
- the recurring cleanup job (`_cleanup_accidental_historical_settlement_replay_safely`) **deleted already-sent** settlement messages whose event happened earlier that same day — forever, not just for the original incident
- **pending** settlement messages were permanently blocked from ever being sent once their event fell before "today's" boundary

Night-hours providers (TIG's Asia Trades) trade right around that boundary, so this reliably ate real stop-loss/trade-complete notifications. Confirmed against live data: two genuine SL-hit messages sent 24 Sep 16:34/16:37 UTC were deleted a few hours later once the day rolled over.

### Fix
- Production branch: `feature/day-10-shared-telegram-sources`
- Merged PR: #255 — `Fix settlement day-boundary bug eating real SL/close Telegram messages`
- Live commit: `0bff1b1c58430951cdbb472c60dc1b4270121360`
- Render deploy: `dep-daqvnvm0tbcc738fgk4g`, live 2026-09-25T04:46:43Z

Changes in `services/api/app/telegram_publisher_canonical.py`:
- Bounded the incident cleanup to the fixed `2026-09-24 14:54:00+00` – `18:00:00+00` window it was actually meant for.
- Restored `broker_position_settled` eligibility to unconditional in all 4 places the hotfix had added the day-boundary gate (settlement is always worth telling a member about, however late it arrives).
- Added a 2-hour grace period to the same-signal ordering guard, so one leg whose `performance_trade_outcomes` row never reconciles no longer blocks every later leg of that trade from ever being announced.
- Fixed the SL-wording gap the owner originally flagged: when a trade's own final closing leg is itself a broker-confirmed stop loss, the message now says "STOP LOSS HIT — TRADE COMPLETE" instead of generic "TRADE LOSS" wording that hid it.
- Updated `test_telegram_member_format.py::test_current_day_broker_settlements_recover_but_history_never_replays` (renamed to `test_broker_settlements_always_recover_and_replay_cleanup_stays_bounded`), which had pinned the exact buggy SQL as "correct" — written alongside the original hotfix.

### Verification
New file `services/api/tests/test_telegram_settlement_day_boundary.py` — 6 real-Postgres integration tests, confirmed to fail against the pre-fix code and pass after it (verified via `git stash` on the source file). Full adjacent suite (29 tests across settlement/member-format/lifecycle-freshness/day13/provider-coverage) green.

## Bug 2 — Broker-fill positions stranded when broker_position_id was never recorded

### Root cause
`BrokerFillSettlementService` (`services/api/app/broker_fill_settlement.py`) already exists to reconcile positions marked `status='error'` against immutable broker deal history, but its candidate query only matched on `broker_position_id`. Some execution paths (an ambiguous timeout, or `broker_position_mapping_invalid` raised *after* the order had already filled) mark a tranche `error` before the broker ever confirms a position id, so that id is never recorded and the row is invisible to the existing reconciliation by construction.

Found via investigating one specific orphaned trade (`broker_client_id=SS_f3abd98151e0_1`, XAUUSD, -$24.86, broker-confirmed SL, 22 Sep 15:09:58–15:46:12 UTC) that the owner asked about directly. That one trade turned out to have **no `positions` row at all** — a step worse than the other 11 found (see below) — and no audit trail whatsoever around its placement timestamp (every other order that day logged the normal `mt5.day26_*`/`mt5.day38_*` sequence; this one logged nothing). Root cause of *that specific* placement could not be determined — it may have bypassed the normal signal pipeline entirely. **Deliberately left as a documented gap, not fixed**: owner decided (25 Sep) it's not worth chasing further — 3 days old, $24.86, already closed, no ongoing impact, and there's no safe way to code-fix an event whose origin is unknown without risking a wrong guess against execution-critical state.

Widening the same investigation found **11 real positions** on the Owner account stuck this way (`broker_client_id` e.g. `SS_842d397c7347_1`, `SS_420e2a6e98e1_1`, `SS_bf20aae80f1f_1`, `SS_b99e6335a03b_1`, `SS_ba1266f08b32_1`, `SS_d52b220338a7_1`, `SS_d2a92aba1890_1`, `SS_3902626d625f_E1T1`, `SS_ed4beff3dc2c_1`, `SS_a0ff3423a6d5_1`, `SS_f7cb5dc05a7f_3`), spanning 19 Aug – 23 Sep — all real broker fills and closes in `broker_deals`, none of it ever reaching `pnl_amount`, `performance_trade_outcomes`, or a member Telegram post.

### Fix
- Merged PR: #256 — `Settle stranded fills whose broker_position_id was never recorded`
- Live commit: `eafe4aa8a6c33abbb21848f0a01511e04d0de941`
- Render deploy: `dep-dar0jq49v7es73925bh0`, live 2026-09-25T05:45:01Z

`broker_client_id` is assigned locally before every submission and is always present, so it's the fallback key back to a tranche's real broker deals when `broker_position_id` is missing. Extended `_stranded_rows`'s LATERAL join with an OR-branch resolving via `broker_client_id`, and backfilled `broker_position_id` once evidence resolves the tranche. The original `broker_position_id`-only path is unchanged (regression-tested). This is the same read-evidence → decide → apply service already running on a schedule (`unified_pending_reconciler.py`) — never contacts the broker, never invents state.

### Verification
New file `services/api/tests/test_broker_fill_settlement_client_id_join.py` (real Postgres, 3 tests) + extended `test_broker_fill_settlement.py` (stub-level, house style). All fail pre-fix, pass post-fix. Confirmed live in production immediately after deploy: all 11 known stranded positions self-healed within ~90 seconds of the reconciler's next poll, each now `status='closed'` with the correct broker-confirmed `pnl_amount` and `broker_position_id` backfilled (net across the 11: +$11.02).

## Not touched / explicitly deferred
- The Sep-22 fully-orphaned trade (`SS_f3abd98151e0_1`, no position row) — documented gap, owner confirmed not worth chasing further.
- Root cause of *why* `performance_trade_outcomes`/`broker_position_id` sometimes never gets written in the first place (the upstream cause producing both the 11 stranded positions and, differently, the fully-orphaned one) was not investigated further — Bug 2's fix is a downstream reconciliation safety net, not a fix to whatever in execution/mapping produces the ambiguous/ never-confirmed state to begin with. If this class of position keeps recurring going forward, that upstream cause is the next thing worth understanding.

## No changes to
Signal parsing, risk sizing, trade dispatch/execution, or the OpenAI API key. Both fixes are read-only with respect to the broker (no MetaAPI/gateway calls) and additive to existing tested behavior (regression-tested).
