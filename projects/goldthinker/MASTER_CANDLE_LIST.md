# GoldThinker — Master candle list (draft for owner review)

Built 2026-09-30 from all 13 research sources. **40 candle types; 51 direction-specific versions**
once bullish and bearish are counted separately (matches the owner's "around 50").

Rules below are what the sources say, not decided. Sources: PS = Pro-Scalper.com pages (vendor of
MT5 gold EAs; extracts by a small model, not verbatim), TV = TradingView post, SA = Seeking Alpha,
SH = Shankar A.G. notes, INV = Investing.com scanner (names only). **No source gives results data.**
"Confirm" = a confirmation candle the source requires; it must be defined using only information
known at entry.

Plan status: **FULL** = a source gives entry + stop + target. **PARTIAL** = shape and/or some of
entry/stop/target. **NONE** = only the name is known; rules still to be gathered.

Counts: 21 FULL, 10 PARTIAL, 9 NONE.

## Single-candle

| # | Candle | Side | Shape (source numbers) | Trade plan (source) | Status | Src |
|---|---|---|---|---|---|---|
| 1 | Hammer | bull | Lower wick >= 2x body (best 3-4x); body in upper third **and** "upper 40%" (source disagrees); upper wick < 20% of range; after downtrend / at support | Confirm; enter confirmation open, or pullback into upper half of body; stop below low + 15-20 pips; target >= 2:1 | FULL | PS TV SA SH |
| 2 | Hanging Man | bear | Hammer shape after an uptrend | Confirm bearish next candle; RSI > 70; MA entry (SH). No stop/target given | PARTIAL | TV SH INV |
| 3 | Inverted Hammer | bull | Mirror of hammer after downtrend | Confirm: next candle bullish, closes higher; RSI < 30. No stop/target | PARTIAL | TV SH INV |
| 4 | Shooting Star | bear | Body in lower third; upper wick >= 2x body (best 3-4x); little/no lower wick; after uptrend / at resistance | Confirm; enter on confirmation close or retest; stop above wick high + 15-25 pips; T1 swing low, T2 rally origin; >= 1.5:1; skip/shrink Asian | FULL | PS TV SH |
| 5 | Pin Bar | both | Wick >= 2/3 of range; body < 1/3; body inside prior candle's range; at key S/R | Enter next open, or 50% retrace of wick; stop 10-15 pips beyond wick tip; T1 swing, T2 = pin range; >= 1:2; best London/NY open | FULL | PS |
| 6 | Doji | neutral | Open ~ close; **no numeric threshold** | Trade the confirmation candle; stop beyond doji wick; target next S/R >= 1.5:1; ignore Asian doji | PARTIAL | PS SH TV |
| 7 | Long-legged Doji | neutral | Very long wicks both sides, tiny body | Same as doji | PARTIAL | PS SH |
| 8 | Dragonfly Doji | bull | Open = close = high; lower wick >= 2-3x body (best 5-10x); at support tested >= 2x; H4/D1 matter more | Confirm: next candle closes bullish above dragonfly level; or buy limit at level; stop below wick low + 5-15 pips; >= 1:1.5; avoid Asia and +-30 min of CPI/NFP/FOMC | FULL | PS SH |
| 9 | Gravestone Doji | bear | Open = close = low; long upper wick; ~zero body (vs shooting star's visible body) | Confirm: next close below level; short at next open or sell limit at level; stop above wick high + 5-15 pips; >= 1:1.5 | FULL | PS SH |
| 10 | Spinning Top | neutral | Body ~10-20% of range, roughly equal wicks | Not traded alone; wait for confirm; clusters -> breakout above/below cluster; 1:3 from breakout; no stop numbers | PARTIAL | PS |
| 11 | Marubozu | both | No wicks (2-5% of body tolerated); full / opening / closing types | Do not chase; pullback entry 20-40% retrace (Fib 38.2/50/61.8); wait 15-30 min after news. **No stop or target** | PARTIAL | PS SH |
| 12 | Belt Hold | both | Name only (INV scanner) | - | NONE | INV |

## Two-candle

| # | Candle | Side | Shape | Trade plan | Status | Src |
|---|---|---|---|---|---|---|
| 13 | Bullish Engulfing | bull | C1 bearish; C2 opens <= C1 close, closes >= C1 open, larger body (best 2-3x); at support/Fib/round number. SH adds: wicks engulfed, RSI < 30 | Enter engulfing close, or pullback to midpoint; stop below lowest wick of either candle + 15-25 pips; T1 nearest resistance (1.5-2x), T2 measured move (3-5x) | FULL | PS TV SH SA |
| 14 | Bearish Engulfing | bear | Mirror; at resistance/round/Fib extensions | Enter engulfing close or midpoint pullback; stop above both candles + 15-25 pips; T1 support (>= 1.5:1), full = candle height projected (3:1); DXY check; avoid Asia | FULL | PS TV SH |
| 15 | Outside Bar | both | High > prior high AND low < prior low; size 1.5-2x ATR | Enter next open after close; stop beyond bar's opposite wick; target next S/R 1.5-2R; wait 1-2 candles after news spikes; no extra confirm | FULL | PS |
| 16 | Inside Bar | both | High strictly < mother high, low strictly > mother low; 30-50% of mother range = strong compression | Buy stop 2-5 pips above mother high (or short below low), stop 2-5 pips beyond other side; wait for a **close** outside range (source states both); >= 1:1.5; H1+; avoid Asia, M5, pre-news | FULL | PS TV SH |
| 17 | Harami | both | C2 body fully inside C1 body, opposite colours, wicks may exit | Enter after 3rd candle closes beyond harami body; stop beyond C1 extreme; **no target**; M5/M15 "unreliable", H4 "sweet spot" | PARTIAL | PS SH SA |
| 18 | Harami Cross | both | Harami whose C2 is a doji; "stronger" | As harami | PARTIAL | PS SH INV |
| 19 | Tweezer Top | bear | Two highs within 2-5 pips; C1 bullish, C2 bearish closing near/below C1 midpoint; at resistance in uptrend | Enter below C2 low after close (or 3rd open/pullback); stop a few pips above both highs; T1 nearest support; London/NY overlap best | FULL | PS |
| 20 | Tweezer Bottom | bull | Two lows within 1-5 pips; C1 bearish near low, C2 bullish near high; at support | Enter above C2 high after close; stop a few pips below both lows; target prior swing high | FULL | PS |
| 21 | Piercing Line | bull | C1 large bearish; C2 opens below C1 close (gap strengthens), closes above 50% of C1 body (75% strong, 90%+ near-engulfing) | Enter C2 close or C3 open; stop below C2 low; T1 resistance, T2 measured move; min 1:2; best at London/NY open after Asian weakness | FULL | PS SA SH |
| 22 | Dark Cloud Cover | bear | C1 large bullish; C2 opens above prior close (gap required), closes below C1 body midpoint | Enter C2 close or C3 open; stop above C2 high; targets prior support then trend swing low; scale out half | FULL | PS SH |
| 23 | Kicker | both | C2 opens at ~C1's **open**, gap; C1 large opposite colour; C2 closes near its extreme | Enter C2 open; stop beyond C1's far extreme; target prior swing; daily most reliable, H4 moderate, H1 weak, **M15 and below "almost never worth trading"** | FULL | PS |
| 24 | Doji Star | both | Name only (INV) | - | NONE | INV |

## Three-candle

| # | Candle | Side | Shape | Trade plan | Status | Src |
|---|---|---|---|---|---|---|
| 25 | Morning Star | bull | C1 large bearish; C2 small star (any colour); C3 large bullish closing above C1 body midpoint; at support/Fib; RSI < 30 adds weight | Enter C3 close (execute next open); stop tight below C2 low or wide below C1 low (30-60 pips); T1 C1 high (take 60%), T2 next swing high; >= 1:2 | FULL | PS TV SH SA |
| 26 | Morning Doji Star | bull | Morning star with a doji as C2 | As morning star | PARTIAL | SH INV |
| 27 | Evening Star | bear | C1 large bullish; C2 small star (gap up or near C1 close); C3 large red closing below C1 midpoint | Enter open after C3; stop above C2 high (or C1 high); T1 C1 low (60%), T2 support; >= 1:2 | FULL | PS TV SH |
| 28 | Evening Doji Star | bear | Evening star with a doji as C2 | As evening star | PARTIAL | SH |
| 29 | Three White Soldiers | bull (cont.) | Three bullish candles, each opens in prior body, closes near high, similar substantial bodies (no ratios) | Enter pullback to 3rd body or breakout above 3rd high; stop below 3rd low (pullback) or below post-pattern consolidation; target = pattern height added to 3rd high; scale out 50%; caution RSI > 75-80, resistance within 50 pips, after 15-20 candle run | FULL | PS SH |
| 30 | Three Black Crows | bear (cont.) | Three red candles, each opens in prior body, closes near low | Retracement entry (short the bounce, stop above bounce high) or breakdown below 3rd low after consolidation; target = pattern height projected down, then support; check weekly trend, DXY; avoid RSI < 25 | FULL | PS SH |
| 31 | Abandoned Baby | both | C1 large; C2 doji gapping away (no overlap incl. shadows); C3 large opposite, also gapping | Enter C3 open; stop beyond doji extreme; target prior swing; RSI <= 30 / >= 70. **Daily XAUUSD 2-4 times a year; weekly 1-2** | FULL | PS |
| 32 | Three Inside Up | bull | Name only | - | NONE | INV SH |
| 33 | Three Inside Down | bear | Name only | - | NONE | INV |
| 34 | Three Outside Up | bull | Name only | - | NONE | INV |
| 35 | Three Outside Down | bear | Name only | - | NONE | INV |
| 36 | Three Line Strike | both | Name only | - | NONE | INV |
| 37 | Advance Block | bear | Name only | - | NONE | INV |

## Five-candle / gap

| # | Candle | Side | Shape | Trade plan | Status | Src |
|---|---|---|---|---|---|---|
| 38 | Rising Three Methods | bull (cont.) | C1 large bullish; C2-4 small bearish, none closes outside C1's range; C5 large bullish closing above C1 close | Enter C5 close / C6 open; stop below lowest wick of C2-4; T1 1.272 Fib extension, T2 1.618; >= 1:2 | FULL | PS INV |
| 39 | Falling Three Methods | bear (cont.) | Mirror; no middle wick above C1 high | Enter C5 close / C6 open; stop above highest high of C2-4; T1 1.272 ext, T2 1.618 or prior lows; check DXY | FULL | PS |
| 40 | Upside Gap Three Methods | bull (cont.) | Name only | - | NONE | INV |

## Shared definitions to settle BEFORE any candle is coded

Every row above leans on these; each one needs one fixed value, chosen once, or two candles that
"agree" will still behave differently:
1. **Pip:** what is a gold pip on Vantage XAUUSD? (PS quotes "30-80 pips" for a typical H1 move,
   which implies $0.10, but this is unconfirmed.) All "15-25 pip buffer" style rules depend on it.
2. **Trend:** how "downtrend/uptrend" is decided (and on which timeframe).
3. **Key level / support / resistance:** the numeric rule for "at support", round numbers,
   Fibonacci levels.
4. **Large / small candle:** e.g. a multiple of ATR (PS uses 1.5-2x ATR for outside bars).
5. **Confirmation candle:** exact test, using only information known at entry.
6. **Session windows:** Asian is written 22:00-07:00, 23:00-07:00 and 23:00-08:00 GMT; pick one.
7. **News blackout:** window around CPI/NFP/FOMC (sources say +-30 min, or 30-60 min before).
8. **Gaps:** continuous spot gold rarely gaps intraday (weekend open and news are the exceptions),
   so gap-dependent candles (Kicker, Abandoned Baby, Piercing, Dark Cloud, Evening/Morning Star gap
   versions) will fire rarely on short timeframes. Need a rule for "gap".
9. **Partial exits:** several plans scale out (40-60% at first target); the paper engine must model
   that.
10. **Overlapping signals:** if several candles fire at once at 1% each, risk stacks. Owner said
    trigger "each and every one"; how simultaneous exposure is recorded/limited is undecided.

## Conflicts between sources found so far (owner to settle per candle)

- Hammer body: "upper third" vs "upper 40%" (same PS page).
- Inside bar entry: buy/sell stop beyond the mother bar vs waiting for a candle **close** outside.
- Bullish engulfing: PS (body engulf) vs SH (body **and wicks**, RSI < 30, 3rd candle closes above).
- Harami: SA/SH want a confirming later candle and a prior trend; PS wants confirmation and H4.
- Timeframe advice differs by candle (Kicker: not below H4; Harami: not M5/M15; Inside bar: not M5).
  Owner chose all timeframes, so these become claims the paper results can check.
