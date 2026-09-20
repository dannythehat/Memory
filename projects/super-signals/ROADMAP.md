# Super Signals — Roadmap

Current roadmap verified against production/source state on **2026-09-16**.

## Immediate blocker — AIDY Provider Context health

Super Signals is production-live on SHA `d3f3f8898ff85c3235875bd298d51066f0f5a82e` with continuous AIDY probing and a one-minute Provider Lab supervisor.

The remaining blocker is upstream AIDY Provider Context. Market capture is fresh, but current provider signals still encounter stale AIDY context. AIDY PR #133 is the recovery path and has passed external exact-head acceptance, but is not yet production verified.

Do not begin claiming AIDY decision intelligence is live until a current provider signal receives current AIDY context in production.

## Weekend gated intelligence modules — active 2026-09-19

- **Build 1 — Historical Time Machine:** ENGINEERING/PRODUCTION VERIFIED. 103 development + 19 validation cases completed under strict PIT replay; 18-case holdout remains sealed. This validates the exam infrastructure, not trading edge.
- **Build 2 — News/Event + Liquidity/Execution:** ENGINEERING/PRODUCTION VERIFIED. 103 development + 19 validation cases completed under strict PIT replay; 18-case holdout remains sealed. Evidence plumbing passed, no trading-edge claim.
- **Build 3 — Provider Conditional-Alpha + Historical Analogue:** NEXT. Reuse existing Day 13 preregistered conditional-alpha engine; add the historical-analogue decision surface.
- **Build 4 — Probability/EV + Trade Management/Profit Extraction:** locked behind Build 3.
- **Build 5 — Failure Attribution/UNKNOWN + AIDY self-critique/judging:** locked behind Build 4.

Every build uses the same gate: build -> tests/exam -> fix until clean -> PR/merge -> runtime evidence where applicable -> Memory update/validation/merge/re-read -> next build.

## Strategic destination

AIDY is not intended to remain a Telegram parser or provider-ranking system. Providers are training/evidence inputs. The destination is an evidence-scored Gold/XAUUSD decision system that can:

1. understand what Gold is doing now and why;
2. form its own directional/market thesis;
3. judge provider trades rather than simply copy them;
4. approve or deny trades using factual evidence;
5. prevent duplicate or conflicting exposure;
6. decide when early exit is better than continuing;
7. score each decision against what would otherwise have happened;
8. learn which providers are trustworthy under which conditions;
9. eventually manage broader live decisions only after prospective validation and explicit owner approval.

The current 1% live-risk directive remains unchanged unless explicitly changed.

## Phase 1 — shadow AIDY decision for every eligible trade

Start immediately after AIDY Provider Context is healthy.

For every eligible provider trade, persist one immutable AIDY decision:

- `APPROVE`
- `DENY`
- `HOLD/NO_SECOND_ENTRY`
- `CONFLICT_DENY`
- `CLOSE_EARLY`
- `CONTINUE`

The decision must freeze the exact facts known at that moment.

### Decision Ledger minimum evidence

- provider/signal identity
- original Telegram message/revision ancestry
- signal timestamp
- AIDY decision timestamp
- exact AIDY context/snapshot IDs and digests
- provider statistics available then
- open account/exposure state
- duplicate/conflict cluster state
- decision and reasons
- confidence/uncertainty
- model/rules version
- broker action/result when authority exists

No future information may rewrite the original decision state.

## Phase 2 — counterfactual scoring

Every decision must later be judged against a fixed baseline.

Examples:

- deny -> compare against following the provider normally;
- close early -> compare against the provider's original management path;
- approve -> score realised P&L, MFE/MAE, TP progression and management quality.

Persist a factual `decision_delta`:

`AIDY outcome - baseline outcome`

This answers the business question: did AIDY make/save money, or did it cost money?

Do not label a loss as saved unless the baseline path actually demonstrates that loss.

## Phase 3 — conditional provider intelligence

A provider is not simply good or bad. Build provider evidence by condition.

Required dimensions include:

- BUY vs SELL;
- Asia/London/New York/evening and weekday;
- observable volatility/regime/liquidity conditions;
- TP1/TP2/TP3 progression;
- small-profit versus runner style;
- original-call quality versus management quality;
- effect of provider close/BE/SL/cancel instructions;
- edit/repost/duplicate behaviour;
- latency and slippage sensitivity;
- provider agreement and conflict;
- stop-width and entry-distance sensitivity;
- adverse duration after 5/10/20/30 minutes;
- recovery/re-entry behaviour;
- provider-regime specialisation.

Where sample/evidence is insufficient, answer `unknown`.

## Phase 4 — persistent AIDY question/hypothesis registry

Each research question must have:

- stable question ID;
- plain-English question;
- exact cohort/filter definition;
- required factual features;
- metric;
- minimum observations;
- current sample size;
- answer/status;
- uncertainty/confidence;
- last-calculated timestamp;
- supporting trade/decision IDs;
- observational-only versus decision-eligible status.

Retrospective findings do not automatically become authority. Freeze the definition and test prospectively.

## Phase 5 — duplicate/conflict exposure engine

This is a high-priority risk-control build.

Create canonical exposure clusters using:

- symbol;
- direction;
- entry vicinity;
- stop vicinity;
- provider;
- message ancestry/edit/reply relationships;
- timestamp;
- current broker exposure;
- cross-provider agreement/conflict.

AIDY must know whether a proposed trade is already represented, an edit/repost, a materially equivalent same-direction risk addition, opposite exposure or genuinely independent.

If evidence is insufficient to choose between conflicting exposures, fail safely and flag it.

## Phase 6 — graduated authority

Do not switch broad AIDY control on at once.

Likely graduation order:

1. deterministic duplicate rejection;
2. obvious duplicate/conflicting exposure controls;
3. provider/regime denies;
4. early-close management;
5. broader approve/deny/management authority.

Every authority class requires:

- explicit enable/disable control;
- immutable audit trail;
- prospective evidence;
- kill switch/rollback;
- explicit owner/live gate;
- no silent change to the 1% live-risk directive.

## Supporting owner surface — AIDY Data Hub

The Data Hub remains valuable, but it is a supporting visibility layer rather than the central next milestone.

It should read stored database/current state rather than invoke OpenAI or MetaAPI simply because a browser refreshes.

The Hub should expose:

- AIDY health and context freshness;
- current Gold thesis/regime/watch conditions;
- Decision Ledger entries;
- factual decision delta;
- provider conditional performance;
- hypothesis/question state;
- duplicate/conflict exposure state;
- provider fingerprints/drift/governance;
- system and owner-attention alerts.

## Existing Provider Intelligence foundation

The previously built A-F foundation remains useful and should be reused rather than rebuilt:

- PIT-safe context join
- provider fingerprints
- research governance
- provider-specific adaptation
- combined-book conflict observation
- append-only provider intelligence persistence

The next work must extend those foundations into actual decision evidence rather than creating another disconnected subsystem.

## Operational rule while GitHub Actions credits are exhausted

GitHub Actions is temporarily unavailable due to exhausted credits for approximately one week. Do not make runtime continuity depend on Actions and do not repeatedly rerun jobs that cannot obtain a runner.

Use trusted external exact-SHA acceptance where necessary, preserve branch-protection intent and restore normal required-check operation when Actions credits return.

## Success metric

AIDY succeeds only if prospective evidence shows that its decisions improve Super Signals versus following providers unchanged.

Track factual decision delta by decision type, provider, direction, session and market regime.