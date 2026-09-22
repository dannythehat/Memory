# AIDY Blocker 1 — Aggregation Redesign Pre-Registration (DRAFT v1, 2026-09-22)

**Status: DRAFT — NOT APPROVED, NOT IMPLEMENTED.**
No code has been written. No production, config or holdout has been touched.

This document exists to fix the decision mathematics **before** anyone sees how it changes historical outcomes. Once both reviewers and the owner approve, the constants in Section 4 are **frozen**. Any later change to them must be recorded as a new dated pre-registration with an explicit reason, not edited in place.

Governing rule: **we may inspect input distributions for engineering sanity, but we may not tune any threshold using the 41-cycle outcomes.** Build 23 is re-run only after the constants are frozen.

---

## 1. What is being replaced

Current live behaviour (`gold_environment_gate_selector.py:472`, `gold_meta_direction.py:298`):

    authority_g   = shrunk_accuracy × sample_confidence × scope × calibration × recency × dependency
    directional_total = Σ authority_g   over gates concluding bullish/bearish
    abstain if directional_total < 0.30

Three defects:

1. **Units mismatch.** `dependency` is Build 20's evidence-redundancy *ratio* — "how much of this is new information?" — not a confidence. Multiplying it into a reliability product destroys each expert's reliability instead of governing how much independent evidence exists. Live values: 0.0207-0.2168 per gate.
2. **Absolute threshold on a shrunken sum.** `directional_total` averages **0.004491** live against a required 0.30.
3. **Unbounded, uninterpretable scale.** The sum has no natural range, so no threshold on it can be principled.

### 1.1 Two further defects found while designing this

Both are new to this document and should be fixed in the same change.

**(a) Small samples are penalised twice, multiplicatively.**
`shrunk_accuracy = (correct_n + 0.5 × 20) / (N + 20)` already pulls low-N gates toward the prior. The product then multiplies by `sample_confidence = N / (N + 20)`, which penalises low N *again*. At N=4 the second term alone costs 83%. Sample size must discount reliability **once**, or — as proposed below — act as an eligibility condition rather than a multiplier.

**(b) The shrinkage prior of 0.5 is wrong for this target.**
The outcome is three-class (bullish / bearish / neutral) and gates commit to one of two directions, so 0.5 is not chance. On the live resolved sample the marginal rates are roughly bearish 0.58, bullish 0.29, neutral 0.13. A gate committing bearish is right ~58% of the time by luck; one committing bullish, ~29%. Shrinking both toward 0.5 flatters bullish calls and punishes bearish ones. The prior must be the **PIT marginal rate of the class the gate is committing to**.

This is also why Section 6's baselines are not cosmetic: without them "41.67% accuracy" cannot be read as good or bad.

---

## 2. Design principles (locked)

1. **Reliability, independence and directional balance are separate quantities** and are never multiplied into one another.
   - *Reliability* — how trustworthy has this evidence been, in comparable conditions?
   - *Independence* — how much genuinely new information does it add?
   - *Directional balance* — which way does the trustworthy, independent evidence lean?
2. **Build 20 is retained in full.** Its duplicate elimination, correlation grouping, parent-family graph and evidence identity are the machinery that makes independence computable. Nothing in it is discarded. What changes is only how its output is *consumed*.
3. **The directional measure is normalised** to `[-1, +1]`. Absolute evidence quantity becomes a **separate sufficiency gate**, never mixed into the directional score.
4. **Abstain must remain reachable for principled reasons** — too few independent families, inadequate history, heavy contradiction, or a balance too close to zero — and must never again be produced by a unit artifact.
5. **An ABSTAIN gate never votes.** A gate that says "I don't know" contributes zero directional weight at gate level. Information is recovered *below* it (Section 5.3), not by assigning it a direction.

---

## 3. Proposed mathematics

### Stage A — Gate reliability, `[0, 1]`

    baseline_g   = PIT marginal rate of the outcome class this gate is concluding,
                   computed only from outcomes resolved strictly before as_of
    edge_g       = shrunk_accuracy_g − baseline_g            # skill above chance
    quality_g    = clamp(edge_g / EDGE_SCALE, 0, 1)
    reliability_g = quality_g × scope_mult × calibration_mult × recency_mult

Changes from today: `sample_confidence` is **removed** from the product (defect 1.1a — N now acts in Stage D instead); `dependency` is **removed** from the product (it moves to Stage B, where it belongs); the shrinkage prior becomes `baseline_g` rather than 0.5 (defect 1.1b).

A gate with no edge above its baseline gets `reliability = 0` and is silent. That is correct and intended.

### Stage B — Collapse to independent root families

Build 20 already declares the root graph (`FAMILY_PARENT`):

| root family | children | live status |
|---|---|---|
| `price_action` | structure, momentum, location | **live, directional** |
| `liquidity_mechanism` | liquidity | **live, directional** |
| `volatility_regime` | volatility | live, context-only |
| `participation_flow` | session_participation, futures_microstructure | partly live, context-only |
| `macro_information` | event, rates_usd, cross_market, news_mechanism | UNKNOWN |
| `analogue_memory` | analogue | UNKNOWN |
| `data_quality` | data_quality | never directional |

Each root family contributes **at most one unit of directional evidence**, no matter how many gates or signals sit inside it:

    members_f      = directional, scoreable contributors in family f with reliability > 0
    reliability_f  = weighted consensus reliability of members_f, capped at 1.0
    direction_f    = +1 bullish / −1 bearish / 0 neutral, by reliability-weighted consensus of members_f
    internal_conflict_f = share of member reliability opposing direction_f

This is the actual fix for "five versions of the same Gold move are not five confirmations": M5, M15, H1, H4, momentum and location all live under `price_action` and collapse to **one** vote.

### Stage C — Normalised directional balance, `[-1, +1]`

    S       = Σ_f  reliability_f × direction_f        over directional families
    W       = Σ_f  reliability_f                      over directional families with direction_f ≠ 0
    balance = S / W              (defined only when W > 0)

### Stage D — Evidence sufficiency (separate gate)

Direction is permitted only when **all** hold:

    independent_families_with_direction ≥ MIN_FAMILIES
    every counted family has effective sample_n ≥ MIN_FAMILY_N
    W ≥ MIN_TRUSTWORTHY_WEIGHT
    cross_family_conflict ≤ MAX_CONFLICT

`MIN_FAMILY_N` is where sample size re-enters — **once**, as an eligibility condition rather than a second multiplicative penalty.

### Stage E — Decision

    if not sufficient                    → abstain  (reason names the failed condition)
    elif cross_family_conflict > MAX_CONFLICT → abstain  ("genuine_independent_disagreement")
    elif |balance| < NEUTRAL_BAND        → neutral  ("balanced_independent_evidence")
    else                                 → bullish / bearish by sign of balance

Confidence remains **withheld** until meta-calibration exists. No number is invented.

---

## 4. Pre-registered constants — FREEZE ON APPROVAL

Justified from first principles only. **None is derived from the 41-cycle outcomes.**

| constant | value | justification |
|---|---|---|
| `EDGE_SCALE` | `0.15` | 15 percentage points above baseline is a large, sustained edge for 15-minute FX/metals direction. Treating that as full reliability is deliberately demanding. |
| `MIN_FAMILIES` | `2` | One family cannot corroborate itself. Two is the minimum at which "independent agreement" is meaningful. **See Section 4.1 — this is the most consequential choice in the document.** |
| `MIN_FAMILY_N` | `12` | Matches the existing `mini_exact` minimum already in the trust engine; below ~12 a directional rate is not distinguishable from its baseline. |
| `MIN_TRUSTWORTHY_WEIGHT` | `0.40` | Requires the equivalent of roughly one family at moderate reliability plus corroboration, rather than two near-zero families technically clearing a count. |
| `NEUTRAL_BAND` | `0.20` | Balance within ±0.20 means the trustworthy independent evidence is close to evenly split; calling that a direction is noise-chasing. |
| `MAX_CONFLICT` | `0.45` | Retained unchanged from the current `STRONG_CONTRADICTION_RATIO`, which is a reasonable definition of genuine disagreement and is not implicated in Blocker 1. |

### 4.1 The `MIN_FAMILIES` decision needs an explicit owner ruling

Today only **two** root families are live and directional: `price_action` and `liquidity_mechanism`. `macro_information` and `analogue_memory` are UNKNOWN; `volatility_regime` and `participation_flow` are context-only.

- `MIN_FAMILIES = 2` → AIDY can make a call when price action and liquidity agree, once each shows edge and N ≥ 12. **Direction becomes reachable in the current live configuration.**
- `MIN_FAMILIES = 3` → AIDY is **structurally blocked from ever making a call** until Macro/Event or Analogue is wired. That would be a deliberate, principled abstention, but it recreates a hard block and must be chosen knowingly rather than by accident.

**Recommendation: 2**, with the reachability test asserting that 3 independent families also work. This also sharpens the case for wiring Macro/Event, since it is the cheapest route to a genuinely independent third root.

---

## 5. Abstain semantics

### 5.1 Reachable, principled abstentions
`insufficient_independent_families`, `insufficient_family_history`, `insufficient_trustworthy_weight`, `genuine_independent_disagreement`. Each names the specific failed condition. No abstention may be produced by scale or units.

### 5.2 Never again
No abstention may arise from comparing a shrunken sum to an unrelated absolute constant.

### 5.3 Recovering sub-evidence without letting abstain vote
A gate concluding `abstain` contributes **zero** at gate level. Its individual **scoreable directional sub-calculators** may enter their root family as members in their own right, but only when each independently satisfies:

- it is `role: directional`, `state: known`, and `scoreable`;
- it has its **own** PIT track record as `subject_type = 'subcalculator'` meeting `MIN_FAMILY_N`;
- it shows `reliability > 0` by Stage A on its own history.

The infrastructure already exists — 3,742 sub-calculator snapshots are being recorded and scored. This recovers "the gate is unsure overall, but these two sub-calculators have historically been valuable" **without** assigning a direction to an expert that explicitly declined to give one.

---

## 6. Coverage must be visible (reporting change, not a trust change)

An expert that is 75% correct on 4 opportunities and abstains everywhere else must not read as better than one that is 58% correct across 200 varied decisions.

Every scorecard row gains:

    coverage_g            = committed_cycles_g / eligible_cycles_g
    accuracy_on_commit_g  = existing accuracy, explicitly relabelled as conditional on committing
    baseline_g            = PIT marginal rate of the committed class
    edge_g                = accuracy_on_commit_g − baseline_g

plus the three required baselines on every scorecard: **majority-class, persistence, and uniform-random**.

**In v1 coverage is reported, not weighted into trust.** Changing selection on coverage is a separate decision with its own failure modes and should be pre-registered separately once there is enough history to see the distribution. Recording it now means the data exists when we want it.

---

## 7. Acceptance tests — must fail before, pass after

**T1 — Reachability (the test whose absence caused Blocker 1).**
Construct the production-realistic graph: 15 gates, ~91 signals, the real `FAMILY_PARENT` topology, plausible mature trust values. Assert that **all four** outcomes — bullish, bearish, neutral, abstain — are reachable under intentionally constructed conditions. **This test must fail against current `main` and pass after the change.** If it does not fail first, it is not testing what we think.

**T2 — Redundancy.** Six agreeing `price_action` gates must not outvote one `price_action` plus one `liquidity_mechanism`. Directly encodes "five versions of one move are not five confirmations."

**T3 — Abstain never votes.** A gate concluding `abstain` contributes exactly zero at gate level, with and without qualifying sub-calculators.

**T4 — Principled abstention.** Each Section 5.1 reason is independently reachable and correctly named.

**T5 — Bounds.** `balance ∈ [-1, +1]` always; `W = 0` never divides.

**T6 — PIT.** `baseline_g`, `reliability_g` and every calibration input use only evidence resolved strictly before `as_of`. Existing hindsight guards extended to the new fields.

**T7 — No-edge silence.** A gate at or below its baseline contributes zero.

---

## 8. Gate calibration producer (may follow immediately)

Build the producer from already-resolved gate history with strict `observed_at < decision_as_of`, feeding the existing, already-tested Build 21 consumer.

**Explicitly not a guaranteed improvement.** The current `unknown` state applies 0.85. Real calibration returns 1.00, 0.90, 0.80, 0.75 **or 0.50** depending on N and error. Wiring it may lower some gates. That is the correct outcome: we wire it and accept what the evidence says.

**Meta calibration is deferred.** It requires resolved directional meta predictions, which cannot exist until this change lands and enough cycles resolve. Attempting it now would produce a second empty producer. Revisit after the soak in Section 10.

---

## 9. Explicitly NOT in scope

Multi-horizon targets; magnitude or probability-distribution prediction; MAE/MFE excursion; volatility-normalised outcome labels; coverage-weighted trust; any new data vendor; Databento. Each may be worth doing later; none may be bundled into a change whose purpose is to make the decision layer coherent. **One change, one question.**

---

## 10. Falsification — what would make us reject this design

Stated in advance so the result cannot be rationalised afterwards:

1. **T1 does not fail against current `main`** → the test is wrong, not the code. Stop and fix the test.
2. **Direction remains unreachable after the change** under any plausible mature trust configuration → the redesign failed; do not relax constants to rescue it. Return here and re-derive.
3. **Every cycle becomes directional** (abstention rate near zero on replay) → sufficiency is too weak; the design is over-corrected and equally wrong.
4. **Build 23 validation shows no improvement over the legacy view** once direction is reachable → the aggregation is coherent but the experts carry no usable information. That is a real and acceptable finding, and it is the question we actually want answered.
5. **Any constant requires adjustment after seeing outcomes** → record a new dated pre-registration with the reason. Never silently retune.

## 11. Sequence after approval

1. Freeze constants. 2. Write T1-T7; confirm T1 fails on current `main`. 3. Implement Stages A-E. 4. All tests green plus full regression. 5. Gate calibration producer (Section 8). 6. Environment cardinality fix. 7. PIT-safe H4/D1 rebuild from M1 lineage. 8. Maintenance-window bug. 9. Watchdog, append-only health history, scorecard baselines. 10. Re-run Build 23 honestly. 11. **Soak unchanged across multiple regimes.** 12. Only then judge whether the experts contain useful Gold information.

## 12. Open questions for the owner

1. **`MIN_FAMILIES` = 2 or 3?** (Section 4.1 — the consequential one.)
2. Do you accept `EDGE_SCALE = 0.15`, or prefer a gentler `0.10`? This directly controls how quickly a modest edge earns authority.
3. Confirm coverage is **reported only** in v1, not weighted into trust.
4. Confirm gate calibration proceeds immediately after this change, accepting it may reduce some gates.
