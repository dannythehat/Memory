# Portfolio Simulation golden vectors (GVP-0.1)

For `PORTFOLIO_RULES.md` v0.1. Each vector gives the strategies' virtual trades (already resolved: fill tick, quantised stop, exits) and the expected portfolio decisions. Defaults: EUR 10,000 start, EURUSD 1.25 (a fixture chosen so EUR amounts are exact), XAUUSD tick 0.01, USD 1.00 per tick per lot, 100 oz contract, lot step and minimum 0.01, server time UTC+1. Lots are rounded DOWN. Marks default to 'no floating P&L' unless ticks are listed. Every number below was derived by hand from the rules first and then compared with a scratch calculator (all 18 agree); the calculator is not stored (D-005).

#### `GV-PS-01`
> Base sizing. Equity 10,000; EURUSD 1.25; risk 1% = EUR 100 = USD 125; stop 1000 ticks -> 0.125 lot, rounded DOWN to 0.12. Realised risk 0.12 x 1000 / 1.25 = EUR 96.00. Caps are not binding. Exit at +2R (2000 ticks): USD 240 = EUR 192.00.

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t1 | HAMMER-BULL-v1.0/BASE | H1 | BUY | c1 | 3 | 10-05 10:00 | 4200.00 | 4190.00 | 10-05 10:30 4220.00 | ACCEPTED | 0.12 | 1 | 96.00 | 192.00 |

Final balance: **EUR 10192.00**

#### `GV-PS-01b`
> Commission: EUR 3.50 per lot per side. Same trade as GV-PS-01: 0.12 lot -> EUR 0.42 at entry and 0.42 at exit; P&L 192.00 - 0.84 = 191.16.

Config overrides: `commission_per_lot_side_eur=3.50`

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t1 | HAMMER-BULL-v1.0/BASE | H1 | BUY | c1 | 3 | 10-05 10:00 | 4200.00 | 4190.00 | 10-05 10:30 4220.00 | ACCEPTED | 0.12 | 1 | 96.00 | 191.16 |

Final balance: **EUR 10191.16**

#### `GV-PS-02a`
> Wide stop: 8000 ticks -> 125/8000 = 0.0156 -> 0.01 lot (the minimum lot; taken because lots = lots_risk). Realised risk EUR 64.00; stopped out: -EUR 64.00.

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t1 | KICKER-BULL-v1.0/BASE | D1 | BUY | c1 | 3 | 10-05 10:00 | 4200.00 | 4120.00 | 10-05 11:00 4120.00 | ACCEPTED | 0.01 | 1 | 64.00 | -64.00 |

Final balance: **EUR 9936.00**

#### `GV-PS-02b`
> Very wide stop: 30000 ticks -> 125/30000 = 0.0042 -> 0.00 lot, below the minimum -> SKIPPED_PORTFOLIO_MIN_LOT.

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t1 | KICKER-BULL-v1.0/BASE | MN1 | BUY | c1 | 3 | 10-05 10:00 | 4200.00 | 3900.00 | 10-05 11:00 3900.00 | SKIPPED_PORTFOLIO_MIN_LOT | - | - | - | - |

Final balance: **EUR 10000.00**

#### `GV-PS-03`
> Same-idea rule. Cluster c1 (H1 BUY): three signals; the one with the smallest verdict rank (rank 2, SRC-PS) is considered, the other two are DUPLICATE_CLUSTER. Cluster c2 (later): equal ranks, so a BASE signal beats a variant, and between BASE signals the smaller strategy id wins.

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a | HAMMER-BULL-v1.0/BASE | H1 | BUY | c1 | 3 | 10-05 10:00 | 4200.00 | 4190.00 | 10-05 10:30 4220.00 | SKIPPED_PORTFOLIO_DUPLICATE_CLUSTER | - | - | - | - |
| b | PINBAR-BULL-v1.0/BASE | H1 | BUY | c1 | 3 | 10-05 10:00 | 4200.00 | 4190.00 | 10-05 10:30 4220.00 | SKIPPED_PORTFOLIO_DUPLICATE_CLUSTER | - | - | - | - |
| c | HAMMER-BULL-v1.0/SRC-PS | H1 | BUY | c1 | 2 | 10-05 10:00 | 4200.00 | 4190.00 | 10-05 10:30 4220.00 | ACCEPTED | 0.12 | 1 | 96.00 | 192.00 |
| d | HAMMER-BULL-v1.0/SRC-PS | M15 | BUY | c2 | 3 | 10-05 11:00 | 4200.00 | 4190.00 | 10-05 11:30 4220.00 | SKIPPED_PORTFOLIO_DUPLICATE_CLUSTER | - | - | - | - |
| e | PINBAR-BULL-v1.0/BASE | M15 | BUY | c2 | 3 | 10-05 11:00 | 4200.00 | 4190.00 | 10-05 11:30 4220.00 | SKIPPED_PORTFOLIO_DUPLICATE_CLUSTER | - | - | - | - |
| f | HAMMER-BULL-v1.0/BASE | M15 | BUY | c2 | 3 | 10-05 11:00 | 4200.00 | 4190.00 | 10-05 11:30 4220.00 | ACCEPTED | 0.12 | 1 | 96.00 | 192.00 |

Final balance: **EUR 10384.00**

#### `GV-PS-04`
> Conflict rule. Same TF (M15) and signal bar, opposite directions: every member of both clusters is CONFLICT. A SELL on H1 (different TF, its own bar) is an independent idea and is taken (0.12 lot, stop 1000 ticks, target hit: +EUR 192.00).

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a | HAMMER-BULL-v1.0/BASE | M15 | BUY | c1 | 3 | 10-05 10:00 | 4200.00 | 4190.00 | 10-05 10:30 4220.00 | SKIPPED_PORTFOLIO_CONFLICT | - | - | - | - |
| b | SHOOTINGSTAR-BEAR-v1.0/BASE | M15 | SELL | c2 | 3 | 10-05 10:00 | 4200.00 | 4210.00 | 10-05 10:30 4180.00 | SKIPPED_PORTFOLIO_CONFLICT | - | - | - | - |
| c | EVENINGSTAR-BEAR-v1.0/BASE | H1 | SELL | c3 | 3 | 10-05 10:00 | 4200.00 | 4210.00 | 10-05 10:30 4180.00 | ACCEPTED | 0.12 | 1 | 96.00 | 192.00 |

Final balance: **EUR 10192.00**

#### `GV-PS-05`
> Direction cap (DIR_MAX overridden to 2.5% so scaling can occur, NOTIONAL_MAX to 100x so it does not interfere). Three BUYs, each 0.12 lot (EUR 96 risk). Equity is slightly below 10,000 because the open longs are marked at the BID (4200.00) while they filled at the ASK (4200.20). Third: headroom 2.5% x equity - 192 leaves 0.07 lot: at least half of the intended 0.12, so ACCEPTED_SCALED_DIRECTION. Fourth: headroom leaves 0.00 -> below the minimum -> SKIPPED_PORTFOLIO_DIRECTION_CAP.

Config overrides: `dir_max=0.025`, `notional_max=100`

Marks (bid/ask): 10-05 09:00 4200.00/4200.20

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S1-BULL-v1.0/BASE | H1 | BUY | c1 | 3 | 10-05 09:00 | 4200.20 | 4190.20 | 10-05 12:00 4220.20 | ACCEPTED | 0.12 | 1 | 96.00 | 192.00 |
| 2 | S2-BULL-v1.0/BASE | M30 | BUY | c2 | 3 | 10-05 09:30 | 4200.20 | 4190.20 | 10-05 12:00 4220.20 | ACCEPTED | 0.12 | 1 | 96.00 | 192.00 |
| 3 | S3-BULL-v1.0/BASE | M15 | BUY | c3 | 3 | 10-05 09:45 | 4200.20 | 4190.20 | 10-05 12:00 4220.20 | ACCEPTED_SCALED_DIRECTION | 0.07 | 1 | 56.00 | 112.00 |
| 4 | S4-BULL-v1.0/BASE | M5 | BUY | c4 | 3 | 10-05 10:00 | 4200.20 | 4190.20 | 10-05 12:00 4220.20 | SKIPPED_PORTFOLIO_DIRECTION_CAP | - | - | - | - |

Final balance: **EUR 10496.00**

#### `GV-PS-06`
> Gross heat counts both directions but the direction cap counts each side alone (HEAT_MAX overridden to 2.5%, NOTIONAL_MAX to 100x). Open BUY 0.12 (EUR 96) and SELL 0.12 (EUR 96) on different timeframes; a third BUY sees direction headroom 300 - 96 (plenty) but heat headroom 250 - 192: 0.07 lot -> ACCEPTED_SCALED_HEAT.

Config overrides: `heat_max=0.025`, `notional_max=100`

Marks (bid/ask): 10-05 09:00 4200.00/4200.20

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S1-BULL-v1.0/BASE | H1 | BUY | c1 | 3 | 10-05 09:00 | 4200.20 | 4190.20 | 10-05 12:00 4220.20 | ACCEPTED | 0.12 | 1 | 96.00 | 192.00 |
| 2 | S2-BEAR-v1.0/BASE | H4 | SELL | c2 | 3 | 10-05 09:30 | 4200.00 | 4210.00 | 10-05 12:00 4180.00 | ACCEPTED | 0.12 | 1 | 96.00 | 192.00 |
| 3 | S3-BULL-v1.0/BASE | M15 | BUY | c3 | 3 | 10-05 09:45 | 4200.20 | 4190.20 | 10-05 12:00 4220.20 | ACCEPTED_SCALED_HEAT | 0.07 | 1 | 56.00 | 112.00 |

Final balance: **EUR 10496.00**

#### `GV-PS-07a`
> Notional cap. Stop 200 ticks: lots_risk = 125/200 = 0.625 -> 0.62; notional per lot = 100 oz x 4200 / 1.25 = EUR 336,000; 15 x 10,000 / 336,000 = 0.4464 -> 0.44 lot, which is at least half of 0.62 -> ACCEPTED_SCALED_NOTIONAL, realised risk 0.44 x 200 / 1.25 = EUR 70.40.

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t1 | HAMMER-BULL-v1.0/BASE | M5 | BUY | c1 | 3 | 10-05 10:00 | 4200.00 | 4198.00 | 10-05 10:30 4204.00 | ACCEPTED_SCALED_NOTIONAL | 0.44 | 1 | 70.40 | 140.80 |

Final balance: **EUR 10140.80**

#### `GV-PS-07b`
> Notional cap, too tight: stop 100 ticks -> lots_risk 1.25; the cap allows 0.44, less than half of 1.25 -> SKIPPED_PORTFOLIO_NOTIONAL_CAP.

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t1 | HAMMER-BULL-v1.0/BASE | M1 | BUY | c1 | 3 | 10-05 10:00 | 4200.00 | 4199.00 | 10-05 10:30 4202.00 | SKIPPED_PORTFOLIO_NOTIONAL_CAP | - | - | - | - |

Final balance: **EUR 10000.00**

#### `GV-PS-08`
> Drawdown ladder. Eighteen consecutive stop-outs, three a day (the daily loss limit is never reached). Each entry is sized on current equity; once DD from the high-water mark (10,000) reaches 5% the risk is halved, at 10% quartered. The record shows the ladder multiplier and lots of every entry.

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | L1-BULL-v1.0/BASE | H1 | BUY | c1 | 3 | 10-05 09:00 | 4200.00 | 4190.00 | 10-05 09:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| 2 | L2-BULL-v1.0/BASE | H1 | BUY | c2 | 3 | 10-05 10:00 | 4200.00 | 4190.00 | 10-05 10:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| 3 | L3-BULL-v1.0/BASE | H1 | BUY | c3 | 3 | 10-05 11:00 | 4200.00 | 4190.00 | 10-05 11:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| 4 | L4-BULL-v1.0/BASE | H1 | BUY | c4 | 3 | 10-06 09:00 | 4200.00 | 4190.00 | 10-06 09:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| 5 | L5-BULL-v1.0/BASE | H1 | BUY | c5 | 3 | 10-06 10:00 | 4200.00 | 4190.00 | 10-06 10:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| 6 | L6-BULL-v1.0/BASE | H1 | BUY | c6 | 3 | 10-06 11:00 | 4200.00 | 4190.00 | 10-06 11:30 4190.00 | ACCEPTED | 0.11 | 1 | 88.00 | -88.00 |
| 7 | L7-BULL-v1.0/BASE | H1 | BUY | c7 | 3 | 10-07 09:00 | 4200.00 | 4190.00 | 10-07 09:30 4190.00 | ACCEPTED | 0.05 | 0.5 | 40.00 | -40.00 |
| 8 | L8-BULL-v1.0/BASE | H1 | BUY | c8 | 3 | 10-07 10:00 | 4200.00 | 4190.00 | 10-07 10:30 4190.00 | ACCEPTED | 0.05 | 0.5 | 40.00 | -40.00 |
| 9 | L9-BULL-v1.0/BASE | H1 | BUY | c9 | 3 | 10-07 11:00 | 4200.00 | 4190.00 | 10-07 11:30 4190.00 | ACCEPTED | 0.05 | 0.5 | 40.00 | -40.00 |
| 10 | L10-BULL-v1.0/BASE | H1 | BUY | c10 | 3 | 10-08 09:00 | 4200.00 | 4190.00 | 10-08 09:30 4190.00 | ACCEPTED | 0.05 | 0.5 | 40.00 | -40.00 |
| 11 | L11-BULL-v1.0/BASE | H1 | BUY | c11 | 3 | 10-08 10:00 | 4200.00 | 4190.00 | 10-08 10:30 4190.00 | ACCEPTED | 0.05 | 0.5 | 40.00 | -40.00 |
| 12 | L12-BULL-v1.0/BASE | H1 | BUY | c12 | 3 | 10-08 11:00 | 4200.00 | 4190.00 | 10-08 11:30 4190.00 | ACCEPTED | 0.05 | 0.5 | 40.00 | -40.00 |
| 13 | L13-BULL-v1.0/BASE | H1 | BUY | c13 | 3 | 10-09 09:00 | 4200.00 | 4190.00 | 10-09 09:30 4190.00 | ACCEPTED | 0.05 | 0.5 | 40.00 | -40.00 |
| 14 | L14-BULL-v1.0/BASE | H1 | BUY | c14 | 3 | 10-09 10:00 | 4200.00 | 4190.00 | 10-09 10:30 4190.00 | ACCEPTED | 0.05 | 0.5 | 40.00 | -40.00 |
| 15 | L15-BULL-v1.0/BASE | H1 | BUY | c15 | 3 | 10-09 11:00 | 4200.00 | 4190.00 | 10-09 11:30 4190.00 | ACCEPTED | 0.05 | 0.5 | 40.00 | -40.00 |
| 16 | L16-BULL-v1.0/BASE | H1 | BUY | c16 | 3 | 10-12 09:00 | 4200.00 | 4190.00 | 10-12 09:30 4190.00 | ACCEPTED | 0.05 | 0.5 | 40.00 | -40.00 |
| 17 | L17-BULL-v1.0/BASE | H1 | BUY | c17 | 3 | 10-12 10:00 | 4200.00 | 4190.00 | 10-12 10:30 4190.00 | ACCEPTED | 0.05 | 0.5 | 40.00 | -40.00 |
| 18 | L18-BULL-v1.0/BASE | H1 | BUY | c18 | 3 | 10-12 11:00 | 4200.00 | 4190.00 | 10-12 11:30 4190.00 | ACCEPTED | 0.02 | 0.25 | 16.00 | -16.00 |

Final balance: **EUR 8976.00**

#### `GV-PS-09`
> Drawdown halt (RISK_BASE overridden to 6% and the other caps opened up so the ladder and the 15% halt are reached in a few trades). One losing trade a day: DD 6.0%, 8.8%, 11.5%, 12.8%, 14.1%, then 15.4% after the Monday 12 October stop-out, which starts the halt: no entries for the rest of that day and the next 10 trading days (Tue 13 Oct ... Mon 26 Oct); trading resumes Tue 27 Oct at the x0.25 ladder step (DD is still >= 10%, so the halt is not re-armed). Signals on 13 Oct, 23 Oct and 26 Oct are SKIPPED_PORTFOLIO_DRAWDOWN_HALT.

Config overrides: `risk_base=0.06`, `heat_max=1`, `dir_max=1`, `notional_max=1000`

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | L1-BULL-v1.0/BASE | H1 | BUY | c1 | 3 | 10-05 10:00 | 4200.00 | 4190.00 | 10-05 10:30 4190.00 | ACCEPTED | 0.75 | 1 | 600.00 | -600.00 |
| 2 | L2-BULL-v1.0/BASE | H1 | BUY | c2 | 3 | 10-06 10:00 | 4200.00 | 4190.00 | 10-06 10:30 4190.00 | ACCEPTED | 0.35 | 0.5 | 280.00 | -280.00 |
| 3 | L3-BULL-v1.0/BASE | H1 | BUY | c3 | 3 | 10-07 10:00 | 4200.00 | 4190.00 | 10-07 10:30 4190.00 | ACCEPTED | 0.34 | 0.5 | 272.00 | -272.00 |
| 4 | L4-BULL-v1.0/BASE | H1 | BUY | c4 | 3 | 10-08 10:00 | 4200.00 | 4190.00 | 10-08 10:30 4190.00 | ACCEPTED | 0.16 | 0.25 | 128.00 | -128.00 |
| 5 | L5-BULL-v1.0/BASE | H1 | BUY | c5 | 3 | 10-09 10:00 | 4200.00 | 4190.00 | 10-09 10:30 4190.00 | ACCEPTED | 0.16 | 0.25 | 128.00 | -128.00 |
| 6 | L6-BULL-v1.0/BASE | H1 | BUY | c6 | 3 | 10-12 10:00 | 4200.00 | 4190.00 | 10-12 10:30 4190.00 | ACCEPTED | 0.16 | 0.25 | 128.00 | -128.00 |
| 7 | L7-BULL-v1.0/BASE | H1 | BUY | c7 | 3 | 10-13 10:00 | 4200.00 | 4190.00 | 10-13 10:30 4190.00 | SKIPPED_PORTFOLIO_DRAWDOWN_HALT | - | - | - | - |
| 8 | L8-BULL-v1.0/BASE | H1 | BUY | c8 | 3 | 10-23 10:00 | 4200.00 | 4190.00 | 10-23 10:30 4190.00 | SKIPPED_PORTFOLIO_DRAWDOWN_HALT | - | - | - | - |
| 9 | L9-BULL-v1.0/BASE | H1 | BUY | c9 | 3 | 10-26 10:00 | 4200.00 | 4190.00 | 10-26 10:30 4190.00 | SKIPPED_PORTFOLIO_DRAWDOWN_HALT | - | - | - | - |
| 10 | L10-BULL-v1.0/BASE | H1 | BUY | c10 | 3 | 10-27 10:00 | 4200.00 | 4190.00 | 10-27 10:30 4190.00 | ACCEPTED | 0.15 | 0.25 | 120.00 | -120.00 |

Final balance: **EUR 8344.00**

#### `GV-PS-10`
> Daily loss limit 3% of the day's opening equity. Tue 6 Oct: four stop-outs take the day down 3.84% (after three, 2.88% < 3%, so the fourth is still allowed); the fifth signal that day is SKIPPED_PORTFOLIO_DAILY_LOSS. On Wed 7 Oct the day-opening equity resets and the sixth is taken.

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | L1-BULL-v1.0/BASE | H1 | BUY | c1 | 3 | 10-06 08:00 | 4200.00 | 4190.00 | 10-06 08:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| 2 | L2-BULL-v1.0/BASE | H1 | BUY | c2 | 3 | 10-06 09:00 | 4200.00 | 4190.00 | 10-06 09:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| 3 | L3-BULL-v1.0/BASE | H1 | BUY | c3 | 3 | 10-06 10:00 | 4200.00 | 4190.00 | 10-06 10:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| 4 | L4-BULL-v1.0/BASE | H1 | BUY | c4 | 3 | 10-06 11:00 | 4200.00 | 4190.00 | 10-06 11:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| 5 | L5-BULL-v1.0/BASE | H1 | BUY | c5 | 3 | 10-06 12:00 | 4200.00 | 4190.00 | 10-06 12:30 4190.00 | SKIPPED_PORTFOLIO_DAILY_LOSS | - | - | - | - |
| 6 | L6-BULL-v1.0/BASE | H1 | BUY | c6 | 3 | 10-07 08:00 | 4200.00 | 4190.00 | 10-07 08:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |

Final balance: **EUR 9520.00**

#### `GV-PS-11`
> Partial exits: 0.12 lot, 60% partial at +1R (4210.00), rest at 4230.00. Partial lots = floor(0.12 x 0.6 = 0.072 to the lot step) = 0.07 -> USD 70 = EUR 56.00; remaining 0.05 lot at +3R: USD 150 = EUR 120.00. Total EUR 176.00. Second trade: 0.01 lot: 60% of it rounds down to 0.00, so the partial is not executed and the final exit closes the whole 0.01 lot (+8000 ticks = USD 80 = EUR 64.00).

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t1 | EVENINGSTAR-BEAR-v1.0/BASE | H1 | BUY | c1 | 3 | 10-05 10:00 | 4200.00 | 4190.00 | 10-05 10:30 4210.00 (0.6); 10-05 11:00 4230.00 (0.4) | ACCEPTED | 0.12 | 1 | 96.00 | 176.00 |
| t2 | KICKER-BULL-v1.0/BASE | D1 | BUY | c2 | 3 | 10-05 12:00 | 4200.00 | 4120.00 | 10-05 12:30 4240.00 (0.6); 10-05 13:00 4280.00 (0.4) | ACCEPTED | 0.01 | 1 | 64.00 | 64.00 |

Final balance: **EUR 10240.00**

#### `GV-PS-12`
> EUR conversion. EURUSD 1.25 at the first entry (0.12 lot), 1.60 at its exit: +2R = USD 240 / 1.60 = EUR 150.00 (sizing used the entry-time rate, P&L the exit-time rate). Second trade sized at 1.60 with equity 10,150: 0.01 x 10,150 x 1.60 / 1000 = 0.1624 -> 0.16 lot; stopped out: USD 160 / 1.60 = -EUR 100.00 -> balance 10,050.00.

EURUSD changes: 10-05 10:15 -> 1.60

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t1 | HAMMER-BULL-v1.0/BASE | H1 | BUY | c1 | 3 | 10-05 10:00 | 4200.00 | 4190.00 | 10-05 10:30 4220.00 | ACCEPTED | 0.12 | 1 | 96.00 | 150.00 |
| t2 | HAMMER-BULL-v1.0/BASE | H1 | BUY | c2 | 3 | 10-05 12:00 | 4200.00 | 4190.00 | 10-05 12:30 4190.00 | ACCEPTED | 0.16 | 1 | 100.00 | -100.00 |

Final balance: **EUR 10050.00**

#### `GV-PS-13`
> Queue order at the same instant (HEAT_MAX overridden to 1.25% so only one 0.12-lot trade fits). Entries at the same instant: higher timeframe first, then rank. H4 BUY (rank 3) is processed before the H1 BUY (rank 1): H4 taken (0.12), H1 gets 0.03 lot < half of 0.12 -> SKIPPED_PORTFOLIO_HEAT_CAP. Later, at another instant, two H1 signals with different ranks: the rank-1 signal is processed first and taken; the rank-3 one is skipped.

Config overrides: `heat_max=0.0125`

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a | A-BULL-v1.0/BASE | H4 | BUY | c1 | 3 | 10-05 10:00 | 4200.00 | 4190.00 | 10-05 10:30 4220.00 | ACCEPTED | 0.12 | 1 | 96.00 | 192.00 |
| b | B-BULL-v1.0/BASE | H1 | BUY | c2 | 1 | 10-05 10:00 | 4200.00 | 4190.00 | 10-05 10:30 4220.00 | SKIPPED_PORTFOLIO_HEAT_CAP | - | - | - | - |
| c | C-BULL-v1.0/BASE | H1 | BUY | c3 | 3 | 10-05 12:00 | 4200.00 | 4190.00 | 10-05 12:30 4220.00 | SKIPPED_PORTFOLIO_HEAT_CAP | - | - | - | - |
| d | D-BULL-v1.0/BASE | H1 | BUY | c4 | 1 | 10-05 12:00 | 4200.00 | 4190.00 | 10-05 12:30 4220.00 | ACCEPTED | 0.12 | 1 | 96.00 | 192.00 |

Final balance: **EUR 10384.00**

#### `GV-PS-14`
> Floating equity is used for sizing. RISK_BASE 3%, HEAT/DIR 10%, notional cap 100x (overridden). First BUY: 0.37 lot (stop 1000 ticks; 375/1000 = 0.375). Marked at BID 4192.00 while open (-800 ticks x 0.37 = -USD 296 = -EUR 236.80), equity 9,763.20. The second BUY is sized on that equity: 0.03 x 9,763.20 x 1.25 / 1000 = 0.366 -> 0.36 lot (not 0.37).

Config overrides: `risk_base=0.03`, `heat_max=0.10`, `dir_max=0.10`, `notional_max=100`

Marks (bid/ask): 10-05 10:00 4199.80/4200.00; 10-05 10:30 4192.00/4192.20

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t1 | A-BULL-v1.0/BASE | H1 | BUY | c1 | 3 | 10-05 10:00 | 4200.00 | 4190.00 | 10-05 14:00 4220.00 | ACCEPTED | 0.37 | 1 | 296.00 | 592.00 |
| t2 | B-BULL-v1.0/BASE | M30 | BUY | c2 | 3 | 10-05 11:00 | 4200.00 | 4190.00 | 10-05 14:00 4220.00 | ACCEPTED | 0.36 | 1 | 288.00 | 576.00 |

Final balance: **EUR 11168.00**

#### `GV-PS-15`
> High-water mark rises with profit. Monday: two +2R winners (EUR +192 each) take equity to 10,384, so the end-of-day high-water mark is 10,384. Seven stop-outs follow (Tue 3, Wed 3, Thu 1). Drawdown is measured from 10,384, not from the starting 10,000: the first six entries are full size (equity 10,384 down to 9,904 is 4.6%), and the sixth stop-out takes equity to 9,808, a 5.55% drawdown from 10,384 (it would only be 1.9% from 10,000), so the seventh entry is sized at x0.5 (0.06 lot).

| trade | strategy | TF | side | cluster | rank | fill | entry | stop | exits | decision | lots | ladder | risk EUR | P&L EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| w1 | A-BULL-v1.0/BASE | H1 | BUY | c1 | 3 | 10-05 09:00 | 4200.00 | 4190.00 | 10-05 09:30 4220.00 | ACCEPTED | 0.12 | 1 | 96.00 | 192.00 |
| w2 | B-BULL-v1.0/BASE | H1 | BUY | c2 | 3 | 10-05 10:00 | 4200.00 | 4190.00 | 10-05 10:30 4220.00 | ACCEPTED | 0.12 | 1 | 96.00 | 192.00 |
| l1 | Ll1-BULL-v1.0/BASE | H1 | BUY | cl1 | 3 | 10-06 09:00 | 4200.00 | 4190.00 | 10-06 09:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| l2 | Ll2-BULL-v1.0/BASE | H1 | BUY | cl2 | 3 | 10-06 10:00 | 4200.00 | 4190.00 | 10-06 10:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| l3 | Ll3-BULL-v1.0/BASE | H1 | BUY | cl3 | 3 | 10-06 11:00 | 4200.00 | 4190.00 | 10-06 11:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| l4 | Ll4-BULL-v1.0/BASE | H1 | BUY | cl4 | 3 | 10-07 09:00 | 4200.00 | 4190.00 | 10-07 09:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| l5 | Ll5-BULL-v1.0/BASE | H1 | BUY | cl5 | 3 | 10-07 10:00 | 4200.00 | 4190.00 | 10-07 10:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| l6 | Ll6-BULL-v1.0/BASE | H1 | BUY | cl6 | 3 | 10-07 11:00 | 4200.00 | 4190.00 | 10-07 11:30 4190.00 | ACCEPTED | 0.12 | 1 | 96.00 | -96.00 |
| l7 | Ll7-BULL-v1.0/BASE | H1 | BUY | cl7 | 3 | 10-08 09:00 | 4200.00 | 4190.00 | 10-08 09:30 4190.00 | ACCEPTED | 0.06 | 0.5 | 48.00 | -48.00 |

Final balance: **EUR 9760.00**
