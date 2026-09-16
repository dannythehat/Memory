# AIDY — Current State

Last verified: **2026-09-16**

Authoritative repo: `dannythehat/Aidy-Gold-Signals`
Authoritative branch: `main`
Verified source `main` SHA: `bf3bb05ca5a9320e31173bbd93f41cf797b6ed51`
Live Worker: `aidy-signals-test`

## Current production status — RED / degraded

AIDY market capture is currently running and fresh, but Provider Context is stale.

Latest verified Worker health reported:

- runtime: `cloudflare-workers`
- scheduler: `direct-cron`
- `capture_enabled=true`
- market source: `twelve_data`
- market ownership: `public_independent`
- `formal_forward_enabled=false`
- private-forward model gateway configured: true
- latest scheduled capture success: `2026-09-16T16:32:10.588999+00:00`
- capture-success lag at check: 209 seconds

The active health failure is:

`stale_provider_context`

Reason:

`market capture is fresh but complete Provider Context is stale or missing`

Latest accepted Provider Context snapshot:

`2026-09-15T20:57:36.761999+00:00`

Provider Context lag at the check was 70,683 seconds. Super Signals is therefore correctly rejecting stale AIDY joins with `pit_context_stale` / `AidyContextTerminalMiss`.

Do not describe AIDY as fully healthy until current Provider Context is production verified.

## Recovery already built — PR #133

Open PR #133:

`Keep Provider Intelligence alive when only D1 context is missing`

Head SHA:

`06ffdc8dc87c8aba8e521b237e181121fbd82cfd`

It allows Provider Intelligence to use a fresh scheduled partial snapshot only when M1/M5/M15/H1/H4 are present and D1 alone is missing. The packet explicitly remains observational only. Formal-forward AIDY still requires a complete snapshot.

External exact-head acceptance on Render passed:

- 17/17 focused tests
- 1270/1270 full repository tests
- Ruff passed
- compile passed

PR #133 is still unmerged. Therefore this recovery is **ENGINEERING PROVEN but not PRODUCTION VERIFIED**.

## GitHub Actions constraint

The two required AIDY `main` checks are not executing normal runner work. Recent failed attempts showed 0 ms Ubuntu runner execution. The owner has confirmed GitHub Actions credits are exhausted for approximately one week.

Do not keep rerunning unavailable Actions jobs. AIDY runtime continuity must not depend on GitHub Actions.

During this temporary outage, use trusted external exact-SHA acceptance and preserve branch-protection intent. If a temporary required-check adjustment is necessary for this exact recovery, change only the unavailable check requirement, record the original ruleset, and restore it when Actions credits return.

## Exact immediate recovery step

1. Revalidate the exact current PR #133 head outside GitHub Actions.
2. Merge #133 without weakening unrelated `main` protections.
3. Deploy the canonical Worker while preserving `* * * * *` direct Cron, capture ON, Twelve Data/public-independent ownership and formal-forward OFF.
4. Verify the Cloudflare schedule after deployment.
5. Verify `/health` no longer reports stale Provider Context.
6. Verify a current Super Signals provider signal receives current AIDY context instead of `pit_context_stale`.

## New central product direction — decision intelligence

Once Provider Context is healthy, AIDY should begin producing a shadow decision for every eligible Super Signals provider trade.

Target decision classes:

- `APPROVE`
- `DENY`
- `HOLD/NO_SECOND_ENTRY`
- `CONFLICT_DENY`
- `CLOSE_EARLY`
- `CONTINUE`

The target pipeline is:

`provider signal -> PIT-safe market context -> provider history -> current exposure -> AIDY decision -> action -> outcome -> counterfactual score -> learning`

AIDY must not merely sound intelligent. It must prove whether its intervention made or saved money versus the fixed baseline that would otherwise have occurred.

## Mandatory next capabilities

### Decision Ledger
Persist the exact evidence available at decision time: provider/signal identity, message ancestry, timestamps, AIDY snapshot IDs/digests, provider statistics then available, open exposure, duplicate/conflict cluster, decision/reasons, model/rules version and resulting action.

Future information must never be written back into the original decision state.

### Counterfactual scoring
Score each approve/deny/close/continue decision against a fixed baseline. Persist factual decision delta: money made/saved or money lost because AIDY intervened.

### Conditional provider intelligence
Measure providers by more than overall P&L: BUY versus SELL, session/time of day, weekday, regime/volatility/liquidity conditions, TP progression, management quality, duplicate/repost behaviour, latency/slippage sensitivity, provider agreement/conflict, adverse duration and recovery/re-entry behaviour.

If evidence is weak, the answer is `unknown`.

### Hypothesis/question registry
Persist each question with an exact cohort/filter, required features, metric, minimum sample, current sample size, answer/status, uncertainty, calculation timestamp, supporting records and observational-versus-decision eligibility.

### Duplicate/conflict engine
Identify whether a proposed trade is already represented, merely an edit/repost, a materially equivalent same-direction exposure addition, opposite exposure, or a genuinely independent idea.

## Authority graduation

The owner wants AIDY making smart trading decisions soon, but authority must be graduated by evidence rather than switched on wholesale.

Likely sequence:

1. deterministic duplicate rejection
2. obvious duplicate/conflicting exposure controls
3. provider/regime denies
4. early-close management
5. broader approve/deny/management authority

Each authority class requires an audit trail, kill switch, prospective evidence and explicit owner/live gate. The current live risk directive must not silently change.

## Session rule

Read the 16 September handover first, then verify the current AIDY repo, Worker health and Super Signals production state. Source/runtime truth overrides Memory if it has advanced.