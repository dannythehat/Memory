# GoldThinker — Project Status

**Last updated:** 2026-10-02  
**Authoritative build state:** GoldThinker `docs/PROJECT_STATUS.md` + `docs/BUILD_CALENDAR.md`; this Memory copy mirrors the current state.  
**Current build day:** **Day 8 of 15 — Real-data acceptance (D-058) — IN PROGRESS**

GoldThinker is a new, separate XAUUSD research system. It does not use AIDY or Super Signals. Its own database is the research source of truth. The dedicated Vantage MT5 demo account is a future execution mirror only.

## Latest verified local evidence

- **Owner-machine unit suite:** **128/128 PASS in 52.750 s**.
- Recorder/feed concurrency: **PASS**; no repeat of SQLite writer-lock crash.
- Live-edge performance: **PASS**, 3/3 M1 completions, +1,418 ticks, slowest 13.1 s.
- Earlier 12,711 late-M1 semantic mismatches were an independent-reference early-return schema defect; the exact failing window now passes 171/171 -> 0 mismatches after fix `6fbcd8f` + regression `3271d75`.
- **Full M1 semantic differential evidence:** 55,722 positions, 0 production/reference semantic mismatches, 0 input errors, all 5,716 stored occurrences re-found, 437 real trade paths. The only failure was 14 stale stored RAW horizons.
- RAW persistence root cause fixed: BASE/BASE-EARLY rows no longer become terminal before h1/h3/h5/h10/h20 mature. Production fix `19c78e8`, repair command `d8bdaf2`, regression `b7525bb`.
- **Repair validation PASS:** first repair scan reopened **247** stale BASE RAW rows; `python -m goldthinker.live.run --once` completed normally (12,223 evaluations / 2,157 stored updates); second repair scan returned **0 stale BASE RAW rows**.
- Next M1 verification should be a focused stored-consistency check, not another blind multi-hour semantic rerun, because the 55,722-position semantic population already passed and the subsequent code change touched persistence/terminality rather than evaluation semantics.
- Remaining real differential acceptance still required for M5/M15/M30/H1/H4/D1. H4/D1 independent calendar/label regressions already pass. W1/MN1 remain disabled.

## Day 8 acceptance gate

1. Unit suite — **PASS: 128/128.**
2. Recorder concurrency — **PASS.**
3. Backlog/live-edge — **PASS.**
4. Steady-state benchmark — **PASS.**
5. M1 semantic differential — **PASS evidence:** 55,722/55,722, 0 mismatches, 437 trades; stale RAW history repaired to zero, focused stored consistency still pending.
6. M5/M15/M30/H1/H4/D1 differential — **pending.**
7. Report review/final evidence commit — **pending.**

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
