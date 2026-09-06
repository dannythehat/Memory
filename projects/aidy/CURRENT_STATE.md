# AIDY — Current State

Last verified: **2026-09-06 14:20 UTC**

Authoritative source repo: `dannythehat/Aidy-Gold-Signals`
Authoritative branch: `main`
Verified `main` SHA at this memory snapshot: `bf5bd10a9ccb31f007bea9da04ffa077132c5500`

## Where we are

The current September production-hardening sequence is complete through **Day 6**.

- Day 3: D1 read-budget monitoring, bounded retries, diagnostics and alert path — GREEN.
- Day 4: market-calendar-aware scheduled-capture freshness watchdog — GREEN.
- Day 5: D1 -> R2 archive-outbox durability watchdog — GREEN.
- Day 6: bounded archive retry/backoff plus explicit dead-letter state — GREEN and production verified.

Current Day 6 production evidence is in the AIDY repo at:

`ops/day6-archive-dead-letter-evidence-20260906.md`

PR #92 delivered the Day 6 runtime/schema change. PR #93 repaired the rollout environment without changing runtime semantics. PR #94 recorded the successful merged-main production evidence and closed Day 6.

## Day 6 verified production state

- final merged-main rollout run: `34038324207` — PASS
- Worker deployed from merged `main` with capture enabled
- market data source: Twelve Data / public-independent ownership
- formal-forward: OFF
- live migration for archive delivery state: applied
- bounded retry/backoff and terminal `dead_letter` behaviour: proven live
- healthy archive items continue after a poison item: proven
- scheduled-capture heartbeat advanced after deployment: proven
- full merged-main regression: 1199 passed
- fresh archive-outbox watchdog run `34038831088` at 2026-09-06 14:20 UTC: PASS
  - pending: 0
  - retrying: 0
  - stale: 0
  - dead-letter: 0
  - total outbox rows observed: 28
- latest capture-freshness watchdog available during reconciliation queried live D1 successfully and reported `session_closed`, `alert=false`, which is correct for the canonical Gold session on Sunday.

## Exact next step

**Start Day 7: provider identity, style and behavioural-profile versioning.**

The source repo's Day 6 closeout explicitly defines this as the next intelligence-facing phase. Keep all learning **forward-only** and **shadow-safe** until later evidence gates authorize stronger use.

Day 7 must begin from the actual current `main`, preserve every existing safety boundary, and must not silently create broker execution or formal-forward authority.

## Runtime/safety posture

- AIDY is capture/research infrastructure for Gold intelligence.
- Formal-forward authority remains OFF unless explicitly graduated with evidence and owner approval.
- Twelve Data is the current independent market-data source for the production capture path.
- D1 is operational state/evidence; R2 is durable archive; historical/research analytics may use BigQuery.
- AIDY must never silently gain Super Signals broker execution authority.
- Production changes remain rollback-ready and evidence-gated.

## Important naming warning

The AIDY repo contains older historical files/builds also named `Day 6` and `Day 7` from the August architecture programme. Do not confuse those with the **September 6 production-hardening Day 6** or the new intelligence-facing **Day 7**. Always resolve the active build by date, current `main` history and the newest Memory handover.

## Session rule

Before continuing Day 7, verify `main`, the newest production watchdog evidence and this Memory snapshot again. If Memory disagrees with the repo/runtime, update Memory — do not force the system to match Memory.
