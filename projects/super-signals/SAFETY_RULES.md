# Super Signals — Safety Rules

## Real-money boundary

- Live broker/member execution is the highest-risk path. Research must not block, duplicate or mutate it.
- Shadow discovery providers must never reach broker/member execution.
- Testing/live provider eligibility must remain explicit and evidence-backed.
- Paused/revoked sources must not be reactivated implicitly.

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
