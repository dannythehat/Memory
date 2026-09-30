# AIDY Handover — 2026-09-30

## Finished state

Source repo: `dannythehat/super-signals` (production Postgres `dpg-d9qmc6cs728c73a54kc0-a`, read-only queries)
Branch: n/a (audit only, no code changed)
Verified SHA: live deploy `dep-datnde1srm7s739d7v50`, commit `bac6740d382f3a3b01beb5a6fc014ff7abc0911f`
Status: **PRODUCTION VERIFIED** for the facts below. **No AIDY edge found.** Not STATISTICALLY VALIDATED for anything positive.

Owner asked: does AIDY have any edge, can he understand trade direction, is there any sign he is getting smarter — "if not, forget him".

## What was found

**1. AIDY is switched off in production, so nothing has been learning.** Live logs on every restart since at least 09-29: `AIDY research lane disabled in live Super Signals process; trading and Telegram only`. Newest rows: `aidy_decisions` 09-22 14:28Z, `aidy_decision_outcomes` 09-22 14:46Z, `aidy_reasoning_annotations` 09-23 09:40Z, `provider_trade_scores` 09-24 04:21Z. Trading, Telegram and `ai_message_decisions` are current to 03:38Z on 09-30 — the OpenAI message reader is a different thing and is running. There is no post-09-23 AIDY evidence to measure "getting smarter" on.

**2. The reasoning layer's lean does not pick winners** (2,005 reasoned trades that resolved won/lost, joined decision → provider_trade_scores; base win rate 54.9%):

| lean | n | win % | avg P&L |
|---|---|---|---|
| agree | 595 | 55.6 | +$3.50 |
| caution | 1,337 | 55.2 | +$1.23 |
| disagree | 73 | 43.8 | +$8.87 |

agree vs base p=0.74; agree vs caution p=0.88 — indistinguishable. `disagree` wins less (p=0.06, not significant) but its trades pay MORE per trade, so skipping them would have cost money.

**3. No learning curve.** By prompt version: v1 (geometry only, n=1,880) agree 56.9%; v14_gold_toolbox (latest, n=94) agree **33.3% (11/33, p=0.014 raw — one of ~10 slices looked at, so NOT significant after correction)**. v3–v5 (market context, candles, calendar, day-map — built 09-18) have only 23 resolved trades, too few to judge. The richer versions are not measurably better and the newest is nominally worse.

**4. Gold-direction view is not usable.** 148 annotations have `gold_view_direction` (09-20→09-23, 61% bearish). Of 102 that resolved: provider_alignment `aligned` won 42.0% (21/50, −$272) vs `conflicts` 61.9% (13/21, +$115) — backwards, but Fisher p=0.19, n small. Not a signal either way. The 15-minute gold-direction coin-flip result from 09-23 (2,743 windows, 47.65% baseline) was NOT re-run — needs the AIDY Worker's D1 M1 candles, not reachable from Super Signals Postgres.

**5. Deterministic decision layer, re-scored with all now-resolved trades, split by decision lag:**

| sample | helped | hurt | help % | net $ if skipped |
|---|---|---|---|---|
| LIVE (<10 min lag) | 44 | 53 | 45.4% (p=0.42 vs coin) | **−$384** |
| REPLAY (≥1 day lag) | 82 | 51 | 61.7% (p=0.009) | +$616 |

Live vs replay difference p=0.016. Confirms the 09-23 finding (replay 82/51 reproduced exactly): the replay "edge" is in-sample. Live n grew from 16 to 97; still no positive live evidence. Per class live: conflict_deny 33/27 (−$14), deny 4/16 (−$245), hold_no_second_entry 7/10 (−$125).

**6. Provider scoring is the only real thing, and it is measurement, not AIDY judgement.** 2,255 resolved trades, 40 providers, 08-12→09-24: take-everything baseline ≈ 54.9% win. Walk-forward (25→5 prior trades, per provider): skipping providers with trailing win <45% avoids −$162 of a +$2,658 book; rate ladder not monotonic (53.9% at 45–55% vs 60.7% at 55–65%); rough z≈2.1 using an assumed $25 SD, one of several looks — weak. Split-half persistence across 14 providers with ≥30 trades: Spearman 0.363, p=0.20 (not significant). Two providers persist in both halves: **TRADE GLOBAL −$10.53 → −$9.99/trade** (322 trades), **TIG's Asia +$2.72 → +$3.46** (373). Most others regress toward the mean (GOLDHUNTER +$47.78 → +$12.02, GTMO VIP +$9.17 → −$3.07, TDC V2 +$6.28 → +$3.00). Scorecard reliably identifies extremes only.

## Why

- Owner wanted a clear verdict on whether AIDY is worth keeping. The record of tests says AIDY's own judgement adds nothing measurable over simply taking the providers' trades (which as a group are +EV at ~55%).

## Evidence

- PR: none (read-only audit).
- Runtime proof: Render logs (`AIDY research lane disabled…`), SQL against production Postgres on 2026-09-30 ~03:40Z, exact binomial/Fisher tests computed locally (no scipy; log-space).
- Caveats: reasoning annotations exist mostly for `approve` decisions; won/lost only (open, never_entered and unresolvable excluded); multiple slices examined, so only the live-vs-replay gap (p=0.016) and the null results are firm.

## Safety state

- No writes made to production. No env vars, deploys or code changed.
- Observed, not investigated: **GOLDHUNTER now has `sources.status='shadow'`** (26 executable observations in 7 days). It was `testing` and graduated (`provider_execution_probation.graduated=true`, PR 198) on 09-18. Someone or something changed it since; reason not established. TRADE GLOBAL is `shadow` (observed only, 695 executable observations in 7 days). TIG's Asia is `testing`.

## Unresolved

- Whether to keep spending effort on AIDY's model layers at all — owner decision. Evidence supports stopping the LLM reasoning/gold-view work (it is already off in production).
- Why GOLDHUNTER reverted to `shadow`.
- Gold-direction re-test on fresh candles.

## Exact next step

- Owner decides: keep only the provider scorecard (pure measurement, near-zero cost) and retire AIDY's model layers, or run one more out-of-sample window. If the latter, re-enable only the pieces needed and pre-register the pass/fail rule before looking at results.
