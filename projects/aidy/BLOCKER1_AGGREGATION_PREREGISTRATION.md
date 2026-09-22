# AIDY Blocker 1 — Aggregation Redesign Pre-Registration (DRAFT v4 — FREEZE CANDIDATE, 2026-09-22)

**Status: DRAFT v4 — freeze candidate. NOT IMPLEMENTED. No code written.**
No production, config or holdout touched. v1 `a8b78fe`, v2 `8029712`, v3 `ecdb685` preserved immutably.

v4 applies five required changes. **Two were hard contradictions with the existing contract, both confirmed in source, and both were errors in v3 of mine.**

Governing rule, unchanged: input distributions may be inspected for engineering sanity, but **no threshold may be tuned using the 41-cycle outcomes.** Build 23 is re-run only after constants are frozen.

---

## 0. Revision history

| version | change |
|---|---|
| v1 `a8b78fe` | Separate reliability / independence / balance; normalised balance; separate sufficiency gate. |
| v2 `8029712` | Direction-aware PIT excess skill; exact family mathematics; internal-family conflict; `MIN_FAMILY_STRENGTH`; withdrew `MAX_CONFLICT` as unreachable. |
| v3 `ecdb685` | Qualifying contributors; corrected weak-family rationale; withdrew `MIN_TRUSTWORTHY_WEIGHT` and `insufficient_contributor_history`; continuous Dirichlet baseline; dedicated family ledgers. |
| **v4 (this)** | **`family_weight_eligible` replaces the impossible `scoreable`+neutral conjunction (§3.2).** **Final meta output is BULLISH / BEARISH / ABSTAIN — neutral withdrawn as a prediction (§3.6).** **Filtered decision-consumption dependency view so ABSTAIN has zero indirect influence (§3.3).** **Exact T1 fixture values specified in this document (§7.1).** Reachability classified by topology (§5.1). |

---

## 1. What is being replaced

    authority_g        = shrunk_accuracy × sample_confidence × scope × calibration × recency × dependency
    directional_total  = Σ authority_g   over gates concluding bullish/bearish
    abstain if directional_total < 0.30

1. **Units mismatch.** `dependency` is Build 20's evidence-redundancy *ratio*, not a confidence. Multiplying it into a reliability product destroys each expert's reliability instead of governing how much independent evidence exists. Live 0.0207–0.2168 per gate.
2. **Absolute threshold on a shrunken sum.** Live `directional_total` averages **0.004491** against a required 0.30.
3. **Unbounded, uninterpretable scale.**

### 1.1 Two further defects

**(a) Sample size discounts reliability twice.** Shrinkage plus a separate uncertainty term is not inherently invalid; the defensible finding is narrower: **in the current authority product, combined with the absolute 0.30 threshold, the combination is catastrophically suppressive** (at N=4, `sample_confidence` alone costs 83%).

**(b) The 0.5 prior is wrong, and the class marginal alone does not fix it.** The outcome is three-class while gates commit to one of two directions (live marginals ≈ 0.58 bearish / 0.29 bullish / 0.13 neutral), so 0.5 flatters bullish calls and punishes bearish ones. But existing trust history **blends** each gate's bullish and bearish commitments into one accuracy, so comparing that blend against one of today's class rates compares unlike quantities. §3.1 measures skill per commitment instead.

---

## 2. Design principles (locked)

1. Reliability, independence and directional balance are **separate quantities**.
2. **Build 20 is retained in full.** Only its consumption changes.
3. The directional measure is **normalised** to `[-1, +1]`; evidence quantity is a **separate sufficiency gate**.
4. Abstain stays reachable for **principled** reasons, never from a unit artifact.
5. **An ABSTAIN contributor has zero influence — direct or indirect** (§3.3).
6. **AIDY predicts direction or declines. It does not predict "no movement"** (§3.6).

---

## 3. Proposed mathematics

### 3.1 Stage A — Direction-aware, PIT-aware excess skill

    baseline(c, T) = (count_c(T) + BASELINE_PRIOR_PER_CLASS)
                     / (count_total(T) + BASELINE_PRIOR_STRENGTH)

`BASELINE_PRIOR_PER_CLASS = 10`, `BASELINE_PRIOR_STRENGTH = 30` — a symmetric Dirichlet prior of 30 pseudo-outcomes, 10 per class. Exactly `1/3` at zero history; the observed marginal takes control smoothly. **No hard switch, no discontinuity** (verified: N=29 → 0.5932, N=30 → 0.6000). Window global and expanding, strictly `resolved_at < T`. Deliberately strong early (N=10, count=8 → 0.450 not 0.800) and still conservative at N=1000 (0.573 vs 0.580 observed). Not outcome-tuned.

*Deferred:* rolling / environment-conditional baselines belong with Blocker 2; a conditional baseline cannot be estimated honestly while environment conditioning does not function.

    excess_j        = correct_j − baseline(predicted_class_j, decision_time_j)     ∈ (−1, +1)
    shrunk_excess_i = ( Σ_j excess_j ) / ( N_i + PRIOR_STRENGTH )                 PRIOR_STRENGTH = 20
    quality_i       = clamp( shrunk_excess_i / EDGE_SCALE, 0, 1 )
    reliability_i   = quality_i × scope_mult × calibration_mult × recency_mult     ∈ [0, 1]

`correct_j ∈ {0,1}`; `j` ranges over **directional commitments only**. The ±2/±1 net score stays a separately reported quantity. `sample_confidence` and `dependency` are both removed from this product. A contributor at or below its PIT baseline gets `reliability = 0` and is silent.

### 3.2 `family_weight_eligible` — replacing v3's impossible conjunction

**v3 was self-contradictory.** It required `scoreable == true` **and** `vote ∈ {bullish, bearish, neutral}`. But the contract defines (`gold_expert_gate_contract.py:280-284`, re-enforced by the verifier at `:720-724`):

    scoreable = (role == "directional" and state == "known" and vote in {"bullish","bearish"})

A neutral sub-calculator is `scoreable = False` **by contract**, and a neutral gate is `gate_scoreable = False`. So v3's neutral branch was impossible and T12 could never have passed. **We do not change the scoring contract to rescue a test.** Instead, a separate concept:

A contributor `i` is **`family_weight_eligible`** for family `f` iff **all** hold:

    state == known
    role  == directional
    N_i   ≥ MIN_CONTRIBUTOR_N          # own PIT directional commitments, never summed across members
    reliability_i > 0                  # §3.1
    current vote ∈ { bullish, bearish, neutral }

with this additional requirement by vote:

| current vote | requirement | contributes |
|---|---|---|
| `bullish` / `bearish` | **`scoreable == true` remains mandatory** | `pᵢ` share **and** bull/bear mass |
| `neutral` | `scoreable` is `false` by contract and is **not** required | `pᵢ` share only — **zero** bull/bear mass |
| `abstain`, `unknown`, `context_only` | — | **nothing at all; excluded entirely** |

A neutral contributor's `reliability_i` comes **entirely from its prior bullish/bearish PIT record**. We are explicitly **not** claiming its neutral calls predict neutral outcomes. The claim is narrower and defensible: *this historically useful directional sensor currently sees no direction, so a single bullish outlier must not inherit the whole family.*

This preserves the dilution property without touching target or scoring semantics.

### 3.3 Decision-consumption dependency view — closing the ABSTAIN leak

**v3 asserted "an abstaining contributor consumes nothing at all". That was false.** `gold_evidence_dependency.py:271-276`:

    eligible = (role == "directional" and state == "known"
                and vote in {"bullish","bearish","neutral","abstain"} and weight > 0)

`abstain` **is** `eligible_for_directional_weight`, and the parent cap scales followers against `leader_raw_weight × PARENT_GROUP_INCREMENTAL_CAP` across that eligible set. An abstaining sub-calculator therefore consumes follower budget and **reduces every other contributor's effective weight** — zero direct vote, but real indirect influence.

**Resolution — two dependency passes, both persisted and digested:**

| pass | signal set | purpose |
|---|---|---|
| **full diagnostic** (unchanged) | all currently eligible signals, including `abstain` | Build-20 diagnostics, correlation history, audit trail. Behaviour and output unchanged. |
| **decision-consumption view** (new) | **only `family_weight_eligible` contributors** (§3.2): bullish, bearish, and denominator-only neutral. Excludes `abstain`, `unknown`, `context_only`. | supplies `uᵢ` to §3.4. |

Build 20 itself is **not modified**. Historical rolling-correlation diagnostics continue to use the full PIT history. What changes is only *which current evidence is permitted to consume family allocation*. Both views are stored per cycle so an auditor can see exactly what each produced.

This makes principle 5 true rather than aspirational.

### 3.4 Stage B — Exact family aggregation

For `family_weight_eligible` contributor `i` in root family `f`, with PIT reliability `rᵢ` (§3.1) and **decision-consumption** Build-20 effective weight `uᵢ` (§3.3):

    pᵢ = uᵢ / Σ_{k family_weight_eligible in f} u_k     # Σpᵢ = 1 over ALL eligible contributors,
                                                        # including those voting neutral

    bull_mass_f = Σ pᵢ rᵢ   over bullish contributors
    bear_mass_f = Σ pᵢ rᵢ   over bearish contributors

    family_reliability_f = bull_mass_f + bear_mass_f                           ∈ [0, 1]
    family_balance_f     = (bull_mass_f − bear_mass_f) / family_reliability_f  ∈ [−1, +1]
    family_strength_f    = family_reliability_f × |family_balance_f|

Because `Σpᵢ = 1` and `rᵢ ≤ 1`, six correlated `price_action` contributors cannot create six units of authority. Internally contradictory families weaken themselves.

**Verified identity:** `family_strength_f ≡ |bull_mass_f − bear_mass_f|`, and `sign_f × family_strength_f ≡ bull_mass_f − bear_mass_f`.

`family_direction_f = sign(family_balance_f)`, treated as no-direction when `|family_balance_f| < FAMILY_NEUTRAL_BAND`.

### 3.5 Root family graph (existing, unchanged)

| root family | children | live status |
|---|---|---|
| `price_action` | structure, momentum, location | **live, directional** |
| `liquidity_mechanism` | liquidity | **live, directional** |
| `volatility_regime` | volatility | live, context-only |
| `participation_flow` | session_participation, futures_microstructure | partly live, context-only |
| `macro_information` | event, rates_usd, cross_market, news_mechanism | UNKNOWN |
| `analogue_memory` | analogue | UNKNOWN |
| `data_quality` | data_quality | never directional |

### 3.6 Stage C/D/E — Meta balance, sufficiency, decision

    S            = Σ_f  sign_f × family_strength_f      ( ≡ Σ_f (bull_mass_f − bear_mass_f) )
    W            = Σ_f  family_strength_f
    meta_balance = S / W                                 ∈ [−1, +1], defined only when W > 0

Sums run over **every** family with `family_strength_f > 0`.

    if W == 0                                   → abstain ("no_directional_evidence")
    elif qualifying_family_count < MIN_FAMILIES  → abstain ("insufficient_independent_families")
    elif genuine_independent_disagreement        → abstain ("genuine_independent_disagreement")
    elif |meta_balance| < BALANCED_ABSTAIN_BAND  → abstain ("balanced_directional_evidence")
    else                                         → bullish / bearish by sign(meta_balance)

**`qualifying_family_count`** = families with `family_strength_f ≥ MIN_FAMILY_STRENGTH`.
**Derived invariant, asserted not gated:** two qualifying families force `W ≥ 0.40`.

#### 3.6.1 Neutral withdrawn as a meta prediction — the conceptual correction

v3 emitted `neutral` when `|meta_balance| < 0.20`. **That conflated two different claims.**

> "Bullish and bearish evidence approximately balance" does **not** mean "Gold will make a neutral-sized move."

Balanced evidence is **epistemic uncertainty** — we do not know which way it will go — and the honest output is **ABSTAIN**. A genuine forecast that Gold stays inside the ±2bp band is a **magnitude** claim requiring separate evidence about no-move probability, and no calibrated no-move model exists.

Two independent problems, therefore:

1. **Conceptual.** Predicting "no direction" and predicting "no movement" are not the same statement, and v3 silently equated them.
2. **Reachability.** v3's `neutral` was unreachable anyway. `family_strength_f = family_reliability_f × |family_balance_f|`, so a family inside `FAMILY_NEUTRAL_BAND = 0.20` has `family_strength < 0.20` and can never be a qualifying family. With only two directional roots live, two qualifying families either agree (`|meta_balance| = 1.0`) or oppose (disagreement abstain) — there is no third family to supply opposing mass. Verified: pulling `|meta_balance|` below 0.20 against 0.65 of strong agreeing mass needs **> 0.434** of weak opposing mass, i.e. **≥3 further weak families**, hence **≥5 directional roots**.

**Ruling:** for this repair, AIDY's final predictive output is **BULLISH / BEARISH / ABSTAIN**.

- `neutral` is **retained as a realised outcome class** — a directional prediction can obviously resolve into a neutral market, and scoring is unchanged (`vote == realised_direction`).
- `neutral` is **retained inside experts** as an observation, and neutral contributors still dilute families (§3.2).
- A genuine NEUTRAL meta decision is **deferred** until a no-move/magnitude expert exists and has *prospectively demonstrated* that it predicts neutral outcomes. It then gets its own pre-registration.

Confidence remains **withheld** until meta-calibration exists. No number is invented.

---

## 4. Pre-registered constants — FREEZE ON APPROVAL OF v4

| constant | value | status |
|---|---|---|
| `EDGE_SCALE` | `0.15` | **LOCKED** — 15pp over the PIT baseline (not raw accuracy) as full reliability. |
| `MIN_FAMILIES` | `2` | **LOCKED** |
| `MIN_FAMILY_STRENGTH` | `0.20` | **LOCKED** |
| `MIN_CONTRIBUTOR_N` | `12` | **LOCKED** — conservative **engineering eligibility floor**, matching the existing `mini_exact` minimum. Explicitly **not** a statistical-distinguishability claim. Never summed across correlated members. |
| `BALANCED_ABSTAIN_BAND` | `0.20` | **RENAMED from `NEUTRAL_BAND` (v4)** — same value, now an abstain band, per §3.6.1. |
| `FAMILY_NEUTRAL_BAND` | `0.20` | **LOCKED** — internal family no-direction band; matches the meta band for interpretability. |
| `PRIOR_STRENGTH` | `20` | reused (`TRUST_PRIOR_STRENGTH`). |
| `BASELINE_PRIOR_PER_CLASS` | `10` | **LOCKED** |
| `BASELINE_PRIOR_STRENGTH` | `30` | **LOCKED** — `= 3 × 10`; exactly 1/3 at zero history. |
| `W ≥ 0.40` | derived | **invariant/assertion only**, `= 2 × MIN_FAMILY_STRENGTH`. Not a decision condition. |
| ~~`MAX_CONFLICT`~~ | — | **WITHDRAWN (v2)** — unreachable. |
| ~~`MIN_TRUSTWORTHY_WEIGHT`~~ | — | **WITHDRAWN (v3)** — unreachable as an independent condition. |
| ~~`ALPHA`, `BASE_MIN_N`~~ | — | **WITHDRAWN (v3)** — created a baseline cliff. |
| ~~meta `neutral` output~~ | — | **WITHDRAWN (v4)** — conceptually wrong and unreachable; see §3.6.1. |

---

## 5. Abstain semantics

### 5.1 Reachability, classified honestly by topology

Three conditions were removed as **unreachable by construction** — they could never fire under any topology given the constants:

| condition | why unreachable | resolution |
|---|---|---|
| `MAX_CONFLICT = 0.45` | conflict derives to `(1 − \|meta_balance\|)/2`, so `≥ 0.45` ⟺ `\|meta_balance\| ≤ 0.10`, already inside the 0.20 band | withdrawn; redefined structurally (§5.2) |
| `MIN_TRUSTWORTHY_WEIGHT = 0.40` | two families at ≥ 0.20 force `W ≥ 0.40`; cannot fail once the count succeeds | withdrawn as a condition; retained as an invariant |
| `insufficient_contributor_history` | `MIN_CONTRIBUTOR_N` applies at **eligibility**, so such contributors never enter `pᵢ`; a family of only these already has `family_strength = 0` | withdrawn as a reason; reported as diagnostic detail |

The remaining outcomes, with reachability stated per topology. **This distinction matters: a condition that is unreachable *today but reachable in principle* must not be deleted, and must not be pretended to fire either.**

| outcome | reachable with today's 2 directional roots | reachable in principle |
|---|---|---|
| `bullish` / `bearish` | **yes** (both roots strong and agreeing) | yes |
| `no_directional_evidence` | **yes** (`W = 0`) | yes |
| `insufficient_independent_families` | **yes** (only one root qualifies) | yes |
| `genuine_independent_disagreement` | **yes** (one strong each side) | yes |
| `balanced_directional_evidence` | **no** — needs ≥5 directional roots (§3.6.1) | yes |

T4 asserts the first four against the live 2-root topology and the fifth against an explicit future-topology fixture (§7.1, Scenario F). Explainability is preserved by attaching a structured diagnostic payload to every abstention — `families_below_strength`, `contributors_below_n`, `no_eligible_contributors` — rather than by inventing reasons that can never fire.

### 5.2 Genuine independent disagreement (locked)

    genuine_independent_disagreement  ⟺
        at least one family with family_strength_f ≥ MIN_FAMILY_STRENGTH on EACH side

Both mechanisms must be individually strong, which is materially different from "balance near zero". With the two currently directional roots:

| price_action | liquidity_mechanism | result |
|---|---|---|
| strong bullish | strong bullish | **bullish** |
| strong bearish | strong bearish | **bearish** |
| strong bullish | strong bearish | **abstain** |
| one strong only | — | **abstain** (insufficient families) |

This may prove over-conservative once Macro/Analogue supply three or four independent mechanisms. **If so, a new rule is pre-registered then.** It is not weakened now on the strength of hypothetical future data.

### 5.3 Recovering sub-evidence without letting abstain influence anything

A gate concluding `abstain` contributes **exactly zero, directly and indirectly** — the latter now guaranteed by §3.3. Its individual sub-calculators may enter their root family in their own right, but only where each independently satisfies the full §3.2 `family_weight_eligible` test on its **own** PIT record (including `scoreable == true` when voting directionally).

Infrastructure exists: **3,742 sub-calculator snapshots** are already recorded and scored. Because conflicting sub-evidence now *reduces* `family_balance_f`, this recovers "the gate is unsure overall, but these sub-calculators have historically been valuable" without hiding disagreement and without letting "I don't know" affect the outcome.

---

## 6. Coverage must be visible (reporting only — LOCKED)

Every scorecard row gains `coverage_i`, `accuracy_on_commit_i` (explicitly relabelled as conditional on committing), `baseline_i`, `edge_i`, `shrunk_excess_i`, plus **majority-class, persistence and uniform-random baselines on every scorecard**. Displayed prominently; **not weighted into trust**. Coverage-weighted selection gets its own pre-registration once real distribution exists.

---

## 7. Acceptance tests

### 7.1 T1 — Production-realistic reachability, fixture fully specified here

v3 referred to "pre-registered plausible mature reliability ranges" without stating them, which would have left room to choose a convenient fixture after implementation. **The exact values are therefore fixed below, before any code.** They deliberately do **not** resemble the 41 live outcomes; the purpose is to lock a reasonable mature-state engineering scenario in advance.

**Common mature-state assumptions (all scenarios):**

    count_total(T)    = 5000 resolved outcomes
    class marginals   = bullish 0.40, bearish 0.40, neutral 0.20   (deliberately NOT the live 0.58/0.29/0.13 skew)
    baseline(bullish) = baseline(bearish) = (2000 + 10) / (5000 + 30) = 0.399602
    topology          = all 15 real gate identities, ~91 signals, real FAMILY_PARENT relationships,
                        real Build-20 engine (both passes per §3.3), no stubs
    scope_mult        = 1.00 (mini_exact)     calibration_mult = 1.00 (strong)
    recency_mult      = 1.00 (stable)         so reliability_i = quality_i

**Scenario A — bullish reachable.**
`price_action`: 6 eligible contributors, each `N = 150`, `shrunk_excess = 0.09` → `quality = 0.09/0.15 = 0.60`. Four vote bullish, two vote neutral. Decision-consumption weights equal → `pᵢ = 1/6`.
`bull_mass = 4 × (1/6) × 0.60 = 0.40`, `bear_mass = 0` → `family_strength = 0.40` ✓
`liquidity_mechanism`: 2 contributors, both bullish, `N = 120`, `shrunk_excess = 0.075` → `quality = 0.50`, `pᵢ = 1/2`.
`bull_mass = 0.50` → `family_strength = 0.50` ✓
`S = 0.90`, `W = 0.90`, `meta_balance = 1.0`, qualifying families = 2 → **BULLISH**.

*Same fixture on current `main`:* `shrunk_accuracy ≈ 0.49`, `sample_confidence = 150/170 = 0.882`, and the measured live dependency multiplier (~0.03 for price gates, ~0.05 for liquidity) gives per-gate authority ≈ `0.49 × 0.882 × 0.03 ≈ 0.013`; summed over the directional gates ≈ **0.08 < 0.30 → abstain.** T1 therefore **fails on `main`** and passes after.

**Scenario B — bearish reachable.** Mirror of A with bullish/bearish exchanged → **BEARISH**.

**Scenario C — genuine independent disagreement.** `price_action` as in A (strength 0.40 bullish); `liquidity_mechanism` both contributors bearish at `quality = 0.50` (strength 0.50 bearish). Two qualifying families, opposite signs → **ABSTAIN `genuine_independent_disagreement`**.

**Scenario D — insufficient independent families.** `price_action` as in A (0.40 bullish); `liquidity_mechanism` contributors have `N = 8 < MIN_CONTRIBUTOR_N` so are not eligible → one qualifying family → **ABSTAIN `insufficient_independent_families`**.

**Scenario E — no directional evidence.** All contributors have `shrunk_excess ≤ 0` → `reliability = 0` → none eligible → `W = 0` → **ABSTAIN `no_directional_evidence`**.

**Scenario F — balanced directional evidence (future topology).** Explicitly synthetic: `volatility_regime`, `macro_information` and `analogue_memory` are constructed as directional, which they are **not** in the live configuration. `price_action` 0.40 bullish, `liquidity_mechanism` 0.25 bullish, three weak families at 0.15 bearish each. `S = 0.65 − 0.45 = 0.20`, `W = 1.10`, `meta_balance = 0.1818 < 0.20`; qualifying families = 2, same direction, so no disagreement → **ABSTAIN `balanced_directional_evidence`** (verified). Labelled a future-topology fixture because this condition cannot fire on the live 2-root graph.

**Scenario G — ABSTAIN has no indirect influence.** Run Scenario A, then add an abstaining sub-calculator to `price_action`. Assert `pᵢ`, every `family_strength`, `meta_balance` and the decision are **bit-identical**, and that the full diagnostic pass still records the abstaining signal. This is the §3.3 regression guard.

### 7.2 Remaining tests

**T2 — Redundancy.** Six agreeing `price_action` contributors must not outvote one `price_action` plus one `liquidity_mechanism`.
**T3 — Abstain never votes.** Gate-level `abstain` contributes exactly zero, with and without qualifying sub-calculators.
**T4 — Outcome reachability.** The four live-reachable outcomes asserted on the 2-root topology; `balanced_directional_evidence` on Scenario F. Each correctly named with its diagnostic payload.
**T5 — Bounds.** `rᵢ, pᵢ, family_reliability ∈ [0,1]`; `family_balance, meta_balance ∈ [−1,+1]`; `Σpᵢ = 1` over eligible contributors; `W = 0` never divides.
**T6 — PIT.** `baseline`, `excess_j`, `reliability` and all calibration inputs use only evidence resolved strictly before `as_of`; hindsight guards extended to the new field names and to those the audit found missing (`realised_direction`, `realised_return_bps`, `return_bps`, `score`, `correct`, `impact_class`).
**T7 — No-edge silence.** A contributor at or below its PIT baseline contributes zero.
**T8 — Baseline continuity.** Continuous across **every** N with no rule switch; nothing discontinuous at N=29→30; exactly 1/3 at N=0.
**T9 — Weak families cannot manufacture corroboration.** Ten weak contributors inside one root must not satisfy `MIN_FAMILIES`.
**T10 — Weak-family influence bounded.** A sub-threshold family may move `meta_balance` only within the bound implied by its own `family_strength`, and can never alone carry a decision.
**T11 — Removed conditions stay removed.** No code path can abstain for `insufficient_trustworthy_weight`, `insufficient_contributor_history` or a `MAX_CONFLICT` test; `W ≥ 0.40` holds as an invariant whenever the family count is satisfied.
**T12 — Neutral contributors dilute (rewritten for §3.2).** One bullish contributor plus five `family_weight_eligible` neutral contributors must yield materially lower `family_strength` than that bullish contributor alone — **without** requiring `scoreable == true` for the neutral ones, and without altering the scoring contract.
**T13 — No neutral meta prediction.** Assert the aggregator can never emit `neutral`; balanced directional evidence produces `abstain("balanced_directional_evidence")`. Assert `neutral` remains valid as a **realised outcome** class and that a directional prediction resolving neutral scores as incorrect.

---

## 8. Root families as first-class scored subjects — dedicated tables

`aidy_gold_expert_outcome_ledger` and `aidy_gold_expert_context_scores` are gate-centric: they require `packet_digest`, `gate_id`, `gate_version` (`migrations/d1/0026_gold_expert_conditional_trust.sql:10,40`). **A root family is not a gate**, so forcing `subject_type = 'root_family'` into those columns would corrupt the contract. Create instead:

    aidy_gold_root_family_outcome_ledger
    aidy_gold_root_family_context_scores

carrying `family_id`, `family_version`, `family_balance`, `family_strength`, `bull_mass`, `bear_mass`, member ids/digest, environment/scope keys, resolved outcome and PIT timestamps, with the same `research_only` / `live_money_execution_allowed` guards.

Family quality is initially *inferred* from member histories. After enough prospective cycles AIDY gains direct evidence — "`price_action` in London-open/high-volatility: N=87, edge +X" — and the proxy can be replaced by the family's own learned PIT record, without pretending a family was ever an expert gate packet. Starting the writer on day one is the only way that history exists.

---

## 9. Gate calibration producer (immediately after — LOCKED)

From already-resolved gate history with strict `observed_at < decision_as_of`, feeding the existing tested Build 21 consumer. **Not assumed to be an improvement:** `unknown` currently applies 0.85; real calibration returns 1.00, 0.90, 0.80, 0.75 **or 0.50**. Some gates will rise, others fall. **No rescue tuning.** Meta calibration deferred until the repaired system generates enough genuine directional meta decisions and they resolve.

---

## 10. Explicitly NOT in scope

Multi-horizon targets; magnitude, no-move or distribution prediction; MAE/MFE excursion; volatility-normalised outcome labels; coverage-weighted trust; regime-conditional baselines; a NEUTRAL meta decision; any new data vendor; Databento. **One change, one question.**

---

## 11. Falsification — stated in advance

1. **T1 does not fail against current `main`** → the test is wrong, not the code. Stop.
2. **Direction remains unreachable** under any plausible mature configuration → the redesign failed. Do **not** relax constants; return here and re-derive.
3. **Abstention rate collapses toward zero on replay** → sufficiency too weak; over-corrected and equally wrong.
4. **Build 23 validation shows no improvement over the legacy view** once direction is reachable → the aggregation is coherent but the experts carry no usable Gold information. A real and acceptable finding, and the question we actually want answered.
5. **Any constant needs adjustment after seeing outcomes** → new dated pre-registration with the reason. Never silently retune.

---

## 12. Sequence after approval

1. Freeze constants. 2. Write T1–T13; **confirm T1 fails on current `main`**. 3. Implement §3.1–§3.6 including the §3.3 filtered view. 4. All tests plus full regression green. 5. Dedicated root-family tables and writer (§8). 6. Gate calibration producer (§9). 7. Environment cardinality fix. 8. PIT-safe H4/D1 rebuild from M1 lineage. 9. Maintenance-window bug. 10. Watchdog, append-only health history, scorecard baselines. 11. Re-run Build 23 honestly. 12. **Soak unchanged across multiple regimes.** 13. Only then judge whether the experts contain useful Gold information.

---

## 13. Status

**Approved and locked:** continuous Dirichlet baseline; `MIN_FAMILIES = 2`; `EDGE_SCALE = 0.15` over PIT baseline; `MIN_FAMILY_STRENGTH = 0.20`; weak-family bounded influence; strong-family disagreement rule; dedicated family ledgers; coverage reporting; deferred meta-calibration; `pᵢ` over all eligible contributors including neutral; `FAMILY_NEUTRAL_BAND = 0.20`.

**New in v4, submitted for approval:** `family_weight_eligible` (§3.2); BULLISH/BEARISH/ABSTAIN only, neutral withdrawn as a prediction (§3.6.1); filtered decision-consumption dependency view (§3.3); exact T1 fixtures (§7.1); topology-classified reachability (§5.1); T12 rewritten and T13 added.

**Nothing is left open. v4 is the freeze candidate.**
