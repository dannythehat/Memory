# AIDY Expert-Gate Programme — Build 14 Session / Participation Expert

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 15 — Macro / Event Expert

## What was built

Build 14 adds:

`aidy_gold_session_participation_expert_v1`

This expert is context-only. It describes likely regional participation and whether current activity is unusual for the exact time; it cannot create BUY/SELL direction.

It uses:
- DST-safe London and New York session logic;
- Asia regional hours;
- active-market list;
- London/New York overlap state;
- frozen session phase;
- completed-M1 15-minute realised volatility and range;
- matched weekday × UTC 15-minute clock baselines;
- event-clean baseline history when enough clean observations exist;
- existing Day-42 genuine GC trade-volume and pre-trade BBO spread z-scores when qualified.

## DST safety

Build 14 reuses the deterministic market-session engine:
- modern UK DST;
- modern US DST;
- fixed Tokyo offset.

Acceptance explicitly covers UK and US transition weeks.

## Participation baseline

Current volatility/range is compared only with:
- the same UTC weekday;
- the same 15-minute UTC clock slot;
- prior observations only.

When enough event-clean history exists, event-confounded rows are excluded from the ordinary session baseline.

## Genuine GC activity

Build 14 reuses the Day-42 GC microstructure contract.

Qualified context can include:
- genuine exchange trade-volume z-score;
- genuine pre-trade BBO spread z-score.

Boundaries remain explicit:
- ordinary session activity cannot count as alpha;
- no depth claim;
- no order-book-imbalance claim;
- retrospective GC context remains research-only unless PIT-qualified.

## Event confounding

If the current timestamp is close to a scheduled event, Build 14 records `event_time_confounded`.

It does not automatically attribute unusual activity to London, New York or Asia and it does not claim the event caused the activity.

## Directional safety

There is no:
- London bullish rule;
- New York bearish rule;
- Asia mean-reversion rule;
- session-derived directional vote.

Session context may affect later trust, but it cannot create direction by itself.

## Acceptance

AIDY PR #217 merged:
`58a0425f717342dba28ce67e199087f3e96645f3`

Final exact-candidate checks:
- Evidence Semantic Change Gate: PASS — run `35594582685`
- static checks: PASS
- focused workflow suite: 263 passed
- full repository regression: 1515 passed — run `35594582710`

Acceptance coverage included:
- context-only/no-direction contract;
- UK DST transition;
- US DST transition;
- London/New York overlap;
- matched weekday-clock activity;
- event-clean historical baseline selection;
- current event-time confounding;
- genuine GC volume/spread descriptive context;
- PIT-qualified versus retrospective GC distinction;
- unqualified GC remains UNKNOWN;
- insufficient matched-clock history remains UNKNOWN;
- completed-M1 PIT provenance;
- chronological freeze.

## Production / execution status

No Worker deployment was required because Build 14 is an expert library and is not wired into live gate weighting.

Build 14 does not:
- change Super Signals execution;
- change provider activation;
- change owner 1% risk;
- replace the current live marker brain;
- enable formal-forward authority;
- grant live-money authority.

## Next build

**Build 15 — Macro / Event Expert**

Build 15 will turn the existing official macro/event stack into a Gold-specific specialist using:
- official BLS/BEA/Fed/global central-bank schedules;
- event classes;
- pre-event features;
- consensus, actual and revision separation;
- Gold-learned event tiers;
- standardized surprise where valid;
- event clustering;
- post-release confirmation;
- historical conditional response.

Acceptance requires:
- pre-event logic cannot see the actual release;
- actual values enter only after first-observed timestamp;
- revisions remain separate from first print;
- event tiers come from independent Gold episodes rather than vendor labels;
- no-news periods provide a control sample.

No Build 16 work begins until Build 15 passes its acceptance gate.
