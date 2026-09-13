# Super Signals — Roadmap

Current roadmap verified against production/source state on **2026-09-13**.

## Strategic destination

AIDY is not intended to remain a Telegram parser or provider-ranking system. Providers are valuable training/evidence inputs, but the destination is an **independent Gold/XAUUSD trading intelligence system** that can:

1. understand what Gold is doing now and why;
2. form its own directional/market thesis;
3. identify its own setups, entries, invalidation and targets;
4. judge provider trades rather than merely copy them;
5. agree or disagree with providers using market evidence;
6. propose and manage its own paper/shadow trades;
7. graduate toward any additional live authority only after forward validation and explicit owner approval.

The current 1% live-risk directive and existing execution authority remain unchanged by this roadmap.

## Provider Intelligence A-F

### A — capture/calendar foundation — COMPLETE / VERIFIED FOUNDATION
Continuous provider capture, PIT boundaries, context attachment and evidence hygiene.

### B — market-context join — PRODUCTION VERIFIED
Join provider activity to contemporaneous Gold session/regime/context without hindsight leakage.

### C — provider fingerprints — PRODUCTION VERIFIED
Model provider communication/trading fingerprints: grammar, cadence, entry/order/management style, vocabulary, edits, sequence and drift.

### D — automatic research governance — PRODUCTION VERIFIED
Flag learning/healthy/watch/quarantine-candidate states in research only. No automatic live-source mutation.

### E — provider-specific adaptation — PRODUCTION VERIFIED
Interpret each provider using its own profile/history while prohibiting historical numeric levels as current execution evidence.

### F — combined-book intelligence — PRODUCTION VERIFIED
Observe provider BUY/SELL consensus and conflicts. Broker-level automatic netting remains disabled.

**Important:** engineering completion is not statistical validation. Promotion/profitability conclusions remain `WAITING-FOR-FORWARD-EVIDENCE` until enough genuine forward evidence exists.

## Next — AIDY Data Hub

Build an owner/admin daily control centre that is cheap and database-backed.

### Daily overview
- AIDY status: frozen / learning / active.
- Providers monitored and provider coverage.
- Signals captured, accepted/understood, rejected, ambiguous and missed where measurable.
- Context-attachment coverage.
- Forward/shadow trades scored.
- Provider health: healthy / watch / quarantine candidate.
- Current provider BUY/SELL consensus and conflicts.
- System-health and owner-attention alerts.
- Clear distinction between raw activity, scored evidence and statistically sufficient evidence.

### AIDY market view
As the underlying intelligence becomes available, expose:
- current Gold bias/thesis;
- market regime/session;
- important levels and candidate setups;
- confidence;
- what AIDY is watching;
- invalidation conditions;
- eventually AIDY's own proposed trades and management plan.

### Provider detail
Each provider should be clickable into:
- AIDY's provider fingerprint;
- communication/grammar profile;
- interpretation confidence/read quality;
- context coverage;
- forward performance and W/L/P&L where valid;
- session/regime performance where valid;
- drift/warnings/governance history;
- recent activity/current directional state;
- explanation of why AIDY interpreted a message a certain way.

### Data Hub efficiency rule
The Hub reads PostgreSQL/current snapshot views. A browser refresh must **not** itself invoke OpenAI or MetaAPI.

## After Data Hub — AIDY independent trader progression

### Phase 1 — Gold-state comprehension
Make AIDY continuously characterize trend, momentum, volatility, session structure, liquidity behaviour, reactions/rejections, continuation/reversal conditions and relevant macro/news context using PIT-safe evidence.

### Phase 2 — own thesis engine
AIDY produces its own market bias, confidence, invalidation and alternative scenario even when no provider posts.

### Phase 3 — setup generation
AIDY identifies candidate entries, SL/invalidation, targets and management logic from its own Gold thesis. Initially research/paper only.

### Phase 4 — provider adjudication
Compare provider signals with AIDY's own thesis: support, neutral, reject/veto candidate, or conflict. Measure counterfactual outcomes instead of assuming AIDY is right.

### Phase 5 — AIDY paper/shadow trading
Run AIDY-generated setups through forward paper/shadow evaluation with execution-cost calibration, no hindsight and immutable evidence.

### Phase 6 — management intelligence
Evaluate AIDY's own management choices: hold, BE, partials, trailing/invalidation and exit timing, with clear counterfactual comparison.

### Phase 7 — graduation gate
Only statistically validated forward evidence plus explicit owner approval can grant any new live-money authority. No roadmap item silently changes the existing broker/risk policy.

## Runtime/efficiency cleanup still required

- Remove stale historical error rows from the fast settlement loop while preserving audit evidence.
- Skip broker positions/orders reads when no protection plan exists.
- Remove redundant MetaAPI Gold-price reads from dashboard broker state.
- Add OpenAI token/cost and MetaAPI request telemetry.
- Close the possible weekend-edited-message replay edge.
