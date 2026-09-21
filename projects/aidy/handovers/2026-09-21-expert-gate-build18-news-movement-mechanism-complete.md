# AIDY Expert-Gate Programme — Build 18 News / Movement Mechanism Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 19 — Analogue / Episode Expert

## What was built

Build 18 adds:
- `aidy_gold_news_movement_mechanism_expert_v1`;
- `aidy_finnhub_market_news_adapter_v1`;
- bounded Finnhub source contract using `FINNHUB_API_KEY`;
- scheduled-event/news evidence comparison;
- publication + first-observed timestamp enforcement;
- source-authority state;
- duplicate/syndicated story collapse;
- mechanism-tag extraction;
- evidence agreement/disagreement;
- unsupported-narrative rejection;
- explicit UNKNOWN handling;
- strict no-causality/no-direction boundary.

## Acceptance

Exact tested candidate:
`6ca20729e1925dde30d2cfe123648371d437e648`

Implementation merge:
`5270f17b536d496d39d231b52da76ad391d4a610`

Repository handoff:
`160673ea6172bb3aa182a03ab5b02475edceffd7`

Checks:
- Evidence Semantic Change Gate: PASS — `35608776114`
- Build 18 acceptance workflow: PASS — `35608776007`
- static/compile: PASS
- focused tests: 61 passed
- full regression: 1577 passed
- Memory handoff JSON/JSONL hygiene: validated by repository gate

Acceptance fixtures:
- scheduled event: PASS
- credible news: PASS
- duplicate story collapse: PASS
- unsupported narrative: PASS
- UNKNOWN: PASS
- source disagreement remains unresolved: PASS
- event/news agreement without causal claim: PASS
- future news excluded from frozen packet: PASS
- news directional vote: DISALLOWED

## Finnhub status

The user's existing API is Finnhub. The same key exists on the separate Super Signals Render runtime as `FINNHUB_API_KEY`.

Build 18 deliberately does not create a Super Signals dependency or copy that secret across products. The AIDY adapter is ready for the key in AIDY's own secret store and includes an authenticated workflow-dispatch smoke test for that moment.

This does not block Build 18 acceptance because the blueprint allows the live-news branch to remain non-live while the expert/source contract itself is built and proven.

## Boundaries

Build 18 does not:
- infer causality from one headline;
- use unsupported narratives as evidence;
- allow duplicate headlines to manufacture confirmation;
- turn news into automatic bullish/bearish direction;
- grant live gate weight;
- change Super Signals execution/provider rules;
- change owner 1% risk;
- grant live-money authority.

## Next build

**Build 19 — Analogue / Episode Expert**

Use movement episode memory and analogue retrieval without hindsight. Add gate-state/environment similarity, duplicate collapse, symmetric counterexamples and continuation/retrace distributions. Outcome fields must not enter the similarity vector.
