# AIDY — Roadmap

> **2026-09-19 strategic update:** the approved end-to-end build is now
> [`MASTER_GOLD_INTELLIGENCE_BUILD.md`](MASTER_GOLD_INTELLIGENCE_BUILD.md).
> That document is authoritative for the next intelligence phase. The older phased roadmap
> below remains useful historical/build context but must not be read as limiting the new
> Gold-market, news, liquidity, calibration, profit-extraction and self-critique work.

Current roadmap verified against source/runtime on **2026-09-16**.

## Immediate gate — restore healthy Provider Context

AIDY market capture is running, but Provider Context is stale. No later decision-intelligence milestone can be called production-ready until current Provider Context is restored and Super Signals receives fresh context instead of `pit_context_stale`.

Recovery path:

1. externally revalidate exact PR #133 head `06ffdc8dc87c8aba8e521b237e181121fbd82cfd`;
2. merge #133 while preserving unrelated `main` protections despite the temporary GitHub Actions credit outage;
3. deploy the canonical Worker while preserving `* * * * *` direct Cron, capture ON, Twelve Data/public-independent ownership and formal-forward OFF;
4. verify Cloudflare schedules and `/health`;
5. verify a current Super Signals provider signal receives current AIDY context.

## Strategic destination

AIDY is intended to become an evidence-scored Gold/XAUUSD decision system, not merely a Telegram parser or provider ranking dashboard.

Target capability:

`provider signal -> PIT-safe Gold context -> provider history -> current exposure -> AIDY decision -> action -> outcome -> counterfactual score -> learning`

AIDY should eventually be able to:

- approve a provider trade;
- deny a provider trade;
- block a duplicate or materially equivalent second entry;
- reject/resolve a conflicting position when justified by evidence;
- close a trade early when factual post-entry evidence supports that choice;
- explicitly continue/hold when intervention is not justified.

## Phase 1 — shadow decision for every eligible trade

As soon as Provider Context is healthy, persist an AIDY shadow decision for every eligible Super Signals trade, even while the existing execution rules remain authoritative.

Required Decision Ledger fields include:

- immutable signal/provider/message identity and ancestry;
- signal and decision timestamps;
- exact AIDY snapshot/context IDs and digests available at decision time;
- provider evidence available at decision time;
- current open exposure and duplicate/conflict cluster;
- decision class and reasons;
- confidence/uncertainty;
- model/rules version;
- resulting broker action when authority exists.

Future information must never rewrite the original decision state.

## Phase 2 — counterfactual outcome engine

Every decision must later be compared with a fixed baseline.

Examples:

- deny -> what would the provider trade have done if followed normally?
- early close -> compare AIDY close P&L with original provider-management outcome;
- approve -> score realised P&L, MFE/MAE, TP progression and management quality.

Persist `decision_delta` so AIDY can be judged by actual money made/saved or money lost versus baseline.

## Phase 3 — conditional provider intelligence

Build provider evidence by conditional cohort rather than one overall win rate.

Required study areas include:

- BUY vs SELL;
- Asia/London/New York/evening and weekday;
- observable volatility/regime/liquidity conditions;
- small-profit vs runner style;
- TP1/TP2/TP3 progression;
- original-call quality vs provider management quality;
- effect of provider BE/SL/close/cancel instructions;
- edit/repost/duplicate behaviour;
- latency/slippage sensitivity;
- provider agreement/conflict;
- stop-width and entry-distance sensitivity;
- adverse duration after 5/10/20/30 minutes;
- recovery/re-entry behaviour;
- provider-regime specialisation.

Where sample/evidence is insufficient, answer `unknown`.

## Phase 4 — hypothesis/question registry

Maintain a persistent registry for each research question with:

- stable question ID;
- plain-English question;
- exact cohort/filter;
- required factual features;
- metric;
- minimum observations;
- current sample size;
- answer/status;
- uncertainty/confidence;
- last-calculated timestamp;
- supporting trade/decision IDs;
- observational-only vs decision-eligible status.

Retrospective findings do not automatically become decision rules. Freeze the rule definition and validate it prospectively.

## Phase 5 — duplicate/conflict engine

Create canonical exposure clusters using symbol, direction, entry/stop vicinity, provider, message ancestry, timestamp, current broker exposure and cross-provider agreement/conflict.

AIDY must distinguish:

- already represented exposure;
- edit/repost of an existing idea;
- materially equivalent same-direction risk addition;
- opposite exposure;
- genuinely independent trade idea.

When evidence cannot justify choosing between conflicts, fail safely rather than invent certainty.

## Phase 6 — graduated authority

Grant authority by decision class, not wholesale.

Likely sequence:

1. deterministic duplicate rejection;
2. obvious duplicate/conflicting exposure controls;
3. provider/regime denies;
4. early-close management;
5. broader approve/deny/management authority.

Every authority class requires:

- explicit enable/disable control;
- immutable audit trail;
- prospective evidence;
- rollback/kill switch;
- explicit owner/live gate;
- no silent change to the existing Super Signals risk directive.

## Supporting visibility — AIDY Data Hub

The Data Hub remains useful as the owner/admin view, but it is now a supporting surface rather than the central next milestone. It should expose the Decision Ledger, counterfactual decision delta, provider conditional evidence, hypothesis registry, duplicate/conflict state, AIDY market thesis and system health from stored state without invoking expensive external calls merely because the page refreshes.

## Existing building blocks — verified 2026-09-16, do not rebuild these

A repo-overlap check before starting Phases 1-4 found real, working infrastructure that
already covers large parts of them. Build on these; do not start a parallel system.

**Phase 1 (Decision Ledger) — the raw evidence spine already exists in Super Signals.**
`provider_trade_observations` (migration `0081`, `services/api/app/ai_message_pipeline.py`)
already records signal/provider/message identity, revision index, observed_at, the
decision the interpreter reached, and every extracted field -- for every message,
executable or not, 3,894+ rows. A Decision Ledger is this table plus a new
`aidy_decisions` table keyed on `observation_id`, carrying AIDY's decision class,
reasons, confidence, snapshot/context digest and model version -- not a new evidence
capture path.

**Phase 2 (counterfactual scoring) — built and live today, same benchmark.**
`services/api/app/provider_trade_scorer.py` + `provider_trade_scoring_runner.py` +
`provider_trade_scores` table already replay a trade against retrospective AIDY M1
bars using the live resolver's own `replay_bars`, and record realised P&L, R-multiple,
outcome class. This is Phase 2's engine for the "approve" case (what actually happened).
What Phase 2 adds on top: a *baseline* replay (what the provider's own plan would have
done, unmodified) to diff against for the "deny"/"early close" cases -- the existing
scorer already has every primitive needed (geometry parsing, intrabar conventions,
management-not-modelled caveat) to build that baseline replay as a second entry point
into the same module, not a new one.

**Phase 3 (conditional provider intelligence) — the aggregation layer is live.**
`provider_trade_scoreboard` (migration `0087`) already carries win rate, net P&L,
avg P&L, `scored_coverage_pct` and `update_rate_pct` per provider. It is currently
un-conditioned (one row per provider). Phase 3 is adding `GROUP BY` dimensions
(side, session, weekday) to the same underlying query pattern, not a new pipeline.
`provider_day14_governance.py` (Super Signals) already has the exact
learning -> shadow -> qualified state machine with fail-closed promotion thresholds
that Phase 6's "graduate authority by class" needs -- it is scoped to promoting a
*provider* today; the same pattern (immutable version, explicit owner approval,
out-of-sample evaluation) is what a hypothesis/decision-class promotion needs too.

**Phase 5 (duplicate/conflict engine) — partially built, not cross-provider yet.**
`canonical_signal_ledger.py` already collapses exact same-source duplicate geometry
within a symmetric time window around provider post time (handles the "concise
signal + analysis companion" and "delayed edit vs already-corrected repost" cases).
`signal_events.py` (Day 18) enforces revision-0-only signal creation as a second
duplicate guard. `provider_day18_combined_book.py` already models book-level BUY+SELL
coexistence and only permits literal hedging when a read-only MT5 observation proves
hedging mode -- this is most of the "do we already hold the opposite direction"
check. What's missing for Phase 5: **cross-provider** clustering (two different
groups posting the same directional idea), which none of the above do -- they are
all same-source or same-account. That's the one genuinely new component here.

**Phase 4 (hypothesis registry) — not found. This is the one clean net-new build.**
No existing table or module tracks a question/hypothesis with sample size, confidence
and promotion status. Build this as a thin table over the Phase 3 aggregation queries
(each registry row names a `provider_trade_scoreboard`-style query plus its cohort
filter), not as a separate analytics system.

## Rule

Engineering completion is not statistical validation. AIDY earns decision authority through prospective evidence. Formal-forward/live-money authority remains OFF until explicitly graduated.