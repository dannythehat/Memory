# AIDY — Known Issues / Deferred Work

Updated: **2026-09-16**

Only keep unresolved or deliberately deferred items here. Verify source/runtime before acting because Memory can become stale.

## Current

### 1. Provider Context is stale while market capture is fresh — ACTIVE / RED

The Worker is capturing fresh Twelve Data on direct Cron, but the latest accepted Provider Context snapshot is still from `2026-09-15T20:57:36.761999+00:00`. Current Super Signals joins therefore fail closed with `pit_context_stale` / `AidyContextTerminalMiss`.

Open AIDY PR #133 (`06ffdc8dc87c8aba8e521b237e181121fbd82cfd`) is the engineering-proven recovery path. Exact head passed 17/17 focused tests and 1270/1270 full tests externally, but the change is not yet production verified.

### 2. GitHub Actions unavailable due exhausted credits — TEMPORARY OPERATIONS BLOCKER

The owner reports GitHub Actions credits are exhausted for approximately one week. Required AIDY checks have been failing with 0 ms runner execution.

Do not repeatedly rerun unavailable CI. Use trusted external exact-SHA acceptance for urgent recovery work while preserving branch-protection intent, and restore normal required-check operation when credits return.

### 3. Formal-forward/live-money authority remains OFF

Do not treat new Decision Ledger, shadow decisions or provider intelligence as live-money authority. Decision classes must be separately graduated through prospective evidence and explicit owner/live gates.

### 4. Decision intelligence not yet implemented end-to-end

The new central roadmap requires:

- immutable AIDY Decision Ledger;
- counterfactual scoring and factual decision delta;
- conditional provider intelligence;
- persistent hypothesis/question registry;
- duplicate/conflict exposure engine;
- prospective shadow decisions for every eligible trade after Provider Context recovery.

This is the next major product build after restoring current context health.

### 5. Provider-market credential hygiene

Any bearer/token rotation or remediation must be synchronized with Super Signals and performed in a controlled window with rollback. Never expose credential values in Memory, logs or chat.

### 6. Historical secret-remediation caution

Deleting a file in a later commit does not erase Git history. Any history rewrite must be deliberate and must not casually rewrite protected production history.

## Rule

Do not call AIDY fully healthy until current Provider Context is production verified and a current Super Signals provider signal successfully receives current AIDY context.