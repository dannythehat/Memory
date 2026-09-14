# AIDY — Known Issues / Deferred Work

Updated: **2026-09-14** (source-verified at `main` `cb0f4bc`).

Only unresolved or deliberately deferred items belong here. Verify against a later commit before
acting — Memory can become stale, and this file was badly stale before this update.

## Open

### 1. Formal-forward runtime state is unknown
Memory previously asserted `formal_forward_enabled: false` as settled. A scheduled campaign now
exists that is designed to switch it on. Neither the Worker variable nor the D1 campaign row has
been read. **Do not claim either state.** This is the single highest-priority verification in the
project. See `CURRENT_STATE.md`.

### 2. README documents a superseded market source
`README.md` still describes the keyless Gold-API reference price as the live source. The active
adapter is Twelve Data vendor-built M1 OHLC. The README should be corrected in the source repo so
a future agent does not act on the wrong feed identity — this is a documentation defect, not a
runtime defect.

### 3. Day 54 sample floor not established
At least 300 episode-independent, model-resolved decisions are required in one unbroken cohort
before forward inference. The current count is unknown. Data-quality failures and raw bursts do
not count.

### 4. Hub feeds are built but unconsumed
`/provider/data-health` and `/provider/decision-memory` are merged and authenticated but nothing
reads them. This is planned Super Signals work, not an AIDY defect.

### 5. Free-tier resource discipline
D1 read budget, archive outbox durability and capture freshness are each guarded by a watchdog
and a scheduled workflow. Preserve the bounded/indexed query discipline; do not introduce full
D1 scans. Preserve free-tier constraints unless the owner explicitly approves paid infrastructure.

### 6. Provider-market bearer credential hygiene
Any rotation or remediation of the shared AIDY↔Super Signals bearer token must be synchronised
with Super Signals, performed in a controlled window with rollback, and never near a market open.
Never expose the token value.

### 7. Committed-secret history remediation
Deleting a file in a later commit does not erase Git history. Any final cleanup must be
deliberate and must not casually rewrite protected production history.

### 8. Real-market acceptance evidence
Where a test specifically requires a genuine open-session observation, do not substitute
closed-market or synthetic evidence.

## Resolved since the previous version of this file

- **Archive poison retry lifecycle** — Day 6 delivered bounded backoff and an explicit
  dead-letter state, with a scheduled watchdog. Previously listed as open.
