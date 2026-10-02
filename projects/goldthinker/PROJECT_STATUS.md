# GoldThinker — Project Status

**Last updated:** 2026-10-02  
**Authoritative build state:** GoldThinker `docs/PROJECT_STATUS.md` + `docs/BUILD_CALENDAR.md`; this Memory copy mirrors the current state.  
**Current build day:** **Day 8 of 15 — Real-data acceptance (D-058) — IN PROGRESS**  
**Current GoldThinker Day-8 fix:** `b7525bb` — BASE RAW horizon maturation + stale-row repair regression

GoldThinker is a new, separate XAUUSD research system. It does not use AIDY or Super Signals. Its own database is the research source of truth. The dedicated Vantage MT5 demo account is a future execution mirror only.

## Latest verified local evidence

- Owner-machine suite before latest production fix: **125/125 PASS in 54.867 s**.
- Recorder/feed concurrency: **PASS**; no repeat of SQLite writer-lock crash.
- Live-edge performance: **PASS**, 3/3 M1 completions, +1,418 ticks, slowest 13.1 s.
- Independent H4/D1 post-break labelling regressions: **PASS**.
- Earlier 12,711 late-M1 semantic mismatches were an independent-reference early-return schema defect (`canonical.side` absent). The exact `M1 --last 3` failing window now passes 171/171 -> **0 mismatches** after fix `6fbcd8f` + regression `3271d75`.
- **Full M1 rerun after reference fix:** **55,722 positions, 0 production/reference semantic mismatches, 0 input errors, all 5,716 stored occurrences re-found, 437 real trade paths.** Verdict still FAIL only because **14 stored-vs-fresh differences** remained.
- All 14 are stale D-010 BASE RAW horizons: stored `h5/h10/h20` were NULL while fresh deterministic recomputation now has matured values. No canonical/variant/trade semantic disagreement remained.
- Root cause: `live.detector.is_terminal()` could mark a formed BASE/BASE-EARLY row terminal before RAW h1/h3/h5/h10/h20 finished maturing, so the row was never re-evaluated.
- **Production fix `19c78e8`:** formed BASE/BASE-EARLY occurrences remain non-terminal until every RAW horizon is present, even if the virtual trade already closed.
- **Repair command `d8bdaf2`:** `python -m goldthinker.live.repair_raw` reopens historical prematurely-terminal BASE RAW rows; `python -m goldthinker.live.run --once` deterministically refreshes them.
- **Regression `b7525bb`:** covers pending RAW terminal state, closed-trade RAW maturation and stale-row repair selection.
- **Next:** pull latest, run full suite (expected **128 tests**). With recorder still stopped: run repair -> live run once -> repair again and require `reopened 0`. Then rerun full M1. If clean, run M5/M15/M30/H1/H4/D1.

## Day 8 acceptance gate

1. Unit suite — **125/125 pre-latest-fix PASS; rerun expected 128.**
2. Recorder survives concurrent detector workload — **PASS.**
3. Backlog/live-edge condition — **PASS.**
4. Real steady-state benchmark — **PASS.**
5. Final differential audit — **IN PROGRESS:** M1 production/reference semantics are clean; 14 stale stored RAW horizons exposed and are now fixed/repaired in code, pending owner-machine validation + fresh full M1 audit.
6. H4/D1 independent calendar/label audit — **PASS at unit/regression level; include in final real-data audit.** W1/MN1 remain disabled until exact-bar acceptance.
7. Report review/final evidence commit — **pending**.

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
- Day 15 — Full-system launch acceptance + research-start manifest

## Launch definitions

**Full Research/Paper Launch** = end of Day 15. **Real-money Live** is later and requires discovery reviews, frozen survivors and untouched post-freeze validation; build completion does not authorise real money.
