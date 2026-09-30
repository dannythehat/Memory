# GoldThinker — Discovery and validation rules (v0.1, draft)

Status: **DRAFT 0.1, 2026-09-30, Claude for ChatGPT to challenge** (D-041). Research rule; nothing is coded.
It replaces the "still open" item 3 of `CANDLE_SPEC_V1.md`. It builds on D-011 (no pooling), D-012 (STOP FIRST),
D-018/D-019 (discovery -> freeze -> validation; survival gates). **No outcome of these rules authorises real money;
only the owner can (D-035).**

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

## 2. Stage 1 - Discovery (forward paper trading, months 1-3)

Uses the gates already proposed in D-019, unchanged:

| Review | Min trades | Kill if | Continue if |
|---|---|---|---|
| Month 1 | 20 | expectancy <= -0.20R, or PF < 0.80, or drawdown > 15R | otherwise |
| Month 2 | 40 | (M1 kill tests still apply) | expectancy > 0, PF >= 1.05, DD <= 12R |
| Month 3 | 75 | - | **candidate** if expectancy >= +0.10R, PF >= 1.20, DD <= 10R, positive in 2 of 3 months, **and** the 90% one-sided day-block bootstrap lower bound of expectancy > 0 |

Rules that make the numbers honest:

1. A strategy with fewer trades than the minimum at a review is **UNKNOWN** (< 30 trades) or **PRELIMINARY**
   (30-74). It is not killed and not promoted; it keeps accumulating on the same rule version. Its discovery review
   happens when it reaches 75 trades, or at month 12, whichever is first (then it ends `INSUFFICIENT_DATA`). Slow
   strategies (D1, W1, MN1) will mostly end this way; that is a finding, not a failure of the rules.
2. Killed and unknown strategies stay in the count `K` (about 657) for the report: the number of things looked at is
   always published next to any survivor.
3. Expected false candidates: if all 657 strategies had zero edge and all reached 75 trades, the bootstrap bound alone
   would let through about 5% of them (about 33); the other gates cut that, but it is the reason discovery **selects**
   and never **proves**. Nothing at this stage may be called "profitable".
4. Kill decisions use only trades closed before the review date.

## 3. Freeze

Before validation starts, the survivors (`m` of them) are frozen in a manifest committed to this repository: strategy
list, spec version, golden-vector pack version, detector commit, gate values, freeze date, and `K`. After freezing:

- No rule, parameter, threshold, timeframe or variant may change. Any change is a **new rule version and a new sample**
  (D-011) and cannot inherit validation credit.
- Validation uses **only trades whose signal time is after the freeze time**. Discovery trades are never reused.
- Adding a strategy to validation later requires its own freeze.

## 4. Stage 2 - Validation (untouched period)

Fixed length **3 months** from the freeze, extendable **once** by another 3 months if a candidate is `INCONCLUSIVE`.

**Per-strategy checks** (all must hold for a PASS):

| # | Check | Value |
|---|---|---|
| V1 | Sample | at least **100** closed trades |
| V2 | Practical size | expectancy >= **+0.10R**, PF >= **1.20** |
| V3 | Drawdown | max drawdown <= **10R** over the period |
| V4 | Not one lucky day | expectancy stays >= **+0.05R** after deleting the best single day |
| V5 | Cost stress | expectancy >= **0** when spread is 1.5x and swap 2x, recomputed from the stored ticks |
| V6 | Statistical evidence | one-sided **day-block bootstrap** test of H0: expectancy <= 0 (section 5), adjusted for `m` |

**Multiple testing across the `m` frozen candidates**

- **PASS-STRONG:** V1-V5 hold and the bootstrap p-value survives **Holm** at family-wise 5% (valid under any
  dependence between strategies, which matters because strategies fire on the same candles).
- **PASS-WEAK:** V1-V5 hold and the p-value survives **Benjamini-Hochberg** at q = 10% but not Holm. Meaning: worth
  continuing to observe; **not** enough to propose for live use.
- **FAIL:** at >= 100 trades, expectancy <= 0 or PF < 1.0 or V3 violated; or at the end of the (extended) period the
  80% one-sided upper bound of expectancy is below +0.05R.
- **INCONCLUSIVE:** anything else. After the one extension an INCONCLUSIVE strategy becomes `NOT_PROVEN` (treated as FAIL
  for decisions; it may only re-enter through a new rule version and a new discovery).

Only **PASS-STRONG** strategies may be put to the owner as live candidates, and even then the recommendation requires
the Portfolio Simulation results (D-039 step 3), a live-account risk decision, and the owner's explicit approval.

## 5. The day-block bootstrap (deterministic definition)

- **Blocks:** the trading day on the server-time D1 boundary (G0, timeframe construction), by the day the trade **closed**. A day without
  trades contributes zero R and zero trades but stays in the resampling pool.
- **Statistic:** `E = sum(R) / count(trades)` (ratio estimator over resampled days).
- **Resampling:** `B = 10,000` draws of `N_days` days with replacement, seeded from the SHA-256 of the freeze manifest
  plus the strategy id (reproducible; the algorithm is named in the report).
- **p-value (H0: E <= 0):** centre each day (subtract `E_hat` x that day's trade count), resample, and let
  `p = (1 + #{E* >= E_hat}) / (B + 1)`.
- **Lower/upper bounds:** the corresponding percentiles of the uncentred resampled `E*`.
- **Dependence sensitivity:** repeat with 5-day blocks; the verdict uses the **larger** of the two p-values.

## 6. What sample sizes this implies (calculation, not a result)

Assumes trade-R standard deviation of about 1.5 (a 2R target / 1R stop strategy near breakeven), one-sided test, 80%
power, normal approximation. Trades needed to detect a true expectancy:

| Holm family size `m` | +0.10R | +0.15R | +0.20R | +0.30R |
|---|---|---|---|---|
| 1 | 1,391 | 618 | 348 | 155 |
| 10 | 2,628 | 1,168 | 657 | 292 |
| 30 | 3,209 | 1,426 | 802 | 357 |

Consequences, stated plainly: a true edge of +0.10R cannot be proven in three months by any strategy that trades a few
times a day; only frequent patterns on the short timeframes can reach 300-800 trades in a validation period, and most
survivors will end `INCONCLUSIVE` or `NOT_PROVEN`. That is the correct behaviour: the rules would rather leave a real edge
unproven than approve a false one. V1 (100 trades) is a floor, not evidence; V6 carries the proof burden.

## 7. Reporting and the hub

Every review publishes, for each strategy: n, expectancy with the bootstrap interval, PF, drawdown, stage and verdict,
and for the whole exercise `K`, `m`, the number killed, the number unknown and the expected number of false
candidates. Strategies with too little data show "NOT ENOUGH DATA" (D-023). Verdict labels are `UNKNOWN`,
`PRELIMINARY`, `KILLED`, `CANDIDATE`, `PASS-STRONG`, `PASS-WEAK`, `INCONCLUSIVE`, `NOT_PROVEN`, `FAIL`,
`INSUFFICIENT_DATA`.

## 8. Not decided here

- The Portfolio Simulation (sizing, exposure caps, correlation between concurrent trades): next step.
- Anything about live trading, real-account risk, or copying to a live account: owner only.
- Whether the numbers in section 2 (ChatGPT's D-019 proposal) and section 4 (this draft) are the right ones: open to
  ChatGPT's challenge; they are research thresholds, not results.
