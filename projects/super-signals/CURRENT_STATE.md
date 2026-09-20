# Super Signals — Current State

> **Owner mandate in force since 2026-09-17: read [`OWNER_MANDATE.md`](../../OWNER_MANDATE.md) every session.** It sets the goal (AIDY becomes an evidence-scored decision layer that measurably improves Super Signals' profit) and the one boundary that does not move under it (live-money authority stays OFF until explicitly graduated per class).

Last verified: **2026-09-20**

Authoritative repo: `dannythehat/super-signals`
Authoritative deployed branch: `feature/day-10-shared-telegram-sources`
Verified source/deploy SHA: `79e00b0f514aeb184918f736ce456830a742dab7` (AIDY toolbox-aware historical training stack through PR #235)
Render service: `super-signals-day-8` (`srv-d9qmcgks728c73a555m0`)
Verified live deploy: `dep-danvn2f40ujc73dc8ev0`
Deploy status: **live**. Historical stress is enabled in **train-only** mode; validation and OOS remain sealed; exact replay/18-case holdout remain disabled and unopened.
Quality gate: canonical Render Docker gate **1,194 passed / 137 skipped / 2 warnings**, plus web quality checks and repository secret scan.

**Open concern, not yet confirmed resolved**: the intermittent restart-loop (`instance_count` flapping 0/1 every few minutes) that this session attributed to a lapsed Render payment method earlier tonight was still observed as recently as the 04:27-04:29Z window, well after the owner said they'd paid it. Not re-checked this pass -- next session should check this first before assuming it's fixed.

**Gap flagged for the next session**: between this session's PR #202 (day-map, merged 04:56Z) and this update, PRs **#203, #204, #205, #206** were also merged and deployed to the same service, evidently by a separate concurrent session this same session has no transcript context for: #203 "Harden AIDY Provider Context against transient transport failures", #204 "Fix Day 14 governance for append-only provider cohorts", #205 "Make AIDY use candle tools when structure evidence is needed" (this one's own deploy `build_failed`, followed by 4 more direct-commit build-fix attempts targeting a broken AIDY prompt-regression-test string literal -- 3 more `build_failed` before one succeeded), #206 "Restore Day 13 forward evidence under current Gold session buckets". All four are live in production as of the SHA/deploy recorded above. **Not verified by this session beyond the deploy history and a clean post-deploy log scan** -- read the actual PR diffs before making any claim about what #203-206 changed or relying on them architecturally.

## AIDY toolbox-aware historical training exam — ACTIVE / TRAIN ONLY (2026-09-20)

The owner directed that AIDY must understand and use the tools available to him rather than merely
having research modules in repositories. Production reasoning now uses prompt
`aidy_reasoning_prompt_v12_toolbox` and receives an explicit `toolbox_manifest`.

Relevant merged Super Signals commits:
- PR #227 `e21b4eded371e9c46038d5daaca6514399cf708b`: fixes edited-Telegram hindsight by using the selected revision edit timestamp as effective signal time.
- PR #228 `521b4c9002f7ffa22aae54a585c6edfbd5b10e53`: adds explicit historical toolbox orchestration.
- PR #229 `134a81d79fe88d6b2343a08e657d6307a1d30402`: teaches AIDY to read the toolbox manifest, consider available standing evidence, call material on-demand tools, and preserve UNKNOWN for unavailable evidence.
- PR #230 `36dee29f4b87dfe2f94bb02ea19f21c612b363d4`: aligns the historical manifest key with the reasoning prompt.
- PR #231 `e92c46f92d7c9679066fbdbbb1bd46dd281d4029`: records exact per-decision tool names and versions the measured stress replay to `aidy_historical_stress_lab_v7_tooltrace`.
- PR #232 `5b09fea3f7707a8f752c888f187c99c1a531f8e7`: freezes the training cohort independently so late evaluation rows cannot block or contaminate training.
- PR #233 `f85a0456d1d0cf566c4b6eb4ecdc0c3722e22abb`: expands the historical replay DB contract for research partitions/evidence/run scopes; first deploy failed transactionally because the scoreboard view depended on `partition`.
- PR #234 `745b5af537cd0028535cb5e7400255b49d101156`: fixes the migration by dropping/recreating the replay scoreboard view inside the transaction. Alembic `0108_aidy_hist_stress_schema` is live and verified directly in Postgres.
- PR #235 `79e00b0f514aeb184918f736ce456830a742dab7`: historical v8 deterministic preflight router. M15 is always fetched, H1 is added for unclear/high-risk structure, calendar is focused for unknown/nearby event risk, and provider evidence is inspected when available. Historical stress remains train-only; live reasoning is explicitly enabled.

v7 diagnostic failure (preserved, not training evidence): 55 decisions used 0 model tools and 0 preflight tools. Of 46 scored before shutdown, provider taken P&L was +$31.84, v7 shadow +$23.71, delta -$8.13. Entire v7 namespace is failed diagnostic evidence only.

v8 active replay: `aidy_historical_stress_lab_v8_preflight_router`. Live reasoning engine is explicitly enabled; historical stress is train-only with validation/OOS locked.

Active training identity:
- 571 cases
- SHA-256 `18326c515d12a7e55046828f6fe59198de50b0b7538193174528bf56f7829168`
- first signal 2026-08-12 00:23:26Z
- last signal 2026-09-03 22:23:23Z

The live dynamic source query currently returns 803 eligible rows split 571/70/162 because three
late historical rows appeared in validation/OOS after the original 800-case freeze. Those three are
NOT admitted into the frozen evaluation design. Training stays 571. Validation and OOS remain
locked until their original 69/160 frozen identities are restored explicitly. The exact 18-case
holdout remains sealed.

Historical reasoning can use retrospective XAUUSD candles, official event timing/calendar,
provider as-of evidence, recent provider messages, historical analogues, event/liquidity context,
probability/EV context, self-critique and a focused historical evidence inspector. Per-decision
tool-use telemetry records which on-demand tools were actually used so later analysis can measure
losses avoided versus winners cut by tool.

No broker execution, live risk sizing, provider routing or live-money authority changed in this work.

Full handover:
`projects/super-signals/handovers/2026-09-20-aidy-toolbox-awareness-training-stress.md`.

## AIDY large historical stress lab — MERGED / RESEARCH OFF PENDING TRAIN RUN (2026-09-20)

The five-build 140-case exact-PIT exam remains intact, but it is no longer being mistaken for the
full historical learning corpus. A separate reconstructed stress lab now covers **803 unique
resolved executable XAUUSD provider messages**, frozen chronologically into **571 research_train / 69 research_validation / 160 research_oos**, plus 3 auditable source-universe exclusions with no resolvable score. The official exact-PIT 18-case holdout is untouched.

PR #221 created the isolated lab. PR #222 fixed full-cohort capacity, hard-locked evaluation scopes
and added retrospective candle tool use. PR #223 added conservative official event timing and
provider-specific as-of memory reconstructed only from results known before each target signal.
Latest merged source SHA: `25d6cea1dc7dd127e9890b0363148f1732557da4`.

Runtime stays disabled by default and carries no broker/execution/provider-status/live-money write
authority. Next step: run only the 571 training cases, diagnose AIDY-versus-provider outcome
differences, improve from training evidence only, then evaluate untouched validation and OOS.
Full handover:
`projects/super-signals/handovers/2026-09-20-aidy-large-historical-stress-lab.md`.

## Weekend Build 1 — Historical Time Machine — engineering/production verified, no edge claim (2026-09-19)

Build 1 of the gated weekend sequence is complete as research infrastructure. Super Signals PR #209 merged to the deployed branch as `8ddbc40050e13fb26f04304d2e2de7a364c2efdc`; Render deploy `dep-dan4cg3m8hqs73a0gtb0` is live. The Docker image itself gates deployment on compileall plus the full API pytest suite.

The frozen strict point-in-time cohort is **140 cases**: **103 development / 19 validation / 18 locked holdout**. Replay v4 completed **103/103 development decisions + scores** and then **19/19 validation decisions + scores**. The holdout remains sealed with **0 decisions**. Safety checks show **0 input-digest mismatches, 0 research-flag violations and 0 live-money replay rows**. The bounded anti-drift retry was used 11 times in development and 3 times in validation; every transient provider-claim rejection ultimately resolved under the unchanged strict validator.

The Time Machine passed its engineering exam, but the current AIDY shadow policy did **not** prove edge. Development: provider-taken baseline **+$867.48**, AIDY replay shadow **+$403.65**, delta **-$463.83** (19 improved / 46 harmed / 38 unchanged). Validation: provider-taken baseline **-$39.42**, AIDY replay shadow **-$21.38**, delta **+$18.05** (1 improved / 1 harmed / 17 unchanged). This is deliberately recorded as a generalisation/decision-quality problem to solve, not as profitability proof. No holdout result is available because the holdout remains unopened.

**Build 1 handoff complete:** Build 2 subsequently passed its own separate gate below.


## Weekend Build 2 — News/Event + Liquidity/Execution — engineering/production verified, no edge claim (2026-09-20)

Build 2 is complete as a research evidence layer. Super Signals PRs #210-#213 are merged to the authoritative deployed branch; final source SHA `4bdd56e94bf801a5c22aa9b80168b4f64251b9f1` is live on Render. Validation-scope deploy `dep-danmqtajnfac7395g5cg` is live. The final canonical Docker gate passed **1,144 API tests, 137 skipped**, plus the repository secret scan and web quality gates.

Build 2 adds a deterministic point-in-time `aidy_event_liquidity_execution_v1` surface to AIDY. It uses the signal's own geometry, immutable quote/liquidity evidence, scheduled-event metadata and broker execution calibration available no later than the signal. Scheduled events are timing/risk facts only, never directional predictions; realized event outcomes are unavailable to the decision. Future quote/calibration evidence is rejected. Broker execution calibration is usable only after the existing 30-sample floor is met for every required sample class; otherwise execution friction remains UNKNOWN. The replay provider-history retry was also hardened fail-closed: if strict provider-history prose validation fails, the one bounded retry removes provider history entirely while leaving the validator unchanged.

Historical replay advanced to `aidy_historical_time_machine_v5` with immutable input contract `aidy_historical_replay_input_v4`, preserving the same frozen **140 cases: 103 development / 19 validation / 18 locked holdout**. Development completed **103/103 decisions + 103/103 scores**: taken baseline **+$867.48**, Build 2 AIDY shadow **+$254.63**, delta **-$612.85** (17 improved / 44 harmed / 42 unchanged; 11 bounded provider-claim retries). Validation completed **19/19 decisions + 19/19 scores**: taken baseline **-$39.42**, Build 2 AIDY shadow **-$22.35**, delta **+$17.07** (1 improved / 1 harmed / 17 unchanged; 3 retries). Safety remained clean: **0 holdout decisions, 0 input-digest mismatches, 0 research-flag violations, 0 live-money replay rows**.

This proves the Build 2 evidence plumbing and acceptance discipline, **not trading edge**. Development performance worsened versus both the provider-taken baseline and the Build 1 replay, while the small validation slice remained only modestly positive. The result must be carried forward as a decision-quality/generalisation problem for later modules, not marketed as profitability proof.

**Build 2 handoff complete:** Build 3 subsequently passed its own separate gate below.


## Weekend Build 3 — Provider Conditional-Alpha + Historical Analogue — engineering/production verified, no edge claim (2026-09-20)

Build 3 is complete as a research evidence layer. Super Signals PR #215 merged to the authoritative deployed branch at `3ae5469e2b4ae83c6de64842aaf714cbd51a38f1`; validation-scope Render deploy `dep-dann5mek1f9s7399ndp0` is live. The canonical Docker gate passed **1,149 API tests, 137 skipped**, plus secret scan and web quality gates.

Build 3 deliberately reuses the existing Day 13 preregistered conditional-alpha engine rather than creating a duplicate hypothesis registry. Its current statistical truth remains underpowered: **0/140 historical exam cases have usable pre-trade conditional alpha**, and Day 13 cells conditioned on realized/post-entry duration are never promoted into entry-time directional evidence. The new `aidy_provider_alpha_analogue_v1` layer adds strictly prior-resolved historical analogues only. Every analogue's signal and result-known timestamp is earlier than the target signal, selection bias is explicit, and analogue evidence is descriptive-only with `usable_for_live_edge_claim=false`. Across the 140 frozen cases, 72 had enough prior analogues for a descriptive sample and 68 correctly remained insufficient; **0/140 analogue packets are permitted as live-edge proof**.

Historical replay advanced to `aidy_historical_time_machine_v6` with immutable input contract `aidy_historical_replay_input_v5`, preserving the same **103 development / 19 validation / 18 locked holdout** partition. Development completed **103/103 decisions + scores** with taken baseline **+$867.48**, Build 3 AIDY shadow **+$334.09**, delta **-$533.39** (18 improved / 45 harmed / 40 unchanged; 7 bounded provider-history retries). Validation completed **19/19 decisions + scores** with taken baseline **-$39.42**, Build 3 shadow **-$22.35**, delta **+$17.07** (1 improved / 1 harmed / 17 unchanged; 3 retries). Safety remained clean: **0 holdout decisions, 0 digest mismatches, 0 research-flag violations, 0 live-money replay rows**.

Engineering result: PASS. Trading-edge result: **not proven**. Build 3 improved development replay by **$79.46** versus Build 2 but still materially underperformed the provider-taken baseline and remained worse than Build 1. Validation was unchanged from Build 2. The result is evidence that the new context is safe and usable, not evidence that AIDY should receive wider authority.

**Build 3 handoff complete:** Build 4 subsequently passed its own separate gate below.

## Weekend Build 4 — Probability/EV + Trade Management/Profit Extraction — engineering/production verified, no edge claim (2026-09-20)

Build 4 is complete as a research-only decision-support layer on the authoritative deployed branch. The merged implementation entered through Super Signals PR #216, and the final deployed source SHA is `1c6853e814d59f57c6b55f41361c23c98ffde791`. Validation-scope Render deploy `dep-dannhpugekts739i8660` is live. The canonical Docker gate passed **1,154 API tests, 137 skipped, 2 warnings**, plus web quality and secret-scan gates.

The deployed `aidy_probability_ev_management_v1` layer remains deliberately conservative. It derives descriptive probability only from already-resolved prior Build 3 analogues, keeps selection bias explicit, computes signal reward:risk geometry and execution-cost proxies only from evidence already available at the signal, and does not pretend that prior positive-outcome frequency is a calibrated current TP-hit probability. Across the frozen cohort, **72/140** cases have the minimum prior-outcome sample for descriptive empirical analogue EV and **68/140** correctly remain insufficient. In every case, `usable_for_live_edge_claim=false` and `usable_for_entry_override=false`.

Trade-management authority did not change. Build 4 exposes the existing profit-protection ladder as context only and preserves the Day 20 forward-evidence gate: **AIDY paper management=false and AIDY live management=false**. The research posture is `provider_baseline_only_until_forward_efficacy_is_proven`; Build 4 must not duplicate or override the canonical broker-settlement ladder. No new live-money execution authority was added.

Historical replay advanced to `aidy_historical_time_machine_v7` with immutable input contract `aidy_historical_replay_input_v6`, deriving directly from the exact frozen Build 3 v5 cohort. The cohort remains **140 cases: 103 development / 19 validation / 18 locked holdout** with **0 partition drift**. Development completed **103/103 decisions + 103/103 scores**: provider-taken baseline **+$867.48**, Build 4 AIDY shadow **+$554.52**, delta **-$312.96** (13 improved / 33 harmed / 57 unchanged). That is a **+$220.43 improvement in delta versus Build 3**, but AIDY still materially underperforms simply taking the provider trades, so no trading-edge claim is permitted.

Validation completed **19/19 decisions + 19/19 scores**: provider-taken baseline **-$39.42**, Build 4 AIDY shadow **-$21.38**, delta **+$18.05** (1 improved / 1 harmed / 17 unchanged). Safety/PIT audit is clean: **0 holdout decisions, 0 holdout scores, 0 input-digest mismatches, 0 research/live-money flag violations, 0 future analogue-result violations, 0 future analogue-signal violations, 0 live-management violations, 0 paper-management violations, 0 live-edge-claim violations, and 0 entry-override violations**. All 140 Build 4 cases map back to the same Build 3 source decisions.

Engineering result: PASS. Trading-edge result: **not proven**. Build 4 materially improves development performance versus Build 3 while preserving the safety boundary, but it still does not beat the provider baseline. The 18-case holdout remains sealed and must not be opened merely because development improved.

**Build 4 handoff complete:** Build 5 subsequently passed its engineering/production gate below.

## Weekend Build 5 — Failure Attribution / UNKNOWN + AIDY self-critique — engineering/production verified, no edge claim (2026-09-20)

Build 5 is complete as the fifth and final module in the current weekend sequence. Super Signals PR #219 introduced the PIT-safe self-critique/failure-attribution layer. Its first full replay exposed the exact failure the module was intended to detect: AIDY still used `reduce` as generic caution too often. Build 5 v1 reduced **79/103** development trades and produced development delta **-$407.47**, worse than Build 4's **-$312.96**. That failed result was preserved rather than hidden.

The corrective calibration in PR #220 was selected from **development evidence only**. It made the self-critique enforceable rather than merely advisory: a reduced shadow size is permitted only when the current trade itself has an approved concrete reason (mean target reward below 1R, clear multi-timeframe counter-trend, or a high-impact scheduled event within 60 minutes). Ordinary uncertainty is not a reduce reason. A hard UNKNOWN gate forces `need_more_evidence`. Prior self-feedback remains descriptive only and can never create directional edge, entry authority, paper management, live management or live-money authority.

Final deployed source SHA is `dc642161e59d94c1e6fdb595bc578d070e53ec9c`; Render deploy `dep-dantd12jnfac739q2o2g` is **live**. Canonical Docker gate passed **1,165 API tests / 137 skipped / 2 warnings**, plus web quality and secret scan.

Final Build 5 contracts:
- self-critique context: `aidy_failure_self_critique_v2`
- historical replay: `aidy_historical_time_machine_v9`
- immutable replay input: `aidy_historical_replay_input_v8`
- frozen predecessor contract: `aidy_historical_replay_input_v7`

The exact **140-case** cohort remains unchanged: **103 development / 19 validation / 18 locked holdout**. All 140 final cases map back to the same Build 5-v1 source decisions with **0 partition drift**. The 18-case holdout remains sealed with **0 decisions / 0 scores**.

Final development completed **103/103 decisions + 103/103 scores**:
- provider-taken baseline: **+$867.48**
- Build 5 final AIDY shadow: **+$807.07**
- delta versus provider baseline: **-$60.42**
- improved / harmed / unchanged: **6 / 15 / 82**
- final actions: **74 take / 28 reduce / 1 reject**
- deterministic `reduce -> take` corrections: **42**

Build 5 therefore improves development delta by **+$252.54 versus Build 4** (-$60.42 vs -$312.96), but it still does **not** beat the provider baseline and therefore does **not** prove trading edge.

Validation completed **19/19 decisions + 19/19 scores**:
- provider-taken baseline: **-$39.42**
- Build 5 final AIDY shadow: **-$41.38**
- delta: **-$1.96**
- improved / harmed / unchanged: **0 / 1 / 18**
- final actions: **12 take / 6 reduce / 1 need_more_evidence**
- deterministic `reduce -> take` corrections: **5**
- hard UNKNOWN correction: **1**

This validation result is worse than Build 4's **+$18.05** validation delta. That is important evidence that the large development improvement did **not** fully generalise. Do not tune Build 5 again against the now-observed validation slice. The next proper test must use the still-sealed holdout, with no further fitting first.

Final PIT/safety audit is clean: **0 decision-digest mismatches, 0 partition drift, 0 future self-feedback cutoff violations, 0 research-flag violations, 0 live-money violations, 0 live-management violations, 0 holdout decisions and 0 holdout scores**. Across the 140 frozen inputs, self-feedback identified **56 over-reduction**, **11 prior-filtering-added-value**, **5 mixed/neutral**, and **68 insufficient-prior-feedback** cases; UNKNOWN was hard-required on **1/140** cases. These are descriptive diagnostics only.

Engineering result: **PASS**. Production result: **PASS**. Trading-edge result: **NOT PROVEN**. The five-build sequence is now complete.

**Next step is not Build 6.** The next step is the proper final exam: freeze this exact Build 5 implementation and evaluate the untouched **18-case holdout** without further tuning. Do not open that holdout until the owner explicitly begins the proper exam.

## TIG management-reliability fix, 6 providers switched on for paper trading (2026-09-17/18)

Root-caused and fixed the real reason management instructions could go unmanaged: a stuck trade_update dispatch failure was never retried and never escalated. Built `ManagementReliabilityRuntime` (retry + fail-safe force-close) and fixed the dominant false-failure mode in `AiLifecycleBridge._resolve_signal` (92% of 278 sampled real failures were benign "already closed by another path" no-ops, not broken links). Switched 6 shadow providers (incl. TIG's Asia Trades) to `testing` status, each restricted to its own best-evidenced side via `provider_execution_probation` until graduated. Found and fixed two self-inflicted production bugs from this same work (a `jsonb_build_object` bare-param typing bug, a `:param::interval` SQLAlchemy `text()` adjacency bug) -- both now documented as a recurring pitfall. Overnight audit (owner-requested) confirmed real trades executed, zero messages left undecided despite an unrelated Render billing-lapse restart loop, and all apparent failures were benign. PRs 191, 193, 194, 195, 196. Full detail: `LIVE_STATE.json` -> `management_reliability_and_tig_paper_trading_v1`.

## Probation side/session gate fixed, GOLDHUNTER graduated fully including live money (2026-09-18)

Owner: "we are leaving loads of profits on the table." Investigated GOLDHUNTER specifically (79.1% win rate, 43 resolved trades, both sides individually well past the cohort floor) and found the real bug: the fingerprint's `cohort_sample_met` required both an adequate *side* split and an adequate *session* split before probation eligibility would ever pass, but eligibility only ever needs the side answer -- GOLDHUNTER's trades cluster into one dominant session, so the unrelated session half silently vetoed every trade. Split into independent `side_sample_met`/`session_sample_met` (PR 197) -- unblocked GOLDHUNTER plus 3 other providers with the same latent bug. Owner then explicitly asked to graduate GOLDHUNTER fully off probation, including real member live-money eligibility, not just paper (PR 198) -- offered the narrower paper-only option first and explained the tradeoff; owner chose full graduation with under an hour of real forward history under the corrected gate. **There are 5 connected live MT5 accounts with real trade history already in this system -- this is not a hypothetical switch.** Full detail: `LIVE_STATE.json` -> `provider_probation_side_session_split_and_goldhunter_graduation`.

## AIDY reasoning gets real market context, v1->v2 (2026-09-18)

Owner directly challenged whether AIDY uses any of the data/tools it's been given ("shiny background tool that does nothing"). Real audit found: the reasoning call previously saw only a signal's own entry/stop/TP numbers plus provider history text -- its own system prompt explicitly forbade discussing market conditions. Wired in AIDY's existing, already point-in-time-safe market/regime context (`AidyContextClient` -- real trend direction across M15/H1/H4, session, volatility, event timing) into the reasoning prompt (PR 199). Falls back to no-context reasoning exactly as before when a signal is too old for the context API's bounded lookback window; never blocks the pass. Does not touch `aidy_decision_engine.py` or any execution path -- still `research_only=true` throughout. **Owner has since asked for AIDY to have real-time multi-timeframe candles, a news/economic calendar, on-demand tool-calling access to pull any data it needs, and eventually to generate and score its own trade ideas rather than only judge providers'.** Responded with honest scoping: candle aggregation and tool-calling are buildable now from data already paid for; a calendar needs a new external data-source/credential decision the owner hasn't made; "predict whether price reverses or runs at a level" was declined as framed (nobody reliably does this) in favour of an honest historical-reaction-frequency version; AIDY originating its own trade ideas was flagged as a materially bigger, execution-adjacent system given real money is now live on GOLDHUNTER, and deferred pending explicit owner sign-off on that one piece specifically. Owner's response: "you should build everything." Proceeding with candle aggregation and tool-calling next as the pieces that need no new external dependency. Full detail: `LIVE_STATE.json` -> `aidy_reasoning_market_context_v2`.

## AIDY reasoning gets multi-timeframe candles + bounded tool-calling, v2->v3 (2026-09-18)

Owner escalated further, wanting real-time multi-timeframe candles, liquidity, a news calendar, on-demand data access and AIDY generating its own trade ideas, all at once ("It seems you are the issue here"). Shipped the two pieces buildable with zero new external dependency together (PR 200): a bounded `get_recent_candles` tool on the reasoning call, backed by `AidyMarketClient` (already point-in-time-safe, previously only used for retrospective outcome scoring, never a live decision before now) and a new pure aggregation module producing 1/5/15/30/45/60-minute candles on demand. The model picks timeframe and lookback; the fetch window always ends at, never after, the signal's own posted time. Bounded to 2 rounds of tool use so the model cannot stall indefinitely; `reason()` is now async and issues up to 3 real OpenAI requests per signal, with token/cost/budget accounting summed across every round actually made rather than a flat one-call assumption.

**A real point-in-time bug was caught by a test before merge**: the first version of the fetch-window calculation rounded forward to the end of the current (still-forming) candle bucket, which could request data from *after* the signal's own posted time -- a genuine PIT leak. Fixed by flooring to the signal's own minute instead.

MODEL_VERSION/PROMPT_VERSION bumped v2->v3. Does not touch `aidy_decision_engine.py` or any execution path -- still `research_only=true` throughout. 104 aidy tests green (was 82), full suite green (same pre-existing unrelated exclusion as before), ruff clean.

Owner then asked to pick a free economic calendar source. Recommended **Finnhub** (official free tier, 60 calls/min, no card, has an impact-rated `/calendar/economic` endpoint -- matters for telling a Fed rate decision from a minor regional release) over the unofficial ForexFactory JSON feed some bots scrape (genuinely free/keyless, but undocumented and no support guarantee -- declined as a foundation to build on). **Waiting on the owner to sign up and provide the API key** before this can be built. AIDY generating/scoring its own trade ideas remains explicitly un-started, pending separate owner sign-off given real money is now live on GOLDHUNTER. Full detail: `LIVE_STATE.json` -> `aidy_reasoning_candle_tool_v3`.

## AIDY reasoning gets a real economic calendar tool, corrected off Finnhub (2026-09-18)

Owner sent the Finnhub API key. It checked out live -- but direct testing of the actual endpoint needed (`GET /calendar/economic`) returned `403 "You don't have access to this resource"` while `/quote` and `/calendar/earnings` both returned `200` on the same free-tier key. **The prior recommendation was wrong for this specific endpoint** -- Finnhub's economic calendar requires a paid plan, corrected transparently to the owner rather than shipped broken or silently swapped. Built instead against the free, keyless "Fair Economy" public JSON feed (`nfs.faireconomy.media/ff_calendar_{lastweek,thisweek,nextweek}.json`) that many retail trading tools already rely on -- no signup, verified working directly. Its schema (`title`/`country`/`impact`/`date`/`forecast`/`previous`) is actually safer for AIDY's point-in-time discipline than Finnhub's would have been: **no realized-outcome ("actual") field at all**, so nothing it returns could ever leak a future-relative-to-a-signal result.

Adds a bounded `get_economic_calendar` tool (PR 201) alongside the existing `get_recent_candles` tool, both now generalized behind `tool_schemas`/`tool_executor` params on `AidyReasoningEngine.reason()` rather than the candle tool being hardcoded as the only option -- `AidyReasoningRunner._tools_for()` combines whichever tool clients are actually configured into one schema list and one dispatching executor. The feed only ever reflects the current real-world week; a signal more than ~6 days old gets an explicit "unavailable" result rather than risk silently serving the wrong week's events as if they belonged to it. `FINNHUB_API_KEY` was set on Render (`srv-d9qmcgks728c73a555m0`) while investigating and left in place -- it is a verified-valid key but is **not required or read by any shipped code**, confirmed by a direct grep of the deployed source (only reference is an explanatory docstring in `aidy_economic_calendar_client.py`, not an env-var read).

125 aidy-related tests green (was 104). Full suite green (same pre-existing exclusion as every prior PR tonight). ruff clean. Deploy `dep-damc5kbncjis73der750` (commit `bd731fac83ddf160709f326c848cb99263052fed`) built and went live clean, no FINNHUB or calendar-tool errors in logs, before being superseded by later same-night deploys. Full detail: `LIVE_STATE.json` -> `aidy_reasoning_calendar_tool_v3b`.

## AIDY gets a standing daily gold day-map, v3->v4 (2026-09-18)

Owner: *"He should use that and map the trading day out for gold in real time, then he can refer to it throughout the day."* The `get_economic_calendar` tool above only fires if the model happens to decide to call it for a given signal -- inconsistent (no guarantee any given signal actually gets calendar awareness) and wasteful (repeated fetches for the same day across many signals). This is different in kind: a standing rundown of the current UTC day's own scheduled medium/high-impact events, computed and folded into every signal's `market_context` automatically, never gated behind the model choosing to ask.

`fetch_todays_scheduled_events()` (PR 202) filters the same 3-week feed down to just the signal's own UTC calendar day, medium/high impact only, each event labelled with `session_bucket()` -- the exact same asia/london/london_new_york_overlap/new_york/rollover boundaries already used everywhere else in this codebase for Gold session segmentation, reused rather than redefined. Same freshness discipline as the on-demand tool: refuses (returns `None`, field omitted from `market_context`) for a signal too old for the feed's current-week coverage. `aidy_reasoning_runner.py`'s `_fetch_market_context` now combines two independently-optional sources -- regime/session context (PR 199) and the day map -- so a failure in one never suppresses the other; a genuinely empty day (checked, nothing scheduled) is reported honestly as an empty list, never collapsed into the same `None` used when nothing could be fetched at all. `PROMPT_VERSION` bumped v3->v4 (`MODEL_VERSION` unchanged -- the reasoning mechanism itself didn't change, only its inputs).

134 aidy-related tests green (was 125). Full suite green, ruff clean, no new migration needed. Deploy `dep-damc8p97lnhs73c6nnq0` (commit `e27e2e12de69689c8b64a24f9fa10fbe5c4260a6`) built and went live clean before being superseded by later same-night deploys (#203-206, see the gap note at the top of this file). **All three of that night's AIDY asks -- market context, candles + tool-calling, and the calendar -- are now shipped.** Remaining open items: AIDY generating its own trade ideas (explicitly gated, needs separate owner sign-off) and the still-unconfirmed Render restart-loop. Full detail: `LIVE_STATE.json` -> `aidy_reasoning_day_map_v4`.

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

## AIDY Gold State v2 consumer — BUILT ISOLATED / NOT MERGED

Phase 2 consumer preparation is on
`feature/aidy-gold-state-v2-reasoning` at `f6e1e42ecb8ff18b153912915588f4c6945711b6`, PR #208.

It adds strict intake validation for `aidy_provider_gold_state_v2` and reasoning rules that
forbid turning descriptive close paths, round numbers, liquidity proxies, volatility state or
scheduled-event proximity into causal/predictive claims. `cause_unknown=true` must remain
unknown.

PR #208 is intentionally **not merged** while Phase 1 forward grounding is still waiting.
Production remains `4650d2074ea4d4287285783a5157d4340cd41e8a`; no broker/execution/sizing/provider-status files are
changed by the Phase 2 PR.

## AIDY anti-drift Phase 0/1 — PRODUCTION VERIFIED / WAITING FOR FORWARD ROWS

Verified 2026-09-19 on the live Render service.

- deployed SHA: `33305a020f96e545990906a6de0c5dc253e9fcaf`
- Render deploy: `dep-dan2cv5ii2qc73bhmpig`
- Alembic: `0104_aidy_grounding_health`
- evidence contract: `aidy_reasoning_evidence_v2`
- API acceptance: **1105 passed, 137 skipped, 2 warnings**
- web acceptance: **28 passed**
- secret scan: PASS
- service health + public performance paths: responding after deploy

The AIDY reasoning model no longer receives raw provider identity/profile/fingerprint history.
Provider-history influence is limited to immutable PIT-safe claim objects. Side/session evidence
is scoped to the current signal cohort, unsupported references fail safe, missing cohorts stay
UNKNOWN, and successful annotations freeze both the evidence snapshot and validated claim refs.

Production grounding view at verification: 2674 legacy-unvalidated annotations, 2227 legacy
language-review candidates, 0 fresh evidence-v2 rows, 0 unsupported evidence-v2 rows. The market
is in the canonical weekend closure, so forward acceptance is waiting for the next eligible
signals; do not treat the legacy review count as a false-claim count.

No execution/risk behavior changed. AIDY live-money authority remains OFF and the owner 1% risk
directive is unchanged.

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