# Super Signals Handover — 14 September 2026 — shadow scoring root cause

## Status: RED on scoring, GREEN on capture

**RUNTIME VERIFIED** against production PostgreSQL (`dpg-d9qmc6cs728c73a54kc0-a`) via read-only
queries, 2026-09-14.

## The problem in one line

**750 shadow trades captured. 39 scored. 5%.**

The capture engine works. The scoring layer is starved, and the cause is entirely upstream in
AIDY. See the AIDY handover of the same date.

## Where the 750 trades went

| Outcome | Trades | Cause |
|---|---|---|
| **Never observed** (`quote_mode='unobserved'`) | **423** | No AIDY M1 data covering the trade's life |
| **Blocked on a missing minute** | **107** | 44 distinct missing M1 minutes |
| Correctly excluded | ~181 | own channel, legacy profiles, pre-entry closes, style rules |
| **Scored** (`score_eligible`) | **39** | |

### The 44 missing minutes

`aidy_resolution_note` = `aidy_m1_waiting_for_missing_minute:<ts>`.

- **44 distinct minutes**, spanning **2026-09-04T01:35Z → 2026-09-09T05:40Z**
- They block **107 trades**
- The same minute recurs across clusters — e.g. `2026-09-07T09:00Z` and `2026-09-08T13:31Z` each
  block multiple trades

The resolver hits one absent minute, refuses to guess, and waits indefinitely. That is correct
PIT behaviour. It just needs the hole refilled.

### Main exclusion reasons

`outcome_pending_aidy_m1`, `market_data_not_observed`, `aidy_m1_signal_minute_ambiguous`,
`aidy_m1_management_bar_ambiguous`, `aidy_m1_revalidation_required`, `unsupported_style_scalper`,
`internal_super_signals_source` (correct — own channel), `legacy_profile_unresolvable`.

## Nothing is lost

Every one of the 750 trades retains full geometry: entry, stop, all targets, exact signal
timestamp, provider management messages, PIT profile version. They are **unscored, not
destroyed**. Twelve Data sells historical M1. The backfill machinery already exists —
`twelve_data_bootstrap.py`, `/calibration/market/ohlc`, `provider_day11_calibration_replay`.

Fill the history, re-run the resolver, and the corpus scores itself retrospectively.

Expect partial recovery, not total: where the signal minute itself is missing and the trade
already closed with `aidy_score_blocked`, PIT rules may correctly refuse it.

## Provider populations — verified, corrects Memory

| Status | Count |
|---|---|
| testing | **5** |
| shadow | **28** |
| paused | 14 |
| revoked | 16 |
| **live** | **0** |

Memory previously said "~40 shadow discovery providers". **The real number is 28.** And **no
source carries status `live`** — the five real providers run as `testing`.

Totals: 1,341 signals · 750 shadow trades · 1,775 positions · 15 users · 74 tables · 13 views.
Alembic head `0079_fix_member_entitlements`, matching source.

## Shadow benchmark results — treat as DIRECTIONAL ONLY

On the `fixed_1000_10_per_tp_fair_v2` benchmark ($1,000 notional, $10/leg), net across all
shadowed providers is roughly **−$1,000**.

The five providers with real execution, on the same benchmark:

| Provider | Benchmark P&L | Closed |
|---|---|---|
| TIG's Asia Trades | +$29.61 | 15 |
| United Kings | $0.00 | 1 |
| FXTradingVision | −$30.00 | 6 |
| GTMO VIP | −$160.48 | 8 |
| SureShot GOLD | no closed trades | 0 |

**These numbers are not trustworthy yet and must not drive a promotion or demotion.** Reasons:

1. Only 5% of trades are scored, so the sample is both tiny and non-random.
2. **Every** provider is still `research_state='learning'`. Not one has reached `shadow` or
   `qualified`.
3. The evidence floors need 20–45 distinct trading days. There are ~12 days of data
   (1–14 Sept), and two of those had no capture at all.

Correct status remains `WAITING-FOR-FORWARD-EVIDENCE`.

## Real money — the database is NOT authoritative

Database figures at 2026-09-14:

- `performance_trade_outcomes`: 737 won (+$6,274.32), 440 lost (−$5,791.36), 130 breakeven, 4 open
- `broker_deals` net incl. commission/swap/balance ops: **+$471.26**
- `performance_account_snapshots`: latest **$1,471.26** (10:23 UTC), max $1,795.26, min $987.54

**The owner states the real account is $2,000+ from $1,000 in roughly five weeks, and that
tooling outages left gaps in the recorded ledger.** That is consistent with the capture failures
documented here.

**Therefore: do not quote database P&L as business truth.** The broker is authoritative. Any
future agent must reconcile against the broker before making a performance claim, and must not
repeat the database number as if it were the account.

A related open item: the committed `public/data/public-performance.json` records
`current_recorded_balance: 1889.04`. This is customer-facing on `smartsignals.site` and needs
reconciling against broker truth.

## Next steps

1. AIDY capture restored (see AIDY handover) — prerequisite for everything below.
2. Twelve Data quota headroom, or snapshots keep returning partial.
3. Backfill the 44 missing minutes → unblocks 107 trades. Smallest proof of the repair.
4. Backfill full M1 for 1–14 Sept → addresses the 423 unobserved trades.
5. Re-run the shadow resolver over the whole corpus.
6. Re-read the scoreboard. Only then discuss provider promotion/demotion.
7. Reconcile the public balance.
8. Data Hub last — it should render verified data, not unverified data confidently.

## Rule

Shadow research remains broker-isolated. Nothing in this repair touches execution, risk or
provider eligibility. `shadow` sources still branch into `_dispatch_shadow` before any broker
code path exists.
