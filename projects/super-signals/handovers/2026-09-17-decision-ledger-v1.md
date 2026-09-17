# AIDY Decision Ledger v1 — built, pushed, not yet merged or deployed

**Date:** 2026-09-17
**Repo:** `dannythehat/super-signals`
**Branch:** `claude/codebase-architecture-review-mq0txl` (restarted from trunk tip `8b2ca7f`, after PR #182 merged; see "branch reuse" note below)
**Commits:** `d72a628` (alembic env.py fix), `00deff4` (Decision Ledger)
**PR:** none opened — per standing instruction, a PR is only opened when explicitly asked. Danny needs to say the word.

## What this is

The first piece of the Decision Ledger described in `CURRENT_STATE.md`'s "Mandatory Decision Ledger" / "Conditional provider intelligence" / "Authority graduation" sections, and in the owner's 2026-09-17 mandate (`OWNER_MANDATE.md`): AIDY makes one reasoned, explained call per eligible signal, with nothing invented and no silent authority.

**v1 is deliberately deterministic — no model call.** The owner's mandate asks for AIDY to eventually weigh market conditions, news, candles and forecasts, but that needs a real per-signal model call, which is real ongoing cost, and it is not switched on without a costed proposal to Danny first (build-order item #5 in the plan given to him). What v1 ships is the class of decision that needs none of that: a provider's own recorded track record, and whether a signal duplicates or conflicts with exposure the book already has. Both are exactly-computable from data already in the database.

## What was built

- **`services/api/migrations/versions/0088_aidy_decision_ledger.py`** — `aidy_decisions` and `aidy_decision_outcomes`. Every row is `research_only boolean CHECK(research_only)` and `live_money_execution_allowed boolean CHECK(NOT live_money_execution_allowed)` — structural, not documentary. Both tables are trigger-enforced append-only. `aidy_decisions` has `UNIQUE(observation_id, decision_class, rule_version)` and `CHECK(decided_at >= signal_posted_at)`.
- **`services/api/app/aidy_decision_engine.py`** — `AidyDecisionEngine.evaluate()`: checks duplicate/repost (same source+side+symbol within 15 minutes of a prior approve/hold decision) → opposite-direction book exposure conflict (does the reference book already hold the opposite side open?) → provider track record (`provider_trade_scoreboard`, min 20 resolved trades, denies only when avg P&L ≤ -$3 **and** win rate ≤ 35% together). Never invents confidence — every v1 decision returns `confidence=None`.
- **`services/api/app/aidy_decision_runner.py`** — selects eligible observations (same "understood enough" bar as the trade scorer: side, entry, stop, ≥1 target), decides, persists with `ON CONFLICT ... DO NOTHING`. Re-asks only decisions whose sole prior reason was `insufficient_track_record_evidence` — a resolved approve/deny/conflict/hold is never relitigated (no hindsight rewriting).
- **`services/api/app/aidy_decision_runtime.py`** — runs the runner on a 300s timer inside the running application, no broker credential needed, `AIDY_DECISION_ENGINE_ENABLED=0` to disable, failures logged and retried without ending the loop.
- **`services/api/app/main.py`** — wired `AidyDecisionRuntime` into startup/shutdown alongside the existing `ProviderTradeScoringRuntime`.
- Two test files, 13 tests total: 6 pure unit tests on the track-record rule (no-history, below-minimum, bad book denied, profitable book approved, denial requires both weak signals together, exact-threshold boundary), 7 integration tests against real Postgres (no-history gets a decision not silence, duplicate held, conflict denied, live-authority CHECK fires, append-only trigger fires, runner selects only new/thin-evidence rows).

## Why these tables and not the existing ones

Two prior tables already existed for exactly this purpose (`provider_veto_counterfactual_decisions`/`_outcomes` from Day 16, `provider_management_counterfactual_decisions`/`_outcomes` from Day 20) but were verified **zero rows, never wired to anything** before deciding to build `aidy_decisions` fresh rather than duplicate effort. If a future session finds those tables again, they are dead weight, not a competing source of truth.

## What broke and got fixed along the way: the alembic/pytest logging bug

Running the two new test files alone passed. Running the *full* suite showed 2 failures in `test_aidy_shadow_runtime_startup.py` — both `caplog`-based assertions, both failing with `caplog.text == ''` even though the log line clearly printed to stdout.

Root cause: `services/api/migrations/env.py` unconditionally calls `logging.config.fileConfig(config.config_file_name)` on every Alembic migration. `alembic.ini`'s `[loggers]`/`[handlers]` sections reconfigure the **root logger's handlers** — this replaces pytest's `caplog` capture handler on the root logger for the rest of that test process, not just for the test that happened to run the migration. It had never fired before because no test file that runs an in-process Alembic migration happened to sort alphabetically before `test_aidy_shadow_runtime_startup.py`. `test_aidy_decision_ledger.py` (new, and its `engine` fixture runs `command.upgrade`) was the first, purely by alphabetical file order (`aidy_decision_ledger` < `aidy_shadow_runtime_startup`).

Fix: `env.py` now skips the `fileConfig()` call when `PYTEST_CURRENT_TEST` is set (pytest sets this automatically during test runs). Real CLI/deploy usage — where nothing else has configured logging yet — is unaffected. This is a genuinely pre-existing landmine, not something introduced by the Decision Ledger work; it would have bitten the *next* new alembic-invoking test file whenever one happened to sort earlier than `test_aidy_shadow_runtime_startup.py`.

## A second, unrelated environment issue: local Postgres crashed mid-session

While running the full suite, the local test Postgres cluster under the session scratchpad (`/tmp/claude-0/.../scratchpad/pgdata`) hit `PANIC: could not open file ".../pg_control": Permission denied` and terminated. Investigation showed the scratchpad's parent directories (`/tmp/claude-0`, `/tmp/claude-0/-home-user`, `/tmp/claude-0/-home-user/<session-id>`) had `drwx-----x`/`drwx------` permissions that no longer allowed the non-root `postgres` unix user to traverse them — likely a container-identity artifact from a mid-session restart, not anything in this session's control. Rather than fight that sandboxing, the test cluster was reinitialized fresh under plain `/tmp/pgtest` (normal permissions), which is disposable local test infrastructure only — no production data was at risk. If a future session hits `psycopg.OperationalError: connection failed ... Connection refused` against the usual `127.0.0.1:55432` test database with no obvious cause, check `pg_isready` and this permission failure mode before assuming a code regression.

## Branch reuse note (important for the next session)

This branch name, `claude/codebase-architecture-review-mq0txl`, has now been reused across at least 7 PRs (#174, #175, #176, #177, #178, #182, and now this unopened one), each one opened, immediately merged into `feature/day-10-shared-telegram-sources`, and then the *same branch name* reused for the next chunk of work starting fresh from the new trunk tip. When PR #182 merged just before this build started, the remote `claude/codebase-architecture-review-mq0txl` still pointed at the old (now-merged) history. This session correctly detected that, verified the old branch tip was content-identical to the new trunk tip, reset the branch to `origin/feature/day-10-shared-telegram-sources`, cherry-picked just the 2 new commits on top, and force-with-lease pushed — never stacking new work on already-merged history. Any future session working this branch should do the same check first (`git diff <old-branch-tip> <trunk-tip> --stat` — empty means already merged, reset and replay).

## Verification

- 13 new tests: 100% pass, isolated and in the full suite.
- Full `services/api/tests` suite: green (exit 0, no failures) against a fresh PostgreSQL 16 with migrations `0001`→`0088` applied clean, both before and after the lint pass.
- Ruff: clean on all new/changed files except 2 pre-existing, unrelated `main.py` errors (`UP035`, one `E501` at line 271) confirmed present on the branch before this change via `git stash` comparison — not introduced by this work.
- Nothing here touches Super Signals' execution path. `aidy_decisions` is read by nothing that trades.

## Next steps (in the order given to the owner)

1. Open a PR against `feature/day-10-shared-telegram-sources` **when Danny asks for one**, verify book flat, merge, confirm the `AidyDecisionRuntime` loop is actually producing rows in production.
2. Outcome/counterfactual scoring — reuse `provider_trade_scorer.py`'s replay engine for a baseline-vs-actual `decision_delta_usd` comparison, populating `aidy_decision_outcomes`.
3. Extend `provider_trade_scoreboard` with cohort dimensions (side, session, weekday) so track-record evaluation isn't a single blended number.
4. Hypothesis registry (genuinely new work, not yet started).
5. The LLM-based reasoning layer — needs a costed spend proposal to Danny first (model tier, expected call volume/cost) before switching on.
6. Graduated authority — start with deterministic duplicate rejection, reusing `provider_aidy_authority_audit`'s dormant kill-switch schema.
