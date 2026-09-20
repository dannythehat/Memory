# AIDY toolbox awareness + historical training stress — 2026-09-20

## Owner directive

AIDY must not merely have intelligence modules in repositories. He must understand which tools/evidence surfaces are available, know when each is relevant, use the relevant ones in his reasoning, and then be judged on historical outcomes without hindsight.

## Production commits

Super Signals live branch: `feature/day-10-shared-telegram-sources`

- PR #227 / `e21b4eded371e9c46038d5daaca6514399cf708b`
  - fixes edited-Telegram hindsight: executable edited revisions use their edit timestamp as effective signal time.
- PR #228 / `521b4c9002f7ffa22aae54a585c6edfbd5b10e53`
  - adds explicit research-only historical toolbox registry.
  - adds callable reconstructed calendar and focused evidence inspector alongside retrospective candles.
  - versions large stress replay to `aidy_historical_stress_lab_v6_toolbox` / input `aidy_historical_stress_input_v5_toolbox`.
- PR #229 / `134a81d79fe88d6b2343a08e657d6307a1d30402`
  - reasoning prompt becomes `aidy_reasoning_prompt_v12_toolbox`.
  - teaches AIDY to inspect toolbox_manifest, consider every available standing surface, call relevant tools when material, avoid checklist/noise calls, and preserve UNKNOWN for unavailable evidence.
  - live reasoning gets `aidy_live_toolbox_manifest_v1` on every reasoning call.
- PR #230 / `36dee29f4b87dfe2f94bb02ea19f21c612b363d4`
  - aligns historical supplemental-evidence key to `toolbox_manifest` so the toolbox-aware prompt sees it.
- PR #231 / `e92c46f92d7c9679066fbdbbb1bd46dd281d4029`
  - adds per-decision tool-use telemetry so AIDY's historical exam records which on-demand tools were actually called.
  - measured stress replay becomes `aidy_historical_stress_lab_v7_tooltrace`; old v6 decisions cannot be mixed into the measured run.
- PR #232 / `5b09fea3f7707a8f752c888f187c99c1a531f8e7`
  - freezes the 571-case training identity independently with SHA-256 `18326c515d12a7e55046828f6fe59198de50b0b7538193174528bf56f7829168`.
- PR #233 / `f85a0456d1d0cf566c4b6eb4ecdc0c3722e22abb`
  - adds research partition/evidence/run-scope DB support. Its first Render deploy failed safely and transactionally because the replay scoreboard view depended on the partition column.
- PR #234 / `745b5af537cd0028535cb5e7400255b49d101156`
  - drops/recreates the replay scoreboard view around the schema changes.
  - live Alembic head is `0108_aidy_hist_stress_schema`.
  - direct Postgres verification confirms research partitions, `reconstructed_research`, train scopes and varchar(32) partition columns.
  - canonical Render Docker gate: 1,191 passed, 137 skipped, 2 warnings.
  - late historical rows in validation/OOS can no longer block or contaminate training.
  - evaluation scopes retain the original full-cohort guard and remain fail-closed until their 69/160 frozen identities are explicitly restored.

## AIDY's currently connected reasoning toolbox

On-demand callable:
1. recent XAUUSD candles
2. economic calendar
3. historical-only focused evidence inspector in stress replay

Standing evidence considered in reasoning:
- provider evidence/history claims
- market context / Gold state
- recent provider messages
- event/liquidity/execution context
- provider alpha + historical analogues
- probability / EV / management context
- failure attribution / self-critique
- self-calibration where available

The rule is NOT to mechanically call every tool on every trade. AIDY must consider every available surface and call an on-demand tool when it can materially resolve uncertainty relevant to take/reduce/reject. Irrelevant tool calls are noise.

## Wider AIDY research modules

The AIDY research repository contains additional work including macro vintages, cross-market as-of, CME contract intelligence, GVZ/volatility, semantic context composition and provider decision memory.

These are NOT to be falsely treated as connected callable tools. Until an auditable timestamp/provenance adapter connects them to the Super Signals reasoning contract, the toolbox explicitly reports them as UNKNOWN/not connected or standing-state-only.

## Historical exam safety

Frozen large scoreable cohort: 800
- training: 571 (independently hash-frozen for the active exam)
- validation: 69
- OOS: 160

The live source-universe query now returns 803 eligible historical rows (571/70/162) because three late rows arrived in evaluation partitions after the original freeze. They are NOT admitted into the frozen evaluation set. Training remains 571.

Current stress configuration:
- `AIDY_HISTORICAL_STRESS_ENABLED=1`
- `AIDY_HISTORICAL_STRESS_SCOPE=train`
- `AIDY_HISTORICAL_STRESS_OPEN_VALIDATION=0`
- `AIDY_HISTORICAL_STRESS_OPEN_OOS=0`

Therefore only the 571-case training partition may be used for tuning. Validation and OOS remain sealed.

Exact replay v10 (`aidy_historical_time_machine_v10_effective_time`) remains disabled by configuration and its 18-case holdout remains sealed.

## Verification

Render Docker quality gates:
- after PR #228: 1,187 passed, 137 skipped, 2 deprecation warnings
- after PR #229: 1,189 passed, 137 skipped, 2 deprecation warnings
- health endpoint remained 200
- no broker execution, risk sizing, MT5, or provider-routing changes were made by this toolbox work.

GitHub Actions jobs showed failure without executing steps/logs; Render's Docker quality gate is the substantive test gate currently available.

## Empirical result gate

Do NOT call this training exercise successful until `aidy_historical_stress_lab_v6_toolbox` has:
1. materialized the frozen 571 training cases,
2. produced fresh toolbox-aware decisions,
3. scored them,
4. been compared to the training provider baseline,
5. had tool-call usage and false-reject/false-reduce behaviour audited.

Training baseline already frozen: provider/scorer P&L +$300.45 across 571 cases.

Do not open validation/OOS until a candidate decision policy is frozen from training.

## Important prior calibration lesson

Earlier exact replay showed 42 trades that the model tried to reduce but Build-5 calibration restored to full TAKE produced +$620.49. Therefore AIDY must not learn blanket caution. The target is precise identification of bad trades, while preserving good exposure.

## Next gate

Finish the 571-case v7 toolbox-aware + tool-traced training run; report shadow P&L, delta vs provider baseline, action distribution, tool-call distribution by exact tool name, losses avoided versus winners cut, and only then freeze a candidate before opening validation.


## v7 diagnostic failure and v8 correction

The first tool-traced v7 run proved the toolbox-awareness prompt was insufficient by itself.
v7 wrote 55 decisions with **0 model tool calls and 0 preflight evidence calls**. Of the 46
rows scored before shutdown, provider-taken P&L was +$31.84, AIDY shadow P&L +$23.71 and
delta -$8.13. v7 is therefore preserved as failed diagnostic evidence and must not be used as
the candidate policy.

PR #235 / `79e00b0f514aeb184918f736ce456830a742dab7` introduced
`aidy_historical_stress_lab_v8_preflight_router`. It mirrors the live reasoning runner's
discipline: M15 structure is routed before every decision; H1 is added when trend/volatility is
unclear; high-impact calendar evidence is focused when event timing is unknown or an event is
within six hours; frozen provider evidence is inspected when available. It records preflight
tool names/results separately from any model-initiated tool calls.

Render Docker gate: **1,194 passed / 137 skipped / 2 warnings**. Deploy
`dep-danvn2f40ujc73dc8ev0` is live. Environment is train-only:
`AIDY_HISTORICAL_STRESS_SCOPE=train`, validation=0, OOS=0. Live
`AIDY_REASONING_ENGINE_ENABLED=1`.
