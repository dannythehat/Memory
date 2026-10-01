# GoldThinker — Current Handover

**Updated:** 2026-10-01  
**Primary repo:** `dannythehat/GoldThinker`  
**Working branch:** `claude/trading-bot-prompt-review-hrxbkw`  
**Authoritative status:** `PROJECT_STATUS.md`  
**Gated roadmap:** `BUILD_CALENDAR.md`  
**Current build day:** **Day 8 of 15 — D-058 real-data acceptance — IN PROGRESS**

## Process / governance

- GoldThinker is a new system. Do not import AIDY or Super Signals architecture, data, rules or trading authority.
- Owner decides product/business choices and anything involving real money.
- Claude + ChatGPT settle trading-research and engineering rules, challenge each other and preserve source evidence.
- Same candle + same available data must produce the same deterministic result.
- A Build Day is a gated phase. **Do not advance to the next Build Day until the current day's implementation, tests and evidence pass and are reviewed.**
- Current Day 8 stays IN PROGRESS until the desired clean benchmark + real differential audit outcome is achieved.

## What GoldThinker is

A rules-based XAUUSD research machine that records its own Vantage ticks, builds its own BID/ASK candles, detects deterministic strategies by pattern x side x timeframe x variant x version, records formations/signals/virtual trades, keeps isolated strategy R-ledgers, will later maintain a separate EUR 10,000 Portfolio Simulation, will mirror Portfolio Simulation trades to the dedicated Vantage demo account, will expose one owner Hub, and will use months 1/2/3 discovery followed by untouched frozen validation before any real-money discussion.

## Accepted build days

- **Day 1 — Research foundations**
- **Day 2 — Deterministic rules/evidence packs**
- **Day 3 — Broker/feed/DB**
- **Day 4 — Own candles/feed gate**
- **Day 5 — Production core/research clocks**
- **Day 6 — Wave-1 production pattern/trade engine**
- **Day 7 — Live research loop + real detections**

Full detail and each acceptance gate are in `BUILD_CALENDAR.md`.

## Current Day 8 — D-058 acceptance

### Latest local facts

- Current D-058 code reviewed before documentation update: GoldThinker `0eef777`.
- Local Windows suite: **120 tests pass**.
- Dedicated Vantage tick recorder has been restarted and reports `feed connected`.
- Earlier major real run stored **655 occurrences / 78 virtual trades / 9 open** at that snapshot. Nothing was sent to a broker.
- First real differential audit was rejected because the audit shared a truncated tick input and therefore exercised zero trades. That was an audit-harness defect, not accepted detector evidence.
- Fixes in `c0c8d89`, `a2cbcf1`, `0eef777`: complete later tick coverage, truncation/input errors, independent raw-SQL reference bars/ticks/offsets, `INPUT_MISMATCH`, stored-population completeness, staleness guard, non-vacuous trade checks, honest benchmark, faster reference tick objects and benchmark-first/audit-last orchestration.
- Latest benchmark attempt was backlog catch-up after the recorder had been down: **394.1 s, 151 new bars, 8,679 evaluations, 1,184 stored**. Idle was 2.1 s. This is not steady-state acceptance evidence. Clean rerun with continuous recorder is the current task.

### Day 8 acceptance — all required

1. Full unit suite passes.
2. Fresh ticks continue arriving.
3. Detector backlog is cleared before timing.
4. Benchmark observes **3/3 genuine M1 completions** and returns PASS with desired slowest cycle **<15 s**.
5. Differential audit runs **LAST** with 0 `INPUT_MISMATCH`, 0 semantic production/reference mismatches, 0 stored-vs-recomputed differences, all stored events in scope reached, real trade paths exercised, and no `strategy_events` mutation during audit.
6. If H4/D1 have active research clocks, independent audit coverage must include/resolve them before full detector acceptance.
7. Final reports are reviewed before being committed as accepted evidence.

**No Day 9, Portfolio Simulation or Vantage demo orders until Day 8 passes.**

## Remaining build days to Full Research/Paper Launch

- Day 9 — Runtime hardening and packaging
- Day 10 — Production Portfolio Simulation
- Day 11 — Production Validation Engine
- Day 12 — Vantage demo execution mirror/reconciliation
- Day 13 — Hub data/API layer
- Day 14 — Hub UI + candle pages + operational views
- Day 15 — Full-system launch acceptance + frozen launch manifest

## Technical foundations that must not drift

- Timeframes: M1, M5, M15, M30, H1, H4, D1, W1, MN1.
- W1/MN1 remain disabled until their own completed tick-built BID bar exactly matches native MT5.
- Strategy unit = pattern x side x timeframe x variant x version. Do not pool samples across TF/variant/version.
- Strategy ledgers are fixed non-compounding R evidence. Portfolio Simulation is a separate compounding EUR 10,000 account. Vantage demo is a separate execution mirror.
- 1R strategy reference = 100 reference units. Portfolio base risk = 1% current EUR equity under D-042.
- BUY entry uses ASK; SELL entry uses BID. Buy stops/targets execute on BID; sell stops/targets on ASK.
- Max hold = 50 bars of the pattern's own timeframe.
- Missing/ambiguous same-bar execution is never deleted; STOP-FIRST + target-first sensitivity where required.
- Point-in-time news only; later knowledge cannot backfill earlier decisions.
- Commission unknown means unknown, not zero; net R stays pending until cost evidence exists.
- GoldThinker DB is research source of truth. Native MT5 bars are reconciliation only.
- No real-money authority exists.

## Runtime/local notes

- Windows local machine hosts the real MT5 terminal and official MetaTrader5 Python package.
- Owner repo path: `C:\Users\Admin\Desktop\GoldThinker`.
- Recorder runs in its own window while benchmark/detector runs.
- Fresh PowerShell currently needs the repo `src` import path until Day 9 packages the project properly:

```powershell
cd C:\Users\Admin\Desktop\GoldThinker
$env:PYTHONPATH="$PWD\src"
py -m goldthinker.feed.run_ingest
```

- Day-8 orchestration:

```powershell
powershell -ExecutionPolicy Bypass -File tools\final_audit.ps1
```

It runs tests/candles/detector, benchmark FIRST, differential audit LAST, stops on failed gates and asks before committing reports.

## Launch meanings

**Full Research/Paper Launch:** end of Day 15. Continuous feed/detector + strategy evidence + Portfolio Simulation + Vantage demo mirror + owner Hub operate as one recoverable system.

**Real-money Live:** later owner decision only after required discovery and frozen validation. Day 15 does not authorise real-money trading.

## New-session instruction

Read in this order: `PROJECT_STATUS.md`, `BUILD_CALENDAR.md`, `CURRENT_STATE.md`, then `DECISIONS.md` and rule docs as needed. Continue **only the current Build Day** until its acceptance gate passes.
