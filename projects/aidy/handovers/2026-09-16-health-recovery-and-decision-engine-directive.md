# AIDY Handover — 16 September 2026

## Why this exists

This handover records the current AIDY production-health blocker, the GitHub Actions constraint, the already-tested recovery path, and the owner's next-stage product directive: AIDY must progress from passive Provider Intelligence into an evidence-scored trading decision engine.

## Verified production state

Authoritative repo: `dannythehat/Aidy-Gold-Signals`

Authoritative `main` SHA checked on 16 September 2026:

`bf3bb05ca5a9320e31173bbd93f41cf797b6ed51`

Live Worker health check reported:

- runtime: `cloudflare-workers`
- service: `aidy-signals`
- scheduler: `direct-cron`
- `capture_enabled=true`
- market source: `twelve_data`
- market ownership: `public_independent`
- `formal_forward_enabled=false`
- private-forward model gateway configured: true

Market capture itself was healthy. At the health check the latest scheduled capture success was:

`2026-09-16T16:32:10.588999+00:00`

with a capture-success lag of 209 seconds.

AIDY was nevertheless `degraded` because Provider Context was stale. The health reason was:

`market capture is fresh but complete Provider Context is stale or missing`

Health code:

`stale_provider_context`

Latest accepted Provider Context snapshot:

`2026-09-15T20:57:36.761999+00:00`

Provider Context lag at the check was 70,683 seconds. Super Signals therefore continued receiving `pit_context_stale` / `AidyContextTerminalMiss` rather than current AIDY context.

## Recovery code already built

Open PR #133:

`Keep Provider Intelligence alive when only D1 context is missing`

Head:

`06ffdc8dc87c8aba8e521b237e181121fbd82cfd`

The change allows Provider Intelligence to consume a fresh scheduled partial snapshot only when M1/M5/M15/H1/H4 are present and D1 alone is missing. It records the degraded evidence boundary explicitly and keeps the read path observational only. Formal-forward AIDY continues to require a complete snapshot.

Exact PR #133 head was externally validated on Render:

- focused provider-context tests: 17/17 passed
- full repository suite: 1270/1270 passed
- Ruff: passed
- compilation: passed

This is engineering evidence, not proof that the fix is production-live. PR #133 is still unmerged at the time of this handover.

## GitHub Actions constraint

The two required checks on AIDY `main` are:

- `Evidence Semantic Change Gate / classify-protected-diff`
- `AIDY Day 53 Twelve Data OHLC Adapter / acceptance`

Observed failed attempts consumed 0 ms of Ubuntu runner execution and stopped before normal job execution. The owner has confirmed that GitHub Actions credits are exhausted for approximately one week.

Do not waste time repeatedly rerunning unavailable GitHub Actions during this period.

## Exact recovery sequence for the next agent

1. Revalidate the exact current PR #133 head outside GitHub Actions.
2. Preserve a record of the existing `main` protection/ruleset.
3. If required to merge while Actions is unavailable, remove/bypass only the unavailable required-check requirement needed for this exact externally validated recovery. Do not weaken unrelated PR, deletion or force-push protections.
4. Merge PR #133 only after exact-head external acceptance is reconfirmed.
5. Deploy the canonical Worker while preserving `* * * * *` direct-Cron capture, `capture_enabled=true`, Twelve Data/public-independent market ownership and `AIDY_FORMAL_FORWARD_ENABLED=false`.
6. Verify Cloudflare schedule state after deploy, not only local config.
7. Verify `/health` is no longer stale on Provider Context.
8. Verify a current Super Signals provider signal receives current AIDY context instead of `pit_context_stale`.
9. Restore the exact required-check protection when GitHub Actions becomes available again.

Do not call this recovery GREEN until those production checks are complete.

## Owner product directive — now central

After months of AIDY and Super Signals work, the owner wants AIDY to become measurably useful in trading decisions very soon.

The target flow is:

`provider signal -> PIT-safe market context -> provider history -> current exposure -> AIDY decision -> broker action -> outcome -> counterfactual score -> learning`

AIDY must be built toward explicit decision classes:

- `APPROVE` — allow the provider trade
- `DENY` — reject the trade when evidence says the expected outcome is poor
- `HOLD/NO_SECOND_ENTRY` — prevent duplicate or materially equivalent exposure
- `CONFLICT_DENY` — prevent or resolve conflicting positions when justified by evidence
- `CLOSE_EARLY` — close an existing trade when factual post-entry evidence makes continuation inferior
- `CONTINUE` — explicitly avoid interfering when the evidence does not justify intervention

This directive does not mean uncontrolled model discretion. Each authority class must be separately proven and graduated.

## Mandatory Decision Ledger

Every AIDY decision must become an immutable research record containing at least:

- signal/provider identity and immutable message evidence
- signal and decision timestamps
- decision class
- exact AIDY market/context snapshot IDs and digests available at decision time
- provider statistics actually available at decision time
- open exposure and duplicate/conflict cluster state
- factual reasons and confidence/uncertainty
- model/rules version
- broker action, if any

No hindsight data may be written back into the original decision state.

## Mandatory counterfactual scoring

AIDY must later be scored against the fixed baseline that would otherwise have happened.

Examples:

- denied trade: compare against the provider trade followed normally
- early close: compare actual AIDY close P&L against the original provider management path
- approved trade: score realised P&L plus MFE/MAE, TP progression and management quality

Persist a factual decision delta, e.g. money made/saved or money lost because AIDY intervened. Do not count a saved loss unless the baseline path proves the loss.

## Provider Intelligence questions AIDY must answer from data

The system must move beyond a single provider win rate. It should continuously test and answer questions such as:

- provider BUY vs SELL performance
- performance by Asia/London/New York/evening session and weekday
- performance by observable volatility/regime/liquidity conditions
- providers that take many small profits versus fewer larger winners
- TP1/TP2/TP3 progression quality
- whether a provider's own management messages improve or damage outcomes
- original-call quality versus management quality
- duplicate/repost/edit behaviour
- latency/slippage sensitivity
- performance when providers agree or conflict
- stop-width/entry-distance sensitivity
- outcome after being adverse for 5/10/20/30 minutes
- recovery/re-entry quality
- provider-regime specialisation

Where evidence is weak the answer must be `unknown`, not a confident narrative.

## Persistent hypothesis/question registry

Build a durable registry with:

- `question_id`
- plain-English question
- exact cohort/filter
- required factual features
- metric
- minimum sample
- current sample size
- answer/status
- uncertainty/confidence
- calculation timestamp
- supporting trade/decision IDs
- observational-only versus decision-eligible status

Findings discovered retrospectively do not immediately become decision rules. Promote a finding only after its definition is frozen and then test it prospectively.

## Duplicate/conflict engine priority

AIDY must know whether a proposed trade is:

- already represented by an open equivalent trade
- merely an edit/repost of an existing idea
- a same-direction cross-provider cluster that would multiply risk
- opposite existing exposure
- a genuine independent idea

Use canonical exposure clusters based on symbol, direction, entry/stop vicinity, provider, message ancestry, timestamp and current broker exposure.

If evidence is insufficient to choose between conflicting exposures, fail safely rather than pretending certainty.

## Authority graduation

Once Provider Context is healthy, start producing an AIDY shadow decision for every eligible Super Signals trade immediately and score those decisions prospectively.

Graduate authority classes separately. Likely order:

1. deterministic duplicate rejection
2. obvious duplicate/conflicting exposure controls
3. provider/regime denies
4. early-close management
5. broader approve/deny/management authority

Every authority requires a kill switch and audit trail.

## Success definition

The key business question is not whether AIDY sounds intelligent. It is whether, prospectively and without hindsight, AIDY improves Super Signals versus following providers unchanged.

The durable metric is factual decision delta: how much money AIDY made, saved or cost versus the fixed baseline, segmented by decision type, provider, direction, session and regime.
