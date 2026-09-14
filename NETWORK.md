# The Network — how every repository fits together

Mapped and source-verified: **2026-09-14**

This file is the orientation map for the whole estate. It answers "what is each repository,
what runs where, and how do they talk to each other" in one place so a new session does not
have to rediscover it.

It is **source-verified only**. Every repository below was read at the stated commit. Render,
Cloudflare, PostgreSQL and D1 runtime state were **not** inspected in the session that wrote
this file. Follow `AGENTS.md` precedence: runtime evidence overrides this map.

---

## 1. The five repositories

| Repository | Role | State |
|---|---|---|
| `dannythehat/super-signals` | The business. Member app + API + Telegram ingestion + MT5 execution + Provider Lab research. | **Active production** |
| `dannythehat/super-signals-website` | Public marketing/onboarding site `smartsignals.site` (Cloudflare Worker). | **Active production** |
| `dannythehat/Aidy-Gold-Signals` | AIDY — the independent Gold/XAUUSD intelligence system (Cloudflare Worker). | **Active, private forward paper** |
| `dannythehat/Memory` | This repository. Continuity layer for AI sessions. | **Active, not production** |
| `dannythehat/Telegram-Signals-Auto-Trader` | Earlier friends-and-family auto-trader prototype. | **DORMANT — superseded** (see §7) |

## 2. Brand vs repository names

The repositories are named "Super Signals". The **customer-facing brand is "Smart Signals"**
on the website, in the app UI and in member email. Both names refer to the same product.
Internal code, tables and environment variables keep the `SUPER_SIGNALS_*` prefix; newer
member-facing code uses `SMART_SIGNALS_*`. Do not "fix" this inconsistency casually — it is
split across live environment variables.

## 3. The business in one paragraph

Super Signals pays to join Telegram gold-signal groups as an ordinary member, records what each
group actually does over time, and only promotes the groups that earn it. Approved providers'
messages are captured, interpreted, turned into one canonical signal, published to a private
Smart Signals Telegram channel, shown in the mobile app, and mirrored onto each paying member's
own Vantage MT5 account through MetaAPI. Members pay €99/month or €999/year in USDC on Solana.
Everything that is *not* approved is run as a **shadow** provider: a paper benchmark that can
never touch a broker. AIDY is the separate intelligence system being built to eventually stop
needing providers at all.

## 4. Runtime topology

```text
                    Telegram provider groups (real + shadow)
                                  |
                    Telethon reader sessions (per admin)
                                  v
  +------------------------------------------------------------------+
  |  Render web service  super-signals-day-8  (Frankfurt, Docker)     |
  |  https://super-signals-day-8.onrender.com                         |
  |  FastAPI + React PWA served from the same origin                  |
  |                                                                   |
  |   listener -> AI/deterministic pipeline -> canonical signal        |
  |        |                                        |                 |
  |        |                         +--------------+--------------+  |
  |        |                         v                             v  |
  |        |            source status testing/live        source shadow|
  |        |                         |                             |  |
  |        |                    MetaAPI -> Vantage MT5      shadow_trades
  |        |                    (owner + members)           (paper only)|
  |        |                                                           |
  |        +--> Telegram publisher bot -> private Smart Signals channel |
  |                                                                   |
  |  AidyShadowRuntime (5 min loop, sleeps during weekly freeze)      |
  +-------------------------------|----------------------------------+
                                  | HTTPS + bearer token
                                  v
  +------------------------------------------------------------------+
  |  Cloudflare Worker  aidy-signals-test                             |
  |  https://aidy-signals-test.dannythehat2.workers.dev               |
  |  D1 aidy-ops-test  |  R2 aidy-memory-test  |  BigQuery aidy-signals|
  |  direct Cron capture -> episode memory -> data health             |
  +------------------------------------------------------------------+

  +------------------------------------------------------------------+
  |  Cloudflare Worker  super-signals-website  -> smartsignals.site   |
  |  static site + /account-api/* reverse proxy to the Render service |
  +------------------------------------------------------------------+
```

### PostgreSQL

Render PostgreSQL `super-signals-day-8-db` (free plan, Frankfurt) is the single authoritative
store for the business: users, sources, messages, signals, positions, shadow trades, performance
ledger and all Provider Intelligence evidence. **67 tables**, Alembic head `0079_fix_member_entitlements`
at the source head below. AIDY has no access to it.

### Cloudflare D1

`aidy-ops-test` is AIDY's own operational store (27 tables) — market snapshots, candles, archive
outbox, forward cohorts/evaluations/outcomes, episode memory, learning cards, data-health events.
Super Signals has no access to it.

**The two databases never touch.** The only channel between the systems is the authenticated
HTTP boundary in §5.

## 5. The AIDY ↔ Super Signals boundary

This is the single most important architectural rule in the estate.

Super Signals calls AIDY over HTTPS with a bearer token. Configuration lives in the Render
service as `AIDY_PROVIDER_MARKET_URL` and `AIDY_PROVIDER_MARKET_TOKEN`.

| AIDY route | Consumer | Purpose |
|---|---|---|
| `GET /market/ohlc` | `AidyMarketClient` | PIT-safe M1 XAU/USD bars used as canonical market truth for shadow scoring |
| `GET /calibration/market/ohlc` | `provider_day11_calibration_replay` | Bounded retrospective calibration corpus |
| `GET /provider/context` | `AidyContextClient` | Point-in-time session/regime/context for one provider signal timestamp |
| `GET /provider/data-health` | *(built, not yet consumed)* | **Hub Phase A** — AIDY capture/archive/freshness telemetry |
| `GET /provider/decision-memory` | *(built, not yet consumed)* | **Hub Phase B** — AIDY episodes, outcomes and learning cards |
| `GET /health` | ops | Describes the brain, not just the Worker process |

Direction of trust is **one-way**:

- AIDY may give Super Signals market/context evidence.
- Super Signals must **never** feed broker state, follower state, member accounts or provider
  P&L back into AIDY as market truth. AIDY's own contracts enforce this with explicit
  `broker_state_used=false`, `follower_state_used=false`, `super_signals_used=false` flags on
  every result, and with database CHECK constraints on `aidy_forward_restart_runs`.
- Neither system's research status grants the other broker authority.

## 6. How provider shadowing works

This is the mechanism the owner asked about specifically.

1. A Telegram group is joined and catalogued as a `source` row. Status is one of
   `testing`, `shadow`, `paused`, `live`, `revoked`.
2. Every message is captured. A deterministic-first pipeline classifies it; OpenAI
   `gpt-5-mini-2025-08-07` is used for interpretation where deterministic rules cannot decide.
   AI may identify *which* trade a message refers to; it may **never** donate the action, price,
   TP index or side — those come only from mechanically explicit current-message evidence.
3. `CanonicalExecutionDispatcher` routes the durable decision:
   - status `shadow` → branches immediately into `_dispatch_shadow` and **returns before any
     broker code path exists**. This is a structural guarantee, not a policy check.
   - status `testing`/`live` → real MetaAPI execution on the owner reference account and on
     eligible members' accounts.
4. Shadow signals are enrolled into `shadow_trades` and measured on a deliberately fair
   benchmark defined in `provider_fairness.py`:
   - every provider gets the same notional **$1,000** account;
   - every TP/runner leg carries the same fixed **$10** cash risk;
   - benchmark model id `fixed_1000_10_per_tp_fair_v2`;
   - scalper/intraday/swing providers **must** be scored on AIDY M1 truth (`quote_mode='aidy_m1'`)
     or the trade is recorded but excluded from scoring;
   - minimum evidence before a provider may be judged, by style:
     scalper 100 closed trades / 20 trading days / 4 weeks;
     intraday 60 / 30 / 6; swing-or-sparse 30 / 45 / 8; mixed & unknown 60 / 30 / 6.
5. Shadow outcomes feed provider fingerprints, conditional statistics, governance and the B–F
   intelligence snapshots. **None of that can promote a provider or change risk.** Promotion to
   `testing`/`live` remains an explicit human decision.

### Provider populations — never mix these

- **~40 shadow discovery providers** — research only, broker-isolated.
- **5 real/testing providers** — the ones with live execution policy in `provider_risk_policy.py`.

Answering a question about one population using the other is a standing error. Resolve which
population is meant before analysing anything.

## 7. Telegram-Signals-Auto-Trader — dormant

Two branches, last touched **2026-08-04**. `main` is a design README; `develop` carries a
Phase 1 foundation (strict signal models, parser, order-type logic, SQLite store, safety gate,
Telethon shadow listener, order planner) and then stops.

It is the **earlier, different product**: each *user* connects their own Telegram account and
their own groups with a fixed lot size. Super Signals productised the same idea in the opposite
direction — the *owner* curates approved providers and members only connect MT5. Super Signals
started at the same time and is now ~42 build days plus a provider-intelligence programme ahead.

Treat this repository as an archived specification. Do not build on it, and do not treat its
README as current architecture.

## 8. Verified source heads (2026-09-14)

| Repository | Branch | SHA | Note |
|---|---|---|---|
| super-signals | `feature/day-10-shared-telegram-sources` | `8019f66` | **this is production** |
| super-signals | `main` | `4bb664b` | **141 commits behind production** |
| super-signals | `production` | `ade297e` | misleading name, not deployed |
| super-signals-website | `main` | `088096a` | |
| Aidy-Gold-Signals | `main` | `cb0f4bc` | |
| Telegram-Signals-Auto-Trader | `develop` | `84efe74` | dormant since 2026-08-04 |

**The Render deploy branch is not `main`.** `render.yaml` pins
`branch: feature/day-10-shared-telegram-sources`. Anyone who reads `main` and believes it is
production will be reading code that is 141 commits stale. See the Super Signals known issues.

## 9. What still needs runtime verification

Nothing below was checked when this file was written. These are the first things to confirm
once database/Render/Cloudflare access is available:

1. Render: the live deploy id, that it is built from `8019f66`, and whether auto-deploy is on
   (`render.yaml` says `autoDeployTrigger: off`; Memory's older `LIVE_STATE.json` said
   `auto_deploy: true` — these disagree).
2. PostgreSQL: actual Alembic head, the true count of `shadow`/`testing`/`live`/`paused`/`revoked`
   sources, and whether `provider_intelligence_snapshots` / `provider_book_conflict_snapshots`
   have populated since the market reopened.
3. Cloudflare Worker `aidy-signals-test`: the real values of `AIDY_CAPTURE_ENABLED`,
   `AIDY_MARKET_DATA_SOURCE` and especially `AIDY_FORMAL_FORWARD_ENABLED` — see the AIDY
   current state, this is the biggest open question in the estate.
4. D1 `aidy-ops-test`: the active forward cohort, the Phase B restart campaign's
   `acceptance_state`, and how many episode-independent model-resolved decisions exist against
   the 300 gate.
