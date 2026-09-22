# Super Signals — Real MT5 dashboard balance hotfix — 2026-09-22

## Owner request
Fix the private app so the account card shows the real MetaAPI/MT5 account values instead of a reconstructed Super Signals balance.

## Root cause
`CanonicalDashboardRuntimeService.read()` read the correct MetaAPI account state through the Day 32 dashboard service and then overwrote Balance, Equity and Free Margin using `CanonicalTradingAccountingService.displayed_balance()` plus locally visible floating P/L. This made the app capable of disagreeing with MT5.

## Fix
Production branch: `feature/day-10-shared-telegram-sources`
Merged PR: #245 — `Show real MetaAPI MT5 balance in app`
Live commit: `7a8f61322077adef20c78acb80daefb18e91bd83`

Changes:
- Dashboard now returns MetaAPI account values unchanged.
- App card labels the figures explicitly as:
  - MT5 Balance
  - MT5 Equity
  - Floating P/L
  - Free Margin
  - MetaAPI refresh time
- Cached account values are shown only as last-confirmed fallback during a connection error.
- No provider rules, live trade execution, subscriber balances, Telegram lifecycle logic or AIDY authority changed.

## Verification
Dedicated workflow: `MT5 Balance Truth Gate` — PASS.
Private app web quality — PASS:
- typecheck
- lint
- web tests
- production web build

Render deploy:
- service: `super-signals-day-8`
- deploy: `dep-dapa36rncjis73a5bcp0`
- new process started 2026-09-22 15:42:22 UTC
- application startup completed 2026-09-22 15:42:53 UTC
- Render health probe returned HEAD / 200 OK.

## MetaAPI truth observed before hotfix
Most recent direct Day23 MetaAPI audit reads showed the owner demo account around:
- balance: $1,457.96 to $1,460.24
- equity: about $2,097 to $2,119 depending on live floating P/L
These are distinct MT5 concepts. The app now shows them separately instead of replacing them with a synthetic balance.

## Completion rule
This hotfix is complete because the code is merged, focused regression is green, web quality is green, the new Render process started successfully and the Memory repo handoff is recorded.
