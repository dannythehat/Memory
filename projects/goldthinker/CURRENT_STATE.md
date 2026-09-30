# GoldThinker — Current State

Created: **2026-09-30**. Status: **RESEARCH ONLY — nothing built, nothing tested, no code.**

GoldThinker is the owner's working name for a possible candle-pattern reader / trading-edge
project for gold (XAUUSD). It is a separate system from AIDY and Super Signals. It has no
repository, no runtime and no production authority. Do not import it into either project's
state.

## Why it exists

Owner wants "something with real edge" and noticed that many candle-reader apps are popular
and paid for (~$50/month). Question raised: why can't we build one?

## Where we stand (honest baseline)

- **No edge is demonstrated.** Claude's position, agreed as the framing: popularity and
  willingness to pay show a product sells, not that it makes money. Two separate questions:
  (1) can we build a sellable app; (2) can it trade profitably. (2) must be proven by backtest.
- Prior evidence from AIDY (see `projects/aidy/CURRENT_STATE.md`, 2026-09-23, not re-verified
  this session): 15-minute gold direction over 42 days was ~47% up / 48% down / 6% flat, and
  AIDY's price-structure/momentum experts scored at or below coin-flip. That tested AIDY's own
  experts on one instrument, one horizon, mostly one (bearish) regime. It does not prove that
  no candle approach works.
- The only measured edge in the wider business is **provider selection** (30-day real P&L
  checked 2026-09-29: TIG's Asia Trades +$575, FXTradingVision +$453).

## Research collected so far (12 sources, all 2026-09-30)

Full extracts, exact rules and per-source cautions are in `RESEARCH_SOURCES.md`. One-line summary:
articles and vendor pages (TradingView, FTMO, Seeking Alpha, a hobbyist gold playbook, Investing.com's
scanner, Pro-Scalper's pattern pages) give pattern shapes, entries, stops and targets but **no win
rates, sample sizes or backtests from any of them**. The most repeated claim is "avoid the Asian
session"; every page defers the trade to a confirmation candle (look-ahead risk if not defined
carefully); "location" (support, round numbers, Fibonacci) is what they say matters most and is the
least defined. Owner is still gathering research, and mentioned three friends who read gold and could
supply real rules or trade history (not yet obtained). Owner will supply chart data to pull in
(format not yet agreed).

## Proposed test design (NOT approved, NOT run)

- Rules fixed in writing before any run; no tuning to fit.
- Exits reported as three fixed variants (1R, 2R, fixed N bars); no picking the best afterwards.
- Timeframes 5/15/60 min built from M1; daily/H4 not testable on current data (~12 D1, ~50 H4 bars).
- Entry next bar open; spread and slippage included.
- Compare against random same-direction entries over the same period (gold drifted down, which
  flatters bearish patterns).
- Held-out data untouched until the end; multiple-testing correction across all tests.
- Report trigger counts; small samples are inconclusive.
- **Data is the limiting factor:** ~41k M1 bars / 42 days in AIDY's D1 (`aidy-ops-test`,
  read-only source). Several years of XAUUSD history from a free or Twelve Data source would be
  needed for a meaningful answer; not yet attempted.

## Boundaries

- Research/backtest only. No broker, member or Super Signals execution authority.
- Read-only use of AIDY data; do not write to AIDY's D1 or touch its live loop (an edit to
  that loop already caused a 5h39m outage on 2026-09-23).
- Do not claim edge, "profitable" or "validated" for anything here without the evidence
  language in root `AGENTS.md`.

## Next step

Wait for the owner's further research. Then: confirm exact pattern definitions with the owner,
decide the data source, and only then run the pre-registered backtest.
