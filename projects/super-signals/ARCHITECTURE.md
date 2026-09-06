# Super Signals — Architecture Memory

This is a compact map. Verify implementation details in `dannythehat/super-signals` and live Render/Postgres before acting.

## Core responsibility

Super Signals is the private provider-signal ingestion, interpretation, execution and user-account application.

## Main layers

1. **Telegram ingestion** — provider/source-aware message capture.
2. **Interpretation/canonical signal layer** — current signal/management extraction with provider-aware semantics.
3. **Provider Lab** — isolated research/shadow benchmarking and adaptive provider profiles.
4. **AIDY resolver** — deterministic Provider Lab replay using bounded AIDY XAUUSD M1 market truth for eligible research.
5. **Execution router** — live/testing broker/member path through MetaAPI/Vantage MT5.
6. **Trade management** — SL/TP/BE/closure/cancellation lifecycle handling.
7. **Member/account controls** — subscription/access, pause/resume/revoke, MT5 links and permissions.
8. **Web/PWA UI** — balances, trade history, notifications, admin/provider controls.
9. **Render/Postgres production** — application/runtime and durable operational/provider data.

## Provider Lab principle

Research sidecars should be fail-safe relative to live execution: a benchmark/profile/replay failure must not block or mutate broker routing.

## AIDY relationship

Super Signals consumes a bounded authenticated PIT-safe market feed from AIDY for Provider Lab research. AIDY remains independent market/context infrastructure; Super Signals remains provider/execution infrastructure.
