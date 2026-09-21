# AIDY Expert-Gate Programme — Build 18 News / Movement Mechanism Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 19 — Analogue / Episode Expert

## What was built

Build 18 adds `aidy_gold_news_movement_mechanism_expert_v1` and a bounded Finnhub market-news adapter.

It starts from the already frozen Gold movement investigation, then layers:
- PIT scheduled-event mechanism context;
- Finnhub market news from `/news` using `general` and `forex`;
- publisher timestamp plus local first-observed timestamp;
- source-authority classification;
- duplicate/syndicated-story collapse;
- mechanism tagging across Fed policy, inflation, labour/growth, USD/rates, geopolitics, trade policy, risk sentiment, energy/inflation and Gold-specific context;
- evidence agreement/disagreement state.

## Causality guardrail

Build 18 never says a headline caused the move merely because it appeared nearby in time.

Possible states include:
- scheduled-event context only;
- single credible news source;
- credible sources agree;
- scheduled event + news agree;
- credible sources disagree and remain unresolved;
- unsupported narrative;
- UNKNOWN.

Unsupported narratives are retained for audit but cannot become evidence.

News never becomes an automatic bullish/bearish vote.

## Finnhub source contract

Provider: Finnhub  
Endpoint: `/news`  
Categories: `general`, `forex`  
Runtime secret name: `FINNHUB_API_KEY`

The adapter fails closed without a key.

The API key currently exists on Render from earlier work. It is not stored in AIDY GitHub secrets, so the optional real Finnhub workflow smoke was not run in GitHub. The mocked HTTP adapter test proves the request/schema contract and this live smoke is not part of Build 18 acceptance.

## Acceptance

- exact tested head: `6ca20729e1925dde30d2cfe123648371d437e648`
- PR #225 merge: `5270f17b536d496d39d231b52da76ad391d4a610`
- AIDY repo handoff merge: `160673ea6172bb3aa182a03ab5b02475edceffd7`
- semantic gate: PASS — `35608776114`
- acceptance workflow: PASS — `35608776007`
- focused suite: 61 passed
- full repository regression: 1577 passed
- scheduled event: PASS
- credible news: PASS
- duplicate collapse: PASS
- unsupported narrative: PASS
- UNKNOWN: PASS
- disagreement unresolved: PASS
- event/news agreement: PASS
- future-news exclusion: PASS
- no directional authority: PASS
- mocked Finnhub transport/schema: PASS
- missing key fail-closed: PASS

## Boundaries preserved

Build 18 does not:
- grant live-money authority;
- change owner 1% risk;
- change Super Signals execution/provider rules;
- create formal-forward authority;
- turn news into a directional trading signal;
- claim causality from temporal proximity.

## Next

**Build 19 — Analogue / Episode Expert**

Use existing movement episode memory and analogue retrieval v1/v2/v3 plus semantic analogue work.

Acceptance requires:
- no outcome field in similarity vector;
- duplicate episodes collapsed;
- exact PIT reconstruction;
- positive and counterexample retrieval;
- chronological holdout only.

No Build 20 work begins until Build 19 passes its acceptance gate.
