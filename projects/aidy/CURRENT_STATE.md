# AIDY — Current State

Last verified: **2026-09-16**

Authoritative repo: `dannythehat/Aidy-Gold-Signals`
Authoritative branch: `main`
Verified source `main` SHA: `bf3bb05ca5a9320e31173bbd93f41cf797b6ed51`
Live Worker: `aidy-signals-test`

## Current production status — RED / degraded

AIDY market capture is running and fresh, but Provider Context is stale.

Latest verified Worker health:

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

Active health failure:

`stale_provider_context`

Reason:

`market capture is fresh but complete Provider Context is stale or missing`

Super Signals therefore correctly rejects stale AIDY joins with `pit_context_stale` / `AidyContextTerminalMiss`.

Do not describe AIDY as fully healthy until current Provider Context is production verified.

## Recovery already built — PR #133

Open PR #133:

`Keep Provider Intelligence alive when only D1 context is missing`

Current head SHA:

`01c6a955c5c7c513a6db86f70cdc2e7d146ea246`

The immediately prior head `06ffdc8dc87c8aba8e521b237e181121fbd82cfd` had a genuine Ruff `UP035` failure from deprecated `typing.Mapping`. Claude fixed only that import, changing it to `collections.abc.Mapping`; comparison confirms this final commit changes only `src/aidy/provider_context_api.py` by +2/-1.

Exact current-head acceptance performed outside GitHub Actions:

- Ruff: PASS
- compile: PASS
- focused Provider Context tests: **33/33 PASS**
- full repository suite: **1270/1270 PASS**

Safety boundary independently checked:

- Provider Context keeps `live_money_execution_allowed=false` hardcoded/unconditional.
- Formal forward keeps its own separate untouched complete-snapshot gate in `forward_live_observer.py` and does not inherit the degraded Provider Intelligence allowance.

PR #133 is therefore **ENGINEERING PROVEN but not PRODUCTION VERIFIED**.

## Exact GitHub blocker

The repository ruleset was read directly on 16 September 2026:

- ruleset id: `22096458`
- name: `Protect main`
- enforcement: active
- deletion protection: active
- non-fast-forward protection: active
- pull-request requirement: active
- required approving reviews: 0
- bypass actors: none
- current connected user bypass: `never`
- strict required-check policy: false

The only merge-blocking rule is the two required status checks:

1. `Evidence Semantic Change Gate / classify-protected-diff`
2. `AIDY Day 53 Twelve Data OHLC Adapter / acceptance`

The owner confirms GitHub Actions credits are exhausted for approximately one week. On the current PR head, both checks again failed in about two seconds before normal runner execution.

The ChatGPT GitHub connection can **read** the ruleset but exposes no ruleset-write/admin action. Browser automation was also tested and is not authenticated to GitHub. Auto-merge cannot be enabled because the repository has auto-merge disabled.

Do not use a direct branch-ref update to bypass the PR/ruleset. Preserve the protection intent.

## Remaining owner-authenticated recovery actions

1. In GitHub, temporarily remove **only** the two unavailable required status checks from ruleset `Protect main` (id `22096458`). Keep deletion protection, non-fast-forward protection and PR requirement active.
2. Merge PR #133 at exact head `01c6a955c5c7c513a6db86f70cdc2e7d146ea246`.
3. Restore the two required checks after the merge, or as soon as Actions credits return if GitHub will not allow a currently failing requirement to be restored usefully during the outage.
4. Deploy the canonical Cloudflare Worker with the merged code while preserving `* * * * *` direct Cron, capture ON, Twelve Data/public-independent ownership and `AIDY_FORMAL_FORWARD_ENABLED=false`.
5. Verify Cloudflare schedule state after deployment.
6. Verify `/health` no longer reports stale Provider Context.
7. Verify a genuinely current Super Signals provider signal receives current AIDY context instead of `pit_context_stale`.

Current ChatGPT tooling has no authenticated Cloudflare write/deploy route and no Cloudflare plugin is available. Cloudflare browser automation is also unauthenticated. Do not pretend the Worker has been deployed from this environment.

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

- `provider_trade_observations` — durable per-signal/provider observation spine;
- `provider_trade_scorer.py` + `provider_trade_scores` — deterministic outcome/counterfactual scoring foundation;
- `provider_trade_scoreboard` — provider performance aggregation foundation;
- `canonical_signal_ledger.py` + `signal_events.py` — same-source duplicate/edit collapsing;
- `provider_day14_governance.py` — fail-closed learning -> shadow -> qualified governance pattern;
- `provider_day18_combined_book.py` — combined-book/conflict research foundation.

Genuinely new or incomplete pieces include the persistent hypothesis/question registry and cross-provider duplicate/exposure clustering. Add a small immutable AIDY decision layer on top of the existing observation/scoring spine rather than rebuilding capture or scoring.

## Authority graduation

The owner wants AIDY making smart trading decisions soon, but authority must be graduated by evidence rather than switched on wholesale.

Likely sequence:

1. deterministic duplicate rejection
2. obvious duplicate/conflicting exposure controls
3. provider/regime denies
4. early-close management
5. broader approve/deny/management authority

Each authority class requires an audit trail, kill switch, prospective evidence and explicit owner/live gate. The current Super Signals 1% risk directive must not silently change.

## Session rule

Read the 16 September handover first, then verify the current AIDY repo, Worker health and Super Signals production state. Source/runtime truth overrides Memory if it has advanced.