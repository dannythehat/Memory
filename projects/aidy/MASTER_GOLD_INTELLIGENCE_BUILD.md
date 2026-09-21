# AIDY — Master Gold Intelligence Build

Approved: 2026-09-19

## Build status — 2026-09-19

- **Phase 0/1 anti-drift/evidence grounding:** PRODUCTION VERIFIED engineering; forward
  acceptance WAITING for the next eligible market signals. Exact Super Signals production
  SHA `33305a020f96e545990906a6de0c5dc253e9fcaf`, deploy `dep-dan2cv5ii2qc73bhmpig`, migration
  `0104_aidy_grounding_health`; 1105 API tests passed.
- **Phase 2 Gold-state bridge:** Gold State Engine v1 is built on isolated branches
  (AIDY PR #137; Super Signals PR #208) but is deliberately **not graduated or deployed**
  beyond the already-live backward-compatible intake seam. It contains PIT multi-timeframe
  structure, session/location/liquidity proxies, volatility/range state, scheduled-event
  context, abnormal-move observation and explicit cause-UNKNOWN semantics. Do not merge the
  reasoning consumer or graduate Phase 2 until fresh evidence-v2 decisions prove Phase 1
  acceptance.
- **Live-money authority:** OFF. **Owner live-risk directive:** unchanged at 1%.

## Objective

Build AIDY into a point-in-time, self-evaluating Gold specialist that understands the market independently, uses provider calls as one source of human alpha, explains what it knows and does not know, and proves whether each intervention improves money made or money saved.

The strategic KPI is not raw win rate. It is risk-adjusted realised/counterfactual value: money made, money saved, tail losses avoided, opportunity cost controlled and calibration improved.

## Non-negotiable architecture boundary

- Aidy-Gold-Signals remains the standalone Gold market/research brain.
- super-signals remains provider capture, broker/account execution and the user application.
- Cross-project exchange uses explicit versioned, immutable, PIT-safe contracts only.
- AIDY never reads broker/follower state as market truth and never holds broker credentials.
- Super Signals never silently promotes research evidence into execution authority.
- Existing 1% live risk stays unchanged unless the owner explicitly changes it.
- Missing or stale evidence resolves to UNKNOWN, not fabricated certainty.

## Phase 0 — architecture freeze and evidence contracts

Build:
- versioned Gold-state evidence contract;
- provider-state evidence contract;
- decision evidence contract;
- outcome/failure-attribution contract;
- exact timestamps, provenance, digests, qualification state and stale/missing semantics.

Tests:
- schema/version compatibility;
- deterministic hashing;
- stale/missing fail-to-UNKNOWN;
- no future timestamp accepted;
- no direct execution dependency;
- cross-repo contract fixtures.

## Phase 1 — evidence-grounded reasoning

Every factual statement in an AIDY decision must be addressable to the evidence packet available at that exact decision time.

Build:
- structured claim ledger per decision;
- source field, value, sample N, profile/snapshot version and timestamp per claim;
- contrary-evidence field;
- unsupported-claim detector;
- prompt/schema prohibition on unsupported provider-specific claims.

First regression target: the observed Scalping decision that claimed BUY weakness / Asia preference even though the exact PIT provider profile contained neither fact.

Tests:
- missing-side/missing-session adversarial fixtures;
- property test: no provider claim without supporting evidence;
- replay legacy final-gate rows and flag unsupported claims;
- zero unsupported claims for all new forward rows.

## Phase 2 — unified Gold state dossier

Expose qualified or explicitly research-labelled AIDY Gold Signals features to signal-level reasoning without rebuilding them inside Super Signals.

Inputs:
- genuine XAUUSD multi-timeframe OHLC/structure;
- nominal yields, real yields, breakevens and curve state;
- USD/broad-dollar state and qualified composition evidence;
- policy-path expectations where qualified;
- volatility regime, IV/RV/jump/instability evidence;
- qualified cross-asset mechanisms such as Treasuries, silver/gold-silver and risk state;
- scheduled macro/event map;
- session, liquidity and execution-state features.

Tests:
- exact-as-of joins;
- future-row exclusion;
- stale-source handling;
- provenance/digest verification;
- deterministic reconstruction at historical decision timestamps;
- qualification-state propagation.

## Phase 3 — breaking-news and event intelligence

Scheduled calendar support is not enough. Build a real-time news/event brain using the owner-provided news source plus authoritative official feeds where available.

Each item stores:
- first-observed timestamp;
- source and reliability;
- deduplication cluster;
- mechanism labels: rates, inflation, growth, USD, policy, geopolitical risk, fiscal/credibility, liquidity;
- novelty and Gold relevance;
- whether Gold, USD and yields later confirmed or contradicted the hypothesised mechanism.

News is context, never an automatic BUY/SELL command. AIDY may output cause_unknown.

Tests:
- duplicate/headline burst suppression;
- PIT enforcement;
- source disagreement;
- false-causal-narrative adversarial cases;
- scheduled release surprise tests where qualified actual/forecast/previous/revision data exists;
- forward ablation: with-news versus without-news decision quality.

## Phase 4 — liquidity and execution intelligence

Build the execution-quality model needed to understand when liquidity and timing are the real reason a trade works or fails.

Study:
- Asia, London, New York and overlaps;
- spread, slippage and quote freshness;
- signal age;
- distance from provider entry at receipt/decision/execution;
- opening ranges and prior-session highs/lows;
- volatility expansion/compression;
- stop-run/displacement candidates using measurable price/volume/liquidity evidence;
- MFE/MAE and price path after entry;
- stale-entry and chase-risk classification.

Never claim hidden order flow when the data does not provide it; label proxies explicitly.

Tests:
- session-boundary and DST fixtures;
- stale-entry fixtures;
- spread/slippage stress;
- latency buckets;
- MFE/MAE reconstruction;
- execution-quality counterfactuals.

## Phase 5 — provider alpha decomposition

Replace 'is this provider good?' with conditional expected value.

For every provider learn:
- BUY versus SELL;
- session and weekday;
- first versus second/layered entry;
- re-entry;
- exact versus zone entry;
- raw call versus provider management;
- BE/SL/partial/close behaviour;
- runner performance;
- news/event windows;
- volatility/regime;
- entry lateness;
- MFE/MAE, tail loss and recovery;
- behavioural drift.

Minimum-N and uncertainty are mandatory. UNKNOWN is valid.

Tests:
- cohort leakage protection;
- minimum-N gates;
- Simpson's-paradox checks;
- drift detection;
- exact PIT provider-profile reconstruction;
- raw-signal scorer versus lifecycle-aware scorer comparison.

## Phase 6 — analogue and setup memory

Historical matching must compare distributions, not cherry-pick visually similar examples.

Build:
- regime-matched retrieval;
- independent-episode grouping;
- transparent similarity components;
- symmetric support and counterexamples;
- outcome distributions for MFE, MAE, TP progression, stop probability and duration;
- explicit retrieval coverage/uncertainty.

Reuse existing Aidy-Gold-Signals analogue, evidence-grading and research-governance machinery.

Tests:
- no future analogue;
- duplicate episode collapse;
- neighbour stability;
- counterexample inclusion;
- chronological holdout;
- ablation versus no-analogue baseline.

## Phase 7 — calibrated probability and expected-value engine

Move from prose-first TAKE/REDUCE/HOLD/REJECT to measurable probabilities and EV.

Target outputs where supported:
- P(stop);
- P(TP1+), P(TP2+), P(runner outcome);
- expected R and expected cash delta;
- downside/tail estimate;
- evidence confidence and calibration state;
- TAKE / REDUCE / HOLD / REJECT / NO-TRADE;
- reason codes with evidence references.

No probability is trusted because the model emitted it.

Tests:
- Brier score and log loss;
- calibration curves;
- expected versus realised R;
- confidence-bucket reliability;
- class-specific counterfactual delta;
- REDUCE versus full-take opportunity cost;
- abstention value.

## Phase 8 — trade management and profit extraction

AIDY must optimise realised value, not only entry choice.

Shadow-test:
- provider close versus continue;
- fixed TP versus adaptive partials;
- break-even timing;
- stop tightening;
- TP1/TP2/TP3/runners;
- MFE capture;
- giveback from peak;
- regime/session/event-aware management.

Every alternative uses a frozen baseline and path-safe replay. Future maxima may never justify an earlier decision.

Tests:
- intrabar/path-order ambiguity;
- early-close counterfactual;
- BE counterfactual;
- runner giveback;
- management decision delta;
- provider/regime management calibration.

## Phase 9 — failure attribution and unknowns engine

After each resolved trade/event classify only what the evidence supports:
- bad direction;
- bad entry;
- poor timing;
- stop geometry;
- stale/chased execution;
- provider management;
- regime transition;
- scheduled/breaking event;
- liquidity/spread/slippage;
- valid positive-EV loss;
- unknown.

The original ex-ante thesis remains immutable.

Tests:
- outcome-blind ex-ante freeze;
- post-outcome explanation consistency;
- UNKNOWN required when causal evidence is insufficient;
- cause-confidence calibration;
- no narrative mutation of original decision.

## Phase 10 — self-critique, ablation and continuous learning

For every feature, reason and action measure:
- forward decision delta;
- calibration;
- hit/miss rate;
- opportunity cost;
- performance by provider/regime/session;
- with-feature versus without-feature ablation;
- drift.

Features that do not add incremental forward value are demoted or removed. Complexity does not earn permanent status.

## Graduation gate

No decision class gets live authority until all are true:
1. engineering proven;
2. production shadow verified;
3. PIT/no-hindsight audit clean;
4. unsupported-claim rate = 0 on the graduated surface;
5. sufficient prospective sample;
6. positive counterfactual decision delta with uncertainty reported;
7. probability calibration acceptable where probabilities are used;
8. stress/adversarial tests pass;
9. kill switch and rollback proven;
10. owner explicitly authorizes that exact live-money class.

## Weekend acceleration strategy — historical time machine

Approved 2026-09-19 by the owner.

Do not waste the market-closed weekend waiting for fresh Gold signals. Use stored historical
evidence to sharpen AIDY through strict as-of replay, while keeping fresh forward data as the
final graduation check.

The replay programme must behave like a time machine:

- choose a historical signal timestamp T;
- reconstruct only evidence genuinely available at or before T;
- freeze AIDY's decision before loading any post-T outcome;
- reveal the future path/outcome only after the decision is immutable;
- score AIDY versus the frozen baseline and persist both;
- never tune on the final untouched holdout period.

Chronological partitions are mandatory:

1. development history — may be used to design/repair features;
2. validation history — may be used to select between registered alternatives;
3. untouched holdout history — may only be opened for a formal examination after the
   implementation is frozen.

The replay harness is the reusable test bed for Phases 2-10. It must preserve provider-profile
versions, message ordering, market-data provenance, feed epoch, context timestamps and
outcome-availability timestamps. HistData-era and Twelve-era evidence must remain distinguishable;
blocked/amber feature surfaces must not silently cross feed epochs.

Weekend build blocks:

1. historical time-machine + replay qualification harness;
2. news/event + liquidity/execution replay;
3. provider conditional-alpha + analogue replay;
4. probability/EV + trade-management replay;
5. failure attribution + AIDY self-critique/ablation.

Historical performance can qualify engineering/research value but cannot by itself grant
live-money authority. Fresh prospective forward evidence remains required before any class is
graduated.

## Build order

Build in this sequence: 0 -> 1 -> 2 -> 3/4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10. News and liquidity can proceed in parallel only after evidence contracts and claim-grounding are in place. Live-money authority does not move during this build.


## Owner correction — Gold-first causal learning architecture (2026-09-20)

This is now the primary design rule for AIDY.

**AIDY is a Gold intelligence system first and a provider filter second.**

The core learning loop is not merely provider-signal -> accept/reduce/reject -> outcome. It is:

`Gold movement -> detect abnormality -> investigate cause -> explain the market mechanism -> observe continuation/reversal -> store a structured lesson -> retrieve comparable episodes -> form an independent Gold view -> then compare that view with provider signals.`

Required behaviour:

1. Detect meaningful Gold movement continuously, including spikes, jump-dominant candles, abnormal range expansion, volume/spread anomalies and cross-asset reaction.
2. Trigger an investigation automatically when movement is unusual. Do not rely on a model deciding whether to look.
3. Inspect all qualified evidence available at that time: multi-timeframe Gold candles/structure, scheduled and breaking macro/event evidence, forecast-vs-actual surprise where point-in-time valid, USD/cross-market/rates/yields, CME state, volatility/GVZ, liquidity/session/spread/execution state and recent provider context where relevant.
4. Distinguish **known cause**, **supported mechanism**, **plausible but unconfirmed explanation**, and **cause_unknown**. Never invent a headline or mechanism.
5. Watch the post-event path: immediate displacement, 5/15/30/60 minute continuation or retracement, structure break/reclaim, MFE/MAE, duration and eventual normalization/continuation.
6. Persist each event as a retrievable **Gold movement episode / learning card** with immutable evidence and timestamps.
7. Before later decisions, retrieve genuinely comparable prior Gold episodes and include counterexamples, not only confirming examples.
8. AIDY must form an **independent Gold directional view** before using a provider signal as additional human alpha.
9. Counterfactual scoring must include:
   - provider trade taken unchanged;
   - provider trade avoided;
   - provider trade reduced;
   - AIDY independent opposite-direction hypothesis when explicitly emitted before the outcome;
   - no-trade/abstention.
10. AIDY is judged by forward/out-of-sample economic value and calibration, not by the sophistication of its explanation.

Important architectural finding from the 2026-09-20 audit: the standalone repo already has many required components (shock detection, macro surprise capture, cross-market as-of reconstruction, volatility/jump intelligence, episode memory, learning cards and semantic analogue retrieval), but they are fragmented. In particular, `build_unexplained_market_shock()` intentionally forbids narrative cause attribution. The next build is therefore an **evidence-backed Gold Movement Investigator** that joins these existing components rather than creating a parallel stack.

Live-money authority remains OFF while this is built and tested. The research system may learn an independent opposite-direction view, but that does not silently become broker authority.


## Owner refinement — toolbox mastery + cycle-learning lens (2026-09-21)

This refines, but does **not replace**, the Gold-first causal-learning architecture above.

AIDY must understand the full toolbox already built across Aidy-Gold-Signals and Super Signals. A capability merely existing in code is insufficient. The reasoning contract must know:
- the capability/tool name;
- what market question it answers;
- when it is relevant;
- whether it is live/PIT-safe, standing evidence, downstream callable, historical/research-only, or not yet connected;
- whether it was considered/used for a decision or movement investigation;
- how useful it has actually been in resolved forward/historical evaluation.

The 15-minute cycle idea is an **additional learning lens**, not AIDY's entire specification. It should complement 5m shock detection, multi-timeframe structure, macro/calendar, rates/yields, cross-market, volatility/GVZ, CME, news, liquidity, provider evidence, historical analogues, execution context and self-critique.

Cycle-learning objective:
1. Maintain a continuous 15-minute Gold state/view timeline with bullish / bearish / neutral / unknown states.
2. Freeze each view before its future window is known.
3. After the window resolves, attach the realised 15-minute direction/path and score the prior view.
4. Build intraday sequences/cycles from those windows and measure persistence, transition, reversal and duration.
5. Retrieve genuinely similar prior day/path/setup sequences, including counterexamples, and measure what happened next rather than assuming cycles repeat.
6. Track daily accuracy/calibration and feed resolved results into AIDY's research memory/self-critique.
7. Record which toolbox surfaces were available, considered and used for each cycle view so future evaluation can identify which tools add value.
8. Historical cycle evidence remains research/descriptive unless its provenance and no-hindsight boundary are qualified. It cannot silently create live-money authority.

The goal is a richer Gold memory: AIDY should be able to ask, for example, “have I seen a similar developing day/setup before, how did those paths evolve, how long did the state persist, what contradicted it, and which evidence tools were actually useful?” It must also be willing to answer UNKNOWN when historical support is weak.
