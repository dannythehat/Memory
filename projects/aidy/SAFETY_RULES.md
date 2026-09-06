# AIDY — Safety Rules

These are operating constraints, not suggestions.

## Authority

- Formal-forward must remain OFF unless the owner explicitly authorizes graduation and the evidence supports it.
- Research/shadow output must not gain broker or member execution authority by accident.
- AIDY may provide market/context evidence to Super Signals through explicit bounded interfaces, but it does not own the Super Signals real-money execution path.

## Evidence

- No hindsight leakage into forward evaluation.
- Every claim about freshness, continuity, deployment or statistical quality must be evidenced.
- Closed-market minutes must not be misclassified as missing data.
- A failing archive item must not be allowed to stop market capture.
- A stale/failed capture path must fail visibly rather than look healthy.

## Production changes

- Keep rollback evidence for production-affecting AIDY changes.
- Avoid auth/token rotation immediately before market open unless that exact change is explicitly authorized.
- Secret material must never be committed or printed.
- Do not use expensive D1 full scans when bounded/indexed queries can answer the question.
- Preserve free-tier constraints unless the owner explicitly approves paid infrastructure.

## Cross-project boundary

- Do not import Super Signals broker/follower state into AIDY as market truth.
- Do not treat Super Signals provider performance as AIDY market evidence.
- Do not silently change Super Signals production while completing an AIDY build.

## Graduation language

Use `BUILT`, `ENGINEERING PROVEN`, `PRODUCTION VERIFIED`, `STATISTICALLY VALIDATED`, `WAITING`, and `RED` precisely as defined in root `AGENTS.md`.
