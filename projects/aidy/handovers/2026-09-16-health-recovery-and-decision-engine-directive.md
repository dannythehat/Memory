# AIDY Handover — 16 September 2026

## Latest recovery update — read this first

The original handover below was written before the PR's final lint correction. The current facts override the older SHA/test figures in the historical section below.

- AIDY `main` remains `bf3bb05ca5a9320e31173bbd93f41cf797b6ed51`.
- PR #133 current head is `01c6a955c5c7c513a6db86f70cdc2e7d146ea246`.
- The prior head `06ffdc8d...` had a real Ruff `UP035` failure (`typing.Mapping`). Claude fixed only the import to `collections.abc.Mapping`; compare shows this final commit changes only `src/aidy/provider_context_api.py` by +2/-1.
- Exact current-head external acceptance: Ruff PASS, compile PASS, focused **33/33**, full **1270/1270**.
- Provider Context remains observational-only with `live_money_execution_allowed=false`; the separate formal-forward complete-snapshot gate remains unchanged.

The exact GitHub ruleset has now been independently read through the ChatGPT GitHub connection:

- id `22096458`, `Protect main`, enforcement active;
- deletion protection active;
- non-fast-forward protection active;
- PR required, 0 approvals required;
- bypass actors none, current connected user bypass `never`;
- required checks are exactly `Evidence Semantic Change Gate / classify-protected-diff` and `AIDY Day 53 Twelve Data OHLC Adapter / acceptance`.

The ChatGPT connection can read but not write rulesets. GitHub browser automation is not authenticated. Repository auto-merge is disabled. A direct branch-ref bypass was deliberately **not** attempted because it would violate the protection intent.

No Cloudflare write/deploy plugin is available, and Cloudflare browser automation is not authenticated. Therefore the two remaining steps require an owner-authenticated GitHub/Cloudflare session:

1. temporarily remove **only** the two unavailable required checks from `Protect main`, merge exact head `01c6a955...`, and preserve all other protections;
2. deploy the merged Worker manually while preserving minute Cron/capture/Twelve Data/public-independent/formal-forward OFF, then verify health and fresh Super Signals attachment.

Latest Worker health rechecked after the PR documentation update:

- status `degraded`;
- latest scheduled capture success `2026-09-16T18:22:09.331000+00:00`;
- capture lag 88 seconds;
- latest Provider Context snapshot `2026-09-15T20:57:36.761999+00:00`;
- Provider Context lag 77,161 seconds;
- formal forward OFF.

PR #133 body and conversation were updated with these exact facts so the repository itself now carries the current recovery evidence.

## Why this exists

This handover records the current AIDY production-health blocker, the GitHub Actions constraint, the recovery path, and the owner's next-stage product directive: AIDY must progress from passive Provider Intelligence into an evidence-scored trading decision engine.

## Production diagnosis

Market capture is healthy and direct-Cron scheduled capture continues. Provider Context is stale, so Super Signals correctly fails closed rather than consuming old context.

The recovery change permits Provider Intelligence to consume a fresh scheduled partial snapshot only when M1/M5/M15/H1/H4 are present and D1 alone is missing. It does not relax formal-forward completeness.

## GitHub Actions constraint

The owner confirms GitHub Actions credits are exhausted for approximately one week. On the current PR head, both required jobs still fail in about two seconds before normal runner execution.

Do not keep rerunning unavailable Actions jobs. Do not make AIDY runtime continuity depend on CI availability.

## Exact remaining recovery sequence

1. Owner-authenticated GitHub: edit ruleset `Protect main` id `22096458` and temporarily remove only the two unavailable status-check requirements.
2. Merge PR #133 at exact head `01c6a955c5c7c513a6db86f70cdc2e7d146ea246`.
3. Restore required checks when operationally useful / once Actions credits return, without weakening deletion/non-fast-forward/PR protections.
4. Owner-authenticated Cloudflare/local terminal: deploy canonical Worker preserving `* * * * *` direct Cron, `capture_enabled=true`, Twelve Data/public-independent market ownership and `AIDY_FORMAL_FORWARD_ENABLED=false`.
5. Verify Cloudflare schedule state after deploy, not only config files.
6. Verify `/health` no longer reports stale Provider Context.
7. Verify a genuinely current Super Signals provider signal receives current AIDY context instead of `pit_context_stale`.

Do not call recovery GREEN until these production checks are complete.

## Owner product directive — now central

After months of AIDY and Super Signals work, the owner wants AIDY to become measurably useful in trading decisions very soon.

Target flow:

`provider signal -> PIT-safe market context -> provider history -> current exposure -> AIDY decision -> broker action -> outcome -> counterfactual score -> learning`

Target decisions:

- `APPROVE`
- `DENY`
- `HOLD/NO_SECOND_ENTRY`
- `CONFLICT_DENY`
- `CLOSE_EARLY`
- `CONTINUE`

Each authority class must be separately proven and graduated. Do not grant uncontrolled model discretion.

## Reuse existing Super Signals foundations

Do not rebuild capture/scoring/governance from scratch. Existing infrastructure already includes:

- `provider_trade_observations` as the durable per-signal/provider evidence spine;
- `provider_trade_scorer.py` and `provider_trade_scores` for deterministic outcome scoring;
- `provider_trade_scoreboard` for provider aggregates;
- `canonical_signal_ledger.py` and `signal_events.py` for same-source duplicate/edit collapsing;
- `provider_day14_governance.py` for fail-closed learning -> shadow -> qualified governance;
- `provider_day18_combined_book.py` for combined-book/conflict research.

Build a small immutable AIDY decision layer on top. Genuinely new/incomplete work is the persistent hypothesis/question registry and cross-provider duplicate/exposure clustering.

## Mandatory Decision Ledger

Every AIDY decision must freeze only the evidence available at decision time: signal/provider/message identity, decision timestamp, exact AIDY snapshot/context IDs and digests, provider evidence then available, open exposure, duplicate/conflict state, decision reasons, confidence/uncertainty, rules/model version and resulting action when authority exists.

Future outcomes must never rewrite the original decision state.

## Mandatory counterfactual scoring

Every decision must later be compared with a fixed baseline.

- denied trade -> compare with following the provider normally;
- early close -> compare actual AIDY close with the original provider-management outcome;
- approved trade -> score realised P&L, MFE/MAE, TP progression and management quality.

Persist factual `decision_delta`. Do not claim money was saved unless the baseline demonstrates it.

## Provider Intelligence questions AIDY must answer

Move beyond one overall win rate. Study provider BUY vs SELL, session/time/weekday, observable volatility/regime/liquidity conditions, TP progression, small-profit versus runner style, initial-call versus management quality, provider close/BE/SL/cancel effectiveness, duplicate/edit/repost habits, latency/slippage sensitivity, agreement/conflict, stop/entry geometry, adverse duration, recovery/re-entry and provider-regime specialisation.

If evidence is insufficient, answer `unknown`.

## Persistent hypothesis/question registry

Each question needs a stable ID, exact cohort/filter, required features, metric, minimum observations, current sample size, answer/status, uncertainty, last calculation, supporting trade/decision IDs and observational-only versus decision-eligible status.

Retrospective findings do not automatically become live rules. Freeze the definition and validate prospectively.

## Duplicate/conflict engine priority

AIDY must distinguish already represented exposure, edit/repost, same-direction equivalent risk addition, opposite exposure and genuinely independent trade ideas. Build cross-provider exposure clustering on top of the existing same-source canonical ledger and combined-book research.

If evidence cannot justify choosing between conflicts, fail safely rather than inventing certainty.

## Authority graduation

Once Provider Context is healthy, begin shadow AIDY decisions for every eligible trade immediately and score them prospectively.

Likely authority order:

1. deterministic duplicate rejection;
2. obvious duplicate/conflicting exposure controls;
3. provider/regime denies;
4. early-close management;
5. broader approve/deny/management authority.

Every authority class requires a kill switch, immutable audit trail, prospective evidence and explicit owner/live gate. The Super Signals 1% live-risk directive remains unchanged unless explicitly changed.

## Success definition

The core business question is whether AIDY prospectively improves Super Signals versus following providers unchanged. The durable metric is factual decision delta segmented by decision type, provider, direction, session and regime.