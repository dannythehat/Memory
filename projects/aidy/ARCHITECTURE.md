# AIDY — Architecture Memory

This is a compact orientation map. Verify implementation details in `dannythehat/Aidy-Gold-Signals`.

## Core responsibility

AIDY is the independent Gold/XAUUSD intelligence and evidence system. It captures market/macro evidence, preserves point-in-time truth, builds context and supports forward research/decision infrastructure.

## Main layers

1. **Capture/orchestration** — Cloudflare Worker + scheduler + queue.
2. **Operational evidence** — Cloudflare D1.
3. **Durable archive** — Cloudflare R2 through an archive outbox.
4. **Market data** — Twelve Data XAU/USD minute capture and derived timeframes.
5. **Macro/cross-market evidence** — independent/public evidence paths with first-observed/revision semantics.
6. **Forward decision infrastructure** — model/context/safety/immutable ex-ante records; formal-forward authority is explicitly gated.
7. **Research/analytics** — historical/forward analysis including BigQuery where appropriate.
8. **Provider boundary** — bounded authenticated market OHLC interface used by Super Signals Provider Lab without exposing internal evidence or broker state.

## Current resilience layers

- D1 row-read budget monitor.
- market-calendar-aware capture freshness watchdog.
- archive-outbox durability watchdog.
- bounded/index-driven acceptance queries.

## Key principle

AIDY should know **what the market looked like at the time**, without hindsight and without borrowing broker/provider outcome information as if it were market evidence.
