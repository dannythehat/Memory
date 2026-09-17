# Super Signals / AIDY handover — 17 September 2026

## Production recovery completed

Super Signals production is live at source SHA:

`356dfcf1801f70c786ff7fa2de38ce88d55ec071`

Render service: `super-signals-day-8` (`srv-d9qmcgks728c73a555m0`)
Render deploy: `dep-dalma2gae00c739qlul0`
Deploy reached live: `2026-09-17T04:00:25Z`

Quality gate during Render build:

- 989 passed
- 93 skipped
- 0 failed
- 2 warnings

## What was fixed

`services/api/app/aidy_market_client.py` now protects the live AIDY M1 fetch path from transient transport failures with bounded retries and exponential backoff. Retryable conditions include connection/read timeouts, connection errors, protocol errors, HTTP 429 and transient 5xx responses. The intent is that one transient upstream/network failure cannot kill the resolution cycle.

## Post-deploy runtime proof

- `AIDY Provider Lab resolver loop started` at `2026-09-17T04:00:26Z`.
- `AIDY Provider Context live probe READY` at `2026-09-17T04:00:37Z`.
- Probe context lag: 196 seconds.
- No new AIDY error or `pit_context_stale` event was observed in the checked post-deploy window.

The stale `AidyContextTerminalMiss` state from 16 September must not be treated as current Super Signals production truth.

## Boundaries unchanged

- Gold/XAUUSD only.
- Owner live-risk directive remains 1% only.
- AIDY/provider research has no new broker/live-money authority.
- Existing TP management semantics remain unchanged.
- Weekend XAUUSD freeze remains unchanged.

## Next work

Provider Context is now READY, so continue the planned AIDY shadow decision / counterfactual learning work from the existing observation/scoring/governance spine. Do not create a parallel provider system. Verify live runtime and database truth before changing code because source/runtime evidence overrides this Memory record if production has advanced.
