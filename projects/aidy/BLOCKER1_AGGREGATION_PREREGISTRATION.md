# AIDY Blocker 1 — Aggregation Redesign Pre-Registration (v8 — MATHEMATICS FROZEN, FIXTURE REBUILD IN PROGRESS, 2026-09-22)

**Status: v8 — the aggregation MATHEMATICS IS APPROVED AND FROZEN.** The remaining work is fixture validation only; **no aggregation change is in scope.** NOT IMPLEMENTED. No AIDY code written. No production, config or holdout touched. v1 `a8b78fe` … v7 `0738716` preserved immutably.

**v7's T1 fixture is WITHDRAWN as non-executable.** Attempting to run it through the real pipeline proved it could not work: its eight synthetic contributors (`m5s:accept`, `h1s:trend`, …) do not exist. The real production path emits **70 sub-calculator subjects** with identities of the form `gate_id:calculator_id`, e.g. `m5_price_structure_expert:m5_trend_path`. The claim "the same frozen history derives every real contributor reliability" was therefore false, exactly as review stated.

Governing rule, unchanged: input distributions may be inspected for engineering sanity, but **no threshold may be tuned using the 41-cycle outcomes.** Build 23 is re-run only after constants are frozen.

---

## 0. Revision history

| version | change |
|---|---|
| v1–v6 | architecture, then successive corrections (see git history) |
| v7 `0738716` | graph-first `dᵢ`; canonical equation on `dᵢ`; first "immutable" fixture. **Mathematics approved.** |
| **v8 (this)** | **Mathematics frozen — unchanged.** v7's fixture **withdrawn as non-executable**; real 15-gate pipeline executed and the **real 70-subject manifest** captured; production-shaped windows, session-aware calendar and PIT `first_observed_at` corrected; **new latent production defect found** (§0.2). |

### 0.1 What executing the real pipeline established

A read-only validator (`projects/aidy/fixtures/blocker1_t1_pipeline_validator.py`) now runs the frozen source state through the genuine path: session-aware M1 spine → aggregates → `build_cycle_environment` → the 10 real expert builders (+5 explicit UNKNOWN). Verified output:

| fact | value |
|---|---|
| expert packets | **15** (10 computed + 5 explicit UNKNOWN) ✓ |
| **real sub-calculator subjects** | **70** — not the 8 v7 assumed |
| directional + known + vote ∈ {bullish,bearish,neutral} | 40 |
| of which `scoreable` (bullish/bearish) | 13 |
| manifest digest | `67de9eef1e92cd853f1b5a4bf1d4fbac96435561712dd9af9bffb2e3c2b9d437` |

Per-gate subject counts: `liquidity_reclaim_expert` 15, `h4` 8, `m5`/`m15`/`h1` 7 each, `momentum_impulse` 6, `volatility_jump` 6, `d1_context` 5, `price_location` 5, `session_participation` 4.

**Four fixture-shape errors found and corrected by execution:**

1. **Identities were fiction.** Real subjects are `gate_id:calculator_id`. The committed manifest is now the authority.
2. **Window shape was wrong.** Production uses **M1 = 2 days** and **aggregates = 45 days** (`private_forward_context.py:309-310`). v7 supplied a single 2-day M1 series and nothing else, so every `price_location` sub-calculator came back `insufficient`.
3. **The timeline was impossible.** v7 generated 2,880 consecutive M1 bars backwards from a Monday, trading straight through the weekend. The validator uses a session-aware calendar (Sun 18:00 → Fri 17:00 NY, daily maintenance 17:00–18:00 NY Mon–Thu): 2,880 market-open minutes now span **50 wall-clock hours**, not 48 — closures are genuinely skipped.
4. **`first_observed_at` was PIT-wrong.** v7 set it to the bar's **open**, though a completed bar's high/low/close cannot be known then. Corrected to the bar's **close** — which is also what the repo's own expert tests use (`first_observed_at = opened + STEP`).

Also corrected: `session_code` must match `market_sessions.session_code_at()` exactly or the session expert raises. At the frozen `as_of` (2026-06-03 14:00Z) the DST-correct code is `london_new_york_overlap`, not `new_york`.

### 0.2 NEW LATENT DEFECT — Liquidity/Reclaim expert can raise in the live path

Found while building the validator; reproducible.

`gold_liquidity_reclaim_expert._conclusion()` returns **`"neutral"`** when no sweep/reclaim proxy event carries a bullish or bearish vote. But the gate contract (`gold_expert_gate_contract.py:381-390`) requires a **known directional sub-calculator voting `neutral`** for a `neutral` conclusion. When `usable` is true (30 contiguous completed M1 present) and the event list is empty, the only sub-calculator is the `context_only` session/volatility context — so `build_liquidity_reclaim_expert` raises:

    ValueError: neutral gate conclusion requires a known neutral subcalculator

Reproduced when `price_location_expert` yields **zero references** (which happens whenever `exact_facts.location.mid` is absent, since `usable = mid is not None`).

**Blast radius.** `_build_experts` calls the builder unguarded, but `provider_entry.py:244` wraps the whole sync in try/except. So **market capture survives while the entire shadow cycle is lost** — recorded only in the singleton `aidy_gold_expert_shadow_sync_health` row, which keeps no history (audit Finding 7). A recurrence would look like an unexplained cycle gap with no durable trace.

**Not established:** whether live conditions actually produce zero references — in 41 live cycles they did not. But the crash path is real, unguarded, and reflects a genuine disagreement between the expert and the contract about what `neutral` means. It should be fixed regardless, and is logged in `KNOWN_ISSUES.md`.

### 0.3 Remaining work before the fixture can be frozen

Honest status: **the fixture is not yet frozen.** Still required —

- rebuild the frozen history against the **70 real subjects** from the committed manifest;
- add **production-shaped Build-3 gate-level trust history**: packet/version linkage, scope keys, scoped trust rows, so Build 21 can derive its selector envelopes from the fixture alone;
- add explicit **`decision_time_utc`** per commitment and derive `correct` as `predicted_class == realised_direction`, rather than storing `correct` as an independent knob;
- run **both paths** off that one state and record the old-path `directional_total` and decision by execution;
- freeze a manifest digest covering fixture SHA, packet count, subject-id list, outcome-history, trust-history and environment digests.

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
7. **Written mathematics must describe the machine that actually runs.** Every fixture in this document is derived by executing the real engine (§7.1), never by assuming its output.

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

#### 3.2.1 Stage-B contributors are SUB-CALCULATORS ONLY

v4 spoke generically of a "contributor" while also saying an abstaining *gate* contributes zero but its sub-calculators may enter. That left the contributor universe undefined.

Verified: `extract_dependency_signals` (`gold_evidence_dependency.py:184-236`) iterates **`packet["subcalculators"]` only** and never emits a gate-level signal. **There is therefore no Build-20 `uᵢ` for a gate at all**, and admitting gates alongside their own sub-calculators would count the same evidence twice.

**Ruling: for aggregation v1, `family_weight_eligible` applies to sub-calculators only.** Gate conclusions remain fully used for expert-level explanation, gate trust and scorecards, contradictions, gate diagnostics and judging whether the expert itself was right — but the root-family meta calculation consumes the underlying sub-calculator evidence graph **once**.

    sub-calculators -> dependency -> root families -> meta brain

with gates remaining human-readable specialist summaries over those same sub-calculators.

### 3.3 Decision-consumption dependency view — closing the ABSTAIN leak

**v3 asserted "an abstaining contributor consumes nothing at all". That was false.** `gold_evidence_dependency.py:271-276`:

    eligible = (role == "directional" and state == "known"
                and vote in {"bullish","bearish","neutral","abstain"} and weight > 0)

`abstain` **is** `eligible_for_directional_weight`, and the parent cap scales followers against `leader_raw_weight × PARENT_GROUP_INCREMENTAL_CAP` across that eligible set. An abstaining sub-calculator therefore consumes follower budget and **reduces every other contributor's effective weight** — zero direct vote, but real indirect influence.

**Resolution — two dependency passes, both persisted and digested:**

| pass | signal set | purpose |
|---|---|---|
| **full diagnostic** (unchanged) | all currently eligible signals, including `abstain` | Build-20 diagnostics, correlation history, audit trail. Behaviour and output unchanged. |
| **decision-consumption view** (new) | **only `family_weight_eligible` contributors** (§3.2): bullish, bearish, and denominator-only neutral. Excludes `abstain`, `unknown`, `context_only`. | supplies **structural facts only** — `correlation_group`, `evidence_identity`, `high_dependency` pairs — from which §3.4.3 computes `dᵢ`. It does **not** consume Build-20 weights or multipliers. |

Build 20 itself is **not modified**. Historical rolling-correlation diagnostics continue to use the full PIT history. What changes is only *which current evidence is permitted to consume family allocation*. Both views are stored per cycle so an auditor can see exactly what each produced.

This makes principle 5 true rather than aspirational.

### 3.4 Stage B — Exact family aggregation

For `family_weight_eligible` contributor `i` in root family `f`, with PIT reliability `rᵢ` (§3.1) and **order-independent dependency weight `dᵢ`** (§3.4.3). **No Build-20 weight or multiplier `uᵢ` is consumed anywhere in the decision path** — that formulation is withdrawn:

    pᵢ = dᵢ / Σ_{k family_weight_eligible in f} d_k     # Σpᵢ = 1 over ALL eligible contributors,
                                                        # including those voting neutral
                                                        # dᵢ per §3.4.3; Σd = 1 by construction, so pᵢ = dᵢ

    bull_mass_f = Σ pᵢ rᵢ   over bullish contributors
    bear_mass_f = Σ pᵢ rᵢ   over bearish contributors

    family_signed_evidence_f = bull_mass_f − bear_mass_f                  ∈ [−1, +1]
    family_strength_f        = | family_signed_evidence_f |               ∈ [ 0, +1]
    family_reliability_f     = bull_mass_f + bear_mass_f                  ∈ [ 0, +1]   (reporting)
    family_balance_f         = family_signed_evidence_f / family_reliability_f          (reporting)

Because `Σpᵢ = 1` and `rᵢ ≤ 1`, correlated `price_action` contributors cannot create several units of authority. Internally contradictory families weaken themselves, because opposing mass cancels inside `family_signed_evidence_f`.

**This replaces v4's `sign_f`, which was algebraically ambiguous.** v4 said `family_direction_f = sign(family_balance_f)` "treated as no-direction when `|family_balance_f| < FAMILY_NEUTRAL_BAND`", while simultaneously asserting `S = Σ sign_f × family_strength_f ≡ Σ (bull_mass_f − bear_mass_f)`. Those cannot both hold: at `family_balance_f = +0.10` a zeroed `sign_f` contributes 0 to `S`, yet `bull_mass_f − bear_mass_f ≠ 0`, so the identity breaks. There is now **one** definition and no sign function.

**`FAMILY_NEUTRAL_BAND` is therefore reporting/diagnostic only** and never zeroes evidence. A family inside the band is labelled `weak_no_directional_consensus` while its small signed evidence still influences `S` and `W` proportionally — exactly the bounded weak-family behaviour intended.

It also cannot affect any qualifying family: since `family_strength_f = family_reliability_f × |family_balance_f|` with `family_reliability_f ≤ 1`, any family meeting `family_strength_f ≥ 0.20` already has `|family_balance_f| ≥ 0.20`. So as a decision gate it was redundant — a fourth redundancy removed.

#### 3.4.1 Identity-order dependence — deeper than the parent cap

Found by executing the engine. Build 20 processes signals sorted by `(-raw_weight, signal_id)` and compares each against those already adjusted, so **three separate mechanisms are identity-order dependent**, not just one:

| mechanism | behaviour | rename test |
|---|---|---|
| `parent_root_incremental_cap` | leader keeps full weight; all other same-root evidence shares `leader_raw × 0.50`, so the leader carries ~2/3 of a family | ids `aaa`/`zzz` → leader `aaa:x`; renamed to `bbb`/`aab` → leader `aab:y` |
| `same_correlation_group_damped` | first-sorted keeps 1.000, later same-group same-vote signals damped to 0.350 | `aaa:p` 1.000 / `zzz:q` 0.350 → after rename `bbb:q` 1.000 / `yyy:p` 0.350 |
| `exact_duplicate_zero_increment` | first-sorted survives at 1.000, the duplicate is zeroed | same inversion under rename |

So **v5's fix was wrong.** Supplying `raw_weights = reliability_i` (a) only reordered the sort, leaving ties to fall back to `signal_id`, and (b) violated design principle 1 by making reliability determine independence: `rᵢ → raw_weight → pᵢ`, then `massᵢ = pᵢ × rᵢ` — reliability applied twice, with nonlinear leverage on the leader. **`raw_weights = reliability` is withdrawn.** Using Build 20's pre-parent-cap multipliers instead would also have failed, because two of the three mechanisms above sit *before* the cap.

#### 3.4.2 Build-20's parent-root cap is not used for decision consumption

The parent-root cap existed because every signal formerly entered **one global weighted sum**, where N correlated signals would otherwise contribute N. Stage B already supplies that bound mathematically: `Σpᵢ = 1` within a family and `|family_signed_evidence_f| ≤ 1`, so a root family can contribute at most one bounded unit however many members it has.

Applying the cap again therefore adds no protection and is the sole source of "leader carries two-thirds". **The obsolete aggregation mechanic is dropped; the dependency intelligence is kept.**

- The **full diagnostic pass stays byte-for-byte unchanged** (§3.3) — cap, sequential damping, diagnostics, persistence, audit trail.
- The **decision-consumption view** consumes Build 20's *structural facts* only: `correlation_group`, `evidence_identity`, and `high_dependency` pairs from the rolling diagnostics. It does **not** consume `dependency_multiplier`, `dependency_multiplier_pre_parent_cap` or `effective_weight`.

#### 3.4.3 `dᵢ` — order-independent dependency weight, graph built before reliability

Computed by the new aggregator, **per root family**, from Build-20 structural facts only. Prototyped and verified (`projects/aidy/blocker1_dependency_weight_prototype.py`).

**v6's own construction leaked.** v6 ordered it: collapse duplicates → pick the highest-reliability representative → *then* build the dependency graph on survivors. That lets reliability delete dependency edges. Counterexample, executed:

> `A1` and `A2` are exact duplicates. `A2` carries the **only** `high_dependency` edge to `B`.
> With `A1` more reliable, `A2` is discarded and the `A2↔B` edge disappears → **2 components**.
> With `A2` more reliable, `A2` survives and `B` joins its cluster → **1 component**.

So reliability still changed independence, indirectly through representative selection — re-joining the two quantities separated over six rounds. **Corrected order:**

    eligible signals -> structural graph -> connected components
                     -> duplicate slots -> cluster weight allocation
                     -> reliability applied ONCE

**Step 1 — build the structural graph over EVERY `family_weight_eligible` contributor.** Reliability is not consulted. Undirected edge between two contributors when **any** hold:

- same `correlation_group`;
- same `evidence_identity` (identical evidence is one cluster by definition);
- Build-20 rolling diagnostics report `high_dependency` for the pair.

Take **connected components** by union-find. Set-based, so the result is independent of input order and of every identifier. **No contributor is removed before this step**, so no edge can be lost.

**Step 2 — inside each completed component, collapse exact duplicates.** Group by `(evidence_identity, vote)`; each group yields **one duplicate slot**. The representative is the member with the highest `rᵢ`; **if several tie at the maximum they split that one slot equally** — never resolved by `signal_id`. *(Reliability selects the representative among identical evidence; it does not set the weight and can no longer affect topology.)*

**Step 3 — one unit per component.**

    dᵢ = (1 / component_count) × (duplicate_slot_shareᵢ / Σ slot shares in i's component)
    pᵢ = dᵢ / Σ_{k in family} d_k        # Σd = 1 by construction, so pᵢ = dᵢ

A discarded duplicate has no `dᵢ` and contributes nothing.

**Step 4 — reliability applied exactly once.**

    bull_mass_f = Σ pᵢ rᵢ   over bullish contributors
    bear_mass_f = Σ pᵢ rᵢ   over bearish contributors

`dᵢ` answers *"is this the same information?"*; `rᵢ` answers *"which reading of that information has historically been better?"* The separation is now real.

**Verified invariances** (prototype output):

| check | result |
|---|---|
| rename every `signal_id` | signed evidence identical (`0.341666667`) |
| tied reliability, opposing votes, renamed | identical (`0.200000000`) |
| tied exact duplicates, renamed | identical (`0.100000000`) |
| all 24 permutations of input order | **exactly 1 distinct result** |
| **duplicate carrying the only `high_dependency` edge, reliabilities swapped** | **components = 1 either way; signed evidence identical (`0.100000000`)** — was 2 vs 1 under v6 |

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

    S            = Σ_f  family_signed_evidence_f
    W            = Σ_f  family_strength_f                ( = Σ_f |family_signed_evidence_f| )
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

## 4. Pre-registered constants — FREEZE ON APPROVAL OF v7

| constant | value | status |
|---|---|---|
| `EDGE_SCALE` | `0.15` | **LOCKED** — 15pp over the PIT baseline (not raw accuracy) as full reliability. |
| `MIN_FAMILIES` | `2` | **LOCKED** |
| `MIN_FAMILY_STRENGTH` | `0.20` | **LOCKED** |
| `MIN_CONTRIBUTOR_N` | `12` | **LOCKED** — conservative **engineering eligibility floor**, matching the existing `mini_exact` minimum. Explicitly **not** a statistical-distinguishability claim. Never summed across correlated members. |
| `BALANCED_ABSTAIN_BAND` | `0.20` | **RENAMED from `NEUTRAL_BAND` (v4)** — same value, now an abstain band, per §3.6.1. |
| `FAMILY_NEUTRAL_BAND` | `0.20` | **REPORTING ONLY (v5)** — labels a family `weak_no_directional_consensus`. Never zeroes evidence and cannot affect a qualifying family, since `family_strength ≥ 0.20` already implies `\|family_balance\| ≥ 0.20`. |
| `PRIOR_STRENGTH` | `20` | reused (`TRUST_PRIOR_STRENGTH`). |
| `BASELINE_PRIOR_PER_CLASS` | `10` | **LOCKED** |
| `BASELINE_PRIOR_STRENGTH` | `30` | **LOCKED** — `= 3 × 10`; exactly 1/3 at zero history. |
| `W ≥ 0.40` | derived | **invariant/assertion only**, `= 2 × MIN_FAMILY_STRENGTH`. Not a decision condition. |
| ~~`MAX_CONFLICT`~~ | — | **WITHDRAWN (v2)** — unreachable. |
| ~~`MIN_TRUSTWORTHY_WEIGHT`~~ | — | **WITHDRAWN (v3)** — unreachable as an independent condition. |
| ~~`ALPHA`, `BASE_MIN_N`~~ | — | **WITHDRAWN (v3)** — created a baseline cliff. |
| ~~meta `neutral` output~~ | — | **WITHDRAWN (v4)** — conceptually wrong and unreachable; see §3.6.1. |
| ~~`sign_f`~~ | — | **WITHDRAWN (v5)** — algebraically ambiguous; replaced by `family_signed_evidence_f` (§3.4). |
| ~~`raw_weights = reliability_i`~~ | — | **WITHDRAWN (v6)** — re-coupled reliability and independence, and left ties resolved by `signal_id`. Replaced by order-independent `dᵢ` (§3.4.3). |
| ~~Build-20 parent cap in decision path~~ | — | **WITHDRAWN (v6)** — root-family normalisation already bounds a family at one unit (§3.4.2). Retained unchanged in the diagnostic pass. |

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

**v6 still only froze target *properties*** — 5,000 outcomes, 40/40/20 classes, N in [120,180], excess in [0,0.09]. Many different histories satisfy those, and different ones make the real experts behave differently. That is still "construct a source state later that satisfies these properties", not "freeze the source state, then see what happens".

**The actual fixture is therefore committed now, immutable:**

    projects/aidy/fixtures/blocker1_t1_fixture_generator.py    # every parameter fixed, seed 20260922
    projects/aidy/fixtures/blocker1_t1_full_fixture.json       # 1,323,314 bytes

    SHA-256: 656e56bfdbd5e2eb3f54d1f0eb1449a620b95893c7f594f9dd2492fb5287e5f3

Regenerable byte-identically (`--verify` confirms the digest). **Neither reviewer may change it after approval.** It contains exactly:

| element | frozen content |
|---|---|
| `as_of_utc` | `2026-06-01T12:00:00+00:00` |
| resolved outcome history | 5,000 rows with PIT `resolved_at_utc`, classes 2000/2000/1000 |
| PIT baselines at `as_of` | bullish `0.399602`, bearish `0.399602`, neutral `0.200795` — **derived**, per §3.1 |
| contributor histories | 8 contributors, 1,136 individual commitment rows with per-row `correct` and PIT timestamps |
| M1 series | 2,880 bars with `first_observed_at` and `revision_index`, the deterministic source for every aggregate |
| expected counts | 15 gates, 8 eligible contributors |

**Every reliability is derived from that history, never stated.** Applying §3.1 (`PRIOR_STRENGTH = 20`, `EDGE_SCALE = 0.15`, calibration `unknown` → 0.85 per §9) yields, for the record:

| contributor | family | vote | N | correct | `shrunk_excess` | `rᵢ` |
|---|---|---|---|---|---|---|
| `m5s:accept` | structure | bullish | 168 | 82 | 0.079079 | 0.448113 |
| `m15s:break` | structure | bullish | 156 | 74 | 0.066262 | 0.375482 |
| `h1s:trend` | structure | bullish | 144 | 66 | 0.051569 | 0.292222 |
| `h4s:swing` | structure | bullish | 132 | 59 | 0.041135 | 0.233097 |
| `momi:eff` | momentum | **neutral** | 150 | 69 | 0.053292 | 0.301988 |
| `locr:conf` | location | **neutral** | 138 | 61 | 0.037056 | 0.209985 |
| `liqp:depth` | liquidity | bullish | 162 | 77 | 0.067387 | 0.381859 |
| `liqr:speed` | liquidity | bullish | 126 | 54 | 0.025001 | 0.141671 |

The generator's `target_shrunk_excess` field is a construction aid only; **the derived values above are authoritative** (shrinkage over `N + 20` puts them slightly under target).

**Both paths read this one fixture:**

    OLD PATH:  fixture -> real expert builders -> 15 packets -> Build 20 -> 21 -> 22
    NEW PATH:  same fixture -> same 15 packets -> same sub-calculators
               -> decision view -> dᵢ (§3.4.3) -> root families -> new meta

**Scenario A — bullish reachable.** Verified against the frozen fixture: `price_action` signed `+0.224819`, `liquidity_mechanism` signed `+0.261765`, two qualifying families, `meta_balance = 1.000000` → **BULLISH**. Both families clear the 0.20 floor only narrowly, so the fixture is realistically tight rather than engineered to pass. **The expected decision is what this document freezes**; the old path's `directional_total` is recorded by execution at implementation, never estimated.

**Scenario B — bearish reachable.** The identical frozen fixture with every directional vote mirrored → expected **BEARISH**. No arithmetic is pre-committed; v5's `S = −0.964931` came from the withdrawn weighting scheme and is removed.

**Scenario C — genuine independent disagreement.** The identical frozen fixture with `liquidity_mechanism`'s directional evidence reversed → expected **ABSTAIN `genuine_independent_disagreement`**. v5's `+0.498264` / `−0.466667` values are likewise withdrawn.

**Scenario D — insufficient independent families.** Scenario A inputs, but both `liquidity` sub-calculators have `N = 8 < MIN_CONTRIBUTOR_N` so are not `family_weight_eligible` and never enter the decision-consumption pass → one qualifying family → **ABSTAIN `insufficient_independent_families`**.

**Scenario E — no directional evidence.** All contributors have `shrunk_excess ≤ 0` → `reliability = 0` → none eligible → `W = 0` → **ABSTAIN `no_directional_evidence`**.

**Scenario F — balanced directional evidence (future topology).** Explicitly synthetic: `volatility_regime`, `macro_information` and `analogue_memory` are constructed as directional, which they are **not** in the live configuration. `price_action` 0.40 bullish, `liquidity_mechanism` 0.25 bullish, three weak families at 0.15 bearish each. `S = 0.65 − 0.45 = 0.20`, `W = 1.10`, `meta_balance = 0.1818 < 0.20`; qualifying families = 2, same direction, so no disagreement → **ABSTAIN `balanced_directional_evidence`** (verified). Labelled a future-topology fixture because this condition cannot fire on the live 2-root graph.

**Scenario G — ABSTAIN has no indirect influence.** Run Scenario A, then add an abstaining sub-calculator to `price_action`. Assert `pᵢ`, every `family_strength`, `meta_balance` and the decision are **bit-identical**, and that the full diagnostic pass still records the abstaining signal. This is the §3.3 regression guard.

### 7.2 Remaining tests

**T2 — Redundancy.** Six agreeing `price_action` contributors must not outvote one `price_action` plus one `liquidity_mechanism`.
**T3 — Abstain never votes.** Gate-level `abstain` contributes exactly zero, with and without qualifying sub-calculators.
**T4 — Outcome reachability.** The four live-reachable outcomes asserted on the 2-root topology; `balanced_directional_evidence` on Scenario F. Each correctly named with its diagnostic payload.
**T5 — Bounds.** `rᵢ, pᵢ, family_reliability ∈ [0,1]`; `family_signed_evidence, family_balance, meta_balance ∈ [−1,+1]`; `family_strength = |family_signed_evidence|`; `Σpᵢ = 1` over eligible contributors; `W = 0` never divides; and the identity `S ≡ Σ family_signed_evidence_f` holds with no sign function anywhere.
**T6 — PIT.** `baseline`, `excess_j`, `reliability` and all calibration inputs use only evidence resolved strictly before `as_of`; hindsight guards extended to the new field names and to those the audit found missing (`realised_direction`, `realised_return_bps`, `return_bps`, `score`, `correct`, `impact_class`).
**T7 — No-edge silence.** A contributor at or below its PIT baseline contributes zero.
**T8 — Baseline continuity.** Continuous across **every** N with no rule switch; nothing discontinuous at N=29→30; exactly 1/3 at N=0.
**T9 — Weak families cannot manufacture corroboration.** Ten weak contributors inside one root must not satisfy `MIN_FAMILIES`.
**T10 — Weak-family influence bounded.** A sub-threshold family may move `meta_balance` only within the bound implied by its own `family_strength`, and can never alone carry a decision.
**T11 — Removed conditions stay removed.** No code path can abstain for `insufficient_trustworthy_weight`, `insufficient_contributor_history` or a `MAX_CONFLICT` test; `W ≥ 0.40` holds as an invariant whenever the family count is satisfied.
**T12 — Neutral contributors dilute (rewritten for §3.2).** One bullish contributor plus five `family_weight_eligible` neutral contributors must yield materially lower `family_strength` than that bullish contributor alone — **without** requiring `scoreable == true` for the neutral ones, and without altering the scoring contract.
**T14 — Identity cannot influence intelligence (§3.4.3).** Renaming every `signal_id` in the T1 fixture must leave `dᵢ`, `pᵢ`, every `family_signed_evidence`, `meta_balance` and the decision **bit-identical**. Include the negative control: the *current* Build-20 decision path under the same rename **does** change (`same_correlation_group_damped` and `exact_duplicate_zero_increment` invert), proving the test detects the defect it guards.
**T18 — Dependency topology is invariant to duplicate reliability (§3.4.3).** Two exact duplicates where **only the lower-reliability one carries a `high_dependency` edge** to a third contributor: swap their reliabilities and assert the component count, every `dᵢ`, `family_signed_evidence`, `meta_balance` and the decision are identical. Negative control: the v6 ordering (dedupe before graph) **must** change the component count from 1 to 2 under the same swap, proving the test detects the leak it guards.
**T17 — Tied-reliability redundancy is symmetric (§3.4.3).** Two highly dependent contributors with **equal** historical reliability, different `signal_id`s and **opposing current votes**: rename them and assert every meta-relevant output is identical. Repeat with tied exact duplicates (same `evidence_identity`, same vote). Also assert order invariance: all permutations of the input signal list produce one identical result.
**T15 — Gates never enter Stage B (§3.2.1).** Assert the decision-consumption contributor set contains only sub-calculator subjects, that no gate-level signal exists in it, and that a bullish gate does not add mass alongside its own bullish sub-calculators.
**T16 — Family scoring semantics (§8.1).** A frozen family at `strength ≥ 0.20` records bullish/bearish and is scoreable; below 0.20 records abstain and is unscoreable; a realised neutral makes a directional family prediction incorrect.
**T13 — No neutral meta prediction.** Assert the aggregator can never emit `neutral`; balanced directional evidence produces `abstain("balanced_directional_evidence")`. Assert `neutral` remains valid as a **realised outcome** class and that a directional prediction resolving neutral scores as incorrect.

---

## 8. Root families as first-class scored subjects — dedicated tables

`aidy_gold_expert_outcome_ledger` and `aidy_gold_expert_context_scores` are gate-centric: they require `packet_digest`, `gate_id`, `gate_version` (`migrations/d1/0026_gold_expert_conditional_trust.sql:10,40`). **A root family is not a gate**, so forcing `subject_type = 'root_family'` into those columns would corrupt the contract. Create instead:

    aidy_gold_root_family_outcome_ledger
    aidy_gold_root_family_context_scores

carrying `family_id`, `family_version`, `family_balance`, `family_strength`, `bull_mass`, `bear_mass`, member ids/digest, environment/scope keys, resolved outcome and PIT timestamps, with the same `research_only` / `live_money_execution_allowed` guards.

### 8.1 Prospective root-family scoring semantics (defined before collection starts)

Because family scorebooks begin on day one, how a family is scored is fixed **now**, so direct family reliability has a clean definition from the first recorded cycle:

| frozen family state | recorded family prediction | scoreable |
|---|---|---|
| `family_strength_f ≥ MIN_FAMILY_STRENGTH` and `family_signed_evidence_f > 0` | **bullish** | yes |
| `family_strength_f ≥ MIN_FAMILY_STRENGTH` and `family_signed_evidence_f < 0` | **bearish** | yes |
| `family_strength_f < MIN_FAMILY_STRENGTH` | **abstain** | no — unscoreable |

A realised `neutral` outcome remains legitimate and makes a bullish or bearish family prediction **incorrect**, exactly as for gates. Family excess skill uses the same §3.1 estimator (`excess_j` against the PIT baseline of the predicted class, shrunk toward zero edge), so family reliability will one day be directly comparable with contributor reliability.

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

1. Freeze constants. 2. Write T1–T18; **confirm T1 fails on current `main`** using the committed fixture (digest verified first). 3. Implement §3.1–§3.6, including the §3.3 filtered view and the §3.4.3 order-independent `dᵢ`. 4. All tests plus full regression green. 5. Dedicated root-family tables and writer (§8). 6. Gate calibration producer (§9). 7. Environment cardinality fix. 8. PIT-safe H4/D1 rebuild from M1 lineage. 9. Maintenance-window bug. 10. Watchdog, append-only health history, scorecard baselines. 11. Re-run Build 23 honestly. 12. **Soak unchanged across multiple regimes.** 13. Only then judge whether the experts contain useful Gold information.

---

## 13. Status

**Approved and locked:** continuous Dirichlet baseline; `MIN_FAMILIES = 2`; `EDGE_SCALE = 0.15` over PIT baseline; `MIN_FAMILY_STRENGTH = 0.20`; weak-family bounded influence; strong-family disagreement rule; dedicated family ledgers; coverage reporting; deferred meta-calibration; `pᵢ` over all eligible contributors including neutral; `FAMILY_NEUTRAL_BAND = 0.20`.

**Approved and unchanged in v7:** sub-calculators-only aggregation; `family_signed_evidence`; BULLISH/BEARISH/ABSTAIN; the Dirichlet baseline; family scoring semantics; weak-family bounded influence; the 0.20 strength floor; dedicated family ledgers; `family_weight_eligible`; filtered decision-consumption view; parent cap dropped from the decision path; topology-classified reachability; coverage reporting; deferred meta-calibration. **No frozen threshold or constant was altered by v7.**

**New in v7, submitted for approval:**
1. **Dependency leak in v6's own fix closed** (§3.4.3). The structural graph is now built over **every** eligible contributor *before* reliability selects any representative. Under v6, discarding a duplicate could delete the only `high_dependency` edge — executed counterexample: component count moved 2 → 1 purely by swapping two reliabilities. Reliability could still alter topology; now it cannot.
2. **Canonical Stage-B equation uses `dᵢ`** (§3.4). The obsolete `uᵢ = Build-20 effective weight` formulation is removed, so no implementer can follow the stale section and rebuild the mechanic §3.4.2 discards.
3. **T1's fixture is now real and immutable** (§7.1): `blocker1_t1_full_fixture.json`, 1,323,314 bytes, SHA-256 `656e56bf…87e5f3`, regenerable byte-identically from a committed generator with every parameter fixed. All 8 reliabilities are **derived** from its 1,136 frozen commitment rows, and Scenario A is verified to reach **BULLISH** with both families only narrowly clearing the 0.20 floor.
4. **Stale v5 arithmetic removed** from Scenarios B and C; they now freeze only the source transformation and the expected decision.
5. **T18 added** (topology invariance to duplicate reliability, with the v6 ordering as negative control); test count **T1–T18**.
6. §4 heading corrected to "FREEZE ON APPROVAL OF v7".

**Nothing is left open. v7 is the freeze candidate.**