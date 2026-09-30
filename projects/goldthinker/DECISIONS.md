# GoldThinker — Decisions log

Append-only. Each entry says who decided and its status. **OWNER** = the owner said it directly.
**PROPOSED** = agreed between Claude and the independent reviewer (ChatGPT), awaiting the owner's explicit
confirmation. Nothing here authorises building or any live trading.

| # | Date | Decision | Status |
|---|---|---|---|
| D-001 | 2026-09-30 | GoldThinker is a separate system from AIDY and Super Signals: own data, database and code. | OWNER |
| D-002 | 2026-09-30 | Vision: watch XAUUSD Mon-Fri, detect every defined candle, place a paper trade per that candle's plan, record per candle type, review at 1/2/3 months, keep only proven ones, only then go live. | OWNER |
| D-003 | 2026-09-30 | Paper trades are recorded in GoldThinker's own database AND on a Vantage demo account. | OWNER |
| D-004 | 2026-09-30 | All timeframes; 1% risk per paper trade; rules-based (same candle, same trade). | OWNER |
| D-005 | 2026-09-30 | Nothing is built until the foundations are agreed. | OWNER |
| D-006 | 2026-09-30 | Timeframes = M1, M5, M15, M30, H1, H4, D1, W1, MN1 (the nine common ones). | PROPOSED |
| D-007 | 2026-09-30 | 1% of a fixed reference balance per independent strategy, not of shared demo equity. | PROPOSED |
| D-008 | 2026-09-30 | GoldThinker's own database is the source of truth for results; the Vantage demo account is an execution mirror only. | PROPOSED |
| D-009 | 2026-09-30 | Every signal gets its own independent virtual trade, even when an earlier one is open or several patterns fire together; a separate portfolio view shows the combined exposure. | PROPOSED |
| D-010 | 2026-09-30 | Three measurement layers per detection: (A) raw candle behaviour, (B) uniform GoldThinker baseline, (C) each source's own plan. Never averaged together. | PROPOSED |
| D-011 | 2026-09-30 | Results are never pooled across timeframes, variants or rule versions. A changed rule creates a new version and a new sample. | PROPOSED |
| D-012 | 2026-09-30 | Ambiguous stop/target trades (no tick data) are scored STOP FIRST and tagged; a target-first sensitivity figure is also reported; they are never deleted. | PROPOSED |
| D-013 | 2026-09-30 | Indicator filters (RSI/MACD/DXY/Bollinger) are recorded as context and the plain candle is tested first; where a source requires a filter, that source version also exists as its own variant. | PROPOSED |
| D-014 | 2026-09-30 | Classical gap patterns stay as defined; any gold adaptation gets a different name. | PROPOSED |
| D-015 | 2026-09-30 | Source-language "pips" are never used internally; store dollars/ATR fractions. `PIP_SRC_USD = 0.10` is an unconfirmed assumption. | PROPOSED |
| D-016 | 2026-09-30 | Confirmation must occur on the immediately following completed bar unless a source explicitly allows longer (max 3 bars); expiry = no trade. | PROPOSED |
| D-017 | 2026-09-30 | Wave 1 = the 22 patterns with FULL plans; other patterns join later with their own clocks. Every rule must be fully defined before its detector is enabled. | PROPOSED |
| D-018 | 2026-09-30 | Discovery (3 months) -> freeze survivors -> untouched validation period -> live candidate. A Month-3 winner does not go straight to real money. | PROPOSED |
| D-019 | 2026-09-30 | Survival gates (net R after costs): M1 review min 20 obs, kill only if expectancy <= -0.20R, PF < 0.80 or DD > 15R; M2 min 40 obs, continue if expectancy > 0, PF >= 1.05, DD <= 12R; M3 min 75 obs, candidate if expectancy >= +0.10R, PF >= 1.20, DD <= 10R, positive in 2 of 3 months, plus a day-block bootstrap CI lower bound above zero. Rare candles: <30 trades UNKNOWN, 30-74 PRELIMINARY. Numbers are ChatGPT's proposal. | PROPOSED |
| D-020 | 2026-09-30 | Feed: separate Vantage demo account, tick stream (bid/ask/spread) with our own bars; feed reliability tested first (MetaAPI timed out repeatedly on the Super Signals side this week). | PROPOSED |
| D-021 | 2026-09-30 | Authoritative record is versioned documents in this repo (`CANDLE_SPEC_V1.md`, `DECISIONS.md`, `CURRENT_STATE.md`), not any chat's memory. | PROPOSED |
| D-022 | 2026-09-30 | **Hub requirement (owner's words):** one place he can check at any time showing ALL candlesticks: every trade logged, which candles traded and when, P&L in dollars and percentages, how many times each formed, latest stats per candle, balance continuously updated and broken down per candlestick, daily profit and loss, which candles made or lost what. Every candle has a page with an image of the exact candle and how it works, plus its information. | OWNER |
| D-023 | 2026-09-30 | The hub is a core part of GoldThinker, not an optional report. Home = grid of candlestick cards; each candle has its own page (illustration, how it works, exact definition, trade rules, stats, timeframe comparison, equity curve, recent detections/trades, individual trade chart). Global top section: Total Experimental P&L (until Portfolio Simulation rules exist, D-024), today/week/month P&L, open positions, total trades, winners, losers, best/worst candle. Candles with too little data show "NOT ENOUGH DATA", never a headline win rate. | PROPOSED (ChatGPT + Claude) |
| D-024 | 2026-09-30 | Balances shown separately, never merged: (1) Strategy Balance = fixed $10,000 reference per candle x timeframe x variant (1R = $100, non-compounding); (2) Portfolio Simulation Balance under explicit portfolio rules (rules still to be defined; until they are, the hub's top figure is labelled "Total Experimental P&L", and "research balance" in D-023 means this Portfolio Simulation Balance once it exists); (3) the Vantage demo account's real balance as the execution mirror. Home cards show one selected timeframe and variant at a time; any all-timeframe total is labelled a sum of separate ledgers, not a strategy result. Baseline and source-plan results are never blended. | PROPOSED (Claude, adding to ChatGPT) |
| D-025 | 2026-09-30 | Event model (reworded 2026-09-30 for Draft 0.2.1): SHAPE_DETECTED -> BASE_PATTERN_FORMED (canonical shape + prior state) -> VARIANT_QUALIFIED (a variant's own context/identity rules; may qualify without the base pattern forming) -> SIGNAL (with exact `signal_time`) -> TRADE, with a reason code for every non-trade. Canonical shape/formed counts are stored once per pattern x side x TF x version; qualified/signals/trades/skips/P&L per pattern x side x TF x variant x version. Formation counts never come from trades. | PROPOSED (ChatGPT review) |
| D-026 | 2026-09-30 | Kicker and Abandoned Baby are each split into the completed pattern (entry after completion) and an EARLY_SETUP pattern (the source's opening-tick entry). Every early trigger counts as a trade; the completed outcome is only a label, never a filter. | PROPOSED (ChatGPT review) |
| D-027 | 2026-09-30 | Layer C is renamed SOURCE-NORMALIZED and every variant carries `source_deviation_notes`. Canonical (BASE) identities must not depend on the unconfirmed source-pip assumption. | PROPOSED (ChatGPT review) |
| D-028 | 2026-09-30 | Bar completion follows the broker calendar (next bar start or scheduled closure), never `open + duration`. Stale-entry rule counts market-open time only. Sizing uses the broker's tick size, tick value and lot step. | PROPOSED (ChatGPT review) |
| D-029 | 2026-09-30 | Structural targets use the NEAREST support/resistance or swing and are skipped if that gives under the minimum R; targets must be strictly beyond the actual entry (else skip). | PROPOSED (ChatGPT review) |
| D-030 | 2026-09-30 | Candle Specification moved to Draft 0.2 (32 pattern sides, up to about 657 strategies). Golden test vectors wait until 0.2 is approved. Superseded in part by D-031/D-032 (0.2.1). | PROPOSED |
| D-031 | 2026-09-30 | Draft 0.2.1: early-setup triggers (Kicker Early, Abandoned Baby Early) are tested on the BID/chart opening price and executed at ask (buy) / bid (sell); S/R and swing targets are computed once at entry from data confirmed at `entry_eligible_time` and frozen for the trade (`zones_prepattern` for location flags kept separate from `zones_at_entry` for targets). | PROPOSED (ChatGPT review) |
| D-032 | 2026-09-30 | Every source-normalized variant that depends on `PIP_SRC_USD` (SRC-PS of Hammer, Shooting Star, Pin Bar, Dragonfly, Gravestone, Bullish/Bearish Engulfing, Inside Bar, Tweezer Top/Bottom) is `DISABLED_PENDING_PIP_CONFIRMATION` until the pip definition is confirmed; BASE strategies and pip-free variants run regardless. | PROPOSED (ChatGPT review) |
| D-033 | 2026-09-30 | `MAX_HOLD = 50` bars of each pattern's own timeframe for all timeframes (W1/MN1 samples will be very slow). Reviewer-approved; owner has not yet stated it. | PROPOSED (ChatGPT review) |

## Open

- Owner's explicit confirmation of the PROPOSED items above.
- `CANDLE_SPEC_V1.md` Draft 0.2.1 (second-pass fixes applied) goes to the reviewer; then golden test vectors, before any code.
- Owner to approve or reject every PROPOSED item (D-006 to D-021 and D-023 to D-033). ChatGPT recommends approving D-006 to D-024 and D-026 to D-033 (D-025 in its reworded form); the owner has not yet said so.
- Owner confirmation of `MAX_HOLD = 50` bars (D-033).
- Confirm `PIP_SRC_USD` (D-032) to enable the disabled SRC-PS variants.
- Validation-stage pass/fail rule (day-block bootstrap, multiple-testing control) to be written before validation.
- Portfolio Simulation rules (position sizing and any exposure cap) - to be defined and approved.
- Vantage demo account created; its symbol/contract/swap/timezone details recorded.
