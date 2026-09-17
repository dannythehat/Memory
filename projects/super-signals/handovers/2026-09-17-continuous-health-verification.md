# Super Signals / AIDY handover — 17 September 2026 (later) — continuous-health verification

## What this adds to the 04:00 recovery handover

The earlier handover proved AIDY Provider Context was READY at one moment, seconds after
startup. That is a single probe, not proof of sustained health, and it cannot repeat: the
probe in `aidy_shadow_runtime.py` is gated `if context_client is not None and not
context_probe_ready` — it fires once per process lifetime and never again. This entry
records multi-cycle, cross-system evidence instead.

## Verified independently, source/runtime, not carried from any report

- **Render deploy**: `dep-dalma2gae00c739qlul0`, commit `356dfcf1801f70c786ff7fa2de38ce88d55ec071`, status `live`, matches exactly what was reported.
- **Quality gate**: local run against the exact deployed SHA reproduced **1,082 passed, 0 failed** with a live Postgres (989 + 93 = 1,082 — the cited CI figure's skips are exactly the tests that don't skip locally; cross-validated, not just repeated).
- **AIDY D1, ground truth**: `market_snapshots` for XAUUSD/twelve_data shows **53 consecutive `complete` snapshots, zero `partial`**, every ~5 minutes from `2026-09-17T00:02Z` through `04:22Z` — spanning well before and after the deploy. AIDY-side capture was not actually the thing broken; this confirms the fix's benefit was in Super Signals' own M1 fetch path.
- **Super Signals DB, active resolver progress**: `shadow_trades` shows 83 rows updated since the deploy, `aidy_m1_cursor_at` advancing from `03:43` to `04:10` across multiple distinct update cycles — the resolver loop is doing real repeated work, not idling.
- **Super Signals logs, full post-deploy window**: zero occurrences of `pit_context_stale`, `AidyContextTerminalMiss`, `NOT_READY`, or any traceback, from deploy through the end of the check.
- **Live AIDY `/health` at time of writing** (independent of any Super Signals-side claim): `status: ok`, `data_health.status: fresh`, `provider_context_snapshot_lag_seconds: 157`.

**Conclusion: the 16 September stale-context state is confirmed superseded by sustained, multi-cycle production evidence, not a single successful probe.** Treat this entry, not the 04:00 one alone, as the basis for "AIDY is healthy" going forward.

## A second, unrelated failure found and partially fixed while verifying

Production logs carried `PROVIDER_DAY14_GOVERNANCE_ERROR=RuntimeError` repeatedly since at
least `2026-09-16T18:15` — irregular intervals, 2 to 90 minutes apart. Nothing to do with
M1/context. Root-caused by direct query rather than trusting the log line (which gave only
the exception type):

`_frozen_boundary()` in `provider_day14_governance.py` requires every row in
`provider_conditional_hypotheses` under the current `registry_version` to share exactly
one `preregistered_at`. Production has two: 15,360 rows from `2026-09-07` and 384 more
from `2026-09-14`. Not a writer bug — `_ensure_preregistry()` is deliberately idempotent
per-cohort (its `ON CONFLICT` key excludes `preregistered_at`), so a newly-onboarded
`shadow` source correctly gets hypotheses stamped with when it actually joined, not
backdated to the original registry date. **The registry will keep growing this way as new
shadow sources are added, which is normal, so this guard can never pass again as written.**

Fixed: the retry loop (both `provider_day14_governance.py` and its duplicate in
`provider_day14_runtime.py`) now logs `str(exc)` alongside the exception type. Verified
live post-deploy: the log now reads
`PROVIDER_DAY14_GOVERNANCE_ERROR=RuntimeError:day13_preregistration_boundary_not_frozen`.

**Not fixed, and deliberately left for the owner:** whether the evaluation window should
freeze one boundary per run (bump `registry_version` per cohort) or let each hypothesis
carry its own `preregistered_at` as its individual out-of-sample cutoff. `frozen_boundary`
is applied identically to every source's observations today
(`observation.signal_posted_at > frozen_boundary`), so this is a real anti-hindsight
methodology decision — changing it changes what counts as in-sample evidence for every
provider evaluation, not a bug fix. Zero live-money impact either way: this subsystem is
`research_only=True` end to end with no `sources.status` or broker write path, and it has
been silently failing since before this session with no effect on current risk.

Deployed: PR #182, squash-merged `8b2ca7f7`, Render deploy `dep-dalmjj3bc2fs7387mrv0`, live.

## Boundaries unchanged

Gold/XAUUSD only. Owner live-risk directive remains 1% only. No new AIDY/provider-research
broker or live-money authority. Existing TP management semantics unchanged. Weekend XAUUSD
freeze unchanged. `sources.status` and broker write paths untouched by anything in this
entry.

## Rule for the next session

A single "resolver loop started" / "probe READY" log line is not health evidence — it is
architecturally incapable of repeating. Check AIDY's own D1 `market_snapshots` for a run
of consecutive `complete` rows, and Super Signals' own resolver-progress tables
(`shadow_trades.aidy_m1_cursor_at` advancing), before calling context "healthy."
