# GoldThinker — Project Status

**Last updated:** 2026-10-01  
**Authoritative build state:** GoldThinker `docs/PROJECT_STATUS.md` + `docs/BUILD_CALENDAR.md`; this Memory copy mirrors the current state.  
**Current build day:** **Day 8 of 15 — Real-data acceptance (D-058) — IN PROGRESS**  
**Current GoldThinker fix:** `b697841` — detector DB-lock fix + regression test

GoldThinker is a new, separate XAUUSD research system. It does not use AIDY or Super Signals. Its own database is the research source of truth. The dedicated Vantage MT5 demo account is a future execution mirror only.

## Where we are now

Seven gated build days are accepted. **Day 8 is not complete and we do not move to Day 9 until its acceptance gate passes.**

## Latest verified local evidence

- Full pre-fix Windows unit suite: **120/120 PASS in 52.386 s**.
- Candle build in isolation: **0.325 s**.
- Idle detector cycle after backlog clearance: initially **6.45 s**, later true benchmark idle **4.3 s**; both are inside the <15 s target.
- Fresh feed was independently verified before the long catch-up: XAUUSD ticks rose **1,701,290 -> 1,701,422 (+132) in 15 s**, latest UTC advanced 16.369 s, spread **21/21.7/29 points**, crossed quotes 0.
- The long benchmark then replayed the backlog in 40-M1-bar chunks and eventually reached idle, but the recorder died before the live 3/3 measurement. The benchmark ended `INCOMPLETE` with 0 new M1 completions.
- **Confirmed recorder traceback:** `sqlite3.OperationalError: database is locked` from `Store.insert_ticks()` while the detector catch-up was running.
- **Root cause:** `live.detector.run_cycle()` wrote `strategy_events` inside the expensive evaluation loop and committed only at the end of the timeframe. After the first event write, SQLite kept the write transaction for the rest of a 2–3 minute M1 chunk, starving the independent recorder until its 30 s timeout expired.
- **Fix committed in GoldThinker `b697841`:** detector evaluation is now read-only; noteworthy event rows are buffered and flushed atomically with the detector cursor only after the timeframe evaluation finishes. This retains chunk atomicity/idempotence while reducing the writer-lock window from minutes to the short final DB flush.
- New regression test: `tests_unit/test_detector_db_lock.py` verifies the detector connection is not in a write transaction during expensive strategy evaluation.
- GoldThinker status documentation was updated after the code fix. **The fix is not yet accepted** until it is pulled and retested on the owner machine.

## Day 8 acceptance gate

1. Unit suite — **pre-fix PASS 120/120; post-fix rerun required.**
2. Recorder writes fresh ticks continuously while detector is active — **pre-fix FAILED under heavy catch-up due confirmed DB lock; post-fix retest required.**
3. Backlog cleared before measurement — clear any small new backlog after pulling/restarting.
4. Real steady-state benchmark — must observe **3/3 M1 completions**, fresh ticks >0, PASS, slowest cycle <15 s.
5. Final differential audit LAST — 0 input mismatches, 0 semantic mismatches, 0 stored-vs-recomputed differences, all stored occurrences reached, real trades exercised, no event mutation during audit.
6. H4/D1 independent calendar/label audit if their clocks are active; W1/MN1 remain disabled until their own exact-bar acceptance.
7. Review reports before committing final evidence.

**No Portfolio Simulation and no Vantage demo orders before Day 8 is clean.**

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

## Launch definitions

**Full Research/Paper Launch** = end of Day 15: continuous feed/detector, strategy evidence, Portfolio Simulation, dedicated Vantage demo mirror and owner Hub functioning without manual coding intervention.

**Real-money Live** is a later owner decision only after the required discovery reviews at months 1/2/3, frozen survivors and untouched post-freeze validation under `VALIDATION_RULES.md`. Build completion does not authorise real money.

## Progress rule

A Build Day is a **gated engineering phase, not necessarily one 24-hour calendar day**. A day is complete only when its documented tests and evidence pass. **No next-day work is accepted while the current day is failed, incomplete or unreviewed.**
