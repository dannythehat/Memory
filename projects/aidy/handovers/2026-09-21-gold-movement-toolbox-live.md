# AIDY Gold movement capture + toolbox awareness — LIVE — 2026-09-21

## Owner mandate verified

AIDY is Gold intelligence first and provider filter second.

Required loop:

`Gold movement -> detect abnormality -> investigate evidence-backed cause/mechanism -> observe continuation/reversal -> store structured movement episode -> retrieve analogues -> form independent Gold view -> compare with provider signal -> score economic value.`

The owner specifically requires meaningful Gold spikes in **both directions** to be captured, investigated and learned, and requires AIDY to know the wider toolbox already built across AIDY/Super Signals.

## Live movement-capture repair

AIDY PR #147 merged as:

`bbbc9a59d2fcc9fc0fe0fd9bf18dd90091dfd084`

Cloudflare deploy workflow:

`35557842332` — SUCCESS.

Changes:
- added immutable `aidy_gold_movement_scan_ledger`;
- every eligible scheduled snapshot is marked scanned whether normal or abnormal;
- scanner now handles a bounded batch of 10 unscanned snapshots per cron cycle rather than only the newest one;
- scanner works through backlog while prioritising latest evidence;
- Provider-Context-eligible D1-only-degraded snapshots are admitted when fresh M1/M5/M15/H1/H4 are all intact;
- strict evidence/no-hindsight rules remain;
- abnormal episodes retain same-direction cooldown/dedupe;
- live-money authority remains OFF.

## Direct live D1 proof

Temporary audit workflow run `35557600712`, attempt 2, job `106205085312` succeeded against remote D1.

At approximately 2026-09-21 03:34 UTC, live D1 contained:
- movement investigations: **2**
- UP: **1**
- DOWN: **1**
- flat: 0
- latest trigger: `2026-09-21T03:12:30.158000+00:00`

Observed episodes:
- UP at `2026-09-21T03:07:30.147000+00:00`, trigger `abnormal_5m_range`, attribution `cause_unknown`
- DOWN at `2026-09-21T03:12:30.158000+00:00`, trigger `abnormal_5m_range`, attribution `cause_unknown`

Both rows were research-only, future-values-used=false and live-money-execution-allowed=false.

This is direct proof that the live directional movement detector is symmetric and is firing on real captured Gold movement in both directions.

Learning cards were still 0 at that audit because the newly discovered episodes had not yet reached the 60-minute forward-observation maturity boundary. Do not claim continuation/reversal learning-card maturation is proven until cards exist after their maturity time.

The temporary audit workflow was removed after use in PR #149. Current AIDY repository main after cleanup: `bbbe8dda8836eff8b673d36ca1bbd3345cc24bac`.

## Canonical Gold toolbox awareness

AIDY PR #148 merged as:

`5f11c13b86467e72cd178b3c92cb44e813732533`

Cloudflare deployment succeeded. Live `/health` exposes:

`gold_toolbox_manifest_version = aidy_gold_toolbox_manifest_v1`

The canonical catalogue contains 30+ known capabilities covering:
- XAUUSD M1/M5/M15/H1/H4/D1 candles and structure;
- session/day map;
- price location/reference levels;
- liquidity sweep/reclaim proxies;
- realised volatility and jump/continuous state;
- scheduled event context and economic calendar;
- macro actual-vs-consensus surprise;
- rates/yields/inflation vintages;
- cross-market backdrop and intraday cross-asset reaction;
- CME contract/roll state;
- GVZ implied volatility;
- breaking-news/official-release search;
- Gold movement detector/memory/analogue retrieval;
- recent Gold candle inspection;
- provider conditional alpha/history;
- recent provider messages;
- execution/slippage/liquidity context;
- provider historical analogues;
- probability/EV/management;
- failure attribution/self-critique;
- self-calibration;
- provider decision memory.

Every capability has an explicit status. The important distinction is preserved:
- `live_here`
- `super_signals_runtime_resolves`
- `research_exists_not_live_connected`
- `known_unknown`

AIDY must know a capability exists without pretending unavailable evidence was observed.

## Super Signals reasoning integration

Super Signals PR #240 merged to production branch `feature/day-10-shared-telegram-sources` as:

`f33a83ffa965b4b42ab2cd579b6012ba85a601f6`

Render deploy:
`dep-daoaeau8bjmc73b6mmeg` — **LIVE**, finished `2026-09-21T03:42:19.642122Z`.

Live reasoning changes:
- toolbox manifest upgraded to `aidy_live_toolbox_manifest_v2`;
- standalone Gold capability catalogue is now copied into every live reasoning toolbox packet;
- reasoning prompt upgraded to `aidy_reasoning_prompt_v14_gold_toolbox`;
- model is explicitly taught availability semantics;
- current candle/calendar tools remain actually callable;
- wider disconnected research remains UNKNOWN until PIT-safe adapters exist.

Post-deploy runtime log proved:
`AIDY Provider Context live probe READY context_lag_seconds=248 snapshot_id=864f2d0b-1855-4191-8272-6be0aa58346a`

Render service health remained HTTP 200 and deployment became live.

## Current connected-vs-known truth

Actually connected/usable now includes:
- live Gold candle/structure evidence;
- session, location and liquidity proxies;
- realised/jump volatility when qualified;
- scheduled-event context when linked;
- stored PIT cross-market backdrop where known;
- Gold movement detector + episode memory + analogue retrieval;
- Super Signals on-demand recent Gold candles;
- Super Signals economic calendar;
- provider evidence/history;
- recent provider messages;
- event/liquidity/execution context;
- provider alpha + prior analogues;
- probability/EV/management;
- failure/self-critique;
- self-calibration.

Known to AIDY but **not yet live/PIT-connected to the movement investigator**:
- live rates/macro vintages;
- macro actual-surprise feed;
- intraday cross-asset reaction at the spike;
- CME live contract state;
- GVZ live feed;
- breaking-news/official-release search;
- provider decision memory as a callable movement-investigation tool.

The system must never convert these statuses into invented evidence.

## Safety

No change to:
- owner live risk: 1%;
- best-side/provider routing rules;
- MT5/MetaAPI/Vantage execution;
- broker credentials;
- AIDY live-money authority.

Formal forward remains OFF.

## Next engineering priority

Operationalise the missing PIT-safe toolbox adapters for abnormal-move investigation, prioritising:
1. economic-calendar / actual-surprise evidence directly into the standalone movement episode;
2. intraday USD/yields/cross-asset reaction;
3. breaking news / official releases;
4. live rates/CME/GVZ evidence.

The capability catalogue is now the control plane: future tools must be registered there and cannot be represented as live until their timestamp/provenance adapter is verified.
