# AIDY — Current State

Last verified: **2026-09-16**

Authoritative repo: `dannythehat/Aidy-Gold-Signals`
Authoritative branch: `main`
Verified source `main` SHA: `0a6230e606282dca97675d63117c4d24dcc38120`
Live Worker: `aidy-signals-test`

## Current production status — RED / degraded

AIDY market capture is running and fresh, but Provider Context is still stale because the newly merged recovery code has not yet been deployed to Cloudflare.

Latest verified Worker health before deployment:

- runtime: `cloudflare-workers`
- scheduler: `direct-cron`
- `capture_enabled=true`
- market source: `twelve_data`
- market ownership: `public_independent`
- `formal_forward_enabled=false`
- latest scheduled capture success: `2026-09-16T18:22:09.331000+00:00`
- capture lag at check: **88 seconds**
- latest accepted Provider Context snapshot: `2026-09-15T20:57:36.761999+00:00`
- Provider Context lag at check: **77,161 seconds**

Active health failure remains:

`stale_provider_context`

Reason:

`market capture is fresh but complete Provider Context is stale or missing`

Do not describe AIDY as fully healthy until the merged recovery is deployed and production-verified.

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

## GitHub ruleset state during recovery

Ruleset `Protect main` id `22096458` was temporarily edited by the owner so the unavailable GitHub Actions required-check rule no longer blocked the merge.

Immediately before merge, the ruleset still preserved:

- enforcement active
- deletion protection active
- non-fast-forward / force-push protection active
- pull-request requirement active

Only the required-status-check rule was removed for the merge because GitHub Actions credits are exhausted for approximately one week.

The required status-check protection should now be restored by the owner. If re-enabled during the credit outage, future PRs will remain intentionally blocked until Actions capacity returns.

## Remaining recovery actions

1. Restore `Require status checks to pass` in `Protect main`, preserving the two original checks if GitHub presents them:
   - `Evidence Semantic Change Gate / classify-protected-diff`
   - `AIDY Day 53 Twelve Data OHLC Adapter / acceptance`
2. Deploy `main` commit `0a6230e606282dca97675d63117c4d24dcc38120` to the canonical Cloudflare Worker.
3. Deployment must preserve `* * * * *` direct Cron, capture ON, Twelve Data/public-independent ownership and `AIDY_FORMAL_FORWARD_ENABLED=false`.
4. Verify Cloudflare schedule state after deploy.
5. Verify `/health` no longer reports stale Provider Context.
6. Verify a genuinely current Super Signals provider signal receives current AIDY context instead of `pit_context_stale`.

Current ChatGPT tooling has no authenticated Cloudflare write/deploy route. The Worker must therefore be deployed from an owner-authenticated Cloudflare/Wrangler session.

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

Read the 16 September handover first, then verify the current AIDY repo, Worker health and Super Signals production state. Source/runtime truth overrides Memory if it has advanced.