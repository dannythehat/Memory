# GoldThinker — Portfolio Simulation rules (v0.2)

Status: **v0.2, 2026-09-30, RESEARCH APPROVED — Claude + ChatGPT (D-042)** with ChatGPT's eight amendments applied. Research rule; nothing is coded. Parameters below
are **research thresholds chosen for caution, not results** (with a $10 stop and 1% risk, one trade is about 4x equity in notional, so `NOTIONAL_MAX = 15x` sits just above the 3-trade direction cap). Test vectors: `tests/portfolio/` (GVP-0.2). The demo account is a dedicated EUR 10,000 account (owner-created); hedging/netting, contract size, tick value, leverage/margin, commission and swap are still queried from the MT5 account during integration, before the Vantage mirror is enabled.
**Nothing here authorises real money (D-035).** The strategy ledgers keep the owner's D-004 exactly (1% risk per paper trade,
fixed); this document only adds what a *portfolio* needs.

## 1. Three things, kept apart (extends D-024)

| | Purpose | Unit | Sizing | Compounds? |
|---|---|---|---|---|
| **Strategy ledger** (one per pattern x side x TF x variant x version) | Compare a Hammer M15 with an Engulfing H1 fairly | **R** (display: 1R = 100 reference units, currency-neutral) | fixed 1R, D-004/D-007 | no |
| **Portfolio Simulation (PS)** | What one account would do if it took these signals together | **EUR**, starts at **EUR 10,000** | this document | yes |
| **Vantage demo** (dedicated GoldThinker account, EUR 10,000 per ChatGPT; **to be confirmed from the account itself**) | Execution mirror of the PS | EUR | copies the PS decisions | - |

- A PS trade follows **the same plan as the strategy's virtual trade** (same fill tick, quantised stop and target, exit rules);
  only the lot size differs (or the trade is not taken). Lot rounding can change partial-exit proportions (a 0.01-lot position
  cannot take a partial at all), so its result in R can differ slightly. **Every closed PS trade stores `strategy_R` (the strategy
  ledger's R), `portfolio_R` (its gross USD result divided by its realised risk in USD) and `rounding_divergence_R =
  portfolio_R - strategy_R`.** The PS answers what the strategy ledgers cannot: how much to size, and which signals to take together.
- Every signal a PS does **not** take keeps its full outcome in its own strategy ledger, and the PS records what it skipped and
  the R those skipped trades would have made (the "opportunity cost of the caps").
- The mirror never changes the PS: any difference between the demo account and the PS (slippage, rejected order, different fill)
  is logged as `MIRROR_DIVERGENCE`; the PS stays the reference.

## 2. Portfolio instances

- **PS-EXPLORE** starts with the experiment: every enabled strategy is eligible. It is **permanently mechanical**: its selection
  rules never use any evidence (no verdict, rank, review result or later data), and it never changes after it starts. It answers
  "what would the unfiltered machine have done?" and says nothing about any strategy's quality (short timeframes signal more and
  crowd the caps first).
- **PS-CANDIDATE** is evidence-selected and **never runs retrospectively**. After a validation cohort reaches its final verdict,
  the PASS-STRONG strategy set is frozen in a **`portfolio_manifest`** (strategy list, and for each strategy its validation lower
  confidence bound and stressed expectancy, plus the versions and the freeze time). PS-CANDIDATE starts at the **first executable
  tick strictly after the manifest time**, with `PS_START` EUR. Any signal that filled before that tick is ignored
  (`IGNORED_BEFORE_PORTFOLIO_START`), even if it is still open, and nothing before it counts toward candidate-portfolio results.
- Each instance has its own balance, high-water mark and counters. Instances are never merged.

## 3. Currency (EUR account, USD instrument)

- XAUUSD profit is in USD. **Tick value in account currency** comes from the account/instrument specification when the broker
  publishes it; otherwise it is `tick_value_usd / EURUSD` with `EURUSD` = the mid of the latest EURUSD tick at or before the time
  (the feed must carry EURUSD, or the broker's dynamic tick value; **TO CONFIRM**). The rate used is stored on every decision.
- **Sizing** converts the risk budget to USD at the decision-time rate. **Each realised P&L** (each partial and the final exit) is
  converted at the rate at that exit tick. Commission and swap follow the account specification (G9) in account currency.
- There is no separate currency-exchange position: the balance is EUR and the only FX effect is the conversion at each close.

## 4. Parameters (research thresholds)

| Name | Value | Meaning |
|---|---|---|
| `PS_START` | EUR 10,000 | starting balance (the dedicated demo account) |
| `RISK_BASE` | 1.0% of current equity | risk budget of one taken trade before throttles (owner's D-004 figure) |
| `HEAT_MAX` | 4% of equity | total open risk (all positions) |
| `DIR_MAX` | 3% of equity | open risk in one direction (all BUY, or all SELL) |
| `NOTIONAL_MAX` | 15 x equity | gross open notional (contract size x price x lots, in EUR) - **the maximum open XAU exposure** |
| `MIN_FRACTION` | 0.5 | a trade is taken at least at half its intended size, or not at all |
| `DAILY_LOSS` | 3% of the day's opening equity | no new entries for the rest of that server day |
| Drawdown ladder | DD < 5%: x1.0; 5% <= DD < 10%: x0.5; DD >= 10%: x0.25 | multiplies `RISK_BASE` |
| `DD_HALT` | DD >= 15% | no new entries for 10 server trading days, then trading resumes at the ladder multiplier |

DD = `1 - equity / high-water mark`. Equity = balance + floating P&L (longs marked at the BID, shorts at the ASK, latest tick
at or before the time). The high-water mark starts at `PS_START` and is raised to the **end-of-server-day equity** each day
(so intrabar spikes cannot set it). The halt is edge-triggered, evaluated at **every portfolio event (entry decisions and exits)**, and re-armed when DD falls below 10%. Blocked: the rest of the trigger day and the next **10 broker trading days**. A broker trading day is a server day with at least one XAUUSD market-open interval in the broker calendar (G0); a full-day closure (holiday) does not consume a halt day. The day's opening equity
is the equity at the server-day boundary (G0). **Open risk of an existing position is measured from the CURRENT executable price to its stop**: a long's downside is `current BID - stop`, a short's is `stop - current ASK` (never below zero), times remaining lots, tick value and the decision-time rate. A position that is well in profit therefore carries more risk than its original 1R. A **new** position's risk is fill-to-stop. (If no tick has been seen since a position opened, its fill price stands in; this only occurs in isolated test vectors.) **Open notional** is recomputed at every decision from the current price (mid) and the current EURUSD; positions never keep an old notional. There are no trailing stops in v1.

## 5. The decision for each signal

A signal reaches the PS at its virtual trade's **fill tick** (`entry_eligible_time` or the confirmation / stop-entry fill). Events at
the same instant are processed **exits first, then entries**. Entries at the same instant are processed **one at a time in
`signal_cluster_id` order** (the text `TF|SIDE|signal bar UTC`, sorted ascending as text; deliberately neutral: no timeframe or
strategy is favoured on evidence). **After every accepted entry the state is updated at once** (commission charged, the position
marked at the current executable price so its spread cost is in equity, open risk, direction risk, notional and the drawdown
ladder recomputed) before the next entry is considered, so simultaneous signals cannot each see the same unused capacity.

1. **Eligibility:** the strategy belongs to the instance's set; otherwise the PS ignores the signal.
2. **Same-idea rule (signal clusters).** Signals with the same `signal_cluster_id` (same TF, direction and signal bar) are one
   idea. Only the highest-ranked member may be considered (PS-EXPLORE: a BASE strategy before a source variant, then strategy id
   ascending; PS-CANDIDATE: section 6);
   every other member is `SKIPPED_PORTFOLIO_DUPLICATE_CLUSTER`. If the winner is then rejected by a later step, the others are
   **not** reconsidered.
3. **Conflict rule.** If two clusters on the same TF and signal bar point in opposite directions, every member of both is
   `SKIPPED_PORTFOLIO_CONFLICT`. Opposite signals on different timeframes, or at different times, are independent ideas and are
   allowed (the account is assumed to be a **hedging** account; if it is netting the rule must be rewritten, **TO CONFIRM**).
4. **Halt:** if a drawdown halt is active -> `SKIPPED_PORTFOLIO_DRAWDOWN_HALT`.
5. **Daily loss:** if `(day-open equity - equity) / day-open equity >= DAILY_LOSS` -> `SKIPPED_PORTFOLIO_DAILY_LOSS`.
6. **Sizing.** `equity_eur` now; `stop_ticks = |entry - stop| / tick_size` (quantised prices, G13).
   - `lots_risk = floor_to_lot_step( RISK_BASE x ladder x equity_eur x fx / (stop_ticks x tick_value_usd) )`.
   - `lots_dir`, `lots_heat`, `lots_notional`: the same conversion applied to the remaining headroom
     (`DIR_MAX x equity - same-direction open risk`, `HEAT_MAX x equity - total open risk`,
     `NOTIONAL_MAX x equity - open notional`), rounded down to the lot step.
   - `lots = min(lots_risk, lots_dir, lots_heat, lots_notional)`; the binding cap is the one that is smallest (ties: direction, heat,
     notional, risk).
   - If `lots_risk < min_lot` -> `SKIPPED_PORTFOLIO_MIN_LOT`. Else if `lots < min_lot` or `lots < MIN_FRACTION x lots_risk` ->
     `SKIPPED_PORTFOLIO_<binding cap>` (`DIRECTION_CAP`, `HEAT_CAP`, `NOTIONAL_CAP`). Else the trade is taken:
     `ACCEPTED` when `lots = lots_risk`, `ACCEPTED_SCALED_<cap>` otherwise.
   - Rounding is always **down**, so realised risk never exceeds the budget.
7. **Exits.** The position follows the virtual trade's stop, target, partials, MAX_HOLD and closures exactly. Partial lots =
   floor(lots x fraction to lot step); if that is zero the partial is not executed and the final exit closes everything.
8. **No look-ahead:** every input is the state at the fill tick; skipped trades are not re-tried later.

## 6. Priority

- **PS-EXPLORE:** no evidence, ever. Within a cluster: BASE before source variant, then strategy id ascending. Across clusters at
  one instant: `signal_cluster_id` order (section 5).
- **PS-CANDIDATE:** every member is PASS-STRONG. Within a cluster, rank by the values **frozen in the portfolio manifest**: highest
  validation lower confidence bound first, then highest stressed expectancy, then strategy id ascending. No later data can change
  the rank. Across clusters at one instant: `signal_cluster_id` order.

## 7. Answers to the questions this document exists for

- **14 valid strategies signal together?** At most one per signal cluster is considered; then heat (4%), direction (3%) and
  notional (15x) caps decide how many are taken and at what size; the rest are skipped with a reason and their opportunity cost recorded.
- **Aggregate risk?** 4% open, 3% one direction, at 1% base risk per trade (about 3-4 trades at full size).
- **Seven signals that are the same gold move?** Same candle and TF: one trade (cluster rule). Different TFs the same move:
  the direction cap stops the stack at about 3 full-size trades.
- **M5 Hammer and M5 Dragonfly on the same candle?** One idea, one trade (higher-ranked member); the other keeps its own ledger.
- **Sizing after drawdown?** The ladder halves, then quarters the risk; a 15% drawdown halts entries for 10 trading days.
- **Opposing BUY and SELL?** Same TF and bar: both skipped. Otherwise both may exist within the gross-heat cap (a hedging account).
- **Maximum open XAU exposure?** 15 x equity in notional: EUR 150,000, about 41-45 oz (0.41-0.45 lot) at a 4,200 price and EURUSD 1.16-1.25. At a 1% risk and a $10 stop each trade is about 4x equity, so the direction cap (3 trades) binds first; the notional cap binds for stops tighter than about $8 (M1-M5) and scales those positions down.
- **USD gold P&L in a EUR account?** Section 3.

## 8. Reporting

The hub's PS panel shows: balance (EUR), return %, max drawdown %, high-water mark, current ladder multiplier, open trades with
risk and notional, gross/net exposure now and at peak, taken / scaled / skipped counts **by reason**, the R the skipped
trades would have made, daily P&L, and `MIRROR_DIVERGENCE` counts. Never blended with the strategy ledgers (D-024).

## 9. To query from the MT5 account during integration (before the mirror is enabled)

The account is a dedicated EUR 10,000 GoldThinker account (settled). Still to query: hedging vs netting; the broker's tick value / EURUSD conversion; margin requirement and
maximum leverage for XAUUSD (a margin cap `SKIPPED_PORTFOLIO_MARGIN` will be added once known); commission and swap
in account currency; whether the feed can carry EURUSD.

## 10. Not decided here

Any live-account sizing, risk limits or copying to a real account (owner only). Position management the sources do not give
(trailing stops, break-even moves) is not simulated in v1.
