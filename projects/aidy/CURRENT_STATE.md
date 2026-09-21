# AIDY — Current State

## Expert-gate programme — BUILDS 1-18 COMPLETE / BUILD 19 NEXT (2026-09-21)

The 24-build expert-gate programme is underway.

**Builds 1-17:** complete. See prior handovers and acceptance evidence.

**Build 18 — News / Movement Mechanism Expert:** complete and engineering-proven.

Build 18 adds `aidy_gold_news_movement_mechanism_expert_v1` plus the bounded Finnhub adapter `aidy_finnhub_market_news_adapter_v1`.

Proven behavior:
- abnormal Gold moves are investigated using the existing frozen movement investigator;
- scheduled-event evidence and Finnhub news evidence remain separate, timestamped evidence families;
- Finnhub uses `FINNHUB_API_KEY`, `/news`, bounded categories `general` + `forex`;
- publication and first-observed timestamps are enforced at the decision as-of;
- future news rows are excluded;
- source authority is explicit;
- duplicate/syndicated stories collapse before agreement scoring;
- credible sources can agree, disagree, or remain insufficient;
- scheduled events can agree/disagree with news without becoming causal proof;
- unsupported narratives remain unsupported and are never admitted as evidence;
- disagreement remains unresolved rather than fabricated;
- the expert is context-only and cannot create an automatic bullish/bearish vote.

Acceptance evidence:
- tested PR #225 head: `6ca20729e1925dde30d2cfe123648371d437e648`;
- implementation merge: `5270f17b536d496d39d231b52da76ad391d4a610`;
- repository handoff merge: `160673ea6172bb3aa182a03ab5b02475edceffd7`;
- Evidence Semantic Change Gate: PASS — run `35608776114`;
- acceptance workflow: PASS — run `35608776007`;
- focused suite: 61 passed;
- full repository regression: 1577 passed;
- Finnhub response-schema adapter: PASS;
- duplicate-story anti-double-counting: PASS;
- unsupported narrative: PASS;
- UNKNOWN path: PASS;
- source disagreement unresolved: PASS;
- scheduled-event/news agreement without causal claim: PASS;
- future-news PIT exclusion: PASS;
- directional authority: FALSE;
- live-money authority: FALSE.

The user already owns a valid Finnhub key on the separate Super Signals Render runtime. Build 18 does not create a Super Signals dependency or silently copy secrets across products. AIDY's Finnhub adapter is ready for the same key in AIDY's own secret store; the optional authenticated smoke workflow remains available.

**Next:** Build 19 — Analogue / Episode Expert. It will retrieve comparable historical Gold states without hindsight using movement episode memory, analogue retrieval, gate/environment similarity, duplicate collapse, symmetric counterexamples and continuation/retrace distributions.

## Factual cycle-start environment v2 — LIVE (2026-09-21)

AIDY now freezes a canonical PIT-safe factual environment before each 15-minute Gold cycle and learns marker usefulness **by market condition** rather than one universal tool score.

Live versions:
- cycle environment: `aidy_gold_cycle_environment_v2`
- contextual marker brain: `aidy_gold_contextual_marker_brain_v2`
- cycle memory: `aidy_gold_cycle_memory_v3`
- Worker: `aidy-signals-test`
- Worker version: `240739fb-849e-410f-a805-70a1e4496514`
- successful deploy run: `35565777824`
- final environment audit: `35565912418`

The environment stores exact start-point facts for audit, but learns on repeatable buckets: session/session phase, price location, nearest liquidity/reference distance band, sweep/reclaim state, prior-day/Asia/session range zone, M5/M15/H1/H4/D1 state, recent path, volatility/jump regime, event proximity, cross-market availability and compound regime.

Contextual scorebooks now span **13 scopes**, including liquidity+location, session+liquidity, location+HTF structure and volatility+movement regime. The canonical **34-item toolbox** is still evaluated every cycle; only legitimately directional/PIT-safe evidence is scored.

Live D1 proof for the `2026-09-21T05:45:00+00:00` cycle: Asia late-session, Gold below `asia_opening_30m_low` by the 3-8bp band, prior-day lower-middle zone, low-side reclaim, H1 bearish, H4 bullish, 4 known cross-market series, 34 toolbox items, 13 scopes, future-values=0 and live-money authority=0.

Persistent cycle-sync health is also live and reported `status=ok` at `2026-09-21T05:48:01.095000+00:00`.

The AIDY repo itself now carries its own memory/handoff: root `MEMORY.md`, `README.md` entry point and `docs/current-gold-learning-state.md`. Full handover: `projects/aidy/handovers/2026-09-21-cycle-environment-v2-live.md`.

No execution/provider/risk authority changed; owner 1% risk and formal-forward OFF remain intact.

## Contextual marker-learning brain — LIVE (2026-09-21)

AIDY's 15-minute Gold learner now scores toolbox markers by **environment**, not just globally. Runtime code from `6f9b607c0201bec77f5996126d158914864d58e5` is live on Worker version `a264b7b3-e26a-406f-827f-2ebd7f128740`; repository main after audit cleanup is `a2c029b9954b2b06964b8cd7f1c9d60d35458192`.

The canonical toolbox has **34 capabilities**. Every capability is evaluated each cycle. Directional/PIT-safe surfaces become scoreable markers; contextual or unavailable tools remain explicit rather than receiving fabricated votes.

Marker outcomes are scored `-2/-1/0/+1/+2`: large correct moves (+2), normal correct (+1), unavailable/unscoreable (0), normal wrong (-1), large wrong (-2). Current large-move threshold is `abs(15m return) >= 5 bps`. Plain accuracy is stored separately.

Each score updates seven environment scopes: global, session, session+15m state, higher-timeframe environment, session+move regime, session+state+event, and full environment. Learned weight multipliers are bounded to 0.5x-1.5x and only become more specific as minimum sample thresholds are met.

Immediate live proof: the resolved 04:00-04:15 miss was backfilled automatically. H4 bullish scored **+2**; H1 bearish, two M15 bearish markers, M5 bearish and the movement detector bearish each scored **-2** against the +6.8 bps bullish outcome. D1 showed **6 marker observations, 6 marker results, and 42 contextual score rows (6 x 7 scopes)**.

Provider Context exposes the selected marker profiles and effective learned weights. No execution, provider-rule or 1% risk changes were made. Full handover: `projects/aidy/handovers/2026-09-21-contextual-marker-learning-brain-live.md`.

## Gold cycle learning + auditable toolbox reasoning — LIVE (2026-09-21)

AIDY main `9b23e1c83fd169fb9ad08ded97a1ba4cce59ddee` is deployed to Cloudflare Worker `aidy-signals-test`, Worker version `395ada01-cf5d-4b51-9b4f-fd207e837a6d`. Final canonical deploy run `35559806815` completed successfully with the direct minute cron present, capture enabled, Twelve Data/public-independent, Provider Context routes live, and formal-forward/live-money authority OFF.

The additive 15-minute Gold cycle learner is now live. Every view is frozen before its target window and stores bullish/bearish/neutral/unknown state plus a cross-checkable reason trail: supporting reasons, contradictory reasons, missing/unavailable evidence, toolbox manifest digest, toolbox considered and toolbox actually used. Post-window outcomes attach realised direction, return, MFE/MAE and scoring without rewriting the original reasoning.

Live D1 audit of the `2026-09-21T04:00:00+00:00` view proved: observed bearish, AIDY bearish, **5 supporting reasons**, **1 contradiction**, **33 toolbox capabilities considered**, **5 tool/evidence surfaces used**, **13 unavailable evidence items kept explicit**, `future_values_used=0`, `live_money_execution_allowed=0`.

Historical cycle memory is also loaded: **46,353** retrospective M15 Gold cycle rows from **47,319** BigQuery research-candle rows across 2024-2025, covering **120 distinct state sequences** and **95 UTC time slots**. Safety audit found **0 illegal PIT rows, 0 illegal research flags and 0 illegal live-money rows**. This history is descriptive analogue memory only.

The 15-minute cycle is one learning lens, not AIDY's full specification. Gold-first causal learning remains primary. Known-but-not-yet-live/PIT-connected parts of the wider arsenal remain explicit UNKNOWN, including parts of rates/macro surprise, intraday cross-asset reaction, CME, GVZ and breaking-news/official-release search. Full handover: `projects/aidy/handovers/2026-09-21-gold-cycle-toolbox-learning-live.md`.

## Gold movement capture + canonical toolbox — LIVE (2026-09-21)

The Gold-first movement spine is now live and directly proven in remote D1. AIDY PR #147 (`bbbc9a59d2fcc9fc0fe0fd9bf18dd90091dfd084`) added an immutable scan ledger and bounded backlog scanning so normal and abnormal snapshots are continuously advanced rather than only checking the single latest snapshot. Live audit run `35557600712` found 2 genuine abnormal episodes: **1 UP and 1 DOWN**, both honestly `cause_unknown`. AIDY PR #148 (`5f11c13b86467e72cd178b3c92cb44e813732533`) deployed `aidy_gold_toolbox_manifest_v1`, a 30+ capability catalogue with explicit live/downstream/research-not-connected states. Super Signals PR #240 (`f33a83ffa965b4b42ab2cd579b6012ba85a601f6`) is LIVE on Render deploy `dep-daoaeau8bjmc73b6mmeg`, consumes that catalogue in `aidy_live_toolbox_manifest_v2`, and uses prompt `aidy_reasoning_prompt_v14_gold_toolbox`. Post-deploy Provider Context probe was READY. Learning-card maturity is not yet proven because the first live episodes had not reached the 60-minute forward horizon at audit time. Rates/macro surprise, intraday cross-asset reaction, CME, GVZ and breaking-news tools are known to AIDY but remain explicitly not live/PIT-connected. Full handover: `projects/aidy/handovers/2026-09-21-gold-movement-toolbox-live.md`.


## AIDY Provider Context self-heal — LIVE (2026-09-21)

AIDY main `aebb414656e9e1f6f30f2cf954366085792dca6f` is deployed to the canonical Cloudflare Worker. Deployment workflow run `35557298002` completed successfully at `2026-09-21T03:23:24Z` after lint/test cleanup. Live health is green: direct-cron, capture enabled, Twelve Data/public-independent, formal forward OFF, and both scheduled capture and Provider Context fresh at `2026-09-21T03:22:30.148000+00:00`. The bounded intraday self-heal is live and may repair only small recent <=30-minute M1 gaps needed for M5/M15/H1/H4 while preserving strict evidence and fail-closed behavior. Full handover: `projects/aidy/handovers/2026-09-21-live-self-heal-deployed.md`.


## Actions monitoring cutover — COMPLETE; Provider Context fault later RESOLVED (2026-09-21)

AIDY GitHub Actions monitoring was rationalized in `dannythehat/Aidy-Gold-Signals` PR #140, merged as `09066e085493b2970530adf82577db132164c94a`. Three every-10-minute GitHub schedules plus one hourly schedule were removed, eliminating approximately 13,680 scheduled GitHub workflow launches per 30-day month. The corresponding workflows remain manually runnable. Cloudflare direct-cron remains the canonical AIDY runtime monitor and already records capture, Provider Context, archive and Gold-movement health.

Post-cutover live verification found a separate Provider Context staleness fault at `2026-09-21T01:57:30.150000+00:00`; Super Signals also logged `AidyContextTerminalMiss`. That fault was subsequently repaired by the bounded intraday self-heal and reverified live. See `projects/aidy/handovers/2026-09-21-live-self-heal-deployed.md`. The Actions-cutover handover remains at `projects/aidy/handovers/2026-09-21-actions-monitoring-cutover.md`.


> **Owner mandate in force since 2026-09-17: read [`OWNER_MANDATE.md`](../../OWNER_MANDATE.md) every session.** It sets the goal (AIDY becomes an evidence-scored decision layer that measurably improves Super Signals' profit) and the one boundary that does not move under it (live-money authority stays OFF until explicitly graduated per class).

Last verified: **2026-09-21**

Authoritative repo: `dannythehat/Aidy-Gold-Signals`
Authoritative branch: `main`
Verified repository `main` SHA: `1635f68a4ed98298f979d6d13521c21c1b0e4463`
Live Worker: `aidy-signals-test`

## Toolbox-aware decision layer + measured historical exam — ACTIVE (2026-09-20)

Super Signals reasoning now carries an explicit AIDY toolbox contract. Production reasoning prompt
`aidy_reasoning_prompt_v12_toolbox` requires AIDY to read `toolbox_manifest`, consider every
available standing evidence surface, call an on-demand tool when it can materially resolve a
take/reduce/reject uncertainty, avoid meaningless checklist calls, and preserve UNKNOWN when a
surface is unavailable or not connected.

Connected on-demand surfaces are candles and economic calendar in live reasoning; the historical
stress lab additionally has a focused evidence inspector. Standing evidence includes provider
history, Gold/market context, recent provider messages, event/liquidity/execution context,
historical analogues/provider alpha, probability/EV/management context, and failure/self-critique.
Broader AIDY modules such as rates/macro vintages, cross-market, CME contract state, GVZ/volatility,
semantic context and provider decision memory are NOT to be falsely treated as callable until an
auditable adapter makes their timestamp/provenance semantics valid. Their unavailable state is
explicit in the manifest.

Production Super Signals commits:
- PR #228 `521b4c9002f7ffa22aae54a585c6edfbd5b10e53`: historical toolbox
- PR #229 `134a81d79fe88d6b2343a08e657d6307a1d30402`: toolbox-aware prompt/live manifest
- PR #230 `36dee29f4b87dfe2f94bb02ea19f21c612b363d4`: historical manifest-key alignment
- PR #231 `e92c46f92d7c9679066fbdbbb1bd46dd281d4029`: exact tool-name telemetry, stress replay `aidy_historical_stress_lab_v7_tooltrace`
- PR #232 `5b09fea3f7707a8f752c888f187c99c1a531f8e7`: independent 571-case training identity freeze
- PR #233 `f85a0456d1d0cf566c4b6eb4ecdc0c3722e22abb`: reconstructed-stress DB schema expansion; first deploy rolled back safely on scoreboard-view dependency
- PR #234 `745b5af537cd0028535cb5e7400255b49d101156`: corrected transactional migration; live Alembic head `0108_aidy_hist_stress_schema`, Render gate 1,191 passed / 137 skipped

The active train identity is 571 cases, SHA-256
`18326c515d12a7e55046828f6fe59198de50b0b7538193174528bf56f7829168`.
Validation and OOS remain sealed. Three late historical rows now make the dynamic source query
571/70/162, but they are not admitted into the original frozen 571/69/160 evaluation design.
The 18-case exact holdout remains sealed.

Full handover:
`projects/super-signals/handovers/2026-09-20-aidy-toolbox-awareness-training-stress.md`.

## Large historical acceleration lab — MERGED / RESEARCH OFF PENDING TRAIN RUN (2026-09-20)

The owner explicitly directed a full AIDY audit and historical acceleration programme. Super Signals
now contains a separate **803-source / 800-scoreable reconstructed research stress lab** over older resolved XAUUSD
provider trades: **571 train / 69 validation / 160 research-OOS**, with 3 source cases excluded because no resolvable provider trade score exists. The official exact-PIT
**18-case holdout remains sealed and separate**.

Hardening found and fixed real gaps before any training claim: the original 650-call ceiling could
not cover all OOS cases; evaluation partitions were insufficiently locked; historical reasoning had
no candle tools; and the large replay lacked reconstructed as-of provider memory. PRs **#221-#223**
are merged; latest implementation SHA is
`25d6cea1dc7dd127e9890b0363148f1732557da4`.

The current replay can use retrospective-research 1/5/15/30/45/60-minute candles, conservative
official scheduled-event timing, recent provider messages, prior-resolved analogues, and
provider-specific overall/side/session evidence known before each target signal. All reconstructed
evidence remains explicitly non-PIT/research-only and cannot grant live authority.

Training protocol is fixed: 571 train first; tune only there; freeze; 70 validation without tuning;
freeze; 162 research-OOS; only then final exact-PIT holdout. See
`projects/super-signals/handovers/2026-09-20-aidy-large-historical-stress-lab.md`.

## Automatic forward acceptance monitor — LIVE

Built and deployed 2026-09-19 so Phase 1 no longer depends on a manual Monday check.

Production Super Signals SHA: `ec7febbdaa2fbd6444eae58a0873769943c5e89b`; Render deploy: `dep-dan2kgdii2qc73bhsi50`;
Alembic: `0105_aidy_grounding_accept`.

The monitor is **observational only**. It reads evidence-v2 AIDY reasoning rows, validates the
frozen evidence contract again, and writes a research-only acceptance ledger. It has no broker,
execution, sizing, provider-status or live-money write path.

It checks:

- evidence contract is exactly `aidy_reasoning_evidence_v2`;
- claim validation already passed and unsupported count is zero;
- every provider claim ref exists in the frozen evidence snapshot;
- no duplicate claim refs/claim IDs;
- source/path/sample/version provenance is present and valid;
- provider evidence timestamps are never later than the signal timestamp;
- provider-profile claim versions match the frozen profile version on the annotation;
- prohibited free-form provider-history language did not escape into rationale/key factors/action reason.

State machine:

- `waiting_forward_rows` — no fresh evidence-v2 decisions yet;
- `clean_so_far` — fresh rows exist and all are clean, but acceptance sample is not yet complete;
- `accepted` — at least 10 clean rows across at least 2 providers;
- `failed` — any audited row violates the contract.

Initial live state: `waiting_forward_rows`, 0 invalid rows, research_only=true,
live_money_execution_allowed=false.

Exact deploy acceptance: **1113 API tests passed, 137 skipped, 2 warnings**; web suite and
secret scan also passed. Public API and website proxy still respond after deploy.

## Phase 0/1 anti-drift — PRODUCTION VERIFIED / WAITING FOR FORWARD ROWS

Verified 2026-09-19 against the deployed Super Signals runtime.

The evidence-grounding/anti-drift layer is now deployed in the signal-level AIDY reasoning
path. Production Super Signals SHA: `33305a020f96e545990906a6de0c5dc253e9fcaf`; Render deploy:
`dep-dan2cv5ii2qc73bhmpig`; Alembic: `0104_aidy_grounding_health`.

Engineering acceptance on the exact deployed build:

- API suite: **1105 passed, 137 skipped, 2 warnings**.
- Web suite: **28 passed**.
- secret scan: PASS.
- Render `/health`: healthy after deploy.
- origin and website public-performance endpoints: responding after the post-deploy startup
  settled.
- AIDY live-money authority: unchanged/OFF.
- Super Signals owner risk: unchanged at 1%.

What is now enforced:

- provider history reaches the model only as versioned, PIT-safe atomic claims;
- every claim carries the exact source path/value/sample N/version/evidence timestamp;
- side-performance evidence is scoped to **this signal's side**;
- session-performance evidence is scoped to **this signal's session**;
- a missing BUY/SELL/session cohort remains UNKNOWN and cannot be inferred from an opposite
  cohort;
- provider identity and raw provider profile/fingerprint text are not sent to the model;
- provider-history prose is rejected outside validated `provider_claim_refs`;
- unsupported claim references fail safe and are not persisted as successful reasoning;
- every new grounded annotation freezes the exact evidence snapshot and claim references;
- production grounding health is queryable through
  `aidy_reasoning_grounding_health`.

Legacy audit at deployment: 2674 historical reasoning annotations are explicitly
`legacy_unvalidated`; 2227 contain language the stricter detector marks for review. That
number is **not** a count of proven false claims. It means those rows predate the evidence-ref
contract and therefore cannot be granted grounded status retrospectively.

Forward acceptance is correctly still **WAITING**: the market is in the canonical weekend
closure and there are currently 0 new `aidy_reasoning_evidence_v2` forward annotations.
The next acceptance is mechanical: on the first fresh eligible signals, require
`claim_validation_status=passed`, `unsupported_claim_count=0`, and inspect the exact frozen
claim/evidence pairs. Do not advance the programme past Phase 1 acceptance before this check.

## Current production status — HEALTHY, multi-cycle verified

The 16 September `stale_provider_context` state is resolved and deployed. Verified not by
a single startup probe but by 53 consecutive `complete` market snapshots (zero `partial`)
across 4+ hours on 2026-09-17 — see
`projects/super-signals/handovers/2026-09-17-continuous-health-verification.md` for the
full cross-system evidence (AIDY D1 ground truth, Super Signals resolver progress, log
window, live health check).

Live Worker health as of last check:

- runtime: `cloudflare-workers`
- scheduler: `direct-cron`
- `capture_enabled=true`
- market source: `twelve_data`
- market ownership: `public_independent`
- `formal_forward_enabled=false`
- `data_health.status`: `fresh`
- `provider_context_snapshot_lag_seconds`: ~150 (fresh, well under the 10-minute cutoff)

No known active health failure.

## PR #133 — MERGED

PR #133 `Keep Provider Intelligence alive when only D1 context is missing` was merged on 16 September 2026.

Verified PR head before merge:

`01c6a955c5c7c513a6db86f70cdc2e7d146ea246`

Merge commit now on `main`:

`0a6230e606282dca97675d63117c4d24dcc38120`

Exact current-head acceptance performed outside GitHub Actions before merge:

- Ruff: PASS
- compile: PASS
- focused Provider Context tests: **33/33 PASS**
- full repository suite: **1270/1270 PASS**

Safety boundary independently checked:

- Provider Context keeps `live_money_execution_allowed=false` hardcoded/unconditional.
- Formal forward keeps its own separate untouched complete-snapshot gate in `forward_live_observer.py`.

## GitHub ruleset state during recovery — resolved

Ruleset `Protect main` id `22096458` was temporarily edited by the owner (Claude has no
ruleset-read/write tool in this environment — confirmed directly by a failed `merge_pull_request`
attempt returning `405` citing the required-check rule, with no admin-bypass path through the
merge API either) so the unavailable GitHub Actions required-check rule no longer blocked
merging PR #133. Deletion protection, force-push protection and the pull-request requirement
stayed active throughout.

## Recovery actions — all complete, verified 2026-09-17

1. Required-status-check protection: restored by the owner.
2. `main` commit `0a6230e606282dca97675d63117c4d24dcc38120` deployed to the canonical Worker
   via `.github/workflows/aidy-provider-research-read-deploy.yml` once Actions capacity
   returned — not a direct Cloudflare/Wrangler session; that workflow is the deploy path,
   and it ran successfully. Confirmed by reading the deployed Worker source directly
   (`workers_get_worker_code`): it contains `aidy_provider_context_api_v2` and
   `intraday_complete_d1_missing`, the exact PR #133 markers.
3. Deploy preserved `* * * * *` direct Cron, capture ON, Twelve Data/public-independent
   ownership and `AIDY_FORMAL_FORWARD_ENABLED=false` — asserted by the deploy workflow itself
   and independently confirmed live.
4. Cloudflare schedule state verified post-deploy.
5. `/health` confirmed `data_health.status: fresh`, no `stale_provider_context`.
6. Super Signals confirmed receiving current AIDY context across 53 consecutive cycles — see
   `projects/super-signals/handovers/2026-09-17-continuous-health-verification.md`.

## Phase 2 Gold State Engine v1 — BUILT IN ISOLATION / NOT YET GRADUATED

Built 2026-09-19 on isolated branches while the Phase 1 anti-drift forward gate remains
`waiting_forward_rows`.

Standalone AIDY branch: `feature/gold-state-engine-v1`, head
`709d7702ec7b479d86ff8f8289d095bad8045cf0`, PR #137.

Super Signals consumer branch: `feature/aidy-gold-state-v2-reasoning`, head
`f6e1e42ecb8ff18b153912915588f4c6945711b6`, PR #208 against the production branch. **Do not merge PR #208 until
Phase 1 forward grounding is accepted.**

Gold State Engine v1 now composes a deterministic PIT-only XAUUSD dossier with:

- completed-bar M1/M5/M15/H1/H4 close-path structure;
- named session state;
- observed prior-day, Asia overnight, named-session and opening-range location/distance;
- explicit descriptive round-number references with no predictive-edge claim;
- liquidity penetration/reclaim **proxies**, explicitly not hidden order flow;
- PIT realised-volatility/jump context where qualified;
- five-minute displacement and five-minute range expansion/compression versus prior
  non-overlapping completed five-minute blocks;
- scheduled-event timing context when known;
- explicit `cause_unknown` for elevated/extreme moves because Phase 2 does not claim
  causality;
- explicit UNKNOWN surfaces and deterministic packet digest.

The engine is hard-coded `research_only=true`, `descriptive_context_only=true`,
`predictive_edge_claimed=false`, `live_money_execution_allowed=false`,
`future_values_used=false`.

Super Signals production was changed only to accept both Gold State v1 and v2 safely before
the isolated build. Production SHA `4650d2074ea4d4287285783a5157d4340cd41e8a`, Render deploy
`dep-dan2p2dii2qc73bi09h0`, **1116 API tests passed, 137 skipped, 2 warnings** plus web/security
gates. The isolated PR #208 adds stricter v2 validation and prompt semantics but is not live.

GitHub Actions remain credit-exhausted: PR jobs terminate in seconds with no job steps/logs,
matching the already-documented account condition. Therefore PR #137 and #208 are deliberately
not merged/deployed and no false green-test claim is made for the isolated heads. Static blast
radius is bounded to Gold-state/provider-context/reasoning files and tests; repository compares
show no broker/execution/sizing/provider-status files touched.

Current production remains unchanged: standalone Worker health `ok`, capture enabled,
formal-forward OFF, Twelve Data/public-independent; Phase 1 acceptance still
`waiting_forward_rows`, 0 invalid rows, research-only, no live-money authority.

## Approved next build — Master Gold Intelligence

Owner and ChatGPT aligned on 2026-09-19 that AIDY's destination is a full Gold specialist,
not merely a provider scorer. The detailed build/test contract is now pinned at
`projects/aidy/MASTER_GOLD_INTELLIGENCE_BUILD.md`.

Core new requirements:

- explain abnormal Gold moves from point-in-time evidence and distinguish known mechanism
  from plausible narrative;
- attribute trade failures without hindsight storytelling;
- treat liquidity/execution quality, MFE/MAE and profit extraction as first-class learning;
- match historical setups by regime and outcome distribution, not visual similarity;
- learn provider edge conditionally by side/session/regime/management/event state;
- require every provider-specific rationale claim to be evidence-addressable;
- maintain an explicit UNKNOWN state and learn what evidence is missing;
- add breaking-news/event intelligence, but only as a qualified context mechanism;
- move toward calibrated probabilities/expected value and measure whether TAKE/REDUCE/HOLD/
  REJECT/NO-TRADE decisions actually improve counterfactual value;
- continuously ablate features and remove complexity that does not add forward value.

Architecture boundary remains unchanged: AIDY market/research stays separate from Super
Signals broker execution; AIDY live-money authority remains OFF until separately graduated.

## New central product direction — decision intelligence

Once Provider Context is healthy, AIDY should begin producing a shadow decision for every eligible Super Signals provider trade.

Target decision classes:

- `APPROVE`
- `DENY`
- `HOLD/NO_SECOND_ENTRY`
- `CONFLICT_DENY`
- `CLOSE_EARLY`
- `CONTINUE`

Target pipeline:

`provider signal -> PIT-safe market context -> provider history -> current exposure -> AIDY decision -> action -> outcome -> counterfactual score -> learning`

AIDY must prove whether its intervention made or saved money versus the fixed baseline that would otherwise have occurred.

## Reuse what already exists

Do not create a parallel system. Existing Super Signals infrastructure already provides substantial foundations:

- `provider_trade_observations`
- `provider_trade_scorer.py` + `provider_trade_scores`
- `provider_trade_scoreboard`
- `canonical_signal_ledger.py` + `signal_events.py`
- `provider_day14_governance.py`
- `provider_day18_combined_book.py`

Genuinely new or incomplete pieces include the persistent hypothesis/question registry and cross-provider duplicate/exposure clustering. Add a small immutable AIDY decision layer on top of the existing observation/scoring spine rather than rebuilding capture or scoring.

## Authority graduation

Likely sequence:

1. deterministic duplicate rejection
2. obvious duplicate/conflicting exposure controls
3. provider/regime denies
4. early-close management
5. broader approve/deny/management authority

Each authority class requires an audit trail, kill switch, prospective evidence and explicit owner/live gate. The current Super Signals 1% risk directive must not silently change.

## Session rule

Read `OWNER_MANDATE.md` first, then verify the current AIDY repo, Worker health and Super Signals production state directly. Source/runtime truth overrides Memory if it has advanced.

## Gold-first causal learning mandate — 2026-09-20

Owner correction: AIDY must be developed as a **Gold intelligence system first, provider filter second**.

Primary loop:
`detect Gold move -> investigate evidence-backed cause/mechanism -> observe continuation/reversal -> store structured movement episode -> retrieve analogues -> form independent Gold view -> compare with provider call -> score economic value.`

This supersedes any testing interpretation that only asks how much of a provider trade AIDY kept.
Historical/live evaluation must separately credit:
- avoiding a losing provider trade;
- reducing a genuinely bad provider trade;
- preserving profitable provider trades;
- an independently emitted opposite-direction Gold hypothesis when it was frozen before outcome;
- abstention/no-trade.

No hindsight and UNKNOWN discipline remain mandatory. Live-money authority remains OFF until separately graduated.

Canonical detailed contract: `projects/aidy/MASTER_GOLD_INTELLIGENCE_BUILD.md`.


## Gold-first build implementation — 2026-09-20

Implemented and merged in standalone AIDY:
- Merge SHA: `f2f809bdd1610d4b16166160bca6a43ceb19322b`
- Gold State Engine v1 remains the descriptive PIT market-state base.
- Added `aidy_gold_movement_investigator_v1`: abnormal Gold displacement/range/jump triggers an evidence-backed investigation with explicit supported/plausible/unknown attribution and missing-evidence requests.
- Added `aidy_gold_movement_memory_v1`: Gold movements are learned independently of provider signals. Abnormal movement episodes are frozen, deduped, and after a 60-minute forward window receive immutable continuation/reversal/mixed learning cards.
- Added D1 migration `0021_gold_movement_memory.sql`.
- Provider Context exposes the verified movement investigation inside Gold state.
- Cloudflare provider deploy workflow now applies D1 migrations, tests investigator/memory modules, and verifies investigator/memory health versions.

Deployment truth at handoff: GitHub Actions did not start after the merge because the account Actions capacity is exhausted. Therefore the standalone AIDY merge is in `main`, but its new Cloudflare Worker/D1 rollout is NOT yet proven live. Do not describe merged code as deployed until the Worker health response shows the new movement investigator/memory versions.

Gold-first rule remains: AIDY forms an independent Gold view first, provider signal second; no live-money authority was added.


## Gold-first build final deployment status — 2026-09-20

Do NOT mark the Gold-first architecture fully complete yet.

- Standalone AIDY Gold-first brain code is merged to main at `f2f809bdd1610d4b16166160bca6a43ceb19322b`.
- GitHub Actions returned no workflow runs for that merge, so Cloudflare Worker/D1 deployment of the new Gold Movement Investigator + Movement Memory is NOT yet proven live.
- The code exists and is merged; deployment remains the blocker.
- Super Signals may safely consume the older Gold-state packet until the standalone provider context v5 rollout is proven live.
