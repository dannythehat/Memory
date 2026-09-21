# AIDY expert-gate environment blueprint — 2026-09-21

## Status

**APPROVED PLAN / NOT BUILT**

This handover closes the research/architecture milestone only. No AIDY implementation code or live runtime was changed.

## What was researched

The planning pass audited the existing AIDY stack before proposing new tooling. Existing reusable assets include PIT/live Gold capture, multi-timeframe features, price structure, swing/reclaim logic, volatility and jump work, macro-event intelligence, rates vintages, cross-market context, CME/futures research, historical Databento GC TBBO microstructure, analogue retrieval, movement memory, contextual marker scoring and the canonical 34-capability toolbox.

External research was used to shape the environment/gate taxonomy around session/time-of-day effects, Gold macro-event response, changing rates/USD relationships, systematic structure recognition, momentum horizons, jump-vs-continuous volatility and microstructure/order-flow concepts.

## Architecture decision

AIDY must know the environment first.

Each expert gate receives:
1. the same frozen PIT-safe global Gold environment; and
2. a smaller specialist mini-environment relevant to that gate.

Each gate then runs multiple auditable sub-calculators, explains its conclusion, records contradictions and exposes current conviction separately from historical reliability.

Historical reliability is environment-specific, sample-aware and hierarchical. Small exact-context samples must shrink toward broader gate/family priors. Exact context may only dominate when evidence is sufficient.

Correlated evidence must be penalised so the same price move is not counted repeatedly through M5/M15/momentum variants.

UNKNOWN, ABSTAIN and context-only outputs are first-class states.

## Blueprint

Canonical document:

`projects/aidy/GOLD_EXPERT_GATE_ENVIRONMENT_BLUEPRINT.md`

It defines **24 sequential builds** with an acceptance gate after each build. Major stages are:

1. Environment Contract v3
2. Expert Gate Contract v1
3. Conditional Trust & Score Engine v3
4. Common Price Expert Mathematics
5-9. M5 / M15 / H1 / H4 / D1 experts
10. Momentum / Impulse
11. Price Location
12. Liquidity / Reclaim
13. Volatility / Jump
14. Session / Participation
15. Macro / Event
16. Rates / USD / Cross-Asset
17. Futures / Microstructure
18. News / Movement Mechanism
19. Analogue / Episode
20. Dependency & Double-Counting
21. Environment-Aware Gate Selector
22. AIDY Meta Aggregator & Explanation
23. Chronological Replay / Ablation / Holdout
24. Live Forward Shadow Soak & Permanent Scorecard

## Tooling decision

No new paid tool is required to begin Builds 1-16.

The existing AIDY stack is sufficient for the first programme stages. Live COMEX/Databento microstructure should only be considered after historical GC TBBO evidence proves independent out-of-sample value. No paid live market-data activation is authorized by this blueprint.

## Safety

- Formal-forward remains OFF.
- AIDY live-money authority remains OFF.
- Super Signals 1% owner-risk rule is unchanged.
- No broker/execution/provider-production logic changed.
- No-hindsight/PIT rules remain mandatory.
- The current simple 15-minute gates remain a legacy baseline until the expert system proves superior out of sample.

## Exact next step

Start **Build 1 — Environment Contract v3** in `dannythehat/Aidy-Gold-Signals` only when implementation begins.

Do not skip ahead to H1/M15 expert coding before Builds 1-4 pass their acceptance gates.
