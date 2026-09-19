# Handover — AIDY Gold State Engine v1

Date: 2026-09-19
Status: BUILT IN ISOLATION / NOT GRADUATED / NOT LIVE-AUTHORITATIVE

## Repositories

Standalone AIDY:
- branch: `feature/gold-state-engine-v1`
- head: `709d7702ec7b479d86ff8f8289d095bad8045cf0`
- PR: #137

Super Signals consumer:
- branch: `feature/aidy-gold-state-v2-reasoning`
- head: `f6e1e42ecb8ff18b153912915588f4c6945711b6`
- PR: #208
- base: `feature/day-10-shared-telegram-sources`

## What is built

`aidy_gold_state_engine_v1` is deterministic and PIT-only. It produces:

- M1/M5/M15/H1/H4 completed-bar close-path state;
- session state;
- current-price distance to prior day, Asia overnight, named-session and opening-range
  highs/lows where actually observed;
- descriptive nearest $10/$50 references, explicitly with no predictive-edge claim;
- prior-day and confirmed-M15 penetration/reclaim liquidity proxies, explicitly
  `proxy_not_order_flow=true` and `hidden_order_flow_claimed=false`;
- qualified realised-volatility/jump context;
- 5m/15m/60m recent movement;
- latest 5m absolute-return percentile versus prior non-overlapping 5m blocks;
- latest 5m range percentile and expansion/compression classification;
- scheduled-event timing context;
- `causal_attribution_proven=false` and `cause_unknown=true` for elevated/extreme
  recent moves until a later phase provides causal evidence;
- explicit unknown list and deterministic digest.

Safety flags are unconditional:
`research_only=true`,
`descriptive_context_only=true`,
`predictive_edge_claimed=false`,
`live_money_execution_allowed=false`,
`future_values_used=false`.

## Consumer safety

Super Signals production already accepts v1/v2 Gold-state envelopes and was independently
deployed with 1116 API tests passing. The isolated PR #208 strengthens v2 intake to reject:

- wrong engine version;
- non-research packets;
- future-valued packets;
- malformed/absent digest;
- missing required sections;
- hidden-order-flow claims;
- causal-attribution claims;
- research surfaces being promoted as decision inputs.

Its prompt explicitly states that close paths are descriptive, liquidity signals are proxies,
round numbers are descriptive, event proximity is not causality, and `cause_unknown=true`
must stay unknown.

## Production blast radius

No Phase 2 isolated branch is merged into the live reasoning path. Production remains:

- Super Signals SHA `4650d2074ea4d4287285783a5157d4340cd41e8a`
- Render deploy `dep-dan2p2dii2qc73bi09h0`
- Phase 1 grounding monitor: `waiting_forward_rows`, 0 invalid rows
- AIDY live-money authority: OFF
- owner risk: 1%, unchanged
- standalone Worker: healthy, capture enabled, formal-forward OFF, Twelve Data/public-independent

## Verification limitation

GitHub Actions credits are exhausted. PR jobs complete immediately with no steps/logs, matching
the repository's already-documented Actions-credit outage. Do not interpret the red checks as a
code-test result, and do not claim these isolated heads have a green full suite.

The branch-level blast radius was inspected by compare:
- AIDY PR touches only Gold-state/private-forward/provider-context/health/workflow/tests.
- Super Signals PR touches only AIDY context intake/reasoning and tests.
- no broker, execution, sizing or provider-status files are touched.

## Graduation

Do **not** merge/activate PR #208 and do not grant Phase 2 authority until Phase 1 has fresh
forward evidence-v2 rows and reaches `accepted`. Once that occurs, run the full standalone
suite outside/after the Actions-credit outage, merge PR #137, execute the safe provider-read
Worker deployment with formal-forward forced OFF, verify public health reports v4/v1/v2
versions, then merge the Super Signals consumer only after its own full regression passes.
