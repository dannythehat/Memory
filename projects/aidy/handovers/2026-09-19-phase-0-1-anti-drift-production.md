# Handover — AIDY Phase 0/1 Anti-Drift Production

Date: 2026-09-19
Status: PRODUCTION VERIFIED engineering / WAITING for fresh forward rows

## Completed

The immediate Master Gold Intelligence gate (Phase 0/1) is implemented in the Super Signals
signal-level AIDY reasoning path.

Production evidence:

- Super Signals branch: `feature/day-10-shared-telegram-sources`
- deployed SHA: `33305a020f96e545990906a6de0c5dc253e9fcaf`
- Render deploy: `dep-dan2cv5ii2qc73bhmpig`
- Alembic: `0104_aidy_grounding_health`
- API tests: **1105 passed, 137 skipped, 2 warnings**
- web tests: **28 passed**
- secret scan: PASS
- production `/health`: healthy
- origin + website public-performance endpoints: 200 after startup settled
- AIDY live-money authority: OFF
- 1% owner risk directive: unchanged

## Anti-drift contract

New reasoning uses `aidy_reasoning_evidence_v2`.

Provider-history evidence is no longer free text supplied to the model. The model sees atomic,
PIT-safe claims only. Each claim contains exact source path, value, sample N, version and
evidence timestamp.

Side/session evidence is scoped to the current signal's side/session. Missing cohorts do not
become implicit comparisons. Provider identity and raw profile/fingerprint text are withheld
from the model. Provider-history prose in rationale/key factors/action reason is rejected.
Unknown claim references are rejected. Successful rows freeze both the evidence snapshot and
the exact claim refs.

The exact Scalping failure that motivated this work is covered by regression tests: SELL-only
history cannot imply BUY weakness, and London-only history cannot imply Asia preference.

## Legacy audit

At deployment:

- total old annotations: 2674
- legacy_unvalidated: 2674
- stricter-language review candidates: 2227
- new evidence-v2 forward rows: 0
- unsupported evidence-v2 rows: 0

The 2227 legacy candidates are **not** labelled false. They predate the evidence-ref contract
and cannot be retroactively called grounded.

## Forward acceptance

The canonical Gold market is in its weekend closure, so zero fresh evidence-v2 decisions is
expected. Phase 1 remains WAITING for the first fresh eligible market signals.

On the first new rows verify:

1. `evidence_contract_version='aidy_reasoning_evidence_v2'`;
2. `claim_validation_status='passed'`;
3. `unsupported_claim_count=0`;
4. every non-empty `provider_claim_refs` entry exists in the frozen evidence snapshot;
5. no free-form provider-history claim escaped into rationale/key factors/action reason.

Do not advance the programme beyond the Phase 1 acceptance gate until this check is clean.

## Other observations

A recurring Telegram summary-repair error (`message to edit not found`) remains visible in
logs and explicitly reports `trading unchanged`; it is unrelated to this AIDY build and was
not modified.

Standalone AIDY Worker health was checked after this build: status `ok`, session closed,
capture enabled, formal-forward OFF, Twelve Data/public-independent market ownership. The
merged standalone Gold-state source SHA was not independently proven as the deployed Worker
source during this handover, so no deployment claim is made for it.
