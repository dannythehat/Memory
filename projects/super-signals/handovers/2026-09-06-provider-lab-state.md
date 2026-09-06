# Super Signals Handover — Provider Lab State — 2026-09-06

## Production snapshot

Source repo: `dannythehat/super-signals`
Known production branch: `feature/day-10-shared-telegram-sources`
Last known live SHA: `9a0080acc06ebc8783ec0b5f44405ee01303fa27`
Render service at last verification: `super-signals-day-8`

Re-verify these before production work.

## Provider populations

- 40 shadow discovery providers — research only, broker-isolated.
- 5 testing providers — current real execution population with broker-deal history.
- 14 paused.
- 4 revoked.

Do not mix these populations in analysis or reporting.

## Recent Provider Lab production work

- PR #133 — adaptive provider intelligence on production branch.
- PR #135 — deterministic AIDY Provider Lab replay engine.
- PR #136 — app-owned AIDY resolver startup.
- PR #137 — removed duplicate broker-owned resolver start.
- PR #138 — production batch outcome logging.

## Why this matters

Provider Lab is being turned from a simple signal counter into a provider-aware research system that can learn how different groups communicate and trade, while AIDY supplies independent point-in-time market truth for fair replay.

## Safety boundary

None of this gives shadow discovery providers broker authority. Research/profile/replay failure must not disrupt live broker execution.

## Current next relationship to AIDY

Finish AIDY Day 6 hardening, then continue the intelligence roadmap: provider identity/style, forward-only context, conditional fingerprints, correlation/drift and AIDY veto/filter research.
