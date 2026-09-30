# GoldThinker — Discovery and validation rules (v0.2)

Status: **v0.2, 2026-09-30, RESEARCH APPROVED — Claude + ChatGPT (D-041)**, with ChatGPT's eight amendments applied. Research
rule; nothing is coded. It replaces the "still open" item 3 of `CANDLE_SPEC_V1.md`. It builds on D-011 (no pooling), D-012
(STOP FIRST), D-018/D-019 (discovery -> freeze -> validation; survival gates). **No outcome of these rules authorises real
money; only the owner can (D-035).**

## 1. What is tested

- **Unit:** one strategy = pattern x side x timeframe x variant x rule version. About 657 exist (spec section 2).
- **Statistic:** net R per closed trade after spread, commission and swap (G9), using the conservative STOP FIRST
  resolution for ambiguous bars (D-012). Trades with `PENDING_COST_SPEC` are excluded (and counted in the report).
- **Layer:** the uniform BASE baseline (Layer B) and each source-normalized variant (Layer C) are each their own
  strategies. RAW behaviour (Layer A) is descriptive and never passes or fails anything.
- **Never shown as a headline:** win rate. Reported are n, expectancy (mean net R), profit factor, max drawdown in R,
  and the confidence bounds below.
- **Independence:** trades are not independent (overlapping signals, one macro day moving several patterns).
  Everything below therefore resamples **whole days**, not trades.
- **Which day a trade belongs to (amendment 1):** the **server trading day containing its `signal_time`** (G0), not the day
  it closed. Trades that arise from one market episode stay together even if they close on different days. The same
  assignment is used for the bootstrap, the "remove the best day" check (V4) and the per-month tests.
- **Day series:** every calendar day (server time) of the window is in the series; days with no signals contribute
  zero R and zero trades but stay in the resampling pool.
- **Trades still open at a review:** discovery reviews (section 2) use trades closed by the review date only. A validation
  verdict (section 4) is computed after every trade whose signal time lies in the window has closed, waiting at most 10
  trading days after the window ends; any trade still open then is closed at the market (bid for longs, ask for shorts),
  tagged `CLOSED_AT_REVIEW` and counted. (Long-timeframe strategies whose MAX_HOLD runs longer will simply carry that tag.)

## 2. Stage 1 - Discovery (forward paper trading)

Uses the gates proposed in D-019, unchanged:

| Review | Min trades | Kill if | Continue if |
|---|---|---|---|
| Month 1 | 20 | expectancy <= -0.20R, or PF < 0.80, or drawdown > 15R | otherwise |
| Month 2 | 40 | (M1 kill tests still apply) | expectancy > 0, PF >= 1.05, DD <= 12R |
| Month 3 | 75 | - | **candidate** if expectancy >= +0.10R, PF >= 1.20, DD <= 10R, positive in 2 of the last 3 completed calendar months, **and** the 90% one-sided day-block bootstrap lower bound of expectancy > 0 |

Rules that make the numbers honest:

1. A strategy with fewer trades than the minimum at a review is **UNKNOWN** (< 30 trades) or **PRELIMINARY**
   (30-74). It is not killed and not promoted; it keeps accumulating on the same rule version. Its discovery review
   happens when it reaches 75 trades, or at month 12, whichever is first (then it ends `INSUFFICIENT_DATA`). Slow
   strategies (D1, W1, MN1) will mostly end this way; that is a finding, not a failure of the rules.
2. **Delayed reviews (amendment 8).** For a review held after month 3, "positive in 2 of 3 months" means the **three most
   recent completed calendar months immediately before the review date**. A month is positive if the sum of net R of the
   trades signalled in it is strictly greater than zero; a month with no trades is not positive. The same definition is
   used at month 3.
3. **Killed never means stopped (amendment 7).** A strategy that hits a kill gate becomes
   `KILLED_CURRENT_DISCOVERY_COHORT`: it cannot be promoted into that cohort, but GoldThinker keeps recording every
   occurrence and virtual trade for it indefinitely on the same rule version. Nothing recorded is ever thrown away. Only
   trades after a strategy's freeze can count as validation evidence, so the extra data never contaminates the formal test.
4. Killed and unknown strategies stay in the count `K` (about 657): the number of things looked at is published next to
   any survivor.
5. Expected false candidates: if all 657 strategies had zero edge and all reached 75 trades, the bootstrap bound alone
   would let through about 5% (about 33); the other gates cut that, but it is the reason discovery **selects** and never
   **proves**. Nothing at this stage may be called "profitable".

## 3. Freeze: one validation cohort at a time (amendment 4)

Survivors are frozen into a **validation cohort**, recorded in a manifest committed to this repository:

`cohort_id`, `freeze_time`, `m` (the number of strategies), the exact strategy list, the alpha budget (section 4), the
spec / golden-vector-pack / detector versions, the gate values, and `K`.

- Once frozen, **`m` never changes**. A strategy that qualifies later waits for the next cohort; it is never added to an
  existing statistical family. For the first GoldThinker study there is one cohort, formed after discovery.
- No rule, parameter, threshold, timeframe or variant may change after freezing. Any change is a **new rule version and a new
  sample** (D-011) and cannot inherit validation credit.
- Validation uses **only trades whose `signal_time` is after `freeze_time`**. Discovery trades are never reused.
- The error rates below hold **within each cohort**. The number of cohorts run is published with every result.

## 4. Stage 2 - Validation (untouched period, two looks)

Two looks at the same untouched, post-freeze data (amendment 3):

| Look | Data used | Holm family-wise alpha | BY false-discovery q |
|---|---|---|---|
| **Interim, month 3** | months 1-3 | **0.01** (20% of 0.05) | **0.02** (20% of 0.10) |
| **Final, month 6** | **months 1-6** (all post-freeze data, not just months 4-6) | **0.04** (80% of 0.05) | **0.08** (80% of 0.10) |

A strategy that passes the interim look keeps that verdict (an early pass). A strategy that neither passes nor fails at the
interim look goes to the final look. A `FAIL` is allowed at the interim look (stopping for futility cannot inflate the
false-positive rate). The family stays all `m` cohort strategies at both looks. Alpha is spent once; the two-look total
never exceeds 0.05 (Holm) or 0.10 (BY).

**Per-strategy checks** (all of V1-V5 must hold for any PASS):

| # | Check | Value |
|---|---|---|
| V1 | Sample | at least **100** closed trades (of the data used at that look) |
| V2 | Practical size | expectancy >= **+0.10R**, PF >= **1.20** |
| V3 | Drawdown | max drawdown <= **10R** over the data used |
| V4 | Not one lucky day | expectancy stays >= **+0.05R** after deleting the single best signal day |
| V5 | Cost stress | expectancy >= **0** under the adverse replay below |
| V6 | Statistical evidence | one-sided day-block bootstrap test of H0: expectancy <= 0 (section 5), p-value adjusted for `m` |

**V5 - adverse-cost replay (amendment 6).** Execution is replayed, not just the final P&L rescaled:

- The stored **BID path is unchanged** (it drives candle formation, so the same signals occur).
- `stressed_ask = original_bid + 1.5 x original_spread`, tick by tick (bars-only fallback trades: apply the same rule to
  each ASK bar field).
- Re-run the whole chain on the stressed path: entry price -> A-30 quantisation -> entry-beyond-stop check -> R distance ->
  lot sizing -> stop / target hits -> partials -> MAX_HOLD -> final P&L.
- Commission is multiplied by **1.5**.
- Swap: a **negative** swap charge is multiplied by **2** (twice as costly); a **positive** swap credit is set to **zero**.
- A trade that the stressed replay would skip (for example entry beyond the stop) is excluded from the stressed set and
  counted; if more than 5% of the trades are excluded, V5 fails. (This 5% cap is Claude's addition; ChatGPT may challenge it.)

**Verdicts**

- **PASS-STRONG:** V1-V5 hold and the bootstrap p-value survives **Holm** at that look's alpha (valid under any dependence
  between strategies, which matters because they fire on the same candles).
- **PASS-WEAK (amendment 5):** V1-V5 hold and the p-value survives **Benjamini-Yekutieli** at that look's q but not Holm.
  BY, unlike ordinary BH, keeps its guarantee under arbitrary dependence. PASS-WEAK is a research label only and **can never
  become a live candidate**.
- **FAIL:** at >= 100 trades, expectancy <= 0 or PF < 1.0 or V3 violated; or, at the final look, the 80% one-sided
  upper bound of expectancy is below +0.05R.
- **INCONCLUSIVE:** anything else at the interim look. At the final look it becomes `NOT_PROVEN` (treated as FAIL for
  decisions; it can re-enter only through a new rule version and a new discovery).
- Holm: order the `m` p-values ascending; reject `p_(i)` while `p_(j) <= alpha / (m - j + 1)` for all `j <= i`.
  BY: with `c(m) = sum_{i=1..m} 1/i`, reject the `k` smallest p-values where `k` is the largest `i` with `p_(i) <= i q / (m c(m))`.

Failed and not-proven strategies keep being observed (section 2, rule 3); their formal verdict simply stays failed or not proven.
Only **PASS-STRONG** strategies may be put to the owner as live candidates, and even then the recommendation requires the
Portfolio Simulation results (`PORTFOLIO_RULES.md`), a live-account risk decision, and the owner's explicit approval.

## 5. The bootstrap (deterministic definition)

Both variants use the same day series, statistic, replicate count and seed system.

- **Statistic:** `E = sum(R) / count(trades)` (ratio estimator over the resampled days).
- **Seed:** SHA-256 of the cohort manifest text + strategy id + look name + the bootstrap name; the generator (PCG64) is named in the report.
- **Replicates:** `B = 10,000`. If a replicate contains zero trades, **redraw it**.
- **p-value (H0: E <= 0):** centre each day (subtract `E_hat` x that day's trade count), resample, and let
  `p = (1 + #{E* >= E_hat}) / (B + 1)`.
- **Bounds:** the corresponding percentiles of the uncentred resampled `E*`.

**A. 1-day bootstrap:** draw `N_days` days with replacement.

**B. 5-day circular moving-block bootstrap (amendment 2):** build every consecutive 5-calendar-day block of the day series
(block `i` = days `i, i+1, ..., i+4`, wrapping past the end of the window back to day 0); draw block start positions
uniformly with replacement; concatenate blocks until at least `N_days` days; truncate to exactly `N_days`.

**Verdict p-value:** the **larger** of A and B. The same two-bootstrap rule applies to the 90% discovery bound (larger p / lower bound of the two).

## 6. What sample sizes this implies (planning guide, not a result)

This is an **optimistic IID approximation and a lower bound**: it assumes trades are independent with trade-R standard
deviation about 1.5 (a 2R target / 1R stop strategy near breakeven), one-sided test, 80% power, normal approximation. Real day
clustering (section 1) generally needs more observations. Trades needed to detect a true expectancy:

| Holm family size `m` | Look (alpha) | +0.10R | +0.15R | +0.20R | +0.30R |
|---|---|---|---|---|---|
| 1 | interim (0.01) | 2,258 | 1,004 | 565 | 251 |
| 1 | final (0.04) | 1,512 | 672 | 378 | 168 |
| 10 | interim | 3,478 | 1,546 | 870 | 386 |
| 10 | final | 2,746 | 1,221 | 687 | 305 |
| 30 | interim | 4,054 | 1,802 | 1,013 | 450 |
| 30 | final | 3,327 | 1,479 | 832 | 370 |

Consequences, stated plainly: a true edge of +0.10R cannot be proven in six months by any strategy that trades a few times a
day; only frequent patterns on the short timeframes can reach several hundred trades, and most survivors will end
`INCONCLUSIVE` or `NOT_PROVEN`. That is the correct behaviour: the rules would rather leave a real edge unproven than approve
a false one. V1 (100 trades) is a floor, not evidence; V6 carries the proof burden.

## 7. Reporting and the hub

Every review publishes, for each strategy: n, expectancy with the bootstrap interval, PF, drawdown, stage and verdict, and for
the whole exercise `K`, `m`, `cohort_id`, the number killed, the number unknown and the expected number of false candidates.
Strategies with too little data show "NOT ENOUGH DATA" (D-023). Verdict labels: `UNKNOWN`, `PRELIMINARY`,
`KILLED_CURRENT_DISCOVERY_COHORT`, `CANDIDATE`, `PASS-STRONG`, `PASS-WEAK`, `INCONCLUSIVE`, `NOT_PROVEN`, `FAIL`,
`INSUFFICIENT_DATA`.

## 8. Not decided here

- Anything about live trading, real-account risk, or copying to a live account: owner only.
- The Portfolio Simulation lives in `PORTFOLIO_RULES.md` and is separate from these per-strategy tests.
