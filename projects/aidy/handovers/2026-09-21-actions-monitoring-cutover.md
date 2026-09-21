# AIDY GitHub Actions monitoring cutover — 2026-09-21

## Completed

AIDY repository: `dannythehat/Aidy-Gold-Signals`

PR #140 merged to `main` at commit `09066e085493b2970530adf82577db132164c94a`.

The following GitHub-hosted recurring schedules were removed while keeping their workflows available for manual diagnostics:

- `aidy-archive-outbox-watchdog.yml`: removed every-10-minute schedule.
- `aidy-capture-freshness-watchdog.yml`: removed every-10-minute schedule.
- `aidy-d1-row-budget-alert.yml`: removed hourly schedule.
- `phase-b-forward-restart.yml`: removed every-10-minute schedule; remains manual-only.

No Gold-learning logic, provider policy, Super Signals execution logic, risk sizing, MT5, MetaAPI or broker code was changed.

Before removal, these schedules represented 456 GitHub workflow launches per day, approximately 13,680 launches per 30-day month.

## Why the monitoring remains covered

The live AIDY Cloudflare Worker already runs its own direct cron and records native data health.

`src/provider_entry.py` runs on Cloudflare direct cron and calls:

- `_record_health_best_effort`
- `_sync_episode_memory_best_effort`
- `_sync_gold_movement_memory_best_effort`

`src/aidy/data_health.py` already evaluates market-capture freshness, Provider Context freshness, archive pending/backoff/dead-letter state, and cross-market archive state. Therefore the two GitHub watchdogs were duplicate monitoring rather than the canonical runtime monitor.

The Phase B guarded forward restart is an activation/deploy mechanism, not a health monitor. It is now manual-only so a polling workflow cannot automatically mutate forward state.

## Live verification after cutover

Public Worker: `aidy-signals-test`.

Post-merge live health confirmed:

- runtime: `cloudflare-workers`
- scheduler: `direct-cron`
- `capture_enabled=true`
- `formal_forward_enabled=false`
- market source: `twelve_data`
- scheduled capture remained fresh

However, the same post-merge check exposed an existing AIDY runtime fault:

- Worker health: `degraded`
- health state: `stale_provider_context`
- latest scheduled capture success observed: `2026-09-21T02:52:30.148999+00:00`
- latest complete Provider Context snapshot observed: `2026-09-21T01:57:30.150000+00:00`

Super Signals independently logged at `2026-09-21T02:49:58Z`:

`AIDY Provider Context live probe NOT_READY error=AidyContextTerminalMiss`

So the GitHub Actions waste is fixed, but AIDY Provider Context is not currently healthy. Do not mark the broader AIDY runtime as healthy until this is resolved and verified.

## Separate Super Signals observation

Render is also still reporting `metaapi_temporarily_unavailable` for broker settlement/member metrics. This is separate from the AIDY Cloudflare Provider Context fault and from the GitHub Actions cutover.

## Next

Diagnose why fresh Twelve Data scheduled captures after 01:57 UTC are no longer producing a Provider-Context-eligible snapshot. Preserve the existing boundary: AIDY remains research-only and must not change live trading authority while this is repaired.
