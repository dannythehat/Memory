# AIDY large historical stress lab — architecture/audit handover

Date: 2026-09-20

## Owner directive

The owner explicitly asked for AIDY to be audited and strengthened using as much stored historical
Gold/provider data as can be used honestly, rather than waiting months for forward learning. The
goal is to maximise decision quality, wins and loss avoidance while keeping current live execution
untouched until evidence proves a change.

## Repositories audited

- `dannythehat/Memory`
- `dannythehat/Aidy-Gold-Signals`
- `dannythehat/super-signals`

Authoritative Super Signals deploy branch remains
`feature/day-10-shared-telegram-sources`.

## What the audit found

The five-build exact-PIT Time Machine was technically sound but deliberately frozen at only 140
cases (103 development / 19 validation / 18 sealed holdout). That is an exam cohort, not the full
historical learning corpus.

Super Signals already had a much larger usable historical spine:
- 36k+ provider trade-observation rows had existed in production;
- 2,598 historical approve decisions had already been reasoned over by the live reasoning backlog;
- 1,700+ provider trades had been resolved/scored in prior production evidence;
- after strict deduplication/eligibility requirements, the large reconstructed stress cohort is
  exactly 803 unique resolved executable XAUUSD provider messages.

Frozen reconstructed split:
- research_train: 571
- research_validation: 70
- research_oos: 162

The official exact-PIT 18-case holdout remains separate and sealed.

The first 803-case stress-lab implementation had four material gaps:
1. lifetime cap was 650 decisions, so only 9 OOS cases would remain after 571 train + 70 validation;
2. validation/OOS could be exposed too easily by one broad scope setting;
3. historical AIDY reasoning had no on-demand tools even though live AIDY can call candle/calendar
   tools;
4. reconstructed cases did not carry a proper as-of provider track record.

A fifth gap was confirmed in the wider architecture: several Day 28-31 research components exist in
AIDY's repo, but the live provider-context endpoint still marks rates/macro vintages, tiered macro
events and CME contract state as not operational. Existing code is not treated as live evidence
merely because it exists.

## Work merged

### PR #221 — initial 803-case stress lab

Merged as `722bdd7872ad899ac4b0e7cf278b1ffe9381457e`.

Created a separate reconstructed-research lab over 803 old provider trades. It is disabled by
default, research-only, uses the existing replay tables under separate contracts, and cannot write
to broker/execution paths.

### PR #222 — hardening + retrospective candle tools

Merged as `6987732dc99124442847d7114b37de3dc181a428`.

Changes:
- max-call capacity raised to the full 803 cohort;
- exact expected partition counts frozen;
- validation and OOS separately locked by explicit flags;
- retrospective candle tool added for 1/5/15/30/45/60-minute XAUUSD candles;
- tool uses `fetch_research_m1`, never the live/PIT market endpoint;
- tool windows end at/before the historical signal;
- every tool result says retrospective/research-only, PIT-ineligible, decision-ineligible;
- replay namespace bumped so an earlier partial run cannot mix with the hardened run.

### PR #223 — historical event timing + provider memory

Merged as `25d6cea1dc7dd127e9890b0363148f1732557da4`.

Changes:
- conservative official historical schedule surface for verified Aug/Sep 2026 events;
- sources include BLS, BEA, US Census, Federal Reserve and ISM official schedules/pages;
- no realized event value, surprise, actual, or hindsight outcome is supplied;
- forecast/previous are intentionally blank when they cannot be proven;
- calendar is labelled `retrospective_official_schedule`, never exact PIT;
- reconstructed provider overall/side/session evidence is built only from prior trades whose
  result-known timestamp is <= the target signal time;
- provider history stays behind validated claim refs;
- the existing one-retry fail-closed claim validator now preserves historical candle tools during
  retry;
- stress input/replay versions bumped again so richer inputs cannot mix with prior exams.

Current stress contracts:
- replay: `aidy_historical_stress_lab_v4_provider`
- input: `aidy_historical_stress_input_v3_provider`
- market: `aidy_historical_stress_market_v1`
- provider evidence: `aidy_historical_provider_evidence_v1`
- calendar: `aidy_historical_official_schedule_v1`

## Safety boundary

All historical stress rows remain:
- `research_only=true`
- `live_money_execution_allowed=false`

No changes were made to:
- broker execution;
- owner/member risk sizing;
- provider promotion/status;
- canonical settlement/management;
- live-money AIDY authority.

The official 18-case exact-PIT holdout still has zero stress-lab authority and remains separate.

## Required training protocol

Do not tune on all 803 cases.

1. Run only 571 `research_train` cases.
2. Diagnose where AIDY helped/harmed versus provider-taken baseline:
   action, provider, side, session, event proximity, trend, volatility, geometry, analogue evidence,
   provider-evidence sample size and tool usage.
3. Make candidate improvements from training only.
4. Bump/freeze the input/replay/model/prompt version for every material change.
5. Open the 70 validation cases only after the candidate is frozen.
6. Do not tune to validation failures.
7. Freeze again, then open 162 research-OOS.
8. Only after that process is complete should the official 18-case exact-PIT holdout be used as the
   final untouched exam.

AIDY is not considered improved merely because training P&L rises. A useful candidate must
generalise and reduce avoidable loss without systematically clipping profitable provider trades.

## Current execution status

The research runtime remains disabled by default after merge. No historical model calls from the
new v4-provider stress contract have been claimed as completed yet in this handover.

The next operational step is to query the Render Postgres state, confirm deployment/migrations,
enable the stress runtime for `train` only, run/score the 571-case cohort, and analyse the
resulting decision-level evidence. Validation/OOS must remain locked during that phase.

This handover is the Memory completion gate for the historical-stress architecture module.
