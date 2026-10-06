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

## Day 9 implementation — pending owner-machine validation

- Installable editable package added via `pyproject.toml`; owner command is `goldthinker` and should work in a fresh PowerShell without manual `PYTHONPATH` after `py -m pip install -e .`.
- Owner CLI now includes `start`, `stop`, `status`, `log`, `integrity`, `backup`, `restore`, and Windows `startup` commands.
- Detached supervisor owns recorder and detector as separate workers; either worker is automatically restarted after an unexpected exit.
- Cooperative per-worker stop files allow recorder feed sessions and detector DB connections to close cleanly before a hard-kill fallback.
- `goldthinker start` refuses to launch over a manual recorder that appears to be actively writing fresh ticks.
- Status heartbeat includes supervisor/worker PIDs and restart counts, newest live tick, newest completed M1, detector cursors, last successful detector cycle, strategy-event count and non-terminal count.
- Recorder/detector logs rotate at 5 MB with five backups; supervisor lifecycle/restart log rotates separately.
- SQLite online backup + SHA-256 sidecar + integrity/foreign-key verification implemented. Restore requires runtime stopped, explicit `--yes`, source integrity PASS and post-restore integrity PASS.
- Windows logon recovery helper implemented with `goldthinker startup install|status|remove`.
- Four Day-9 runtime unit tests added. **Expected next owner-machine full suite: 132 tests.**

## Day 9 acceptance still required

1. Pull/install and prove `goldthinker` works in a fresh PowerShell with no `PYTHONPATH`.
2. Full suite PASS (expected 132).
3. Migrate from legacy manual recorder to supervised runtime.
4. Status shows supervisor + recorder + detector healthy with fresh tick/M1/detector heartbeat.
5. Forced recorder crash auto-restarts without duplicate ticks.
6. Forced detector crash auto-restarts without duplicate strategy events.
7. `goldthinker stop` exits workers cooperatively.
8. Integrity + backup + restore drill PASS.
9. Windows startup task test PASS.
10. Supervised soak completes without feed loss, DB lock, restart loop or stale detector.

**No Portfolio Simulation and no Vantage demo orders until Day 9 is accepted.**

## Accepted build days

- Day 1 — Research foundations
- Day 2 — Deterministic rules + evidence packs
- Day 3 — Broker, MT5, DB and tick feed
- Day 4 — Own candles + feed/timeframe gate
- Day 5 — Production core maths + research clocks
- Day 6 — Wave-1 pattern/trade engine
- Day 7 — Live research loop + real detections
- Day 8 — Real-data differential audit + performance

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
