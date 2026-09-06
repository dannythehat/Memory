# AIDY — Current State

Last verified: **2026-09-06**

Authoritative source repo: `dannythehat/Aidy-Gold-Signals`
Authoritative branch: `main`
Verified `main` SHA at this memory snapshot: `38ceebe38a3b9754dedbd9977e5595ae332656fe`

## Where we are

The current September production-hardening sequence is complete through **Day 5**.

- Day 3: D1 read-budget monitoring, bounded retries, diagnostics and alert path — GREEN.
- Day 4: market-calendar-aware scheduled-capture freshness watchdog — GREEN.
- Day 5: D1 -> R2 archive-outbox durability watchdog — GREEN.

Current Day 5 production evidence is in the AIDY repo at:

`ops/day5-archive-outbox-watchdog-evidence-20260906.md`

PR #90 delivered Day 5. PR #91 closed the final production evidence gate.

## Next

**Day 6** is next.

Goal: controlled archive retry/dead-letter hardening so a permanently failing archive item is not retried forever. Preserve evidence truth, capture independence and continuity-auditor semantics.

After the pure hardening sequence, the intelligence roadmap becomes more visibly interesting: provider identity/behavioural profiles, forward-only context, provider fingerprints, conditional strengths/weaknesses, veto/filter intelligence, confidence/sizing and active trade-management research.

## Runtime/safety posture

- AIDY is capture/research infrastructure for Gold intelligence.
- Formal-forward authority must remain OFF unless explicitly graduated with evidence and owner approval.
- Twelve Data is the current independent market-data source for the production capture path.
- D1 is operational state/evidence; R2 is durable archive; historical/research analytics may use BigQuery.
- AIDY must never silently gain Super Signals broker execution authority.

## Important naming warning

The AIDY repo contains older historical files/builds also named `Day 5`, including the August historical XAUUSD backfill milestone. Do not confuse those with the **September 6 Day 5 production-hardening watchdog**. Always resolve the build by date, evidence file and current `main` history.

## Session rule

Before continuing Day 6, verify `main` and the relevant production evidence again. If this file disagrees with the repo/runtime, update Memory — do not force the system to match Memory.
