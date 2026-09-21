# AIDY factual cycle-start environment v2 — LIVE

Date: 2026-09-21

## Final repository/runtime state

Authoritative AIDY repo: `dannythehat/Aidy-Gold-Signals`

Current repository `main` after repo-local memory handoff:
`1635f68a4ed98298f979d6d13521c21c1b0e4463`

Runtime/environment-v2 code is included in the deployed lineage ending at:
`ede4904cc4586320efe120b3e6f9bf72b4c11a40`

Canonical Worker:
`aidy-signals-test`

Live Worker version:
`240739fb-849e-410f-a805-70a1e4496514`

Successful canonical deploy run:
`35565777824`

Final live environment audit run:
`35565912418` — SUCCESS

## What was built and why

The owner clarified that AIDY should learn tool usefulness by the **factual market environment present at cycle start**, not by one universal score per tool.

A new canonical environment contract is live:

`aidy_gold_cycle_environment_v2`

The environment is frozen **before** the target 15-minute window. It separates:
- facts known at decision time;
- directional marker opinions;
- future outcomes.

Exact values are retained for audit, while repeatable condition buckets are used for learning. This avoids the failure mode where exact price makes every environment unique and prevents sample accumulation.

## Cycle-start facts now frozen

Where PIT-safe evidence exists, each new cycle environment contains:
- decision timestamp and lead time;
- named session and session phase;
- minutes since Asia/London/New York opens;
- M5/M15/H1/H4/D1 completed-bar state;
- 5m/15m/60m recent direction, return and range;
- exact Gold mid for audit;
- exact distances to known price/liquidity references;
- repeatable distance bands to the nearest reference;
- side of the nearest reference;
- prior-day/Asia/session/opening-range position;
- liquidity sweep/reclaim signature;
- prior-day breakout/reclaim state;
- realised-volatility, jump/continuous, vol-of-vol, GVZ and IV-RV availability state;
- scheduled-event state/proximity when operationally known;
- cross-market series availability/state;
- compound regime;
- explicit UNKNOWN values.

Environment facts are **not automatically directional predictions**.

## Repeatable learning dimensions

The environment fingerprint now includes repeatable buckets such as:
- session;
- session phase;
- UTC weekday;
- prior 15m state;
- M5/M15/H1/H4/D1 direction;
- recent displacement state;
- recent range regime;
- 60m direction;
- nearest reference identity;
- relative side;
- distance-to-reference band;
- prior-day range zone;
- Asia range zone;
- active-session zone;
- liquidity reclaim signature;
- prior-day breakout state;
- volatility state;
- jump state;
- event timing/proximity;
- count of known cross-market inputs;
- compound regime.

## Contextual scorebooks expanded

The marker brain is now:
`aidy_gold_contextual_marker_brain_v2`

Cycle memory is:
`aidy_gold_cycle_memory_v3`

The scorebook can learn at 13 scopes:
1. global;
2. session;
3. session phase;
4. session + prior 15m state;
5. higher-timeframe alignment;
6. liquidity + price location;
7. session + liquidity;
8. location + higher-timeframe structure;
9. session + movement regime;
10. volatility + movement regime;
11. session + state + event timing;
12. event regime;
13. full environment.

AIDY still falls back toward broader scopes when specific environments have too few observations.

## Toolbox and scoring unchanged in principle

Canonical toolbox evaluated per cycle: **34 capabilities**.

Every capability is considered each cycle. Only legitimately directional/PIT-safe evidence receives a directional marker score. Context-only or unavailable tools remain explicit rather than receiving invented votes.

Marker scoring remains:
- +2 large/meaningful correct;
- +1 normal correct;
- 0 unavailable/unscoreable;
- -1 normal wrong;
- -2 large/meaningful wrong.

Current large-move threshold:
`abs(realised 15m return) >= 5 bps`.

Learned multipliers remain bounded to 0.5x-1.5x and sample-size protected.

## Live proof

Final live D1 audit observed environment v2 for the cycle:
`2026-09-21T05:45:00+00:00`

Frozen facts/learning dimensions included:
- session: `asia`;
- session phase: `late_gt240m`;
- nearest reference: `asia_opening_30m_low`;
- Gold side: `below`;
- nearest-reference distance band: `close_3_8bp`;
- prior-day zone: `lower_middle`;
- liquidity signature: `low_side_reclaim`;
- five-minute range state: `normal_range`;
- H1 direction: bearish;
- H4 direction: bullish;
- known cross-market inputs: 4;
- toolbox items considered: 34;
- environment scopes: 13;
- future values used: 0;
- live-money authority: 0.

The same cycle's reasoning audit showed:
- observed state: bearish;
- AIDY view: bearish;
- 3 supporting reasons;
- 4 contradictory reasons;
- 12 unavailable-evidence items;
- 6 toolbox surfaces used directionally;
- all 34 toolbox items considered.

## Persistent cycle health

A dedicated D1 singleton now records Gold cycle-sync health.

Live audit at `2026-09-21T05:48:01.095000+00:00`:
- status: `ok`;
- creation reason: `outside_view_lead_window`;
- no error type;
- no error message.

This makes skipped/non-created cycles distinguishable from actual cycle-learning failures.

## Repo-local memory completion

The AIDY repository itself now contains:
- `README.md` pointing to the current learning state;
- `docs/current-gold-learning-state.md` as the detailed authoritative architecture/rationale;
- root `MEMORY.md` as the obvious repo-level handoff entry point.

This was explicitly requested by the owner so future work can understand **what was built and why** directly from the actual AIDY repository.

## Safety boundary

No change to:
- Super Signals execution;
- MetaAPI / MT5 / Vantage;
- owner 1% risk;
- provider activation rules;
- formal-forward/live-money authority.

Formal forward remains OFF.

## Completion gate

Complete:
1. canonical environment contract built;
2. marker brain switched to environment v2;
3. cycle memory switched to v3;
4. repeatable location/liquidity/session/event/volatility scopes added;
5. tests enforce repeatable bucket identity instead of exact-price identity;
6. deploy gates updated;
7. Worker deployed;
8. cron verified;
9. live cycle environment v2 row verified;
10. 34-tool coverage verified;
11. persistent cycle-sync health verified;
12. repo-local AIDY memory updated;
13. separate Memory handoff updated.

The forward learning system can now accumulate evidence about **which tools are trustworthy under which Gold environments** instead of learning one universal tool ranking.
