# GoldThinker — Project Status

**Last updated:** 2026-10-01  
**Authoritative build state:** this file + `BUILD_CALENDAR.md`  
**Current build day:** **Day 8 of 15 — Real-data acceptance (D-058) — IN PROGRESS**  
**Current code head reviewed:** GoldThinker current Day-8 branch after documentation updates  

GoldThinker is a new, separate XAUUSD research system. It does not use AIDY or Super Signals. Its own database is the research source of truth. The dedicated Vantage MT5 demo account is a future execution mirror only.

## Where we are now

Seven gated build days are accepted. **Day 8 is not complete and we do not move to Day 9 until its acceptance gate passes.**

The difficult candle/research logic is substantially built: broker/feed foundations, tick-built candles, timeframe gates, exact core calculations, Wave-1 production pattern detectors and variants, virtual execution/RAW, research clocks, the live detector loop, news vintages and the differential-audit framework all exist.

The finished product is not yet complete. Production Portfolio Simulation, the production validation engine, the Vantage demo execution mirror, unattended runtime packaging, and the full Hub/UI still remain.

## Latest verified local evidence

- **Unit-test gate independently rechecked 2026-10-01:** `py -m unittest discover -s tests_unit -v` completed **120/120 tests PASS in 52.386 s**. The synthetic benchmark tests also behaved as designed: one deliberate `INCOMPLETE` and one deliberate `PASS`; those blocks are fixtures, not live evidence.
- **Candle build rechecked in isolation:** **0.325 s**, `m1_bars_touched: 0`; the DB held 2,967 complete M1 bars at that point.
- **Detector steady/catch-up state rechecked in isolation:** **6.45 s total**, with **0 new bars** on M1/M5/M15/M30/H1, 27 open/pending occurrences re-evaluated and no backlog work. This proves the earlier 394.1 s cycle was backlog processing rather than normal steady-state cost.
- **Current live benchmark result:** `INCOMPLETE`, not FAIL. It waited the full **300 s** for completion 1/3 and observed **0 new M1 completions and 0 fresh ticks**. The idle benchmark cycle itself took **6.1 s** (5.98 s detection), which is inside the Day-8 <15 s target, but no live completion was observed so the benchmark cannot pass.
- Therefore the **current blocker is the recorder/feed not writing fresh ticks**, not detector speed and not the unit suite. The recorder had previously printed `feed connected`, but the benchmark proves the DB received no new ticks during its five-minute observation window. `run_forever()` should reconnect on `FeedError`; if the recorder process has returned to a PowerShell prompt, crashed on a non-`FeedError`, or is otherwise stalled, it must be restarted/diagnosed before the benchmark is repeated.
- Earlier real detector run stored **655 occurrences, including 78 virtual trades**. No broker orders were sent.
- The first real differential audit was deliberately rejected because its shared tick input had been truncated, making the trade layer vacuous. The audit was hardened in GoldThinker commits `c0c8d89`, `a2cbcf1` and `0eef777` with complete tick coverage, independent raw-SQL reference loaders, `INPUT_MISMATCH`, stored-population completeness, staleness protection and an honest benchmark.

## Day 8 acceptance gate — all must pass

1. Full local unit suite passes. **CURRENT: PASS — 120/120 in 52.386 s.**
2. Vantage recorder writes fresh ticks continuously. **CURRENT: NOT PROVEN / latest 300 s benchmark window saw 0 fresh ticks.**
3. Detector backlog is cleared before measurement. **CURRENT: PASS — isolated detector cycle had 0 new bars/backlog and completed in 6.45 s.**
4. Steady-state benchmark observes **3/3 real M1 completions** with fresh ticks and returns PASS; desired target is slowest cycle under 15 s. **CURRENT: INCOMPLETE — 0/3 because no fresh ticks arrived.**
5. Final real differential audit runs **after** the benchmark and reports 0 input mismatches, 0 production/reference semantic mismatches, 0 stored-vs-recomputed semantic differences, complete stored-population coverage, actual trade paths exercised, and no strategy-event mutation during the audit.
6. H4/D1 cannot be called fully audited once they have active research clocks unless their independent calendar/labelling audit is included. W1/MN1 remain disabled until their own exact tick-built/native-bar acceptance gate passes.
7. Reports are reviewed before they are committed as final evidence.

**No Portfolio Simulation and no Vantage demo orders before this gate is clean.**

## Accepted build days

- Day 1 — Research foundations
- Day 2 — Deterministic rules + evidence packs
- Day 3 — Broker, MT5, DB and tick feed
- Day 4 — Own candles + feed/timeframe gate
- Day 5 — Production core maths + research clocks
- Day 6 — Wave-1 pattern/trade engine
- Day 7 — Live research loop + real detections

## Remaining build days

- Day 8 — Real-data differential audit + performance — **IN PROGRESS**
- Day 9 — Runtime hardening and packaging
- Day 10 — Production Portfolio Simulation
- Day 11 — Production Validation Engine
- Day 12 — Vantage demo execution mirror + reconciliation
- Day 13 — Hub data/API layer
- Day 14 — Hub UI + candle pages + operational views
- Day 15 — Full-system launch acceptance and research-start manifest

See `BUILD_CALENDAR.md` for the exact purpose, build work and acceptance gate for every day.

## Launch definitions

**Full Research/Paper Launch** = end of Day 15: continuous feed/detector, strategy evidence, Portfolio Simulation, dedicated Vantage demo mirror and owner Hub functioning without manual coding intervention.

**Real-money Live** is a later owner decision only after the required discovery reviews at months 1/2/3, frozen survivors and untouched post-freeze validation under `VALIDATION_RULES.md`. Build completion does not authorise real money.

## Progress rule

A Build Day is a **gated engineering phase, not necessarily one 24-hour calendar day**. Multiple completed phases may occur on one date and one difficult phase may span several dates. A day is complete only when its documented tests and evidence pass. **No next-day work is accepted while the current day is failed, incomplete or unreviewed.**
