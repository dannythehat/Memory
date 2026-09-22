# AIDY Blocker 1 — Aggregation Redesign Pre-Registration (DRAFT v2, 2026-09-22)

**Status: DRAFT v2 — NOT APPROVED, NOT IMPLEMENTED.**
No code has been written. No production, config or holdout touched.

v1 is preserved immutably in git at commit `a8b78fe`. This revision incorporates six amendments from independent review, four owner rulings, and one wording correction. It also raises **three new issues found while formalising the reviewer's family mathematics** (Sections 3.3.1, 3.4.1, 5.2) that must be resolved before freeze.

Governing rule, unchanged: input distributions may be inspected for engineering sanity, but **no threshold may be tuned using the 41-cycle outcomes.** Build 23 is re-run only after constants are frozen.

---

## 0. Revision history

| version | change |
|---|---|
| v1 (`a8b78fe`) | Initial architecture: separate reliability / independence / balance; normalised balance; separate sufficiency gate. |
| **v2 (this)** | Direction-aware PIT excess-skill measurement with a fully specified baseline estimator (§3.1). Exact family mathematics (§3.3). Internal-family conflict reduces family strength (§3.3). `MIN_FAMILY_STRENGTH` added (§4). `MIN_FAMILY_N` redescribed as an engineering floor, never summed across correlated members (§3.4). T1 tightened to production-realistic and required to fail first (§7). Root families become first-class scored subjects (§8). "Penalised twice" wording corrected (§1.1a). |

---

## 1. What is being replaced

    authority_g        = shrunk_accuracy × sample_confidence × scope × calibration × recency × dependency
    directional_total  = Σ authority_g   over gates concluding bullish/bearish
    abstain if directional_total < 0.30

Three defects:

1. **Units mismatch.** `dependency` is Build 20's evidence-redundancy *ratio* — "how much of this is new information?" — not a confidence. Multiplying it into a reliability product destroys each expert's reliability instead of governing how much independent evidence exists. Live values 0.0207–0.2168 per gate.
2. **Absolute threshold on a shrunken sum.** Live `directional_total` averages **0.004491** against a required 0.30.
3. **Unbounded, uninterpretable scale.** The sum has no natural range, so no threshold on it can be principled.

### 1.1 Two further defects found while designing the replacement

**(a) Sample size discounts reliability twice — corrected wording.**
`shrunk_accuracy` already pulls low-N gates toward the prior; the product then multiplies by `sample_confidence = N/(N+20)`, which discounts low N again (at N=4 the second term alone costs 83%).

Shrinkage plus a separate uncertainty term is **not inherently invalid** — they can legitimately represent different concepts. The defensible finding is narrower: **in the current authority product, combined with the absolute 0.30 threshold, the combination is catastrophically suppressive.** In the replacement, `sample_confidence` is removed from directional strength and N becomes an eligibility/uncertainty mechanism instead.

**(b) The 0.5 shrinkage prior is wrong for this target.**
The outcome is three-class and gates commit to one of two directions, so 0.5 is not chance. On the live resolved sample the marginals are ~0.58 bearish / 0.29 bullish / 0.13 neutral: a gate committing bearish is right ~58% of the time by luck, bullish ~29%. Shrinking both toward 0.5 flatters bullish calls and punishes bearish ones — which may be compounding H4's never-bearish behaviour on top of its data starvation.

**Replacing 0.5 with today's class marginal is not sufficient either.** Existing trust history aggregates a gate's bullish and bearish commitments together, so comparing one blended accuracy against one of today's class rates compares unlike quantities. §3.1 fixes this per-commitment instead.

---

## 2. Design principles (locked)

1. **Reliability, independence and directional balance are separate quantities**, never multiplied into one another.
2. **Build 20 is retained in full** — duplicate elimination, correlation grouping, parent-family graph, evidence identity. Only its *consumption* changes: it now determines relative contribution *inside* a root family.
3. **The directional measure is normalised** to `[-1, +1]`; absolute evidence quantity is a **separate sufficiency gate**.
4. **Abstain stays reachable for principled reasons** and must never again be produced by a unit artifact.
5. **An ABSTAIN gate never votes.** Zero directional weight at gate level; information recovered only beneath it (§5.3).

Five distinct questions, never again collapsed into one multiplication:

| question | answered by |
|---|---|
| Has this evidence historically worked? | reliability `rᵢ` (§3.1) |
| How is evidence de-duplicated inside a mechanism? | Build 20 weights `uᵢ` → `pᵢ` (§3.3) |
| Do members of a mechanism agree internally? | `family_balance_f` (§3.3) |
| Do independent mechanisms corroborate each other? | `MIN_FAMILIES`, `MIN_FAMILY_STRENGTH` (§3.4) |
| Which way does it lean, and is there enough? | `meta_balance`, `W` (§3.4) |

---

## 3. Proposed mathematics

### 3.1 Stage A — Direction-aware, PIT-aware excess skill

Skill is measured **per historical commitment**, against the class probability knowable *before that historical decision*.

**Baseline estimator (fully specified, as required).**
For class `c ∈ {bullish, bearish, neutral}` at time `T`:

    resolved(T) = outcomes with resolved_at_utc < T          # strict, PIT
    baseline(c, T) = (count_c(T) + ALPHA) / (count_total(T) + 3 × ALPHA)

- `ALPHA = 1` (Laplace smoothing over three classes).
- **History window: expanding** — all outcomes resolved strictly before `T`.
- **Fallback:** if `count_total(T) < BASE_MIN_N`, `baseline(c, T) = 1/3` for all classes.
- **Deferred:** a rolling or environment-conditional baseline is a known improvement but belongs with the Blocker-2 environment work, not here. v1 of this design uses a global marginal, consistent with the fact that environment conditioning does not currently function.

**Excess skill per commitment.** For each historical directional commitment `j` by contributor `i`:

    excess_j = correct_j − baseline(predicted_class_j, decision_time_j)      ∈ (−1, +1)

`correct_j ∈ {0, 1}`. The existing ±2/±1 net score is **not** used here; it remains a separately reported quantity. This measures only "did it beat chance", which is what reliability should mean.

**Shrink the mean excess toward zero edge** (not toward 0.5 accuracy):

    shrunk_excess_i = ( Σ_j excess_j ) / ( N_i + PRIOR_STRENGTH )        PRIOR_STRENGTH = 20

Equivalent to adding 20 pseudo-observations of zero edge. Reuses the existing `TRUST_PRIOR_STRENGTH = 20`.

**Reliability:**

    quality_i     = clamp( shrunk_excess_i / EDGE_SCALE, 0, 1 )
    reliability_i = quality_i × scope_mult × calibration_mult × recency_mult      ∈ [0, 1]

`sample_confidence` is **removed** (§1.1a); `dependency` is **removed** (it moves to §3.3). A contributor at or below its PIT baseline gets `reliability = 0` and is silent — intended.

### 3.2 Root family graph (existing, unchanged)

| root family | children | live status |
|---|---|---|
| `price_action` | structure, momentum, location | **live, directional** |
| `liquidity_mechanism` | liquidity | **live, directional** |
| `volatility_regime` | volatility | live, context-only |
| `participation_flow` | session_participation, futures_microstructure | partly live, context-only |
| `macro_information` | event, rates_usd, cross_market, news_mechanism | UNKNOWN |
| `analogue_memory` | analogue | UNKNOWN |
| `data_quality` | data_quality | never directional |

### 3.3 Stage B — Exact family aggregation

For qualifying contributor `i` in root family `f`, with PIT reliability `rᵢ` (§3.1) and Build-20 effective dependency weight `uᵢ`:

    pᵢ = uᵢ / Σ_{k ∈ f} u_k                         # normalised within the family; Σpᵢ = 1

    bull_mass_f = Σ pᵢ rᵢ   over bullish  contributors
    bear_mass_f = Σ pᵢ rᵢ   over bearish  contributors

    family_reliability_f = bull_mass_f + bear_mass_f                           ∈ [0, 1]
    family_balance_f     = (bull_mass_f − bear_mass_f) / family_reliability_f  ∈ [−1, +1]
    family_strength_f    = family_reliability_f × |family_balance_f|

Because `Σpᵢ = 1` and `rᵢ ≤ 1`, six correlated `price_action` calculators **cannot** create six units of authority. Internally contradictory families weaken themselves automatically.

**Useful identity (verified):** `family_strength_f` simplifies exactly to `|bull_mass_f − bear_mass_f|`, and `sign_f × family_strength_f = bull_mass_f − bear_mass_f`. This makes implementation trivial and confirms the formula is well-formed and bounded.

`family_direction_f = sign(family_balance_f)`, treated as neutral when `|family_balance_f| < FAMILY_NEUTRAL_BAND`.

#### 3.3.1 NEW ISSUE — what does `pᵢ` normalise over?

`Σpᵢ = 1` over *which* set? Two readings, materially different:

- **(A) All qualifying contributors, including neutral ones.** Neutral members hold probability mass that enters neither bull nor bear, so a family whose members mostly see nothing directional is correctly weaker.
- **(B) Directional contributors only.** A family with one bullish member and nine neutral ones would reach full strength on that single member.

**Recommendation: (A).** A mechanism in which most evidence sees no direction genuinely *is* weak directional evidence, and (B) would let a lone outlier speak for an entire mechanism. This matters immediately: momentum concludes neutral in 26/41 live cycles and `price_action` holds six members.

**Owner ruling required.**

### 3.4 Stage C/D — Meta balance and sufficiency

    S            = Σ_f  sign_f × family_strength_f      ( = Σ_f (bull_mass_f − bear_mass_f) )
    W            = Σ_f  family_strength_f
    meta_balance = S / W                                 ∈ [−1, +1],  defined only when W > 0

Direction is permitted only when **all** hold:

    count of families with family_strength_f ≥ MIN_FAMILY_STRENGTH   ≥ MIN_FAMILIES
    every counted family satisfies the contributor-N floor (below)
    W ≥ MIN_TRUSTWORTHY_WEIGHT
    not genuine independent disagreement (§5.2)

**Contributor-N floor (amendment 5).** Each qualifying contributor must **individually** satisfy `N_i ≥ MIN_CONTRIBUTOR_N`. `MIN_CONTRIBUTOR_N = 12` is a **conservative engineering eligibility floor**, chosen because it already exists in the trust engine as the `mini_exact` minimum — **not** a claim that N=12 is statistically distinguishable from baseline, which is not generally true. Statistical strength is handled by shrinkage and reported uncertainty. **Family N is reported as the minimum across its counted contributors and is never summed across correlated members.**

#### 3.4.1 NEW ISSUE — do sub-threshold families contribute to `S` and `W`?

A family with `family_strength_f = 0.05` fails `MIN_FAMILY_STRENGTH` for *counting*. Does it still enter `S` and `W`?

**Recommendation: yes — include every family with `family_strength_f > 0` in `S` and `W`, while only families ≥ `MIN_FAMILY_STRENGTH` count toward `MIN_FAMILIES`.**

Rationale: including a weak family is strictly conservative-or-neutral. If it agrees it adds equally to `S` and `W`, leaving `meta_balance` unchanged; if it disagrees it lowers `|meta_balance|`, making direction harder. Excluding weak families would mean discarding contrary evidence, which is how a system manufactures confidence.

**Owner ruling required.**

### 3.5 Stage E — Decision

    if not sufficient                          → abstain   (reason names the failed condition)
    elif genuine_independent_disagreement      → abstain   ("genuine_independent_disagreement")
    elif |meta_balance| < NEUTRAL_BAND          → neutral   ("balanced_independent_evidence")
    else                                        → bullish / bearish by sign(meta_balance)

Confidence remains **withheld** until meta-calibration exists. No number is invented.

---

## 4. Pre-registered constants — FREEZE ON APPROVAL OF v2

| constant | value | status | justification |
|---|---|---|---|
| `EDGE_SCALE` | `0.15` | **APPROVED** | 15 percentage points **over the PIT baseline** (not raw accuracy) as full reliability is deliberately demanding. Better to start strict than to make mediocre history look powerful. |
| `MIN_FAMILIES` | `2` | **APPROVED** | One mechanism cannot corroborate itself. Three would deliberately recreate a structural lock, since only `price_action` and `liquidity_mechanism` are directional today. Once Macro is live, three-family agreement becomes *stronger* evidence without becoming mandatory. |
| `MIN_FAMILY_STRENGTH` | `0.20` | **NEW (amendment 4)** | A family counts toward `MIN_FAMILIES` only if it independently carries meaningful evidence. Prevents one real family at 0.399 plus a token family at 0.001 from satisfying "two independent families". Two such families also **derive** the 0.40 total floor rather than leaving it arbitrary. |
| `MIN_TRUSTWORTHY_WEIGHT` | `0.40` | **APPROVED, now derived** | = 2 × `MIN_FAMILY_STRENGTH`. No longer a free parameter. |
| `MIN_CONTRIBUTOR_N` | `12` | revised description | Conservative engineering eligibility floor, matching the existing `mini_exact` minimum. Explicitly **not** a statistical-distinguishability claim. Never summed across correlated members. |
| `NEUTRAL_BAND` | `0.20` | **APPROVED** | Meta balance within ±0.20 means trustworthy independent evidence is close to evenly split. |
| `FAMILY_NEUTRAL_BAND` | `0.20` | **NEW** | Same logic applied inside a family, so an internally split mechanism reports neutral rather than a weak direction. |
| `PRIOR_STRENGTH` | `20` | reused | Existing `TRUST_PRIOR_STRENGTH`; shrinks mean excess toward zero edge. |
| `ALPHA` | `1` | **NEW** | Laplace smoothing for the baseline estimator. |
| `BASE_MIN_N` | `30` | **NEW** | Below this many resolved outcomes the baseline falls back to uniform 1/3. |
| ~~`MAX_CONFLICT`~~ | — | **WITHDRAWN** | See §5.2 — redundant as originally defined. |

---

## 5. Abstain semantics

### 5.1 Reachable, principled abstentions
`insufficient_independent_families`, `insufficient_family_strength`, `insufficient_contributor_history`, `insufficient_trustworthy_weight`, `genuine_independent_disagreement`. Each names its specific failed condition. **No abstention may be produced by scale or units.**

### 5.2 NEW ISSUE — `MAX_CONFLICT = 0.45` is unreachable and must be redefined

Deriving cross-family conflict in the new units: with `P` the strength agreeing with `sign(S)` and `Nn` the strength opposing, `W = P + Nn` and `|S| = P − Nn`, so

    conflict = Nn / W = (1 − |meta_balance|) / 2

Conflict is therefore a **pure function of `|meta_balance|`**. `conflict ≥ 0.45` implies `|meta_balance| ≤ 0.10`, which `NEUTRAL_BAND = 0.20` has already captured. **The `genuine_independent_disagreement` abstention would be unreachable**, silently violating principle 4 and test T4.

**Recommended redefinition — a genuinely distinct state:**

    genuine_independent_disagreement  ⟺
        at least 2 families with family_strength_f ≥ MIN_FAMILY_STRENGTH
        hold opposing family_direction_f

This requires *both* mechanisms to be individually strong, which is meaningfully different from "balance near zero". The distinction matters for a system whose purpose is honest uncertainty:

- **neutral** = the trustworthy evidence indicates no directional move.
- **abstain (disagreement)** = two strong independent mechanisms actively contradict each other, so we do not know.

Collapsing these into one state would lose exactly the signal this architecture exists to preserve. **Owner ruling required.**

### 5.3 Recovering sub-evidence without letting abstain vote

A gate concluding `abstain` contributes **exactly zero** at gate level. Its individual **scoreable directional sub-calculators** may enter their root family as contributors in their own right, but only where each independently satisfies:

- `role: directional`, `state: known`, `scoreable: true`;
- its own PIT track record as `subject_type = 'subcalculator'` with `N_i ≥ MIN_CONTRIBUTOR_N`;
- `reliability_i > 0` by §3.1 on its own history.

Infrastructure already exists: **3,742 sub-calculator snapshots** are being recorded and scored. Because conflicting sub-evidence now *reduces* `family_balance_f`, this recovers "the gate is unsure overall, but these sub-calculators have historically been valuable" **without** hiding disagreement and **without** assigning a direction to an expert that declined to give one.

---

## 6. Coverage must be visible (reporting only in v1 — APPROVED)

Every scorecard row gains:

    coverage_i           = committed_cycles_i / eligible_cycles_i
    accuracy_on_commit_i = existing accuracy, explicitly relabelled as conditional on committing
    baseline_i           = PIT baseline for the committed class
    edge_i               = accuracy_on_commit_i − baseline_i
    shrunk_excess_i      = §3.1

plus **majority-class, persistence and uniform-random baselines on every scorecard**.

Displayed prominently. **Not weighted into trust in v1** — that is a separate decision requiring enough real distribution first, and gets its own pre-registration.

---

## 7. Acceptance tests

**T1 — Production-realistic reachability (tightened, amendment 6).**
Build 22 already has synthetic tests proving the four outcomes can exist under hand-built inputs; those prove nothing we did not know. T1 must therefore use:

- all **15** gates with the real gate identities;
- the real **~91-signal** topology and the real `FAMILY_PARENT` root relationships;
- **pre-registered plausible mature reliability ranges**, fixed in this document before implementation;
- the real Build-20 dependency engine, not a stub.

It must demonstrate that **the current architecture fails under those realistic conditions** and that the replacement succeeds, with all four outcomes reachable. **T1 must fail against current `main`.** If it passes before the fix, the test is wrong — stop and fix the test rather than proceeding.

**T2 — Redundancy.** Six agreeing `price_action` contributors must not outvote one `price_action` plus one `liquidity_mechanism`.
**T3 — Abstain never votes.** Gate-level `abstain` contributes exactly zero, with and without qualifying sub-calculators.
**T4 — Principled abstention.** Every §5.1 reason independently reachable and correctly named — including `genuine_independent_disagreement` under §5.2.
**T5 — Bounds.** `rᵢ, pᵢ, family_reliability ∈ [0,1]`; `family_balance, meta_balance ∈ [−1,+1]`; `W = 0` never divides; `Σpᵢ = 1`.
**T6 — PIT.** `baseline`, `excess_j`, `reliability` and all calibration inputs use only evidence resolved strictly before `as_of`; hindsight guards extended to the new field names (and to the names §9 of the audit found missing).
**T7 — No-edge silence.** A contributor at or below its PIT baseline contributes zero.
**T8 — Baseline estimator.** Laplace smoothing, expanding window, `BASE_MIN_N` fallback to 1/3, and strict `resolved_at < decision_as_of` all verified directly.

---

## 8. Root families become first-class scored subjects (adopted)

From the day this ships, persist and score **root-family outputs** prospectively, not only member gates.

Concretely: `aidy_gold_expert_outcome_ledger` and `aidy_gold_expert_context_scores` currently constrain `subject_type` to `('gate','subcalculator')` (`migrations/d1/0026_gold_expert_conditional_trust.sql:10,40`). A migration must extend this to include `'root_family'`, and each cycle must record `family_balance_f`, `family_strength_f` and the resolved outcome per family.

Initially family quality is *inferred* from member histories. After enough prospective cycles AIDY gains direct evidence — "`price_action` in London-open/high-volatility: N=87, edge +X; `liquidity_mechanism` same environment: N=54, edge +Y" — and the member-derived proxy can eventually be replaced by the family's own learned PIT track record. Starting the writer now costs almost nothing and is the only way that history ever exists.

---

## 9. Gate calibration producer (immediately after — APPROVED)

Built from already-resolved gate history with strict `observed_at < decision_as_of`, feeding the existing tested Build 21 consumer.

**Explicitly not assumed to be an improvement.** `unknown` currently applies 0.85; real calibration returns 1.00, 0.90, 0.80, 0.75 **or 0.50** depending on N and error. Some gates will go up, others down. **No rescue tuning.** Meta calibration stays deferred until the repaired system generates enough genuine directional meta decisions and they resolve.

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

1. Freeze constants. 2. Write T1–T8; **confirm T1 fails on current `main`**. 3. Implement §3.1–§3.5. 4. All tests plus full regression green. 5. Root-family scoring migration and writer (§8). 6. Gate calibration producer (§9). 7. Environment cardinality fix. 8. PIT-safe H4/D1 rebuild from M1 lineage. 9. Maintenance-window bug. 10. Watchdog, append-only health history, scorecard baselines. 11. Re-run Build 23 honestly. 12. **Soak unchanged across multiple regimes.** 13. Only then judge whether the experts contain useful Gold information.

---

## 13. Open rulings required before freeze

| # | question | recommendation |
|---|---|---|
| 1 | §3.3.1 — does `pᵢ` normalise over **all** qualifying contributors (including neutral) or **directional only**? | **All**, so a mostly-neutral mechanism is correctly weak |
| 2 | §3.4.1 — do sub-threshold families still contribute to `S` and `W`? | **Yes** — strictly conservative; excluding contrary evidence manufactures confidence |
| 3 | §5.2 — accept the redefinition of `genuine_independent_disagreement` as ≥2 individually-strong families opposing, and withdraw `MAX_CONFLICT`? | **Yes** — otherwise that abstention is mathematically unreachable |
| 4 | §4 — accept `FAMILY_NEUTRAL_BAND = 0.20` and `BASE_MIN_N = 30`? | Yes as engineering defaults |
| 5 | §3.1 — accept the **expanding-window** global baseline for v1, with regime-conditional deferred to Blocker 2? | Yes — environment conditioning does not currently function, so a conditional baseline cannot be estimated honestly yet |

Already ruled and locked: `MIN_FAMILIES = 2`; `EDGE_SCALE = 0.15` over PIT baseline; coverage report-only; gate calibration immediately after, accepting whatever it says.
