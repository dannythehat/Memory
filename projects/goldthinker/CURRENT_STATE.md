# GoldThinker — Current State

**Updated:** 2026-10-01  
**Authoritative status:** `PROJECT_STATUS.md`  
**Gated roadmap:** `BUILD_CALENDAR.md`  
**Current build day:** **Day 8 of 15 — Real-data differential audit + steady-state performance — IN PROGRESS**

GoldThinker is completely separate from AIDY and Super Signals. It has its own Vantage feed, database, code, research clocks and result ledgers. No Super Signals resource is reused.

## Current position

Days 1-7 of the gated build calendar are accepted. We do **not** move to Day 9 until Day 8 passes its full acceptance gate.

The core research machine is substantially built:

- research/source foundations and Candle Spec Draft 0.3.2;
- deterministic ambiguity rulings A-01..A-30;
- 1,408 pattern-family vectors, 24 portfolio vectors, 10 validation vectors;
- dedicated Vantage demo account and credential-free real broker specification;
- own SQLite tick store, broker-wall clock normalisation, dedupe/resume/reconnect;
- own BID/ASK candles built from ticks;
- native-MT5 reconciliation and per-timeframe gate;
- exact production core calculations;
- Wave-1 production pattern detectors, BASE/SOURCE-NORMALIZED variants, virtual execution, RAW measurements, overlap clusters and hub counters;
- per-strategy research clocks and point-in-time news vintages;
- live research detector loop, event persistence, catch-up and read-only reporting;
- independent production-vs-reference real-data audit and steady-state benchmark.

The finished product still needs:

- Day 8 final acceptance;
- runtime packaging/supervision;
- production Portfolio Simulation;
- production validation engine;
- Vantage demo execution mirror and reconciliation;
- Hub backend/API and owner-facing UI;
- final full-system launch acceptance.

## Latest local evidence

- **120 local unit tests passed** on the current D-058 build.
- GoldThinker's Vantage tick recorder was restarted successfully and reported `feed connected`.
- Earlier real detector snapshot stored **655 occurrences, including 78 virtual trades**; no broker orders were sent.
- The first real differential audit was rejected because the audit itself starved later positions of ticks. The harness was then corrected with complete tick coverage, independent raw-SQL reference loaders, `INPUT_MISMATCH`, population completeness and staleness guards.
- Latest benchmark attempt processed backlog caused by the recorder previously being down: **151 new bars, 8,679 evaluations, 1,184 stored results, 394.1 s**. That is not accepted as steady state. A clean rerun requires a continuously running recorder and cleared backlog.

## Day 8 desired outcome

Day 8 is complete only when:

1. full local suite passes;
2. recorder writes fresh ticks continuously;
3. backlog is cleared before timing;
4. benchmark observes 3/3 genuine M1 completions and returns PASS with the desired target of <15 s slowest cycle;
5. differential audit runs LAST and returns zero input mismatches, zero production/reference semantic mismatches, zero stored-vs-recomputed semantic differences, complete stored-population coverage, actual trade paths exercised and no event mutation during the audit;
6. newly active H4/D1 clocks are included in independent audit coverage before claiming full detector audit acceptance;
7. final reports are reviewed before they are committed as accepted evidence.

**Until this passes: no Portfolio Simulation implementation is accepted and no Vantage demo orders are enabled.**

## Launch meaning

**Full Research/Paper Launch** is the end of Build Day 15: continuous feed/detector, strategy evidence, Portfolio Simulation, dedicated Vantage demo mirror and owner Hub work without manual coding intervention.

**Real-money Live** is not part of the 15 build days. The owner requirement remains: discovery reviews at months 1/2/3, freeze survivors, then untouched post-freeze validation under `VALIDATION_RULES.md`. Only a validated PASS-STRONG candidate may ever be presented to the owner for a real-money decision.

## Governance

A Build Day is a gated engineering phase, not automatically one 24-hour period. Several completed phases can occur on the same date; a failed/incomplete phase can take several dates. **No next Build Day is accepted until the current day's code, tests and evidence have passed and been reviewed.**

Read `BUILD_CALENDAR.md` for Day 1 through Day 15 and `DECISIONS.md` for the full decision history.
