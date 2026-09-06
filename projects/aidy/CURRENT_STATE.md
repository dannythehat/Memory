# AIDY — Current State

Last verified: **2026-09-06**

Authoritative AIDY source repo: `dannythehat/Aidy-Gold-Signals`
Authoritative AIDY branch: `main`
Verified AIDY `main` SHA: `bf5bd10a9ccb31f007bea9da04ffa077132c5500`

## Where we are

The September Provider Intelligence sequence is complete through **Day 8**.

- Day 3: D1 read-budget monitoring, bounded retries, diagnostics and alert path — GREEN.
- Day 4: market-calendar-aware scheduled-capture freshness watchdog — GREEN.
- Day 5: D1 -> R2 archive-outbox durability watchdog — GREEN.
- Day 6: bounded archive retry/backoff and explicit dead-letter handling — GREEN / PRODUCTION VERIFIED.
- Day 7: provider identity, style and behavioural-profile versioning — GREEN / PRODUCTION VERIFIED.
- Day 8: forward-only provider learning boundary and legacy closure — GREEN / PRODUCTION VERIFIED.

Days 7–8 are intentionally implemented in **Super Signals**, because Super Signals owns Telegram provider identity and Provider Lab research. AIDY remains the separate independent point-in-time Gold market/context truth service and gained no provider database or broker authority.

## Day 8 verified production state

Super Signals production:

- production branch: `feature/day-10-shared-telegram-sources`;
- live SHA: `0ea04e9a118b7ae2782cb890a35d9725e1f16746`;
- PR: `#141`;
- migration head: `0057_provider_pit_boundary`;
- Render deploy: `dep-daeoomp5efls73a5134g` — live;
- Render API quality: **752 passed, 67 skipped**;
- GitHub API gate: success against PostgreSQL 18 with the Alembic chain upgraded through the Day 8 head;
- GitHub web typecheck/lint/tests/build: success;
- secret scan: pass;
- post-startup `/health`: 200;
- post-deploy error-level logs observed during verification: 0;
- Provider Lab AIDY resolver startup: `processed=0 failures=0`.

Provider PIT/legacy closure in the real production Postgres database:

- existing research trades: **144**;
- `legacy_unresolvable`: **144**;
- legacy score-eligible trades: **0**;
- the **6** formerly score-eligible pre-Day-7 rows are quarantined as `legacy_profile_unresolvable`;
- invalid legacy provenance rows: **0**;
- resolved-provenance mismatches: **0**;
- database provenance trigger `trg_shadow_trade_provider_profile_pit`: enabled.

Every legacy trade predates its source's Day 7 immutable profile-history origin, so Day 8 deliberately does **not** manufacture a provider profile for those old signals. They remain historical/research records but cannot count as PIT-clean fair-score evidence. New research enrollment resolves and stores the exact immutable provider profile version already effective at the signal timestamp; unresolved timestamps fail closed.

Provider-aware AI historical context now resolves only `provider_research_profile_versions` as of the actual message timestamp. It no longer reads the mutable current provider profile or rebuilds today's adaptive profile when interpreting an old message.

The Day 8 production diff changes only the Provider Intelligence PIT helper, provider-aware research/AI context, shadow research enrollment, migration, tests and gate documentation. It does not change risk sizing, MetaAPI/member routing, live broker execution authority or AIDY source/runtime.

## AIDY state through Day 8

AIDY `main` remained exactly `bf5bd10a9ccb31f007bea9da04ffa077132c5500` throughout Day 8. The latest available archive-outbox watchdog on that unchanged SHA is run `34038831088`, which completed successfully with Gold pending 0, cross-market pending 0, poison 0 and alert false. Formal-forward remains OFF.

## Exact next step

**Day 9 — canonical AIDY context join.**

Join each PIT-clean provider setup to the independent market/session/regime context that AIDY itself knew at that timestamp. Day 9 must preserve both sides of the temporal boundary: provider state must be PIT-safe under Day 8, and AIDY context must independently be PIT-safe. No current/future market state may leak into older provider evaluation.

## Runtime/safety posture

- AIDY is independent Gold market/context intelligence, not the provider or broker database.
- Super Signals owns provider interpretation/profile history, benchmark/replay and broker/member execution.
- Formal-forward authority remains OFF unless explicitly graduated with evidence and owner approval.
- 40 shadow discovery providers remain broker-isolated and distinct from the 5 real/testing providers.
- Historical entry/SL/TP values must never contaminate new current signals.
- Runtime/source/database evidence overrides Memory if they disagree.

## Naming warning

Older August AIDY milestones also use Day 8/Day 9 numbering. The active sequence here is the **6 September 2026 Provider Intelligence sequence**. Resolve by current Memory handover and live repository/runtime evidence.

## Session rule

Before starting Day 9, read the newest Day 8 handover, then verify AIDY `main`, the Super Signals live branch/deploy and the relevant production database state. If Memory is stale, repair Memory from reality first.
