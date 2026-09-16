# AIDY — Known Issues / Deferred Work

Updated: **2026-09-16**

Only keep unresolved or deliberately deferred items here. Verify source/runtime before acting because Memory can become stale.

## Current

### 1. Provider Context is stale while market capture is fresh — ACTIVE / RED, BLOCKED ON OWNER ACTION

The Worker is capturing fresh Twelve Data on direct Cron, but the latest accepted Provider Context snapshot is still from `2026-09-15T20:57:36.761999+00:00` (still true as of 2026-09-16T18:10Z re-check). Current Super Signals joins therefore fail closed with `pit_context_stale` / `AidyContextTerminalMiss`.

Open AIDY PR #133, head `01c6a955c5c7c513a6db86f70cdc2e7d146ea246` (was `06ffdc8d`, updated 2026-09-16 -- see correction below). Independently re-verified locally, outside GitHub Actions entirely: compile clean, 33/33 focused tests, 1270/1270 full suite, ruff clean. Both safety claims checked directly in the diff, not just trusted from the PR body: `live_money_execution_allowed` is hardcoded `False` unconditionally, and `forward_live_observer.py` keeps its own separate, unmodified `capture_status != "complete"` gate -- it never calls the loosened snapshot function this PR touches.

**Correction to what was recorded here before:** the prior "17/17, ruff:pass" figures were accurate for an earlier SHA (`327ad76e`) cited inside the PR body, not for the actual open head at the time (`06ffdc8d`). Re-running against the exact open head found ruff genuinely failing (`UP035`, deprecated `typing.Mapping` import) -- unrelated to the Actions outage, a real bug the prior verification pass did not catch because it checked the wrong commit. Fixed as an import-only change and re-verified. **Lesson for future verification: diff the PR body's cited SHA against `pull_request.head.sha` before trusting any acceptance numbers it quotes.**

The PR is now blocked purely by GitHub's required-status-checks rule (`merge_pull_request` returns `405: 2 of 2 required status checks are failing` -- no other rule cited: no missing review, no other violation). **Claude cannot clear this or deploy the result** -- see the tooling gap below. Two manual actions only the owner can take are recorded in `LIVE_STATE.json -> provider_context_recovery.tooling_gap_blocking_claude`.

### 2. GitHub Actions unavailable due to exhausted credits — TEMPORARY, CONFIRMED REAL

The owner reports GitHub Actions credits are exhausted for approximately one week. Independently confirmed 2026-09-16 across 3 separate workflow runs on 2 different branches, hours apart: every run completes in 2-3 seconds with `conclusion=failure` and a 404 on log download (no runner ever executed). Not this-PR-specific.

**Claude has no way around this in the current environment**, and this is a capability gap worth recording precisely so no future session wastes time rediscovering it:
- **No ruleset/branch-protection tool.** This session's GitHub MCP server exposes PRs, checks, files, merges -- nothing for reading or editing repository rules. No `gh` CLI, no raw API access (both explicitly withheld). A direct `merge_pull_request` attempt confirmed there is no admin-bypass path through the merge API with this token either.
- **No Cloudflare deploy path.** No `CLOUDFLARE_API_TOKEN`/`CLOUDFLARE_ACCOUNT_ID` in this sandbox's environment. The Cloudflare MCP tools available are read-only for Workers (get/list/get_worker_code) -- no deploy/put tool. `aidy-signals-test` has no visible native Cloudflare git integration (unlike Super Signals on Render, which deploys independently of GitHub Actions), so the only deploy path is `uv run pywrangler deploy` inside the same GitHub Actions workflow that is down.

Do not repeatedly rerun unavailable CI -- confirmed dead across multiple attempts already. The owner needs to either bypass the 2 required checks for this one merge (restoring the rule once Actions capacity returns) and then deploy himself (wait for Actions, or run `wrangler deploy` locally against the merged `main`, preserving the `* * * * *` cron exactly as the dead workflow would have asserted it), or wait out the outage.

### 3. Formal-forward/live-money authority remains OFF

Do not treat new Decision Ledger, shadow decisions or provider intelligence as live-money authority. Decision classes must be separately graduated through prospective evidence and explicit owner/live gates.

### 4. Decision intelligence not yet implemented end-to-end

The new central roadmap requires:

- immutable AIDY Decision Ledger;
- counterfactual scoring and factual decision delta;
- conditional provider intelligence;
- persistent hypothesis/question registry;
- duplicate/conflict exposure engine;
- prospective shadow decisions for every eligible trade after Provider Context recovery.

This is the next major product build after restoring current context health.

### 5. Provider-market credential hygiene

Any bearer/token rotation or remediation must be synchronized with Super Signals and performed in a controlled window with rollback. Never expose credential values in Memory, logs or chat.

### 6. Historical secret-remediation caution

Deleting a file in a later commit does not erase Git history. Any history rewrite must be deliberate and must not casually rewrite protected production history.

## Rule

Do not call AIDY fully healthy until current Provider Context is production verified and a current Super Signals provider signal successfully receives current AIDY context.