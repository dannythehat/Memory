# Super Signals — AIDY live-trading isolation and public-repo scrub

Date: 2026-09-22
Status: LIVE ISOLATION VERIFIED / DEFAULT-BRANCH SCRUB MERGED

## Owner mandate

AIDY is research/observation/learning only. It must never gate, delay, cancel, size, suppress or otherwise interfere with the live provider -> Telegram listener -> MT5 execution path.

If AIDY is overloaded, broken, stale or unavailable, AIDY must fail/skip its own research pass. Daily trading signals must continue independently.

## Actual live production branch

- Repo: `dannythehat/super-signals`
- Render service: `super-signals-day-8`
- Render service id: `srv-d9qmcgks728c73a555m0`
- Render branch: `feature/day-10-shared-telegram-sources`
- Live deployed SHA: `26c481df4ac274c76d0028883b33eab250e1f41a`
- Deploy id: `dep-dap89qn1rjqs73d61o2g`
- Deploy became live: 2026-09-22T13:40:48Z

## Verified production isolation

The live branch has two independent SQLAlchemy engines/session factories:

### Live trading lane

`get_engine()` / `get_session_factory()`

- pool_size = 5
- max_overflow = 3
- pool_timeout = 15s
- used by broker, Telegram listener, execution, settlement, publishing and normal application paths

### AIDY research lane

`get_research_engine()` / `get_research_session_factory()`

- same Postgres server, but separate SQLAlchemy pool
- pool_size = 1
- max_overflow = 0
- pool_timeout = 2s
- PostgreSQL statement_timeout defaults to 5000ms
- PostgreSQL lock_timeout = 1000ms
- application_name = `super-signals-aidy-research`

Every AIDY/provider-research background runtime wired in the live `main.py` receives `research_session_factory`, including:

- AidyShadowRuntime
- ProviderTradeScoringRuntime
- AidyDecisionRuntime
- AidyDecisionOutcomeRuntime
- AidyReasoningRuntime
- AidyGroundingAcceptanceRuntime
- AidyHistoricalReplayRuntime
- AidyHistoricalStressLabRuntime
- AidyMessageReviewRuntime
- ProviderFingerprintRuntime

The live Telegram/MT5 execution path continues to receive `session_factory`, not the research factory.

This is resource isolation, not a separate Postgres server. One AIDY query can still consume some shared database CPU/I/O, but it cannot exhaust the live SQLAlchemy connection pool. Research has one connection maximum and bounded database timeouts.

## Runtime evidence

Post-deploy logs show the service live and AIDY research failures occurring inside AIDY runtimes while the application remains up. This is the desired fail-flat direction: AIDY can fail without taking down the trading service.

Do not interpret this as proof that every AIDY research routine is healthy. Several AIDY decision/reasoning/grounding/message-review passes were still erroring post-deploy and need their own repair. Those research failures must remain non-authoritative to live execution.

A separate broker-settlement log also showed `metaapi_temporarily_unavailable`; that is a broker/API condition, not evidence that AIDY blocked execution.

## Default main repair and CI

PR #241: `Hard-isolate AIDY research from live trading`

Merged into default `main`:
- merge SHA: `1a5488d20722f501937f83f1e15bcadba146e545`

Dedicated AIDY Live-Trading Isolation Gate:
- run: `35737906048`
- result: SUCCESS
- compile: PASS
- isolation lint: PASS
- isolation regressions: PASS

The general API suite on the PR still fails because the base repository already has multiple Alembic heads (`0069_provider_day20_mgmt` and `0034_reviewed_provider_trade_result`). This is a pre-existing migration-graph problem and is separate from AIDY isolation.

## Public repository scrub

The default branch README was replaced with a generic proprietary/internal-software notice.

Public explanatory/operational documents were removed from the default branch, including architecture, scope, risk sizing, execution gates, MT5/Telegram operations, security/backup docs and Provider Intelligence/AIDY strategy handovers.

Important caveat: the repository remains PUBLIC. Deleting files from the latest commit does not remove them from Git history, and other public branches remain inspectable. GitHub's repository About description also still says:

`Private Telegram signal aggregation and automated Vantage MT5 trading platform.`

The connected GitHub tool used here cannot edit repository metadata or visibility. For real IP protection, the repo should be made private again and the About description cleared/changed. If old public history must be erased rather than merely hidden by privacy, a history rewrite/new clean private repository is required.

## Execution posture unchanged

This repair does NOT change:
- provider enable/disable policy
- BUY vs SELL routing
- TIG policy
- member risk sizing
- MetaAPI order logic
- trade-management rules
- AIDY live-money authority

AIDY live-money authority remains OFF.
