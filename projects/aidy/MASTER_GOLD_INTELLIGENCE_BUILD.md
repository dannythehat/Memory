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
