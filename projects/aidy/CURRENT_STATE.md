# AIDY — Current State

Last source-verified: **2026-09-14**
Last runtime-verified: **not in this session** — see "Evidence status" below.

Authoritative repo: `dannythehat/Aidy-Gold-Signals`
Authoritative branch: `main`
Verified source `main` SHA: `cb0f4bc` — *Merge guarded Phase B forward restart*
Live Worker: `aidy-signals-test` — `https://aidy-signals-test.dannythehat2.workers.dev`
Worker entrypoint: `src/provider_entry.py`
Cloudflare D1: `aidy-ops-test` (`3588d82a-d686-4430-872d-d4c0e62c3d5d`), migration files to `0020_phase_b_forward_restart_guard`
Cloudflare R2: `aidy-memory-test`
BigQuery: project `aidy-signals`, dataset `aidy_analytics_test`

## Evidence status — read this first

The previous version of this file described AIDY as a Day 10 point-in-time market/context
service with formal-forward OFF. **That was seven days and roughly forty-three build days
stale.** AIDY is now a full Architecture V2 master-trader system with its own thesis engine,
decision ledger, paper simulator, management watcher, Telegram publisher and permanent episode
memory.

This update is **SOURCE VERIFIED** at `cb0f4bc`. It is **not** production verified. The
Cloudflare Worker, D1 contents and live environment variables were not inspected. Do not
restate anything below as live until it is checked against the Worker and D1.

## What AIDY actually is now

AIDY is an independent Gold/XAUUSD trading-intelligence system running entirely on Cloudflare.
It captures its own market and macro evidence, reconstructs point-in-time market state, forms
its own falsifiable thesis through an LLM under a strict contract, evaluates that thesis
forward on paper, and keeps a permanent memory of what it decided and what happened next.

It has **no broker access of any kind** and holds no Super Signals, MT5, MetaAPI or Vantage
credentials.

## The decision cycle (`src/aidy/end_to_end.py`)

1. **Capture** — direct Cloudflare Cron tick records XAU/USD evidence into D1, flushes to R2
   through the archive outbox.
2. **Compose** — `context_composer_v2` + `semantic_context_composer` build a PIT context dossier
   from price structure, regime, volatility, sessions, macro vintages, cross-market and GC basis.
3. **Gate** — `safety_gates` and `twelve_launch_policy` run deterministic pre-model checks. If a
   data gate fails, OpenAI is **not** called and the record is `pre_model_blocked`.
4. **Decide** — `master_trader_contract_v2` calls OpenAI `gpt-5.6-sol` under a strict
   Structured-Outputs schema, sampled **k=3** and reconciled by `self_consistency_v2`.
5. **Record** — `decision_ledger` writes an immutable ex-ante evaluation record with a
   reproducibility bundle.
6. **Simulate** — `paper_simulator` opens a paper position; `master_watcher` + `management_contract_v2`
   manage it; `management_replay` scores counterfactual management.
7. **Learn** — `episode_memory` materialises episodes, resolves due forward outcomes with no
   hindsight, and writes structured learning cards.
8. **Publish** — `telegram_publisher` + `publication_ledger` deliver to a private Telegram
   boundary with a delivery audit.

### The decision contract

Action is one of `new_trade`, `manage_trade`, `close_trade`, `no_trade`. Direction is
`long`/`short`, entry type is market only, management instruction is one of `move_stop`,
`replace_targets`, `move_stop_and_targets`.

V2 adds the falsifiable fields: `thesis`, `expected_horizon_minutes`, `counter_argument`,
`invalidation_condition`, `abstention_basis`, `shadow_thesis`, `shadow_direction`,
`shadow_horizon_minutes`, `shadow_evaluation_condition`.

**AIDY is structurally forbidden from position sizing.** The contract rejects any decision
containing lots, volume, risk percent, balance, equity, leverage or margin, and rejects any
chain-of-thought/reasoning-trace field. Sizing belongs to Super Signals alone.

Setups come from a deterministic taxonomy in `setup_detector.py` (trend pullback, trend
momentum, recent extreme pressure, session extreme pressure and others), each defined by
explicit machine-evaluable conditions on H1/M15 structure — not by model opinion.

## Market data

Current source is **Twelve Data** vendor-built M1 XAU/USD OHLC (`twelve_data_recorder.py`,
`twelve_data_market.py`), `market_data_ownership=public_independent`, scheduler `direct-cron`,
poll 300s at the last recorded rollout.

The README still documents the older keyless **Gold-API** reference-price source. That is
historical. Gold-API gave an indicative mid with no genuine bid/ask or OHLC chain, which is
exactly why the formal-forward observer was blocking with
`pre_model_blocked -> missing_genuine_live_ohlc_and_spread`. Twelve Data was introduced to fix
that, and because it is an **evidence-semantic** change it could not inherit the Gold-API
cohort — it required a new cohort.

## Formal forward — the biggest open question

Memory previously recorded `formal_forward_enabled: false` as a settled safety fact. The source
now shows an active, scheduled campaign designed to turn it **on**.

- `.github/workflows/phase-b-forward-restart.yml` runs **every 10 minutes** against `main`.
- It deploys the Worker with `AIDY_FORMAL_FORWARD_ENABLED='false'`, then, once the gate passes,
  re-applies the deployment with `AIDY_FORMAL_FORWARD_ENABLED='true'`.
- Campaign id `aidy_phase_b_repaired_forward_restart_20260913`, cohort version
  `aidy_formal_forward_cohort_v2_immediate_start`.
- The gate (enforced by CHECK constraints in `migrations/d1/0020`) requires: source
  `twelve_data`, scheduler `direct-cron`, session open, data health fresh, at least 3 consecutive
  capture successes, at least 2 recent complete snapshots, model gateway configured.
- The campaign moves `activated` → `model_resolved` only when a genuine post-activation forward
  evaluation with `data_quality_state='known_good'` appears.

**Therefore: do not assert either state.** The correct status is `WAITING — RUNTIME UNVERIFIED`.
First action with Cloudflare access: read the Worker's `AIDY_FORMAL_FORWARD_ENABLED` and the
`aidy_forward_restart_runs` row for that campaign.

Whatever that value turns out to be, formal forward means **private paper evaluation only**. It
grants no broker authority. The D1 schema hard-codes `broker_or_account_state_allowed=0`,
`follower_state_allowed=0`, `super_signals_dependency_allowed=0`, `live_money_execution_allowed=0`.

## AIDY Hub — Phase A and Phase B are already built

The owner's next product build is a Data Hub. Two of its AIDY-side feeds already exist and are
merged on `main`:

- **Phase A — `GET /provider/data-health`** (`provider_data_health_api.py`): current health plus
  event history. Fields include status/alert/reason, session_open, capture_enabled,
  market_data_source, scheduler, latest scheduled success and request status, latest provider
  context snapshot, success lag, archive pending/backoff/dead-letter counts and oldest
  unarchived age, the same for cross-market, and latest macro observation.
- **Phase B — `GET /provider/decision-memory`** (`provider_decision_memory_api.py`): an episode
  summary (episode count, outcome count, learning-card count, score-eligible count, latest
  availability) plus recent structured learning cards.

Both are bearer-authenticated with the same token as `/market/ohlc` and `/provider/context`, and
both fail closed with 503 rather than inventing data.

**Nothing consumes them yet.** Wiring them into the Hub is Super Signals work, not AIDY work.

## Safety posture

- AIDY remains independent Gold market/context intelligence. It does not own provider identity,
  interpretation, Provider Lab research or any broker/member execution — Super Signals does.
- Formal-forward authority, whatever its current flag value, is paper only.
- No pre-activation backfill into any cohort. No forward-outcome tuning inside an active cohort.
- GC/XAU remains a shadow observation layer, not a decision input.
- The Day 45 selective/conformal abstention layer is shadow-only and cannot block the Master
  Trader or publication.
- Day 54 inference requires at least **300 episode-independent, model-resolved** decisions.
  Data-quality failures are structurally distinct from genuine `no_trade` and do not count.
- Performance improvement is never a valid reason to break a cohort freeze.

## Exact next step

1. Verify runtime: Worker environment variables, the active row in `aidy_forward_cohorts`, the
   Phase B campaign's `acceptance_state`, and the current count of episode-independent
   model-resolved decisions against the 300 gate.
2. Then repair this file with the verified values before building anything on top of it.
3. The Hub build itself is Super Signals work; AIDY's side is already delivered.

## Session rule

Read `NETWORK.md`, then this file, `SAFETY_RULES.md`, `LIVE_STATE.json` and the latest handover.
Then verify the Cloudflare Worker and D1 before making any production claim. Source/runtime truth
overrides this file.
