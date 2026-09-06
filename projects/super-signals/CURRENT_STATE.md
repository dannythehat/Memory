# Super Signals — Current State

Last verified: **2026-09-06**

Authoritative repo: `dannythehat/super-signals`
Production branch: `feature/day-10-shared-telegram-sources`
Live production SHA: `634838b5a559a425a1fe54af5bf7c022763f2743`
Render service: `super-signals-day-8`
Live deploy: `dep-daepomp7lnhs73f213eg`
Alembic head: `0058_provider_aidy_context`

## Provider populations

- 40 shadow discovery providers — research only, broker-isolated.
- 5 testing providers — current real execution population.
- 14 paused.
- 4 revoked.

Never mix the 40 shadow discovery providers with the 5 real/testing providers.

## Provider Intelligence sequence

- Day 7 — immutable provider identity/style/behaviour history — GREEN / PRODUCTION VERIFIED.
- Day 8 — forward-only provider learning boundary + legacy closure — GREEN / PRODUCTION VERIFIED.
- Day 9 — canonical AIDY point-in-time context join — GREEN / PRODUCTION VERIFIED.
- Day 10 — immutable per-signal provider + AIDY context attachment — GREEN / PRODUCTION VERIFIED.

## Day 9

Super Signals can request the canonical AIDY market/session/regime context for a provider signal timestamp, but only after Day 8 has proved the provider profile itself is PIT-clean. Legacy/unresolvable provider history is rejected before the context join.

Day 9 production SHA was `a5798a60af30a5c4e051aa90540e2a3ea1ae6779`; Render health was 200, M1 research was `processed=0 failures=0`, and no post-cutover error-level events were observed.

## Day 10

Migration `0058_provider_aidy_context` creates `provider_signal_context_attachments`, one immutable record per qualifying signal. It freezes the exact provider-profile version and exact AIDY PIT context/snapshot provenance. Database guards reject future provider/AIDY context, duplicate signal attachments, mutable history and any live-money authority.

Production proof:

- PR `#143` merged;
- live SHA `634838b5a559a425a1fe54af5bf7c022763f2743`;
- Render deploy `dep-daepomp7lnhs73f213eg` is live;
- Render API quality: **766 passed, 67 skipped**;
- migration `0058_provider_aidy_context` applied;
- `/health` returned 200;
- M1 resolver: `processed=0 failures=0`;
- context attachment resolver: `attached=0 failures=0`;
- post-cutover error-level logs: 0;
- attachment-table invalid future rows: 0;
- attachment-table live-money rows: 0;
- duplicate signal attachments: 0;
- both validation and immutability triggers are enabled;
- PIT-resolved forward signals currently waiting for attachment: 0.

There are currently zero attachment rows because no genuine post-boundary PIT-clean provider signal exists yet. Historical/legacy rows were deliberately not backfilled. The next qualifying real signal will be attached automatically.

## Cross-project boundary

Super Signals owns provider identity, interpretation, Provider Lab research and broker/member execution. AIDY supplies independent point-in-time Gold context. Day 10 enrichment is asynchronous and isolated from live execution. A failed context lookup cannot stop M1 research or delay/mutate broker routing.

## Next

**Day 11 — execution-cost and paper ↔ broker calibration.**

Calibrate Provider Intelligence against executable reality: spread, slippage, actual fill/entry differences, broker costs and paper-vs-broker divergence. No live sizing or execution authority should change merely because Day 11 is built.
