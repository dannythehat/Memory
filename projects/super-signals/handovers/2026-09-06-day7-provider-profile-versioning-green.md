# Super Signals Day 7 — Provider Profile Versioning — GREEN

Date: 2026-09-06
Status: **PRODUCTION VERIFIED**

Production branch: `feature/day-10-shared-telegram-sources`
Live SHA: `43eddfde8d584b26be807c4ff998f7fd7afad050`
Render service: `super-signals-day-8`
Deploy: `dep-daenlsh42hec73chgsf0`
Alembic head: `0056_provider_profile_versions`

## Delivered

A new append-only `provider_research_profile_versions` ledger records meaningful provider identity/style/behavioural-profile changes while `provider_research_profiles` remains the mutable current-state cache.

The version semantic fingerprint excludes `adaptive_v1.generated_at_epoch`, so a periodic refresh clock cannot manufacture fake intelligence history. A stable PIT as-of function returns only versions already effective at the requested timestamp. Existing provider state was bootstrapped at migration time only and was not backdated.

## Verified live

- Render quality: 745 passed, 67 skipped.
- 48 current provider profiles.
- 48 versioned provider sources.
- 130 profile-history rows observed.
- 0 duplicate `(source_id, version_no)` groups.
- 0 unversioned profiles.
- 0 provider version sequence gaps.
- 82 profile-update versions across 42 sources.
- 0 adjacent duplicate semantic fingerprints.
- 0 non-monotonic effective timestamps.
- append-only database trigger enabled.
- as-of lookup proved older-state selection.
- a timestamp before Day 7 bootstrap returned no profile version.
- live no-op/generated-at-only refreshes did not append history rows.
- no error-level Render events were observed after the deploy during verification.
- AIDY Provider Lab resolver startup reported `failures=0`.

The live Day 7 diff contains exactly three files: the migration, its tests and its gate document. No live broker/member execution, parser, risk, MetaAPI or trade-management code changed.

## Safety

The 40 shadow discovery providers remain broker-isolated and distinct from the 5 real/testing providers. Day 7 adds research memory, not trading authority.

## Next

**Day 8: forward-only learning boundary and legacy closure.** All provider research/replay must resolve provider state as-of the evidence timestamp; current/bootstrap profile knowledge may not leak backward.
