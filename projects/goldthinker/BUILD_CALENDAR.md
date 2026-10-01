# GoldThinker — Gated Build Calendar

**Rule:** a Build Day is a gated phase, not necessarily one 24-hour day. We do not move to the next day until the current day's code, evidence and acceptance tests are clean and reviewed. If a gate fails, we stay on that day and fix it.  
**Current position:** **Day 8 of 15 — IN PROGRESS**.  
**Target of Day 15:** Full Research/Paper Launch. Real-money Live is a later evidence decision after discovery + frozen validation.

| Build Day | Phase | Status | Purpose |
|---|---|---|---|
| 1 | Research foundations | ✅ ACCEPTED | Decide exactly what GoldThinker is and what it is allowed to learn/test. |
| 2 | Deterministic rules + evidence packs | ✅ ACCEPTED | Turn research into exact, testable rules and fixed acceptance vectors. |
| 3 | Broker, MT5, DB and tick feed | ✅ ACCEPTED | Give GoldThinker its own trustworthy market feed and broker specification. |
| 4 | Own candles + feed/timeframe gate | ✅ ACCEPTED | Prove our candles match Vantage before any pattern research uses them. |
| 5 | Production core maths + research clocks | ✅ ACCEPTED | Build exact shared calculations and no-hindsight start clocks. |
| 6 | Wave-1 pattern/trade engine | ✅ ACCEPTED | Build the production candle detectors, variants and virtual execution. |
| 7 | Live research loop + real detections | ✅ ACCEPTED | Run the engine over real recorded Vantage data and persist outcomes safely. |
| 8 | Real-data differential audit + performance | 🟡 IN PROGRESS | Prove the production detector is correct and fast enough on the owner's real DB. |
| 9 | Runtime hardening + packaging | ⬜ NOT STARTED | Make GoldThinker operate reliably without fragile manual setup. |
| 10 | Portfolio Simulation engine | ⬜ NOT STARTED | Build the EUR 10k compounding portfolio layer without contaminating strategy ledgers. |
| 11 | Validation engine | ⬜ NOT STARTED | Automate discovery reviews, freeze manifests and untouched validation rules. |
| 12 | Vantage demo execution mirror | ⬜ NOT STARTED | Mirror accepted Portfolio Simulation trades to the dedicated demo and reconcile them. |
| 13 | Hub data/API layer | ⬜ NOT STARTED | Turn DB truth into exact owner-facing views and metrics. |
| 14 | Hub UI + candle pages | ⬜ NOT STARTED | Build the usable GoldThinker website/dashboard and trade views. |
| 15 | Full-system launch acceptance | ⬜ NOT STARTED | Prove the whole paper/research system can run continuously and freeze the launch manifest. |

## Day 1 — Research foundations ✅ ACCEPTED
**Why:** start clean, separate from AIDY/Super Signals, and define the research objective before coding.  
**Built/decided:** separate GoldThinker system; deterministic same-data/same-decision rule; Mon-Fri XAUUSD observation; all supported timeframes; 1% paper-risk convention; RAW/BASELINE/SOURCE-NORMALIZED layers; core candle-source research; Wave 1 = 22 full patterns + Kicker Early + Abandoned Baby Early.  
**Gate:** D-005 foundations agreed; scope separated; source disagreements recorded rather than guessed.  
**Evidence:** `CANDLE_SPEC_V1.md`, `MASTER_CANDLE_LIST.md`, `RESEARCH_SOURCES.md`, D-001..D-017.

## Day 2 — Deterministic rules + evidence packs ✅ ACCEPTED
**Why:** prose research had to become exact rules that can be independently tested.  
**Built/decided:** A-01..A-30 resolved; zone role/death, entries/exits, tick-side execution, calendar rules, max hold, target precedence, quantisation, RSI, clusters; `PIP_SRC_USD=0.10`; discovery/validation rules; Portfolio Simulation rules; 1,408 pattern-family vectors, 24 portfolio vectors, 10 validation vectors.  
**Gate:** reference calculators reproduce frozen evidence packs; no unresolved high-severity Wave-1 ambiguity.  
**Evidence:** D-036..D-043, `VALIDATION_RULES.md`, `PORTFOLIO_RULES.md`, `tests/`.

## Day 3 — Broker, MT5, DB and tick feed ✅ ACCEPTED
**Why:** the experiment needs its own trustworthy market record and dedicated demo environment.  
**Built:** dedicated Vantage demo connection; credential-free real broker specification; SQLite schema; tick recorder with dedupe/resume/reconnect; raw broker-wall timestamps plus versioned UTC normalisation; fresh-tick offset/DST protections.  
**Gate:** local MT5 connection proven; broker spec captured; feed tests pass; raw data retained for recomputation.  
**Evidence:** D-044/D-045, broker config, `src/goldthinker/feed/`, `src/goldthinker/db/`.

## Day 4 — Own candles + feed/timeframe gate ✅ ACCEPTED
**Why:** no candle research is trustworthy until GoldThinker's candles reproduce Vantage correctly.  
**Built:** own BID/ASK candles; higher TFs aggregated from own M1; native MT5 reconciliation only; feed-health report; per-timeframe gate; quiet-period classification.  
**Gate:** exact native reproduction previously achieved for enabled M1-D1; W1/MN1 remain disabled until their own exact-match evidence exists.  
**Evidence:** D-046/D-047 and candle/reconciliation/health code/reports.

## Day 5 — Production core maths + research clocks ✅ ACCEPTED
**Why:** every strategy must share one exact implementation and start only when contemporaneous prerequisites exist.  
**Built:** exact global production functions G1-G13; ATR, geometry/classes, swings/trend, zones, RSI, sessions/calendar, quantisation; feed gate separated from strategy readiness; per-strategy `research_start`.  
**Gate:** global golden vectors reproduced; research clocks cannot use hidden native history.  
**Evidence:** D-048/D-049, core/gate/research modules.

## Day 6 — Wave-1 pattern/trade engine ✅ ACCEPTED
**Why:** production needed its own candle definitions and virtual execution rather than relying on scratch calculators.  
**Built:** canonical Wave-1 detectors; BASE and SOURCE-NORMALIZED variants; entry/stop/target logic; first-executable tick; max-hold exits; RAW MFE/MAE; overlap clusters; hub counters.  
**Gate:** production reproduces the golden pattern/execution vectors; no rule is changed to make real data look better.  
**Evidence:** D-050 and `src/goldthinker/patterns/`.

## Day 7 — Live research loop + real detections ✅ ACCEPTED
**Why:** golden-tested functions had to run over real recorded Vantage candles and persist evolving outcomes without hindsight.  
**Built:** live loop; research-clock enforcement; point-in-time news; data-gap rules; unknown-commission handling; DB lock fix; chunked catch-up; live report.  
**Gate:** real run completed without broker orders; hundreds of occurrences/trades stored; locking/catch-up defects fixed with regression tests before advancing.  
**Evidence:** D-051..D-057; first major snapshot 655 occurrences, 78 virtual trades, 9 open.

## Day 8 — Real-data differential audit + performance 🟡 IN PROGRESS
**Why:** before portfolio/demo execution, production must match an independently loaded reference on the owner's real DB and keep up in steady state.  
**Already built:** differential audit; independent raw-SQL reference loaders; `INPUT_MISMATCH`; stored-population completeness; staleness guard; non-vacuous trade checks; honest benchmark; `tools/final_audit.ps1`.  
**Current evidence:** 120 local tests pass; recorder connected; prior 394.1 s sample was backlog (151 bars / 8,679 evals / 1,184 stored), not steady state; clean rerun is in progress.  
**Gate — ALL required:** full suite pass; fresh ticks; backlog cleared; 3/3 genuine M1 completions; benchmark PASS with desired slowest <15 s; final differential audit LAST with 0 input mismatches, 0 semantic mismatches, 0 stored-vs-recomputed differences, no unreached stored events, real trade paths exercised, and no strategy-event mutation; H4/D1 independent coverage resolved once clocks are active.  
**Status:** **DO NOT ADVANCE TO DAY 9 UNTIL THIS GATE PASSES AND REPORTS ARE REVIEWED.**

## Day 9 — Runtime hardening + packaging ⬜ NOT STARTED
**Build:** package/install so fresh terminals need no manual `PYTHONPATH`; one start/stop/status workflow; supervise recorder/detector; heartbeat; structured logs; DB backup/restore; Windows reboot recovery; restart idempotence.  
**Gate:** clean fresh-terminal startup; forced recorder/detector restart tests; no duplicate processing; backup/restore succeeds; stopped components are detected; supervised soak has no unexplained feed loss/DB lock.

## Day 10 — Production Portfolio Simulation ⬜ NOT STARTED
**Build:** D-042 EUR 10k compounding portfolio; 1% current-equity sizing; heat/direction/notional caps; clusters; drawdown ladder; daily stop; EUR conversion; separate strategy/portfolio/rounding R; candidate manifests.  
**Gate:** all 24 portfolio vectors reproduce; deterministic integration replay; strategy ledgers unchanged by portfolio decisions; portfolio ledger fully reconciles.

## Day 11 — Production Validation Engine ⬜ NOT STARTED
**Build:** Month-1/2/3 discovery reviews; frozen cohort/manifest; V1-V6 validation; best-day removal; cost stress; moving-block bootstrap; fixed cohort multiplicity; month-3/month-6 validation looks.  
**Gate:** all 10 validation vectors reproduce; freeze is immutable; pre-freeze trades excluded; repeat runs deterministic; open trades cannot create a false PASS.

## Day 12 — Vantage demo execution mirror ⬜ NOT STARTED
**Build:** execute only Portfolio Simulation-accepted trades; deterministic order IDs; SL/TP/exit; broker deal/fill/cost ingestion; restart reconciliation; demo balance kept separate.  
**Gate:** dry-run tests; controlled demo trade lifecycle; restart during an open demo trade creates no duplicate; DB/Portfolio/Demo differences visible; no path to Super Signals.

## Day 13 — Hub data/API layer ⬜ NOT STARTED
**Build:** read-only owner-facing views over DB; separate strategy/portfolio/demo balances; daily/week/month P&L; positions; winners/losers; pattern/TF/variant stats; detections/trades; audit/feed/runtime health.  
**Gate:** every aggregate reconciles against independent SQL; no ledger blending; formation counts not inferred from trades; stale runtime state visibly flagged.

## Day 14 — Hub UI + candlestick pages ⬜ NOT STARTED
**Build:** dashboard/cards; each candle page with illustration, explanation, exact definition, rules, stats, TF comparison, equity curve, detections/trades; individual trade views; health panel; NOT ENOUGH DATA/PRELIMINARY states; optional demo-trade Telegram notifications.  
**Gate:** D-022 represented end-to-end; UI figures exactly match Day-13 data; mobile/desktop usable; no stale/merged balance presentation.

## Day 15 — Full-system launch acceptance ⬜ NOT STARTED
**Build/finalise:** freeze launch manifest; prove recorder/candles/detector/Portfolio/demo/validation/Hub work together; backup/recovery and incident checklist.  
**Gate:** full suite clean; feed/native reconciliation clean; detector differential audit clean; portfolio/validation vectors clean; demo mirror reconciles; Hub figures reconcile; continuous market-session soak passes; deliberate restart recovery passes; launch manifest committed/reviewed.  
**Outcome:** **GoldThinker Full Research/Paper Launch.**

# After Day 15 — evidence calendar, not build days

- **Discovery Month 1:** Month-1 strategy review rules.
- **Discovery Month 2:** Month-2 continuation gates.
- **Discovery Month 3:** candidate gates; surviving strategies frozen into a cohort/manifest; no automatic real-money move.
- **Frozen Validation Month-3 look:** post-freeze observations only; formal first validation look.
- **Frozen Validation Month-6 final look:** final validation + multiplicity control; only PASS-STRONG may be presented as a potential live candidate.
- **Real-money decision:** owner only. Build completion, backtests, demo performance and model decisions never automatically enable real-money trading.
