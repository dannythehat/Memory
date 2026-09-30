# GoldThinker — handover (2026-09-30)

This file lets a brand-new Claude session continue with no chat history.

## People and process

- **Owner: Danny (`dannythehat`).** Decides product/business choices and anything involving real money. Original requirements D-001..D-005 and D-022 are his.
- **Reviewer: ChatGPT.** Danny relays messages between Claude and ChatGPT by pasting them; the pasted text is ChatGPT's, not Danny's. Under D-035 (Danny's forwarded instruction) **Claude and ChatGPT settle trading-research and engineering rules themselves and challenge each other; neither should simply agree.** Danny is needed only for product/business choices and real-money matters. If Danny's own words are absent from a paste, act on the technical content, and say so when a decision touches something owner-level.
- **Style Danny wants:** concise reports; do not jump ahead or presume; do not repeat "no win rates / not proven" caveats; do not change the spec just to make a test pass (flag a genuine ambiguity instead); do not put model identifiers in repository files.

## Where things stand

- Spec `docs/CANDLE_SPEC_V1.md` Draft 0.3.2 (all ambiguities A-01..A-30 ruled; D-038 zone-death rule, PIP_SRC_USD = 0.10 confirmed D-040).
- `docs/VALIDATION_RULES.md` v0.3 and `docs/PORTFOLIO_RULES.md` v0.2: RESEARCH APPROVED — Claude + ChatGPT (D-041, D-042).
- Test packs in `tests/`: 1,408 pattern-family vectors, 24 portfolio vectors, 10 validation vectors. The scratch calculators in `reference/` reproduce them with zero mismatches (`assemble.py` prints `BAD 0`).
- **D-005 (nothing built until foundations agreed) is satisfied** as of 2026-09-30 (row in `docs/DECISIONS.md`; revocable by Danny).
- **Nothing of the detector exists yet.** This repository was created empty by Danny on 2026-09-30 and holds only docs, tests and reference calculators.

## Update 2026-09-30 (later): MT5 connection and feed foundations (D-044)

- The owner confirmed the local MT5 connection to the dedicated demo account works (server `VantageMarkets-Demo`, EUR, EUR 10,000, leverage 500:1, official `MetaTrader5` package, `.env` local and Git-ignored). Credentials are never in this repository or in chat; Claude never has them.
- **Claude's cloud sessions cannot reach MT5** (Windows-only package + a local terminal). So the live specification is captured by `tools/mt5_probe.py`, run locally by the owner, which writes credential-free `config/broker_spec.json` + `config/BROKER_SPEC.md`. **Until those files exist in the repo the real broker values are still unknown and the fixtures stand.**
- Built and unit-tested (9 tests, no MT5 needed): SQLite schema (`src/goldthinker/db/schema.sql`: integer-point prices, raw server-clock time plus derived UTC, sessions, measured server offsets, quiet periods), tick ingester (`src/goldthinker/feed/`), MT5 source, report. Setup: `docs/LOCAL_SETUP.md`.
- Design decisions (Claude's, for ChatGPT to challenge): SQLite first (stdlib, no install; schema is portable SQL) - the hosting/database choice stays open until the hub is built; MT5 times are server-clock epochs, so UTC is derived with an offset measured only from ticks that first appear live after the session started (stale ticks can mimic a valid offset), with the raw time always kept so UTC can be recomputed; ticks are deduplicated by (symbol, time_msc, bid, ask, flags).
- **Fixtures vs real values:** the golden vectors keep their synthetic fixture (they must stay reproducible). Production takes the real values from `config/broker_spec.json` as configuration; nothing in the vectors is regenerated. Items to replace once the probe output arrives: tick size/value and contract size (EUR values), lot min/step/max, swap mode/long/short/triple day, commission, margin, real server offset and DST behaviour (the fixture assumed UTC+1 with no DST, which affects the D1/W1/MN1 boundaries and the calendar), real sessions/pause, EURUSD symbol. Record them in `docs/CANDLE_SPEC_V1.md` G0/G9 "TO CONFIRM" items and `docs/PORTFOLIO_RULES.md` section 9.
- **Timestamps (owner-verified 2026-09-30):** raw MT5 time is the broker wall-clock encoded as an epoch, currently UTC+3 (XAUUSD +10,800 s, EURUSD +10,799 s). D1 bars open 00:00 broker time, H4 at 00/04/08/12/16/20, H1 on whole broker hours. The offset is measured from fresh ticks (both symbols must agree, plausible timezone bounds, quarter-hour rounding), versioned in `server_offsets`, re-measured across DST and the wall-clock jump back is handled (`CLOCK_BACKWARD`). Details: `docs/BROKER_OBSERVATIONS.md`. Golden-vector calendar fixtures are unchanged.
- Password note: the owner's correction (a lowercase `l`, not a capital `I`) needs no change here: no credential was ever stored in any repository or record.

## Update 2026-09-30 (evening): candles and the acceptance gate (D-046)

- The live recorder is running against Vantage (first report: 340 ticks, spread 21-22 points, no crossed quotes, UTC normalisation correct). The real broker specification is committed (`config/broker_spec.json`, `config/BROKER_SPEC.md`; hedging account, EUR 10,000, 500:1, XAUUSD 2 digits, contract 100, tick 0.01 = EUR 0.88/lot, swap in points -79.48 long / +34.41 short, triple Wednesday, D1 00:00 and H4 00/04/08/12/16/20 broker time, week open Mon 01:00, daily break about 23:58-01:00 PROVISIONAL, EURUSD available). The golden-vector fixtures are unchanged.
- The recorder stays the only source. **Our own BID and ASK candles M1..MN1 are built from the ticks** (`src/goldthinker/candles/`); native MT5 bars are used for reconciliation only (`tools/reconcile_candles.py`). Boundaries are in the broker wall-clock domain; W1 = Sunday 00:00 is an assumption the reconciliation confirms or refutes (a one-constant change).
- Feed-health acceptance report (`python -m goldthinker.feed.health`): evidence volume, tick continuity (against the PROVISIONAL calendar `config/broker_calendar.json`), spread distribution, duplicates, out-of-order ticks, UTC normalisation incl. live latency, completed candles and boundaries vs native MT5, and a gate that enables pattern detection **per timeframe only** when that timeframe reproduces the native candles exactly with enough compared bars. Nothing is enabled until the first real reconciliation has been run and its report reviewed.
- Next: run the four commands in `docs/LOCAL_SETUP.md` step 6, push `reports/`, review; then the shared calculations (ATR, swings, zones...) on top of the verified candles.

## Update 2026-09-30 (night): gate, first production code (D-047, D-048)

- Reconciliation accepted; timeframes M1-D1 are enabled for detection, W1/MN1 are not (see D-047). Apply with: `git pull; python tools/reconcile_candles.py; python -m goldthinker.feed.health --update-gate` (the last command writes `reports/` and updates the runtime gate table `timeframe_gate`; the detector must call `goldthinker.gate.require_enabled(con, tf)`).
- **There is no production detector yet.** The "tested detector/event pipeline" people refer to is the scratch reference calculator in `reference/`, not product code. The production build started: `src/goldthinker/core/` holds the shared exact-rational functions; all 51 global golden vectors reproduce (`python -m unittest tests_unit.test_golden_global`). Still to build, in this order: pattern detectors (P01..P22 + early companions) and variants, event model (G0b), execution/RAW (G9/G10), hub counters, then portfolio and validation functions. Then the detector loop over completed bars, calendar built from `config/broker_spec.json` + versioned offsets (wall-clock domain), and only after live output is audited: Vantage demo execution.
- No demo/live execution of any kind yet (owner/ChatGPT decision).

## Update 2026-09-30 (late night): production detectors (D-049, D-050)

- Production pattern layer done and golden-tested: `python -m unittest discover -s tests_unit` reproduces the 51 global, 1,329 pattern, 21 overlap and 7 hub vectors exactly. Read `src/goldthinker/patterns/` (spec, canonical, variants, targets, execution, raw, strategy, clusters, readiness), `src/goldthinker/core/`, `src/goldthinker/hub/`.
- New rules: feed gate != strategy readiness; each strategy has its own `research_start` (`goldthinker.research`), computed by `python -m goldthinker.feed.health --update-gate`; reviews count from it. Provisional wall-clock broker calendar: `core/broker_calendar.py` (+ `config/broker_calendar.json`).
- Still to build (in order): the live detector loop over completed own bars (gate + research_start enforcement, wall-clock -> real UTC for news/sessions, event persistence), portfolio simulation and validation functions against `tests/portfolio` and `tests/validation`, then live-detection audit. **No demo execution until that audit.**

## Update 2026-09-30 (night, later): live detector loop (D-051..D-053)

- Windows fixes (tzdata dependency, UTF-8 file IO, test isolation): the owner's local suite passes (68 tests at that point).
- Live loop built and unit-tested: `python -m goldthinker.live.run --once` (builds candles, refreshes research clocks, detects on enabled timeframes, stores `strategy_events`). Read `src/goldthinker/live/` and D-053 (four PROPOSED items for ChatGPT: RSI seed window, NEWS_CALENDAR prerequisite, gap scope, sizing currency).
- Next: ChatGPT's answer on D-053; a differential audit of production vs the reference calculators on real recorded bars; then portfolio/validation functions. No demo execution until that audit passes.

## Exact next step (D-043)

Build the detector so that it reproduces the golden vectors exactly. Proposed order:

1. Pure functions: G1 ATR, G2 size classes, G3 swings and trend, G4 zones (role/death/AMBIGUOUS), G13 quantisation. Target: `tests/golden_vectors.json` kind `global` cases.
2. The 22 pattern detectors + early companions, their BASE and SRC variants, the event model (G0b), execution (G9/G10), RAW layer.
3. Hub counters, then the portfolio simulation (`tests/portfolio/`) and validation functions (`tests/validation/`).
4. Only then: data feed, database, hub UI, Vantage mirror (needs an MT5 account query: hedging/netting, contract size, tick value, leverage/margin, commission, swap, EURUSD feed).

Claude's proposals to put to ChatGPT before or during step 1 (not yet decided): implementation language Python 3.11+ using `fractions`/`decimal` (exact arithmetic, matching the reference calculators); a test runner that loads the JSON vectors and diffs exact expected values.

## Things that must not be forgotten

- Exact arithmetic everywhere (integer ticks, rationals, no float rounding before comparisons - ruling A-22). Quantise executable prices per G13 (A-30).
- Test fixtures: XAUUSD tick 0.01, USD 1.00 per tick per lot, 100 oz contract, lot step/min 0.01, spread 0.20, calendar open Sun 23:00-Fri 22:00 UTC with a Mon-Thu 22:00-23:00 UTC pause, server time UTC+1, EURUSD 1.25 in portfolio vectors. These are fixtures, not Vantage's real values.
- Strategy ledgers are in R, isolated and non-compounding (D-004 1% risk, fixed); the Portfolio Simulation is a separate EUR 10,000 compounding account; the Vantage demo is only a mirror (D-024, D-042).
- The dedicated GoldThinker demo account is EUR 10,000 (created by Danny).
- No live trading, no real-money capability, no connection to the Super Signals account (D-001, D-035).
- Parked, unrelated: Super Signals fix branch `fix/broker-deal-sync-silent-truncation` awaits Danny's go-ahead (no PR opened). The root `AGENTS.md` in the `Memory` repo removes ChatGPT as a development agent for AIDY/Super Signals; GoldThinker's ChatGPT-review process is Danny's separate instruction (D-035).
- Older research and the full decision history are also in the `Memory` repo on branch `claude/trading-bot-prompt-review-hrxbkw` under `projects/goldthinker/` (same files as `docs/` here; this repository is now the primary home).

## Starting a new window

Open a Claude Code session on this repository and say: "Read CLAUDE.md and HANDOVER.md, then continue with the next step."
