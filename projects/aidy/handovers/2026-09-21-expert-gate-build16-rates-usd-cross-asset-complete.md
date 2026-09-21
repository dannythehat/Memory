# AIDY Expert-Gate Programme — Build 16 Rates / USD / Cross-Asset Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 17 — Futures / Microstructure Expert

## What was built

Build 16 adds `aidy_gold_rates_usd_cross_asset_expert_v1`.

It is a context-only mechanism specialist for:
- DGS2 / DGS10 / DFII10 / T10YIE;
- policy-path futures;
- broad USD;
- EURUSD / USDJPY;
- SI / ES / VIX;
- qualified intraday Treasury and related futures.

## No permanent sign assumptions

Build 16 contains no rule such as:
- USD up = Gold down forever;
- real yields up = Gold down forever.

Instead, rolling Gold beta/correlation is estimated inside the current compound regime.

Positive, negative, weak and sign-flipping relationships are all valid states.

A historical regime where Gold rises together with USD or real yields is therefore representable and acceptance-tested.

## Frequency safety

PIT-vintaged DGS2/DGS10/DFII10/T10YIE remain daily cash-rate context.

They can provide:
- latest value;
- 1/5/20-observation changes.

They cannot provide:
- 15-minute reaction;
- 60-minute reaction.

Official daily/fix broad USD, EURUSD, USDJPY and VIX context is also prevented from masquerading as intraday reaction data.

Only genuinely timestamped exchange observations may carry intraday changes, and only when current evidence is fresh and decision-qualified.

## Dependency control

Correlated mechanisms are explicitly grouped:
- rates curve;
- policy path;
- USD mechanism;
- precious complex;
- risk state.

Cross-asset breadth counts one representative per dependency group instead of treating every correlated series as an independent vote.

## Relationship stability and divergence

Build 16 records:
- rolling correlation;
- rolling beta;
- relationship sign;
- first-half versus second-half correlation;
- stability state;
- sign-flip state.

Divergence means current Gold is moving opposite to the empirical current-regime relationship. It does not mean “opposite to a textbook sign.”

## Acceptance

AIDY PR #219 merged:
`e9f992b71246eec029b7a8449e3143ff855b057f`

Final exact-candidate checks:
- Evidence Semantic Change Gate: PASS — run `35597301241`
- static checks: PASS
- focused workflow suite: 292 passed
- full repository regression: 1544 passed — run `35597301237`

Acceptance coverage included:
- context-only / no permanent sign;
- positive Gold-with-USD relationship;
- positive Gold-with-real-yield relationship;
- relationship sign flip;
- daily cash-rate intraday guard;
- daily USD/FX/VIX intraday guard;
- fresh exchange futures intraday changes;
- stale exchange observation intraday rejection;
- retrospective current observation not decision-qualified;
- same-mechanism dependency tagging;
- one-representative-per-group breadth;
- learned-sign divergence;
- future relationship row exclusion;
- insufficient regime history UNKNOWN;
- future cross-asset observation exclusion;
- future rate vintage exclusion;
- environment-specific Build-3 trust scopes.

## Production / execution status

No Worker deployment was required because Build 16 is an expert library and is not wired into live gate weighting.

Build 16 does not:
- change Super Signals execution;
- change provider activation;
- change owner 1% risk;
- replace the current live marker brain;
- enable formal-forward authority;
- grant live-money authority.

## Next build

**Build 17 — Futures / Microstructure Expert**

Phase A will test whether genuine historical COMEX information adds independent value beyond spot OHLC experts using:
- GC TBBO;
- signed aggressor imbalance;
- BBO spread;
- exchange trade volume;
- anchored/session VWAP;
- clock-normalised baselines;
- contract/roll state;
- CME volume/open interest where genuinely available.

Phase B remains separately gated:
- live/delayed data entitlement and pricing review;
- owner approval before recurring paid data;
- PIT contract before any live use.

No depth claim is allowed without depth data, and no paid feed may be activated merely to increase feature count.

No Build 18 work begins until Build 17 passes its acceptance gate.
