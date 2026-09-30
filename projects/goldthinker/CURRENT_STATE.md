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

## Source material collected so far

TradingView education post "Top 5 Best Candlestick Patterns for Gold XAUUSD Trading"
(Aug 12). Article text as extracted (small-model summary, wording not verified verbatim):

| Pattern | Article rules |
|---|---|
| Doji | Not an entry signal; sentiment context only |
| Rejection candle | Long wicks mark support/resistance; no entry/stop/target |
| High-momentum candle | Large body, tiny wicks, large vs preceding candles; no entry/stop/target |
| Engulfing | Enter at close of engulfing candle; stop beyond its extreme (low for buys, high for sells). Bearish text says "close above" — likely a typo for below |
| Inside bar | 3+ candles; mother bar; enter on close outside mother bar range; stop at far side of mother bar |

Article gives **no take-profit, no timeframe (only an hourly example), no win rates.** Any
result therefore depends on choices we make. The article's thumbnail also shows 12 classic
patterns (morning/evening star, harami, engulfing, tweezer top/bottom, hammer, hanging man,
inverted hammer, shooting star) — a different list from the article body.

### Source 2 — FTMO Academy, "Bollinger Bands: Calculation & Trading Strategies" (2026-09-30)

Extracted (small-model summary, not verbatim). Bands = SMA(20) ± 2 standard deviations; multiplier
adjustable (says at least 2.1 for a 50-period average, below 2 for shorter periods).

| Strategy | Article rules |
|---|---|
| Squeeze breakout | Both bands squeezed, then a break of one band: upper break = long, lower break = short. "Squeeze" is not quantified. No stop, exit or target. |
| Band-touch reversal | Touch of a band, then wait for a confirming candle (bearish after upper touch, bullish after lower touch). No stop, exit or target. |

Article's own caveats: a band touch is not an automatic signal, price can stay outside the bands
in strong trends, and it recommends confirming with VWAP, RSI, ATR or price action. **No
win rates or performance claims.** It is a prop-firm education page reached via a paid ad, so
treat it as marketing-adjacent teaching material, not evidence. The formula is described in
"days", so the daily-chart setup is not testable on our ~42 days of data; intraday versions
would be our own extension, not the article's.

Both strategies here are direction-of-move opposites (breakout follows the break, reversal
fades the touch), so a backtest must treat them as separate hypotheses. "Squeeze" needs a
fixed numeric definition (e.g. bandwidth percentile) before it can be tested.

### Source 3 — Seeking Alpha blog, "Bullish Reversal Candlestick Patterns" (Michael Battat, 2026-09-30)

Extracted (small-model summary, not verbatim). Four bullish reversal patterns, all described
for **stocks on daily candles**, not gold or intraday:

| Pattern | Article definition |
|---|---|
| Bullish engulfing | Small down candle "engulfed" by a large up candle; best in a downtrend |
| Hammer | Small body, shadow at least 2x the body, at the end of a downtrend; same shape in an uptrend is a hanging man (bearish). Wants a close near the high, and higher volume |
| Bullish harami | Large red candle followed by a smaller candle inside its range; downtrend; says bullish version is "much more reliable" than bearish |
| Piercing | Second candle opens below the first (gap down) and closes above the first's midpoint |

Suggested confirmation: pattern at support (moving averages, Fibonacci, round numbers), plus
momentum (stochastics, RSI), oversold readings or divergence. **No entry, stop or target rules, no
statistics, no backtest.** The author says patterns only "augment a trader's outlook". Volume
confirmation is not usable for spot XAUUSD (tick volume only).

Testing notes: piercing requires a gap, and gold M1-M60 candles rarely gap outside the weekend
open, so it needs an adapted definition (e.g. open below prior close by X) or should be dropped.
"Downtrend" and "at support" are undefined and would each need a numeric rule. Bullish-only
article: a fair test needs the mirrored bearish versions too. Overlaps with source 1 (engulfing,
hammer, harami), so those definitions should be fixed once, not per source.

### Source 4 — "Trading in Gold" notes by Shankar A.G. (Scribd doc, owner-supplied .docx, 2026-09-30)

Read in full (25k characters of text; the docx also embeds ~18+ chart images that were not
inspected). A personal discretionary playbook for gold: reads XAUUSD (OANDA) for levels and
places orders in MCX GoldMini futures (India). **Author is a hobbyist; document contains no
statistics, no backtest and no P&L evidence.** It is the first source that describes a whole
method, not just pattern shapes.

**Framework it describes**
- Three timeframe pairs: 4H levels/trend + 1H entries (major swings); 1H + 15m (minor);
  15m + 5m (very minor). "Always trade in the direction of the trend" of the higher timeframe,
  judged by higher-highs/higher-lows vs lower-highs/lower-lows.
- Support/resistance by eye: swing-high tips (wicks matter more than closes), two or more
  medium/large swings at one level, psychological levels in multiples of 50 (e.g. 3100, 3150),
  and a level is invalid if price cuts it 2-3 times.
- Breakout: medium/big candle with most of its body beyond the line, little wick, and a volume
  surge.

**Patterns (about 19) and their confirmation stacks**
Bullish: engulfing, harami (+cross), morning star (+doji), piercing line, hammer, inverted
hammer, three white soldiers, dragonfly doji. Bearish: engulfing, harami, evening star (+doji),
hanging man, dark cloud cover, shooting star, three black crows, gravestone doji. Neutral:
inside bar, marubozu, doji. Each has a required prior trend (down for bullish reversals, up for
bearish) and a stack of extras: RSI below 30 or above 70 (or divergence), MACD colour, higher
volume, Bollinger band proximity, a moving-average touch (20 EMA on 15m, 5 or 9 EMA on 5m, 50
EMA on 1H), and a follow-up candle closing beyond the pattern.

**Only explicit entries:** bullish engulfing = enter at its close; morning star = buy on a break
above the 3rd candle's high; evening star = short below the 3rd candle's low; inside bar = break
of the high/low. Other patterns: wait for a confirming next candle. **Stops:** only morning star
(below the star candle). **Targets and position sizing: none.**

**Testing implications (Claude's read, not agreed)**
- Much of it is unrulable as written: hand-drawn trendlines/levels, "medium to large" candles,
  "quiet bigger", volume (spot XAUUSD has tick volume only; the doc is written for stocks and
  futures). Every one of those needs an arbitrary number, and each choice is a chance to fit
  the past. Fewer rules = safer test.
- The most testable coherent reading: **higher-timeframe trend filter + lower-timeframe reversal
  pattern back in the trend's direction + RSI extreme + confirming candle close.** That is my
  interpretation of "trade with the higher-timeframe trend" combined with counter-move patterns;
  the doc does not say it this way and the owner should confirm.
- 19 patterns x several confirmations x 3 timeframe pairs is hundreds of variants; the
  multiple-testing correction will be harsh, so pre-register a short list.
- Overlaps sources 1 and 3 (engulfing, harami, hammer, stars, inside bar): fix one definition
  each.

### Source 5 — Investing.com gold candlestick page (a real "candle reader" product, 2026-09-30)

`investing.com/commodities/gold-candlestick`: live Gold futures chart (GCZ6, ~4,205 at fetch time)
with an automatic pattern scanner (extracted by a small model, wording not verified). Table of
about 60 detected patterns per view (Hanging Man, Morning Star, Bullish Engulfing, etc.), columns:
pattern, timeframe (15 min to 1 month), **"reliability" rating** (values seen from 2 to 67),
candles ago, timestamp.

- The reliability number is **not defined on the page** as fetched, and no hit rate, sample size
  or backtest is shown. Do not assume it is a measured win rate.
- This is the closest thing to the product the owner asked about ("many candle reader apps that
  people love"). It shows what the market sells: an always-on scanner across many timeframes.
- Possible later use: its output could be checked against what price actually did next, as an
  outside benchmark for our own pattern tests. Not attempted; scraping or reusing its data would
  need the site's terms checked first.

Owner is continuing to collect research. **Do not run backtests until the owner says the
research phase is done and the rules are confirmed.**

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
