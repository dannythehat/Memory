# AIDY — Current State

Last verified: **2026-09-06**

Authoritative repo: `dannythehat/Aidy-Gold-Signals`
Authoritative branch: `main`
Verified source `main` SHA: `b860e1b83e9f5bbfd52c94453c86443e2c16b276`
Live Worker: `aidy-signals-test`
Verified live Worker version: `d124b317-708d-4f57-afbb-3bd6844a32cf`

## Provider Intelligence sequence

The September Provider Intelligence sequence is complete through **Day 10**.

- Day 7 — immutable provider identity/style/behaviour history — GREEN / PRODUCTION VERIFIED.
- Day 8 — forward-only provider learning boundary + legacy closure — GREEN / PRODUCTION VERIFIED.
- Day 9 — canonical AIDY point-in-time context join — GREEN / PRODUCTION VERIFIED.
- Day 10 — immutable per-signal provider + AIDY context attachment — GREEN / PRODUCTION VERIFIED.

## Day 9

AIDY now exposes an authenticated read-only `/provider/context` route. It resolves only a scheduled Gold snapshot that existed at or before the requested provider-signal timestamp and rebuilds the existing Architecture V2 context/regime from point-in-time evidence. The route is research/private-forward only and has no broker or live-money authority.

Day 9 source is merged at `b860e1b83e9f5bbfd52c94453c86443e2c16b276`. The live code-only rollout preserved the existing bearer secret, capture configuration, scheduler and D1 schema. Verification proved `/provider/context` and `/market/ohlc` remain bearer protected, capture remains ON, Twelve Data remains the source and formal-forward remains OFF.

## Day 10

Super Signals now persists one immutable context attachment per qualifying forward provider signal. Each record freezes the exact provider profile version plus the exact AIDY point-in-time context/snapshot identity used for that signal. AIDY itself does not gain provider ownership or broker authority.

The first genuine attachment row is **waiting for the next real PIT-clean provider signal**. This is not a build blocker: production currently has zero eligible resolved forward signals waiting for attachment, and the live attachment resolver reports `attached=0 failures=0`.

## Exact next step

**Day 11 — execution-cost and paper ↔ broker calibration.**

Measure how theoretical/provider-research performance differs from executable reality: spread, slippage, actual fill/entry differences, broker costs and paper-vs-broker divergence. This remains research/calibration work and must not change live provider sizing or broker authority without a later evidence/owner gate.

## Safety posture

- AIDY remains independent Gold market/context intelligence.
- Super Signals owns provider identity, interpretation, Provider Lab research and broker/member execution.
- Formal-forward remains OFF.
- 40 shadow discovery providers remain broker-isolated and distinct from the 5 real/testing providers.
- No historical/future information may leak into point-in-time provider evidence.
- Runtime/source/database evidence overrides Memory if they disagree.

## Session rule

Before Day 11, read the latest Day 10 handover, then verify AIDY source/live Worker, Super Signals live branch/deploy and production databases. Repair Memory first if reality differs.