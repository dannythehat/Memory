# AIDY Gold cycle learning + toolbox reasoning — LIVE

Date: 2026-09-21

## Final live state

Authoritative AIDY repo: `dannythehat/Aidy-Gold-Signals`

Authoritative branch: `main`

Final main SHA: `9b23e1c83fd169fb9ad08ded97a1ba4cce59ddee`

Canonical Worker: `aidy-signals-test`

Cloudflare Worker version: `395ada01-cf5d-4b51-9b4f-fd207e837a6d`

Final deploy workflow run: `35559806815` — **SUCCESS**

Runtime remains:
- Cloudflare Workers + D1 + R2
- direct cron `* * * * *`
- capture enabled
- Twelve Data / public-independent market source
- formal forward/live-money authority OFF

## What is now live

AIDY now has an additive 15-minute Gold cycle-learning surface under the existing Gold-first architecture. It does **not** replace the wider Gold-intelligence mandate.

Each live cycle view:
- is frozen before its target 15-minute window;
- records bullish / bearish / neutral / unknown;
- records a concise reasoning summary;
- stores supporting reasons and contradictory reasons separately;
- records unavailable/missing evidence rather than inventing it;
- records the canonical toolbox manifest digest;
- records every toolbox capability considered;
- records the subset of evidence/tool surfaces actually used;
- carries an immutable view digest;
- is hard-gated `research_only=true`, `future_values_used=false`, `live_money_execution_allowed=false`.

After the 15-minute target window completes, AIDY can attach:
- realised direction;
- return bps;
- MFE/MAE;
- exact-direction score where scorable;
- an outcome review of the original reasoning without rewriting the original view.

Provider Context exposes current cycle memory PIT-safely, including the day state sequence, state-run duration, latest view and resolved/scored results available by the requested as-of time.

## Live reasoning proof

Final deploy audit queried the live D1 cycle table after deployment.

Latest audited view:
- window: `2026-09-21T04:00:00+00:00`
- observed 15-minute state: **bearish**
- AIDY view: **bearish**
- reasoning present: yes
- supporting reasons: **5**
- contradictory reasons: **1**
- unavailable evidence items: **13**
- canonical toolbox capabilities considered: **33**
- tool/evidence surfaces actually used: **5**
- `future_values_used=0`
- `live_money_execution_allowed=0`

Final workflow emitted:
`cycle_reasoning_audit=true window=2026-09-21T04:00:00+00:00 observed=bearish view=bearish supporting=5 contradicting=1 unavailable=13 toolbox_used=5`

This proves AIDY is not merely writing a direction label. The live view has a frozen, cross-checkable reason trail and explicit toolbox usage/absence metadata.

## Historical cycle memory

A one-time retrospective seed was built from existing BigQuery `research_candles` M15 XAUUSD history for 2024-2025 and loaded into D1.

Source rows: **47,319**

Historical cycle rows loaded: **46,353**

Coverage:
- first historical window: `2024-01-01T23:00:00+00:00`
- last historical window: `2025-12-31T21:30:00+00:00`
- distinct prior state sequences: **120**
- distinct UTC time slots: **95**

Safety verification:
- illegal PIT rows: **0**
- illegal research flags: **0**
- illegal live-money rows: **0**

Historical rows are explicitly:
- `source_provenance=retrospective_history`
- `pit_eligible=0`
- `research_only=1`
- `live_money_execution_allowed=0`

They are descriptive analogue memory only. They cannot silently become live evidence or authority.

## Wider Gold movement spine

The Gold movement scanner remains live and symmetric for both directions. Earlier live D1 audit proved genuine abnormal movement episodes in both directions:
- 1 UP
- 1 DOWN

The movement scanner now:
- advances through eligible snapshots using an immutable scan ledger;
- records normal as well as abnormal scanned snapshots;
- processes a bounded backlog instead of checking only one latest snapshot forever;
- accepts the same PIT-safe intraday evidence boundary used by Provider Context where D1 alone is missing;
- stores abnormal movement investigations independently of provider Telegram signals;
- matures movement learning cards only after the forward horizon becomes genuinely available.

## Toolbox-awareness rule

AIDY's canonical Gold toolbox remains the source of truth for capability awareness.

AIDY must know:
- what capabilities exist;
- what market question each capability answers;
- whether each capability is live/PIT-safe, downstream-resolved, historical/research-only, or not connected;
- which capabilities were considered;
- which were actually used;
- what evidence remains unavailable.

Capability awareness is not permission to fabricate evidence. A tool marked unavailable/not connected remains UNKNOWN.

Known-but-not-yet-live/PIT-connected surfaces still include parts of:
- rates/macro vintages and surprise;
- intraday cross-asset reaction;
- CME contract state;
- GVZ/implied-volatility state;
- breaking-news/official-release search.

Those gaps remain explicit in the toolbox and reasoning trail instead of being silently ignored.

## Owner refinement preserved

The 15-minute cycle framework is **one learning lens**, not AIDY's entire specification.

The primary architecture remains:

`detect Gold move -> investigate evidence-backed cause/mechanism -> observe continuation/reversal -> store structured movement episode -> retrieve analogues -> form independent Gold view -> compare with provider call -> score economic value -> learn from resolved outcome`

AIDY may use 5-minute shock detection, 15-minute cycle memory, higher-timeframe structure, calendar/event evidence, liquidity, volatility, historical analogues, provider intelligence, execution evidence and any other qualified toolbox surface according to relevance.

## Trading/execution boundary

This build did **not** change:
- Super Signals broker execution;
- MetaAPI / MT5 / Vantage;
- provider activation rules;
- owner 1% risk;
- live-money authority.

AIDY remains research/shadow intelligence until separately graduated by explicit authority class.

## Cleanup

The one-time historical seed workflow was removed after successful use.

The normal Cloudflare deploy workflow now treats the Gold cycle module and migration as canonical deploy inputs and includes the live reasoning/toolbox audit.

The previous temporary movement-audit workflow is no longer present.

## Completion gate

This build is complete because:
1. implementation merged;
2. tests/regression passed;
3. D1 migration applied;
4. Worker deployed;
5. minute cron verified;
6. live routes verified;
7. historical analogue memory loaded and safety-checked;
8. a real live cycle view with reasons/toolbox usage was verified;
9. Memory handoff updated.

AIDY can now be left running to accumulate forward cycle views, resolve them, score them and build its live research memory while preserving UNKNOWN and no-hindsight boundaries.
