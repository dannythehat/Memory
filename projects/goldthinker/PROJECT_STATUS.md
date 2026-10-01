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
- Clean live-edge benchmark #1: **3/3 genuine M1 completions, 1,175 fresh ticks**, genuine idle 5.2 s with 0 new bars, completion cycles 12.3 / 6.8 / 17.3 s, verdict WARN because one cycle exceeded the <15 s target.
- **Clean live-edge benchmark #2 PASSED:** 3/3 genuine M1 completions, **1,418 fresh ticks**, slowest measured cycle **13.1 s**. Completion cycles were **13.1 / 7.7 / 10.3 s**. The nominal idle cycle took 7.9 s and one M1 bar completed during it; this did not invalidate the explicit 3/3 post-completion measurements, all of which were below target.
- **Performance and concurrent-feed gates are accepted.** Next action is the final real differential audit, run last with no detector cycle mutating `strategy_events` while it executes.

## Day 8 acceptance gate

1. Unit suite — **PASS: 121/121.**
2. Recorder survives concurrent detector workload — **PASS: +4,093 ticks during heavy catch-up, +1,175 during the WARN benchmark, +1,418 during the PASS benchmark; no lock crash.**
3. Backlog/live-edge condition — **PASS.**
4. Real steady-state benchmark — **PASS: 3/3 M1 completions, +1,418 fresh ticks, slowest 13.1 s; completion cycles 13.1/7.7/10.3 s.**
5. Final differential audit LAST — **pending now**; must show 0 input mismatches, 0 semantic mismatches, 0 stored-vs-recomputed differences, complete stored-population coverage, real trades exercised, and no event mutation.
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
