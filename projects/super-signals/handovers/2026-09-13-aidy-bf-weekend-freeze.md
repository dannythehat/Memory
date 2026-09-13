# Super Signals Handover — 13 September 2026

## Scope completed

This handover records the production-verified weekly XAUUSD freeze plus the AIDY Provider Intelligence B-F integration, and records the owner's clarified strategic north star for AIDY.

## Production evidence

- Repo: `dannythehat/super-signals`
- Deployed branch: `feature/day-10-shared-telegram-sources`
- Source/deploy SHA: `278496ccbe71ec14f4e2e63b0dbd05004ea774b5`
- Render service: `super-signals-day-8`
- Render deploy: `dep-dajb9cmk1f9s73fm0b3g`
- Deploy status: LIVE
- Migration head: `0078_aidy_intel_bf`
- Quality gate: 931 passed, 67 skipped, 0 failed, 2 warnings
- Current views verified present: `provider_intelligence_current`, `provider_book_conflict_current`
- New snapshot tables verified present: `provider_intelligence_snapshots`, `provider_book_conflict_snapshots`

## Weekly market freeze

`services/api/app/weekend_trading_freeze.py` implements the standard XAUUSD weekly closure in `Europe/Sofia`:

- Friday >= 23:57: frozen
- Saturday: frozen
- Sunday: frozen
- Monday < 01:01: frozen
- Monday >= 01:01: open

Automatic MetaAPI read/margin/trade gateways hard-block external trading/broker traffic during the freeze. Telegram provider readers stop and original weekend messages are rejected. Settlement and pending reconciliation return early. AIDY Provider Lab external market/context research sleeps. B-F refresh therefore also sleeps.

Do not describe this as the whole website/app being powered off. Health checks, cached/stored data, free Gold quote display and short timer wake-ups can remain. User-initiated provisioning was not included in the hard block.

A narrow follow-up remains: a pre-weekend message edited during closure may have a recovery path after reopen unless `edited_at` is also freeze-gated.

## AIDY Provider Intelligence B-F

Implementation: `services/api/app/provider_intelligence_bf.py`.

### B — market-context join
Produces PIT-only context/session/regime coverage and outcome buckets from existing signal-context attachments.

### C — provider fingerprint
Consolidates existing provider footprint/adaptive-profile evidence into a provider behavioural fingerprint including cadence, sequence, entry/order/management style, vocabulary and drift.

### D — research governance
Produces `learning`, `healthy_research`, `watch` or `quarantine_candidate` evidence. It cannot mutate `sources.status` or grant live authority.

### E — provider-specific adaptation
Represents provider-specific communication/trading style for interpretation. Historical numeric levels are explicitly not valid current-message execution evidence.

### F — combined-book conflict
Summarises recent provider BUY/SELL consensus/conflicts. Recommendation remains `observe_only`; broker netting is prohibited.

Persistence is append-only through migration `0078_aidy_intel_bf`. Identical snapshot payloads are digest-deduplicated. Database triggers reject UPDATE/DELETE on the snapshot tables.

## Sunday evidence state

At verification both new snapshot tables had zero rows. This is correct because the weekly freeze was active and the B-F refresh runs inside the paused AIDY Provider Lab runtime. Do not bypass the freeze or fabricate records. Population should begin from genuine forward activity after market reopen.

## Statistical status

B-F is engineering/prod verified, not statistically validated. Current provider promotion/profitability conclusions must continue to respect sample/evidence floors. `WAITING-FOR-FORWARD-EVIDENCE` is the correct state where no sufficient eligible OOS evidence exists.

## Live-risk contract

- Current owner directive: **1% only**.
- TP1 + TP2 -> move SL to entry.
- TP3 -> move SL to TP2.
- Moving SL to entry does not mean closing the trade.
- B-F does not change those rules.

## Owner strategic north star — important

The owner explicitly corrected an overly narrow framing of AIDY on 13 September 2026.

**AIDY is intended to become an independent Gold trader/intelligence system.** It should understand Gold market movements and moments, form its own thesis/bias, identify its own setups, judge provider trades, disagree when appropriate, and eventually propose/manage its own trades. Telegram providers are an evidence/training corpus, not AIDY's final purpose.

This is a product/architecture direction, not current broker authority. Independent AIDY setups must be paper/shadow/forward validated and explicitly graduated before any additional live-money authority.

## Exact next build — AIDY Data Hub

Build an owner/admin Data Hub that makes AIDY visible every day.

Use stored database/current views, not fresh OpenAI/MetaAPI calls triggered by page refresh.

Overview should include:
- AIDY active/frozen/learning state
- provider coverage
- signal capture/read/ambiguous/rejected metrics where reliable
- context coverage
- eligible forward/shadow evidence
- provider health/governance/drift
- current provider BUY/SELL consensus and conflicts
- system health and owner-attention alerts
- evidence maturity, clearly separating raw activity from statistical validation

AIDY section should evolve toward:
- current Gold thesis/bias
- session/regime
- important levels/setups
- confidence
- current watch conditions
- invalidation
- future AIDY-proposed paper trades

Provider drill-down should expose fingerprint, grammar/style, interpretation confidence, context coverage, valid forward performance, session/regime performance, warnings/drift, governance history and recent activity.

## Runtime-efficiency follow-ups

1. Quarantine four stale historical `broker_filled_position_not_visible` rows from the fast settlement path while preserving audit history.
2. Return before broker position/order reads when there are no protection plans.
3. Remove the redundant dashboard MetaAPI Gold-price read; UI display already uses free feeds.
4. Persist exact OpenAI token/cost and MetaAPI request telemetry.
5. Consider the weekend `edited_at` replay gate.

## Session bootstrap for the next agent

Read this handover, `CURRENT_STATE.md`, `LIVE_STATE.json`, `SAFETY_RULES.md`, `ROADMAP.md`, then verify the current Super Signals branch/Render/Postgres state before changing production. If production has advanced, repair Memory from production truth first.