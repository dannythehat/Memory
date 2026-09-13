# Super Signals — Current State

Last verified: **2026-09-13**

Authoritative repo: `dannythehat/super-signals`
Authoritative deployed branch: `feature/day-10-shared-telegram-sources`
Verified source/deploy SHA: `278496ccbe71ec14f4e2e63b0dbd05004ea774b5`
Render service: `super-signals-day-8` (`srv-d9qmcgks728c73a555m0`)
Verified live deploy: `dep-dajb9cmk1f9s73fm0b3g`
Verified migration head: `0078_aidy_intel_bf`
Quality gate at deployed SHA: **931 passed, 67 skipped, 0 failed**.

## Product north star

Super Signals is not building AIDY merely to classify Telegram providers. Provider signals are evidence and training material. The strategic objective is for AIDY to become an independent Gold/XAUUSD trading intelligence system that can understand Gold market moments, form its own market thesis, identify setups, judge or disagree with providers, and eventually propose and manage its own trades.

That strategic objective does **not** grant new broker authority today. Live execution remains governed by the explicit production rules and owner gates below.

## Current live execution posture

- Trading universe remains Gold/XAUUSD.
- Owner live risk directive remains **1% only** unless explicitly changed.
- Approved management semantics remain: TP1 + TP2 hit -> move SL to entry; TP3 hit -> move SL to TP2; `move SL to entry` does not mean close the trade.
- Research/shadow/provider-intelligence systems cannot silently change risk, promote/demote live providers, place trades, net broker positions or acquire live-money authority.

## Weekly XAUUSD freeze — PRODUCTION VERIFIED

The automatic trading/research runtime now follows the standard XAUUSD weekly closure in `Europe/Sofia` time:

- Friday from 23:57 -> frozen.
- Saturday -> frozen.
- Sunday -> frozen.
- Monday before 01:01 -> frozen.
- Monday 01:01 onward -> open.

During the freeze the automatic MetaAPI read/margin/trade paths are blocked, Telegram provider readers are disconnected, original weekend messages are rejected, settlement and pending reconciliation return idle results, and the AIDY Provider Lab external research loop sleeps. B-F intelligence refresh is inside that paused runtime and therefore sleeps too.

The web/app itself is not globally powered off: health checks, stored/cached views and the free Gold quote path may remain available, and timer tasks may briefly wake to check the clock. User-initiated MetaAPI provisioning is not claimed to be frozen by this gate.

## AIDY Provider Intelligence A-F

The provider-intelligence foundation and B-F integration are built and production verified at the deployed SHA. Statistical/provider-profit claims remain separate and require forward evidence.

- **A — capture/calendar foundation:** PIT-safe provider capture/research foundation and learning boundary.
- **B — market-context join:** per-provider signal evidence is summarized against contemporaneous session/regime/context only.
- **C — provider fingerprints:** provider style, cadence, sequence, vocabulary, entry/order/management habits and drift are consolidated from existing footprint/adaptive profiles.
- **D — automatic research governance:** providers can be classified `learning`, `healthy_research`, `watch` or `quarantine_candidate`; this cannot mutate live source status.
- **E — provider-specific adaptation:** interpretation can use provider-specific grammar/behaviour while historical numeric levels remain prohibited as current execution evidence.
- **F — combined-book conflict intelligence:** current provider BUY/SELL consensus/conflicts are visible in observe-only form; broker netting is explicitly disabled.

Persistence is append-only through:

- `provider_intelligence_snapshots`
- `provider_book_conflict_snapshots`
- `provider_intelligence_current`
- `provider_book_conflict_current`

At Sunday verification the new snapshot tables contained zero rows because the weekly market freeze was active. That is expected; do not bypass the freeze to fabricate/populate forward evidence.

## Current evidence quality

Engineering completion is **not** statistical validation. The latest provider-forward evidence remains insufficient for broad promotion/profitability claims. Where Day 13-style evaluation has no eligible OOS trades/results, the correct status is `WAITING-FOR-FORWARD-EVIDENCE`, not profitable/unprofitable.

## Immediate next product build

**AIDY Data Hub** — owner/admin daily control centre.

The Hub should read stored database state/current views rather than trigger OpenAI or MetaAPI simply because the page refreshes. It should expose provider coverage, capture/read quality, context coverage, forward evidence, provider fingerprints/confidence/drift/governance, current provider consensus/conflicts, system health and owner-attention alerts.

It must also show **AIDY itself**: current Gold bias/thesis, market regime, important levels/setups, confidence, what it is watching and what would invalidate the view as those capabilities become available. Individual providers should be clickable into their detailed AIDY knowledge/profile/evidence.

## Efficiency work still open

- Quarantine four stale historical `broker_filled_position_not_visible` rows from the fast settlement/history path without deleting audit evidence.
- Avoid position/order broker reads when there are no protection plans.
- Remove the redundant dashboard MetaAPI XAU price read where the UI already uses the free Gold quote feeds.
- Persist OpenAI token/cost and MetaAPI request telemetry.
- Consider an `edited_at` weekly-freeze gate so a pre-weekend message edited during closure cannot be replayed after reopen.

## Session rule

Before any production change, verify the live source branch, Render deploy/runtime and relevant production database evidence. Source/runtime truth overrides this Memory file if they disagree.