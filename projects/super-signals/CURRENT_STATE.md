# Super Signals — Current State

Last verified: **2026-09-07**

Authoritative repo: `dannythehat/super-signals`
Production branch: `feature/day-10-shared-telegram-sources`
Live production SHA: `e4afce8207933339e6745478363228dc75154d51`
Render service: `super-signals-day-8`
Live deploy: `dep-daf9ipuq1p3s73dn6kn0`
Alembic head: `0062_provider_day13_conditional`

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
- Day 11 — execution-cost and paper ↔ broker calibration — COMPLETE / PRODUCTION VERIFIED as a partial fail-closed provider disposition; not universal reconciliation GREEN.
- Day 12 — fingerprint core + hierarchical statistics harness — ENGINEERING GREEN / PRODUCTION VERIFIED; statistical authority WAITING-FOR-FORWARD-EVIDENCE.
- Day 13 — conditional fingerprints + preregistration + BH FDR + effect-size gates + shrunken conditional posteriors — **ENGINEERING GREEN / PRODUCTION VERIFIED; statistical authority WAITING-FOR-FORWARD-EVIDENCE.**

## Day 13 — conditional preregistration and FDR harness

PR `#148` built the Day 13 research harness. Its delivery head `987e2cfe1602a81284c4c620ca0103c687a85e86` passed `api`, `web` and Workers checks and merged as `db5f026a5a289a2c634a8c4037e56ca1072f552c`. Production migration `0062_provider_day13_conditional` applied successfully and froze the preregistration before confirmatory evidence.

The first production research run then failed closed because the loader queried a non-existent attachment alias `context_as_of_utc`; production stores the canonical field as `aidy_context_as_of_utc`. No execution, sizing, provider authority or live-money path was affected. PR `#149` fixed only that production schema binding. Exact hotfix head `80c2e6e1713d8f1a542814e878a706fe268977ea` passed `api`, `web` and Workers checks, merged as `e4afce8207933339e6745478363228dc75154d51`, and deployed live as `dep-daf9ipuq1p3s73dn6kn0`.

The original preregistration remained immutable through the hotfix:

- registry: `provider_day13_preregistered_v1`;
- shadow providers: **40**;
- hypotheses: **15,360**;
- unique preregistration digests: **15,360**;
- frozen OOS boundary: **2026-09-07T10:50:52.042190Z** for every hypothesis;
- directions: BUY / SELL;
- Super Signals session buckets: asia / europe / ny_early / other;
- realized-duration buckets: `<15m`, `15m–60m`, `1h–4h`, `>=4h` — descriptive post-entry only;
- AIDY regime facets use canonical `aidy_gold_regime_v1` known labels; `unknown` is not guessed into confirmatory evidence.

Builder-proposed statistical gates are frozen but **not owner-approved statistical authority**:

- minimum OOS N: **30** per cell and matched complement;
- global Benjamini–Hochberg FDR family: `provider_day13_v1_global`;
- proposed FDR q: **0.05**;
- proposed minimum absolute shrunken effect: **0.25R**;
- threshold approval status: `PROPOSED_UNAPPROVED`.

Production run `717adf78-f8a0-4934-b766-91e15431bb0a` completed against live SHA `e4afce8207933339e6745478363228dc75154d51` with:

- model: `provider_day13_v1`;
- engineering status: `ENGINEERING_PROVEN`;
- deterministic known-signal/pure-noise simulation acceptance: **passed**;
- statistical status: `WAITING-FOR-FORWARD-EVIDENCE`;
- provider count: **40**;
- preregistered hypotheses: **15,360**;
- eligible post-preregistration OOS trades: **0**;
- tested hypotheses: **0**;
- BH rejections: **0**;
- builder-gate candidates: **0**;
- authoritative discoveries: **0**;
- evidence digest: `8b6873c76b2c1cee5a37866a2048d967865be189ec26e526a0673b88ed61a7ea`;
- `research_only=true`;
- `live_money_execution_allowed=false`.

Zero tested hypotheses is the correct state immediately after preregistration: existing history is not reused as confirmatory OOS evidence. Day 13 engineering is therefore complete and production verified while real provider statistical conclusions correctly remain WAITING until genuinely new eligible evidence arrives.

## Cross-project boundary

Super Signals owns provider identity, Provider Lab research and broker/member execution. AIDY supplies bounded independent market/context evidence only. Day 13 reads only canonical attached PIT context already stored in Super Signals; it does not write to AIDY/D1 and cannot mutate broker/member execution, provider live status, routing, sizing or AIDY authority.

## Exact next step

Day 13 needs no further engineering closure work. Allow genuinely post-preregistration, PIT-resolved, score-eligible shadow evidence to accumulate under the frozen Day 13 registry. Statistical authority remains `WAITING-FOR-FORWARD-EVIDENCE`. **Day 14 is NOT STARTED and requires separate owner instruction.**
