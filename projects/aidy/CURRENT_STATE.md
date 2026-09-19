# AIDY — Current State

> **Owner mandate in force since 2026-09-17: read [`OWNER_MANDATE.md`](../../OWNER_MANDATE.md) every session.** It sets the goal (AIDY becomes an evidence-scored decision layer that measurably improves Super Signals' profit) and the one boundary that does not move under it (live-money authority stays OFF until explicitly graduated per class).

Last verified: **2026-09-19**

Authoritative repo: `dannythehat/Aidy-Gold-Signals`
Authoritative branch: `main`
Verified source `main` SHA: `526c561bf98183c58f2cabf970962eb2b26d670b`
Live Worker: `aidy-signals-test`

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