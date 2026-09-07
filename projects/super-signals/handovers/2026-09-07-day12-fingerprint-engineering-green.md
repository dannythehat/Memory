# Super Signals Day 12 — FINGERPRINT CORE + HIERARCHICAL STATISTICS HARNESS

Date: 2026-09-07
Status: **ENGINEERING GREEN / PRODUCTION VERIFIED — statistical authority WAITING-FOR-FORWARD-EVIDENCE**

## Production proof

- Super Signals PR: `#147`.
- Delivery head: `5eb27148bdbd1512e01269746578d86fb2a3d519`.
- Delivery-head checks: `api` success, `web` success, Workers success.
- Production merge SHA: `d48a81744af6dda5e644b929d713d3d1ec95c6d3`.
- Render deploy: `dep-daf8spc9v7es73bpqd30` — `live`.
- Alembic head: `0061_provider_day12_fingerprint`.
- New Render instance `/health`: repeated 200 responses.
- Production fingerprint run: `92c29d7a-fd65-41ad-bacc-fa082666d870`.
- Evidence digest: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.

## What Day 12 built

The harness computes research fingerprints for the 40 shadow discovery providers only, never the five testing/real calibration providers. Admission requires closed paper evidence that is both `score_eligible` and PIT-resolved (`provider_profile_pit_status='resolved'`).

Fingerprint dimensions:

- provider;
- provider × BUY/SELL direction;
- provider × session;
- provider × direction × session.

Fingerprint metrics:

- TP hit rates;
- stop rate;
- break-even rate;
- duration;
- MAE in R;
- MFE in R.

The primary statistical surface is deterministic empirical-Bayes hierarchical partial pooling with posterior estimates and 95% intervals. Raw per-cell rates/means are persisted only as descriptive values and are not the primary decision statistic.

The explicit minimum forward N is `30`. Day 12 database constraints hard-wall statistical status to `WAITING-FOR-FORWARD-EVIDENCE`, `research_only=true` and `live_money_execution_allowed=false`; this harness cannot grant broker, sizing, provider-routing or AIDY authority.

## Real production state

Run `92c29d7a-fd65-41ad-bacc-fa082666d870` completed with:

- model version: `provider_day12_v1`;
- primary estimate: `posterior_partial_pool`;
- engineering status: `ENGINEERING_PROVEN`;
- statistical status: `WAITING-FOR-FORWARD-EVIDENCE`;
- provider population: **40 shadow discovery providers**;
- eligible forward trades: **0**;
- fingerprint cells: **0**;
- minimum forward N: **30**;
- research-only: `true`;
- live-money authority: `false`.

This zero-evidence result is correct. The existing closed shadow outcomes do not currently clear the previously-established forward/PIT fairness eligibility gates, so Day 12 deliberately creates no fake 0/0 cells and makes no statistical claim from them.

## Safety / cost boundaries

- No `broker_deals` input.
- No MetaAPI/live execution call.
- No live-money mutation.
- No provider activation/routing/sizing mutation.
- No AIDY/D1 write.
- The Day 11 historical calibration runner was removed from Render startup now that Day 11 is closed.
- The Day 12 deployment therefore did not consume additional D1 row writes after the owner's 93% daily free-tier write warning.

## Acceptance interpretation

**Day 12 engineering is GREEN and production verified.**

**Day 12 statistical authority is NOT GREEN; it is correctly `WAITING-FOR-FORWARD-EVIDENCE`.** This is the pre-registered expected state until enough genuinely forward eligible evidence exists. Engineering completion must never be confused with a statistical claim.

## Exact next step

No further Day 12 engineering work is required. Let forward PIT-resolved, score-eligible shadow evidence accumulate under the existing safety gates. Day 13 is **NOT STARTED** and requires explicit owner instruction.
