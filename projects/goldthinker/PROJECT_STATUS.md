# GoldThinker — Project Status

**Last updated:** 2026-10-01  
**Authoritative build state:** GoldThinker `docs/PROJECT_STATUS.md` + `docs/BUILD_CALENDAR.md`; this Memory copy mirrors the current state.  
**Current build day:** **Day 8 of 15 — Real-data acceptance (D-058) — IN PROGRESS**  
**Current GoldThinker Day-8 fix:** `3271d75` — reference gap/warm-up canonical-side identity + regression test

GoldThinker is a new, separate XAUUSD research system. It does not use AIDY or Super Signals. Its own database is the research source of truth. The dedicated Vantage MT5 demo account is a future execution mirror only.

## Latest verified local evidence

- **Current owner-machine unit suite: 125/125 PASS in 54.867 s.** This includes the new early-return canonical-side regression plus the prior H4/D1 and detector-lock regressions.
- Recorder/feed concurrency fix is proven under heavy load; no repeat of `sqlite3.OperationalError: database is locked`.
- **Follow-up live-edge benchmark PASSED:** **3/3 real M1 completions**, **1,418 fresh ticks**, slowest measured cycle **13.1 s**; completion cycles **13.1 / 7.7 / 10.3 s**.
- Independent H4/D1 post-break labelling is unit-tested: 01:00 reopen -> H4/D1 00:00, H1 and lower 01:00.
- The first full differential run reached 43,000 M1 comparisons with 0 mismatches, then accumulated **12,711 M1 mismatches** before moving to M5; observed M5 work did not add mismatches.
- Quick diagnostic `M1 --last 3` produced **171/171 mismatches**, all the same field: production `.canonical.side` = BULL/BEAR/NEUTRAL vs independent reference absent. All 171 were gap/warm-up early-return rows with 0 detections/signals/trades.
- **Root cause + fix:** the scratch reference added canonical side only after detection, while production defines it before readiness/data-gap exits. Fix `6fbcd8f` retains strategy side on reference early returns, independently derived from the reference strategy id; regression `3271d75` covers BULL/BEAR/NEUTRAL.
- **Targeted post-fix verification PASS:** the exact `M1 --last 3` window now reports **171 compared, 0 mismatches, 0 stored-vs-recomputed differences, 0 input errors, 0 stored occurrences not reached**.
- **Next:** keep DB frozen; run the complete M1 population first. If M1 passes, run M5/M15/M30/H1/H4/D1. Final Day-8 acceptance still requires zero semantic/input/stored differences, complete stored-population coverage, real trade paths, and no event mutation across the full accepted set.

## Day 8 acceptance gate

1. Unit suite — **PASS: 125/125 in 54.867 s.**
2. Recorder survives concurrent detector workload — **PASS.**
3. Backlog/live-edge condition — **PASS.**
4. Real steady-state benchmark — **PASS: 3/3, +1,418 fresh ticks, slowest 13.1 s.**
5. Final differential audit — **IN PROGRESS:** targeted failing window is now clean; full-population rerun still required.
6. H4/D1 independent calendar/label audit — **PASS at unit/regression level; include in final real-data audit.** W1/MN1 remain disabled until exact-bar acceptance.
7. Review reports before final evidence commit — **pending**.

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
