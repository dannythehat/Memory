# AIDY contextual marker learning brain — LIVE

Date: 2026-09-21

## Live runtime

AIDY repo runtime code merged at:
`6f9b607c0201bec77f5996126d158914864d58e5`

Repository main after temporary audit cleanup:
`a2c029b9954b2b06964b8cd7f1c9d60d35458192`

Canonical Worker:
`aidy-signals-test`

Worker version:
`a264b7b3-e26a-406f-827f-2ebd7f128740`

Successful deploy run:
`35562116744`

Verified:
- minute cron present
- capture enabled
- Twelve Data/public-independent source
- formal forward OFF
- live-money authority OFF
- Gold cycle memory `aidy_gold_cycle_memory_v2`
- contextual marker brain `aidy_gold_contextual_marker_brain_v1`

## Owner learning model now implemented

Every 15-minute Gold cycle evaluates the complete canonical Gold toolbox.

Current catalogue: **34 capabilities**.

Each capability is recorded every cycle as one of:
- scoreable directional marker;
- live environment/context marker;
- downstream context not available in standalone cycle;
- known research not live/PIT connected;
- known unknown.

AIDY never fabricates a directional vote just to give a tool a score.

Directional evidence currently includes any legitimately available signals such as:
- M5 structure/move;
- M15 structure/move;
- H1 structure;
- H4 structure;
- D1 structure when available;
- measured liquidity reclaim proxies when they imply direction;
- abnormal movement detector;
- historical cycle analogue direction when minimum evidence exists.

Contextual/non-directional tools still shape the environment fingerprint and remain available for future scoring once they produce a defensible directional marker.

## Environment scorebooks

Each marker result updates multiple contextual scorebooks simultaneously:
1. global;
2. session;
3. session + observed 15m state;
4. higher-timeframe environment;
5. session + movement/range regime;
6. session + state + event timing;
7. full environment fingerprint.

This lets AIDY learn that a tool may be useful in one Gold environment and poor in another rather than assigning one universal score.

The selected profile uses the most specific environment with enough sample size and falls back toward broader scopes while data is thin.

## Fair marker scoring

Marker outcome score range is **-2 to +2**.

Current rule:
- +2: correct marker on a meaningful/large directional move;
- +1: correct marker on a normal directional move;
- 0: unavailable/unscoreable;
- -1: wrong marker on a normal directional move;
- -2: wrong marker on a meaningful/large directional move.

Current explicit large-move threshold:
`abs(realised 15m return) >= 5 bps`.

Plain correct/incorrect counts and accuracy are stored separately from impact score, so a small number of large moves cannot hide basic accuracy.

## Learned weighting safeguard

Original marker weights remain bootstrap priors.

Contextual performance creates a learned multiplier bounded to:
- minimum 0.5x;
- maximum 1.5x.

The multiplier strengthens gradually with sample size and reaches full reliability scaling only after 20 observations.

More-specific contexts require minimum samples before selection:
- full environment: 8;
- session+state+event: 7;
- session+move regime: 6;
- higher timeframe: 5;
- session+state: 5;
- session: 4;
- global: 1.

Thus one or two results cannot dominate the Gold view.

## Immediate learning proof

The already-resolved 04:00-04:15 UTC cycle was backfilled automatically after deployment.

Realised move was bullish +6.8 bps, therefore a large move under the current impact rule.

The frozen markers scored:
- H4 bullish: **+2**, correct;
- H1 bearish: **-2**, incorrect;
- M15 completed-bar structure bearish: **-2**, incorrect;
- recent M15 movement bearish: **-2**, incorrect;
- M5 movement/structure bearish: **-2**, incorrect;
- abnormal Gold movement detector bearish: **-2**, incorrect for the final 15-minute direction.

Live D1 audit at 04:46 UTC showed:
- environments materialized: 1 initially, with subsequent cycle backfill continuing;
- marker observations: 6;
- marker results: 6;
- contextual score rows: **42** = 6 markers x 7 environment scopes.

The older 04:00/04:30/04:45 frozen views correctly retain the 33-tool manifest that existed when they were created. The current canonical catalogue is 34 tools including `gold_contextual_marker_brain`; new views after this deployment use the new catalogue.

## Learning flow

The live cycle sequence is now:

`environment -> evaluate full toolbox -> freeze scoreable marker votes + all-tool coverage -> retrieve contextual marker histories -> apply bounded learned multipliers -> form/freeze AIDY view + reasoning -> observe 15m result -> score each marker -2..+2 -> update all contextual scorebooks -> use qualified scores on later cycles`

The marker observations preserve:
- stable marker identity;
- parent toolbox surface;
- source path;
- directional vote;
- bootstrap weight;
- selected score scope;
- selected sample count;
- selected net score/accuracy;
- learned multiplier;
- effective weight.

Provider Context exposes the latest marker profiles so downstream reasoning can cross-check which learned trust values affected AIDY's view.

## Safety boundary

No changes were made to:
- Super Signals execution;
- MetaAPI / MT5 / Vantage;
- owner 1% risk;
- provider activation rules;
- live-money authority.

This is a research/learning layer only.

## Completion gate

Complete:
1. schema migration 0024 applied to live D1;
2. contextual brain code merged;
3. full regression passed;
4. Worker deployed;
5. health/version verified;
6. cron verified;
7. first resolved cycle backfilled;
8. +2/-2 impact scoring verified in live D1;
9. seven-scope contextual scorebooks verified;
10. all-tool coverage persisted;
11. temporary audit workflow removed;
12. Memory handoff updated.

The brain is now accumulating forward evidence immediately. New cycle views will increasingly prefer environment-specific marker trust as sample sizes become sufficient.
