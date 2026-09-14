# Super Signals — Current State

Last source-verified: **2026-09-14**
Last runtime-verified: **not in this session** — Render, PostgreSQL and MetaAPI were not inspected.

Authoritative repo: `dannythehat/super-signals`
**Deployed branch: `feature/day-10-shared-telegram-sources`**
Verified source head: `8019f66` — *Hotfix Render web API base to same-origin root* (2026-09-14)
Render service: `super-signals-day-8` (`srv-d9qmcgks728c73a555m0`), Frankfurt, Docker, **Starter plan**
Render database: `super-signals-day-8-db` (`dpg-d9qmc6cs728c73a54kc0-a`), PostgreSQL 18, `basic_256mb`
Live deploy: `dep-dajrrs5g1s2s73bv0pvg` at `8019f66b36c90b6fe06b41e9acb6ff2ad845dc3a`
**Auto-deploy: ON** from the deployed branch
Alembic head in source: `0079_fix_member_entitlements`
Customer-facing brand: **Smart Signals** (`smartsignals.site`)

## Branch reality — read before touching anything

| Branch | Head | Meaning |
|---|---|---|
| `feature/day-10-shared-telegram-sources` | `8019f66` | **This is production.** `render.yaml` pins it. |
| `main` | `4bb664b` | **141 commits behind production.** |
| `production` | `ade297e` | Misleadingly named. Not deployed. |

Since Memory was last updated at `278496cc` on 13 September, **71 further commits** have landed
on the deployed branch, including a merged stability release (`a2ee912` "Keep trading app alive"):
dashboard polling paused off-screen, gold quote and Today summary preserved while Home is hidden,
no forced frontend reloads during live sessions, owner account portfolio overview, owner manual
close on live and demo accounts, retry-hardened manual close, MT5 reconciliation moved off the web
event loop, and a rebuilt member MT5 onboarding (Connection V2) that no longer blocks on MetaAPI
inventory.

Anyone reading `main` and believing it is production will be reading stale code.

### Auto-deploy is ON — the deploy branch is live-fire

A push to `feature/day-10-shared-telegram-sources` deploys to the real-money production service
with no manual gate. Two consequences follow:

1. Never push to that branch without an explicit go-ahead, and never close to Monday 01:01
   Europe/Sofia. Work on a separate branch and merge deliberately.
2. Repointing Render at `main`, or merging `main` into the deploy branch carelessly, would roll
   production back 141 commits **instantly**.

Note that the committed `render.yaml` declares `autoDeployTrigger: off`. The live dashboard
setting is ON and governs behaviour; the repository file is misleading and should be corrected.

## Product north star

Super Signals is not building AIDY merely to classify Telegram providers. Provider signals are
evidence and training material. The strategic objective is for AIDY to become an independent
Gold/XAUUSD trading intelligence system that can understand Gold market moments, form its own
thesis, identify setups, judge or disagree with providers, and eventually propose and manage its
own trades.

That objective grants **no** new broker authority today.

## The business

Members pay **€99/month or €999/year in USDC on Solana**, are approved by the owner, connect
their own Vantage MT5 account, and receive approved provider trades mirrored onto that account
via MetaAPI. Onboarding funnel: account → Vantage → membership payment → owner approval → MT5
connection. Roles are `owner`, `trading_admin` and `user` (shown as "Member").

Public performance is served from the Owner reference ledger through `/dashboard/public/*`.
Recorded baseline: reconstructed from $1,000 on 2026-08-06, verified live tracking from
**$1,517.23 on 2026-08-31**, with per-day P/L published only after reconciliation. A $100→$1,000
challenge on a dedicated funded subaccount is scheduled from 2026-09-10.

## Live execution contract — corrected

Memory previously recorded the risk directive as "1% only". **That phrasing was wrong and is
corrected here** from `provider_risk_policy.py` (`POLICY_GENERATION =
"owner-authority-2026-09-09-v2-one-percent-per-tp"`):

> Owner authority from 9 September 2026: **every enabled TP/runner broker leg carries exactly 1%
> planned risk.** Entry sections distribute those target legs; they never multiply the risk
> budget. Four TP/runner legs therefore mean **4% planned signal risk**, whether the provider
> supplied one entry or several entry sections.

Automatic profit protection, from `broker_settlement_canonical.py`:

- **TP2 hit** → cancel every unused entry order for the setup, and move every open TP3+ leg to
  **its own entry** (true per-leg breakeven).
- **TP3 hit** → move every remaining TP4+/runner stop to the signal's **TP2 price**.
- Existing protection is never loosened. Moving SL to entry does **not** mean closing the trade.

### Approved provider directions

`provider_risk_policy.py` is the single production source of truth. Historical audit rankings and
old migration comments must never alter live eligibility or risk.

| Provider | Allowed directions | Note |
|---|---|---|
| FXTradingVision | BUY and SELL | capped at 3 targets |
| GTMO | BUY only | |
| TIG's Asia Trades | BUY and SELL | |
| SureShot | SELL only | |
| United Kings | SELL only | |

A disabled direction returns a zero risk profile and fails closed before broker mutation.

## How signals flow

1. Telethon reader sessions (private per administrator) capture messages from selected sources.
2. A deterministic-first canonical pipeline classifies and interprets. OpenAI
   `gpt-5-mini-2025-08-07` is used through the Responses API only where deterministic rules
   cannot decide. **AI may identify which trade a message refers to; it may never donate the
   action, price, TP index or side** — those come only from mechanically explicit current-message
   evidence (`day27_management_policy.py`).
3. `CanonicalExecutionDispatcher` routes one durable decision. Source status decides everything:
   - `shadow` → branches into `_dispatch_shadow` and returns **before any broker path exists**.
   - `testing` / `live` → MetaAPI execution on the Owner reference account and eligible members.
   - `paused` / `revoked` → nothing.
4. Canonical signals are published to the private Smart Signals Telegram channel, shown in the
   PWA, and settled against broker truth.

## Shadow / Provider Lab

Shadow providers are measured on a deliberately fair benchmark (`provider_fairness.py`,
model `fixed_1000_10_per_tp_fair_v2`): the same notional **$1,000** account and **$10** cash risk
per TP/runner leg for everyone. Scalper, intraday and swing providers must be scored on AIDY M1
truth (`quote_mode='aidy_m1'`) or the trade is retained for audit but excluded from scoring.

Minimum evidence before a provider may be judged — closed trades / trading days / calendar weeks:
scalper 100/20/4, intraday 60/30/6, swing-or-sparse 30/45/8, mixed and unknown 60/30/6.

**Provider populations must never be mixed:** ~40 shadow discovery providers versus the 5
real/testing providers above.

## Weekly XAUUSD freeze

`weekend_trading_freeze.py`, `Europe/Sofia`: frozen from Friday **23:57**, all Saturday and
Sunday, and Monday before **01:01**; open from Monday 01:01.

During the freeze the automatic MetaAPI read/margin/trade paths are blocked, Telegram provider
readers disconnect, original weekend messages are rejected, settlement and pending reconciliation
return idle, and the AIDY Provider Lab research loop sleeps — so the B–F refresh sleeps too.

This is an automatic-runtime gate, **not** a claim that the whole app is powered off. Health
checks, stored/cached views and the free Gold quote path remain available, and user-initiated
MetaAPI provisioning is not claimed to be frozen.

## AIDY Provider Intelligence A–F

Built and previously production-verified at `278496cc`; still present at `8019f66` in
`provider_intelligence_bf.py`, contract `aidy-provider-intelligence-bf-v1`.

- **A** capture/calendar foundation and learning boundary.
- **B** market-context join — PIT session/regime/context coverage only.
- **C** provider fingerprints — style, cadence, sequence, vocabulary, entry/order/management
  habits, drift.
- **D** research governance — `learning`, `healthy_research`, `watch`, `quarantine_candidate`.
  Cannot mutate `sources.status`.
- **E** provider-specific adaptation — provider grammar may inform interpretation; historical
  numeric levels are prohibited as current execution evidence.
- **F** combined-book conflict — observe-only BUY/SELL consensus and conflicts. Broker netting
  explicitly disabled.

Persistence is append-only through migration `0078_aidy_intel_bf`:
`provider_intelligence_snapshots`, `provider_book_conflict_snapshots`, with current views
`provider_intelligence_current` and `provider_book_conflict_current`. Database triggers reject
UPDATE and DELETE on the snapshot ledgers. Refresh runs inside `AidyShadowRuntime` on a 5-minute
loop that sleeps during the weekly freeze.

At the last Sunday verification both snapshot tables held zero rows because the freeze was
active. Whether they have populated since the market reopened is **unverified** — check it.

## Evidence quality

Engineering completion is not statistical validation. Provider ranking, profitability and
promotion claims remain `WAITING-FOR-FORWARD-EVIDENCE` wherever sample floors are unmet.

## Immediate next product build — AIDY Data Hub

An owner/admin daily control centre reading stored database state and current views. A browser
refresh must **not** itself invoke OpenAI, MetaAPI or external AIDY research.

It should show provider coverage, capture/read quality, context coverage, forward evidence,
fingerprints/confidence/drift/governance, current provider consensus and conflicts, system health
and owner-attention alerts — with raw activity, scored evidence and statistically sufficient
evidence clearly separated.

It must also show **AIDY itself**: current Gold bias/thesis, regime, important levels and setups,
confidence, what it is watching and what would invalidate the view. Providers should be clickable
into their detailed knowledge/profile/evidence.

**AIDY's two Hub feeds already exist** and are merged on AIDY `main` — `/provider/data-health`
(Phase A) and `/provider/decision-memory` (Phase B), bearer-authenticated, failing closed with
503. Nothing consumes them yet. Consuming them is this build.

## Efficiency work still open

- Quarantine four stale historical `broker_filled_position_not_visible` rows from the fast
  settlement/history path without deleting audit evidence.
- Return before broker position/order reads when there are no protection plans.
- Remove the redundant dashboard MetaAPI XAU price read; the UI already uses free Gold feeds.
- Persist OpenAI token/cost and MetaAPI request telemetry.
- Consider an `edited_at` weekly-freeze gate so a pre-weekend message edited during closure
  cannot be replayed after reopen.

## Session rule

Read `NETWORK.md` first. Before any production change, verify the live **deployed branch**
(not `main`), the Render deploy and the relevant production database evidence. Source and
runtime truth override this file.
