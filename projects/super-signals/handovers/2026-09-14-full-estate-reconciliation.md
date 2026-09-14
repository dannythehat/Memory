# Super Signals Handover — 14 September 2026

## Scope

A full read of all five repositories in the estate, followed by a reconciliation of Memory
against source truth. No code was changed in any project repository. Only Memory was updated.

This was an **understanding and reconciliation pass**, not a build day.

## Evidence status

**SOURCE VERIFIED.** Render, PostgreSQL, MetaAPI, Cloudflare and D1 were not accessible in this
session and were not inspected. Runtime figures carried forward from the 13 September handover
are labelled as such in `LIVE_STATE.json`.

## What was read

- `dannythehat/super-signals` — deployed branch `feature/day-10-shared-telegram-sources` at
  `8019f66`; 199 API modules, 38 route modules, 82 migrations, 67 tables, 171 API test files.
- `dannythehat/super-signals-website` — `main` at `088096a`; Cloudflare Worker, entry
  `src/index-v4.js`, domain `smartsignals.site`.
- `dannythehat/Aidy-Gold-Signals` — `main` at `cb0f4bc`; 130 source files, 104 workflows,
  20 D1 migrations.
- `dannythehat/Telegram-Signals-Auto-Trader` — dormant since 2026-08-04.
- `dannythehat/Memory` — this repository.

## Findings that changed Memory

### 1. The deployed branch had moved 71 commits

Memory recorded the deploy SHA as `278496cc` (13 Sep 17:35). The deployed branch head is now
`8019f66` (14 Sep 12:05). The 71 intervening commits include a merged stability release
(`a2ee912` "Merge stability release: keep trading app alive"):

- dashboard polling paused while off-screen, with Today summary and gold quote preserved;
- dashboard kept mounted across workspace navigation; no forced frontend reloads during live
  sessions; active trading sessions kept on the current service worker;
- owner account portfolio overview across all connected accounts;
- owner manual close made account-environment neutral and retry-hardened through transient
  Render outages;
- MT5 reconciliation moved off the web event loop;
- member MT5 onboarding rebuilt as Connection V2 without blocking on MetaAPI inventory;
- final hotfix pointing the Render web API base at the same-origin root.

### 2. `main` is 141 commits behind production

`render.yaml` pins `feature/day-10-shared-telegram-sources`. `main` sits at `4bb664b`. A branch
named `production` sits at `ade297e` and is **not** deployed. This is now recorded as the
highest-priority governance item in `KNOWN_ISSUES.md`.

### 3. The risk directive in Memory was materially wrong

Memory said "owner live risk directive remains **1% only**". `provider_risk_policy.py` says every
enabled TP/runner leg carries exactly 1% planned risk, so four legs mean **4% planned signal
risk**. Policy generation `owner-authority-2026-09-09-v2-one-percent-per-tp`. Corrected, and a
decision recorded.

### 4. The protection ladder was paraphrased incorrectly

Memory said "TP1 + TP2 hit → move SL to entry; TP3 hit → move SL to TP2". The implementation says
**TP2 hit** cancels unused entry orders and moves every open TP3+ leg to **its own entry**
(per-leg breakeven); **TP3 hit** moves every remaining TP4+/runner stop to the signal's TP2 price.
Corrected.

### 5. Alembic head had moved

`0078_aidy_intel_bf` → `0079_fix_member_entitlements`, which splits a shared entitlement trigger
function so each trigger references only columns present on its own table.

### 6. The approved provider roster was not recorded anywhere in Memory

Now recorded from `provider_risk_policy.py`: FXTradingVision (BUY+SELL, 3 targets), GTMO (BUY
only), TIG's Asia Trades (BUY+SELL), SureShot (SELL only), United Kings (SELL only).

### 7. The brand split was not recorded

Repositories say "Super Signals"; the customer-facing brand is **Smart Signals** on the website,
in the app UI and in member email. Environment variables are split across `SUPER_SIGNALS_*` and
`SMART_SIGNALS_*`. Recorded so nobody "tidies" it casually.

### 8. AIDY's Hub feeds already exist

`/provider/data-health` and `/provider/decision-memory` are merged on AIDY `main`,
bearer-authenticated, failing closed with 503. Nothing in Super Signals consumes them. This
materially reduces the remaining Data Hub work.

## Architecture confirmed unchanged

- Weekly XAUUSD freeze, `Europe/Sofia`, Friday 23:57 → Monday 01:01, code identical at `8019f66`.
- B–F provider intelligence present, append-only, broker-isolated, refreshed on the 300s
  `AidyShadowRuntime` loop that sleeps during the freeze.
- Shadow isolation is structural: a `shadow` source branches into `_dispatch_shadow` and returns
  before any broker code path exists.
- The interpretation boundary holds: AI may link a message to a trade; only mechanically explicit
  current-message evidence may donate the action, price, TP index or side.
- Quality is enforced as a Docker build gate across secret-scan, web-quality and api-quality
  stages. A failing test cannot be deployed.

## Live-risk contract (restated)

- Instrument XAUUSD.
- **1% planned risk per enabled TP/runner leg.**
- TP2 hit → cancel unused entry orders, move open TP3+ legs to their own entry.
- TP3 hit → move remaining TP4+/runner stops to the signal TP2 price.
- Moving SL to entry does not mean closing the trade. Protection is never loosened.
- B–F intelligence changes none of this.

## Unresolved / next verification

Nothing below was checked. These come first once database, Render and Cloudflare access exist:

1. Render deploy id, the SHA it was built from, and whether auto-deploy is on — `render.yaml`
   says `autoDeployTrigger: off` while the previous `LIVE_STATE.json` said `auto_deploy: true`.
2. PostgreSQL: real Alembic head; counts of sources by status (`testing`/`shadow`/`live`/
   `paused`/`revoked`) to confirm the ~40 shadow vs 5 real split; whether
   `provider_intelligence_snapshots` and `provider_book_conflict_snapshots` have populated since
   the market reopened on Monday.
3. Re-run the quality gate at `8019f66` — the 931/67/0 figure was measured at `278496cc`.
4. The five open efficiency items, unchanged from 13 September.

## Exact next step

**Build the AIDY Data Hub.**

Read stored database state and current views only — a browser refresh must not invoke OpenAI,
MetaAPI or external AIDY research. The B–F current views are ready. AIDY's `/provider/data-health`
and `/provider/decision-memory` are ready and unconsumed.

Before writing Hub code, verify the runtime items above, and read `../../../NETWORK.md` for the
whole-estate map.

## Session bootstrap for the next agent

`NETWORK.md` → `CURRENT_STATE.md` → `SAFETY_RULES.md` → `LIVE_STATE.json` → this handover. Then
verify the **deployed branch** (not `main`), the Render deploy and the production database before
changing anything.
