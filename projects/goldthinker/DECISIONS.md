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

## Open

- Owner's explicit confirmation of the PROPOSED items above.
- `CANDLE_SPEC_V1.md` review (owner + ChatGPT) and golden test vectors before any code.
- What "balance" means on the hub (per-candle virtual balance vs combined portfolio vs the Vantage demo account) - owner to choose.
- Vantage demo account created; its symbol/contract/swap/timezone details recorded.
