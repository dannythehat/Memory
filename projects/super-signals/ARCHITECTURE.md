# Super Signals — Architecture

Source-verified: **2026-09-14** at deployed branch `feature/day-10-shared-telegram-sources`
head `8019f66`.

## System boundary

Super Signals owns Telegram provider ingestion and interpretation, provider research state,
member/broker execution, settlement, account/runtime UX and the embedded provider-intelligence
layer.

`dannythehat/Aidy-Gold-Signals` is a **separate system** with its own runtime, database and
forward-research lifecycle. It supplies independent Gold market/context intelligence. Do not
merge their runtime state merely because both are called AIDY. See `../../NETWORK.md`.

## Deployment shape

One Render web service, `super-signals-day-8`, serves both the FastAPI API and the built React
PWA from the same origin. The public marketing site is a separate Cloudflare Worker that reverse
proxies `/account-api/*` to this same Render origin.

The Dockerfile enforces quality as a build gate across four stages — `security-scan` (a secret
scan that must pass), `web-quality` (typecheck, lint, web tests, production build),
`api-quality` (compileall plus the full pytest suite), then `runtime`. The runtime stage refuses
to build unless all three markers are present. **A failing test cannot be deployed.**

`scripts/render-start.sh` runs `alembic upgrade head`, a one-time TDC retirement, the idempotent
owner bootstrap, then launches the Day 13 conditional research refresh and Day 14 governance in
the background, then `exec python -m app.serve_runtime`.

`serve_runtime.py` imports the Connection V2 member-onboarding router **before** `app.main` so
every production process exposes the same onboarding endpoints without account-specific runtime
patching. Routers are then composed in `app/routes/__init__.py` by nesting child routers into
parents that `main.py` already includes — small extensions register themselves rather than
requiring `main.py` edits.

## Production path

1. Telethon reader sessions, private per administrator, capture messages from selected sources.
2. A deterministic-first canonical message pipeline classifies and interprets. OpenAI
   `gpt-5-mini-2025-08-07` is used through the Responses API only where deterministic rules
   cannot decide.
3. `CanonicalExecutionDispatcher` routes one durable decision by source status.
4. Provider profile/version/PIT evidence preserves what was known at signal time.
5. AIDY/provider market-context attachments join signals to contemporaneous Gold context.
6. Shadow/research outcomes feed provider benchmark, fingerprint and governance evidence.
7. B–F provider intelligence persists append-only provider and combined-book snapshots.
8. Canonical signals publish to the private Smart Signals Telegram channel and to the PWA;
   broker truth settles them.

### The interpretation boundary

This is a core safety rule, implemented in `day27_management_policy.py`:

> OpenAI may identify **which** trade a provider is talking about, but broker mutations come only
> from mechanically explicit current-message instructions. Ambient history may link a trade; it
> may never donate an action, price, TP index or side.

Management actions are matched by explicit, audited regular expressions — close all, exit now,
partial close, move stop, breakeven, cancel — with deliberate handling of optional/suggested
wording ("if you want", "or go BE") so a provider's suggestion is not executed as an instruction.

### The shadow boundary

Source status is the switch. In `CanonicalExecutionDispatcher.dispatch_stored_decision`, a
`shadow` source branches into `_dispatch_shadow` and returns **before any broker code path
exists**. This is structural isolation, not a policy check that could be bypassed by a
configuration mistake.

## Data model

PostgreSQL, 67 tables across 82 Alembic migrations. Only 10 core tables have ORM models
(`roles`, `users`, `user_roles`, `invitations`, `telegram_accounts`, `sources`, `messages`,
`signals`, `positions`, `audit_events`); the rest are created and managed directly in migrations.

Broad groupings:

- **Identity/access** — users, roles, permissions, role_permissions, user_roles, auth_sessions,
  auth_rate_limits, password_recovery_requests, invitations.
- **Membership/commerce** — member_subscriptions, subscription_payment_claims,
  complimentary_access_grants, complimentary_access_tokens.
- **Telegram ingestion** — telegram_accounts, sources, source_reader_access, messages,
  message_revisions, message_classifications, message_parses, message_validations,
  message_review_items, ai_message_decisions.
- **Signals/execution** — signals, signal_observations, signal_lifecycle_events, positions,
  telegram_publications, telegram_live_board_state, user_trading_controls.
- **Performance/settlement** — broker_deals, performance_account_snapshots,
  performance_trade_outcomes, performance_summaries, performance_reporting_overrides.
- **Notifications** — notification_events, notification_reads, push_subscriptions,
  push_notification_deliveries, telegram_notification_deliveries.
- **Provider Lab research** — shadow_trades, shadow_trade_legs, provider_research_profiles,
  provider_research_profile_versions, provider_signal_context_attachments,
  provider_shadow_enrollment_audit.
- **Provider Intelligence** — execution reconciliation (runs/samples/tolerances/provider_results),
  fingerprint (runs/cells), conditional (runs/hypotheses/results), governance
  (runs/policies/results), veto counterfactual (decisions/outcomes), management counterfactual
  (decisions/outcomes), resource usage, aidy authority audit, and the append-only
  `provider_intelligence_snapshots` / `provider_book_conflict_snapshots`.

Current views for research read paths: `provider_intelligence_current`,
`provider_book_conflict_current`, `provider_fingerprint_latest`, `provider_governance_latest`,
`provider_conditional_latest`, `provider_benchmark_performance`, `provider_benchmark_segments`,
`provider_execution_calibration_samples`, `provider_execution_cost_model`,
`provider_execution_reconciliation_latest`, `provider_shadow_execution_projection`.

## Risk and execution policy

`provider_risk_policy.py` is the **single production source of truth** for provider execution and
risk. Production execution imports it directly; no other module may invent a provider direction
veto or a hidden TP risk ladder.

Owner authority from 9 September 2026: every enabled TP/runner leg carries exactly **1% planned
risk**. Entry sections distribute those legs and never multiply the risk budget. Four TP/runner
legs mean 4% planned signal risk. Disabled provider directions return a zero risk profile and
fail closed before broker mutation.

Automatic profit protection lives in `broker_settlement_canonical._apply_profit_protection_ladder`:
TP2 hit cancels unused entry orders and moves every open TP3+ leg to its own entry; TP3 hit moves
every remaining TP4+/runner stop to the signal's TP2 price. Existing protection is never loosened,
and the next settlement poll retries any broker mutation that did not become locally confirmed.

## AIDY Provider Intelligence B–F

Implementation: `services/api/app/provider_intelligence_bf.py`, contract
`aidy-provider-intelligence-bf-v1`. Deliberately broker-isolated — it never places, sizes, changes
or closes a trade.

- **B market context** — PIT-safe session/regime/context coverage and benchmark outcome buckets,
  built only from real context attachments. Context is never invented for unattached signals.
- **C fingerprint** — consolidates footprint and adaptive-profile evidence into one behavioural
  fingerprint: message sequence, dominant session, entry/order/management style, vocabulary,
  cadence and drift.
- **D governance** — emits `learning`, `healthy_research`, `watch` or `quarantine_candidate` with
  explicit reasons, and carries `automatic_source_status_mutation_allowed: false`.
- **E adaptation** — provider-specific interpretation hints with a confidence band, and explicit
  `historical_numeric_levels_allowed: false` plus
  `current_message_or_direct_reply_evidence_required: true`.
- **F combined book** — latest directional stance per provider over a 45-minute window, with
  conflict pairs and net bias. Recommendation is always `observe_only`;
  `broker_netting_allowed: false`.

Persistence is append-only through migration `0078_aidy_intel_bf`. Identical snapshot payloads are
digest-deduplicated. Database triggers reject UPDATE and DELETE on the snapshot ledgers. Refresh
runs inside `AidyShadowRuntime` on a 300-second loop after M1 resolution and context attachment,
and sleeps during the weekly freeze.

## Weekly market freeze

`weekend_trading_freeze.py` defines the standard XAUUSD weekly close/open gate in `Europe/Sofia`
(Friday 23:57 → Monday 01:01). Automatic MetaAPI read/margin/trade gateways, Telegram monitoring,
settlement, pending reconciliation and the AIDY research loop respect it.

It is an automatic-runtime gate, not a claim that every web/UI/provisioning action is disabled.

## Gold price display

The displayed Gold quote uses free HTTP feeds (`biquote.io` primary, `api.gold-api.com` fallback)
rather than MetaAPI, isolated from the user's broker account. Dashboard broker-state code still
contains a redundant MetaAPI XAU price read that should be removed as an efficiency cleanup.

## Public performance feed

`routes/gold_quote.py` also serves the privacy-safe public feed the marketing site consumes:
daily realised P/L and provider-hidden trade outcomes from the Owner reference ledger. Audited
reporting overrides are applied to the public cash ledger **without** changing immutable broker
evidence, and revoked providers stay outside user-facing performance.

## Data Hub architecture requirement

The AIDY Data Hub is an owner/admin read surface over durable database evidence and current
views. Querying PostgreSQL on refresh is acceptable; invoking OpenAI, MetaAPI or external AIDY
research because the owner opened or refreshed a page is not.

The Hub should surface both provider intelligence and AIDY's own evolving Gold-market
intelligence without conflating evidence maturity with statistical validation. AIDY's side is
already built: `/provider/data-health` and `/provider/decision-memory`.
