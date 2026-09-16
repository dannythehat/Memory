# Super Signals Handover — 16 September 2026

## Scope

This handover records the current Super Signals production state around AIDY, the reliability changes deployed today, the upstream AIDY Provider Context blocker, and the owner's directive to make AIDY an evidence-scored decision layer for Super Signals rather than a passive dashboard/research sidecar.

## Verified production state

Repo: `dannythehat/super-signals`

Deployed branch:

`feature/day-10-shared-telegram-sources`

Verified branch/deploy SHA:

`d3f3f8898ff85c3235875bd298d51066f0f5a82e`

Render service:

`super-signals-day-8` (`srv-d9qmcgks728c73a555m0`)

Live deploy:

`dep-dalblphm57gc73d7cta0`

Deploy status: `live`

Production build gate at that SHA:

- 989 passed
- 93 skipped
- 0 failed
- 2 warnings

## AIDY runtime hardening deployed in Super Signals

Super Signals now keeps AIDY Provider Context health probing armed rather than stopping checks after the first successful response.

A one-minute application-owned supervisor also watches the AIDY Provider Lab task and can restart that task if it unexpectedly stops during the trading week. The existing weekend market freeze remains respected.

This is a Super Signals runtime reliability layer. It does not grant AIDY broker/live-money authority.

## Current blocker is upstream AIDY context, not Super Signals capture

After the live deploy, Super Signals continued logging:

`AIDY Provider Context live probe NOT_READY error=AidyContextTerminalMiss`

The upstream AIDY Worker was independently checked and its market capture was fresh, but its Provider Context snapshot remained stale. Current Super Signals signals therefore continued to encounter `pit_context_stale` rather than receiving current AIDY context.

The AIDY recovery is tracked in the AIDY handover dated 16 September 2026 and open AIDY PR #133.

## GitHub Actions constraint

The owner confirmed that GitHub Actions credits are exhausted for approximately one week. Do not design AIDY runtime continuity around GitHub Actions and do not waste time repeatedly rerunning unavailable CI.

AIDY and Super Signals production runtimes must continue independently of CI availability. Use trusted external exact-SHA acceptance where necessary during this temporary Actions outage and preserve normal protection intent.

## Owner directive — AIDY becomes a decision layer

The strategic destination is now more concrete.

Once current AIDY context is healthy, Super Signals should begin obtaining a shadow AIDY decision for every eligible provider trade and persist the complete decision evidence.

Target decisions:

- approve
- deny
- hold/no second entry
- conflict deny
- close early
- continue

These decisions must be based on PIT-safe facts available at decision time, never hindsight.

## Required decision evidence

For every eligible signal persist an immutable Decision Ledger entry containing:

- signal/provider identity
- original Telegram evidence/revision ancestry
- signal and AIDY decision timestamps
- exact AIDY context/snapshot IDs and digests
- provider statistics available at that instant
- current account/open-exposure state
- duplicate/conflict cluster state
- decision/reasons/confidence
- model/rules version
- broker action/result if authority existed

The decision record must never be rewritten later with future information.

## Counterfactual scoring

Every decision must later be judged against a fixed baseline.

Examples:

- AIDY deny -> compare with the trade if provider instructions had been followed normally
- AIDY early close -> compare the early close with the original provider-management outcome
- AIDY approve -> record realised P&L, MFE/MAE, TP progression and management quality

Persist a factual `decision_delta` so the owner can answer: did AIDY actually make/save money, or did it cost money?

No avoided loss may be claimed unless the baseline path demonstrates the loss.

## Provider intelligence must be conditional, not just provider-wide

Build evidence that can answer, where sample sizes are sufficient:

- BUY versus SELL quality by provider
- session/time-of-day/weekday differences
- performance by volatility/regime/liquidity conditions based on observable facts
- small-profit versus large-runner style
- TP progression patterns
- provider initial-call quality versus management quality
- whether provider close/BE/SL messages improve outcomes
- edit/repost/duplicate habits
- latency and slippage sensitivity
- performance during provider agreement versus conflict
- stop/entry geometry sensitivity
- adverse-duration behaviour after 5/10/20/30 minutes
- recovery/re-entry behaviour
- provider-regime specialisation

If evidence is insufficient, return `unknown` rather than a made-up conclusion.

## AIDY questions/hypothesis registry

Create a persistent research-question registry with a stable ID, exact cohort/filter, required features, metric, minimum sample, current sample size, answer/status, uncertainty, last-calculated timestamp, supporting trade/decision IDs and whether the finding is observational only or decision-eligible.

Retrospective discoveries must not silently become live rules. Freeze a rule definition and then evaluate it prospectively before authority is granted.

## Duplicate and conflict control — high priority

Super Signals must stop blindly multiplying the same idea when Telegram produces repeats, edits or materially equivalent cross-provider trades.

Build canonical exposure clusters using:

- symbol
- direction
- entry vicinity
- stop vicinity
- provider
- message ancestry/edit/reply relationships
- timestamp
- current broker exposure
- cross-provider agreement/conflict

AIDY should explicitly know whether a proposed trade is already represented, a duplicate/repost, an equivalent same-direction risk addition, opposite exposure, or a genuinely independent idea.

Where evidence is insufficient to choose between conflicting trades, fail safely and flag the situation rather than invent certainty.

## Rollout rule

Do not grant broad live authority in one step.

Start with shadow decisions for every eligible trade and continuously score them.

Graduate decision classes separately, likely beginning with deterministic duplicate rejection, then clear exposure conflicts, then provider/regime denies, then early-close management.

Every authority class must have:

- explicit enable/disable control
- immutable audit trail
- prospective evidence
- rollback/kill switch
- no silent change to the existing 1% risk directive

## North-star metric

AIDY succeeds when it measurably improves Super Signals compared with following providers unchanged.

Track the factual decision delta by decision class, provider, direction, session and market regime. That is the core proof of whether AIDY is becoming smarter and more profitable rather than merely more complicated.
