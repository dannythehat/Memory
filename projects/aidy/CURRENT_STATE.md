# AIDY — Current State

> **Owner mandate in force since 2026-09-17: read [`OWNER_MANDATE.md`](../../OWNER_MANDATE.md) every session.** It sets the goal (AIDY becomes an evidence-scored decision layer that measurably improves Super Signals' profit) and the one boundary that does not move under it (live-money authority stays OFF until explicitly graduated per class).

Last verified: **2026-09-17**

Authoritative repo: `dannythehat/Aidy-Gold-Signals`
Authoritative branch: `main`
Verified source `main` SHA: `0a6230e606282dca97675d63117c4d24dcc38120`
Live Worker: `aidy-signals-test`

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