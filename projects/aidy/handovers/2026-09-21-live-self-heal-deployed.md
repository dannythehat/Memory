# AIDY live self-heal deployment — 2026-09-21

## Result

AIDY repository `dannythehat/Aidy-Gold-Signals` was temporarily made public by the owner so GitHub-hosted public runners could be used after private Actions minutes were exhausted.

Final deployed AIDY main SHA:

`aebb414656e9e1f6f30f2cf954366085792dca6f`

Final successful deployment workflow run:

`35557298002`

The deploy completed successfully at `2026-09-21T03:23:24Z`.

## What changed

1. Removed duplicate GitHub-scheduled AIDY monitoring:
   - archive watchdog 10-minute schedule removed
   - capture freshness watchdog 10-minute schedule removed
   - D1 budget hourly schedule removed
   - Phase B forward restart 10-minute schedule removed and left manual-only

   This eliminates approximately 13,680 scheduled GitHub workflow launches per 30-day month.

2. Added bounded Twelve Data intraday Provider Context self-heal:
   - strict M1/M5/M15/H1/H4 completeness remains required
   - if scheduled capture is partial because of a small recent M1 gap, AIDY may repair only a bounded <=30-minute recent gap
   - repair uses the existing ledgered bootstrap admission path
   - broad historical bootstrap remains separate
   - generic config defaults self-heal OFF
   - canonical live config enables the bounded self-heal
   - formal forward remains OFF
   - live-money authority remains OFF

3. Aligned data health with the existing Provider Context rule that permits observational use when M1/M5/M15/H1/H4 are complete and D1 alone is missing.

4. Cleaned Ruff blockers and corrected synthetic test fixtures that had invalid OHLC geometry.

## Verification

Successful deploy workflow stages:
- checkout: pass
- Cloudflare credentials present: pass
- Ruff / compile / focused tests: pass
- live config build with minute cron: pass
- D1 migrations: pass
- Worker deploy: pass
- post-deploy configuration / cron / provider route verification: pass

Live Worker verification after deployment:
- service: `aidy-signals`
- runtime: `cloudflare-workers`
- status: `ok`
- scheduler: `direct-cron`
- capture_enabled: `true`
- market_data_source: `twelve_data`
- market_data_ownership: `public_independent`
- formal_forward_enabled: `false`
- Provider Context API: `aidy_provider_context_api_v5`
- Gold State Engine: `aidy_gold_state_engine_v1`
- Gold movement investigator: `aidy_gold_movement_investigator_v1`
- Gold movement memory: `aidy_gold_movement_memory_v1`
- data health: `fresh`
- latest scheduled capture observed: `2026-09-21T03:22:30.148000+00:00`
- latest Provider Context snapshot observed: `2026-09-21T03:22:30.148000+00:00`
- both lags observed at approximately 60 seconds

## Safety boundary

No Super Signals execution logic, provider best-side rules, 1% risk rule, MT5, MetaAPI, Vantage or live-money authority was changed.

The owner can return `Aidy-Gold-Signals` to private immediately after this deployment verification.
