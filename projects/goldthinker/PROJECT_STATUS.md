# GoldThinker — Project Status

**Last updated:** 2026-10-01  
**Authoritative build state:** GoldThinker `docs/PROJECT_STATUS.md` + `docs/BUILD_CALENDAR.md`; this Memory copy mirrors the current state.  
**Current build day:** **Day 8 of 15 — Real-data acceptance (D-058) — IN PROGRESS**  
**Current GoldThinker fix under validation:** `b697841` — detector DB-lock fix + regression test

GoldThinker is a new, separate XAUUSD research system. It does not use AIDY or Super Signals. Its own database is the research source of truth. The dedicated Vantage MT5 demo account is a future execution mirror only.

## Latest verified local evidence

- **Post-fix unit suite: 121/121 PASS in 68.656 s**, including `test_expensive_evaluation_phase_is_read_only`.
- Post-fix feed check: **+86 XAUUSD ticks in 15 s**, latest UTC +15.989 s, spread 21/21.7/29 points, crossed quotes 0, quiet periods 0.
- **Concurrent feed survival now proven:** during the next heavy benchmark catch-up the recorder remained alive and added **4,093 fresh ticks**; the prior `database is locked` crash did not recur.
- The benchmark observed **3/3 genuine M1 completions**. Completion cycles were **15.0 s, 9.9 s, 14.6 s**.
- The benchmark verdict was still **FAIL** because its row labelled `idle, 0 new bars` actually processed **12 new bars** (9 M1, 2 M5, 1 M15) and took **36.9 s**. Those bars accumulated while the preceding long catch-up was running, so this was a contaminated catch-up sample rather than a genuine idle steady-state measurement.
- Detector is now at the live edge. **Next action: rerun the 3/3 benchmark immediately with recorder left running.** Day-8 performance acceptance remains strict: clean PASS and slowest genuine steady-state cycle **<15 s**. If a clean completion cycle is >=15 s, optimize before acceptance.

## Day 8 acceptance gate

1. Unit suite — **PASS: 121/121.**
2. Recorder survives concurrent detector workload — **PASS: +4,093 ticks during heavy catch-up; no lock crash.**
3. Backlog cleared/live edge — **PASS for current state; rerun immediately.**
4. Real steady-state benchmark — **3/3 observed, but clean PASS still required because the measured idle row contained 12 new bars; completion timings 15.0/9.9/14.6 s.**
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
