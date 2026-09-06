# Super Signals — Current State

Last verified: **2026-09-06**

Authoritative repo: `dannythehat/super-signals`
Production branch: `feature/day-10-shared-telegram-sources`
Live production SHA: `0ea04e9a118b7ae2782cb890a35d9725e1f16746`
Render service: `super-signals-day-8`
Live deploy: `dep-daeoomp5efls73a5134g`
Alembic head: `0057_provider_pit_boundary`

## Provider populations

- 40 shadow discovery providers — research only, broker-isolated.
- 5 testing providers — current real execution population.
- 14 paused.
- 4 revoked.

Never mix the 40 shadow discovery providers with the 5 real/testing providers.

## Provider Intelligence sequence

- Day 7 — provider identity/style/behavioural-profile versioning — GREEN / PRODUCTION VERIFIED.
- Day 8 — forward-only learning boundary + legacy closure — GREEN / PRODUCTION VERIFIED.

## Day 8 production proof

Day 8 made the immutable Day 7 provider-profile ledger operationally authoritative for historical/forward research.

Production facts:

- PR `#141` merged to the production branch;
- live SHA `0ea04e9a118b7ae2782cb890a35d9725e1f16746`;
- Render deploy `dep-daeoomp5efls73a5134g` is live;
- migration `0057_provider_pit_boundary` applied successfully;
- production API quality: **752 passed, 67 skipped**;
- GitHub API gate passed against PostgreSQL 18 with the migration chain upgraded through Day 8;
- web typecheck/lint/tests/build passed;
- secret scan passed;
- `/health` returned 200 on the new instance;
- Provider Lab AIDY resolver startup reported `processed=0 failures=0`;
- no error-level Render events were observed after the new instance became live during verification.

Real production Postgres PIT/legacy closure:

- research trades: **144**;
- `legacy_unresolvable`: **144**;
- legacy score-eligible trades: **0**;
- formerly score-eligible legacy rows quarantined: **6**;
- invalid legacy provenance rows: **0**;
- resolved-profile provenance mismatches: **0**;
- provenance trigger `trg_shadow_trade_provider_profile_pit`: enabled.

Every pre-Day-7 research trade predates its source's immutable provider-profile history origin. Day 8 therefore does not manufacture historical provider knowledge. Those rows remain available as legacy research records but cannot count as PIT-clean fair-score evidence.

New research enrollment stamps the immutable provider profile version already effective at `signal_posted_at`; unresolved timestamps fail closed. Provider-aware historical AI context now resolves only provider-profile history as of the actual message timestamp and no longer falls back to today's mutable profile/adaptive grammar.

## Cross-project boundary

Super Signals owns provider identity, interpretation, profile history, benchmark/replay and broker/member execution. AIDY supplies bounded independent point-in-time Gold market/context truth. The databases remain separate. Shadow research does not gain broker authority. Formal-forward remains OFF.

## Next

**Day 9 — canonical AIDY context join.**

Join each PIT-clean provider setup to only the independent market/session/regime context that AIDY itself knew at that timestamp. Both temporal boundaries must remain clean: provider knowledge from Super Signals and market/context knowledge from AIDY.

Before production work, verify Render, the production branch, Postgres and AIDY runtime again. Runtime truth overrides Memory.
