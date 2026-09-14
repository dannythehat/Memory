# AIDY — Roadmap

Source-verified: **2026-09-14** at `main` `cb0f4bc`.

## Strategic destination

AIDY's purpose is to become an **independent Gold/XAUUSD trader-intelligence system**: to
understand what Gold is doing and why, form its own thesis, identify its own setups, judge or
disagree with providers, and eventually propose and manage its own trades.

Telegram providers are a training and evidence corpus, not AIDY's final purpose. This direction
does **not** change current live authority. Any additional broker authority requires forward
statistical validation plus an explicit owner gate.

## Completed build sequence

The previous version of this file stopped at Day 10 and listed Days 11–21 as "next". Those,
and a great deal more, are done. Reconstructed from merged branches and `docs/` contracts:

**Days 1–10 — foundation and evidence.** Cloudflare bootstrap, queue/scheduler, real evidence
capture, continuity auditor, BigQuery analytical memory, historical XAUUSD backfill, PIT as-of
reconstruction, deterministic Gold features, official macro event evidence, cross-market
evidence, objective context packet.

**Days 11–22 — understanding.** Deterministic Gold regimes, move detective, trade outcomes,
no-trade counterfactuals, setup taxonomy, historical Gold cases, historical analogue retrieval,
evidence grades, PIT adversarial integrity, Master Trader contract, OpenAI reasoning gateway,
deterministic safety gates.

**Days 23–40 — Architecture V2.** J1–J16 baseline, trader context composer, independent episode
retrieval, market structure calendar, price structure feed health, historical bid/ask (J3),
PIT-vintaged rates, tiered macro event intelligence, CME contract intelligence, GVZ volatility
state, PIT attestation trial registry, falsifiable Master Trader contract, immutable decision
ledger, context composer v2, Master Trader self-consistency, frozen replay CPCV, evaluation
scorers J16–J21, controlled strategy promotion, pre-paper architecture gate.

**Days 41–52 — trading behaviour.** GC shadow basis spine, genuine flow VWAP (J2–J3), richer
volatility (J7–J8), policy path cross-asset (J11–J14), selective abstention (J9–J10), paper
simulator invalidation, master watcher orchestration, manage/close v2 thesis-aware, management
replay counterfactual, private Telegram publisher, publication ledger delivery audit,
end-to-end fidelity restart.

**Day 53 — the forward boundary.** Architecture V2 launch integration, Twelve Data OHLC adapter
and qualification, D1 free-tier read-budget work, formal-forward freeze contract, immediate-start
amendment, genuine live Gold feed, live forward activation, deployment identity proof.

**AIDY Hub Phase A — data health.** `/provider/data-health`, `aidy_data_health_events`,
health telemetry wired into the Cron tick and the public `/health` response.

**AIDY Hub Phase B — episode memory.** Permanent episode ledger, decision→outcome→learning loop,
`/provider/decision-memory`, and a guarded forward-restart campaign.

Engineering completion is not statistical validation, and none of the above was runtime-verified
in the session that wrote this file.

## Next

### 1. Runtime verification (blocking)

Before any new AIDY build, confirm against Cloudflare and D1:

- Worker environment: `AIDY_FORMAL_FORWARD_ENABLED`, `AIDY_CAPTURE_ENABLED`,
  `AIDY_MARKET_DATA_SOURCE`.
- The active row in `aidy_forward_cohorts` for
  `aidy_formal_forward_cohort_v2_immediate_start`.
- `aidy_forward_restart_runs.acceptance_state` for
  `aidy_phase_b_repaired_forward_restart_20260913` — `activated` or `model_resolved`.
- Episode-independent model-resolved decision count against the Day 54 gate of 300.
- Whether `/provider/data-health` and `/provider/decision-memory` answer correctly in production.

Then repair `CURRENT_STATE.md` and `LIVE_STATE.json` with verified values.

### 2. Day 54 — forward inference

Only once at least **300 episode-independent, model-resolved** decisions exist in one unbroken
cohort. Data-quality failures do not count toward that floor. Raw bursts cannot substitute for
episode-independent N.

### 3. AIDY inside the Data Hub

AIDY's two Hub feeds are built. The remaining work is on the Super Signals side: consume them
and render AIDY's current bias/thesis, regime/session, levels, confidence, what it is watching,
invalidation conditions, recent decisions and learning cards. See the Super Signals roadmap.

### 4. Toward independent trading

Sequenced, and each step gated:

1. Continuous Gold-state comprehension (largely built — verify it actually runs).
2. Own thesis produced even when no provider posts.
3. Own setup generation with entry, invalidation and targets — research/paper only.
4. Provider adjudication: support, neutral, reject, conflict — with measured counterfactuals
   rather than an assumption that AIDY is right.
5. Forward paper/shadow evidence with execution-cost calibration and no hindsight.
6. Management intelligence: hold, BE, partials, trailing, exit timing, counterfactually scored.
7. **Graduation gate** — statistically validated forward evidence *plus* explicit owner approval
   before any new live-money authority. No roadmap item silently changes broker or risk policy.

## Rule

Engineering completion is not statistical validation. Formal forward is paper. Performance
improvement is never a valid reason to break a cohort freeze.
