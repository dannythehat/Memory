# Super Signals Day 13 — CONDITIONAL FINGERPRINTS + PREREGISTRATION + BH FDR

Date: 2026-09-07
Status: **ENGINEERING GREEN / PRODUCTION VERIFIED — statistical authority WAITING-FOR-FORWARD-EVIDENCE**

## Production proof

- Main Day 13 PR: `#148`.
- Main delivery head: `987e2cfe1602a81284c4c620ca0103c687a85e86`.
- Main delivery-head checks: `api` success, `web` success, Workers success.
- Initial Day 13 merge SHA: `db5f026a5a289a2c634a8c4037e56ca1072f552c`.
- Migration applied: `0062_provider_day13_conditional`.
- Runtime schema hotfix PR: `#149`.
- Hotfix head: `80c2e6e1713d8f1a542814e878a706fe268977ea`.
- Hotfix-head checks: `api` success, `web` success, Workers success.
- Final production merge SHA: `e4afce8207933339e6745478363228dc75154d51`.
- Render deploy: `dep-daf9ipuq1p3s73dn6kn0` — `live`.
- New Render instance repeatedly returned `/health` 200.
- Production Day 13 run: `717adf78-f8a0-4934-b766-91e15431bb0a`.
- Evidence digest: `8b6873c76b2c1cee5a37866a2048d967865be189ec26e526a0673b88ed61a7ea`.

## What Day 13 built

Day 13 extends the Day 12 shadow-only statistics harness with conditional fingerprints and explicit confirmatory governance. It is limited to the 40 shadow discovery providers and cannot grant broker, provider-routing, sizing or live-money authority.

The preregistered condition space is the cross-product of:

- provider;
- BUY / SELL;
- Super Signals session bucket: `asia`, `europe`, `ny_early`, `other`;
- fixed realized-duration bucket: `<15m`, `15m–60m`, `1h–4h`, `>=4h`;
- one known canonical AIDY `aidy_gold_regime_v1` facet value across trend, volatility, quote/spread condition and event timing.

`unknown` AIDY regime labels are not guessed into confirmatory evidence. Duration is explicitly a realized descriptive post-entry axis and must not be represented as a signal-time predictor.

The resulting registry contains **15,360** unique hypotheses for the **40** shadow providers. All 15,360 were frozen at the same timestamp, `2026-09-07T10:50:52.042190Z`, and all 15,360 preregistration digests are unique. The preregistration timestamp is the OOS boundary: evidence at or before it cannot test the hypothesis.

## Statistical governance

The primary conditional estimate is the existing shrunken empirical-Bayes partial-pooling R estimate. Raw R differences remain descriptive only.

The builder-proposed confirmatory gates are:

- minimum OOS N: `30` in both cell and matched complement;
- one global Benjamini–Hochberg family: `provider_day13_v1_global`;
- proposed FDR `q=0.05`;
- proposed minimum absolute shrunken effect: `0.25R`.

These thresholds are deliberately stored as `PROPOSED_UNAPPROVED`. They do **not** constitute owner-approved statistical authority. Database constraints keep real conclusions fail-closed at `WAITING-FOR-FORWARD-EVIDENCE` and `authoritative_discovery=false`.

A deterministic synthetic acceptance uses a known-signal family and a pure-noise family. Production recorded `simulation_acceptance_passed=true`, proving the engineering path can recover the planted signal while not creating a candidate from the fixed pure-noise fixture. Synthetic acceptance is engineering proof only, not provider evidence.

## Production runtime correction

The initial PR `#148` deployed successfully and committed the immutable preregistration before reading outcomes. Its first research run then failed closed because the observation loader referenced `provider_signal_context_attachments.context_as_of_utc`, while the canonical production field is `aidy_context_as_of_utc`.

PR `#149` fixed only that persisted-schema binding through the Day 13 production wrapper. It did not change the preregistration, minimum N, FDR, effect-size gate, partial-pooling model, provider population or authority semantics. The original `10:50:52.042190Z` OOS boundary remained intact; the hotfix did not move it forward.

## Real production state

Run `717adf78-f8a0-4934-b766-91e15431bb0a` completed with:

- code SHA: `e4afce8207933339e6745478363228dc75154d51`;
- evidence cutoff: `2026-09-07T11:01:52.956320Z`;
- completed: `2026-09-07T11:03:05.742506Z`;
- model: `provider_day13_v1`;
- registry: `provider_day13_preregistered_v1`;
- engineering status: `ENGINEERING_PROVEN`;
- statistical status: `WAITING-FOR-FORWARD-EVIDENCE`;
- threshold status: `PROPOSED_UNAPPROVED`;
- provider count: **40**;
- preregistered hypotheses: **15,360**;
- eligible OOS trades after the frozen boundary: **0**;
- result rows: **0**;
- tested hypotheses: **0**;
- BH rejections: **0**;
- builder-gate candidates: **0**;
- authoritative discoveries: **0**;
- simulation acceptance: **passed**;
- research-only: `true`;
- live-money authority: `false`;
- failure reason: `null`.

Zero real tests is correct immediately after preregistration. Existing history is deliberately not recycled as confirmatory OOS evidence, and the harness does not manufacture empty statistical result rows.

## Safety boundaries

- 40 shadow providers only; five testing/real providers excluded.
- Closed, score-eligible, PIT-resolved shadow evidence only.
- Attached AIDY context must be no later than the provider signal timestamp.
- No `broker_deals` input.
- No MetaAPI/live execution call.
- No provider activation/routing/sizing mutation.
- No live-money authority.
- No AIDY/D1 write.
- No owner approval was granted for the proposed statistical thresholds, so `DECISIONS.jsonl` requires no new authority decision for this build.

## Acceptance interpretation

**Day 13 engineering is GREEN and production verified.**

**No Day 13 real provider statistical conclusion is validated.** Statistical authority is correctly `WAITING-FOR-FORWARD-EVIDENCE` until sufficient genuinely post-preregistration evidence accumulates and any required governance approval is explicitly made.

## Exact next step

No further Day 13 engineering closure work is required. Preserve the frozen registry and let genuinely post-preregistration, PIT-resolved, score-eligible shadow evidence accumulate. Day 14 is **NOT STARTED** and requires separate owner instruction.
