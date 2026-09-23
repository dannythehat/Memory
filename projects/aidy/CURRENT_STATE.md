# AIDY — Current State

Updated: **2026-09-23** (post Blocker-1 merge + directional skill measurement)

## RATES PATH CONNECTED (2026-09-23, PR #252)

The orphaned rates pipeline is joined. `treasury_rate_vintages` adapts the Treasury
curve AIDY has stored since 2026-08-18 into the FRED-shaped version records the rates
expert asks for, and `rates_usd_cross_asset_expert` is **no longer a stub** — it was
removed from `_DISCONNECTED_CONTEXT_GATES`, so four remain (macro_event,
futures_microstructure, news_mechanism, analogue).

| FRED series the expert asks for | Treasury source |
|---|---|
| DGS2 | UST_NOMINAL_2Y |
| DGS10 | UST_NOMINAL_10Y |
| DFII10 | UST_REAL_10Y |
| T10YIE | UST_NOMINAL_10Y − UST_REAL_10Y (derived, marked as derived) |

### The point-in-time rule, and why last night's fear was misplaced

`conservative_available_after(D)` is midnight UTC on **D+1** and is source-agnostic.
Treasury publishes date D's curve on D itself, about 19:30–22:00 UTC, so the existing
bound is already 2–4.5 hours **later** than real publication. **No new availability rule
was needed and no lookahead is introduced** — the thing I refused to rush was smaller
than I thought.

Availability is `max(conservative_available_after(D), first_observed_at)`, because ingest
sometimes lags: the 2026-09-11 curve was not in the database until 2026-09-13T07:00Z.
`verify_version_record` therefore accepts `>=` for a Treasury record and keeps `==` for
ALFRED. The argument that makes this safe: **moving availability later can only withhold
evidence the system might have used; it can never manufacture knowledge it did not
have.** Tests pin that the relaxation does not leak to ALFRED and that earlier-than-bound
is refused under both sources.

### What this does and does not do

It does NOT break the family deadlock and cannot. The expert is `context_only`, so every
subcalculator is non-scoreable and it contributes zero directional mass — pinned by test.
It turns the rates block from `unknown` on every cycle into `known`, which is context the
trust engine can condition on, and it stops a live daily feed being written and never read.

19 tests, **all driven by the real 69 rows exported from production**, including the real
expert builder against the real data and the empty-rows case. That choice was deliberate:
this morning a synthetic fixture passed while production stayed broken.

## READ FIRST — RECOVERED 2026-09-23 07:19Z

AIDY is back up. `status=ok`, the wedge cycle
`aidy_cycle_a4d43ad0d391e11a782a421b3b0ebb1e` is scored, and the loop is
**backfilling the missed window** in 15-minute steps (01:55 → 03:25 and climbing).

Verification of the fix, from production:

- packets split cleanly by version: **1,785 v1** frozen at 01:40:21 (never rewritten)
  and **105 v2** from 01:55 onward. The builder emits v2; old evidence stays verifiable.
- the scoreable rule validated in SQL against **all 10,749 stored subcalculators: zero
  violations**.
- the outcome ledger is growing again (246 → 251 resolutions) and now contains **29
  neutral outcomes** — neutral votes are being scored for the first time, which is what
  #249 was for.
- accuracy 0.3825 vs 0.3821 before, i.e. flat so far on a small number of new rows.

Total outage: **01:40:21Z → 07:19:25Z, five hours 39 minutes**, entirely self-inflicted,
across two incomplete fixes before the correct one.

### Deploy mechanics worth knowing next time

The deploy workflow has `concurrency: aidy-worker-deploy` with
`cancel-in-progress: false`, and its last step ("Prove first genuine Build 24 prospective
cycle and score") polls for up to ~22 minutes. So a failed deploy **blocks the next
deploy for 22 minutes** — including the deploy that fixes it. Cancelling the doomed run
releases the group immediately; its Deploy step has already completed by then, so
cancelling costs only the verification.

## OUTAGE DETAIL AND THE REAL BINDING CONSTRAINT (2026-09-23 07:00)

### AIDY was down for five hours and I caused it

Last cycle 2026-09-23T01:40:21Z. First error 01:47:54Z. 307 consecutive failed runs,
`RuntimeError: stored Build 24 expert packet failed verification`. Candle ingestion was
healthy the whole time, so only the shadow loop was dead.

PR #249 changed `subcalculator_is_scoreable` (scoring neutral votes) **without giving the
packet contract a new version**. Verification re-derives `scoreable` and compares it to
the stored value, so all 1,785 packets written before the change failed against the new
rule. The failure raises inside the scoring loop, which aborts the whole scheduled run,
so no new cycles were created either — and the unscored cycle stayed at the head of the
queue and failed again every minute. A permanent wedge.

Fixed in TWO parts. PR #250 versioned the contract (`v1` old rule, `v2` new rule,
verification dispatching on the packet's own declared version). **That was incomplete and
AIDY stayed down**, because `v1` does not identify one rule: the rule changed without a
version bump, so packets written either side of the #249 deploy both say `v1`.

Measured with `json_each` over the stored subcalculators:

| contract_version | neutral `scoreable` | packets | window |
|---|---|---|---|
| v1 | `false` | 673 | 09-21T16:10 → 09-23T01:25 |
| v1 | `true` | **5** | 09-23T01:40:21.480Z only |

Those 5 are the whole of cycle `aidy_cycle_a4d43ad0d391e11a782a421b3b0ebb1e` — the last
cycle created before the break and the single unscored cycle at the head of the queue.
Treating v1 as strictly the old rule rejected exactly those 5, so the loop stayed wedged
on the same cycle. PR #251 makes a v1 `directional`/`known`/`neutral` flag tolerant of
either value and nothing else; validated in SQL against all 10,749 stored
subcalculators with **zero violations**.

**I asserted in #250 that no packet was ever written under the new rule. That was false.**
The check matched `'"vote": "neutral"'` *with a space* against compact stored JSON, so it
could never match anything, and I read the zero as evidence. Third time this session a
broken query produced a confident wrong conclusion — **a query returning zero must be
proven able to return non-zero before it is used as evidence.**

Stored packets are never rewritten — `calculator_digest` seals `scoreable`, so amending
one would mean recomputing the digest that is the only reason it counts as evidence.

**Rule for the future: `scoreable` is sealed inside the packet digest. Any change to the
scoreable rule MUST ship a new contract version in the same commit.** A test now pins
both versions' rules so CI fails if this is forgotten again.

**Two signals fired and both were ignored:** the #249 deploy run itself FAILED
(run #39, 01:35→02:21), and the `AIDY Shadow Loop Watchdog` ran at 04:01 and FAILED.
Nobody was reading either. A watchdog that nothing watches is not a watchdog.

### Correction: I had the two families backwards

An earlier entry said price_action is the qualifier and the single-member
liquidity_mechanism is dead weight. **Measured over the 8 cycles that have family data,
the opposite is true:**

| family | members | cycles qualified | best strength | max possible if unanimous |
|---|---|---|---|---|
| liquidity_mechanism | 1 | **2 of 8** | 0.339 | **0.582** |
| price_action | 8–9 | **0 of 8** | 0.042 | **0.093** |

`min_family_strength` is **0.20**.

### The binding constraint is not the family count. It is reliability.

**price_action cannot qualify even if every one of its nine members voted the same way.**
Its ceiling is Σ(dependency_weight × reliability) = **0.093 against a 0.20 bar** — 46 per
cent of the threshold. Two things cause it:

1. **Dependency discount.** Eight members share one price series, so each is weighted
   0.125. This is correct — they are not independent evidence — but it means the family's
   total influence is capped near one member's worth.
2. **Low reliabilities.** Most members sit under 0.07, because `quality` is 0.000 for
   many of them: no measured edge over baseline. `calibration_state` is still `unknown`
   (×0.85) across the board.

So the abstention is **not a plumbing failure. It is the gate correctly refusing to
trade on experts that have no measured edge.** That is the machinery working.

### Why the reliabilities are honest

Over 246 resolved directional calls at gate_global: **38.21 per cent correct** against a
majority baseline of **51.22 per cent** (always-bearish). That is ~13 points below
baseline, and below a coin flip, at z ≈ −3.7 (p ≈ 0.0002). The experts are momentum
extrapolators committing when momentum looks strongest, which is when it stops.

Being reliably wrong is information — but the specific mechanism is still under-powered
(n=138, p=0.27), so it is measured per expert and nothing is inverted.

### What this means for the plan

Adding a new directional family is still necessary (2 families needed, only 1 can ever
qualify today), but it is **not sufficient**: a new expert with no edge would carry the
same low reliability and fail the same 0.20 bar. The order is:

1. Keep AIDY alive and accruing labelled evidence — the scarcest resource here, and the
   only thing that can move `quality` off 0.000.
2. Fix the orphaned rates path (below) so macro evidence exists at all.
3. Then build a directional expert in an empty root family, judged on measured edge
   rather than on being new.

Do NOT lower `min_family_strength` or `min_families` to make this go away. That is
making the threshold fit the answer. The thresholds are the only thing currently
preventing AIDY from acting on experts that are provably worse than a coin flip.

## READ FIRST — THE FULL BLOCKER CHAIN (2026-09-23, diagnosis complete)

### Correction to an earlier entry

An earlier note said the fix was to "populate the five dark experts' data sources".
**That is wrong and must not be actioned.** All nine context experts are
`gate_mode="context_only"` — verified in source. A context_only gate emits
`conclusion="context_only"` and contributes **zero directional mass**. Feeding them data
cannot break the family deadlock. It would add context, not votes.

### The five dark experts are not data-starved. They are never called.

`gold_expert_shadow.py` defines `_DISCONNECTED_CONTEXT_GATES` containing
macro_event, rates_usd_cross_asset, futures_microstructure, news_movement_mechanism and
analogue_episode. At line ~627 the shadow loop iterates that set and emits
`_build_unknown_with_history(...)` for each — **the real expert builder is never
invoked**. Five fully built, fully tested experts are hardcoded stubs in the live path.

### Two parallel rates pipelines, neither connected

| | |
|---|---|
| `cross_market.py` writes | `UST_NOMINAL_2Y`, `UST_NOMINAL_10Y`, `UST_REAL_10Y` — **live, fresh to 2026-09-22T20:01** |
| read by | **nothing** (only `ENABLED_SERIES`, a config list, is imported) |
| `gold_rates_usd_cross_asset_expert` reads | FRED series `DGS2`, `DGS10`, `DFII10`, `T10YIE` via ALFRED |
| stored FRED data | none in D1 |

All four FRED series are available or derivable from the orphaned Treasury data —
`T10YIE = DGS10 − DFII10` is its actual definition (`macro_vintages.py:517`).

**Why this was not fixed tonight:** `verify_version_record` (`macro_vintages.py:396`)
hard-requires `source == "fred_alfred"`. Adapting Treasury data means either falsifying
provenance — never — or extending a point-in-time integrity contract with a correct
conservative availability rule for Treasury publication times (~15:30 ET, different
vintage semantics from ALFRED). Getting that rule wrong injects lookahead into the one
subsystem proven clean. It needs doing carefully and awake, not quickly.

### News feeds: three of four stalled

| feed | rows | last observed |
|---|---|---|
| federal_reserve_rss | 55 | **2026-09-22** (live) |
| bea_releases | 16 | 2026-09-05 (stalled) |
| bea_schedule | 46 | 2026-09-04 (stalled) |
| federal_reserve_calendar | 6 | 2026-09-01 (stalled) |

### The deadlock, and what actually breaks it

Need 2 qualifying independent families. Only 2 produce directional mass: price_action
(8 members) and liquidity_mechanism (**1 member**). Measured since the brain deployed at
00:22: best achieved is **1** qualifying family, and it stays 1 even when liquidity
abstains — so the qualifier is price_action and the single-member family never gets
there. **The deadlock does not resolve on its own.**

Do NOT break it by:
- lowering the family threshold (fitting the threshold to the answer);
- splitting `momentum` out of `price_action` to manufacture a third family — they derive
  from the same price series and the folding is a correct dependency claim;
- promoting volatility_jump or session_participation to directional — volatility and
  participation are not directional phenomena and forcing a vote invents signal.

**The one legitimate route is a genuinely independent directional evidence source.**
Real yields → gold is the honest candidate: it is a real economic mechanism, it lands in
the empty `macro_information` root family, and the data is already arriving daily.

### Ordered build plan

1. Extend the vintage contract to accept a `us_treasury` source with its own correct
   conservative availability rule. Prerequisite for everything macro.
2. Connect `rates_usd_cross_asset_expert` — remove it from `_DISCONNECTED_CONTEXT_GATES`
   and feed it real records. Adds context, not votes.
3. Build a **directional** macro expert on real yields in `macro_information`. This is
   the step that breaks the deadlock.
4. Restart the three stalled news feeds.

## PREVIOUS READ FIRST — THE STRUCTURAL DEADLOCK (2026-09-23, brain deployed 00:22 UTC)

The Blocker-1 brain is **deployed and running**. Proof: the abstain reason changed from
`insufficient_directional_authority` (old 0.30 weight gate) to
`insufficient_independent_families` (new family aggregator).

It still abstains, and now we know exactly why — and it is not a data-volume problem.

### Only 6 of 15 experts can ever vote a direction

| | count | experts |
|---|---|---|
| **directional** | **6** | liquidity_reclaim, momentum_impulse, h1/h4/m5/m15_price_structure |
| context_only, available | 4 | price_location, session_participation, d1_context, volatility_jump |
| **context_only, DARK** | **5** | analogue_episode, macro_event, futures_microstructure, news_movement_mechanism, rates_usd_cross_asset |

A `context_only` gate emits `conclusion = "context_only"`. It can **never** contribute
directional evidence. So nine of the fifteen experts cannot, by design, move the
decision — and five of those nine are `explicit_unknown` because their data sources are
effectively empty (news 123 rows, cross-market 75 rows).

### Those 6 collapse into 2 root families, against a requirement for 2

Live family view at 2026-09-23T01:25:

| family | members | reliability | strength | qualifies |
|---|---|---|---|---|
| price_action (structure + momentum) | 8 | 0.069476 | 0.014078 | no |
| **liquidity_mechanism** | **1** | 0.000000 | 0.000000 | no |

`qualifying_family_count = 0`, threshold 2.

**There is no third family and no margin.** AIDY can only ever speak when BOTH
price_action AND a single-expert family qualify at the same moment. The headline "15
experts, 24 builds" hides that the decision rests on six voters in two groups, one of
which is one expert.

### Do NOT fix this by lowering the family threshold

That is the frozen pre-registered spec, and relaxing it to 1 family would be making the
threshold fit the answer — the exact error this programme keeps catching. The fix is to
**add genuine evidence diversity**: populate the five dark experts' data sources, and/or
promote context_only experts that legitimately carry direction.

### Why the neutral fix matters more than it first appeared

`liquidity_mechanism` shows reliability 0.000000 partly because its single member voted
neutral, and a neutral vote carried no mass and produced no trust. Scoring neutral
(merged in #249, deployed) lets that single-member family accumulate reliability at all
instead of sitting at zero — it is the specific unblocker for the family that gates the
whole aggregator, not just "more evidence in general".

### The data context that still applies

Entire labelled history is **three days**: 66 cycles (21 Sep), 88 (22 Sep), 7 (23 Sep) —
88/day, one per 15-minute window. 156 outcomes. No regime filter, polarity verdict or
per-expert conclusion is reachable yet at any significance. Session continuation rates
order sensibly (asia 60%, overlap 45.2%) but at z = 1.16, p = 0.25 — nowhere near, and
Bonferroni over three pre-registered hypotheses makes it worse.

## PREVIOUS READ FIRST — WHY AIDY IS NOT SMART (measured 2026-09-23)

The machinery is not the problem. The evidence base and the label are. All figures
below were measured directly against production D1 `aidy-ops-test`.

### 1. The 68,000-row ledger is 240 observations

`aidy_gold_expert_outcome_ledger` holds 68,058 rows. Those are 11,908 results fanned
across 3,648 scope keys. At `gate_global` — the scope every expert actually falls back
to — the entire scored evidence base is **240 directional gate calls** (126 bullish,
114 bearish).

This is why `sample_confidence` climbs while accuracy never moves: the trust engine
counts the same handful of events hundreds of times. **Confidence is growing while
information is not.**

### 2. The higher timeframes barely exist

| timeframe | bars in existence |
|---|---|
| 1m | 41,222 (42 days) |
| 5m | 1,933 |
| 15m | 736 |
| 1h | 184 |
| **4h** | **50** |
| **1d** | **12** |

`h4_price_structure_expert` made 7 directional calls all session because it has 50 bars.
The daily context expert has 12. They are starving, not broken.

News (`market_event_observations`) = **123 rows**. Cross-market = **75 rows**.
`aidy_memory_episodes` = **0**. `aidy_forward_outcomes` = **0**. There is no rich
multi-source dataset yet — there is 42 days of gold M1 and very little else.

### 3. The label is close to noise

Horizon 15 minutes, 15 M1 bars. Mean move: bullish +11.53 bps, bearish −11.27 bps,
neutral band roughly ±2 bps. On gold near $4,350 that is about $5 of movement — roughly
three times the spread.

Accuracy does improve with horizon but never reaches the baseline:

| horizon | accuracy | majority baseline | gap |
|---|---|---|---|
| 15 min | 0.3775 | 0.5076 | −13.0 |
| 60 min | 0.3659 | 0.4499 | −8.4 |
| 240 min | 0.3831 | 0.4845 | −10.1 |
| 960 min | 0.4185 | 0.4665 | −4.8 |

### 3b. WHY THEY READ IT BACKWARDS — momentum extrapolation (2026-09-23)

**Ruled out: the label.** Six consecutive outcomes recomputed from raw M1 candles match
the stored values exactly to six decimal places (e.g. 4357.95862 → 4349.03998 = −20.465
bps, stored −20.465178). Sign convention correct, 15 bars each, and every outcome window
opens strictly after its decision. No label bug, no inverted sign, no lookahead.

**Ruled out: simple mean reversion.** Across contiguous cycle pairs gold *continues* the
prior 15-minute move **56.9%** of the time. A trivial "same as last 15 minutes" rule
would beat every expert.

**The mechanism.** Over the 138 gate calls where the previous resolved move was known:

| | |
|---|---|
| experts voted WITH the prior move | **66.7%** |
| market continued the prior move | **43.5%** |
| followed momentum | n=92, accuracy **0.4022** |
| faded momentum | n=46, accuracy **0.5000** |

The experts are **momentum extrapolators**. Conditional on the moments they commit to a
direction, gold reverts more often than it continues — they commit when momentum looks
strongest, which is exactly when it stops. That reconciles everything: clean label,
clean PIT, no simple reversion, ensemble consistently below baseline.

**Not yet proven.** At n=138 the follow/fade split is z = −1.1, p = 0.27. Only the
aggregate inversion is significant (p = 0.026). **Do not flip, weight or invert anything
on this.** `gold_expert_momentum_stance.py` measures it per expert on the daily report
(`MIN_STANCE_N = 40`, frozen before the result was examined) so the hypothesis hardens
or dies on evidence.

If it does harden, the options in order of honesty are: (a) move the primary horizon to
where momentum persists — the baseline gap already narrows from −13.0 at 15 min to −4.8
at 960 min; (b) teach the experts a regime filter so they only extrapolate when
continuation is likely; (c) invert. (c) is last for a reason.

### 4. THE FINDING — the experts are anti-correlated, symmetrically

| expert says | scored | correct | accuracy | base rate | gap |
|---|---|---|---|---|---|
| bullish | 126 | 40 | 31.75% | 39.0% | **−7.25** |
| bearish | 114 | 50 | 43.86% | 50.8% | **−6.94** |

Both call types underperform their own base rate by almost exactly 7 points. A
directional bias would help one side and hurt the other; this hurts both equally.
Expected correct under random guessing with the same call mix: 107. Observed: 90.
**z = −2.22, p ≈ 0.026.**

No skill sits *at* base rate. This is consistent, significant, anti-correlated
information — the experts are reading something real and reporting it backwards. Same
signature as the m5 finding (`gold_expert_directional_skill.py`), now at ensemble level.
**Do not flip anything yet**; the daily skill report will say when it clears the
family-wise threshold.

### 5. Two-thirds of the brain's output is discarded

Directional experts vote: **abstain 34.1%, neutral 30.0%**, bullish 19.0%, bearish 17.0%.
The market is neutral **10.2%** of the time.

Experts call neutral three times too often, and a neutral vote is not scoreable, so
**64% of expert output never becomes evidence**. That is why 156 cycle outcomes produced
only 240 scored gate calls across six directional experts.

### Priority order

1. **Neutral band** — experts' neutral threshold and the outcome's ±2 bps definition are
   measuring different things by a factor of three. Fixing this roughly triples the
   evidence base with no new data collection. **In progress.**
2. **Stop counting 156 events as 68,000** — `sample_confidence` must key on distinct
   cycles, not ledger rows.
3. **Backfill H1/H4/D1 from the 42 days of M1** — cheapest capability gain available;
   three of fifteen experts cannot function without it.
4. **Then** test the inversion, once it clears family-wise significance.

## PREVIOUS READ FIRST

**The Blocker-1 repair is now on `main`** (PR #245, merge `7349331`). It had been
sitting as a *draft PR* since 2026-09-22 09:46 with CI green — that is the only reason
it never shipped. `main` now carries `gold_family_meta_direction.py`, wired into the
live shadow path, plus the reusable global-core trust scope.

**`main` is NOT deployed.** Deployment is a separate owner-initiated step via
`aidy-provider-research-read-deploy.yml`.

## What the live brain was doing before the merge

Measured against D1 `aidy-ops-test` (3588d82a-d686-4430-872d-d4c0e62c3d5d) at
2026-09-22T23:39Z, 110 cycles over 31 hours:

| | |
|---|---|
| cycles returning `abstain` | **110 of 110**, `insufficient_directional_authority` |
| directional authority mean / max | 0.0242 / 0.0643 against a **0.30** threshold |
| cycles ever clearing the threshold | **0** |
| meta outcomes resolved | 106, **all `correct IS NULL`** |

An abstain cannot be scored, so the meta loop had produced zero labelled examples
about itself. Expert-level scoring *was* working: 64,485 ledger rows, 116 subjects.

## Accuracy against baselines — the number that matters

| | accuracy |
|---|---|
| always answer "bearish" (majority class) | **48.46%** |
| guess in proportion to base rates | 40.5% |
| **AIDY gates** (n=1,362) | **37.44%** |
| **AIDY subcalculators** (n=9,471) | **38.36%** |
| uniform random over 3 classes | 33.3% |

Class balance: bearish 48.46% / bullish 39.46% / neutral 12.07%. AIDY sits ~11 points
below the trivial baseline. Caveat: 31 hours, one instrument, a bearish-skewed window
that flatters majority-class.

**Accuracy is flat across scopes** — `mini_exact` 0.3826 vs `gate_global` 0.3823.
Conditioning bought nothing measurable.

## Why trust never conditioned (Blocker 2, now fixed on main)

| scope | rows | distinct keys | rows per key |
|---|---|---|---|
| `gate_global` | 11,280 | 15 | 752 |
| `mini_exact` | 11,281 | 815 | 13.8 |
| `global_core` | 11,280 | **1,600** | **7.05** |

`global_core` needs 6 samples but generated 1,600 keys in 31 hours, because its
dimension set carried `utc_weekday` and `utc_clock_bucket_15m` — a key can recur only
weekly, so the current key is always new. Every subject fell back to `gate_global`.
Fixed by `_TRUST_GLOBAL_CORE_DIMENSIONS` (8 dims, no clock/weekday).

## The most important open finding: m5 may be inverted

Outcome ledger joined to gate snapshots on `packet_digest`, `gate_global`:

| expert | n | agreed | opposed | rate |
|---|---|---|---|---|
| **m5_price_structure** | 54 | 18 | **36** | **0.333** |
| liquidity_reclaim | 45 | 21 | 24 | 0.467 |
| momentum_impulse | 36 | 18 | 18 | 0.500 |
| m15_price_structure | 34 | 13 | 21 | 0.382 |
| h1_price_structure | 27 | 13 | 14 | 0.481 |

m5's 95% Wilson interval `[0.222, 0.466]` excludes chance, and the inversion is
**symmetric across both call types** (says bullish → bearish 19/32; says bearish →
bullish 17/29), which base-rate bias cannot produce. Likely mean reversion read as
momentum on 5-minute gold structure.

**DO NOT FLIP IT YET.** Six experts were examined; Bonferroni over six widens the
interval to `[0.192, 0.513]`, which includes chance. `gold_expert_directional_skill.py`
(PR #248) measures this on a daily schedule with the rule frozen in advance
(`MIN_DIRECTIONAL_N = 40`, `ALPHA = 0.05` family-wise). Let it accumulate and act when
the family-wise interval excludes chance — not before.

## Isolation from Super Signals — enforced, not assumed

Six contract tests (PR #247) pin it: `Default.fetch` (serves `/provider/context`) does
no learning-loop work; the shadow sync runs only from `scheduled`/`queue`; health
telemetry catches `Exception` and never raises; AIDY binds exactly one datastore
(`AIDY_OPS`); no Super Signals table name appears in AIDY source; AIDY's own Telegram
publisher is imported by no deployed Worker entry.

## What to judge next

After deployment, AIDY will start emitting directions that get **scored**. Judge the
result against **48.46%**, not against zero. If accuracy stays near 38% once trust can
finally condition on environment, the problem is the experts themselves and no amount
of aggregation will fix it.


---

## Previous state (superseded 2026-09-23)

# AIDY — Current State

## READ FIRST — independent audit found the decision layer non-functional — RED (2026-09-22)

An independent adversarial audit of Builds 1-24 at verified SHA `47ffe131b9a8d2180c8d78ba3c1dc1b9253b9e4a` found that **a directional view is practically unreachable in the current production architecture.** Builds 1-24 are BUILT and ENGINEERING PROVEN. The live decision layer is RED.

**Independently verified 2026-09-22** by a second reviewer in a separate read-only run against the same SHA and live D1 (verification run `35687904986`, no production change). All headline numbers confirmed, plus average `directional_total` = **0.004491** against the required 0.30. Two wording corrections from that verification are applied below.

Do not treat the 41/41 abstention as correctly-calibrated newborn caution. It is a permanent arithmetic condition.

Blocking findings (full detail and line references: `projects/aidy/handovers/2026-09-22-independent-24-build-audit.md`):

1. **Meta-direction abstention is arithmetic, not judgement.** `MIN_DIRECTIONAL_WEIGHT` is 0.30; measured live `directional_total` is max **0.016939**, average **0.004491** — short by 18x-67x on every cycle. Build 20's evidence-redundancy ratio (91 raw signal-units collapsed to 4.0 effective) is multiplied into Build 21's confidence chain and then summed by Build 22 against an absolute constant. Units mismatch: dependency should govern *how much independent evidence exists*, not annihilate each expert's reliability. Realistic mature ceiling is **0.179**, still below 0.30.

   **Correction (verified 2026-09-22):** with *perfect* reliability across every directional gate the current formula can just exceed 0.30 (ceiling 0.5137), so this is **practically unreachable, not mathematically impossible**. Earlier phrasing here ("cannot produce a direction at any achievable N", "would still abstain at N=10,000") was too absolute. The operative conclusion is unchanged: no realistic system reaches the threshold.
2. **Environment-conditional learning never runs.** 41 cycles produced **41 distinct `environment_key` values** because `utc_clock_bucket_15m` and `utc_weekday` sit in `GLOBAL_CORE_DIMENSIONS`. `global_core` max N=1 across 570 rows; `mini_exact` max N=3. Every gate falls back to `gate_global`, the environment-blind global average. The programme's central premise is not operating.
3. **Two calibration subsystems are dead code.** `calibration_rows=()` and `meta_calibration_rows=()` are hardcoded empty in the live bundle, so Build 21's calibration multiplier is permanently 0.85 and Build 22 `calibrated_confidence` is permanently `None`.
4. **The two best gates contribute exactly zero.** Gate-level `abstain` receives no directional weight. H1 abstains 29/41, H4 33/41; M5 (31.82%, worst gate) commits 25/41 and dominates. Selection is inverted. H4 has concluded bearish **0 times in 41 cycles**.
5. **D1 and H4 experts are structurally starved.** Verified admitted depth: D1 Context **10 bars**, H4 **42 bars**, H1 156. Daily structure is not derivable from 10 observations. This is the mechanical cause of H4's never-bearish output, and means H4's "57% on N=7" is not evidence of skill. **40,771 M1 bars back to 2026-08-12 already exist** and would fix both experts at zero data cost.

Non-blocking but material: the 135.2-minute gap was **not an outage** (capture ran throughout) but a zero-market-minute H1 bucket misclassified as inadmissible, recurring ~60 min every Mon-Thu (~1,000 cycles/year); **no scheduled workflow or alerting exists** and shadow health is a single overwritten row, so the loop can stop silently; **no baselines are computed** (always-bearish scores 57.9% on the resolved sample, so 36.11% legacy and 31.82% M5 are below both random and majority-class); the hindsight blacklist omits this codebase's own outcome field names.

Verified sound under attack: PIT window discipline (0/41 windows start before their decision), vendor-revision immunity, explainability (630 gate snapshots = exactly 42 cycles x 15 gates, plus 3,742 sub-calculator snapshots), Build 19 analogue no-hindsight design, Build 2 contract enforcement, AIDY/Super Signals isolation, legacy MetaAPI exclusion at the data layer, 1:1 cycle yield, and 1,665 passing tests.

**Test-suite caveat:** the 1,665 tests prove software correctness, not reachability. The meta-direction fixture defaults to `n=100, correct=75` with 1-2 gates in one dependency family; production has N<=23, ~40% accuracy and 91 damped signals. No test asserts a non-abstain direction is reachable under the live graph. Build 23 results that reported non-abstain behaviour should be treated as suspect until re-run.

**Next step is repair, not new data.** Fix order: re-denominate the aggregator; add the reachability test; fix the environment key; wire both calibration paths; backfill H4/D1 aggregates from existing M1; fix the bucket bug and abstain weighting; add cron'd monitoring and health history; add baselines; then soak 2-4 weeks unchanged before any promotion reasoning.

## Expert-gate programme — BUILDS 1-24 BUILT / ENGINEERING PROVEN / DECISION LAYER RED (2026-09-22)

The planned 24-build Gold expert-gate programme is implemented end to end. The audit above supersedes any earlier reading of this section as "complete and working".

**Build 24 — Live Forward Shadow Soak & Permanent Scorecard:** complete and live in research/shadow mode.

Final engineering/live evidence:
- implementation PR #238 tested head `a0b8710abc3fe4ea569deed868ea6538294169ad`;
- implementation merge `6644892d12be6ae497f07db2a69119eaa58e0d27`;
- health-telemetry fix merge `c472d761b25f7c7a91880e2de99d27189bbf43f8`;
- Build-24 acceptance run `35623113260`: PASS;
- semantic gate run `35623113461`: PASS;
- focused/component suite: 103 passed;
- full repository regression: 1664 passed;
- final rollout run `35630952162`: PASS;
- final D1 diagnostic run `35630952252`: PASS;
- health-hotfix deploy run `35630952178`: PASS;
- final semantic verification `35630952012`: PASS.

Overnight prospective proof as of 2026-09-22 03:42 UTC:
- activation: 2026-09-21 16:06:57 UTC;
- 39 prospective shadow cycles frozen;
- 36 outcomes resolved/scored;
- 39 AIDY final views = 39 abstentions because directional authority remains insufficient;
- 20 bearish, 11 bullish and 5 neutral realised outcomes among the 36 resolved cycles;
- all cycles carry 15 expected gate identities: 10 currently live-known, 5 explicit UNKNOWN;
- latest shadow sync health = OK, no error;
- one 135.2-minute cycle gap occurred from 20:55 to 23:10 UTC and the loop recovered automatically;
- old/simple 15-minute view on the same 36 resolved cycles was correct 13 and incorrect 23 (36.11% exact-direction accuracy).

Initial gate-global learning remains small-N and is not promotion evidence:
- H1 structure: N=4, 75.0%, net +3;
- H4 structure: N=7, 57.14%, net +2;
- liquidity/reclaim: N=15, 40.0%, net -4;
- M15 structure: N=12, 41.67%, net -5;
- M5 structure: N=22, 31.82%, net -15;
- momentum/impulse: N=12, 41.67%, net -4.

The five live-unconnected research gates remain explicit UNKNOWN rather than being reconstructed retrospectively: macro/event, rates/USD/cross-asset, futures/microstructure, news/mechanism and analogue/episode.

**Programme state:** BUILDS 1-24 BUILT and ENGINEERING PROVEN; **live decision layer RED** (see READ FIRST above). Permanent prospective shadow capture, resolution and scoring are active. Formal-forward and live-money authority remain OFF. The overnight evidence proves the machinery is capturing, resolving, scoring and accumulating trust without hindsight. It does **not** prove predictive edge, and the 2026-09-22 audit established that the accumulated trust **cannot currently change the meta view at any sample size** — the learning loop closes mechanically but is disconnected from the decision.

## Factual cycle-start environment v2 — LIVE (2026-09-21)

AIDY now freezes a canonical PIT-safe factual environment before each 15-minute Gold cycle and learns marker usefulness **by market condition** rather than one universal tool score.

Live versions:
- cycle environment: `aidy_gold_cycle_environment_v2`
- contextual marker brain: `aidy_gold_contextual_marker_brain_v2`
- cycle memory: `aidy_gold_cycle_memory_v3`
- Worker: `aidy-signals-test`
- Worker version: `240739fb-849e-410f-a805-70a1e4496514`
- successful deploy run: `35565777824`
- final environment audit: `35565912418`

The environment stores exact start-point facts for audit, but learns on repeatable buckets: session/session phase, price location, nearest liquidity/reference distance band, sweep/reclaim state, prior-day/Asia/session range zone, M5/M15/H1/H4/D1 state, recent path, volatility/jump regime, event proximity, cross-market availability and compound regime.

Contextual scorebooks now span **13 scopes**, including liquidity+location, session+liquidity, location+HTF structure and volatility+movement regime. The canonical **34-item toolbox** is still evaluated every cycle; only legitimately directional/PIT-safe evidence is scored.

Live D1 proof for the `2026-09-21T05:45:00+00:00` cycle: Asia late-session, Gold below `asia_opening_30m_low` by the 3-8bp band, prior-day lower-middle zone, low-side reclaim, H1 bearish, H4 bullish, 4 known cross-market series, 34 toolbox items, 13 scopes, future-values=0 and live-money authority=0.

Persistent cycle-sync health is also live and reported `status=ok` at `2026-09-21T05:48:01.095000+00:00`.

The AIDY repo itself now carries its own memory/handoff: root `MEMORY.md`, `README.md` entry point and `docs/current-gold-learning-state.md`. Full handover: `projects/aidy/handovers/2026-09-21-cycle-environment-v2-live.md`.

No execution/provider/risk authority changed; owner 1% risk and formal-forward OFF remain intact.

## Contextual marker-learning brain — LIVE (2026-09-21)

AIDY's 15-minute Gold learner now scores toolbox markers by **environment**, not just globally. Runtime code from `6f9b607c0201bec77f5996126d158914864d58e5` is live on Worker version `a264b7b3-e26a-406f-827f-2ebd7f128740`; repository main after audit cleanup is `a2c029b9954b2b06964b8cd7f1c9d60d35458192`.

The canonical toolbox has **34 capabilities**. Every capability is evaluated each cycle. Directional/PIT-safe surfaces become scoreable markers; contextual or unavailable tools remain explicit rather than receiving fabricated votes.

Marker outcomes are scored `-2/-1/0/+1/+2`: large correct moves (+2), normal correct (+1), unavailable/unscoreable (0), normal wrong (-1), large wrong (-2). Current large-move threshold is `abs(15m return) >= 5 bps`. Plain accuracy is stored separately.

Each score updates seven environment scopes: global, session, session+15m state, higher-timeframe environment, session+move regime, session+state+event, and full environment. Learned weight multipliers are bounded to 0.5x-1.5x and only become more specific as minimum sample thresholds are met.

Immediate live proof: the resolved 04:00-04:15 miss was backfilled automatically. H4 bullish scored **+2**; H1 bearish, two M15 bearish markers, M5 bearish and the movement detector bearish each scored **-2** against the +6.8 bps bullish outcome. D1 showed **6 marker observations, 6 marker results, and 42 contextual score rows (6 x 7 scopes)**.

Provider Context exposes the selected marker profiles and effective learned weights. No execution, provider-rule or 1% risk changes were made. Full handover: `projects/aidy/handovers/2026-09-21-contextual-marker-learning-brain-live.md`.

## Gold cycle learning + auditable toolbox reasoning — LIVE (2026-09-21)

AIDY main `9b23e1c83fd169fb9ad08ded97a1ba4cce59ddee` is deployed to Cloudflare Worker `aidy-signals-test`, Worker version `395ada01-cf5d-4b51-9b4f-fd207e837a6d`. Final canonical deploy run `35559806815` completed successfully with the direct minute cron present, capture enabled, Twelve Data/public-independent, Provider Context routes live, and formal-forward/live-money authority OFF.

The additive 15-minute Gold cycle learner is now live. Every view is frozen before its target window and stores bullish/bearish/neutral/unknown state plus a cross-checkable reason trail: supporting reasons, contradictory reasons, missing/unavailable evidence, toolbox manifest digest, toolbox considered and toolbox actually used. Post-window outcomes attach realised direction, return, MFE/MAE and scoring without rewriting the original reasoning.

Live D1 audit of the `2026-09-21T04:00:00+00:00` view proved: observed bearish, AIDY bearish, **5 supporting reasons**, **1 contradiction**, **33 toolbox capabilities considered**, **5 tool/evidence surfaces used**, **13 unavailable evidence items kept explicit**, `future_values_used=0`, `live_money_execution_allowed=0`.

Historical cycle memory is also loaded: **46,353** retrospective M15 Gold cycle rows from **47,319** BigQuery research-candle rows across 2024-2025, covering **120 distinct state sequences** and **95 UTC time slots**. Safety audit found **0 illegal PIT rows, 0 illegal research flags and 0 illegal live-money rows**. This history is descriptive analogue memory only.

The 15-minute cycle is one learning lens, not AIDY's full specification. Gold-first causal learning remains primary. Known-but-not-yet-live/PIT-connected parts of the wider arsenal remain explicit UNKNOWN, including parts of rates/macro surprise, intraday cross-asset reaction, CME, GVZ and breaking-news/official-release search. Full handover: `projects/aidy/handovers/2026-09-21-gold-cycle-toolbox-learning-live.md`.

## Gold movement capture + canonical toolbox — LIVE (2026-09-21)

The Gold-first movement spine is now live and directly proven in remote D1. AIDY PR #147 (`bbbc9a59d2fcc9fc0fe0fd9bf18dd90091dfd084`) added an immutable scan ledger and bounded backlog scanning so normal and abnormal snapshots are continuously advanced rather than only checking the single latest snapshot. Live audit run `35557600712` found 2 genuine abnormal episodes: **1 UP and 1 DOWN**, both honestly `cause_unknown`. AIDY PR #148 (`5f11c13b86467e72cd178b3c92cb44e813732533`) deployed `aidy_gold_toolbox_manifest_v1`, a 30+ capability catalogue with explicit live/downstream/research-not-connected states. Super Signals PR #240 (`f33a83ffa965b4b42ab2cd579b6012ba85a601f6`) is LIVE on Render deploy `dep-daoaeau8bjmc73b6mmeg`, consumes that catalogue in `aidy_live_toolbox_manifest_v2`, and uses prompt `aidy_reasoning_prompt_v14_gold_toolbox`. Post-deploy Provider Context probe was READY. Learning-card maturity is not yet proven because the first live episodes had not reached the 60-minute forward horizon at audit time. Rates/macro surprise, intraday cross-asset reaction, CME, GVZ and breaking-news tools are known to AIDY but remain explicitly not live/PIT-connected. Full handover: `projects/aidy/handovers/2026-09-21-gold-movement-toolbox-live.md`.


## AIDY Provider Context self-heal — LIVE (2026-09-21)

AIDY main `aebb414656e9e1f6f30f2cf954366085792dca6f` is deployed to the canonical Cloudflare Worker. Deployment workflow run `35557298002` completed successfully at `2026-09-21T03:23:24Z` after lint/test cleanup. Live health is green: direct-cron, capture enabled, Twelve Data/public-independent, formal forward OFF, and both scheduled capture and Provider Context fresh at `2026-09-21T03:22:30.148000+00:00`. The bounded intraday self-heal is live and may repair only small recent <=30-minute M1 gaps needed for M5/M15/H1/H4 while preserving strict evidence and fail-closed behavior. Full handover: `projects/aidy/handovers/2026-09-21-live-self-heal-deployed.md`.


## Actions monitoring cutover — COMPLETE; Provider Context fault later RESOLVED (2026-09-21)

AIDY GitHub Actions monitoring was rationalized in `dannythehat/Aidy-Gold-Signals` PR #140, merged as `09066e085493b2970530adf82577db132164c94a`. Three every-10-minute GitHub schedules plus one hourly schedule were removed, eliminating approximately 13,680 scheduled GitHub workflow launches per 30-day month. The corresponding workflows remain manually runnable. Cloudflare direct-cron remains the canonical AIDY runtime monitor and already records capture, Provider Context, archive and Gold-movement health.

Post-cutover live verification found a separate Provider Context staleness fault at `2026-09-21T01:57:30.150000+00:00`; Super Signals also logged `AidyContextTerminalMiss`. That fault was subsequently repaired by the bounded intraday self-heal and reverified live. See `projects/aidy/handovers/2026-09-21-live-self-heal-deployed.md`. The Actions-cutover handover remains at `projects/aidy/handovers/2026-09-21-actions-monitoring-cutover.md`.


> **Owner mandate in force since 2026-09-17: read [`OWNER_MANDATE.md`](../../OWNER_MANDATE.md) every session.** It sets the goal (AIDY becomes an evidence-scored decision layer that measurably improves Super Signals' profit) and the one boundary that does not move under it (live-money authority stays OFF until explicitly graduated per class).

Last verified: **2026-09-21**

Authoritative repo: `dannythehat/Aidy-Gold-Signals`
Authoritative branch: `main`
Verified repository `main` SHA: `1635f68a4ed98298f979d6d13521c21c1b0e4463`
Live Worker: `aidy-signals-test`

## Toolbox-aware decision layer + measured historical exam — ACTIVE (2026-09-20)

Super Signals reasoning now carries an explicit AIDY toolbox contract. Production reasoning prompt
`aidy_reasoning_prompt_v12_toolbox` requires AIDY to read `toolbox_manifest`, consider every
available standing evidence surface, call an on-demand tool when it can materially resolve a
take/reduce/reject uncertainty, avoid meaningless checklist calls, and preserve UNKNOWN when a
surface is unavailable or not connected.

Connected on-demand surfaces are candles and economic calendar in live reasoning; the historical
stress lab additionally has a focused evidence inspector. Standing evidence includes provider
history, Gold/market context, recent provider messages, event/liquidity/execution context,
historical analogues/provider alpha, probability/EV/management context, and failure/self-critique.
Broader AIDY modules such as rates/macro vintages, cross-market, CME contract state, GVZ/volatility,
semantic context and provider decision memory are NOT to be falsely treated as callable until an
auditable adapter makes their timestamp/provenance semantics valid. Their unavailable state is
explicit in the manifest.

Production Super Signals commits:
- PR #228 `521b4c9002f7ffa22aae54a585c6edfbd5b10e53`: historical toolbox
- PR #229 `134a81d79fe88d6b2343a08e657d6307a1d30402`: toolbox-aware prompt/live manifest
- PR #230 `36dee29f4b87dfe2f94bb02ea19f21c612b363d4`: historical manifest-key alignment
- PR #231 `e92c46f92d7c9679066fbdbbb1bd46dd281d4029`: exact tool-name telemetry, stress replay `aidy_historical_stress_lab_v7_tooltrace`
- PR #232 `5b09fea3f7707a8f752c888f187c99c1a531f8e7`: independent 571-case training identity freeze
- PR #233 `f85a0456d1d0cf566c4b6eb4ecdc0c3722e22abb`: reconstructed-stress DB schema expansion; first deploy rolled back safely on scoreboard-view dependency
- PR #234 `745b5af537cd0028535cb5e7400255b49d101156`: corrected transactional migration; live Alembic head `0108_aidy_hist_stress_schema`, Render gate 1,191 passed / 137 skipped

The active train identity is 571 cases, SHA-256
`18326c515d12a7e55046828f6fe59198de50b0b7538193174528bf56f7829168`.
Validation and OOS remain sealed. Three late historical rows now make the dynamic source query
571/70/162, but they are not admitted into the original frozen 571/69/160 evaluation design.
The 18-case exact holdout remains sealed.

Full handover:
`projects/super-signals/handovers/2026-09-20-aidy-toolbox-awareness-training-stress.md`.

## Large historical acceleration lab — MERGED / RESEARCH OFF PENDING TRAIN RUN (2026-09-20)

The owner explicitly directed a full AIDY audit and historical acceleration programme. Super Signals
now contains a separate **803-source / 800-scoreable reconstructed research stress lab** over older resolved XAUUSD
provider trades: **571 train / 69 validation / 160 research-OOS**, with 3 source cases excluded because no resolvable provider trade score exists. The official exact-PIT
**18-case holdout remains sealed and separate**.

Hardening found and fixed real gaps before any training claim: the original 650-call ceiling could
not cover all OOS cases; evaluation partitions were insufficiently locked; historical reasoning had
no candle tools; and the large replay lacked reconstructed as-of provider memory. PRs **#221-#223**
are merged; latest implementation SHA is
`25d6cea1dc7dd127e9890b0363148f1732557da4`.

The current replay can use retrospective-research 1/5/15/30/45/60-minute candles, conservative
official scheduled-event timing, recent provider messages, prior-resolved analogues, and
provider-specific overall/side/session evidence known before each target signal. All reconstructed
evidence remains explicitly non-PIT/research-only and cannot grant live authority.

Training protocol is fixed: 571 train first; tune only there; freeze; 70 validation without tuning;
freeze; 162 research-OOS; only then final exact-PIT holdout. See
`projects/super-signals/handovers/2026-09-20-aidy-large-historical-stress-lab.md`.

## Automatic forward acceptance monitor — LIVE

Built and deployed 2026-09-19 so Phase 1 no longer depends on a manual Monday check.

Production Super Signals SHA: `ec7febbdaa2fbd6444eae58a0873769943c5e89b`; Render deploy: `dep-dan2kgdii2qc73bhsi50`;
Alembic: `0105_aidy_grounding_accept`.

The monitor is **observational only**. It reads evidence-v2 AIDY reasoning rows, validates the
frozen evidence contract again, and writes a research-only acceptance ledger. It has no broker,
execution, sizing, provider-status or live-money write path.

It checks:

- evidence contract is exactly `aidy_reasoning_evidence_v2`;
- claim validation already passed and unsupported count is zero;
- every provider claim ref exists in the frozen evidence snapshot;
- no duplicate claim refs/claim IDs;
- source/path/sample/version provenance is present and valid;
- provider evidence timestamps are never later than the signal timestamp;
- provider-profile claim versions match the frozen profile version on the annotation;
- prohibited free-form provider-history language did not escape into rationale/key factors/action reason.

State machine:

- `waiting_forward_rows` — no fresh evidence-v2 decisions yet;
- `clean_so_far` — fresh rows exist and all are clean, but acceptance sample is not yet complete;
- `accepted` — at least 10 clean rows across at least 2 providers;
- `failed` — any audited row violates the contract.

Initial live state: `waiting_forward_rows`, 0 invalid rows, research_only=true,
live_money_execution_allowed=false.

Exact deploy acceptance: **1113 API tests passed, 137 skipped, 2 warnings**; web suite and
secret scan also passed. Public API and website proxy still respond after deploy.

## Phase 0/1 anti-drift — PRODUCTION VERIFIED / WAITING FOR FORWARD ROWS

Verified 2026-09-19 against the deployed Super Signals runtime.

The evidence-grounding/anti-drift layer is now deployed in the signal-level AIDY reasoning
path. Production Super Signals SHA: `33305a020f96e545990906a6de0c5dc253e9fcaf`; Render deploy:
`dep-dan2cv5ii2qc73bhmpig`; Alembic: `0104_aidy_grounding_health`.

Engineering acceptance on the exact deployed build:

- API suite: **1105 passed, 137 skipped, 2 warnings**.
- Web suite: **28 passed**.
- secret scan: PASS.
- Render `/health`: healthy after deploy.
- origin and website public-performance endpoints: responding after the post-deploy startup
  settled.
- AIDY live-money authority: unchanged/OFF.
- Super Signals owner risk: unchanged at 1%.

What is now enforced:

- provider history reaches the model only as versioned, PIT-safe atomic claims;
- every claim carries the exact source path/value/sample N/version/evidence timestamp;
- side-performance evidence is scoped to **this signal's side**;
- session-performance evidence is scoped to **this signal's session**;
- a missing BUY/SELL/session cohort remains UNKNOWN and cannot be inferred from an opposite
  cohort;
- provider identity and raw provider profile/fingerprint text are not sent to the model;
- provider-history prose is rejected outside validated `provider_claim_refs`;
- unsupported claim references fail safe and are not persisted as successful reasoning;
- every new grounded annotation freezes the exact evidence snapshot and claim references;
- production grounding health is queryable through
  `aidy_reasoning_grounding_health`.

Legacy audit at deployment: 2674 historical reasoning annotations are explicitly
`legacy_unvalidated`; 2227 contain language the stricter detector marks for review. That
number is **not** a count of proven false claims. It means those rows predate the evidence-ref
contract and therefore cannot be granted grounded status retrospectively.

Forward acceptance is correctly still **WAITING**: the market is in the canonical weekend
closure and there are currently 0 new `aidy_reasoning_evidence_v2` forward annotations.
The next acceptance is mechanical: on the first fresh eligible signals, require
`claim_validation_status=passed`, `unsupported_claim_count=0`, and inspect the exact frozen
claim/evidence pairs. Do not advance the programme past Phase 1 acceptance before this check.

## Current production status — HEALTHY, multi-cycle verified

The 16 September `stale_provider_context` state is resolved and deployed. Verified not by
a single startup probe but by 53 consecutive `complete` market snapshots (zero `partial`)
across 4+ hours on 2026-09-17 — see
`projects/super-signals/handovers/2026-09-17-continuous-health-verification.md` for the
full cross-system evidence (AIDY D1 ground truth, Super Signals resolver progress, log
window, live health check).

Live Worker health as of last check:

- runtime: `cloudflare-workers`
- scheduler: `direct-cron`
- `capture_enabled=true`
- market source: `twelve_data`
- market ownership: `public_independent`
- `formal_forward_enabled=false`
- `data_health.status`: `fresh`
- `provider_context_snapshot_lag_seconds`: ~150 (fresh, well under the 10-minute cutoff)

No known active health failure.

## PR #133 — MERGED

PR #133 `Keep Provider Intelligence alive when only D1 context is missing` was merged on 16 September 2026.

Verified PR head before merge:

`01c6a955c5c7c513a6db86f70cdc2e7d146ea246`

Merge commit now on `main`:

`0a6230e606282dca97675d63117c4d24dcc38120`

Exact current-head acceptance performed outside GitHub Actions before merge:

- Ruff: PASS
- compile: PASS
- focused Provider Context tests: **33/33 PASS**
- full repository suite: **1270/1270 PASS**

Safety boundary independently checked:

- Provider Context keeps `live_money_execution_allowed=false` hardcoded/unconditional.
- Formal forward keeps its own separate untouched complete-snapshot gate in `forward_live_observer.py`.

## GitHub ruleset state during recovery — resolved

Ruleset `Protect main` id `22096458` was temporarily edited by the owner (Claude has no
ruleset-read/write tool in this environment — confirmed directly by a failed `merge_pull_request`
attempt returning `405` citing the required-check rule, with no admin-bypass path through the
merge API either) so the unavailable GitHub Actions required-check rule no longer blocked
merging PR #133. Deletion protection, force-push protection and the pull-request requirement
stayed active throughout.

## Recovery actions — all complete, verified 2026-09-17

1. Required-status-check protection: restored by the owner.
2. `main` commit `0a6230e606282dca97675d63117c4d24dcc38120` deployed to the canonical Worker
   via `.github/workflows/aidy-provider-research-read-deploy.yml` once Actions capacity
   returned — not a direct Cloudflare/Wrangler session; that workflow is the deploy path,
   and it ran successfully. Confirmed by reading the deployed Worker source directly
   (`workers_get_worker_code`): it contains `aidy_provider_context_api_v2` and
   `intraday_complete_d1_missing`, the exact PR #133 markers.
3. Deploy preserved `* * * * *` direct Cron, capture ON, Twelve Data/public-independent
   ownership and `AIDY_FORMAL_FORWARD_ENABLED=false` — asserted by the deploy workflow itself
   and independently confirmed live.
4. Cloudflare schedule state verified post-deploy.
5. `/health` confirmed `data_health.status: fresh`, no `stale_provider_context`.
6. Super Signals confirmed receiving current AIDY context across 53 consecutive cycles — see
   `projects/super-signals/handovers/2026-09-17-continuous-health-verification.md`.

## Phase 2 Gold State Engine v1 — BUILT IN ISOLATION / NOT YET GRADUATED

Built 2026-09-19 on isolated branches while the Phase 1 anti-drift forward gate remains
`waiting_forward_rows`.

Standalone AIDY branch: `feature/gold-state-engine-v1`, head
`709d7702ec7b479d86ff8f8289d095bad8045cf0`, PR #137.

Super Signals consumer branch: `feature/aidy-gold-state-v2-reasoning`, head
`f6e1e42ecb8ff18b153912915588f4c6945711b6`, PR #208 against the production branch. **Do not merge PR #208 until
Phase 1 forward grounding is accepted.**

Gold State Engine v1 now composes a deterministic PIT-only XAUUSD dossier with:

- completed-bar M1/M5/M15/H1/H4 close-path structure;
- named session state;
- observed prior-day, Asia overnight, named-session and opening-range location/distance;
- explicit descriptive round-number references with no predictive-edge claim;
- liquidity penetration/reclaim **proxies**, explicitly not hidden order flow;
- PIT realised-volatility/jump context where qualified;
- five-minute displacement and five-minute range expansion/compression versus prior
  non-overlapping completed five-minute blocks;
- scheduled-event timing context when known;
- explicit `cause_unknown` for elevated/extreme moves because Phase 2 does not claim
  causality;
- explicit UNKNOWN surfaces and deterministic packet digest.

The engine is hard-coded `research_only=true`, `descriptive_context_only=true`,
`predictive_edge_claimed=false`, `live_money_execution_allowed=false`,
`future_values_used=false`.

Super Signals production was changed only to accept both Gold State v1 and v2 safely before
the isolated build. Production SHA `4650d2074ea4d4287285783a5157d4340cd41e8a`, Render deploy
`dep-dan2p2dii2qc73bi09h0`, **1116 API tests passed, 137 skipped, 2 warnings** plus web/security
gates. The isolated PR #208 adds stricter v2 validation and prompt semantics but is not live.

GitHub Actions remain credit-exhausted: PR jobs terminate in seconds with no job steps/logs,
matching the already-documented account condition. Therefore PR #137 and #208 are deliberately
not merged/deployed and no false green-test claim is made for the isolated heads. Static blast
radius is bounded to Gold-state/provider-context/reasoning files and tests; repository compares
show no broker/execution/sizing/provider-status files touched.

Current production remains unchanged: standalone Worker health `ok`, capture enabled,
formal-forward OFF, Twelve Data/public-independent; Phase 1 acceptance still
`waiting_forward_rows`, 0 invalid rows, research-only, no live-money authority.

## Approved next build — Master Gold Intelligence

Owner and ChatGPT aligned on 2026-09-19 that AIDY's destination is a full Gold specialist,
not merely a provider scorer. The detailed build/test contract is now pinned at
`projects/aidy/MASTER_GOLD_INTELLIGENCE_BUILD.md`.

Core new requirements:

- explain abnormal Gold moves from point-in-time evidence and distinguish known mechanism
  from plausible narrative;
- attribute trade failures without hindsight storytelling;
- treat liquidity/execution quality, MFE/MAE and profit extraction as first-class learning;
- match historical setups by regime and outcome distribution, not visual similarity;
- learn provider edge conditionally by side/session/regime/management/event state;
- require every provider-specific rationale claim to be evidence-addressable;
- maintain an explicit UNKNOWN state and learn what evidence is missing;
- add breaking-news/event intelligence, but only as a qualified context mechanism;
- move toward calibrated probabilities/expected value and measure whether TAKE/REDUCE/HOLD/
  REJECT/NO-TRADE decisions actually improve counterfactual value;
- continuously ablate features and remove complexity that does not add forward value.

Architecture boundary remains unchanged: AIDY market/research stays separate from Super
Signals broker execution; AIDY live-money authority remains OFF until separately graduated.

## New central product direction — decision intelligence

Once Provider Context is healthy, AIDY should begin producing a shadow decision for every eligible Super Signals provider trade.

Target decision classes:

- `APPROVE`
- `DENY`
- `HOLD/NO_SECOND_ENTRY`
- `CONFLICT_DENY`
- `CLOSE_EARLY`
- `CONTINUE`

Target pipeline:

`provider signal -> PIT-safe market context -> provider history -> current exposure -> AIDY decision -> action -> outcome -> counterfactual score -> learning`

AIDY must prove whether its intervention made or saved money versus the fixed baseline that would otherwise have occurred.

## Reuse what already exists

Do not create a parallel system. Existing Super Signals infrastructure already provides substantial foundations:

- `provider_trade_observations`
- `provider_trade_scorer.py` + `provider_trade_scores`
- `provider_trade_scoreboard`
- `canonical_signal_ledger.py` + `signal_events.py`
- `provider_day14_governance.py`
- `provider_day18_combined_book.py`

Genuinely new or incomplete pieces include the persistent hypothesis/question registry and cross-provider duplicate/exposure clustering. Add a small immutable AIDY decision layer on top of the existing observation/scoring spine rather than rebuilding capture or scoring.

## Authority graduation

Likely sequence:

1. deterministic duplicate rejection
2. obvious duplicate/conflicting exposure controls
3. provider/regime denies
4. early-close management
5. broader approve/deny/management authority

Each authority class requires an audit trail, kill switch, prospective evidence and explicit owner/live gate. The current Super Signals 1% risk directive must not silently change.

## Session rule

Read `OWNER_MANDATE.md` first, then verify the current AIDY repo, Worker health and Super Signals production state directly. Source/runtime truth overrides Memory if it has advanced.

## Gold-first causal learning mandate — 2026-09-20

Owner correction: AIDY must be developed as a **Gold intelligence system first, provider filter second**.

Primary loop:
`detect Gold move -> investigate evidence-backed cause/mechanism -> observe continuation/reversal -> store structured movement episode -> retrieve analogues -> form independent Gold view -> compare with provider call -> score economic value.`

This supersedes any testing interpretation that only asks how much of a provider trade AIDY kept.
Historical/live evaluation must separately credit:
- avoiding a losing provider trade;
- reducing a genuinely bad provider trade;
- preserving profitable provider trades;
- an independently emitted opposite-direction Gold hypothesis when it was frozen before outcome;
- abstention/no-trade.

No hindsight and UNKNOWN discipline remain mandatory. Live-money authority remains OFF until separately graduated.

Canonical detailed contract: `projects/aidy/MASTER_GOLD_INTELLIGENCE_BUILD.md`.


## Gold-first build implementation — 2026-09-20

Implemented and merged in standalone AIDY:
- Merge SHA: `f2f809bdd1610d4b16166160bca6a43ceb19322b`
- Gold State Engine v1 remains the descriptive PIT market-state base.
- Added `aidy_gold_movement_investigator_v1`: abnormal Gold displacement/range/jump triggers an evidence-backed investigation with explicit supported/plausible/unknown attribution and missing-evidence requests.
- Added `aidy_gold_movement_memory_v1`: Gold movements are learned independently of provider signals. Abnormal movement episodes are frozen, deduped, and after a 60-minute forward window receive immutable continuation/reversal/mixed learning cards.
- Added D1 migration `0021_gold_movement_memory.sql`.
- Provider Context exposes the verified movement investigation inside Gold state.
- Cloudflare provider deploy workflow now applies D1 migrations, tests investigator/memory modules, and verifies investigator/memory health versions.

Deployment truth at handoff: GitHub Actions did not start after the merge because the account Actions capacity is exhausted. Therefore the standalone AIDY merge is in `main`, but its new Cloudflare Worker/D1 rollout is NOT yet proven live. Do not describe merged code as deployed until the Worker health response shows the new movement investigator/memory versions.

Gold-first rule remains: AIDY forms an independent Gold view first, provider signal second; no live-money authority was added.


## Gold-first build final deployment status — 2026-09-20

Do NOT mark the Gold-first architecture fully complete yet.

- Standalone AIDY Gold-first brain code is merged to main at `f2f809bdd1610d4b16166160bca6a43ceb19322b`.
- GitHub Actions returned no workflow runs for that merge, so Cloudflare Worker/D1 deployment of the new Gold Movement Investigator + Movement Memory is NOT yet proven live.
- The code exists and is merged; deployment remains the blocker.
- Super Signals may safely consume the older Gold-state packet until the standalone provider context v5 rollout is proven live.
