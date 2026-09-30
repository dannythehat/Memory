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
pattern, timeframe (15 min to 1 month), reliability, candles ago, timestamp.

- **CORRECTION (owner pasted the raw page, same day):** the earlier extraction said reliability
  values ran from 2 to 67. That was wrong. Those numbers are the **"Candles Ago"** column. In the
  pasted text the **Reliability column is empty** (probably icons/stars that did not copy), so its
  scale is unknown. No hit rate, sample size or backtest is shown anywhere on the page.
- The raw page shows the scanner tagging one candle with several patterns at once, including
  opposite ones (1H candle of Sep 29 02:00: Shooting Star bearish + Inverted Hammer + Three
  Outside Up bullish). Patterns fire constantly and conflict, so any test must report trigger
  frequency and cannot treat a pattern's presence as rare or informative by default.
- Page footer prohibits using, storing or reproducing its data without written permission. Do
  not scrape or store this scanner's output.
- This is the closest thing to the product the owner asked about ("many candle reader apps that
  people love"). It shows what the market sells: an always-on scanner across many timeframes.
- Not usable as a data source: terms forbid storing/reproducing its data. Our own detector on
  our own candles is the only route.

### Source 6 — Pro-Scalper.com, "Evening Star" (2026-09-30)

Site sells XAUUSD Expert Advisors for MetaTrader 5, so it has a commercial interest. Extracted by
a small model, wording not verified. **The most complete rule set so far, but still no evidence.**

- Bearish 3-candle reversal at the top of an uptrend, at resistance. C1 large bullish; C2 small
  "star" that gaps above C1 or opens near its close with minimal range; C3 large red candle that
  closes below the midpoint of C1's body.
- **Entry:** market, at the open after C3 closes. **Stop:** just above C2's high (or above C1's
  high for more room). **Targets:** first at C1's low (close 60% of the position), second at next
  major support. **Risk:reward:** at least 1:2 on H1/H4, up to 1:4+ on daily.
- Typical move claimed: H1 30-80 pips (frequent, noisy), H4 150-300 pips ("one of the cleanest
  short setups"), Daily rare (5-10 a year).
- **No win rate, sample size or backtest anywhere.** "Cleanest" is opinion.
- Testable as written once thresholds are set: "large", "small", "gap" and "at resistance" each
  need a numeric rule. Daily/H4 sample would be tiny on 42 days of data.
- The mirror-image morning star page on the same site likely exists and would pair with this.

### Source 7 — Pro-Scalper.com, "Bullish Engulfing" (2026-09-30)

Same commercial site as source 6 (sells XAUUSD EAs). Extracted by a small model, wording not
verified. **No win rate, sample size or backtest.**

- **Definition:** two candles at the end of a downtrend or at significant support. Candle 1
  bearish; candle 2 opens at or below candle 1's close, closes at or above candle 1's open, and
  its body is larger than candle 1's. Strongest when candle 2 is "two to three times" candle 1.
- **Location:** round numbers (examples quote $2300/$2400/$2500 - stale for gold at ~4,200),
  former swing highs turned support, Fibonacci 61.8% / 78.6%, multi-timeframe confluence.
- **Entry:** at the engulfing candle's close (aggressive) or a pullback to its midpoint
  (conservative). **Stop:** below the lowest wick of either candle plus a 15-25 pip buffer.
  **Targets:** nearest overhead resistance (1.5-2x risk), then a measured move (3-5x risk).
- **Timeframe/session:** H1 and H4; says reliability peaks at London open (08:00-10:00 GMT) and
  New York open (13:00-15:00 GMT).
- Testable pieces: the two entry styles, the size-ratio filter (1x vs 2-3x), and the session
  filter can each be compared against the plain pattern. "Pip" size for gold must be fixed
  (sources 6 and 7 do not define it); "support" and Fibonacci location need numeric rules.
- Overlaps source 1 (engulfing rules), source 3 and source 4 - fix ONE definition.

### Source 8 — Pro-Scalper.com, "Bearish Engulfing" (2026-09-30)

Same commercial site as sources 6-7. Extracted by a small model, wording not verified.
**No win rate, sample size or backtest.**

- **Definition:** candle 2 opens above candle 1's close, closes below candle 1's open, red body
  fully contains the prior green body. After an uptrend or at significant resistance.
- **Location:** round numbers (examples $2000/$2100/$2200 - stale for gold at ~4,200), prior
  all-time highs, Fibonacci extensions 127.2% and 161.8%.
- **Entry:** engulfing candle's close (aggressive) or pullback to its midpoint. **Stop:** above the
  high of the whole two-candle pattern plus a 15-25 pip buffer. **Targets:** nearest support at
  at least 1.5:1; full target is the engulfing candle's height projected down, "3:1 or greater".
- **Timeframes claimed:** H4 "most reliable" (200-500 pips), H1 "most popular" (50-150 pips), M15
  only with strict filtering.
- **Filters that are NOT in the bullish page:** avoid the Asian session (London/NY only); check
  the dollar (DXY) - "patterns fail when dollar weakens"; RSI divergence or a failed breakout for
  counter-trend trades.
- **Worth noting for later:** "avoid the Asian session" sits against our own data, where TIG's
  Asia Trades (Asia-session provider) is the top 30-day performer. Different things (a provider's
  signals vs. a candle pattern) so it proves nothing, but a session filter is testable directly.
- Bullish (source 7) and bearish (source 8) pages are not exact mirrors: the bearish one adds the
  session and DXY filters and uses a different stop rule and target. Test each as written first.

### Source 9 — Pro-Scalper.com, "Hammer Candlestick" (2026-09-30)

Same commercial site as sources 6-8. Extracted by a small model, wording not verified.
**No win rate, sample size or backtest.** The most numeric pattern definition so far.

- **Shape:** lower wick at least 2x the body (strongest at 3-4x); body in the upper third of the
  range but also stated as "upper 40%" (the page's two thresholds differ - pick one before
  testing); upper wick under 20% of the total range.
- **Context:** needs a prior downtrend or a known support; no reversal status without one.
- **Entry:** never on the hammer itself. Wait for the next candle and enter on its open "showing
  initial bullish momentum" (aggressive) or on a pullback into the upper half of the hammer body
  (conservative). **Look-ahead trap:** "initial momentum" cannot be known at the open, so a
  backtest must define it with data available at entry (e.g. next bar closes above the hammer's
  high, entering the bar after) or it will overstate results.
- **Stop:** below the hammer's low plus a 15-20 pip buffer (spread/stop-hunt). **Target:** 2:1
  minimum.
- **Timeframes:** M5 only with tight H1/H4 support confluence (10-25 pip target, 5-8 pip stop);
  H1 the "sweet spot" (50-120 pip target, 20-35 pip stop); D1 200-800 pips over days to weeks.
- Overlaps sources 1, 3, 4 (hammer / hanging man). Fix ONE definition; the numeric one here is
  the best candidate.

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
