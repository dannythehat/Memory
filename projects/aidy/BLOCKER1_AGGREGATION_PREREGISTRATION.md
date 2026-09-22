# AIDY Blocker 1 — Aggregation Redesign Pre-Registration (DRAFT v3, 2026-09-22)

**Status: DRAFT v3 — awaiting final approval. NOT IMPLEMENTED. No code written.**
No production, config or holdout touched.

v1 (`a8b78fe`) and v2 (`8029712`) are preserved immutably in git. This revision applies the seven changes required by independent review, and records **one further redundancy found by applying the reviewer's own method** (§5.1).

Governing rule, unchanged: input distributions may be inspected for engineering sanity, but **no threshold may be tuned using the 41-cycle outcomes.** Build 23 is re-run only after constants are frozen.

---

## 0. Revision history

| version | change |
|---|---|
| v1 (`a8b78fe`) | Separate reliability / independence / balance; normalised balance; separate sufficiency gate. |
| v2 (`8029712`) | Direction-aware PIT excess skill; exact family mathematics; internal-family conflict; `MIN_FAMILY_STRENGTH`; tightened T1; withdrew `MAX_CONFLICT` as unreachable. |
| **v3 (this)** | Explicit qualifying-contributor definition (§3.2). Corrected the weak-family rationale — the previous "changes nothing" claim was **false** (§3.5.1). Locked strong-opposing-families abstain (§5.2). Removed `insufficient_trustworthy_weight` as an independent condition; retained `W ≥ 0.40` as a derived invariant (§4, §5.1). Replaced the `BASE_MIN_N` cliff with continuous symmetric Dirichlet smoothing (§3.1). Dedicated root-family tables instead of forcing `root_family` into gate-centric tables (§8). Tests for all three redundancies and for weak-family bounds (§7). |

---

## 1. What is being replaced

    authority_g        = shrunk_accuracy × sample_confidence × scope × calibration × recency × dependency
    directional_total  = Σ authority_g   over gates concluding bullish/bearish
    abstain if directional_total < 0.30

1. **Units mismatch.** `dependency` is Build 20's evidence-redundancy *ratio* — "how much of this is new information?" — not a confidence. Multiplying it into a reliability product destroys each expert's reliability instead of governing how much independent evidence exists. Live values 0.0207–0.2168 per gate.
2. **Absolute threshold on a shrunken sum.** Live `directional_total` averages **0.004491** against a required 0.30.
3. **Unbounded, uninterpretable scale.** No natural range, so no threshold on it can be principled.

### 1.1 Two further defects found while designing the replacement

**(a) Sample size discounts reliability twice — precise wording.**
Shrinkage plus a separate uncertainty term is **not inherently invalid**; they can represent different concepts. The defensible finding is narrower: **in the current authority product, combined with the absolute 0.30 threshold, the combination is catastrophically suppressive** (at N=4, `sample_confidence` alone costs 83%). In the replacement, `sample_confidence` leaves directional strength and N becomes an eligibility mechanism.

**(b) The 0.5 shrinkage prior is wrong for this target, and the class marginal alone does not fix it.**
The outcome is three-class and gates commit to one of two directions, so 0.5 is not chance (live marginals ≈ 0.58 bearish / 0.29 bullish / 0.13 neutral — a bearish commitment is right ~58% of the time by luck, a bullish one ~29%). This flatters bullish calls and punishes bearish ones, and may compound H4's never-bearish behaviour on top of its data starvation.

But existing trust history **blends each gate's bullish and bearish commitments into one accuracy**, so comparing that blend against one of today's class rates compares unlike quantities. §3.1 measures skill per commitment instead.

---

## 2. Design principles (locked)

1. Reliability, independence and directional balance are **separate quantities**, never multiplied into one another.
2. **Build 20 is retained in full.** Only its consumption changes: it now sets relative contribution *inside* a root family.
3. The directional measure is **normalised** to `[-1, +1]`; evidence quantity is a **separate sufficiency gate**.
4. Abstain stays reachable for **principled** reasons and must never again be produced by a unit artifact.
5. **An ABSTAIN gate never votes.** Zero weight at gate level; information recovered only beneath it (§5.3).

| question | answered by |
|---|---|
| Has this evidence historically beaten chance? | `rᵢ` (§3.1) |
| How is evidence de-duplicated inside a mechanism? | Build 20 weights → `pᵢ` (§3.3) |
| Do members of a mechanism agree internally? | `family_balance_f` (§3.3) |
| Do independent mechanisms corroborate each other? | `MIN_FAMILIES`, `MIN_FAMILY_STRENGTH` (§3.5) |
| Which way does it lean? | `meta_balance` (§3.5) |

---

## 3. Proposed mathematics

### 3.1 Stage A — Direction-aware, PIT-aware excess skill

**Baseline estimator — continuous from observation one.** For class `c ∈ {bullish, bearish, neutral}` at time `T`:

    resolved(T)     = outcomes with resolved_at_utc < T                    # strict, PIT
    baseline(c, T)  = (count_c(T) + BASELINE_PRIOR_PER_CLASS)
                      / (count_total(T) + BASELINE_PRIOR_STRENGTH)

with `BASELINE_PRIOR_PER_CLASS = 10` and `BASELINE_PRIOR_STRENGTH = 30` (a symmetric Dirichlet prior equal to 30 pseudo-outcomes, 10 per class).

- At zero history: `10/30 = 1/3` exactly, for all classes.
- The observed marginal takes control smoothly as N grows. **There is no hard switch and no discontinuity.**
- Window: **global and expanding**, strictly `resolved_at < historical decision T`.

This replaces v2's `ALPHA = 1` plus `BASE_MIN_N = 30` fallback, which created an artificial cliff: with 29 heavily bearish outcomes the bearish baseline would read 0.333, then jump toward 0.60+ at outcome 30, though nothing happened in the market at that boundary — the estimator simply changed rules. Verified continuity: N=29 → 0.5932, N=30 → 0.6000.

The prior is deliberately strong early (N=10, count=8 → 0.450 rather than 0.800) and decays slowly (N=1000, count=580 → 0.573 vs observed 0.580). This is conservative by intent and is **not** outcome-tuned.

**Deferred:** a rolling or environment-conditional baseline is a known improvement but belongs with Blocker 2. A conditional baseline cannot be estimated honestly while environment conditioning does not function.

**Excess skill per commitment.** For each historical directional commitment `j` by contributor `i`:

    excess_j = correct_j − baseline(predicted_class_j, decision_time_j)      ∈ (−1, +1)

`correct_j ∈ {0,1}`. The ±2/±1 net score is **not** used here; it stays a separately reported quantity. This measures only "did it beat chance", which is what reliability should mean.

**Shrink the mean excess toward zero edge:**

    shrunk_excess_i = ( Σ_j excess_j ) / ( N_i + PRIOR_STRENGTH )        PRIOR_STRENGTH = 20

Equivalent to 20 pseudo-observations of zero edge; reuses the existing `TRUST_PRIOR_STRENGTH`.

    quality_i     = clamp( shrunk_excess_i / EDGE_SCALE, 0, 1 )
    reliability_i = quality_i × scope_mult × calibration_mult × recency_mult      ∈ [0, 1]

`sample_confidence` and `dependency` are both **removed** from this product. A contributor at or below its PIT baseline gets `reliability = 0` and is silent — intended.

### 3.2 Qualifying contributor — explicit definition

A contributor `i` **qualifies** for family `f` if and only if **all** hold:

    state            == known
    role             == directional
    scoreable        == true
    N_i              ≥ MIN_CONTRIBUTOR_N          (own PIT record, never summed across members)
    reliability_i    > 0                          (§3.1)
    current vote     ∈ { bullish, bearish, neutral }

**Excluded entirely** — consuming no family weight: `abstain`, `unknown`, `context_only`, and any contributor with `reliability_i = 0`.

A historically reliable contributor voting **neutral does qualify** and **does consume family weight** while adding neither bull nor bear mass. This is deliberate: if five trustworthy components see nothing directional and one sees bullish, the family must not behave like a pure bullish mechanism.

**Implementation note.** A contributor voting neutral today is unscoreable for *this* cycle (correctly — neutral is not a directional commitment), so `N_i` and `reliability_i` derive solely from its past bullish/bearish commitments. Reliability is a property of the contributor's track record, not of today's vote.

**The ABSTAIN boundary is preserved:** an abstaining contributor consumes nothing at all.

### 3.3 Stage B — Exact family aggregation

For qualifying contributor `i` in root family `f`, with PIT reliability `rᵢ` and Build-20 effective dependency weight `uᵢ`:

    pᵢ = uᵢ / Σ_{k qualifying in f} u_k                # Σpᵢ = 1 over ALL qualifying contributors,
                                                        # including those voting neutral

    bull_mass_f = Σ pᵢ rᵢ   over bullish contributors
    bear_mass_f = Σ pᵢ rᵢ   over bearish contributors

    family_reliability_f = bull_mass_f + bear_mass_f                           ∈ [0, 1]
    family_balance_f     = (bull_mass_f − bear_mass_f) / family_reliability_f  ∈ [−1, +1]
    family_strength_f    = family_reliability_f × |family_balance_f|

Because `Σpᵢ = 1` and `rᵢ ≤ 1`, six correlated `price_action` contributors **cannot** create six units of authority. Internally contradictory families weaken themselves automatically.

**Verified identity:** `family_strength_f ≡ |bull_mass_f − bear_mass_f|`, and `sign_f × family_strength_f ≡ bull_mass_f − bear_mass_f`. Implementation is therefore trivial and the formula is provably bounded.

`family_direction_f = sign(family_balance_f)`, treated as neutral when `|family_balance_f| < FAMILY_NEUTRAL_BAND`.

### 3.4 Root family graph (existing, unchanged)

| root family | children | live status |
|---|---|---|
| `price_action` | structure, momentum, location | **live, directional** |
| `liquidity_mechanism` | liquidity | **live, directional** |
| `volatility_regime` | volatility | live, context-only |
| `participation_flow` | session_participation, futures_microstructure | partly live, context-only |
| `macro_information` | event, rates_usd, cross_market, news_mechanism | UNKNOWN |
| `analogue_memory` | analogue | UNKNOWN |
| `data_quality` | data_quality | never directional |

### 3.5 Stage C/D — Meta balance and sufficiency

    S            = Σ_f  sign_f × family_strength_f      ( ≡ Σ_f (bull_mass_f − bear_mass_f) )
    W            = Σ_f  family_strength_f
    meta_balance = S / W                                 ∈ [−1, +1],  defined only when W > 0

Sums run over **every** family with `family_strength_f > 0`.

Direction is permitted only when **both** hold:

    count of families with family_strength_f ≥ MIN_FAMILY_STRENGTH  ≥  MIN_FAMILIES
    not genuine independent disagreement (§5.2)

**Derived invariant (not a decision condition):** two qualifying families at ≥ 0.20 force `W ≥ 0.40`. This is asserted in code for auditability but is **not** an independent gate — see §5.1.

#### 3.5.1 Sub-threshold families — corrected rationale

Families below `MIN_FAMILY_STRENGTH` **do** contribute to `S` and `W`; they simply cannot satisfy the independent-family requirement.

**The v2 justification was false** and is withdrawn. v2 claimed an agreeing weak family "adds equally to `S` and `W` and changes nothing". That holds only when `|meta_balance|` is already 1.0. Counterexample: `S = 0.30, W = 0.60 → balance 0.500`; adding an agreeing family of strength 0.05 gives `S = 0.35, W = 0.65 → balance 0.538`. It **does** strengthen the balance whenever disagreement already exists.

**Correct statement:** *sub-threshold families may influence the balance proportionally to their strength, but they cannot satisfy the independent-family sufficiency requirement.* That is weighted weak evidence behaving exactly as weighted evidence should, bounded by its actual strength. Discarding it would mean discarding legitimate contrary evidence, which is how a system manufactures confidence. Tests T9 and T10 bound this behaviour.

### 3.6 Stage E — Decision

    if W == 0                                  → abstain  ("no_directional_evidence")
    elif qualifying_family_count < MIN_FAMILIES → abstain  ("insufficient_independent_families")
    elif genuine_independent_disagreement       → abstain  ("genuine_independent_disagreement")
    elif |meta_balance| < NEUTRAL_BAND          → neutral  ("balanced_independent_evidence")
    else                                        → bullish / bearish by sign(meta_balance)

Confidence remains **withheld** until meta-calibration exists. No number is invented.

---

## 4. Pre-registered constants — FREEZE ON APPROVAL OF v3

| constant | value | status |
|---|---|---|
| `EDGE_SCALE` | `0.15` | **LOCKED** — 15pp over the PIT baseline (not raw accuracy) as full reliability. Deliberately demanding. |
| `MIN_FAMILIES` | `2` | **LOCKED** — one mechanism cannot corroborate itself; 3 would recreate a structural lock while only two roots are directional. |
| `MIN_FAMILY_STRENGTH` | `0.20` | **LOCKED** — a family counts only if it independently carries meaningful evidence. |
| `MIN_CONTRIBUTOR_N` | `12` | **LOCKED** — conservative **engineering eligibility floor**, matching the existing `mini_exact` minimum. Explicitly **not** a statistical-distinguishability claim. Never summed across correlated members. |
| `NEUTRAL_BAND` | `0.20` | **LOCKED** |
| `FAMILY_NEUTRAL_BAND` | `0.20` | **LOCKED** — matches the meta band so interpretation stays straightforward. |
| `PRIOR_STRENGTH` | `20` | reused (`TRUST_PRIOR_STRENGTH`) — shrinks mean excess toward zero edge. |
| `BASELINE_PRIOR_PER_CLASS` | `10` | **NEW (v3)** — symmetric Dirichlet, continuous from observation one. |
| `BASELINE_PRIOR_STRENGTH` | `30` | **NEW (v3)** — `= 3 × 10`; gives exactly 1/3 at zero history. |
| `W ≥ 0.40` | derived | **invariant/assertion only**, `= 2 × MIN_FAMILY_STRENGTH`. Not a decision condition. |
| ~~`MAX_CONFLICT`~~ | — | **WITHDRAWN (v2)** — unreachable; see §5.2. |
| ~~`MIN_TRUSTWORTHY_WEIGHT`~~ | — | **WITHDRAWN (v3)** — unreachable as an independent condition; see §5.1. |
| ~~`ALPHA`, `BASE_MIN_N`~~ | — | **WITHDRAWN (v3)** — created a baseline cliff; replaced above. |

---

## 5. Abstain semantics

### 5.1 Three redundancies found and removed

All three were conditions that could never independently fail. Each was found by formalising the mathematics rather than by testing, which is precisely why this pre-registration exists.

| condition | why unreachable | resolution |
|---|---|---|
| `MAX_CONFLICT = 0.45` | Cross-family conflict derives to `(1 − \|meta_balance\|)/2`, so `conflict ≥ 0.45` ⟺ `\|meta_balance\| ≤ 0.10`, already captured by `NEUTRAL_BAND = 0.20`. | Withdrawn; redefined structurally in §5.2. |
| `MIN_TRUSTWORTHY_WEIGHT = 0.40` | Two families at ≥ 0.20 force `W ≥ 0.40` since all strengths are non-negative. Cannot fail once the family count succeeds. | Withdrawn as a decision condition; retained as a derived invariant. |
| `insufficient_contributor_history` | `MIN_CONTRIBUTOR_N` is applied at **qualification** — a contributor below it never enters the `pᵢ` denominator. A family of only such contributors has `family_strength = 0` and already fails the family count. | Withdrawn as a distinct reason; reported as **diagnostic detail** under `insufficient_independent_families`. |

**The five remaining outcomes are each independently reachable** and are all asserted by T4:
`no_directional_evidence`, `insufficient_independent_families`, `genuine_independent_disagreement`, `neutral`, `bullish`/`bearish`.

Explainability is preserved by attaching a structured diagnostic payload to every abstention naming the precise cause — `families_below_strength`, `contributors_below_n`, `no_qualifying_contributors` — rather than by inventing decision reasons that can never fire.

### 5.2 Genuine independent disagreement (locked)

    genuine_independent_disagreement  ⟺
        at least one family with family_strength_f ≥ MIN_FAMILY_STRENGTH on EACH side

Both mechanisms must be individually strong, which is materially different from "balance near zero". The distinction is the point of the architecture:

- **neutral** = the trustworthy evidence indicates no directional move.
- **abstain (disagreement)** = two strong independent mechanisms actively contradict, so we do not know.

With the two currently directional roots this gives exactly the intended conservatism:

| price_action | liquidity_mechanism | result |
|---|---|---|
| strong bullish | strong bullish | potentially **bullish** |
| strong bearish | strong bearish | potentially **bearish** |
| strong bullish | strong bearish | **abstain** |

This may prove over-conservative once Macro/Analogue supply three or four independent mechanisms. **If so, a new rule is pre-registered then.** It is not weakened now on the strength of hypothetical future data.

### 5.3 Recovering sub-evidence without letting abstain vote

A gate concluding `abstain` contributes **exactly zero** at gate level. Its individual scoreable directional sub-calculators may enter their root family as contributors in their own right, but only where each independently satisfies the full §3.2 qualification test on its **own** PIT record.

Infrastructure exists: **3,742 sub-calculator snapshots** are already recorded and scored. Because conflicting sub-evidence now *reduces* `family_balance_f`, this recovers "the gate is unsure overall, but these sub-calculators have historically been valuable" **without** hiding disagreement and **without** assigning a direction to an expert that declined to give one.

---

## 6. Coverage must be visible (reporting only in v1 — LOCKED)

Every scorecard row gains `coverage_i`, `accuracy_on_commit_i` (explicitly relabelled as conditional on committing), `baseline_i`, `edge_i` and `shrunk_excess_i`, plus **majority-class, persistence and uniform-random baselines on every scorecard**. Displayed prominently; **not weighted into trust**. Coverage-weighted selection is a separate decision needing real distribution first, and gets its own pre-registration.

---

## 7. Acceptance tests

**T1 — Production-realistic reachability.** All **15** gates with real identities; the real **~91-signal** topology and real `FAMILY_PARENT` relationships; **pre-registered plausible mature reliability ranges** fixed in this document; the real Build-20 dependency engine, not a stub. Must demonstrate that **the current architecture fails** under these realistic conditions and the replacement succeeds, with all five §3.6 outcomes reachable. **T1 must fail against current `main`.** If it passes before the fix, the test is wrong — stop and fix the test. Build 22's existing synthetic tests prove only what we already knew and do not satisfy T1.

**T2 — Redundancy.** Six agreeing `price_action` contributors must not outvote one `price_action` plus one `liquidity_mechanism`.
**T3 — Abstain never votes.** Gate-level `abstain` contributes exactly zero, with and without qualifying sub-calculators.
**T4 — All five outcomes reachable** and correctly named, including `genuine_independent_disagreement` per §5.2.
**T5 — Bounds.** `rᵢ, pᵢ, family_reliability ∈ [0,1]`; `family_balance, meta_balance ∈ [−1,+1]`; `Σpᵢ = 1` over qualifying contributors; `W = 0` never divides.
**T6 — PIT.** `baseline`, `excess_j`, `reliability` and all calibration inputs use only evidence resolved strictly before `as_of`; hindsight guards extended to the new field names and to the names the audit found missing (`realised_direction`, `realised_return_bps`, `return_bps`, `score`, `correct`, `impact_class`).
**T7 — No-edge silence.** A contributor at or below its PIT baseline contributes zero.
**T8 — Baseline continuity.** Assert the estimator is continuous across **every** N with no rule switch; specifically that nothing discontinuous occurs at N=29→30, and that N=0 yields exactly 1/3.
**T9 — Weak families cannot manufacture corroboration.** Ten weak contributors inside one root family must not satisfy `MIN_FAMILIES`; corroboration requires genuinely distinct roots.
**T10 — Weak-family influence is bounded.** A sub-threshold family may move `meta_balance` only within the bound implied by its own `family_strength`, and can never by itself carry a decision.
**T11 — Removed conditions stay removed.** Assert no code path can abstain for `insufficient_trustworthy_weight`, `insufficient_contributor_history` or a `MAX_CONFLICT` test, and that `W ≥ 0.40` holds as an invariant whenever the family count is satisfied.
**T12 — Neutral contributors consume weight.** One bullish plus five reliable neutral contributors in a family must yield materially lower `family_strength` than one bullish alone.

---

## 8. Root families become first-class scored subjects — dedicated tables

Adopted, with the reviewer's correction on schema. `aidy_gold_expert_outcome_ledger` and `aidy_gold_expert_context_scores` are gate-centric: they require `packet_digest`, `gate_id`, `gate_version` (`migrations/d1/0026_gold_expert_conditional_trust.sql:10,40`). **A root family is not a gate**, and forcing `subject_type = 'root_family'` into columns with the wrong semantics would corrupt the contract.

Instead create dedicated tables:

    aidy_gold_root_family_outcome_ledger
    aidy_gold_root_family_context_scores

carrying a clean contract of their own: `family_id`, `family_version`, `family_balance`, `family_strength`, `bull_mass`, `bear_mass`, member ids/digest, environment/scope keys, resolved outcome, and PIT timestamps — with the same `research_only` / `live_money_execution_allowed` guards as the existing ledgers.

Initially family quality is *inferred* from member histories. After enough prospective cycles AIDY gains direct evidence — "`price_action` in London-open/high-volatility: N=87, edge +X; `liquidity_mechanism` same environment: N=54, edge +Y" — and the member-derived proxy can eventually be replaced by the family's own learned PIT track record, **without** pretending a family was ever an expert gate packet. Starting the writer on day one costs almost nothing and is the only way that history ever exists.

---

## 9. Gate calibration producer (immediately after — LOCKED)

Built from already-resolved gate history with strict `observed_at < decision_as_of`, feeding the existing tested Build 21 consumer.

**Explicitly not assumed to be an improvement.** `unknown` currently applies 0.85; real calibration returns 1.00, 0.90, 0.80, 0.75 **or 0.50** depending on N and error. Some gates will rise, others fall. **No rescue tuning.** Meta calibration stays deferred until the repaired system generates enough genuine directional meta decisions and they resolve.

---

## 10. Explicitly NOT in scope

Multi-horizon targets; magnitude or distribution prediction; MAE/MFE excursion; volatility-normalised outcome labels; coverage-weighted trust; regime-conditional baselines; any new data vendor; Databento. **One change, one question.**

---

## 11. Falsification — stated in advance

1. **T1 does not fail against current `main`** → the test is wrong, not the code. Stop.
2. **Direction remains unreachable** under any plausible mature configuration → the redesign failed. Do **not** relax constants to rescue it; return here and re-derive.
3. **Abstention rate collapses toward zero on replay** → sufficiency is too weak; over-corrected and equally wrong.
4. **Build 23 validation shows no improvement over the legacy view** once direction is reachable → the aggregation is coherent but the experts carry no usable Gold information. A real and acceptable finding, and the question we actually want answered.
5. **Any constant needs adjustment after seeing outcomes** → new dated pre-registration with the reason. Never silently retune.

---

## 12. Sequence after approval

1. Freeze constants. 2. Write T1–T12; **confirm T1 fails on current `main`**. 3. Implement §3.1–§3.6. 4. All tests plus full regression green. 5. Dedicated root-family tables and writer (§8). 6. Gate calibration producer (§9). 7. Environment cardinality fix. 8. PIT-safe H4/D1 rebuild from M1 lineage. 9. Maintenance-window bug. 10. Watchdog, append-only health history, scorecard baselines. 11. Re-run Build 23 honestly. 12. **Soak unchanged across multiple regimes.** 13. Only then judge whether the experts contain useful Gold information.

---

## 13. Status of rulings

**All prior rulings locked:** `pᵢ` over all qualifying contributors including neutral; sub-threshold families remain in `S`/`W` (with corrected rationale); strong opposing families → `genuine_independent_disagreement`; `FAMILY_NEUTRAL_BAND = 0.20`; global expanding PIT baseline; `MIN_FAMILIES = 2`; `EDGE_SCALE = 0.15` over PIT baseline; coverage report-only; gate calibration immediately after, accepted as-is.

**Nothing in v3 is left open.** The seven required changes are applied and the third redundancy (§5.1) is resolved. v3 is submitted for approval and freeze.
