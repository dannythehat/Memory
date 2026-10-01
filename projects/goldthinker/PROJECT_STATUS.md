# GoldThinker — Project Status

**Last updated:** 2026-10-01  
**Authoritative build state:** GoldThinker `docs/PROJECT_STATUS.md` + `docs/BUILD_CALENDAR.md`; this Memory copy mirrors the current state.  
**Current build day:** **Day 8 of 15 — Real-data acceptance (D-058) — IN PROGRESS**  
**Current GoldThinker fix under validation:** `b697841` — detector DB-lock fix + regression test

GoldThinker is a new, separate XAUUSD research system. It does not use AIDY or Super Signals. Its own database is the research source of truth. The dedicated Vantage MT5 demo account is a future execution mirror only.

## Latest verified local evidence

- **Post-fix unit suite: 121/121 PASS in 68.656 s**, including `test_expensive_evaluation_phase_is_read_only`.
- Post-fix feed check: **+86 XAUUSD ticks in 15 s**, latest UTC +15.989 s, spread 21/21.7/29 points, crossed quotes 0, quiet periods 0.
- **Concurrent feed survival proven:** during heavy benchmark catch-up the recorder remained alive and added **4,093 fresh ticks**; the prior `database is locked` crash did not recur.
- First post-fix 3/3 benchmark had a contaminated nominal idle row that actually processed 12 new bars, so its 36.9 s FAIL was not a genuine steady-state idle sample.
- **Clean live-edge benchmark:** 3/3 genuine M1 completions, **1,175 fresh ticks**, genuine idle **5.2 s with 0 new bars**, completion cycles **12.3 s / 6.8 s / 17.3 s**, verdict **WARN** because the slowest genuine cycle exceeded the <15 s Day-8 target.
- The 17.3 s cycle was mostly detector time (**15.72 s**); timeframe timings were roughly M1 4.4 s, M5 0.2 s, M15 0.5 s, M30 5.8 s, H1 4.8 s. If repeated, optimise M30/H1 open-occurrence/tick-loading work.
- **Next action:** one more clean 3/3 benchmark immediately at the live edge with recorder running. PASS if all genuine cycles are <15 s. If another WARN/FAIL occurs, optimise before acceptance.

## Day 8 acceptance gate

1. Unit suite — **PASS: 121/121.**
2. Recorder survives concurrent detector workload — **PASS: +4,093 ticks during catch-up and +1,175 during the clean benchmark; no lock crash.**
3. Backlog cleared/live edge — **PASS: clean idle sample had 0 new bars, 5.2 s.**
4. Real steady-state benchmark — **3/3 observed with fresh ticks, but current clean verdict WARN due one 17.3 s cycle; one more clean run required, optimise if repeated.**
5. Final differential audit LAST — still pending; must show 0 input mismatches, 0 semantic mismatches, 0 stored-vs-recomputed differences, complete stored-population coverage, real trades exercised, and no event mutation.
6. H4/D1 independent calendar/label audit if clocks active; W1/MN1 remain disabled until exact-bar acceptance.
7. Review reports before final evidence commit.

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

**Full Research/Paper Launch** = end of Day 15. **Real-money Live** is later and requires discovery reviews, frozen survivors and untouched post-freeze validation; build completion does not authorise real money.
