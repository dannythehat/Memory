# AIDY — Known Issues / Deferred Work

Only keep unresolved or deliberately deferred items here. Remove or move items to a handover when resolved.

## Current

1. **Archive poison retry lifecycle** — Day 5 detects stale/retrying/poison archive items, but the live archive schema/runtime does not yet have bounded backoff + explicit dead-letter state. This is Day 6.
2. **Formal-forward remains OFF** — do not treat forward-decision infrastructure as real-money authority.
3. **Provider-market bearer credential hygiene** — any rotation/remediation must be synchronized with Super Signals and performed in a controlled window with rollback. Never expose the token value.
4. **Committed-secret history remediation** — deleting a file in a later commit does not erase Git history. Any final cleanup must be deliberate and must not casually rewrite protected production history.
5. **Real-market acceptance evidence** — where a test specifically requires a genuine open-session observation, do not substitute closed-market or synthetic evidence.

## Rule

Before acting on this file, verify whether a later source-repo commit/PR already resolved the item. Memory can become stale.
