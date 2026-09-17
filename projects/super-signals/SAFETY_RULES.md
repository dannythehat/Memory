# Super Signals — Safety Rules

## Real-money boundary

- Live broker/member execution is the highest-risk path. Research must not block, duplicate or mutate it.
- Shadow discovery providers must never reach broker/member execution.
- Testing/live provider eligibility must remain explicit and evidence-backed.
- Paused/revoked sources must not be reactivated implicitly.

## One pipeline, paper and real, any balance — owner directive 2026-09-17

Paper (demo-account) and real-money execution are treated as equally serious, run through
the **same** execution/sizing pipeline, and must never fork into separate code paths keyed
on account mode or balance size. Funding €50 or €10,000 changes only what 1% (or the
selected risk percent) computes to in cash — never which logic runs. This already matches
the architecture as built: `active_account_execution.py`'s own docstring states "one
canonical active MT5 slot that may be either Vantage Demo or Vantage Live," `_load_demo_account`
is a direct alias of `_load_active_account`, and `risk_sizing_day24.py` computes purely
from "the real broker account balance" with an explicit small-account guard (the broker-minimum-lot
accommodation is capped at 2.5% actual risk specifically so a tiny account is never overexposed
by a lot-size floor). Verified 2026-09-17: 4 sources currently at `status='testing'`
(paper/demo) run through the identical `positions` table and execution path as `live` sources.

This is a standing constraint on all future work, very much including the AIDY decision
layer being built under `OWNER_MANDATE.md`: a shadow/paper decision and a live decision use
the same reasoning, the same risk math, the same code. Never add an `if is_paper` /
`if balance < X` branch to execution or sizing logic. If AIDY needs to reason about
risk/reward at different balance sizes, that reasoning must be balance-*proportional*
(percentage-of-account), not balance-*tiered* (different logic above/below a threshold).

## Provider populations

Never answer a question about the 40 discovery/testing groups using the five existing real providers, or vice versa. Resolve the requested population before analysing results.

## Provider research

- Provider Lab may learn from durable historical language/behaviour, but historical entry/SL/TP values must not contaminate a new current signal.
- Current-message/direct-reply evidence remains mandatory where production execution requires it.
- Research/benchmark failures should be isolated from broker routing.
- Small-N benchmark results are learning evidence, not proof that a provider is best.

## AIDY boundary

- AIDY market data/context may inform Provider Lab through the explicit bounded provider-market interface.
- Super Signals provider outcomes/broker state must not be fed back into AIDY as independent market truth.
- AIDY formal-forward state does not grant Super Signals broker authority and vice versa.

## Production changes

- Verify the actual Render deploy and production branch before claiming a change is live.
- Do not assume repository `main` is the live production branch.
- Use rollback-ready production changes.
- Never expose broker credentials, Telegram session secrets, API keys or provider-market bearer tokens.

## User-facing privacy

Provider identities are private business intelligence. Do not expose provider names publicly unless the owner explicitly requests them for a private operational purpose.
