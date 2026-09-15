# Super Signals + AIDY Handover — 15 September 2026 — per-group P&L is live

## Status: DEPLOYED AND VERIFIED · scoring still converging at time of writing

Everything below is runtime verified against production, not inferred. Where a number is
still moving it says so.

## The headline: the business question is answered

"Which shadow groups make money" now has an answer in the database, refreshed
automatically. Read it from `provider_trade_scoreboard`.

At 10:03Z: **664 won / 532 lost / 4 breakeven / 50 never entered / 52 still open**,
1,042 not yet scorable, out of **2,348 scorable trades**. The counts were still climbing
as the pass ran — re-read the view rather than quoting these.

Directional finding worth keeping: **TRADE GLOBAL was the worst group by a distance**
(−$21.54 per trade over 34 resolved, 26.5% win rate) and **FXTradingVision the best on a
meaningful sample** (70.3% win rate, +$7.73 per trade over 37). Coverage was low for both
— treat as directional, re-read the view before acting.

## The architectural correction that made it possible

Scoring was being built on `shadow_trades`. That could never have answered the question,
because a shadow trade only exists where a trade was **also mirrorable**:

| Provider | Trades recorded | Shadow trades |
| --- | ---: | ---: |
| TDC V2 | 565 | 0 |
| The Gold Club | 508 | 0 |
| GOLD VIP | 92 | 0 |
| PipXpert | 47 | 0 |
| TIG's Asia Trades | 665 | 571 |

The three largest providers by volume had none. Scoring now keys on
`provider_trade_observations`, which holds every trade the interpreter understood
whether or not it could be mirrored. **Check the data before building on a table.**

## What is live

Super Signals deploy chain today: `3a925fb7` → `a5258c7b` (#175) → `f948f46b` (#176) →
`e21e29bc` (#177) → `9ab11790` (#178). Alembic head in production:
**`0087_provider_scoreboard`**. Book was flat (0 open positions) at every merge.

New surface:
- `provider_trade_scores` — one row per observation. `forward_evidence_eligible` is
  CHECK-constrained false; no promotion gate reads it.
- `provider_trade_scoreboard` — per-provider view carrying its own caveats.
- `ProviderTradeScoringRuntime` — runs a pass every 30 min inside the API process.
  `PROVIDER_SCORING_ENABLED=0` disables it without a deploy.

AIDY: `72809f7c` (#131), `bf3bb05c` (#132), plus D1 migration
`0021_retrospective_research_request_kind.sql`.

## Scoring conventions — these decide every number

Applied uniformly so providers stay comparable. If any of these change, every figure
changes with it.

1. **A posted range is a limit**, filled at the edge *least favourable* to the trader —
   including a range the message labelled "market". Filling at the good edge would
   flatter whoever posts the widest zones.
2. **A bar touching both stop and target is read as the stop** — the worse reading.
3. **A target on the wrong side of the entry is dropped** as a misread, not counted as an
   instant win.
4. **Replay starts at the first whole minute after the signal.** 2,306 of 2,348 trades
   are posted mid-minute; the seconds before the post are unattributable, so they are
   skipped rather than credited. Rounding is always up.
5. **Management is not modelled.** Nothing reliably links a "move SL to BE" message to
   its trade outside the signal pipeline, so every trade runs to stop, target, or window
   end. Actively-managed groups score worse than they deserve —
   `update_rate_pct` in the view is how much to discount, and it runs 40–83%.

`scored_coverage_pct` says how much of a catalogue the P&L rests on. A group with four
scored trades out of two hundred has a P&L and it means almost nothing.

## Two live incidents found and fixed

### AIDY capture was dead for 5.4 hours

`wrangler.test.example.jsonc` declares `crons: ["* * * * *"]` and `/health` reports
`scheduler: "direct-cron"` — **that minute cron is scheduled capture**.
`day11-calibration-backfill.yml` rebuilds the config with `triggers.crons = []`, so its
deploy at 03:44 silently removed it. Last scheduled success 03:52, last stored vendor bar
03:51, nothing after. The deploy was green and the capture was dead.

Fixed by `aidy-provider-research-read-deploy.yml`, which asserts the cron in the config it
builds and then verifies it against **Cloudflare's own schedules endpoint** rather than
trusting the file it just wrote. Capture resumed 09:17Z, lag back to 25s.

**`day11-calibration-backfill.yml` still strips the cron if re-run.** Not fixed. Do not
run it without restoring the cron afterwards.

### A stale edit could become a live market order

`_persist_edit` recovers an edit whose original message is missing, gated on freshness —
"so a stale edit can never be turned into a late market order", per its own comment. The
gate started at `True` and narrowed only if a freshness check existed, so listeners
*without* one recovered every orphaned edit unconditionally, including hours-old ones, as
a market order at today's price. Now requires an affirmative answer on all three counts.

This was also why `test_edit_for_paused_source_is_ignored_and_missing_original_is_audited`
had been red on the deploy branch. The test was right and was reporting this.

## Bugs worth remembering because the shape recurs

- **The PIT cutoff was applied to research.** `fetch_research_m1` parsed bars with `_bar`,
  which refuses a bar first observed after its window closed. Correct for decisions,
  fatal for research where every bar is observed later — 2,214 trades failed to parse.
  Now a parameter defaulting to enforced, opted out by name only on the research path.
- **AIDY selected `first_observed_at` and `payload_digest` and never emitted them.** The
  only consumer required both. A field read from the store must also be sent; there is
  now a test saying so.
- **A retry allowlist of exception names stranded everything it had not predicted.**
  1,427 rows carried `research_fetch_failed:ValueError`, which was not in the list, so
  they would never have been re-asked after the fix. Now matches any fetch failure.
- **An error reason naming only the exception type is not a diagnosis.** Finding the
  cause cost a full deploy cycle; the message had named it all along. Reasons now carry
  the message.
- **A D1 CHECK constraint rejected the new `request_kind`.** The retrospective service's
  tests stubbed the store, so nothing caught it until production. Rebuilding the table
  needed care: D1 *enforces* foreign keys where local SQLite defaults off, so child rows
  had to be moved aside around the swap, and the decision-admitted view dropped and
  recreated verbatim. Verified 9,904 admitted rows before and after.

## AIDY M1 coverage

Backfilled 2026-08-12 → 2026-09-15 via `aidy-retrospective-m1-backfill.yml`
(`workflow_dispatch`, mints an ephemeral admin token and deletes it). Twelve Data **does**
serve five-week-old M1 at full 60 bars/hour — that was the open question and it is
answered. Most days 08-12 → 09-08 are now complete where several held only 120 bars.

Retrospective bars land under `twelve_data_retrospective_m1_v1`, which
`twelve_data_decision_admitted_m1_v1` does not select. They cannot reach a forward
decision.

## Still open

- 197 `aidy_m1_entry_target_sequence_ambiguous` and ~10 related — genuinely undecidable
  from M1. Deliberately *not* re-asked, or they loop forever.
- 96 `no_price_history_for_window`, 41 `no_target_beyond_entry`,
  22 `aidy_original_geometry_stop_invalid` — data, not code.
- GTMO VIP instrument declaration (20 trades, `testing`/live-executing) — owner decision.
- `public/data/public-performance.json` (`current_recorded_balance: 1889.04`) not
  reconciled against broker truth.
- `day11-calibration-backfill.yml` cron-stripping, as above.

## Test state

Super Signals API suite: **1,082 passed, 0 failed** — green for the first time in this
work. Migrations `0001`→`0087` apply clean on a fresh PostgreSQL.
