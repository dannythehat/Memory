# Super Signals — Known Issues / Open Risks

Updated: **2026-09-13**

## 1. Forward statistical evidence is still sparse
The B-F intelligence layer is engineering/prod verified, but broad provider ranking/profitability/promotion claims are not statistically validated yet. Use `WAITING-FOR-FORWARD-EVIDENCE` where sample floors are not met.

## 2. Stale settlement errors can keep the fast path hot on weekdays
Four historical August positions with `broker_filled_position_not_visible` remained in an unsettled/error shape and previously caused repeated deal-history settlement work. Preserve the audit rows but quarantine them from the fast settlement path after bounded retry/repair handling.

## 3. Protection polling performs unnecessary broker reads
The profit-protection path can fetch positions/orders even when there are no protection plans. Compute plans first and return before broker reads when the plan set is empty.

## 4. Redundant MetaAPI XAU price read
The UI Gold quote is sourced from the free Gold feeds, but dashboard broker-state collection still performs a MetaAPI XAU price request alongside account/position reads. Remove that redundant broker read where it is not required for execution logic.

## 5. Usage telemetry is incomplete
Exact OpenAI token/cost telemetry and consolidated MetaAPI request telemetry are not persisted. Historical decision counts show deterministic-first routing dramatically reduced OpenAI use, but cost/request observability should be made explicit.

## 6. Weekend edited-message replay edge
Original messages posted during the weekly closure are blocked. A pre-weekend message edited during closure may still have a narrow recovery path after reopen through direct edit/recovery handling. Add an `edited_at` freeze boundary if the owner wants a strict no-weekend-content replay guarantee.

## 7. Data Hub not built yet
The B-F current views exist, but the owner-facing AIDY Data Hub has not yet been implemented. It is the next substantive product build.

## 8. Independent AIDY trader is a strategic destination, not current live authority
The owner has clarified that AIDY must become capable of understanding Gold and proposing its own trades. That capability is not yet equivalent to validated independent live trading. Own-thesis/setup generation must be built and forward-tested before any authority change.

## 9. Provider interpretation failures remain a business-critical regression class
Past incidents include missed new trades, duplicate edited posts, missed `move SL` / `take loss` updates, hidden/open trades not visible in the app and provider-specific grammar failures. New provider fingerprints/adaptation improve the architecture, but forward monitoring must prove actual capture/interpretation quality across the full intended provider roster.

## 10. Runtime/UI reliability issues remain relevant
Historical issues include notification delay, stats refresh delay, login persistence, empty account state, calendar trade visibility and balance/equity presentation. Do not assume these are fixed solely because provider intelligence advanced.
