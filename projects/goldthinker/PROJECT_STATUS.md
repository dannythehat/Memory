# GoldThinker — Project Status

**Last updated:** 2026-10-02  
**Authoritative build state:** GoldThinker `docs/PROJECT_STATUS.md` + `docs/BUILD_CALENDAR.md`; this Memory copy mirrors the current state.  
**Current build day:** **Day 8 of 15 — Real-data acceptance (D-058) — IN PROGRESS**

GoldThinker is a new, separate XAUUSD research system. It does not use AIDY or Super Signals. Its own database is the research source of truth. The dedicated Vantage MT5 demo account is a future execution mirror only.

## Latest verified local evidence

- **Owner-machine unit suite:** **128/128 PASS in 52.750 s**.
- Recorder/feed concurrency: **PASS**; no repeat of SQLite writer-lock crash.
- Live-edge performance: **PASS**, 3/3 M1 completions, +1,418 ticks, slowest 13.1 s.
- **M1 semantic differential evidence:** 55,722 positions, 0 semantic mismatches, 0 input errors, all 5,716 stored occurrences re-found, 437 real trade paths. Historical RAW persistence bug repaired: 247 stale BASE rows reopened/recomputed and follow-up scan returned 0 stale rows.
- **M5 differential PASS:** 12,900 positions, 0 mismatches, 0 stored-vs-recomputed, 0 input errors, all 1,663 stored occurrences re-found, 153 trades.
- **M15/M30/H1/H4 combined differential PASS:** 0 semantic mismatches, 0 stored-vs-recomputed differences, 0 input errors and 0 unreached stored occurrences. M15: 4,263 positions, 43 trades, 553/553 stored. M30: 2,153 positions, 12 trades, 267/267 stored. H1: 1,287 positions, 15 trades, 154/154 stored. H4: 72 positions, 0 trades, 12/12 stored.
- **D1 in that report had 0 units / 0 positions / 0 stored occurrences**, meaning no D1 strategy research clocks were active in the DB snapshot. Day-8 rules require H4/D1 independent real-data coverage only when their clocks are active; H4 was active and passed. One quick D1 capability report remains to record why its clocks are not active and confirm the zero population is expected readiness rather than an omission.
- W1/MN1 remain disabled.

## Day 8 acceptance gate

1. Unit suite — **PASS: 128/128.**
2. Recorder concurrency — **PASS.**
3. Backlog/live-edge — **PASS.**
4. Steady-state benchmark — **PASS.**
5. M1 semantic differential + repaired RAW persistence — **PASS evidence.**
6. M5 differential — **PASS.**
7. M15/M30/H1/H4 differential — **PASS.**
8. D1 readiness explanation — **one quick capability check pending**; no D1 clocks were active during the audit.
9. Final report/evidence commit — **pending the D1 readiness check.**

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

- Day 8 — Real-data differential audit + performance — **IN PROGRESS (one D1 readiness check remains)**
- Day 9 — Runtime hardening and packaging
- Day 10 — Production Portfolio Simulation
- Day 11 — Production Validation Engine
- Day 12 — Vantage demo execution mirror + reconciliation
- Day 13 — Hub data/API layer
- Day 14 — Hub UI + candle pages + operational views
- Day 15 — Full-system launch acceptance + research-start manifest

## Launch definitions

**Full Research/Paper Launch** = end of Day 15. **Real-money Live** is later and requires discovery reviews, frozen survivors and untouched post-freeze validation; build completion does not authorise real money.
