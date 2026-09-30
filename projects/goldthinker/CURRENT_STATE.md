# GoldThinker — Current State

Created: **2026-09-30**. Status: **FOUNDATIONS / RESEARCH ONLY — nothing built, no code, no repo, no runtime.**

GoldThinker is the owner's project for a gold (XAUUSD) candlestick trader. It is a **separate
system** from AIDY and Super Signals: own data feed, own database, own code. The owner said
explicitly (2026-09-30) "Fuck Aidy... this is new" — do not build on AIDY's data or loop.
It has no production or broker authority. Do not import it into either project's state.

## The vision (owner's words, agreed 2026-09-30)

1. GoldThinker monitors gold **24/7, Monday to Friday (until the Friday close)** on a server with
   a database, using a live market feed (Vantage candles, or other tools).
2. He is taught **every candle type (~50)**, each with an exact definition and a best-practice
   trade plan. Images of candle types can be supplied as examples.
3. When the market shows a candle type, he **places the paper trade(s) that candle's plan calls
   for**. Every candle type fires whenever it appears, including rare ones (some occur monthly).
4. Results are **recorded per candle type** and reviewed after **1 month, then 2, then 3**.
5. Only the **profitable, tried-and-tested candle types are kept**. **Only then does he go live.**
   Nothing goes live before that.

## Decisions made by the owner (2026-09-30)

- **Paper trades are recorded in both places:** GoldThinker's own database AND a Vantage demo
  account.
- **Rule conflicts between sources:** owner says this "won't happen" — he settles one rule set per
  candle. (Note: the collected sources already differ in details, e.g. hammer body "upper third" vs
  "upper 40%". Claude will flag each difference to him when a candle is defined so he chooses.)
- **Timeframes: all.**
- **Trade size: 1% risk per paper trade, fixed, for easy calculation.**
- **Rules-based, same candle = same trade.** Owner is unsure whether AI may be needed "to read or
  look for candle types". Claude's recommendation (not yet confirmed by owner): rules-only for the
  trading step so every trade is repeatable and explainable; AI used at build time to read
  images/articles and check the definitions. Revisit if some candle types cannot be expressed in
  numbers.

## Not yet decided

- Live data source: owner points to Vantage's live gold chart. Claude had proposed a separate
  Vantage demo account connected through MetaAPI (not the trading account, so it cannot affect live
  trading) — owner has not agreed to that; he said not to jump ahead. Secrets must never be pasted
  into chat.
- Hosting/server, database, how the owner views it (web page or Telegram), the full candle list,
  and each candle's exact trade plan (entry, stop, target, direction).
- Whether the owner's three friends who read gold will share rules or trade history.
- The owner is consulting ChatGPT on the design and will bring its input back.

## Prior evidence (context, not a verdict)

- Not re-verified this session: AIDY's own price-structure experts scored at or below coin-flip on
  42 days of gold (see `projects/aidy/CURRENT_STATE.md`, 2026-09-23). That tested AIDY's experts
  only; the owner's plan is to find out from forward paper results.
- Within the wider business, provider selection is the measured edge so far (30-day real P&L
  checked 2026-09-29: TIG's Asia Trades +$575, FXTradingVision +$453).

## Research collected so far (15 sources, all 2026-09-30)

Rules are consolidated in `CANDLE_SPEC_V1.md`; full extracts are in `RESEARCH_SOURCES.md`; the merged candle list (41 types, 53 versions, with status of each plan and the shared definitions still to settle) is in `MASTER_CANDLE_LIST.md`. Vendor and article pages give pattern shapes, entries,
stops and targets; none gives results data, which is why the plan is to generate the results by
paper trading. Recurring themes: every page defers the trade to a confirmation candle (must be
defined using only information available at entry); "location" (support, round numbers,
Fibonacci) is what they say matters and is the least defined; almost every page says to avoid or
shrink the Asian session (a filter to record and compare, not assume).

## Hub (owner requirement, 2026-09-30)

A hub/site the owner can open at any time: every candlestick we use, every trade logged when it happens,
which candles traded and when, P&L in dollars and percentages, how many times each formed, latest stats
per candle, balance continuously updated and broken down per candlestick, daily profit and loss, and
which candles made or lost what. Each candle has its own page with an image of the exact candle, how it
works, and its information. Built on the same database as the paper engine; not built yet. Open question:
which "balance" (see `DECISIONS.md`, Open).

## Boundaries

- Paper trading only until the owner decides otherwise after the 1/2/3-month reviews.
- No connection to the Super Signals live trading account or its MetaAPI connection.
- No claim of edge, "profitable" or "validated" without evidence per root `AGENTS.md`.
- Do not build or set up infrastructure until the owner says the foundations are agreed.

## Next step

`CANDLE_SPEC_V1.md` is at DRAFT 0.3.2 (Wave 1: 22 patterns plus 2 early-setup companions); the ambiguity phase is closed
(D-038 accepted by ChatGPT, D-039). Golden test vector pack GV-0.2 (1,408 vectors, incl. end-to-end and tick-path vectors)
is in `tests/` (start with `tests/README.md`; rulings in `tests/RULINGS.md`). Working rule (D-035): Claude and ChatGPT settle
trading-research and engineering rules; the owner decides product/business choices and anything involving real money.
Order of work (D-039): (1) done: `PIP_SRC_USD = 0.10` confirmed (D-040), SRC-PS variants enabled, (2) done: `VALIDATION_RULES.md` v0.2 (D-041, approved),
(3) drafted: `PORTFOLIO_RULES.md` v0.1 + 18 vectors in `tests/portfolio/` (D-042, for ChatGPT to challenge), (4) build the detector against `golden_vectors.json` (needs the owner's go-ahead, D-005).
After that: the Vantage demo account and a feed reliability test.
