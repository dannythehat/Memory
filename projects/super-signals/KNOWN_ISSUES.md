# Super Signals — Known Issues / Deferred Work

Verify every item against current production before acting.

## Current/deferred from the latest provider audit

1. **Discovery interpretation completeness** — the owner observed some shadow groups visibly posting more executable signals than Provider Lab was recording/evaluating. Adaptive provider grammar/replay work has improved the path, but completeness should continue to be measured rather than assumed.
2. **Non-AIDY fair-score eligibility** — mixed/unknown research styles must not gain fair scores from non-canonical market evidence where AIDY evidence is required. Verify whether this has since been fixed before changing it.
3. **Provider-market bearer credential rotation/history cleanup** — must be synchronized with AIDY in a controlled production window. Never expose the credential.
4. **Render configuration drift** — a prior audit found `render.yaml` auto-deploy configuration differed from the live Render setting. Re-check before remediation.
5. **Production branch vs default branch** — source repo `main` is not automatically the live production branch; always resolve the actual Render commit.

## Historical operational risk areas

These have had incidents in the past and therefore deserve regression protection even when currently fixed:

- edited Telegram posts causing duplicates;
- missed management instructions (SL-to-entry, take-loss, cancellation/removal);
- trades placed then closed incorrectly;
- notification delays/freezes;
- balance/equity/UI persistence and stale PWA/session behaviour.

Do not report any historical item as currently broken without fresh evidence.
