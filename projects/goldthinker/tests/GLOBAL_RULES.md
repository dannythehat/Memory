# Global rule vectors

Series/function vectors for the shared definitions (G0-G13). A wrong global rule corrupts every pattern, so each is tested on its own with exact inputs. `in` is the input; `out` the exact expected result.

#### `GV-G-ATR-01` · atr
> G1: ATR = simple mean of True Range over the 14 completed bars ending at i0-1 (needs 15 bars before i0). Constant TR = 4.00 bars (down bars H-L 4.00 with |L-Cprev| 3.50; up bars mirrored): ATR must be exactly 4.00.

| # | in | expected out |
|---|---|---|
| 1 | `{"bars":"[15 bars: first ['4200.00', '4200.50', '4196.50', '4197.00'] ... last ['4200.00', '4200.50', '4196.50', '4197.00']; full series in golden_vectors.json]","i0":15}` | `{"status":"OK","atr":"4.00"}` |

#### `GV-G-ATR-02` · atr
> Only 14 completed bars before i0: warm-up needs 15 -> NOT_EVALUATED_WARMUP.

| # | in | expected out |
|---|---|---|
| 1 | `{"bars":"[14 bars: first ['4200.00', '4200.50', '4196.50', '4197.00'] ... last ['4197.00', '4200.50', '4196.50', '4200.00']; full series in golden_vectors.json]","i0":14}` | `{"status":"NOT_EVALUATED_WARMUP"}` |

#### `GV-G-ATR-03` · atr
> Varied TR values (sum 57): ATR = 57/14 = 4.0714285... It is NOT terminating, so implementations must state their rounding rule; the vector records the exact rational. [Spec gap A-22: no numeric-precision/rounding rule is given.]

| # | in | expected out |
|---|---|---|
| 1 | `{"bars":"[15 bars: first ['4200.00', '4200.00', '4200.00', '4200.00'] ... last ['4200.00', '4202.50', '4197.50', '4200.00']; full series in golden_vectors.json]","i0":15}` | `{"status":"OK","atr":"57/14"}` |

#### `GV-G-ATR-04` · atr
> The candidate bar never influences its own ATR: with a 50-point-range bar at index 15 the ATR at i0=15 is still 4.00; at i0=16 (one bar later) that bar is history and the ATR becomes (13*4 + 50)/14 = 51/7.

| # | in | expected out |
|---|---|---|
| 1 | `{"bars":"[16 bars: first ['4200.00', '4200.50', '4196.50', '4197.00'] ... last ['4197.00', '4222.00', '4172.00', '4197.00']; full series in golden_vectors.json]","i0":15}` | `{"status":"OK","atr":"4.00"}` |
| 2 | `{"bars":"[16 bars: first ['4200.00', '4200.50', '4196.50', '4197.00'] ... last ['4197.00', '4222.00', '4172.00', '4197.00']; full series in golden_vectors.json]","i0":16}` | `{"status":"OK","atr":"51/7"}` |

#### `GV-G-ATR-05` · atr
> True Range uses the previous close: the last bar gaps up (prev close 4197..., open +10): H-L is only 1.50 but |H-Cprev| = 11.00, so TR = 11.00. ATR = (13*4 + 11)/14 = 63/14 = 4.50.

| # | in | expected out |
|---|---|---|
| 1 | `{"bars":"[15 bars: first ['4200.00', '4200.50', '4196.50', '4197.00'] ... last ['4210.00', '4211.00', '4209.50', '4210.50']; full series in golden_vectors.json]","i0":15}` | `{"status":"OK","atr":"4.50"}` |

#### `GV-G-CAL-01` · cal
> Bar completion (G0): a bar completes at the EARLIER of the next bar's open and the start of a scheduled closure covering the rest of the bar - never open + duration. TEST CALENDAR FIXTURE (not Vantage's real calendar, which is still 'TO CONFIRM'): market open Sun 23:00 UTC - Fri 22:00 UTC; daily pause Mon-Thu 22:00-23:00 UTC; server time UTC+1. Intraday.

| # | in | expected out |
|---|---|---|
| 1 | `{"tf":"M1","open":"2026-09-16T12:00:00Z"}` | `{"complete":"2026-09-16T12:01:00Z"}` |
| 2 | `{"tf":"M1","open":"2026-09-16T21:59:00Z"}` | `{"complete":"2026-09-16T22:00:00Z"}` |
| 3 | `{"tf":"M1","open":"2026-09-18T21:59:00Z"}` | `{"complete":"2026-09-18T22:00:00Z"}` |
| 4 | `{"tf":"M5","open":"2026-09-17T21:55:00Z"}` | `{"complete":"2026-09-17T22:00:00Z"}` |
| 5 | `{"tf":"M15","open":"2026-09-16T21:45:00Z"}` | `{"complete":"2026-09-16T22:00:00Z"}` |
| 6 | `{"tf":"M30","open":"2026-09-16T21:30:00Z"}` | `{"complete":"2026-09-16T22:00:00Z"}` |
| 7 | `{"tf":"H1","open":"2026-09-16T21:00:00Z"}` | `{"complete":"2026-09-16T22:00:00Z"}` |
| 8 | `{"tf":"H1","open":"2026-09-16T23:00:00Z"}` | `{"complete":"2026-09-17T00:00:00Z"}` |
| 9 | `{"tf":"H1","open":"2026-09-18T21:00:00Z"}` | `{"complete":"2026-09-18T22:00:00Z"}` |

#### `GV-G-CAL-02` · cal
> Higher timeframes: the H4 bar opening 19:00 covers the daily pause, so it completes at 22:00 (closure start), NOT at 23:00 (open + 4h). The D1 bar opening Sunday 23:00 completes Monday 22:00, not Monday 23:00. The W1 bar completes Friday 22:00; open + 7 days would be the following Sunday 23:00. A month bar completes at the last closure start of the month.

| # | in | expected out |
|---|---|---|
| 1 | `{"tf":"H4","open":"2026-09-16T19:00:00Z"}` | `{"complete":"2026-09-16T22:00:00Z"}` |
| 2 | `{"tf":"H4","open":"2026-09-16T15:00:00Z"}` | `{"complete":"2026-09-16T19:00:00Z"}` |
| 3 | `{"tf":"H4","open":"2026-09-16T23:00:00Z"}` | `{"complete":"2026-09-17T03:00:00Z"}` |
| 4 | `{"tf":"H4","open":"2026-09-18T19:00:00Z"}` | `{"complete":"2026-09-18T22:00:00Z"}` |
| 5 | `{"tf":"D1","open":"2026-09-13T23:00:00Z"}` | `{"complete":"2026-09-14T22:00:00Z"}` |
| 6 | `{"tf":"D1","open":"2026-09-17T23:00:00Z"}` | `{"complete":"2026-09-18T22:00:00Z"}` |
| 7 | `{"tf":"W1","open":"2026-09-13T23:00:00Z"}` | `{"complete":"2026-09-18T22:00:00Z"}` |
| 8 | `{"tf":"MN1","open":"2026-08-31T23:00:00Z"}` | `{"complete":"2026-09-30T22:00:00Z"}` |
| 9 | `{"tf":"MN1","open":"2026-09-30T23:00:00Z"}` | `{"complete":"2026-10-30T22:00:00Z"}` |

#### `GV-G-CAL-03` · oe
> open_elapsed(a,b) = time from a to b EXCLUDING scheduled closures; feed outages while the market is open DO count. Stale entry when open_elapsed > 15 min.

| # | in | expected out |
|---|---|---|
| 1 | `{"a":"2026-09-18T21:59:00Z","b":"2026-09-20T23:00:30Z"}` | `{"open_elapsed_s":90,"stale":false}` |
| 2 | `{"a":"2026-09-18T22:00:00Z","b":"2026-09-20T23:15:00Z"}` | `{"open_elapsed_s":900,"stale":false}` |
| 3 | `{"a":"2026-09-18T22:00:00Z","b":"2026-09-20T23:15:01Z"}` | `{"open_elapsed_s":901,"stale":true}` |
| 4 | `{"a":"2026-09-14T21:55:00Z","b":"2026-09-14T23:05:00Z"}` | `{"open_elapsed_s":600,"stale":false}` |
| 5 | `{"a":"2026-09-16T10:00:00Z","b":"2026-09-16T10:20:00Z"}` | `{"open_elapsed_s":1200,"stale":true}` |
| 6 | `{"a":"2026-09-16T10:00:00Z","b":"2026-09-16T10:15:00Z"}` | `{"open_elapsed_s":900,"stale":false}` |
| 7 | `{"a":"2026-09-16T10:00:00Z","b":"2026-09-16T10:15:01Z"}` | `{"open_elapsed_s":901,"stale":true}` |
| 8 | `{"a":"2026-09-15T22:00:00Z","b":"2026-09-15T22:59:59Z"}` | `{"open_elapsed_s":0,"stale":false}` |
| 9 | `{"a":"2026-09-17T21:50:00Z","b":"2026-09-17T23:10:00Z"}` | `{"open_elapsed_s":1200,"stale":true}` |

#### `GV-G-CAL-04` · seriesgap
> Data integrity (G0): a pattern is evaluated only if all its bars exist with no UNEXPLAINED gap; scheduled closures are allowed and tagged across_break; otherwise NOT_EVALUATED_DATA_GAP.

| # | in | expected out |
|---|---|---|
| 1 | `{"tf":"M15","opens":["2026-09-16T10:00:00Z","2026-09-16T10:15:00Z","2026-09-16T10:30:00Z"]}` | `{"status":"OK","across_break":[]}` |
| 2 | `{"tf":"M15","opens":["2026-09-16T10:00:00Z","2026-09-16T10:30:00Z"]}` | `{"status":"NOT_EVALUATED_DATA_GAP","across_break":[]}` |
| 3 | `{"tf":"M15","opens":["2026-09-18T21:30:00Z","2026-09-18T21:45:00Z","2026-09-20T23:00:00Z"]}` | `{"status":"OK","across_break":[2]}` |
| 4 | `{"tf":"M15","opens":["2026-09-16T21:45:00Z","2026-09-16T23:00:00Z"]}` | `{"status":"OK","across_break":[1]}` |
| 5 | `{"tf":"H1","opens":["2026-09-18T20:00:00Z","2026-09-18T21:00:00Z","2026-09-20T23:00:00Z"]}` | `{"status":"OK","across_break":[2]}` |
| 6 | `{"tf":"H1","opens":["2026-09-18T21:00:00Z","2026-09-21T00:00:00Z"]}` | `{"status":"NOT_EVALUATED_DATA_GAP","across_break":[]}` |
| 7 | `{"tf":"H4","opens":["2026-09-16T15:00:00Z","2026-09-16T19:00:00Z","2026-09-16T23:00:00Z"]}` | `{"status":"OK","across_break":[2]}` |
| 8 | `{"tf":"H4","opens":["2026-09-16T19:00:00Z","2026-09-17T03:00:00Z"]}` | `{"status":"NOT_EVALUATED_DATA_GAP","across_break":[]}` |

#### `GV-G-CLS-01` · class
> G2 LARGE = B>=0.60*ATR AND R>=0.80*ATR AND B/R>=0.60 (ATR 4: B>=2.40, R>=3.20). Each clause exactly on its boundary and 0.01 beyond.

| # | in | expected out |
|---|---|---|
| 1 | `{"bar":["4210.00","4210.60","4207.00","4207.60"],"atr":"4"}` | `{"LARGE":true,"SMALL":false,"DOJI":false}` |
| 2 | `{"bar":["4210.00","4210.60","4207.00","4207.61"],"atr":"4"}` | `{"LARGE":false,"SMALL":false,"DOJI":false}` |
| 3 | `{"bar":["4210.00","4210.20","4207.00","4207.00"],"atr":"4"}` | `{"LARGE":true,"SMALL":false,"DOJI":false}` |
| 4 | `{"bar":["4210.00","4210.19","4207.00","4207.00"],"atr":"4"}` | `{"LARGE":false,"SMALL":false,"DOJI":false}` |
| 5 | `{"bar":["4210.00","4211.00","4206.00","4207.00"],"atr":"4"}` | `{"LARGE":true,"SMALL":false,"DOJI":false}` |
| 6 | `{"bar":["4210.00","4211.01","4206.00","4207.00"],"atr":"4"}` | `{"LARGE":false,"SMALL":false,"DOJI":false}` |

#### `GV-G-CLS-02` · class
> G2 SMALL = B<=0.25*ATR AND R<=0.60*ATR (ATR 4: B<=1.00, R<=2.40); DOJI = B<=0.05*R. R=0 bars are never LARGE, SMALL or DOJI.

| # | in | expected out |
|---|---|---|
| 1 | `{"bar":["4203.00","4204.20","4202.00","4204.00"],"atr":"4"}` | `{"LARGE":false,"SMALL":true,"DOJI":false}` |
| 2 | `{"bar":["4203.00","4204.21","4202.00","4204.01"],"atr":"4"}` | `{"LARGE":false,"SMALL":false,"DOJI":false}` |
| 3 | `{"bar":["4203.00","4204.40","4202.00","4203.40"],"atr":"4"}` | `{"LARGE":false,"SMALL":true,"DOJI":false}` |
| 4 | `{"bar":["4203.00","4204.41","4202.00","4203.40"],"atr":"4"}` | `{"LARGE":false,"SMALL":false,"DOJI":false}` |
| 5 | `{"bar":["4200.00","4210.00","4190.00","4200.50"],"atr":"4"}` | `{"LARGE":false,"SMALL":false,"DOJI":true}` |
| 6 | `{"bar":["4200.00","4210.00","4190.00","4201.01"],"atr":"4"}` | `{"LARGE":false,"SMALL":false,"DOJI":false}` |
| 7 | `{"bar":["4200.00","4200.00","4200.00","4200.00"],"atr":"4"}` | `{"LARGE":false,"SMALL":false,"DOJI":false}` |

#### `GV-G-CLS-03` · class
> Size classes scale with ATR: the same 2.40-body bar is LARGE at ATR 4 (0.6*4 = 2.40) but at ATR 5 needs B >= 3.00 and R >= 4.00.

| # | in | expected out |
|---|---|---|
| 1 | `{"bar":["4210.00","4210.60","4207.00","4207.60"],"atr":"4"}` | `{"LARGE":true,"SMALL":false,"DOJI":false}` |
| 2 | `{"bar":["4210.00","4210.60","4207.00","4207.60"],"atr":"5"}` | `{"LARGE":false,"SMALL":false,"DOJI":false}` |
| 3 | `{"bar":["4210.00","4210.50","4206.50","4207.00"],"atr":"5"}` | `{"LARGE":true,"SMALL":false,"DOJI":false}` |

#### `GV-G-GP-01` · gapthr
> G5 gap threshold = max($0.10, 0.05*ATR): the fixed floor dominates below ATR 2, the ATR term above it.

| # | in | expected out |
|---|---|---|
| 1 | `{"atr":"0.5"}` | `{"thr":"0.10"}` |
| 2 | `{"atr":"1"}` | `{"thr":"0.10"}` |
| 3 | `{"atr":"2"}` | `{"thr":"0.10"}` |
| 4 | `{"atr":"4"}` | `{"thr":"0.20"}` |
| 5 | `{"atr":"8"}` | `{"thr":"0.40"}` |
| 6 | `{"atr":"16"}` | `{"thr":"0.80"}` |
| 7 | `{"atr":"100"}` | `{"thr":"5.00"}` |

#### `GV-G-GP-02` · gap
> Gap test: bullish L_b >= H_a + thr, bearish H_b <= L_a - thr. Prior bar H 4201.00 / L 4199.00.

| # | in | expected out |
|---|---|---|
| 1 | `{"a":["4200.00","4201.00","4199.00","4200.50"],"b":["4201.30","4203.00","4201.20","4202.00"],"atr":"4","dir":"BULL"}` | `{"gap":true,"thr":"0.20"}` |
| 2 | `{"a":["4200.00","4201.00","4199.00","4200.50"],"b":["4201.30","4203.00","4201.19","4202.00"],"atr":"4","dir":"BULL"}` | `{"gap":false,"thr":"0.20"}` |
| 3 | `{"a":["4200.00","4201.00","4199.00","4200.50"],"b":["4198.70","4198.80","4197.00","4197.50"],"atr":"4","dir":"BEAR"}` | `{"gap":true,"thr":"0.20"}` |
| 4 | `{"a":["4200.00","4201.00","4199.00","4200.50"],"b":["4198.71","4198.81","4197.00","4197.50"],"atr":"4","dir":"BEAR"}` | `{"gap":false,"thr":"0.20"}` |
| 5 | `{"a":["4200.00","4201.00","4199.00","4200.50"],"b":["4201.50","4203.00","4201.40","4202.00"],"atr":"8","dir":"BULL"}` | `{"gap":true,"thr":"0.40"}` |
| 6 | `{"a":["4200.00","4201.00","4199.00","4200.50"],"b":["4201.50","4203.00","4201.39","4202.00"],"atr":"8","dir":"BULL"}` | `{"gap":false,"thr":"0.40"}` |

#### `GV-G-NW-01` · news
> G6 news windows (interior points): F_NEWS_HIGH blocks T-30..T+15 around any HIGH-impact USD event; F_NEWS_MAJOR blocks T-60..T+30 around NFP, CPI, FOMC decision, FOMC press conference only. Event: CPI 12:30 UTC.

| # | in | expected out |
|---|---|---|
| 1 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"CPI"}],"t":"2026-09-16T12:30:00Z","kind":"HIGH"}` | `{"blocked":true}` |
| 2 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"CPI"}],"t":"2026-09-16T12:00:01Z","kind":"HIGH"}` | `{"blocked":true}` |
| 3 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"CPI"}],"t":"2026-09-16T11:59:59Z","kind":"HIGH"}` | `{"blocked":false}` |
| 4 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"CPI"}],"t":"2026-09-16T12:44:59Z","kind":"HIGH"}` | `{"blocked":true}` |
| 5 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"CPI"}],"t":"2026-09-16T12:45:01Z","kind":"HIGH"}` | `{"blocked":false}` |
| 6 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"CPI"}],"t":"2026-09-16T11:30:01Z","kind":"MAJOR"}` | `{"blocked":true}` |
| 7 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"CPI"}],"t":"2026-09-16T11:29:59Z","kind":"MAJOR"}` | `{"blocked":false}` |
| 8 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"CPI"}],"t":"2026-09-16T12:59:59Z","kind":"MAJOR"}` | `{"blocked":true}` |
| 9 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"CPI"}],"t":"2026-09-16T13:00:01Z","kind":"MAJOR"}` | `{"blocked":false}` |

#### `GV-G-NW-02` · news
> Which events count: a high-impact NON-major USD event (PPI) blocks F_NEWS_HIGH but not F_NEWS_MAJOR; EUR events and medium-impact USD events block nothing.

| # | in | expected out |
|---|---|---|
| 1 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"PPI"}],"t":"2026-09-16T12:20:00Z","kind":"HIGH"}` | `{"blocked":true}` |
| 2 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"PPI"}],"t":"2026-09-16T12:20:00Z","kind":"MAJOR"}` | `{"blocked":false}` |
| 3 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"EUR","impact":"high","name":"CPI"}],"t":"2026-09-16T12:30:00Z","kind":"HIGH"}` | `{"blocked":false}` |
| 4 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"medium","name":"CPI"}],"t":"2026-09-16T12:30:00Z","kind":"HIGH"}` | `{"blocked":false}` |
| 5 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"NFP"},{"time":"2026-09-16T19:00:00Z","currency":"USD","impact":"high","name":"FOMC decision"}],"t":"2026-09-16T18:20:00Z","kind":"MAJOR"}` | `{"blocked":true}` |
| 6 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"CPI"},{"time":"2026-09-16T19:00:00Z","currency":"USD","impact":"high","name":"FOMC press conference"}],"t":"2026-09-16T18:59:00Z","kind":"MAJOR"}` | `{"blocked":true}` |

#### `GV-G-NW-03` · news
> News window BOUNDARIES (inclusive at both ends assumed - spec silent, A-07): HIGH blocked at exactly T-30 and T+15; MAJOR at exactly T-60 and T+30.

| # | in | expected out |
|---|---|---|
| 1 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"CPI"}],"t":"2026-09-16T12:00:00Z","kind":"HIGH"}` | `{"blocked":true}` |
| 2 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"CPI"}],"t":"2026-09-16T12:45:00Z","kind":"HIGH"}` | `{"blocked":true}` |
| 3 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"CPI"}],"t":"2026-09-16T11:30:00Z","kind":"MAJOR"}` | `{"blocked":true}` |
| 4 | `{"events":[{"time":"2026-09-16T12:30:00Z","currency":"USD","impact":"high","name":"CPI"}],"t":"2026-09-16T13:00:00Z","kind":"MAJOR"}` | `{"blocked":true}` |

#### `GV-G-QT-01` · quant
> G13 executable-price quantisation (tick 0.01). Internal values are exact; order levels are quantised: STOPS away from the entry (long down, short up); fixed-R / Fibonacci / measured TARGETS in the profit direction (long up, short down); STRUCTURAL targets toward the entry (long down, short up); STOP-ENTRY triggers in the trigger direction (long up, short down). Prices already on the grid are unchanged.

| # | in | expected out |
|---|---|---|
| 1 | `{"kind":"stop","dir":1,"x":"4193.795"}` | `{"q":"4193.79"}` |
| 2 | `{"kind":"stop","dir":-1,"x":"4206.205"}` | `{"q":"4206.21"}` |
| 3 | `{"kind":"stop","dir":1,"x":"4193.79"}` | `{"q":"4193.79"}` |
| 4 | `{"kind":"stop","dir":1,"x":"4193.791"}` | `{"q":"4193.79"}` |
| 5 | `{"kind":"stop","dir":1,"x":"4193.7899"}` | `{"q":"4193.78"}` |
| 6 | `{"kind":"profit","dir":1,"x":"4257.432"}` | `{"q":"4257.44"}` |
| 7 | `{"kind":"profit","dir":-1,"x":"4142.568"}` | `{"q":"4142.56"}` |
| 8 | `{"kind":"profit","dir":1,"x":"4257.44"}` | `{"q":"4257.44"}` |
| 9 | `{"kind":"structural","dir":1,"x":"4229.7875"}` | `{"q":"4229.78"}` |
| 10 | `{"kind":"structural","dir":-1,"x":"4229.7875"}` | `{"q":"4229.79"}` |
| 11 | `{"kind":"structural","dir":1,"x":"4229.78"}` | `{"q":"4229.78"}` |
| 12 | `{"kind":"trigger","dir":1,"x":"4211.204"}` | `{"q":"4211.21"}` |
| 13 | `{"kind":"trigger","dir":-1,"x":"4211.204"}` | `{"q":"4211.20"}` |
| 14 | `{"kind":"trigger","dir":1,"x":"4211.20"}` | `{"q":"4211.20"}` |

#### `GV-G-RS-01` · rsi
> G7 RSI14 (Wilder): the first average is the simple mean of the first 14 changes, later averages are smoothed (avg = (prev*13 + new)/14). Alternating +-1 changes -> 50; all gains -> 100; all losses -> 0.

| # | in | expected out |
|---|---|---|
| 1 | `{"closes":["100","101","100","101","100","101","100","101","100","101","100","101","100","101","100"]}` | `{"rsi":"50.00"}` |
| 2 | `{"closes":["100","101","102","103","104","105","106","107","108","109","110","111","112","113","114"]}` | `{"rsi":"100.00"}` |
| 3 | `{"closes":["100","99","98","97","96","95","94","93","92","91","90","89","88","87","86"]}` | `{"rsi":"0.00"}` |

#### `GV-G-RS-02` · rsi
> Wilder smoothing (not a simple average): after 14 alternating +-1 changes (avg gain = avg loss = 0.5) one +7 change gives avg gain 13.5/14, avg loss 6.5/14, RS = 27/13, RSI = 67.50. A 14-close SMA implementation would give a different number.

| # | in | expected out |
|---|---|---|
| 1 | `{"closes":["100","101","100","101","100","101","100","101","100","101","100","101","100","101","100","107"]}` | `{"rsi":"67.50"}` |

#### `GV-G-RS-03` · rsi
> Warm-up: RSI needs 100 completed bars in the spec (variants that require it record NOT_EVALUATED_WARMUP with fewer; see GV-P06-H05/H06). The arithmetic itself needs 15 closes: with 14 closes there is no first average.

| # | in | expected out |
|---|---|---|
| 1 | `{"closes":["100","101","100","101","100","101","100","101","100","101","100","101","100","101"]}` | `{"rsi":null}` |

#### `GV-G-SN-01` · snapshot
> Target snapshot (G4 two zone sets, G10 entry snapshot): the pivot at bar 17 (H 4230.40) sits right before the 2-bar pattern (bars 18-19) and needs two later bars to be confirmed. At i0-1 (17) only the older 4230.00 high is confirmed -> no zone (zones_prepattern = none). At the entry (pattern complete, cutoff 19) both highs are confirmed -> zone [4229.70, 4230.70] (zones_at_entry). Later bars form a nearer zone [4225.70, 4226.70] and a support zone, which must NOT change the frozen target of a trade already entered.

| # | in | expected out |
|---|---|---|
| 1 | `{"bars":"[34 bars: first ['4200.00', '4200.10', '4196.77', '4196.87'] ... last ['4225.80', '4225.90', '4225.50', '4225.60']; full series in golden_vectors.json]","atr":"4","cutoffs":{"pre":17,"entry":19,"later":33}}` | `{"pre":[],"entry":[["4229.70","4230.70"]],"later":[["4225.70","4226.70"],["4229.70","4230.70"]]}` |

#### `GV-G-SS-01` · session
> G6 sessions from local clocks: ASIA 09:00-17:00 Asia/Tokyo (no DST), LONDON 08:00-17:00 Europe/London, NY 08:00-17:00 America/New_York; ASIA_ONLY = in ASIA and in neither LONDON nor NY. Interior times only (boundaries are in GV-G-SS-02). September: London on BST, New York on EDT.

| # | in | expected out |
|---|---|---|
| 1 | `{"t":"2026-09-16T03:00:00Z"}` | `{"ASIA":true,"LONDON":false,"NY":false,"ASIA_ONLY":true}` |
| 2 | `{"t":"2026-09-16T07:30:00Z"}` | `{"ASIA":true,"LONDON":true,"NY":false,"ASIA_ONLY":false}` |
| 3 | `{"t":"2026-09-16T10:00:00Z"}` | `{"ASIA":false,"LONDON":true,"NY":false,"ASIA_ONLY":false}` |
| 4 | `{"t":"2026-09-16T13:00:00Z"}` | `{"ASIA":false,"LONDON":true,"NY":true,"ASIA_ONLY":false}` |
| 5 | `{"t":"2026-09-16T17:00:00Z"}` | `{"ASIA":false,"LONDON":false,"NY":true,"ASIA_ONLY":false}` |
| 6 | `{"t":"2026-09-16T22:00:00Z"}` | `{"ASIA":false,"LONDON":false,"NY":false,"ASIA_ONLY":false}` |

#### `GV-G-SS-02` · session
> DST divergence: the UK leaves BST on 25 Oct 2026 but the US stays on EDT until 1 Nov; the US enters DST on 8 Mar 2026 but the UK stays on GMT until 29 Mar. The SAME UTC time changes session membership: 07:30 UTC is ASIA_ONLY on 27 Oct (London 07:30 GMT, closed) but London-open on 16 Sep (08:30 BST).

| # | in | expected out |
|---|---|---|
| 1 | `{"t":"2026-10-27T07:30:00Z"}` | `{"ASIA":true,"LONDON":false,"NY":false,"ASIA_ONLY":true}` |
| 2 | `{"t":"2026-10-27T08:30:00Z"}` | `{"ASIA":false,"LONDON":true,"NY":false,"ASIA_ONLY":false}` |
| 3 | `{"t":"2026-10-27T12:30:00Z"}` | `{"ASIA":false,"LONDON":true,"NY":true,"ASIA_ONLY":false}` |
| 4 | `{"t":"2026-10-27T21:30:00Z"}` | `{"ASIA":false,"LONDON":false,"NY":false,"ASIA_ONLY":false}` |
| 5 | `{"t":"2026-11-03T12:30:00Z"}` | `{"ASIA":false,"LONDON":true,"NY":false,"ASIA_ONLY":false}` |
| 6 | `{"t":"2026-11-03T13:30:00Z"}` | `{"ASIA":false,"LONDON":true,"NY":true,"ASIA_ONLY":false}` |
| 7 | `{"t":"2026-11-03T21:30:00Z"}` | `{"ASIA":false,"LONDON":false,"NY":true,"ASIA_ONLY":false}` |
| 8 | `{"t":"2026-03-12T12:30:00Z"}` | `{"ASIA":false,"LONDON":true,"NY":true,"ASIA_ONLY":false}` |
| 9 | `{"t":"2026-03-02T12:30:00Z"}` | `{"ASIA":false,"LONDON":true,"NY":false,"ASIA_ONLY":false}` |

#### `GV-G-SS-03` · session
> Session BOUNDARIES (start inclusive, end exclusive assumed - spec silent, A-06): Tokyo 09:00 = 00:00 UTC; Tokyo 17:00 = 08:00 UTC; London opens 08:00 BST = 07:00 UTC and closes 17:00 BST = 16:00 UTC; New York opens 08:00 EDT = 12:00 UTC and closes 17:00 EDT = 21:00 UTC.

| # | in | expected out |
|---|---|---|
| 1 | `{"t":"2026-09-16T00:00:00Z"}` | `{"ASIA":true,"LONDON":false,"NY":false,"ASIA_ONLY":true}` |
| 2 | `{"t":"2026-09-15T23:59:59Z"}` | `{"ASIA":false,"LONDON":false,"NY":false,"ASIA_ONLY":false}` |
| 3 | `{"t":"2026-09-16T06:59:59Z"}` | `{"ASIA":true,"LONDON":false,"NY":false,"ASIA_ONLY":true}` |
| 4 | `{"t":"2026-09-16T07:00:00Z"}` | `{"ASIA":true,"LONDON":true,"NY":false,"ASIA_ONLY":false}` |
| 5 | `{"t":"2026-09-16T07:59:59Z"}` | `{"ASIA":true,"LONDON":true,"NY":false,"ASIA_ONLY":false}` |
| 6 | `{"t":"2026-09-16T08:00:00Z"}` | `{"ASIA":false,"LONDON":true,"NY":false,"ASIA_ONLY":false}` |
| 7 | `{"t":"2026-09-16T11:59:59Z"}` | `{"ASIA":false,"LONDON":true,"NY":false,"ASIA_ONLY":false}` |
| 8 | `{"t":"2026-09-16T12:00:00Z"}` | `{"ASIA":false,"LONDON":true,"NY":true,"ASIA_ONLY":false}` |
| 9 | `{"t":"2026-09-16T15:59:59Z"}` | `{"ASIA":false,"LONDON":true,"NY":true,"ASIA_ONLY":false}` |
| 10 | `{"t":"2026-09-16T16:00:00Z"}` | `{"ASIA":false,"LONDON":false,"NY":true,"ASIA_ONLY":false}` |
| 11 | `{"t":"2026-09-16T20:59:59Z"}` | `{"ASIA":false,"LONDON":false,"NY":true,"ASIA_ONLY":false}` |
| 12 | `{"t":"2026-09-16T21:00:00Z"}` | `{"ASIA":false,"LONDON":false,"NY":false,"ASIA_ONLY":false}` |

#### `GV-G-SW-01` · swings
> G3: a swing high at bar j needs H[j] strictly greater than the highs of the 2 bars before and 2 after; it is CONFIRMED only when bar j+2 is complete. Zig-zag series (pivot tips L4190@2, H4210@5, L4192@8, H4212@11, L4194@14, H4214@17). The pivot at bar 5 is invisible at cutoff 6 and visible at cutoff 7.

*Note: cutoff 17: the pivot at bar 17 needs bars 18 and 19 -> still unconfirmed.*

| # | in | expected out |
|---|---|---|
| 1 | `{"bars":"[18 bars: first ['4200.00', '4200.10', '4196.77', '4196.87'] ... last ['4209.22', '4214.00', '4209.12', '4213.40']; full series in golden_vectors.json]","cutoff":6}` | `{"swings":[["L",2,"4190.00"]]}` |
| 2 | `{"bars":"[18 bars: first ['4200.00', '4200.10', '4196.77', '4196.87'] ... last ['4209.22', '4214.00', '4209.12', '4213.40']; full series in golden_vectors.json]","cutoff":7}` | `{"swings":[["L",2,"4190.00"],["H",5,"4210.00"]]}` |
| 3 | `{"bars":"[18 bars: first ['4200.00', '4200.10', '4196.77', '4196.87'] ... last ['4209.22', '4214.00', '4209.12', '4213.40']; full series in golden_vectors.json]","cutoff":16}` | `{"swings":[["L",2,"4190.00"],["H",5,"4210.00"],["L",8,"4192.00"],["H",11,"4212.00"],["L",14,"4194.00"]]}` |
| 4 | `{"bars":"[18 bars: first ['4200.00', '4200.10', '4196.77', '4196.87'] ... last ['4209.22', '4214.00', '4209.12', '4213.40']; full series in golden_vectors.json]","cutoff":17}` | `{"swings":[["L",2,"4190.00"],["H",5,"4210.00"],["L",8,"4192.00"],["H",11,"4212.00"],["L",14,"4194.00"]]}` |

#### `GV-G-SW-02` · swings
> Strictness: a bar whose high EQUALS a neighbour's high (within 2 bars) is not a swing high. Highs 4200,4201,4205,4205,4203,4201,4200: bars 2 and 3 tie -> no swing high. Highs 4200,4201,4205,4203,4201,4200,4199 -> bar 2 is a swing high.

| # | in | expected out |
|---|---|---|
| 1 | `{"bars":"[7 bars: first ['4198.00', '4200.00', '4190.00', '4199.00'] ... last ['4198.00', '4200.00', '4190.00', '4199.00']; full series in golden_vectors.json]","cutoff":6}` | `{"swings":[]}` |
| 2 | `{"bars":"[7 bars: first ['4198.00', '4200.00', '4190.00', '4199.00'] ... last ['4197.00', '4199.00', '4190.00', '4198.00']; full series in golden_vectors.json]","cutoff":6}` | `{"swings":[["H",2,"4205.00"]]}` |

#### `GV-G-SW-03` · swings
> A pivot needs two bars on each side: highs 4200,4205,4203,4202,4201 -> bar 1 has only one bar before it, so it is not a swing high even though it is the maximum.

| # | in | expected out |
|---|---|---|
| 1 | `{"bars":[["4198.00","4200.00","4190.00","4199.00"],["4203.00","4205.00","4190.00","4204.00"],["4201.00","4203.00","4190.00","4202.00"],["4200.00","4202.00","4190.00","4201.00"],["4199.00","4201.00","4190.00","4200.00"]],"cutoff":4}` | `{"swings":[]}` |

#### `GV-G-SW-04` · swings_summary
> Window: swings come from the last 200 completed bars. A 212-bar zig-zag (pivots at bars 2, 5, 8, ...). With cutoff 211 the window starts at bar 12, so the pivots at bars 2, 5, 8 and 11 are gone and the first swing returned is bar 14; the last is bar 209 (needs bars 210 and 211). Only the first and last returned swings and the count are asserted.

*Note: Case 2 (A-24): with cutoff 210 the window starts at bar 11, the pivot CENTRE at bar 11 is inside it and is returned even though its left neighbours (bars 9 and 10) lie just outside; the pivot at bar 209 needs bars 210 and 211 and is not yet confirmed.*

| # | in | expected out |
|---|---|---|
| 1 | `{"bars":"[212 bars: first ['4200.00', '4200.10', '4196.77', '4196.87'] ... last ['4209.40', '4209.50', '4209.30', '4209.40']; full series in golden_vectors.json]","cutoff":211}` | `{"count":66,"first":["L",14,"4190.00"],"last":["H",209,"4210.00"]}` |
| 2 | `{"bars":"[212 bars: first ['4200.00', '4200.10', '4196.77', '4196.87'] ... last ['4209.40', '4209.50', '4209.30', '4209.40']; full series in golden_vectors.json]","cutoff":210}` | `{"count":66,"first":["H",11,"4210.00"],"last":["L",206,"4190.00"]}` |

#### `GV-G-SZ-01` · sizing
> Sizing (G8): 1R = 1% of REF_EQUITY $10,000 = $100. loss_per_lot = (R / tick_size) * tick_value; lots = risk / loss_per_lot (unrounded on the virtual ledger); the demo mirror rounds DOWN to the lot step and records the actual risk. Test account: tick_size 0.01, tick_value $1.00, lot_step 0.01, min_lot 0.01.

| # | in | expected out |
|---|---|---|
| 1 | `{"R":"6.60"}` | `{"risk_usd":"100.00","loss_per_lot":"660.00","lots":"5/33","demo_lots":"0.15","mirror":"OK","actual_demo_risk":"99.00"}` |
| 2 | `{"R":"6.51"}` | `{"loss_per_lot":"651.00","lots":"100/651","demo_lots":"0.15","actual_demo_risk":"97.65"}` |
| 3 | `{"R":"0.80"}` | `{"loss_per_lot":"80.00","lots":"1.25","demo_lots":"1.25","actual_demo_risk":"100.00"}` |

#### `GV-G-SZ-02` · sizing
> Minimum lot: R = 100.00 gives exactly 0.01 lot (mirrored); R = 100.01 gives 0.0099990 lot which rounds down to 0.00 < min_lot -> MIRROR_SKIPPED_MIN_LOT (the virtual trade still counts).

| # | in | expected out |
|---|---|---|
| 1 | `{"R":"100.00"}` | `{"lots":"0.01","demo_lots":"0.01","mirror":"OK","actual_demo_risk":"100.00"}` |
| 2 | `{"R":"100.01"}` | `{"lots":"100/10001","demo_lots":"0.00","mirror":"MIRROR_SKIPPED_MIN_LOT","actual_demo_risk":"0.00"}` |

#### `GV-G-SZ-03` · sizing
> The formula uses the broker's tick size and tick VALUE, never a contract size: a $0.50 tick value doubles the lots; tick_size 0.10 with tick_value $10.00 gives the same loss_per_lot as 0.01/$1.00; lot_step 0.10 rounds 0.1515 down to 0.10.

| # | in | expected out |
|---|---|---|
| 1 | `{"R":"6.60","acct":{"tick_value":"0.50"}}` | `{"loss_per_lot":"330.00","lots":"10/33","demo_lots":"0.30","actual_demo_risk":"99.00"}` |
| 2 | `{"R":"6.60","acct":{"tick_size":"0.10","tick_value":"10.00"}}` | `{"loss_per_lot":"660.00","lots":"5/33","demo_lots":"0.15"}` |
| 3 | `{"R":"6.60","acct":{"lot_step":"0.10"}}` | `{"lots":"5/33","demo_lots":"0.10","actual_demo_risk":"66.00"}` |

#### `GV-G-SZ-04` · sizing
> Commission in R: with $7.00 per lot round trip, R 6.60 and 5/33 lot the commission is $7 x 5/33 = $1.0606 = 7/660 R. It is subtracted from the trade result.

| # | in | expected out |
|---|---|---|
| 1 | `{"R":"6.60","commission":"7.00"}` | `{"lots":"5/33","commission_R":"7/660"}` |

#### `GV-G-TR-01` · trend
> G3 trend from the last two confirmed swing highs (SH1 older, SH2 newer) and lows, tolerance +-0.10*ATR (ATR 4 -> 0.40). UP needs BOTH SH2>=SH1+0.40 AND SL2>=SL1+0.40.

| # | in | expected out |
|---|---|---|
| 1 | `{"swings":[["L",2,"4190.00"],["H",5,"4210.00"],["L",8,"4190.40"],["H",11,"4210.40"]],"atr":"4"}` | `{"trend":"UP"}` |
| 2 | `{"swings":[["L",2,"4190.00"],["H",5,"4210.00"],["L",8,"4190.40"],["H",11,"4210.39"]],"atr":"4"}` | `{"trend":"RANGE"}` |
| 3 | `{"swings":[["L",2,"4190.00"],["H",5,"4210.00"],["L",8,"4190.39"],["H",11,"4210.40"]],"atr":"4"}` | `{"trend":"RANGE"}` |
| 4 | `{"swings":[["L",2,"4190.00"],["H",5,"4210.00"],["L",8,"4189.60"],["H",11,"4209.60"]],"atr":"4"}` | `{"trend":"DOWN"}` |
| 5 | `{"swings":[["L",2,"4190.00"],["H",5,"4210.00"],["L",8,"4189.60"],["H",11,"4209.61"]],"atr":"4"}` | `{"trend":"RANGE"}` |
| 6 | `{"swings":[["L",2,"4190.00"],["H",5,"4210.00"],["L",8,"4188.00"],["H",11,"4212.00"]],"atr":"4"}` | `{"trend":"RANGE"}` |
| 7 | `{"swings":[["L",2,"4190.00"],["H",5,"4210.00"],["L",8,"4190.00"],["H",11,"4210.00"]],"atr":"4"}` | `{"trend":"RANGE"}` |

#### `GV-G-TR-02` · trend
> Trend is UNDETERMINED with fewer than two confirmed swing highs or fewer than two swing lows; only the LAST two of each are used (older ones are ignored).

| # | in | expected out |
|---|---|---|
| 1 | `{"swings":[["H",5,"4210.00"],["L",2,"4190.00"],["L",8,"4192.00"]],"atr":"4"}` | `{"trend":"UNDETERMINED"}` |
| 2 | `{"swings":[["H",5,"4210.00"],["H",11,"4212.00"]],"atr":"4"}` | `{"trend":"UNDETERMINED"}` |
| 3 | `{"swings":[["L",2,"4190.00"]],"atr":"4"}` | `{"trend":"UNDETERMINED"}` |
| 4 | `{"swings":[],"atr":"4"}` | `{"trend":"UNDETERMINED"}` |
| 5 | `{"swings":[["H",1,"4300.00"],["L",2,"4100.00"],["H",5,"4210.00"],["L",8,"4190.00"],["H",11,"4211.00"],["L",14,"4191.00"]],"atr":"4"}` | `{"trend":"UP"}` |

#### `GV-G-TR-03` · trend
> Tolerance scales with ATR: the same +0.40 rise is UP at ATR 4 (tol 0.40) but RANGE at ATR 5 (tol 0.50) and UP at ATR 2 (tol 0.20).

| # | in | expected out |
|---|---|---|
| 1 | `{"swings":[["L",2,"4190.00"],["H",5,"4210.00"],["L",8,"4190.40"],["H",11,"4210.40"]],"atr":"4"}` | `{"trend":"UP"}` |
| 2 | `{"swings":[["L",2,"4190.00"],["H",5,"4210.00"],["L",8,"4190.40"],["H",11,"4210.40"]],"atr":"5"}` | `{"trend":"RANGE"}` |
| 3 | `{"swings":[["L",2,"4190.00"],["H",5,"4210.00"],["L",8,"4190.40"],["H",11,"4210.40"]],"atr":"2"}` | `{"trend":"UP"}` |

#### `GV-G-TR-04` · series_trend
> End-to-end trend from a bar series (atr_pre given as 4.00). Confirmed swings only, at cutoff = i0-1: the DOWN staircase (highs 4230, 4226, 4222; lows 4190, 4186, 4182) -> DOWN; the UP staircase mirrored -> UP. Each last pivot is not yet confirmed at the last bar and must not be used.

| # | in | expected out |
|---|---|---|
| 1 | `{"bars":"[21 bars: first ['4230.00', '4230.10', '4229.70', '4229.80'] ... last ['4209.67', '4218.00', '4209.57', '4217.40']; full series in golden_vectors.json]","cutoff":20,"atr":"4"}` | `{"trend":"DOWN"}` |
| 2 | `{"bars":"[21 bars: first ['4200.00', '4200.10', '4196.77', '4196.87'] ... last ['4210.33', '4210.43', '4202.00', '4202.60']; full series in golden_vectors.json]","cutoff":20,"atr":"4"}` | `{"trend":"UP"}` |

#### `GV-G-TR-05` · series_trend
> No look-ahead: the final pivot (H 4260, bar 20) would flip the trend (SH2 > SH1) but is not confirmed until two more bars complete. At cutoff = bar 20 the trend is still DOWN (last confirmed highs 4226, 4222); two bars later it is RANGE (a higher high with a lower low).

*Note: The two appended bars have lower highs than the pivot, confirming it.*

| # | in | expected out |
|---|---|---|
| 1 | `{"bars":"[23 bars: first ['4230.00', '4230.10', '4229.70', '4229.80'] ... last ['4242.33', '4260.00', '4242.23', '4259.40']; full series in golden_vectors.json]","cutoff":20,"atr":"4"}` | `{"trend":"DOWN"}` |
| 2 | `{"bars":"[23 bars: first ['4230.00', '4230.10', '4229.70', '4229.80'] ... last ['4259.40', '4259.10', '4258.10', '4258.70']; full series in golden_vectors.json]","cutoff":22,"atr":"4"}` | `{"trend":"RANGE"}` |

#### `GV-G-ZN-01` · zones
> G4 clustering: sort confirmed swing prices (highs and lows pooled) ascending; a cluster starts at the lowest unassigned price p0 and takes every price <= p0 + 0.25*ATR (ATR 4 -> 1.00). A zone needs >= 2 pivots with at least one pair >= 3 bars apart; centre = median; zone = centre +- 0.125*ATR (0.50).

| # | in | expected out |
|---|---|---|
| 1 | `{"swings":[["H",10,"4230.00"],["H",20,"4230.60"]],"atr":"4"}` | `{"zones":[["4229.80","4230.80"]],"centres":["4230.30"]}` |
| 2 | `{"swings":[["H",10,"4230.00"],["H",20,"4231.00"]],"atr":"4"}` | `{"zones":[["4230.00","4231.00"]],"centres":["4230.50"]}` |
| 3 | `{"swings":[["H",10,"4230.00"],["H",20,"4231.01"]],"atr":"4"}` | `{"zones":[],"centres":[]}` |
| 4 | `{"swings":[["H",10,"4230.00"]],"atr":"4"}` | `{"zones":[],"centres":[]}` |

#### `GV-G-ZN-02` · zones
> Greedy, not chained: prices 4200.00, 4200.90, 4201.80. The cluster starting at 4200.00 takes everything <= 4201.00 (4200.00, 4200.90); 4201.80 starts a new cluster and is alone -> one zone [4199.95, 4200.95]. A chained clustering would merge all three.

| # | in | expected out |
|---|---|---|
| 1 | `{"swings":[["H",10,"4200.00"],["H",20,"4200.90"],["H",30,"4201.80"]],"atr":"4"}` | `{"zones":[["4199.95","4200.95"]],"centres":["4200.45"]}` |

#### `GV-G-ZN-03` · zones
> Median centre with an odd count: 4200.00, 4200.30, 4200.90 -> centre 4200.30 -> zone [4199.80, 4200.80].

| # | in | expected out |
|---|---|---|
| 1 | `{"swings":[["H",10,"4200.00"],["H",20,"4200.30"],["H",30,"4200.90"]],"atr":"4"}` | `{"zones":[["4199.80","4200.80"]],"centres":["4200.30"]}` |

#### `GV-G-ZN-04` · zones
> Median with an EVEN count is not defined in the spec (A-23). The vector uses the mean of the two middle prices (4200.2, 4200.4 -> 4200.30).

| # | in | expected out |
|---|---|---|
| 1 | `{"swings":[["H",10,"4200.00"],["H",20,"4200.20"],["H",30,"4200.40"],["H",40,"4200.90"]],"atr":"4"}` | `{"zones":[["4199.80","4200.80"]],"centres":["4200.30"]}` |

#### `GV-G-ZN-05` · zones
> The pair-spacing rule: pivots only 2 bars apart (10 and 12) are one event, not a zone; 3 bars apart (10 and 13) is enough. With three pivots at bars 10, 11, 14 the pair (10, 14) qualifies; at bars 10, 11, 12 no pair is >= 3 apart.

| # | in | expected out |
|---|---|---|
| 1 | `{"swings":[["H",10,"4230.00"],["L",12,"4230.30"]],"atr":"4"}` | `{"zones":[],"centres":[]}` |
| 2 | `{"swings":[["H",10,"4230.00"],["L",13,"4230.30"]],"atr":"4"}` | `{"zones":[["4229.65","4230.65"]],"centres":["4230.15"]}` |
| 3 | `{"swings":[["H",10,"4200.00"],["H",11,"4200.20"],["H",14,"4200.40"]],"atr":"4"}` | `{"zones":[["4199.70","4200.70"]],"centres":["4200.20"]}` |
| 4 | `{"swings":[["H",10,"4200.00"],["H",11,"4200.20"],["H",12,"4200.40"]],"atr":"4"}` | `{"zones":[],"centres":[]}` |

#### `GV-G-ZN-06` · zones
> Highs and lows are pooled (role flips are not modelled in v1): a swing high at 4230.00 and a swing low at 4230.50 form one zone [4229.75, 4230.75].

| # | in | expected out |
|---|---|---|
| 1 | `{"swings":[["H",10,"4230.00"],["L",20,"4230.50"]],"atr":"4"}` | `{"zones":[["4229.75","4230.75"]],"centres":["4230.25"]}` |

#### `GV-G-ZN-07` · zones
> Zone width scales with ATR: at ATR 8 the cluster width is 2.00 and the half-width 1.00: 4230.00 and 4231.90 cluster (zone [4229.95, 4231.95]); 4232.01 does not.

| # | in | expected out |
|---|---|---|
| 1 | `{"swings":[["H",10,"4230.00"],["H",20,"4231.90"]],"atr":"8"}` | `{"zones":[["4229.95","4231.95"]],"centres":["4230.95"]}` |
| 2 | `{"swings":[["H",10,"4230.00"],["H",20,"4232.01"]],"atr":"8"}` | `{"zones":[],"centres":[]}` |

#### `GV-G-ZN-08` · zones
> Two separate zones come out sorted ascending: lows 4190.0/4190.4 and highs 4220.0/4220.7.

| # | in | expected out |
|---|---|---|
| 1 | `{"swings":[["L",5,"4190.00"],["L",15,"4190.40"],["H",25,"4220.00"],["H",40,"4220.70"]],"atr":"4"}` | `{"zones":[["4189.70","4190.70"],["4219.85","4220.85"]],"centres":["4190.20","4220.35"]}` |

#### `GV-G-ZN-09` · atzone
> AT_SUPPORT / AT_RESISTANCE: distance from the pattern extreme to the nearest zone (0 if inside) <= 0.10*ATR (ATR 4 -> 0.40; ATR 8 -> 0.80).

| # | in | expected out |
|---|---|---|
| 1 | `{"zones":[["4229.80","4230.80"]],"price":"4230.30","atr":"4"}` | `{"dist":"0.00","at":true}` |
| 2 | `{"zones":[["4229.80","4230.80"]],"price":"4231.20","atr":"4"}` | `{"dist":"0.40","at":true}` |
| 3 | `{"zones":[["4229.80","4230.80"]],"price":"4231.21","atr":"4"}` | `{"dist":"0.41","at":false}` |
| 4 | `{"zones":[["4229.80","4230.80"]],"price":"4229.40","atr":"4"}` | `{"dist":"0.40","at":true}` |
| 5 | `{"zones":[["4229.80","4230.80"]],"price":"4229.39","atr":"4"}` | `{"dist":"0.41","at":false}` |
| 6 | `{"zones":[["4229.80","4230.80"]],"price":"4231.60","atr":"8"}` | `{"dist":"0.80","at":true}` |
| 7 | `{"zones":[["4229.80","4230.80"]],"price":"4231.61","atr":"8"}` | `{"dist":"0.81","at":false}` |
| 8 | `{"zones":[],"price":"4230.30","atr":"4"}` | `{"dist":null,"at":false}` |

#### `GV-G-ZN-10` · round50
> ROUND_50 context flag: the extreme lies within 0.10*ATR of a multiple of $50 (ATR 4 -> 0.40). Context only; no rule requires it.

| # | in | expected out |
|---|---|---|
| 1 | `{"price":"4200.40","atr":"4"}` | `{"round_50":true}` |
| 2 | `{"price":"4200.41","atr":"4"}` | `{"round_50":false}` |
| 3 | `{"price":"4249.60","atr":"4"}` | `{"round_50":true}` |
| 4 | `{"price":"4249.59","atr":"4"}` | `{"round_50":false}` |
| 5 | `{"price":"4225.00","atr":"4"}` | `{"round_50":false}` |
| 6 | `{"price":"4150.00","atr":"4"}` | `{"round_50":true}` |

#### `GV-G-ZN-11` · zonedeath
> G4 zone role and death (Claude's ruling E). ROLE = type of the most recent contributing pivot: swing high -> RESISTANCE, swing low -> SUPPORT. A RESISTANCE zone is dead once a completed candle after that pivot closes more than 0.10*ATR (0.40 at ATR 4) ABOVE its top; a SUPPORT zone once one closes more than 0.40 BELOW its bottom. A bounce AWAY from the zone (up from support, down from resistance) does not kill it. Zones below are [4229.80,4230.80] (resistance) and [4189.80,4190.80] (support).

| # | in | expected out |
|---|---|---|
| 1 | `{"swings":[["H",10,"4230.00"],["H",20,"4230.60"]],"closes":{},"cutoff":30,"atr":"4"}` | `{"zones":[["4229.80","4230.80",true,"RESISTANCE"]]}` |
| 2 | `{"swings":[["H",10,"4230.00"],["H",20,"4230.60"]],"closes":{"25":"4231.20"},"cutoff":30,"atr":"4"}` | `{"zones":[["4229.80","4230.80",true,"RESISTANCE"]]}` |
| 3 | `{"swings":[["H",10,"4230.00"],["H",20,"4230.60"]],"closes":{"25":"4231.21"},"cutoff":30,"atr":"4"}` | `{"zones":[["4229.80","4230.80",false,"RESISTANCE"]]}` |
| 4 | `{"swings":[["H",10,"4230.00"],["H",20,"4230.60"]],"closes":{"25":"4210.00"},"cutoff":30,"atr":"4"}` | `{"zones":[["4229.80","4230.80",true,"RESISTANCE"]]}` |
| 5 | `{"swings":[["L",10,"4190.00"],["L",20,"4190.60"]],"closes":{"25":"4189.40"},"cutoff":30,"atr":"4"}` | `{"zones":[["4189.80","4190.80",true,"SUPPORT"]]}` |
| 6 | `{"swings":[["L",10,"4190.00"],["L",20,"4190.60"]],"closes":{"25":"4189.39"},"cutoff":30,"atr":"4"}` | `{"zones":[["4189.80","4190.80",false,"SUPPORT"]]}` |
| 7 | `{"swings":[["L",10,"4190.00"],["L",20,"4190.60"]],"closes":{"25":"4210.00"},"cutoff":30,"atr":"4"}` | `{"zones":[["4189.80","4190.80",true,"SUPPORT"]]}` |

#### `GV-G-ZN-12` · zonedeath
> Zone death scan window: only closes AFTER the latest contributing pivot count. A close at bar 15 (between pivots at 10 and 20) is ignored; the same close at bar 25 kills the resistance zone. A LATER pivot (bar 35, high 4230.20) that re-joins the cluster revives a dead zone (its latest pivot is now bar 35, and bars before it are not scanned); a close beyond the top after bar 35 kills it again. ATR scaling: at ATR 8 the tolerance is 0.80.

| # | in | expected out |
|---|---|---|
| 1 | `{"swings":[["H",10,"4230.00"],["H",20,"4230.60"]],"closes":{"15":"4232.00"},"cutoff":30,"atr":"4"}` | `{"zones":[["4229.80","4230.80",true,"RESISTANCE"]]}` |
| 2 | `{"swings":[["H",10,"4230.00"],["H",20,"4230.60"]],"closes":{"25":"4232.00"},"cutoff":30,"atr":"4"}` | `{"zones":[["4229.80","4230.80",false,"RESISTANCE"]]}` |
| 3 | `{"swings":[["H",10,"4230.00"],["H",20,"4230.60"],["H",35,"4230.20"]],"closes":{"25":"4232.00"},"cutoff":40,"atr":"4"}` | `{"zones":[["4229.70","4230.70",true,"RESISTANCE"]]}` |
| 4 | `{"swings":[["H",10,"4230.00"],["H",20,"4230.60"],["H",35,"4230.20"]],"closes":{"25":"4232.00","36":"4231.11"},"cutoff":40,"atr":"4"}` | `{"zones":[["4229.70","4230.70",false,"RESISTANCE"]]}` |
| 5 | `{"swings":[["H",10,"4230.00"],["H",20,"4231.90"]],"closes":{"25":"4232.75"},"cutoff":30,"atr":"8"}` | `{"zones":[["4229.95","4231.95",true,"RESISTANCE"]]}` |
| 6 | `{"swings":[["H",10,"4230.00"],["H",20,"4231.90"]],"closes":{"25":"4232.76"},"cutoff":30,"atr":"8"}` | `{"zones":[["4229.95","4231.95",false,"RESISTANCE"]]}` |

#### `GV-G-ZN-13` · zonedeath
> G4 zone role AMBIGUOUS (D-038 addendum): if the latest contributing candle is BOTH a swing high and a swing low and both pivots join the same zone, neither is 'latest', so the role is AMBIGUOUS and the zone is excluded from AT_SUPPORT/AT_RESISTANCE and from every structural target (reported live=false) until a LATER single-type confirmed pivot establishes a role. Case 1: bar 20 is both (4230.30 high, 4229.60 low) -> AMBIGUOUS. Case 2: a later swing low at bar 30 re-establishes the zone as SUPPORT (zone recentred on the 4 pivots). Case 3: the same, then a close at bar 35 of 4229.14 (more than 0.40 below the bottom 4229.55) kills it. Case 4: an ambiguous candle that is NOT the latest pivot does not matter (latest = high at bar 20 -> RESISTANCE). Case 5: no death scan applies to an AMBIGUOUS zone (a close far below changes nothing).

| # | in | expected out |
|---|---|---|
| 1 | `{"swings":[["H",10,"4230.00"],["H",20,"4230.30"],["L",20,"4229.60"]],"closes":{},"cutoff":30,"atr":"4"}` | `{"zones":[["4229.50","4230.50",false,"AMBIGUOUS"]]}` |
| 2 | `{"swings":[["H",10,"4230.00"],["H",20,"4230.30"],["L",20,"4229.60"],["L",30,"4230.10"]],"closes":{},"cutoff":40,"atr":"4"}` | `{"zones":[["4229.55","4230.55",true,"SUPPORT"]]}` |
| 3 | `{"swings":[["H",10,"4230.00"],["H",20,"4230.30"],["L",20,"4229.60"],["L",30,"4230.10"]],"closes":{"35":"4229.14"},"cutoff":40,"atr":"4"}` | `{"zones":[["4229.55","4230.55",false,"SUPPORT"]]}` |
| 4 | `{"swings":[["H",10,"4230.00"],["L",10,"4229.70"],["H",20,"4230.30"]],"closes":{},"cutoff":30,"atr":"4"}` | `{"zones":[["4229.50","4230.50",true,"RESISTANCE"]]}` |
| 5 | `{"swings":[["H",10,"4230.00"],["H",20,"4230.30"],["L",20,"4229.60"]],"closes":{"25":"4220.00"},"cutoff":30,"atr":"4"}` | `{"zones":[["4229.50","4230.50",false,"AMBIGUOUS"]]}` |

