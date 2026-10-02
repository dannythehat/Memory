# GoldThinker — Project Status

**Last updated:** 2026-10-02  
**Authoritative build state:** GoldThinker `docs/PROJECT_STATUS.md` + `docs/BUILD_CALENDAR.md`; this Memory copy mirrors the current state.  
**Current build day:** **Day 9 of 15 — Runtime hardening + packaging — IN PROGRESS**  
**Day 8:** **ACCEPTED**

GoldThinker is a new, separate XAUUSD research system. It does not use AIDY or Super Signals. Its own database is the research source of truth. The dedicated Vantage MT5 demo account is a future execution mirror only.

## Day 8 final evidence

- Unit suite: **128/128 PASS in 52.750 s**.
- Recorder/feed concurrency: PASS.
- Steady-state benchmark: PASS — 3/3 genuine M1 completions, +1,418 fresh ticks, slowest 13.1 s.
- M1 semantic differential: **55,722 positions, 0 production/reference mismatches, 0 input errors, 5,716/5,716 stored occurrences re-found, 437 trades**.
- BASE RAW persistence defect fixed and regression-tested. Historical repair reopened 247 stale rows; deterministic recomputation completed; second repair scan returned **0 stale BASE RAW rows**.
- M5 differential: PASS — 12,900 positions, 0 mismatches/stored differences/input errors/unreached, 1,663/1,663 stored, 153 trades.
- M15 differential: PASS — 4,263 positions, 0 mismatches/stored differences/input errors/unreached, 553/553 stored, 43 trades.
- M30 differential: PASS — 2,153 positions, 0 mismatches/stored differences/input errors/unreached, 267/267 stored, 12 trades.
- H1 differential: PASS — 1,287 positions, 0 mismatches/stored differences/input errors/unreached, 154/154 stored, 15 trades.
- H4 differential: PASS — 72 positions, 0 mismatches/stored differences/input errors/unreached, 12/12 stored. Independent H4/D1 post-break calendar regressions pass.
- D1 has **0 research clocks by design**: only 3 complete D1 bars exist, only 1 post-enable, while strategy readiness requires 16–102 bars. Therefore no D1 strategy population is eligible yet; 0 audited units is expected, not a failure.
- W1/MN1 remain disabled until their own exact tick-built/native-bar acceptance.

**Day 8 verdict: ACCEPTED.**

## Accepted build days

- Day 1 — Research foundations
- Day 2 — Deterministic rules + evidence packs
- Day 3 — Broker, MT5, DB and tick feed
- Day 4 — Own candles + feed/timeframe gate
- Day 5 — Production core maths + research clocks
- Day 6 — Wave-1 pattern/trade engine
- Day 7 — Live research loop + real detections
- Day 8 — Real-data differential audit + performance

## Current build day

### Day 9 — Runtime hardening + packaging — IN PROGRESS

Requirements: installable package with no manual `PYTHONPATH`; one start/stop/status workflow; separate recorder/detector supervision; runtime heartbeat; structured rotating logs; DB backup/restore + integrity check; Windows reboot/startup recovery; restart/idempotence tests; supervised soak before acceptance.

**No Portfolio Simulation and no Vantage demo orders until Day 9 is accepted.**

## Remaining build days

- Day 9 — Runtime hardening and packaging — IN PROGRESS
- Day 10 — Production Portfolio Simulation
- Day 11 — Production Validation Engine
- Day 12 — Vantage demo execution mirror + reconciliation
- Day 13 — Hub data/API layer
- Day 14 — Hub UI + candle pages + operational views
- Day 15 — Full-system launch acceptance + research-start manifest

## Launch definitions

**Full Research/Paper Launch** = end of Day 15. **Real-money Live** is later and requires discovery reviews, frozen survivors and untouched post-freeze validation; build completion does not authorise real money.
