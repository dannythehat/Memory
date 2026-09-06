# Super Signals — Current State

Last verified: **2026-09-06**

Authoritative repo: `dannythehat/super-signals`
Production branch: `feature/day-10-shared-telegram-sources`
Live production SHA: `43eddfde8d584b26be807c4ff998f7fd7afad050`
Render service: `super-signals-day-8`
Live deploy: `dep-daenlsh42hec73chgsf0`

## Provider populations

- 40 shadow discovery providers — research only, broker-isolated.
- 5 testing providers — current real execution population.
- 14 paused.
- 4 revoked.

Never mix the 40 shadow discovery providers with the 5 real/testing providers.

## Day 7 — GREEN / PRODUCTION VERIFIED

Day 7 added append-only point-in-time provider identity/style/behavioural-profile history without changing execution semantics.

Production proof:

- Alembic head `0056_provider_profile_versions`;
- 48 current research profiles and 48 versioned sources;
- 130 immutable versions observed;
- 0 duplicate `(source_id, version_no)` groups;
- 0 unversioned profiles;
- 0 version-sequence gaps;
- 82 real profile-update versions across 42 sources;
- no adjacent duplicate semantic fingerprints;
- append-only UPDATE/DELETE trigger enabled;
- as-of reader proved older-version retrieval and zero fabricated pre-bootstrap history;
- generated-at-only/no-op adaptive refreshes do not append fake versions;
- Render API quality gate: 745 passed, 67 skipped;
- post-deploy error-level logs: none during verification;
- AIDY Provider Lab resolver startup reported failures=0.

The Day 7 production diff contains exactly three files: the migration, its tests and its gate document. No execution/parser/risk/MetaAPI/member-routing code changed.

## Cross-project boundary

Super Signals owns provider identity, interpretation, profile history, benchmark/replay and broker/member execution. AIDY supplies bounded independent point-in-time Gold market/context truth. The databases remain separate. Shadow research does not gain broker authority.

## Next

**Day 8 — forward-only learning boundary and legacy closure.** Historical/provider evaluation must use only the provider profile version actually knowable at that timestamp. Day 7 bootstrap/current state must never be projected backward.

Before production work, verify Render, the production branch, Postgres and AIDY runtime again. Runtime truth overrides Memory.
