# Handover — AIDY Master Gold Intelligence Build

Date: 2026-09-19
Status: APPROVED BUILD PLAN / NOT YET IMPLEMENTED

## Why this handover exists

The owner and ChatGPT reached a clear architecture agreement for the next AIDY phase. AIDY is to become a full Gold specialist that understands the market independently, uses provider signals as one source of human alpha, explains supported causes of Gold moves and trade failures, understands liquidity/execution, learns provider conditional strengths, optimises profit extraction, compares historical regimes, and continuously measures whether its own decisions improve outcomes.

Do not interpret this handover as claiming the new features are built. The detailed plan is in `projects/aidy/MASTER_GOLD_INTELLIGENCE_BUILD.md`.

## Evidence that drove the plan

- Live Super Signals AIDY reasoning is genuinely using provider profiles and market context.
- The final-gate sample is still small and has not yet proven a durable edge.
- A reasoning audit found at least one unsupported provider-history claim in a Scalping rationale: the model said BUY was weaker / Asia preferred even though the exact PIT profile lacked those facts.
- This establishes the first build priority: evidence-addressable claims before adding more intelligence.
- Existing standalone Aidy-Gold-Signals already contains substantial research machinery for rates, real yields, macro events, volatility, cross-asset context, analogues and research governance. Reuse it; do not rebuild parallel versions in Super Signals.
- Current Super Signals reasoning has scheduled calendar support but no verified breaking-headline/news intelligence client feeding the final decision layer.

## Frozen build sequence

0. Freeze cross-repo evidence contracts.
1. Enforce evidence-grounded claims and unsupported-claim rejection.
2. Build the bounded PIT-safe bridge for qualified Gold-state evidence.
3. Add breaking-news/event intelligence and mechanism classification.
4. Add liquidity/execution intelligence.
5. Deepen conditional provider alpha decomposition.
6. Reuse/qualify historical analogue and setup memory.
7. Add calibrated probability/expected-value outputs and abstention.
8. Build trade-management/profit-extraction counterfactuals.
9. Build failure-attribution and UNKNOWN engine.
10. Run continuous feature ablation/self-critique and remove non-incremental complexity.

## Test doctrine

- No hindsight leakage.
- No unsupported provider claims.
- Exact PIT profile/context reconstruction.
- Chronological holdout and forward-only evaluation.
- Counterfactual decision delta is the primary intervention metric.
- Probability calibration must be measured, never assumed.
- News/liquidity/analogue features must prove incremental forward value via ablation.
- UNKNOWN and NO-TRADE are valid successful outputs.
- No live authority during this build.

## Immediate next engineering step

Start Phase 0 and Phase 1 in Super Signals/AIDY integration:

1. define a versioned structured claim/evidence schema;
2. persist claim references with each reasoning annotation;
3. make unsupported provider-specific claims a hard validation failure / safe fallback;
4. add regression fixtures from the observed Scalping rationale failure;
5. replay existing final-gate annotations to quantify unsupported legacy claims;
6. deploy shadow-only and verify new forward rows have zero unsupported claims;
7. only then begin the Gold-state bridge and news/liquidity expansion.

## Safety

- AIDY live-money authority remains OFF.
- Existing 1% Super Signals risk directive remains unchanged.
- Aidy-Gold-Signals remains broker-isolated.
- Super Signals remains the execution system.
- Do not merge the two repos or make broker state market truth.
