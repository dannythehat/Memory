# AIDY Gold Expert Gates & Environment Learning Blueprint

**Status:** RESEARCH BLUEPRINT ONLY — NO AIDY IMPLEMENTATION AUTHORIZED BY THIS DOCUMENT  
**Date:** 2026-09-21  
**Implementation repository when builds begin:** `dannythehat/Aidy-Gold-Signals`  
**Blueprint/continuity repository:** `dannythehat/Memory`

> **Progress update — 2026-09-21:** Builds 1-18 are COMPLETE. Build 18 News / Movement Mechanism Expert is engineering-proven with a bounded Finnhub market-news adapter, PIT timestamp/source authority, duplicate-story collapse, disagreement/UNKNOWN preservation, unsupported-narrative rejection and no directional authority. Build 19 — Analogue / Episode Expert — is next. The blueprint remains the authoritative sequential plan; do not skip acceptance gates.

## 1. Purpose

The current AIDY 15-minute contextual learning loop is a useful skeleton, but several directional gates are intentionally simple. In particular, a timeframe gate can presently reduce a rich price path to a coarse bullish/bearish close-path vote. That is deterministic, not random, but it is not intelligent enough to be the long-term basis of AIDY's Gold brain.

The next programme will turn each material evidence family into a small specialist or **expert gate**. Each expert gate will:

1. receive the same frozen point-in-time global Gold environment;
2. receive a smaller gate-specific mini-environment;
3. run multiple auditable sub-calculators;
4. return a conclusion or ABSTAIN/UNKNOWN;
5. explain exactly why;
6. carry separate current conviction and historical reliability;
7. be scored after the future window resolves;
8. learn different reliability under different environments;
9. remain observable even when its current weight is low so it can continue learning.

AIDY's meta-brain will then learn which expert gates deserve the most trust in the environment that exists **before** the next 15-minute Gold window begins.

This blueprint is deliberately staged. **Build N+1 must not start until Build N's acceptance gate passes.**

## 2. Core architecture decision

### 2.1 Environment first, then gates, then historical trust, then AIDY

The immutable order is:

1. Freeze the global Gold environment at decision time.
2. Build each gate's mini-environment from information available at that same time.
3. Each gate runs its own sub-calculators and produces its current conclusion, conviction, evidence and contradictions.
4. AIDY retrieves that gate/sub-calculator's historical performance under comparable environments.
5. Historical reliability is shrunk for small samples and backed off hierarchically when exact context is sparse.
6. AIDY adjusts gate trust using reliability, sample confidence, environment similarity, calibration and dependency penalties.
7. AIDY combines independent evidence into a final 15-minute view or abstains.
8. The complete decision packet is frozen.
9. Only after the target window ends is the outcome admitted.
10. Score AIDY, every directional gate and every scoreable sub-calculator.
11. Update environment-specific scorebooks for later cycles.

### 2.2 Do not create one gigantic environment ID

A full cross-product such as:

`session × phase × volatility × liquidity × H1 × H4 × location × event × USD × yields × ...`

would fragment data into thousands of rarely repeated cells.

Use a **factorised hierarchical environment** instead:

- global core dimensions shared by all gates;
- expert-specific mini-environment dimensions;
- exact-context scoring when sample support is sufficient;
- reduced-context backoff;
- gate-global prior as the final fallback;
- similarity retrieval as a secondary pointer, not a substitute for PIT-safe scorebooks.

### 2.3 Same gate, different score by environment

There is no permanent "H1 score".

Conceptually:

- H1 in London opening + expansion + accepted breakout can have one reliability;
- H1 in late Asia + compression + middle-of-range can have another;
- H1 around a Tier-3 event can have another.

The displayed percentage must be a sample-aware/shrunk estimate, never a raw small-sample win rate presented as certainty.

### 2.4 Internal conviction is not historical reliability

A gate can say:

- current internal conviction: 82% bearish;
- historically reliable in matching conditions: 67% with n=143;
- AIDY effective trust after sample/dependency/calibration adjustment: high.

These are separate concepts and must remain separate in storage and explanation.

### 2.5 Context-only experts must not invent direction

Volatility, session participation and data-quality experts are often better as trust/regime modifiers than BUY/SELL voters. UNKNOWN and ABSTAIN are valid first-class outputs.

### 2.6 Correlated evidence cannot be counted repeatedly

M15 trend, recent 15-minute momentum and M5 momentum may all describe the same price impulse. AIDY must learn/declare evidence families and reduce duplicated influence. Cross-family agreement is more meaningful than repeated copies of one movement.

---

## 3. Research findings that shape the blueprint

### 3.1 Gold has multiple driver families, and their relationships change

World Gold Council's Gold Return Attribution Model groups Gold drivers into economic expansion, risk/uncertainty, opportunity cost via FX/rates, and momentum. WGC also explicitly notes that driver relationships shift over time. This supports conditional gate reliability rather than permanent rules such as "real yields up means Gold down."

### 3.2 Gold intraday information is session- and news-dependent

Published intraday Gold research finds:
- New York futures play a large price-discovery role;
- London/New York overlap can be particularly informative;
- macro surprises alter Gold price discovery;
- surprise magnitude, asymmetry and state dependence matter;
- Gold futures have shown global leadership in price discovery/volatility spillover.

Therefore session, participation and event state belong in the environment rather than being cosmetic labels.

### 3.3 Intraday liquidity/volatility/volume have time-of-day structure

Gold-futures research shows intraday seasonality in efficiency, liquidity, volatility and volume across Tokyo/New York/global trading hours. Raw "high volume" or "high spread" is therefore less useful than **volume/spread relative to the expected weekday + clock-slot baseline**.

AIDY already has this idea in historical GC microstructure code and should reuse it.

### 3.4 Pattern/structure analysis should be systematic, not visual storytelling

Lo, Mamaysky and Wang formalised technical-pattern recognition to reduce subjective chart interpretation. The lesson for AIDY is not to copy classic chart patterns blindly, but to make swing, slope, persistence, breakout and rejection definitions deterministic and testable.

### 3.5 Momentum must be multi-horizon and regime-aware

Time-series momentum literature shows persistence can exist but depends strongly on horizon and can reverse at longer horizons. That literature is not proof of a 15-minute Gold edge. It supports building multi-horizon momentum measurements and forcing AIDY to validate their Gold-specific forward usefulness.

### 3.6 Jump/continuous volatility can be separated

Realized/bipower-variation literature provides a principled way to distinguish continuous volatility from jump-like movement. AIDY already has jump-vs-continuous research; this should become a formal volatility mini-brain rather than a simple high/low label.

### 3.7 Microstructure can contain incremental short-horizon information

Order-flow imbalance literature shows short-interval price changes can be related to supply/demand imbalance at the best bid/ask, though that evidence is not Gold-specific and must not be treated as proof of Gold edge.

AIDY is unusually well positioned here because it already contains historical COMEX GC Databento TBBO research: genuine trades, aggressor side when known, BBO spread, signed trade imbalance and anchored/session VWAP. This should be validated retrospectively before any paid live-feed decision.

---

## 4. What AIDY already has — reuse before buying/building

### 4.1 Live/PIT-capable foundation already present

Existing source modules include:

- `gold_cycle_environment.py`
- `gold_cycle_memory.py`
- `gold_marker_brain.py`
- `gold_state_engine.py`
- `feature_engine.py`
- `price_structure_v2.py`
- `regime_classifier.py`
- `setup_detector.py`
- `gold_movement_investigator.py`
- `gold_movement_memory.py`
- analogue retrieval v1/v2/v3 + semantic analogue retrieval
- evidence grading
- cross-market capture/as-of storage
- macro event intelligence
- macro vintages/rates decomposition
- volatility intelligence + richer volatility
- CME contract intelligence
- policy/cross-asset research
- historical GC microstructure
- D1/R2/BigQuery provenance/evidence infrastructure
- live Twelve Data XAUUSD OHLC capture with self-heal
- canonical 34-capability toolbox registry.

### 4.2 Existing price features that must be reused

AIDY already computes, by timeframe where available:

- 1-bar return
- 5-bar return/direction
- candle body
- range
- close location inside candle
- ATR(14)
- realized volatility
- recent 20-bar high/low
- distance to recent high/low
- 20-bar range position
- confirmed swing high/low.

### 4.3 Existing structure features that must be reused

Price Structure v2 already includes:

- prior-period levels;
- Asia overnight range;
- session extremes;
- 15/30/60-minute opening ranges;
- UTC-day gap;
- trend persistence/acceleration;
- prior-day breakout state;
- wick footprint;
- confirmed swing penetration and reversion;
- PIT/feed-health controls.

### 4.4 Existing macro/cross-asset stack

Already present:

- official event schedules;
- pre-event drift/range/compression;
- consensus/actual first-print contracts;
- surprise state/revisions;
- DGS2, DGS10, DFII10, T10YIE and CPI vintages;
- broad USD;
- nominal/real Treasury context;
- research contracts for ZQ, SR3, ZN, GC, SI, EURUSD, USDJPY, VIX and ES.

### 4.5 Existing futures microstructure research

Historical Databento GLBX.MDP3/GC code already supports:

- GC contract identity/roll provenance;
- trade count and volume;
- buy/sell aggressor volume;
- signed trade imbalance;
- BBO spread;
- VWAP;
- anchored/session VWAP;
- VWAP distance;
- weekday + 15-minute clock baselines.

This is retrospective research today, not a live PIT order-flow feed.

### 4.6 Tool procurement decision for the blueprint

**No new paid tool is required for Builds 1–16.**

Use the current stack first.

Potential future additions are conditional:

1. **Live CME/Databento microstructure** — only consider after historical GC microstructure proves independent out-of-sample incremental value.
2. **Live breaking-news/official-release search** — required only for the later News/Mechanism Expert if no existing approved source can satisfy PIT/source-provenance requirements.
3. Full-depth MBO/MBP-10 should not be purchased merely because it exists. The existing repo deliberately avoids expensive depth schemas during the free-first research phase.

The current Python dependency stack is intentionally small. Initial expert calculations such as slopes, R², efficiency ratios, beta-binomial shrinkage, rolling correlations and Brier scores can be implemented deterministically without introducing a heavyweight ML dependency. Add a dependency only if a later benchmark demonstrates a real need.

---

## 5. Global Gold environment taxonomy v1 target

The environment contract should preserve exact values for audit and also create repeatable categorical states for learning.

### 5.1 Time / participation

- UTC timestamp and weekday
- Gold-session-open/closed
- Asia / London / New York / London-New York overlap / transition
- minutes since relevant session open
- phase: opening / early / middle / late
- weekday-clock bucket
- pre-weekend/post-weekend state
- contract roll/settlement proximity where relevant.

### 5.2 Broad price/structure state

- trend / range / mixed / transition
- M5/M15/H1/H4/D1 alignment state
- slope family state
- trend quality
- persistence
- path efficiency/chop
- swing regime
- breakout / accepted breakout / rejected breakout / reclaim
- acceleration / deceleration
- range position.

### 5.3 Movement / momentum state

- 1/5/15/30/60-minute return where data supports it
- return percentile relative to appropriate baseline
- volatility-normalised momentum
- impulse vs drift
- acceleration/deceleration
- continuation vs exhaustion candidate
- abnormal-move state.

### 5.4 Volatility state

- realized volatility level and percentile
- ATR state
- range percentile
- compression / normal / expansion
- compression-to-expansion transition
- jump-dominant vs continuous
- vol-of-vol
- implied-volatility/GVZ state when PIT-qualified
- IV/RV relationship when qualified.

### 5.5 Liquidity / microstructure state

Two evidence classes must remain distinct:

**PIT/live OHLC proxy class**
- sweep/reclaim count
- side swept
- penetration depth
- reclaim speed
- hold/retest state
- range/opening-range breakout/rejection
- proxy intensity.

**Genuine exchange microstructure class**
- GC spread vs weekday/clock baseline
- trade volume vs weekday/clock baseline
- signed aggressor imbalance
- VWAP/anchored-VWAP distance
- active contract/roll state
- data-quality/unknown-side fraction.

Never relabel OHLC proxies as true order-book liquidity.

### 5.6 Price location / reference state

- prior-day high/low/close
- Asia range high/low
- active-session high/low
- session opening 15/30/60 range
- confirmed swing high/low
- recent multi-bar high/low
- round-number references
- nearest reference
- side of reference
- distance in bps and ATR units
- prior-day/session/range quartile
- session/anchored futures VWAP when genuine GC evidence is available.

### 5.7 Scheduled event / macro state

- event class
- event tier learned from Gold response history
- minutes before/after
- event cluster vs isolated event
- pre-event drift
- pre-event range
- pre-event volatility compression
- consensus availability
- actual/first print
- standardized surprise where mathematically valid
- revision state
- immediate post-event reaction state
- scheduled vs unscheduled.

### 5.8 Opportunity-cost / USD / rates state

- broad USD level/change regime
- nominal 2Y/10Y state/change
- real 10Y state/change
- breakeven/inflation-expectation state
- curve/policy-path state
- rolling Gold sensitivity to USD/rates
- divergence state when Gold and traditional drivers move together
- relationship stability/break state.

No permanent sign assumption is allowed.

### 5.9 Cross-asset / risk state

- Silver/precious-complex agreement/divergence
- ES risk-on/risk-off proxy when qualified
- VIX risk state when qualified
- EURUSD/USDJPY composition context
- intraday ZN/ZQ/SR3 reaction when qualified
- cross-asset breadth/agreement
- stale/partial coverage.

### 5.10 Futures/positioning state

- active GC contract
- days/time to roll/expiry milestones
- roll quality/continuity
- volume state
- open-interest state
- curve/spot-futures relationship where qualified
- settlement-window proximity
- historical COT/positioning only if a later PIT contract is explicitly added.

### 5.11 Information/data-quality state

- source freshness
- M1 completeness
- timeframe completeness
- gap/self-heal state
- quote freshness
- spread known/unknown
- cross-market coverage
- event coverage
- provenance class
- PIT eligibility
- available/unavailable tools.

This state modifies trust; it does not vote direction.

### 5.12 Episode / analogue state

- normal vs abnormal movement
- move magnitude percentile
- jump/continuous
- supported/plausible/unknown cause
- analogous episode count
- analogue similarity
- continuation/retrace distribution
- counterexample availability.

---

## 6. Expert-gate mini-brains

Every expert gets the global environment plus only the specialist state relevant to its task.

### 6.1 M5 Price Structure Expert

Mini-environment:
- M1/M5 microstructure of price path;
- current session phase;
- short-horizon volatility;
- nearest reference/location;
- M15 alignment.

Sub-calculators:
- multiple lookback return/slope;
- linear/log-price slope and R²;
- higher/lower-close persistence;
- path efficiency;
- confirmed swings;
- BOS/acceptance/reclaim;
- range position;
- candle body/wick/close location;
- ATR-normalised displacement;
- acceleration;
- compression/expansion;
- contradiction detector.

### 6.2 M15 Price Structure Expert

Mini-environment:
- M15 swing regime;
- H1 alignment;
- session/phase;
- range/reference location;
- volatility transition;
- liquidity/reclaim state.

Uses the same common mathematical family as M5 but longer horizons and M15-appropriate thresholds learned/frozen independently.

### 6.3 H1 Price Structure Expert

Mini-environment:
- H1 swing regime;
- H4/D1 alignment;
- session;
- broad volatility regime;
- prior-day/Asia/session location;
- breakout/rejection state;
- event proximity.

Primary goal: distinguish genuine H1 trend quality from noisy first-close/last-close direction.

### 6.4 H4 Price Structure Expert

Mini-environment:
- H4 swing/trend regime;
- D1 context;
- daily location;
- macro/rates regime;
- broad volatility;
- major-event state.

Expected role: slower structural context and contradiction, not automatically a strong next-15m vote.

### 6.5 D1 Context Expert

Mini-environment:
- daily/weekly structure when qualified;
- prior-day/week references;
- multi-day volatility;
- macro/rates/risk environment;
- futures positioning/roll context.

Expected role: slow context. Must prove that it adds value to the 15-minute target before being given meaningful directional weight.

### 6.6 Momentum / Impulse Expert

Mini-environment:
- multi-horizon returns;
- realized volatility;
- session/phase;
- price location;
- trend/range state.

Sub-calculators:
- 1/5/15/30/60m momentum;
- volatility-normalised momentum;
- acceleration;
- persistence;
- path efficiency;
- impulse vs drift;
- exhaustion/divergence;
- continuation/reversion conflict.

### 6.7 Price Location Expert

Mini-environment:
- all qualified reference levels;
- active session;
- volatility;
- breakout state.

Sub-calculators:
- distance to prior day/Asia/session/opening-range/swing/round levels;
- distance in bps and ATR units;
- range percentile/quartile;
- confluence density;
- accepted side vs rejected side;
- session/anchored VWAP later when exchange data is qualified.

Primarily context; may produce directional evidence only for explicitly tested reactions such as acceptance/rejection.

### 6.8 Liquidity / Reclaim Expert

Mini-environment:
- reference identity/type;
- session participation;
- volatility;
- sweep depth;
- reclaim/hold/retest state.

Sub-calculators:
- high/low sweep identity;
- penetration magnitude;
- reclaim speed;
- number of confirming closes;
- retest success/failure;
- wick/body geometry;
- competing nearby reference;
- proxy intensity.

Historical genuine GC microstructure can later augment but must remain labelled separately from OHLC proxies.

### 6.9 Volatility / Jump Expert

Mini-environment:
- clock/session baseline;
- event state;
- realized vol family;
- GVZ/IV state where qualified.

Sub-calculators:
- RV/ATR percentile;
- compression/expansion;
- range expansion;
- bipower/jump-style decomposition where supported;
- jump persistence;
- vol-of-vol;
- IV vs RV state.

Default output is regime/trust modifier, not forced direction.

### 6.10 Session / Participation Expert

Mini-environment:
- weekday/clock;
- session/overlap;
- expected volume/vol/spread baseline;
- event schedule.

Sub-calculators:
- session phase;
- deviation from normal volatility for that clock slot;
- deviation from normal volume/spread when genuine GC data available;
- session handoff;
- London/NY overlap;
- DST-safe timing.

Default output is participation/information-quality state, not forced direction.

### 6.11 Macro / Event Expert

Mini-environment:
- event class/tier;
- minutes before/after;
- pre-event drift/compression;
- consensus/actual/surprise;
- rates/USD reaction;
- session.

Sub-calculators:
- Gold-specific event impact history;
- surprise magnitude;
- direction of first print vs consensus;
- immediate market confirmation/rejection;
- pre-event compression;
- event cluster;
- scheduled/unscheduled.

Pre-event direction must not use the future actual. Post-event states may use the actual only after its first-observed timestamp.

### 6.12 Rates / USD / Cross-Asset Expert

Mini-environment:
- Gold volatility/structure;
- session;
- event state;
- current driver-relationship regime.

Sub-calculators:
- USD movement;
- nominal/real yield changes;
- breakeven changes;
- policy-path proxies;
- silver;
- risk assets;
- rolling beta/correlation;
- agreement/divergence;
- structural-break/relationship-instability flag.

No permanent "USD up = Gold down" or "real yield up = Gold down" rule.

### 6.13 Futures / Microstructure Expert

Mini-environment:
- active GC contract;
- session/clock;
- roll proximity;
- event state;
- Gold spot path.

Historical sub-calculators already available:
- signed aggressor imbalance;
- trade volume;
- spread;
- anchored/session VWAP;
- VWAP distance;
- clock-normalised anomalies.

Add:
- contract volume/OI/roll state;
- futures/spot dislocation if PIT-qualified.

Starts retrospective/shadow. Paid live data only after independent value is demonstrated.

### 6.14 News / Mechanism Expert

Mini-environment:
- abnormal move state;
- scheduled-event context;
- session;
- source recency/authority.

Sub-calculators:
- official release match;
- breaking-news match;
- source agreement;
- timestamp proximity;
- causal confidence class.

Output can be supported / plausible / unknown. Never force a narrative.

### 6.15 Analogue / Episode Memory Expert

Mini-environment:
- global environment;
- gate states;
- movement class;
- event class.

Sub-calculators:
- nearest historical analogues;
- similarity components;
- continuation/retrace distribution;
- symmetric counterexamples;
- sample diversity.

No duplicated episodes and no future-derived similarity fields.

### 6.16 Data Quality / Availability Meta-Gate

Mini-environment:
- source freshness/completeness only.

Outputs:
- which experts are qualified;
- which must be downweighted;
- which must be UNKNOWN;
- whether cycle can be scored.

Never directional.

---

## 7. Scoring/trust model target

For every scoreable gate/sub-calculator store at minimum:

- gate_id / subcalculator_id / version;
- target horizon;
- global environment scope;
- mini-environment scope;
- vote/conclusion;
- outcome;
- +2/+1/0/-1/-2 score;
- correct/incorrect/neutral;
- sample N;
- net score;
- mean score;
- raw accuracy;
- shrunk/partial-pooled reliability;
- calibration statistics when probabilities exist;
- first/last observation;
- recent-vs-long-term split;
- environment similarity/backoff level;
- dependency family.

### 7.1 Small samples

Do not rank gates by raw percentage alone.

A result of 8/10 must not automatically outrank 137/200.

Use partial pooling / beta-binomial-style shrinkage or an equivalently auditable deterministic approach:
- small environment cells borrow strongly from the gate/family prior;
- large cells increasingly own their estimate;
- report N beside every percentage.

### 7.2 Backoff hierarchy

Example H1 trust lookup:

1. exact H1 mini-environment if N sufficient;
2. H1 structure + session + volatility;
3. H1 structure + session;
4. H1 structure family;
5. H1 global;
6. neutral prior.

The exact hierarchy is frozen by build and versioned.

### 7.3 Recency

Keep all history, but allow a bounded recency component to detect regime drift. Never allow one recent run to erase a large historical sample. Store long-term and recent views separately before combining.

### 7.4 Calibration

If gates expose probabilities/conviction:
- reliability/calibration curves;
- Brier score;
- over/under-confidence;
- enough observations per bin before claims.

### 7.5 Dependency penalty

Each sub-calculator belongs to an evidence family:
- price trend;
- price momentum;
- location;
- liquidity;
- volatility;
- event;
- rates/USD;
- futures flow;
- analogue.

Highly overlapping signals receive reduced aggregate influence. Independent cross-family confirmation earns more influence than duplicated price-path evidence.

---

# 8. Sequential implementation programme

## Build 1 — Environment Contract v3

**Objective:** freeze the complete factorised global environment before any gate reasons.

Reuse:
- `gold_cycle_environment.py`
- `market_sessions.py`
- `regime_classifier.py`
- `gold_state_engine.py`.

Add:
- canonical dimension registry;
- exact value + categorical bucket side by side;
- environment digest;
- availability/unknown semantics;
- hierarchical environment scopes;
- explicit distinction between global environment and gate mini-environments.

**Tests / acceptance**
- deterministic same-input same-digest test;
- no future field adversarial test;
- session/DST boundary tests;
- every bucket edge test;
- stale/missing source tests;
- closed-market handling;
- exact facts preserved for audit;
- no monolithic cross-product key;
- every live cycle emits all mandatory global dimensions or explicit UNKNOWN.

**Do not proceed until:** historical replay and a fresh forward shadow cycle produce identical environment classifications from identical PIT inputs.

---

## Build 2 — Expert Gate Contract v1

**Objective:** standard interface for every mini-brain.

Gate packet fields:
- gate/version;
- as-of time;
- global environment digest;
- mini-environment + digest;
- evidence inputs/references;
- sub-calculator outputs;
- direction or context-only/ABSTAIN/UNKNOWN;
- internal conviction;
- contradictions;
- readable explanation;
- scoreability;
- dependency family;
- no-hindsight attestation.

**Tests / acceptance**
- schema/digest verification;
- missing data => UNKNOWN, never fabricated direction;
- context-only experts cannot accidentally become directional;
- evidence reference integrity;
- every explanation traceable to a numeric/categorical input;
- mutation/future-field adversarial test.

---

## Build 3 — Conditional Trust & Score Engine v3

**Objective:** make every gate/sub-calculator have different trust under different environments.

Reuse existing contextual marker tables/logic where sound; version rather than rewrite history.

Add:
- gate-level and sub-calculator scorebooks;
- +2/+1/0/-1/-2 outcomes;
- sample-aware shrinkage;
- hierarchical backoff;
- long-term vs bounded recent stats;
- confidence intervals/uncertainty state where practical;
- score lookup before current decision.

**Tests / acceptance**
- 8/10 does not automatically dominate 137/200;
- exact context wins only when minimum evidence met;
- correct fallback order;
- no current/future outcome can enter lookup;
- idempotent outcome resolution;
- large correct/wrong move gives +/-2;
- normal gives +/-1;
- unavailable/unscoreable gives 0;
- score math deterministic.

---

## Build 4 — Common Price Expert Mathematics

**Objective:** replace "last close versus first close" as the sole structure logic with reusable, deterministic primitives.

Add:
- multi-lookback returns;
- OLS/log-price slope;
- R²/trend quality;
- close-step persistence;
- path efficiency = net displacement / total path;
- ATR/RV normalisation;
- acceleration/deceleration;
- confirmed swing sequences;
- structure break;
- acceptance/hold/retest/reclaim;
- range position;
- wick/body/close geometry;
- contradiction flags.

Reuse existing feature/price-structure functions where already correct.

**Tests / acceptance**
- synthetic clean uptrend/downtrend/range/chop/reversal/breakout/rejection fixtures;
- exact expected outputs;
- flat/noisy paths do not masquerade as strong trends;
- partial bars excluded;
- no look-ahead swing confirmation;
- no duplicate feature counting.

---

## Build 5 — M5 Price Structure Expert

**Status: COMPLETE / ENGINEERING PROVEN — AIDY merge `eaa6f49636ae4ae9f73d6a17db4c9d8f46d8743a`; 148 focused / 1400 full tests.**

Use Build 4 primitives with M5-specific lookbacks and mini-environment.

**Acceptance**
- expert explains every sub-vote;
- synthetic and PIT historical tests;
- chronological replay;
- compare against legacy M5 rule;
- must not gain weight merely by being more complex.

---

## Build 6 — M15 Price Structure Expert

**Status: COMPLETE / ENGINEERING PROVEN — AIDY PR #209, 159 focused / 1411 full tests.**

Same contract, independently calibrated M15 horizons/thresholds.

**Acceptance**
- M15 8-bar path, latest 15m momentum and swing/breakout features are separately identified;
- correlation/dependency metadata present;
- legacy M15 baseline retained for ablation.

---

## Build 7 — H1 Price Structure Expert

**Status: COMPLETE / ENGINEERING PROVEN — AIDY PR #210, 172 focused / 1424 full tests.**

Focus on genuine hourly trend quality, swing structure, acceleration and breakout acceptance.

**Acceptance**
- an H1 path with positive first-to-last return but poor persistence/choppy structure cannot be labelled "strong bullish";
- H1 explanations include slope, quality, swings, location and contradictions;
- historical conditional scorebook begins separately from M15.

---

## Build 8 — H4 Price Structure Expert

**Status: COMPLETE / ENGINEERING PROVEN — AIDY PR #211, 187 focused / 1439 full tests.**

Slow structural expert.

**Acceptance**
- H4 cannot dominate next-15m forecast merely due to timeframe;
- it must prove incremental conditional value;
- conflict with lower timeframes is explicit and scoreable.

---

## Build 9 — D1 Context Expert

**Status: COMPLETE / ENGINEERING PROVEN — AIDY PR #212, 199 focused / 1451 full tests.**

Slowest structural/macro-location context.

**Acceptance**
- abstains when D1 evidence is stale/partial;
- no forced 15m direction;
- historical tests must distinguish context value from direct forecast value.

---

## Build 10 — Momentum / Impulse Expert

**Status: COMPLETE / ENGINEERING PROVEN — AIDY PR #213, 211 focused / 1463 full tests.**

**Objective:** distinguish continuation-quality momentum from noisy direction.

Features:
- 1/5/15/30/60m returns;
- vol-normalised return;
- acceleration;
- persistence;
- path efficiency;
- impulse/drift;
- exhaustion;
- multi-horizon agreement.

**Acceptance**
- one large candle does not automatically equal persistent momentum;
- regime/clock normalisation tested;
- correlated price-expert influence tagged for later penalty.

---

## Build 11 — Price Location Expert

**Status: COMPLETE / ENGINEERING PROVEN — AIDY PR #214, 223 focused / 1475 full tests.**

**Objective:** know where Gold is, not merely where it is moving.

Use:
- prior day;
- Asia;
- active session;
- opening ranges;
- swings;
- recent extrema;
- round numbers;
- ATR-normalised distance.

**Acceptance**
- exact nearest-level calculations;
- reference priority auditable;
- conflicting/confluent levels represented;
- no directional vote unless a separately tested location-reaction rule exists.

---

## Build 12 — Liquidity / Reclaim Expert

**Status: COMPLETE / ENGINEERING PROVEN — AIDY PR #215, 235 focused / 1487 full tests.**

**Objective:** make sweep/reclaim reasoning measurable and multi-step.

Add:
- level identity;
- penetration depth;
- reclaim speed;
- confirmation closes;
- retest;
- rejection geometry;
- competing-level distance;
- session/volatility context.

**Acceptance**
- OHLC sweep proxy explicitly remains proxy;
- fake "order flow" language forbidden;
- synthetic sweep/no-sweep/reclaim/failure tests;
- retrospective genuine GC flow is stored separately.

---

## Build 13 — Volatility / Jump Expert

**Status: COMPLETE / ENGINEERING PROVEN — AIDY PR #216, 249 focused / 1501 full tests.**

**Objective:** classify movement conditions that change the usefulness of other gates.

Use current RV/ATR/GVZ/jump work.

Add:
- clock-normalised vol percentile;
- compression/expansion transition;
- continuous vs jump state;
- vol-of-vol;
- optional IV/RV relation when qualified.

**Acceptance**
- no forced direction;
- event-driven jump distinguishable from normal expansion when evidence allows;
- sparse GVZ/IV remains UNKNOWN;
- compare simple ATR band vs richer regime in ablation.

---

## Build 14 — Session / Participation Expert

**Status: COMPLETE / ENGINEERING PROVEN — AIDY PR #217, 263 focused / 1515 full tests.**

**Objective:** quantify who is likely active and whether current activity is unusual for this time.

Use:
- DST-safe sessions;
- session phase;
- overlap;
- weekday-clock volatility/range baselines;
- historical GC volume/spread baselines where available.

**Acceptance**
- DST transitions;
- clock-slot baseline tests;
- event-time confounding explicitly represented;
- no hardcoded "London bullish" style rule.

---

## Build 15 — Macro / Event Expert

**Status: COMPLETE / ENGINEERING PROVEN — AIDY PR #218, 276 focused / 1528 full tests.**

**Objective:** turn the existing event stack into a Gold-specific specialist.

Use:
- official BLS/BEA/Fed/global CB schedules;
- event classes;
- pre-event features;
- consensus/actual/revisions;
- Gold-learned event tiers.

Add:
- standardized surprise where valid;
- event clustering;
- post-release confirmation state;
- historical conditional response score.

**Acceptance**
- pre-event gate cannot see actual;
- actual enters only after first-observed timestamp;
- revisions separated from first print;
- event tier based on independent Gold episodes, not vendor importance labels;
- no-news period provides control sample.

---

## Build 16 — Rates / USD / Cross-Asset Expert

**Status: COMPLETE / ENGINEERING PROVEN — AIDY PR #219, 292 focused / 1544 full tests.**

**Objective:** model Gold's opportunity-cost/risk mechanisms without permanent sign assumptions.

Use:
- broad USD;
- DGS2/DGS10/DFII10/T10YIE;
- policy-path research;
- SI/ES/VIX/EURUSD/USDJPY when qualified.

Add:
- changes over multiple horizons;
- rolling Gold beta/correlation;
- relationship-stability state;
- divergence state;
- cross-asset breadth/agreement.

**Acceptance**
- historical regime where Gold rose with real rates/USD must be representable;
- stale daily series cannot masquerade as intraday reaction;
- same-mechanism series are dependency-tagged;
- no hardcoded forever-sign.

---

## Build 17 — Futures / Microstructure Expert

**Objective:** test whether genuine COMEX information adds independent predictive value.

Phase A:
- use existing historical Databento GC TBBO;
- signed aggressor imbalance;
- BBO spread;
- trade volume;
- anchored/session VWAP;
- clock-normalised baselines;
- contract/roll state;
- CME volume/OI where available.

Phase B only if Phase A passes:
- price/entitlement review for live/delayed GC data;
- owner approval before recurring paid data;
- PIT contract before any live use.

**Acceptance**
- retrospective holdout shows incremental value beyond spot OHLC experts;
- order-flow feature definitions match actual data entitlement;
- no depth claim without depth data;
- no paid activation solely to improve feature count.

**Completion — 2026-09-21:** PASS. Genuine Phase-A evidence used 61 valid weekly episodes with 20 normalization, 10 development, 1 embargo and 30 untouched holdout episodes. The development-only rule `override_1p5_0p5` improved holdout accuracy from 20.0000% spot-only to 23.3333% spot+microstructure (+3.3333pp). Research-only boundaries remain: statistically validated=false, formal-forward evidence=false, paid/live feed=false, depth claim=false, live weight=false, live-money authority=false.

---

## Build 18 — News / Movement Mechanism Expert

**Objective:** explain abnormal moves without inventing causality.

Use current movement investigator and scheduled event evidence.

Add only when source contract exists:
- official/breaking-news search;
- source authority/timestamp;
- duplicate story collapse;
- evidence agreement.

**Acceptance**
- scheduled event, credible news, unsupported narrative and UNKNOWN fixtures;
- disagreement remains unresolved rather than fabricated;
- news context does not automatically become direction.

If live source is not available, this build may remain BUILT with the live branch explicitly UNKNOWN.

**Completion — 2026-09-21:** PASS. Finnhub market-news adapter/source contract added; scheduled-event, credible-news, unsupported-narrative, UNKNOWN, disagreement, agreement, duplicate-collapse, future-news exclusion and no-direction fixtures all pass. Semantic gate PASS, 61 focused tests and 1577 full regression tests. Optional real Finnhub smoke was not run in GitHub because the existing key is on Render rather than AIDY GitHub secrets; this was not an acceptance requirement.

---

## Build 19 — Analogue / Episode Expert

**Objective:** retrieve comparable historical states without hindsight.

Use:
- movement episode memory;
- analogue retrieval v1/v2/v3;
- semantic analogue work.

Add:
- gate-state similarity components;
- environment similarity;
- symmetric counterexamples;
- continuation/retrace distributions.

**Acceptance**
- no outcome field in similarity vector;
- duplicate episodes collapsed;
- exact PIT reconstruction;
- positive and counterexample retrieval;
- chronological holdout only.

---

## Build 20 — Evidence Dependency & Double-Counting Engine

**Objective:** stop the same underlying Gold move from voting five times.

Implement:
- evidence-family graph;
- declared parent/child relationships;
- rolling correlation/dependency diagnostics;
- duplicated-signal cap;
- independent-family bonus only when justified.

**Acceptance**
- exact duplicate signals do not double weight;
- highly correlated M5/M15/momentum inputs are damped;
- independent liquidity + macro + structure agreement remains distinct;
- removing one duplicate does not radically change final score.

---

## Build 21 — Environment-Aware Gate Selector

**Objective:** AIDY knows the environment first and then knows which gates historically deserve attention there.

For every available gate:
- retrieve matching-context trust;
- apply sample shrinkage;
- apply similarity/backoff;
- apply calibration adjustment;
- apply recency drift state;
- apply dependency penalty;
- preserve low-weight observation for continued learning.

Outputs:
- selected/high-trust gates;
- reduced-trust gates;
- unavailable gates;
- exact reason for current trust;
- trust score + N + context label.

**Acceptance**
- selector cannot see current outcome;
- small-N star performers are suppressed;
- strong large-N contextual performers rise;
- unavailable gate gets zero authority;
- weak gate remains observable/scoreable;
- deterministic replay.

---

## Build 22 — AIDY Meta Direction Aggregator & Explanation

**Objective:** combine expert evidence into one final 15-minute research view.

Output:
- bullish/bearish/neutral/abstain;
- calibrated confidence only if enough evidence;
- supporting gates;
- contradictions;
- environment;
- gate trust/N;
- dependency adjustment;
- readable "why".

**Acceptance**
- no magic percentage;
- every contribution traceable;
- strong contradiction can reduce confidence;
- context-only gates modify trust without forced votes;
- abstain works;
- future values = false;
- live-money authority = false.

---

## Build 23 — Chronological Replay, Ablation & Untouched Holdout

**Objective:** prove the expert system beats complexity for a reason.

Compare:
- legacy simple 15m gate system;
- each new gate alone;
- full system;
- full system minus each gate;
- full system with/without dependency penalty.

Metrics:
- directional accuracy by class;
- +2/+1/-1/-2 score;
- calibration/Brier where probabilities exist;
- coverage/abstention;
- performance by environment;
- stability across time;
- incremental contribution;
- sample N.

Design:
- chronological development window;
- validation window;
- untouched final holdout;
- no threshold tuning on holdout.

**Acceptance**
- complexity that adds no out-of-sample value is pruned or downweighted;
- no gate promoted from in-sample beauty;
- results reproducible from versioned PIT inputs.

---

## Build 24 — Live Forward Shadow Soak & Permanent Scorecard

**Objective:** prove the entire system prospectively.

Every fresh cycle stores:
- environment;
- all gate packets;
- sub-calculator outputs;
- pre-outcome trust;
- final AIDY view;
- outcome later;
- score updates.

Permanent scorecard exposes:
- gate + mini-environment;
- sample N;
- raw and shrunk reliability;
- net score;
- calibration;
- current trust;
- drift;
- dependency family;
- last score time.

**Acceptance**
- continuous fresh cycles;
- no hindsight;
- all expected gates either present or explicit UNKNOWN;
- scores update after resolution only;
- exact environment-specific history inspectable;
- fresh live examples prove different gate weights under different environments;
- formal-forward/live-money authority remains OFF.

Only after a separate future owner decision would any decision class be considered for live authority. This blueprint does not authorize that step.

---

## 9. Build execution discipline

For every future build:

1. Re-read Memory and authoritative AIDY source/runtime.
2. Create one bounded branch/PR.
3. Add unit tests before/with implementation.
4. Run lint + compile + focused tests.
5. Run full relevant regression suite.
6. Run PIT/no-hindsight adversarial tests.
7. Run historical replay specific to the gate.
8. Deploy only when that build requires live shadow evidence.
9. Pull live evidence after deploy.
10. Record BUILD/ENGINEERING PROVEN/PRODUCTION VERIFIED accurately.
11. Update Memory handover before calling the build complete.
12. Then and only then begin the next numbered build.

No multiple expert gates should be implemented in one opaque mega-change.

---

## 10. Research sources retained for future implementers

Primary/reference research informing this plan:

- World Gold Council, Gold Return Attribution Model and 2026 outlook: economic expansion, risk/uncertainty, opportunity cost and momentum; relationships can shift over time.
  - https://www.gold.org/goldhub/tools/gold-return-attribution-model
  - https://www.gold.org/goldhub/research/gold-mid-year-outlook-2026
- World Gold Council, regime-dependent Gold/rates/cross-asset relationships:
  - https://www.gold.org/goldhub/research/gold-market-commentary-january-2025
  - https://www.gold.org/goldhub/research/gold-most-effective-commodity-investment-2026-edition
- Sobti, Sehgal & Ilango (2021), macro surprises and round-the-clock Gold price discovery:
  - https://doi.org/10.1016/j.irfa.2021.101893
- Sehgal (2021), spot/futures/ETF intraday Gold price discovery:
  - https://doi.org/10.1002/fut.22208
- Hauptfleisch et al. (2016), London vs New York Gold price discovery:
  - https://doi.org/10.1002/fut.21775
- Iwatsubo, Watkins & Xu (2018), Gold-futures intraday seasonality in efficiency/liquidity/volatility/volume:
  - https://doi.org/10.1016/j.jcomm.2018.05.001
- Lo, Mamaysky & Wang (2000), systematic technical pattern recognition:
  - https://www.nber.org/papers/w7613
- Moskowitz, Ooi & Pedersen (2012), time-series momentum across futures:
  - https://doi.org/10.1016/j.jfineco.2011.11.003
- Barndorff-Nielsen & Shephard (2004), realized/bipower variation and jumps:
  - https://doi.org/10.1093/jjfinec/nbh001
- Cont, Kukanov & Stoikov (2014), order-flow imbalance and short-horizon price impact; methodological evidence, not Gold-specific proof:
  - https://doi.org/10.1093/jjfinec/nbt003
- CME Group Gold/Precious Metals official product and volume/open-interest sources:
  - https://www.cmegroup.com/markets/metals/precious.html
  - https://www.cmegroup.com/markets/metals/precious/gold.volume.html
- Official event schedules:
  - https://www.bls.gov/schedule/
  - https://www.bea.gov/news/schedule
  - https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm

## 11. Final architectural target

AIDY should eventually be able to say, before a 15-minute Gold window:

> I know the current Gold environment.  
> I know what each expert sees.  
> I know why each expert reached its conclusion.  
> I know how reliable each expert and its sub-calculators have historically been in comparable conditions.  
> I know which experts are redundant with each other.  
> I know which experts are strongest here, with sample-aware confidence.  
> I can combine them without hindsight, explain the result, abstain when evidence is weak, and learn from what happens next.

That is the target. The current simple timeframe votes remain a **legacy baseline** until the expert-gate programme proves superior out of sample.
