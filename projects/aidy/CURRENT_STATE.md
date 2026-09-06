# AIDY — Current State

Last verified: **2026-09-06**

Authoritative AIDY source repo: `dannythehat/Aidy-Gold-Signals`
Authoritative AIDY branch: `main`
Verified AIDY `main` SHA: `bf5bd10a9ccb31f007bea9da04ffa077132c5500`

## Where we are

The September Provider Intelligence sequence is complete through **Day 7**.

- Day 3: D1 read-budget monitoring, bounded retries, diagnostics and alert path — GREEN.
- Day 4: market-calendar-aware scheduled-capture freshness watchdog — GREEN.
- Day 5: D1 -> R2 archive-outbox durability watchdog — GREEN.
- Day 6: bounded archive retry/backoff and explicit dead-letter handling — GREEN / PRODUCTION VERIFIED.
- Day 7: provider identity, style and behavioural-profile versioning — GREEN / PRODUCTION VERIFIED.

Day 7 is intentionally implemented in **Super Signals**, because Super Signals owns Telegram provider identity and Provider Lab profiles. AIDY remains the independent point-in-time market/context truth service and gained no provider database or broker authority.

## Day 7 verified production state

Super Signals live implementation:

- production branch: `feature/day-10-shared-telegram-sources`;
- live SHA: `43eddfde8d584b26be807c4ff998f7fd7afad050`;
- migration head: `0056_provider_profile_versions`;
- Render deploy: `dep-daenlsh42hec73chgsf0`;
- production API quality gate: **745 passed, 67 skipped**;
- current provider profiles: **48**;
- versioned sources: **48**;
- immutable profile versions observed during verification: **130**;
- duplicate `(source_id, version_no)` groups: **0**;
- unversioned current profiles: **0**;
- provider version sequences with gaps: **0**;
- production append-only trigger: enabled;
- no-op adaptive refreshes: proved not to manufacture history rows when only `generated_at_epoch` changed;
- point-in-time as-of lookup: returned the older version between later changes and returned no fabricated state before the Day 7 bootstrap origin;
- profile changes: 82 append-only update versions across 42 sources, with no adjacent duplicate semantic fingerprints and no non-monotonic effective times.

The Day 7 production diff contains exactly three files: the migration, its tests and the Day 7 gate document. No execution/parser/risk/MetaAPI/member-routing code changed. Render logged no error-level events after the Day 7 deployment during verification.

AIDY remained unchanged by Day 7. Its checked archive watchdog run `34038831088` was healthy with zero Gold pending items, zero cross-market pending items, zero poison items and no alert. Super Signals' post-Day-7 Provider Lab resolver startup also reported zero AIDY resolution failures.

## Next

**Day 8 — forward-only learning boundary and legacy closure.**

Goal: make the Day 7 profile-version ledger operationally authoritative for point-in-time provider research. Any provider learning/context used for historical or forward evaluation must be provably limited to what was knowable at that timestamp. Pre-Day-7 mutable profile state must not be silently projected backwards.

## Runtime/safety posture

- AIDY is independent Gold market/context intelligence, not the provider or broker database.
- Super Signals owns provider interpretation/profile history, benchmark/replay and broker/member execution.
- Formal-forward authority remains OFF unless explicitly graduated with evidence and owner approval.
- Shadow discovery providers remain broker-isolated.
- Historical entry/SL/TP values must never contaminate new current signals.
- Runtime/source/database evidence overrides Memory if they disagree.

## Naming warning

Older August AIDY milestones also use Day 7/Day 8 numbering. The active sequence here is the **6 September 2026 Provider Intelligence sequence**. Resolve by current Memory handover and live repository/runtime evidence.

## Session rule

Before starting Day 8, read the newest Day 7 handover, then verify AIDY `main`, the Super Signals live branch/deploy and the relevant production database state. If Memory is stale, repair Memory from reality first.
