# Super Signals — Architecture

Verified/updated: **2026-09-13**

## System boundary

Super Signals owns Telegram provider ingestion/interpretation, provider research state, member/broker execution, settlement, account/runtime UX and the embedded provider-intelligence layer.

Standalone `dannythehat/Aidy-Gold-Signals` is a separate system. It supplies independent Gold market/context intelligence and has its own forward-research lifecycle. Do not merge their runtime state merely because both are called AIDY.

## Strategic AIDY direction

The long-term product is an independent Gold/XAUUSD trading intelligence system, not a provider-copying endpoint. Provider evidence is one learning/input channel. AIDY should increasingly build its own market-state understanding, thesis, setup proposals and management intelligence. Any transition from research/paper intelligence into new live-money authority requires a separate explicit gate.

## Production path

High-level flow:

1. Telegram provider reader captures eligible provider messages.
2. Deterministic-first canonical message pipeline classifies/interprets messages, with AI used only where needed.
3. Canonical signals/updates flow into provider research and, where explicitly authorised, the existing live execution path.
4. Provider profile/version/PIT evidence preserves what was known at signal time.
5. AIDY/provider market-context attachments join signals to contemporaneous Gold context.
6. Shadow/research outcomes feed provider benchmark/fingerprint/governance evidence.
7. B-F provider intelligence persists append-only provider and combined-book snapshots.
8. The future Data Hub should read these stored/current views without causing new broker or AI calls.

## AIDY Provider Intelligence B-F

Implementation: `services/api/app/provider_intelligence_bf.py`.

- **B market context:** PIT-safe session/regime/context coverage and benchmark outcome summaries.
- **C fingerprint:** consolidates existing provider footprint/adaptive-profile behaviour.
- **D governance:** research-only learning/healthy/watch/quarantine-candidate classification.
- **E adaptation:** provider-specific language/style/sequence/cadence knowledge; historical price levels cannot become current execution evidence.
- **F combined book:** observe-only current BUY/SELL provider consensus/conflicts; broker netting disabled.

Append-only persistence introduced by migration `0078_aidy_intel_bf`:

- `provider_intelligence_snapshots`
- `provider_book_conflict_snapshots`
- current views `provider_intelligence_current` and `provider_book_conflict_current`

Database triggers block UPDATE/DELETE on the snapshot ledgers.

## Weekly market freeze

`services/api/app/weekend_trading_freeze.py` defines the standard XAUUSD weekly close/open gate in `Europe/Sofia`.

The automatic MetaAPI read/margin/trade gateways, Telegram monitoring, settlement, pending reconciliation and AIDY Provider Lab external-research loop respect the freeze. This is an automatic-runtime gate, not a claim that every web/UI/provisioning action is disabled.

## Live risk/execution boundary

- Current owner directive: **1% risk only**.
- B-F intelligence cannot place/close/change/cancel broker trades.
- B-F governance cannot mutate live source status.
- F cannot perform broker netting.
- Research evidence cannot silently become execution authority.

## Gold price display

The app's displayed Gold quote uses free HTTP feeds rather than MetaAPI as the primary/fallback display source. Dashboard broker-state code still has a redundant MetaAPI XAU price read that should be removed as an efficiency cleanup.

## Data Hub architecture requirement

The AIDY Data Hub is an owner/admin read surface over durable database evidence/current views. Page refreshes should stay cheap: querying PostgreSQL is acceptable; invoking OpenAI, MetaAPI or external AIDY research simply because the owner opened/refreshed the page is not.

The Hub should surface both provider intelligence and AIDY's own evolving Gold-market intelligence without conflating evidence maturity with statistical validation.
