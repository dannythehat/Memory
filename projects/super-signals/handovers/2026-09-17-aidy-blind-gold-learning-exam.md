# AIDY blind Gold learning exam — 2026-09-17

## Owner direction

Danny asked to stop re-running already-proven Claude decision-ledger tests and instead test whether AIDY actually understands Gold, learns provider/market relationships, and becomes measurably smarter over time.

## AIDY repo work

Repository: `dannythehat/Aidy-Gold-Signals`
PR: #135 `Add forward-only blind Gold learning exam`
Branch: `feature/blind-gold-learning-exam-20260917`
Latest branch commit at this handover: `3492beaf064780469367a28564bef3739aec18e9`
Status: open / research-only / not deployed at this handover.

Implemented:
- governed chronological blind-exam scorer;
- directional accuracy and Brier scoring when AIDY actually emitted confidence;
- difficulty ladder 1–5;
- explicit `insufficient_evidence`, `memory_accumulating`, `learning_candidate`, `learning_observed`, and regression state;
- learning is never claimed merely because memory-card count increases;
- read-only D1 bridge from immutable AIDY episode memory + score-eligible forward outcomes;
- PIT count of learning cards that genuinely existed before each episode; same episode's future card excluded;
- frozen market-context extraction from episode evidence: market structure, volatility, liquidity/spread state, session and event state where actually present;
- difficulty derived only from frozen contemporaneous features, never future outcome;
- context coverage report so missing intelligence is exposed instead of backfilled/fabricated;
- tests for PIT-only context enrichment and missing-context preservation.

## Existing architecture leveraged

AIDY already materializes immutable episode memory, forward outcomes and structured learning cards. Episode runtime preserves `regime_state`, `setup_state`, confidence/setup/reason codes and compact context summary where they existed ex ante. The blind exam consumes this rather than creating a second learning system.

## Important limitation / next evidence step

The scorer and PIT bridge are built, but this handover does NOT claim AIDY has become smarter yet. The branch still needs its real production/D1 scorecard run and adequate chronological unseen samples. If later batches do not improve, state must remain `memory_accumulating` or regression; never relabel that as learning.

Provider identity/context is not fabricated when it is absent from AIDY episode memory. Provider-conditioned learning should be joined only from a PIT-safe identity/context source.

## Safety boundaries

- research only;
- no broker/live-money authority;
- no Super Signals execution-rule change;
- 1% live-risk directive unchanged;
- future authority remains class-by-class and requires separate forward evidence.
