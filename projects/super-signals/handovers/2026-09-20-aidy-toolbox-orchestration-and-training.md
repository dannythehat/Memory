# AIDY toolbox orchestration + historical training handover

Date: 2026-09-20

## Owner directive

Owner clarified that AIDY must understand and use the tools available to him, then use that evidence to judge historical/provider results. The intended behavior is **not** to call every tool mechanically on every trade. AIDY must know which tools/evidence surfaces exist, consider every available standing surface, call on-demand tools when they can materially resolve uncertainty, and keep unavailable evidence UNKNOWN.

Live-money authority remains OFF.

## Authoritative Super Signals state

Repository: `dannythehat/super-signals`  
Deployed branch: `feature/day-10-shared-telegram-sources`

Latest verified toolbox merge:
- PR #228 — historical research toolbox
- PR #229 — explicit toolbox-awareness instructions + live toolbox manifest
- PR #230 — aligned historical `supplemental_evidence.toolbox_manifest` with the reasoning prompt
- final SHA: `36dee29f4b87dfe2f94bb02ea19f21c612b363d4`
- Render deploy: `dep-danv6k5ii2qc73c8fdqg`
- deploy status: live
- canonical API gate: **1,189 passed / 137 skipped / 2 warnings**
- secret scan: PASS
- service health: 200 after deploy

No broker execution, live risk sizing, provider routing/status, MT5 management, or live-money authority was changed by these PRs.

## Tool model now understood by AIDY

### On-demand tools

Live AIDY:
1. `get_recent_candles`
2. `get_economic_calendar`

Historical stress AIDY:
1. retrospective `get_recent_candles`
2. retrospective official-schedule `get_economic_calendar`
3. `inspect_historical_evidence`

The historical evidence inspector can focus AIDY on:
- provider history
- reconstructed market context
- event/liquidity context
- historical analogues
- probability/EV context
- failure/self-critique context
- recent provider messages

### Standing evidence AIDY must consider

The toolbox manifest explicitly reports availability for:
- provider history
- market context
- recent messages
- event/liquidity
- historical analogues
- probability/EV
- self-critique

The reasoning prompt now tells AIDY:
- read the toolbox manifest before deciding;
- consider every standing surface marked available;
- call a tool when its answer could materially change `take/reduce/reject`;
- do not call tools merely to satisfy a checklist;
- never manufacture an answer for a surface marked unknown/unavailable/not connected;
- tool evidence never grants execution authority or exposes the target outcome.

The engine can execute multiple function calls returned in one tool round and is bounded to two tool-use rounds before a final structured answer.

## Wider AIDY research-stack audit

Several research modules exist in `dannythehat/Aidy-Gold-Signals`, but code existence is not treated as operational evidence.

Verified from the AIDY private-forward/provider-context implementation:
- rates/macro vintages: UNKNOWN — no operational Day 28 vintage feed;
- tiered macro events: UNKNOWN — no operational Day 29 schedule feed in private-forward context;
- CME contract state: UNKNOWN — no operational Day 30 bulletin feed;
- GVZ implied volatility: UNKNOWN — no operational Day 31 GVZ feed;
- realized volatility: derivable when admitted candle history is sufficient;
- price/liquidity structure: derived from admitted Twelve Data candles in private-forward context;
- cross-market/semantic context exists in the AIDY private-forward stack, but the Super Signals historical stress window does not have enough immutable AIDY context attachments to use it honestly.

Production SQL verification of the historical stress window (2026-08-01 through 2026-09-08 13:22:57Z) found only **1** immutable `provider_signal_context_attachments` row. Therefore cross-market/semantic context is **not backfilled retrospectively** into August cases. Doing so would reintroduce hindsight risk.

Recent provider-context attachment counts confirm the live PIT path is populated later:
- 2026-09-14: 32
- 2026-09-15: 5
- 2026-09-16: 1
- 2026-09-17: 112
- 2026-09-18: 97

Those rows did not yet contain a non-empty Gold State payload, so current capability claims stay scoped to what is actually attached.

## Historical training runtime

New independent contracts:
- replay: `aidy_historical_stress_lab_v6_toolbox`
- input: `aidy_historical_stress_input_v5_toolbox`

Frozen scoreable cohort remains:
- train: 571
- validation: 69
- OOS: 160
- total: 800

Render configuration was explicitly set:
- stress enabled = true
- scope = train
- validation open = false
- OOS open = false
- max calls = 800

Post-deploy production verification showed the training runtime is active: `pg_stat_activity` showed the effective-time historical candidate query executing from the service immediately after the protected startup grace period.

At the time this handover was first written, the materialization transaction had not yet committed new v6 rows, so no v6 P&L/edge result is claimed here.

## Safety / evidence rules

- historical candles are retrospective research data, cut off before the target signal;
- official event schedules contain scheduled timestamps only, no realized/forecast surprise leakage;
- provider evidence uses only prior outcomes whose result-known time is <= target signal time;
- edited Telegram signals use the executable revision's edit timestamp as effective signal time;
- validation and OOS remain sealed during training;
- the separate exact-PIT 18-case holdout remains sealed;
- no training result is a live-profitability claim.

## Next exact step

Let the 571-case training materialization/reasoning/scoring complete under v6, then analyse AIDY versus the provider-taken training baseline using only training data:
- action distribution;
- loss saved;
- winning profit clipped;
- provider/side/session/event/trend/geometry buckets;
- tool-call usage and whether each tool improved or harmed decisions;
- false rejects/reductions versus correctly avoided losses.

Only after a candidate is frozen from training may validation be opened. OOS and the exact 18-case holdout stay closed until their later gates.
