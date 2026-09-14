# AIDY — Architecture Memory

Source-verified: **2026-09-14** at `main` `cb0f4bc`.

Compact orientation map. Verify implementation detail in `dannythehat/Aidy-Gold-Signals`.

## Core responsibility

AIDY is the independent Gold/XAUUSD intelligence system. It captures its own market and macro
evidence, preserves point-in-time truth, composes context, forms its own falsifiable thesis,
evaluates it forward on paper, and remembers what happened.

It holds no broker, MT5, MetaAPI, Vantage or Super Signals credentials, and never reads broker
or follower state.

## Runtime

Everything runs on Cloudflare. There is no Render dependency; Render is Super Signals
infrastructure only. GitHub Actions is used for CI, migrations, provisioning and deployment
transport — never as the trading runtime.

- **Cloudflare Workers** — `aidy-signals-test`, Python Workers, entry `src/provider_entry.py`
  which extends the core `src/entry.py`. Capture runs from a **direct Cron trigger**, not a
  Queue; the Queue ABI is retained only for rollback.
- **Cloudflare D1** — `aidy-ops-test`, operational state and the archive outbox (27 tables).
- **Cloudflare R2** — `aidy-memory-test`, durable append-only archive.
- **Google BigQuery** — project `aidy-signals`, dataset `aidy_analytics_test`, historical
  analytics warehouse for regime research, feature studies, analogue retrieval and evaluation.
- **OpenAI** — `gpt-5.6-sol` through `openai_gateway_v2`, strict Structured Outputs, k=3.
- **Telegram** — private publication boundary with a delivery-audited ledger.

Each scheduled tick runs capture, then best-effort episode-memory sync, then best-effort
data-health telemetry. Observability may report a failure but must never undo a successful
capture — that ordering is deliberate.

## Layers

1. **Capture / orchestration** — `runtime.py`, `market_recorder.py`, `twelve_data_recorder.py`,
   `live_gold_recorder.py`, `reference_price_recorder.py`.
2. **Operational evidence** — D1 via `cloudflare_storage.py`, `storage_contracts.py`.
3. **Durable archive** — R2 through the archive outbox, with bounded retry, backoff and an
   explicit dead-letter state.
4. **Market data** — Twelve Data vendor-built M1 OHLC plus the AIDY gold session calendar.
   Older keyless Gold-API and a historical MetaAPI adapter exist as prototype code only.
5. **Macro / cross-market evidence** — `official_macro.py`, `fed_rss.py`, `fed_h10_dollar.py`,
   `fomc_calendar_parser.py`, `bls_calendar_parser.py`, `macro_vintages.py`, `cross_market*.py`,
   with first-observed / revision semantics so a later revision never contaminates a past view.
6. **Point-in-time reconstruction** — `pit_reconstruction.py`, `pit_integrity.py`,
   `market_structure_context.py`, `price_structure_v2.py`.
7. **Feature and regime** — `feature_engine.py`, `regime_classifier.py`,
   `volatility_intelligence.py`, `richer_volatility.py`, `gc_shadow_spine.py`,
   `gc_microstructure.py`, `policy_cross_asset.py`.
8. **Memory and analogues** — `historical_cases.py`, `analogue_retrieval*.py`,
   `semantic_analogue_retrieval.py`, `episode_memory.py`.
9. **Decision** — `context_composer_v2.py`, `semantic_context_composer.py`, `safety_gates.py`,
   `master_trader_contract{,_v2}.py`, `self_consistency{,_v2}.py`, `selective_abstention.py`,
   `decision_ledger.py`.
10. **Evaluation** — `paper_simulator.py`, `master_watcher.py`, `management_contract_v2.py`,
    `management_replay.py`, `forward_evaluation.py`, `replay_evaluation.py`,
    `evaluation_scoring.py`, `no_trade_counterfactual.py`, `strategy_promotion.py`.
11. **Publication** — `telegram_publisher.py`, `publication_ledger.py`.
12. **Provider / Hub boundary** — `provider_market_api.py`, `provider_context_api.py`,
    `provider_calibration_api.py`, `provider_data_health_api.py`,
    `provider_decision_memory_api.py`.

## Resilience layers

- D1 row-read budget monitor and bounded, index-driven acceptance queries (free-tier discipline).
- Market-calendar-aware capture freshness watchdog.
- Archive-outbox durability watchdog with bounded retry/backoff and dead-letter.
- `data_health.py` point-in-time health telemetry, surfaced on `/health` so production health
  describes the brain rather than merely the Worker process.

Four GitHub Actions schedules back these up: archive-outbox watchdog (every 10 min offset 8),
capture-freshness watchdog (every 10 min offset 3), D1 row-budget alert (hourly), and the
Phase B forward-restart proof (every 10 min).

## Forward evaluation governance

Formal forward evidence is organised into **cohorts**. A cohort is identified by an immutable
frozen manifest binding the exact accepted code head plus the identities of the runtime, model
gateway, self-consistency layer, decision ledger, abstention layer, GC spine, macro contract,
market-data source, decision-context adapter and parameter-provenance audit.

Cohort states are only `prepared`, `active`, `closed`. A closed cohort cannot be reopened.

**Evidence-semantic change rule.** Changes to the feed adapter, price basis, session calendar,
candle construction, feature construction, thresholds, scales or analogue geometry are
*presumed* evidence-semantic, and the default consequence is a new cohort. Preserving a cohort
is the exception and needs affirmative deterministic proof recorded at PR time, before merge and
before any post-change outcome is observed. Accumulated N, reset cost and observed performance
are explicitly not evidence that a change was transport-only.

A cohort may be broken only for `material_safety_or_data_integrity_defect`,
`forced_model_or_api_deprecation` or `objective_market_structure_or_venue_rule_change`.

Outcomes attach later through a separate immutable table. They never mutate the ex-ante record
and cannot tune an active cohort. `no_trade` is a first-class evaluated decision.

## Episode memory (Phase B)

The learning loop, in D1:

```text
aidy_end_to_end_cycles ──> aidy_memory_episodes
         │                        │
aidy_forward_evaluations ──> aidy_forward_outcomes ──> aidy_memory_outcomes ──> aidy_learning_cards
```

Versions: `aidy_episode_memory_v1`, `aidy_episode_memory_outcome_v1`,
`aidy_structured_learning_card_v1`, `aidy_m1_episode_outcome_resolver_v1`,
`aidy_episode_memory_sync_v1`. Outcome resolution is due-based and hindsight-free.

## Key principle

AIDY should know **what the market looked like at the time**, without hindsight and without
borrowing broker or provider outcome information as if it were market evidence.
