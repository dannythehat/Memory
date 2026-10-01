# GoldThinker — Project Status

**Last updated:** 2026-10-01  
**Authoritative build state:** GoldThinker `docs/PROJECT_STATUS.md` + `docs/BUILD_CALENDAR.md`; this Memory copy mirrors the current state.  
**Current build day:** **Day 8 of 15 — Real-data acceptance (D-058) — IN PROGRESS**  
**Current GoldThinker Day-8 fix:** `3271d75` — reference gap/warm-up canonical-side identity + regression test

GoldThinker is a new, separate XAUUSD research system. It does not use AIDY or Super Signals. Its own database is the research source of truth. The dedicated Vantage MT5 demo account is a future execution mirror only.

## Latest verified local evidence

- **Owner-machine unit suite before latest fix: 124/124 PASS in 66.569 s.**
- Recorder/feed concurrency fix is proven under heavy load; no repeat of `sqlite3.OperationalError: database is locked`.
- **Follow-up live-edge benchmark PASSED:** **3/3 real M1 completions**, **1,418 fresh ticks**, slowest measured cycle **13.1 s**; completion cycles **13.1 / 7.7 / 10.3 s**.
- Independent H4/D1 post-break labelling is unit-tested: 01:00 reopen -> H4/D1 00:00, H1 and lower 01:00.
- The full differential run reached 43,000 M1 comparisons with 0 mismatches, then accumulated **12,711 M1 mismatches** before moving to M5; observed M5 work did not add mismatches.
- Quick diagnostic `M1 --last 3` produced **171/171 mismatches**, all the same field: production `.canonical.side` = BULL/BEAR/NEUTRAL vs independent reference `<absent>`. All 171 were gap/warm-up early-return rows with 0 detections/signals/trades.
- **Root cause:** production defines canonical side from the strategy unit before readiness/data-gap checks; the scratch reference historically added it only after detection. Thus early `NOT_EVALUATED_WARMUP` / `NOT_EVALUATED_DATA_GAP` outputs were schema-incomplete on the reference side. This is an audit/reference defect, not evidence of production semantic divergence for those rows.
- **Fix `6fbcd8f` + regression `3271d75`:** independent reference now retains strategy side on early returns, deriving it independently from its own strategy id (`NEUTRAL` for P08/P09). Added BULL/BEAR/NEUTRAL early-return regression coverage.
- **Next:** pull latest, rerun full suite (expected **125 tests**), then rerun `py -m goldthinker.audit.real_differential --tf M1 --last 3`. It must return 0 mismatches before any full multi-timeframe audit rerun.

## Day 8 acceptance gate

1. Unit suite — **124/124 pre-fix PASS; rerun latest, expected 125.**
2. Recorder survives concurrent detector workload — **PASS.**
3. Backlog/live-edge condition — **PASS.**
4. Real steady-state benchmark — **PASS: 3/3, +1,418 fresh ticks, slowest 13.1 s.**
5. Final differential audit — **blocked pending validation of the reference early-return side fix, then full rerun.**
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
