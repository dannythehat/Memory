# Super Signals — Current State

Last verified project snapshot: **2026-09-06**

Authoritative source repo: `dannythehat/super-signals`

## Production branch warning

The repository default branch is `main`, but the live Super Signals production line has been the long-lived branch:

`feature/day-10-shared-telegram-sources`

Do not assume `main` is production. Verify the live Render deploy and production branch before changing or describing production.

Last known live production SHA from the Sept 5 verification: `9a0080acc06ebc8783ec0b5f44405ee01303fa27`.

Live service at that verification: Render `super-signals-day-8`.

## What Super Signals does

Private Gold/XAUUSD app that reads Telegram provider signals/instructions, interprets entries/SL/TP/management, and can execute/manage trades through the MetaAPI/Vantage MT5 path for authorized users.

Provider Lab runs alongside production to learn/evaluate providers without giving discovery sources broker authority.

## Critical provider split

Never confuse these populations:

- **40 shadow providers** = discovery/research pool. They must remain broker-isolated.
- **5 testing providers** = current real execution providers with broker-deal history.
- 14 paused and 4 revoked sources were also present in the latest roster audit.

The active research universe is 45, but **40 shadow + 5 real/testing are not interchangeable**.

## Provider Lab state

Recent production work added:

- adaptive provider language/behaviour profiles;
- deterministic AIDY M1 Provider Lab replay for eligible intraday/swing evidence;
- explicit shadow-safe routing;
- app-owned AIDY resolver startup independent of broker credentials;
- production logs proving resolver batch outcomes.

Recent delivery PRs on the production branch include #133, #135, #136, #137 and #138.

## Cross-project relationship

AIDY supplies bounded, PIT-safe Gold market evidence/context to Provider Lab. Super Signals owns provider interpretation, benchmark/replay and broker/member execution. AIDY does not own the broker path.

## Current priority

AIDY hardening/intelligence build is being completed first through Day 6, then the broader provider-intelligence roadmap continues. Super Signals production must remain protected while research intelligence is improved.

Before acting, verify the production branch, latest Render deploy, database state and relevant runtime logs.
