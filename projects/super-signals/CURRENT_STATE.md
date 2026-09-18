# Super Signals — Current State

> **Owner mandate in force since 2026-09-17: read [`OWNER_MANDATE.md`](../../OWNER_MANDATE.md) every session.** It sets the goal (AIDY becomes an evidence-scored decision layer that measurably improves Super Signals' profit) and the one boundary that does not move under it (live-money authority stays OFF until explicitly graduated per class).

Last verified: **2026-09-18**

Authoritative repo: `dannythehat/super-signals`
Authoritative deployed branch: `feature/day-10-shared-telegram-sources`
Verified source/deploy SHA: `d52c0241c6a134cbcbfd8b837ca043127372be44`
Render service: `super-signals-day-8` (`srv-d9qmcgks728c73a555m0`)
Verified live deploy: `dep-dambc90ae00c73ajkq0g`
Deploy status: **healthy, migration 0096 applied** (verified directly against production Postgres + `/health` 200, instance stable)
Quality gate at deployed SHA: **989 passed, 93 skipped, 0 failed, 2 warnings** (this is the last full-suite baseline, NOT re-run this session -- only targeted suites touching changed files were re-verified this pass, all green against real local Postgres; GitHub Actions remains credit-exhausted, same no-runner-executed signature diagnosed earlier, not a real failure).

## TIG management-reliability fix, 6 providers switched on for paper trading (2026-09-17/18)

Root-caused and fixed the real reason management instructions could go unmanaged: a stuck trade_update dispatch failure was never retried and never escalated. Built `ManagementReliabilityRuntime` (retry + fail-safe force-close) and fixed the dominant false-failure mode in `AiLifecycleBridge._resolve_signal` (92% of 278 sampled real failures were benign "already closed by another path" no-ops, not broken links). Switched 6 shadow providers (incl. TIG's Asia Trades) to `testing` status, each restricted to its own best-evidenced side via `provider_execution_probation` until graduated. Found and fixed two self-inflicted production bugs from this same work (a `jsonb_build_object` bare-param typing bug, a `:param::interval` SQLAlchemy `text()` adjacency bug) -- both now documented as a recurring pitfall. Overnight audit (owner-requested) confirmed real trades executed, zero messages left undecided despite an unrelated Render billing-lapse restart loop, and all apparent failures were benign. PRs 191, 193, 194, 195, 196. Full detail: `LIVE_STATE.json` -> `management_reliability_and_tig_paper_trading_v1`.

## Probation side/session gate fixed, GOLDHUNTER graduated fully including live money (2026-09-18)

Owner: "we are leaving loads of profits on the table." Investigated GOLDHUNTER specifically (79.1% win rate, 43 resolved trades, both sides individually well past the cohort floor) and found the real bug: the fingerprint's `cohort_sample_met` required both an adequate *side* split and an adequate *session* split before probation eligibility would ever pass, but eligibility only ever needs the side answer -- GOLDHUNTER's trades cluster into one dominant session, so the unrelated session half silently vetoed every trade. Split into independent `side_sample_met`/`session_sample_met` (PR 197) -- unblocked GOLDHUNTER plus 3 other providers with the same latent bug. Owner then explicitly asked to graduate GOLDHUNTER fully off probation, including real member live-money eligibility, not just paper (PR 198) -- offered the narrower paper-only option first and explained the tradeoff; owner chose full graduation with under an hour of real forward history under the corrected gate. **There are 5 connected live MT5 accounts with real trade history already in this system -- this is not a hypothetical switch.** Full detail: `LIVE_STATE.json` -> `provider_probation_side_session_split_and_goldhunter_graduation`.

## AIDY reasoning gets real market context, v1->v2 (2026-09-18)

Owner directly challenged whether AIDY uses any of the data/tools it's been given ("shiny background tool that does nothing"). Real audit found: the reasoning call previously saw only a signal's own entry/stop/TP numbers plus provider history text -- its own system prompt explicitly forbade discussing market conditions. Wired in AIDY's existing, already point-in-time-safe market/regime context (`AidyContextClient` -- real trend direction across M15/H1/H4, session, volatility, event timing) into the reasoning prompt (PR 199). Falls back to no-context reasoning exactly as before when a signal is too old for the context API's bounded lookback window; never blocks the pass. Does not touch `aidy_decision_engine.py` or any execution path -- still `research_only=true` throughout. **Owner has since asked for AIDY to have real-time multi-timeframe candles, a news/economic calendar, on-demand tool-calling access to pull any data it needs, and eventually to generate and score its own trade ideas rather than only judge providers'.** Responded with honest scoping: candle aggregation and tool-calling are buildable now from data already paid for; a calendar needs a new external data-source/credential decision the owner hasn't made; "predict whether price reverses or runs at a level" was declined as framed (nobody reliably does this) in favour of an honest historical-reaction-frequency version; AIDY originating its own trade ideas was flagged as a materially bigger, execution-adjacent system given real money is now live on GOLDHUNTER, and deferred pending explicit owner sign-off on that one piece specifically. Owner's response: "you should build everything." Proceeding with candle aggregation and tool-calling next as the pieces that need no new external dependency. Full detail: `LIVE_STATE.json` -> `aidy_reasoning_market_context_v2`.

## AIDY blind Gold learning exam — in build, research-only (2026-09-17)

Owner explicitly redirected testing away from re-running already-proven Claude decision-ledger checks. New objective: measure whether AIDY actually understands Gold/provider-market relationships and becomes measurably smarter on later unseen data.

AIDY repo PR #135 (`feature/blind-gold-learning-exam-20260917`), latest branch commit recorded here `3492beaf064780469367a28564bef3739aec18e9`, now contains a governed chronological blind scorer plus a PIT-safe bridge from immutable AIDY episode memory and score-eligible forward outcomes. It counts only learning cards available before each episode, excludes same-episode future learning, scores direction/Brier/difficulty where AIDY genuinely emitted the needed ex-ante fields, and reports `insufficient_evidence`, `memory_accumulating`, `learning_candidate`, `learning_observed`, or regression. Memory growth alone can never be labelled learning.

The exam now extracts frozen contemporaneous market context already preserved in episode memory (`regime_state`/`setup_state`): market structure, volatility, liquidity/spread state, session and event state where present. Difficulty is assigned from those frozen features only. Missing context stays unknown and is surfaced through a context-coverage report rather than retrospectively invented. Provider identity/context is likewise not fabricated when absent; provider-conditioned learning needs a PIT-safe join.

**Do not claim AIDY is smarter yet.** PR #135 is open/research-only and the real production/D1 blind scorecard still has to be run with adequate chronological unseen samples. If later batches do not improve, the result must remain memory accumulation/regression. Full handover: `handovers/2026-09-17-aidy-blind-gold-learning-exam.md`.

Safety unchanged: no broker authority, no execution-rule change, 1% live-risk directive unchanged.

## AIDY visibility layer — v1 live, both repos (2026-09-17)

Investigated build item #4 (hypothesis registry) before building it and found it already exists: `provider_conditional_hypotheses`/`_runs`/`_results` (Day 13) -- 15,744 hypotheses preregistered with real Benjamini-Hochberg significance testing and out-of-sample gating, just barely fed (42 of 15,744 ever tested, 0 significant). A "needs more live evidence" problem, not a "needs code" problem -- building a second registry would have duplicated real, more rigorous work. Built the visibility layer instead, at the owner's direction ("keep building, get AIDY ready for launch").

- **Backend** (`dannythehat/super-signals` PR #186): `GET /admin/aidy/overview`, owner/trading_admin gated (`activity.view` permission, same as the existing Day 35 control centre). Returns decision totals, per-class breakdown with net delta and resolution mix, top/bottom cohort standouts (min 15 resolved trades), hypothesis registry status. Read-only, no writes, no broker/OpenAI calls.
- **Frontend** (`dannythehat/super-signals-website` PR #4): **https://smartsignals.site/admin-aidy** (not `/admin/aidy`). Same auth pattern as the existing `/complimentary` page.

## AIDY reasoning engine — v1 live, disabled by default (2026-09-17)

Owner redirect: *"I'm not bothered about the hub yet, I'm more bothered about getting Aidy running and making him smart."* Investigated the deeper question first: why is Day 13's conditional-hypothesis registry (AIDY's actual statistical learning engine, 15,360+ preregistered hypotheses) still basically untested (`tested_hypothesis_count=0` on the latest production run)? Real finding, verified directly against production: it runs on every deploy as designed, but 702 of ~734 candidate shadow-provider signals got a permanent `pit_context_stale` miss (AIDY's own server saying it has no valid historical market snapshot for that exact minute) — all from *before* AIDY's snapshot-cadence recovery already recorded above (`continuous_health_verification`). Zero new misses since 2026-09-16T22:46Z; evidence has been flowing normally since. **This is a genuine wait-for-evidence situation, not a bug** — the historical gap is permanent by the system's own point-in-time-safety design, but it's healthy and self-healing going forward. Given how fine-grained the preregistered cells are (384 per provider, each needing 30+ forward observations both sides), meaningful results here are realistically a multi-month proposition even now that AIDY is healthy. Full detail: `LIVE_STATE.json` → `day13_day14_evidence_starvation_diagnosis`.

Given that, shipped the more direct lever instead: `aidy_decision_engine.py`'s own docstring already said a real model call per signal "is not switched on silently" — so it never had one. **PR #188** (merged `45d49a0d3ed8b3631f81f7c84b71ffe224439a50`) adds `AidyReasoningEngine`: one OpenAI call (same pattern as the existing Telegram message-interpretation supervisor — `gpt-5-mini`, strict JSON schema) per `approve` decision reasoned `insufficient_track_record_evidence` — the exact case where the deterministic engine has nothing left to say. Reads the signal's own entry/stop/target geometry and returns a lean (agree/caution/disagree), confidence and rationale. Purely additive: never changes `aidy_decisions.decision_class`, same `research_only`/no-live-authority contract as every other AIDY table (migration 0090, append-only). **Ships disabled** — `AIDY_REASONING_ENGINE_ENABLED` defaults to `"0"`, so merging started no real spend; an explicit monthly budget gate (soft $120/hard $180, inside the owner's pre-authorized ~€200/month ceiling) is enforced whenever it is turned on. Full detail: `LIVE_STATE.json` → `aidy_reasoning_engine_v1`.

**Live since 2026-09-17T09:55Z** — owner said "Turn it on." Verified directly against production: 15 real annotations written within 90 seconds of restart, $0.0082 spent (~$0.0005/call), 196 more candidates queued to drain over the next several passes. Spot-checked output is genuinely useful, not placeholder text — e.g. correctly flagged `disagree` on a signal whose stop was only 1-6 ticks from entry (undefined reward:risk).

## AIDY reasoning widened + provider fingerprints shipped (2026-09-17)

v1's scope (only `insufficient_track_record_evidence` approvals) meant every provider with an established track record — all 4 real/testing providers included — got zero signal-level reasoning, since win rate alone already cleared the deterministic bar. **PR #189** (merged `e3c26b6961fafe62c09e8f0c69403d10aad2bac5`) widens the reasoning engine to every `approve` decision (real backlog cost checked against production first: ~$1.30 for all 2,598 historical decisions) and speeds up the drain loop to clear the backlog in under an hour. Owner reacted with real alarm to the original $120/$180 monthly cap ("I can't afford $180 per month. Are you insane?") even though it was a ceiling, not a bill — immediately lowered to soft $5 / hard $10/month via Render env vars, still ~50-100x actual observed spend.

Owner then asked directly: does AIDY understand what separates each provider's wins from losses, for every trader, as a permanent running capability, not an ad-hoc query ("We've given aidy a full stack, so he needs to use it"). **PR #190** (merged `6082ed7ec53b5339b26300a10c60f54fd9e16f9c`) adds `ProviderFingerprintEngine`: computes per-provider stop-distance/reward:risk comparisons (winners vs losers) and best/worst side/session, straight from already-resolved trades — no need to wait on new forward evidence the way Day 13 does. Explicitly descriptive, not statistically certified, with honest sample floors (8 resolved per outcome for geometry, 15 per cohort cell) — verified live: GOLDHUNTER's 79.1% win rate correctly got **no** geometry claim (only 7 losses, below the floor) rather than a fabricated pattern. Runs daily, on by default. Critically, **it's actually read**: the reasoning engine now pulls each provider's latest fingerprint into its prompt, so a new signal is judged against that specific provider's own history, not generic rules. Full detail: `LIVE_STATE.json` → `aidy_reasoning_engine_v2_and_provider_fingerprints`.

## Provider coverage — v1 live, both repos (2026-09-17)

Owner asked directly, looking at the new visibility dashboard: *"Why is the skills so low? We have 38 traders no? Why isn't Aidy studying them all?"* Investigated with real production SQL rather than guessing. Finding: AIDY was already deciding on **41 of 63** connected sources (46 have any trade history at all). The dashboard looked thin because its cohort-standouts table requires 15+ resolved trades in one specific side+session+weekday slice (70 possible slices per provider) — almost nothing clears that yet, hiding ~36 of the 41 actively-decided providers. This was a **dashboard display-threshold gap, not a real coverage gap** in what AIDY processes.

Fixed same-session in both repos:
- **Backend** (`dannythehat/super-signals` PR #187, merged `e4ed35bf148a25f257c232e5204ea36e2008c715`): coverage totals + a full blended (non-cohort-sliced) per-provider table added to `GET /admin/aidy/overview`.
- **Frontend** (`dannythehat/super-signals-website` PR #5, merged `9aec4e4f354b60ec80536cbe8120133b8373ba25`): new coverage stat row + "every provider AIDY has decided on" table at **https://smartsignals.site/admin-aidy**. Same PR also fixed a real mobile layout bug the owner caught via phone screenshots ("Bit shit isn't it") — tables were cut off mid-column; now stack as cards below 640px, verified with an actual Playwright screenshot at a 390px viewport, not just a `curl` 200 check.

Real spread confirmed across named providers: net P&L from **-$1,351.26** (TRADE GLOBAL, 36.6% win rate) to **+$1,605.31** (GOLDHUNTER, 78.6% win rate) — AIDY is genuinely differentiating providers, not producing flat output. Full detail: `LIVE_STATE.json` → `provider_coverage_v1`.

## Book-flat-before-merge rule dropped (2026-09-17)

Danny: *"Merge it.. nobody cares about open positions."* Routine research merges are no longer held on open-position count. Execution/risk-sizing changes still require scrutiny. Full detail: `OWNER_MANDATE.md`.

## Scoreboard cohort dimensions — v1 live (2026-09-17)

PR #185 merged/deployed. `provider_trade_scoreboard_by_cohort` splits provider performance by source, side, session and weekday (Europe/Sofia). Cohort evidence is not yet wired into live AIDY decisions.

## Decision Ledger outcome scoring — v1 live (2026-09-17)

PR #184 merged/deployed. `AidyDecisionOutcomeRuntime` scores decisions against `provider_trade_scores` fixed baseline. `approve` gets delta 0; denied/held trades are scored counterfactually from already-computed baseline outcomes. Early historical evidence showed duplicate/repost holds promising while conflict-deny was not convincing. Treat this as thin historical evidence, not authority.

## Current AIDY runtime state — recovered / READY, multi-cycle verified

17 September production patch hardened Super Signals AIDY M1 transport with bounded retry/backoff. Sustained health was independently confirmed across multiple systems/cycles; do not cite the one-time startup READY probe alone. Full detail: `handovers/2026-09-17-continuous-health-verification.md`.

## Day 14 governance issue

`PROVIDER_DAY14_GOVERNANCE_ERROR` root cause is a preregistration-boundary methodology mismatch as registry cohorts grow. Logging was fixed; methodology choice remains unresolved. Zero live-money impact (`research_only=True`).

## Live execution posture

- Gold/XAUUSD only.
- **1% only** live-risk directive unless owner explicitly changes it.
- TP1 + TP2 -> SL to entry; TP3 -> SL to TP2; move SL to entry != close.
- Research/provider intelligence cannot silently change risk, promote/demote live providers or acquire broker authority.
- AIDY live-money authority OFF.
- XAUUSD weekend freeze unchanged.

## Product north star

`provider signal -> PIT-safe Gold context -> provider history -> current exposure -> AIDY decision -> action -> outcome -> counterfactual score -> learning`

AIDY must become measurably better on forward unseen evidence, not merely accumulate more data.