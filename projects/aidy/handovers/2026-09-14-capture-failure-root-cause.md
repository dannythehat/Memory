# AIDY Handover — 14 September 2026 — capture failure root cause

## Status: RED

First session with live Render + Cloudflare access. This handover records the first genuine
runtime diagnosis of AIDY. It is **RUNTIME VERIFIED**, not inferred.

## The single most important fact

**AIDY has never made a decision.** `aidy_end_to_end_cycles` = 0. Not one. The full
Architecture V2 cycle — compose → gate → OpenAI k=3 → ledger → paper → watcher → memory — has
never executed a single time in production.

This is **not** a design failure. Every failure is at the deterministic pre-model gate. AIDY
refused to think on incomplete data 121 times without supervision, exactly as designed. The
brain is untested, not proven bad.

## Live runtime state (verified 2026-09-14 10:34 UTC via `GET /health`)

```
status:                      degraded
capture_enabled:             true
formal_forward_enabled:      FALSE          <- definitively answers the open Memory question
market_data_source:          twelve_data
scheduler:                   direct-cron
private_forward_model_gateway_configured: true
data_health.status:          stale_capture
data_health.alert:           true
session_open:                true           <- market IS open
latest_scheduled_success:    2026-09-13T10:35:47Z   (lag 86,525s = 24h)
latest_provider_context:     2026-09-09T04:30:25Z   (lag 454,046s = 5.25 days)
```

## D1 evidence (`aidy-ops-test`)

| Metric | Value |
|---|---|
| `aidy_end_to_end_cycles` | **0** |
| `aidy_memory_episodes` | **0** |
| `aidy_memory_outcomes` | **0** |
| `aidy_learning_cards` | **0** |
| `aidy_forward_restart_runs` | **0** — Phase B campaign never activated |
| `aidy_forward_evaluations` | 121, **0 `known_good`**, 0 model-resolved |
| `market_snapshots` | 227, **only 7 `complete`** |
| `market_candles` | 10,092 |
| `twelve_data_feed_observations` | 834 |
| Active cohort | `aidy_formal_forward_cohort_v2_immediate_start`, activated 2026-09-04T04:25:58Z |
| Day 54 gate | **0 of 300** episode-independent model-resolved decisions |

### Why all 121 forward evaluations failed

| Reason code | Count |
|---|---|
| `market_reference_not_complete` | 68 |
| `missing_genuine_live_ohlc_and_spread` | 48 |
| `production_decision_context_build_failed` | 4 |
| `market_reference_unavailable` | 1 |

Last forward evaluation of any kind: **2026-09-05**. Nothing in the nine days since.

### Capture by day — the real shape

| Day | Snapshots | `complete` | Note |
|---|---|---|---|
| Sun 06 Sep | 83 | 0 | |
| Mon 07 Sep | 61 | 0 | |
| Tue 08 Sep | 16 | 4 | |
| Wed 09 Sep | 14 | 3 | stops 05:40 |
| **Thu 10 Sep** | **0** | 0 | **Twelve Data quota exhausted (owner-confirmed)** |
| **Fri 11 Sep** | **0** | 0 | **same** |
| Sun 13 Sep | 53 | 0 | stops 10:35 |
| **Mon 14 Sep** | **0** | 0 | **market open since Sun 22:01 UTC — nothing captured** |

Sunday capture is **not** a fault: the Worker runs on Sundays and correctly marks
`session_closed`. Do not treat weekend activity as an anomaly.

**Only 7 of 227 snapshots are `complete`.** That single number explains
`market_reference_not_complete` and therefore explains why AIDY has never thought.

## Root cause chain

```
Twelve Data plan too small (minute credits hit 1 remaining repeatedly)
        │
        ├── Thu 10 / Fri 11 Sept: daily quota exhausted -> zero capture
        │
        └── partial snapshots when running (7/227 complete)
                    │
                    v
        market_reference_not_complete
                    │
                    v
        every forward evaluation pre_model_blocked -> AIDY never decides
                    │
                    ├── 0 episodes -> 0 learning cards -> Day 54 gate stuck at 0/300
                    │
                    └── M1 history has holes -> Super Signals shadow scoring stalls
                                (44 missing minutes block 107 shadow trades)

SEPARATE, CURRENT FAULT:
        Cloudflare Cron not firing since 2026-09-13 10:35
        (capture_enabled=true, code deployed, market open, zero requests made)
```

### The deadlock

`aidy_forward_restart_runs` is empty and **can never populate**. The Phase B gate requires
≥3 consecutive capture successes plus fresh data health. Capture is stale, so the gate fails,
so formal forward stays off, so AIDY never decides — every 10 minutes, indefinitely.

Everything is downstream of the Cron.

## Monitoring gap

`aidy-capture-freshness-watchdog` **works**. It went `failure` at 2026-09-13T23:08, again at
01:01 and 06:05 on the 14th — correctly detecting stale capture from the moment the market
reopened.

Nobody saw it. The alert is a red ✗ in GitHub Actions with **no notification channel**.

Worse: the workflow is scheduled `3,13,23,33,43,53 * * * *` (every 10 min) but actually ran at
18:50, 21:09, 23:08, 01:01, 06:05 — GitHub is heavily throttling scheduled runs. **Do not rely
on GitHub Actions cron for time-sensitive monitoring.** The same throttling applies to
`phase-b-forward-restart.yml`.

## Action taken this session

Dispatched `phase-b-episode-memory-rollout.yml` on `main` (owner-approved) to restore the
Cloudflare Cron. That workflow runs the full test suite, rebuilds canonical production config
(capture on, twelve_data, poll 300s, **formal forward off**), applies D1 migrations, redeploys
the Worker, and explicitly proves the direct Cron schedules survived deployment.

Nothing else was changed. Formal forward was not touched.

## Next steps, in order

1. **Confirm the rollout restored the Cron** — `/health` should show `success_lag_seconds`
   falling and `data_health.status` leaving `stale_capture`.
2. **Attach a real alert channel** to the freshness watchdog, and move time-sensitive
   monitoring off GitHub Actions cron.
3. **Twelve Data headroom** — the ledger shows `provider_minute_credits_left` reaching 1.
   Either upgrade the plan or reduce the per-capture request footprint. Until this is fixed,
   snapshots will keep coming back partial even with the Cron running.
4. **Backfill** the 44 missing M1 minutes (2026-09-04 → 2026-09-09), then full M1 for
   1–14 Sept, then re-run the shadow resolver. See the Super Signals handover of the same date.
5. Only then consider the Day 54 gate and the Data Hub.

## Rules reaffirmed

- Formal forward remains OFF. It was not changed and must not be without an explicit owner gate.
- No broker, MT5, MetaAPI, Vantage or Super Signals credentials in AIDY.
- The pre-model gate behaviour is correct and must not be loosened to "get data flowing".
  Fix the feed, never the gate.
