# AIDY Handover — 14 September 2026

## Scope

Full read of `dannythehat/Aidy-Gold-Signals` and reconciliation of AIDY Memory against source
truth. No code was changed in the AIDY repository. Only Memory was updated.

## Finished state

Source repo: `dannythehat/Aidy-Gold-Signals`
Branch: `main`
Verified SHA: `cb0f4bc` — *Merge guarded Phase B forward restart*
Previous Memory SHA: `b860e1b8`
Status: **SOURCE VERIFIED** — the Cloudflare Worker, D1 and live environment variables were not
inspected in this session.

## The headline

Memory described AIDY as a Day 10 point-in-time market/context service with formal-forward OFF.
**AIDY is a full Architecture V2 master-trader system at Day 53, plus Hub Phase A and Phase B.**
Memory was roughly forty-three build days behind.

That gap mattered: a session bootstrapping from the old Memory would have believed AIDY was a
context endpoint and could have set about building capabilities that already exist.

## What AIDY actually is

An independent Gold/XAUUSD intelligence system running entirely on Cloudflare, with no broker
access and no Super Signals, MT5, MetaAPI or Vantage credentials.

Decision cycle (`src/aidy/end_to_end.py`): capture → compose PIT context → deterministic safety
gates → OpenAI `gpt-5.6-sol` under a strict Structured-Outputs contract sampled **k=3** and
reconciled by self-consistency → immutable ex-ante decision ledger with a reproducibility bundle
→ paper simulator → master watcher and management contract → management replay counterfactual →
episode memory → Telegram publication with a delivery-audited ledger.

Decision contract `aidy_master_trader_decision_v2_falsifiable`: actions `new_trade`,
`manage_trade`, `close_trade`, `no_trade`; V2 adds `thesis`, `counter_argument`,
`invalidation_condition`, `abstention_basis` and a shadow thesis with its own direction, horizon
and evaluation condition.

**AIDY is structurally forbidden from position sizing.** The contract rejects any decision
containing lots, volume, risk percent, balance, equity, leverage or margin, and rejects
chain-of-thought fields. Sizing belongs to Super Signals alone. Setups come from a deterministic
taxonomy with explicit machine-evaluable conditions on H1/M15 structure, not model opinion.

## Build sequence reconstructed

- **Days 1–10** foundation and evidence — Cloudflare bootstrap, continuity auditor, BigQuery,
  historical backfill, PIT as-of reconstruction, deterministic features, official macro,
  cross-market, objective context packet.
- **Days 11–22** understanding — regimes, move detective, trade outcomes, no-trade
  counterfactuals, setup taxonomy, historical cases, analogue retrieval, evidence grades, PIT
  adversarial, Master Trader contract, OpenAI gateway, deterministic safety gates.
- **Days 23–40** Architecture V2 — J1–J16 baseline, context composer, episode retrieval, market
  structure calendar, historical bid/ask, PIT-vintaged rates, macro event intelligence, CME
  contract intelligence, GVZ volatility, attestation registry, falsifiable contract, immutable
  ledger, self-consistency, frozen replay CPCV, scorers J16–J21, strategy promotion,
  architecture gate.
- **Days 41–52** trading behaviour — GC shadow basis spine, flow VWAP, richer volatility, policy
  cross-asset, selective abstention, paper simulator invalidation, master watcher, manage/close
  v2, management replay, private Telegram publisher, publication ledger, end-to-end fidelity.
- **Day 53** forward boundary — Twelve Data adapter and qualification, D1 read-budget work,
  formal-forward freeze contract, immediate-start amendment, live forward activation.
- **Hub Phase A** data health — `/provider/data-health`, `aidy_data_health_events`, telemetry on
  the Cron tick and in `/health`.
- **Hub Phase B** episode memory — permanent episode ledger, decision→outcome→learning loop,
  `/provider/decision-memory`, guarded forward-restart campaign.

## Infrastructure

Worker `aidy-signals-test` at `https://aidy-signals-test.dannythehat2.workers.dev`, entry
`src/provider_entry.py`. D1 `aidy-ops-test` (`3588d82a-d686-4430-872d-d4c0e62c3d5d`), 27 tables,
migration files to `0020`. R2 `aidy-memory-test`. BigQuery project `aidy-signals`, dataset
`aidy_analytics_test`.

Capture runs from a **direct Cron trigger**, not a Queue; the Queue ABI is retained for rollback.
Each tick runs capture, then best-effort episode-memory sync, then best-effort data-health
telemetry — deliberately ordered so observability can never undo a successful capture.

Four scheduled GitHub workflows: archive-outbox watchdog, capture-freshness watchdog, D1
row-budget alert, and the Phase B forward-restart proof every ten minutes.

## Open question — formal forward

Memory asserted `formal_forward_enabled: false` as a settled safety fact. The source shows an
active scheduled campaign designed to turn it **on**:

- `phase-b-forward-restart.yml` runs every 10 minutes against `main`;
- it deploys with `AIDY_FORMAL_FORWARD_ENABLED='false'`, then, once the gate passes, redeploys
  with `'true'`;
- campaign `aidy_phase_b_repaired_forward_restart_20260913`, cohort version
  `aidy_formal_forward_cohort_v2_immediate_start`;
- the gate — enforced by CHECK constraints in `migrations/d1/0020` — requires source
  `twelve_data`, scheduler `direct-cron`, session open, fresh data health, ≥3 consecutive capture
  successes, ≥2 recent complete snapshots and a configured model gateway;
- the campaign moves `activated` → `model_resolved` only on a genuine post-activation evaluation
  with `data_quality_state='known_good'`.

**Correct status is `WAITING — RUNTIME UNVERIFIED`.** Do not assert either value.

Whatever it is, formal forward means private paper evaluation only. The D1 schema hard-codes
`broker_or_account_state_allowed=0`, `follower_state_allowed=0`,
`super_signals_dependency_allowed=0`, `live_money_execution_allowed=0`.

## Market data note

`README.md` still documents the older keyless Gold-API reference source. The active adapter is
Twelve Data vendor-built M1 OHLC. Gold-API's indicative mid with no genuine bid/ask or OHLC chain
is exactly why the forward observer was blocking with
`pre_model_blocked -> missing_genuine_live_ohlc_and_spread`. Because a feed change is
**evidence-semantic**, Twelve Data could not inherit the Gold-API cohort and required a new one.
The README is a documentation defect worth fixing in the source repo.

## Safety posture

- No broker, MT5, MetaAPI, Vantage or Super Signals credentials. AIDY never reads broker or
  follower state.
- No pre-activation backfill into any cohort; no forward-outcome tuning inside an active cohort.
- GC/XAU is a shadow observation layer, not a decision input. The Day 45 selective/conformal
  abstention layer is shadow-only and cannot block the Master Trader or publication.
- Day 54 inference requires ≥300 **episode-independent, model-resolved** decisions. Data-quality
  failures are structurally distinct from genuine `no_trade` and do not count. Raw bursts cannot
  substitute for episode-independent N.
- A cohort may be broken only for a material safety/data-integrity defect, a forced model/API
  deprecation, or an objective market-structure/venue rule change. Performance improvement is
  never a valid freeze-break reason.

## Exact next step

**Runtime verification, before any further AIDY claim or build:**

1. Worker environment — `AIDY_FORMAL_FORWARD_ENABLED`, `AIDY_CAPTURE_ENABLED`,
   `AIDY_MARKET_DATA_SOURCE`.
2. `aidy_forward_cohorts` — the active row for `aidy_formal_forward_cohort_v2_immediate_start`.
3. `aidy_forward_restart_runs` — `acceptance_state` for
   `aidy_phase_b_repaired_forward_restart_20260913`.
4. Count of episode-independent model-resolved decisions against the 300 gate.
5. That `/provider/data-health` and `/provider/decision-memory` answer correctly in production.

Then repair `CURRENT_STATE.md` and `LIVE_STATE.json` with the verified values.

The Data Hub build itself is Super Signals work; AIDY's side is delivered. See
`../../../NETWORK.md` and the Super Signals handover of the same date.
