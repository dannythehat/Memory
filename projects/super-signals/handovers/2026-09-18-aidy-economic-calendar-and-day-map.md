# AIDY gets a real economic calendar tool, then a standing daily day-map (v3 -> v3b -> v4)

**Date:** 2026-09-18
**Repo:** `dannythehat/super-signals`
**Branch:** `feature/day-10-shared-telegram-sources`
**PRs:** 201 (calendar tool), 202 (standing day-map), both merged, both deployed
**Verified SHAs:** `bd731fac83ddf160709f326c848cb99263052fed` (PR 201), `e27e2e12de69689c8b64a24f9fa10fbe5c4260a6` (PR 202)
**Verified deploys at merge time:** `dep-damc5kbncjis73der750` (PR 201), `dep-damc8p97lnhs73c6nnq0` (PR 202) -- both confirmed built and went live clean, both since superseded by later same-night deploys (see "Gap found on return" below).

## Context

Direct continuation of `2026-09-18-aidy-candle-tool-calling.md`. That handover closed with: *"Owner asked to pick a free economic calendar source: recommended Finnhub... Waiting on the owner to sign up and hand over the API key."*

## What happened with the Finnhub key

The owner sent what looked like three different, garbled API key pastes across several messages, plus a screenshot of the Finnhub dashboard after "stop being a clown" -- the actual cause was a 40-character key getting visually truncated in a narrow mobile input box, not three different keys. Re-tested the full concatenated string and got a real `200`.

With a confirmed-valid key in hand, **tested the actual endpoint needed before building on it**: `GET /calendar/economic` returned `403 "You don't have access to this resource"` on the same key that returned `200` on `/quote` and `/calendar/earnings`. Finnhub's economic calendar specifically requires a paid plan -- the prior session's recommendation was wrong for this endpoint. Corrected this to the owner directly rather than either shipping something broken or silently switching sources without saying so.

## What was built instead

**`aidy_economic_calendar_client.py`** (new): `EconomicCalendarClient`, free and keyless, against the public "Fair Economy" JSON feed (`nfs.faireconomy.media/ff_calendar_{lastweek,thisweek,nextweek}.json`) that many retail trading tools already rely on. Schema: `title`, `country`, `date`, `impact` (Low/Medium/High), `forecast`, `previous` -- **no "actual"/realized-outcome field at all**, which makes it inherently point-in-time-safe: forecast and previous are both legitimately public knowledge regardless of an event's timing relative to any given signal, so there is nothing in this feed's schema that could ever leak a future result. `from_environment()` needs no key or URL, just a kill switch (`AIDY_ECONOMIC_CALENDAR_ENABLED`, default on).

**`aidy_reasoning_calendar_tools.py`** (new, PR 201; extended PR 202): two distinct things live here, deliberately kept separate in the same module:

1. **`get_economic_calendar`** (`build_calendar_tool_executor`) -- an on-demand tool the model may choose to call for a specific `hours_before`/`hours_after`/`min_impact` window, same shape as the existing `get_recent_candles` tool.
2. **`fetch_todays_scheduled_events`** (PR 202, the owner's actual next ask -- see below) -- a *standing* rundown, computed fresh per signal and folded into `market_context` automatically, never gated behind the model deciding to call anything.

Both share `_fetch_merged_weeks()` (last/this/next week, de-duplicated -- a window near a Sunday/Monday boundary can span two weeks) and `_too_old_for_current_week()` -- the feed only ever reflects the real-world current week, so a signal more than ~6 days from real "now" gets an explicit refusal (`None`/`{"error": "signal_too_old_for_current_calendar_window"}`) rather than silently served the wrong week's events as if they belonged to it.

**`aidy_reasoning_engine.py`** generalized: `reason()` now takes `tool_schemas: list[dict] | None` instead of hardcoding the candle schema as the only option, so multiple tools can be offered together. `AidyReasoningRunner._tools_for(signal_posted_at)` combines whichever tool clients are actually configured (candles, calendar, both, or neither) into one schema list and one dispatching executor -- a tool whose client isn't configured is simply never offered.

## Then the owner asked for more: the standing day-map

Right after PR 201 shipped, the owner said: *"He should use that and map the trading day out for gold in real time, then he can refer to it throughout the day?"*

Recognized this as a different ask in kind, not degree: an on-demand tool the model might or might not choose to call per signal does not deliver "a map of the day, refer to it throughout" -- that needs something standing. Built `fetch_todays_scheduled_events(client, *, as_of)` (PR 202): filters the same 3-week feed to just `as_of`'s own UTC calendar day, medium/high impact only, each event labelled with `session_bucket()` -- reused directly from `provider_fairness.py`, the same asia/london/london_new_york_overlap/new_york/rollover boundaries already used everywhere else in this codebase for Gold session segmentation, not redefined.

`aidy_reasoning_runner.py`'s `_fetch_market_context` now combines **two independently-optional sources**: regime/session context (`AidyContextClient`, from PR 199) and the day map. Each degrades independently -- a failure in one (e.g. `AidyContextTerminalMiss`) never suppresses the other. `PROMPT_VERSION` bumped v3->v4 (`MODEL_VERSION` stayed v3 -- the reasoning mechanism itself didn't change, only its inputs).

**A real test-writing mistake caught before it shipped**: an early draft test asserted `context is None` when a calendar client with zero matching events was configured. That's wrong -- the actual (correct) behavior returns `{"todays_scheduled_events": []}`. A genuinely-checked empty day is different information from "couldn't check at all," and the model should be able to tell the two apart. Caught this before running the test, renamed and fixed it, and added a separate test for the true no-data case (no clients configured at all).

## What this does NOT do

Neither PR touches `aidy_decision_engine.py` or any execution path. Every row is still `research_only=true`, `live_money_execution_allowed=false` at the schema level.

## FINNHUB_API_KEY disposition

Set on Render (`srv-d9qmcgks728c73a555m0`) while investigating, left in place rather than risk a destructive env-var replace operation. **It is not read by any shipped code** -- confirmed by direct grep of the deployed source at the current HEAD: the only reference anywhere in the codebase is an explanatory docstring in `aidy_economic_calendar_client.py` describing why Finnhub was *not* used, not an env-var read.

## Verification

- PR 201: 125 aidy-related tests green (was 104). PR 202: 134 green (was 125).
- Full `services/api/tests` suite run clean both times (same pre-existing `test_ai_lifecycle_already_closed.py` exclusion as every prior PR that night). `ruff check` clean on every new/changed file.
- Both deploys (`dep-damc5kbncjis73der750`, `dep-damc8p97lnhs73c6nnq0`) confirmed via `get_deploy` to have finished and gone live cleanly (no `build_failed`) before being superseded by later same-night commits.
- PR 202 needed no new migration.

## Gap found on return -- read this before trusting "current state" claims

When this session returned to verify PR 201's deploy and write this handover, the deploy history showed **four more PRs had landed since PR 202: #203, #204, #205, #206**, apparently from a separate concurrent session this one has no transcript context for:

- **#203** "Harden AIDY Provider Context against transient transport failures"
- **#204** "Fix Day 14 governance for append-only provider cohorts"
- **#205** "Make AIDY use candle tools when structure evidence is needed" -- this PR's own deploy came back `build_failed`, followed by four more direct commits ("Fix wrapped AIDY tool-policy assertion", "Make AIDY prompt regression test whitespace-safe", "Fix malformed newline in AIDY regression test", "Repair literal newline escape in AIDY test", "Normalize whitespace in AIDY prompt regression test") -- three more `build_failed` before one finally succeeded, all apparently chasing a broken string literal in an AIDY prompt regression test.
- **#206** "Restore Day 13 forward evidence under current Gold session buckets" -- now the current live deploy (`dep-damehgfgejbc7385hgg0`).

This session verified only that the *current* live deploy is up, `/health`-equivalent healthy, and its app logs show no errors touching AIDY reasoning/market_context/calendar/FINNHUB. **It did not read #203-206's actual diffs.** Next session: read those PRs before making any claim about what they changed, especially #205 given its rocky build history -- confirm the eventual fix that shipped is actually correct and not just "made the build pass."

## Open items unchanged from prior handover

1. AIDY generating and scoring its own trade ideas remains explicitly un-started, pending separate, deliberate owner sign-off -- real money is live on GOLDHUNTER.
2. The Render restart-loop (`instance_count` flapping) was last observed 04:27-04:29Z, attributed to a lapsed payment method the owner believed was fixed. **Still not re-confirmed** -- not re-checked this pass either.
