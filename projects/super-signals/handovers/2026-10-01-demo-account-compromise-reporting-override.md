# Super Signals Handover — 2026-10-01

## Finished state

Source repo: `dannythehat/super-signals`
Branch: `feature/day-10-shared-telegram-sources` (production; Render service `super-signals-day-8`, autoDeploy off, deployed by API trigger)
Verified SHA: `9d856f12c1fc7fcd163b1503437f013625019979` (PR #257, squash-merged), Render deploy `dep-dav16rfpn0mc739kmq3g` LIVE at `2026-10-01T08:05:03Z`
Status: PRODUCTION VERIFIED for the override row and public figures; app Today strip on-screen display WAITING owner confirmation

## What changed

- Migration `0125_incident_20261001_override` inserted one `performance_reporting_overrides` row (incident key `incident-2026-10-01-demo-compromise`) for the owner demo (same MetaApi demo account as the 26 Aug override), Europe/Sofia reporting day 2026-10-01, reviewed cash **+384.84**, cutoff **2026-10-01T07:45:00Z**, plus one `performance.reporting_override_created` audit event. Alembic head is now `0125_incident_20261001_override` (production DB confirmed).
- Reporting layer only. No broker deals, positions, snapshots, balances, risk sizing, auth, Telegram, parsing or execution changed.

## Why

- Between 07:11 and 07:23 UTC on 2026-10-01 the owner's Vantage DEMO account (login ending 1913, USD) was traded from outside Super Signals: balance 2,309.66 -> 383.70 -> 312.50 -> 254.38 -> 21.74 (snapshots). The owner reports the account was hacked and had Vantage restore the demo to 2,300.00 (first seen by Super Signals at 07:38:37Z).
- Owner asked for the app's "today" to read about +$380. The public website already followed account equity (21:00 Sofia close 30 Sep 1,915.16 -> 2,300.00 = +384.84). The app Today strip counts only Super Signals' own trades and restarts at any same-day balance jump of >=100 and >=20%, so it would not have shown that. The owner approved a reviewed override of +384.84 and chose to KEEP that figure after being told Super Signals' own recorded exits before the cutoff net -97.51 (so the reviewed amount includes about +482 of account movement NOT made by Super Signals trades, including a +394.50 balance rise earlier on 1 Oct whose source is not in Super Signals' positions). The override reason text states this.
- Evidence the loss was external: Super Signals' own positions that day were 0.01 lot at 1% risk (about -10 each, many `external_close`); the large positions are not in the `positions` table; trading controls (risk 1.0, active) unchanged since 2026-09-14/08-31; audit log shows no setting/profile changes in the previous 30h.

## Evidence

- PR: https://github.com/dannythehat/super-signals/pull/257 (head `claude/incident-20261001-override`, owner approved pushing to a new branch).
- Tests: `test_incident_20261001_override.py` + `test_trade_global_shadow_migration.py` (single-head test now `0125_incident_20261001_override`) + existing override/accounting/today-summary tests pass locally (Postgres-dependent migration tests skip without DATABASE_URL).
- Production proof (read-only SQL after deploy): `alembic_version=0125_incident_20261001_override`; override row present (+384.84, cutoff 07:45Z, Europe/Sofia); 1 audit event; 4 override rows total; latest owner snapshot 2300.00/2300.00 at 08:05:40Z; 0 exit deals after the cutoff, so by the code path the Today strip realised P/L is 384.84 + 0. `https://smartsignals.site/data/public-performance.json` showed current balance 2300 and 2026-10-01 cash_pnl 384.84 (it briefly served the stale static fallback, balance 2075.81, while the API restarted, then returned to live within a minute).

## Safety state

- Live-money authority unchanged. No broker/execution/sizing change. The balance is the broker's, unmodified (`trading_accounting` single-door rule).
- Live account (login ending 0622, EUR) balance has been EUR 1.35 since at least 2026-09-20 (EUR 56.29 on 2026-09-14): NOT part of the 1 Oct event.
- Demo ending 1813 is in `error`/DISCONNECTED (last confirmed 1,170.01 on 2026-09-14).

## Unresolved

- Who traded the demo 07:11-07:23Z is unknown; owner to check Vantage client-area / MT5 login and trade history for unfamiliar IP/device, change Vantage portal password and enable 2FA, and (if MT5 passwords are rotated) re-save them in Super Signals MT5 settings so MetaApi reconnects. Owner reported securing the account.
- The app Today strip was not seen on screen (no login access); confirm it reads about +$384.84.
- The override makes user-facing realised-P/L windows (today/week/all-time) include +384.84 instead of Super Signals' own -97.51 for 1 Oct. Public statistics follow equity regardless.

## Exact next step

- Owner to confirm the app shows about +$380 for Today and finish the account-security checks above. If any later page still shows -$1,800, tell Claude which screen so the right surface can be fixed.

## Addendum: Telegram group replaced (1-6 Oct 2026)

- The owner deleted the Super Signals Telegram group by mistake and created a new supergroup. New chat id `-1004402233886`; Render env `SUPER_SIGNALS_TELEGRAM_PUBLISH_CHAT_ID` updated (merge mode) and redeployed. Bot token untouched.
- Permission rule (`telegram_publisher._minimum_permissions_ok`): the bot must be a plain member, or an admin with none of change_info, delete_messages, invite_users, restrict_members, promote_members, manage_video_chats, manage_chat, manage_topics, edit_messages, manage_direct_messages. Admin with Post/Edit/Delete on is refused (403 on publish, `minimum_permissions_ok: false`). After the owner dismissed the bot's admin rights, the 08:54Z startup check reported member / `minimum_permissions_ok: true`. The check runs at startup, so a restart is needed after any permission change.
- Bug found and fixed: `telegram_live_board_state` (single row id=1) kept the old group's message id (3586, chat -5314636936), so every board sync failed with 400 "message to edit not found". PR #258 (commit `df4838d`, deployed `dep-dav1v0npn0mc739nte6g`, live 08:56Z) reposts a fresh board when the stored `destination_chat_id` differs from the configured chat. Board message 4 was posted in the new group; status is `ready` as of 2026-10-06.
- Known gap (owner chose to leave it): the board is not pinned. A plain member cannot pin ("not enough rights to manage pinned messages"). Pinning would need the bot as admin with only Pin Messages on (not in the broad-permission list) plus a follow-up fix so a reposted board clears the stale `pinned_at` (ready on branch `claude/telegram-board-repin-after-repost`, not merged, not deployed). `pinned_at` still shows 2026-08-12.
- First signal post in the new group after the permission fix was not yet verified when this was written.
- Owner is considering a $100 real (cent) account (2026-10-06); nothing was changed. No live-money authority given.
