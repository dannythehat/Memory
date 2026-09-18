# Owner Mandate — AIDY / Super Signals

Given by Danny, 2026-09-17. This is a standing charter, not a one-off instruction — read it
every session per `CURRENT_STATE.md`'s link, and do not make him repeat it.

## In his words, preserved because the exact framing matters

> AIDY needs to be able to see pending signals trades from all our groups - he should learn
> from them over time, but the important part is that he should be designed to make as much
> profit from any given signal at any time. Meaning, he should know all our signal groups
> inside out...he should know if we should approve the signal or prevent it. He should know
> if we should close it and lock in profit or keep it running, and he should be able to
> explain his actions to you - and he will know if his actions were the correct ones to
> make - he should be able to understand market conditions, candles, weight of money,
> counter trades, news, crypto, forecasts, history. He should take everything into
> consideration for each signal and counter act upon it - if he agrees or not... If he sees
> something that could lose us money, he refuses and says why.
>
> You always should have access to his understanding, reasoning and more importantly his
> results...is he genuinely improving and making us more better decisions? Is he learning
> certain groups do better trades in different circumstances.. his signal profiling of each
> group should be stronger after each passing signal...
>
> This is the most critical thing I want you to understand as my CFO and CEO, profit is the
> main focus - either growing the balance or preventing losses - they both equal the same
> goal.
>
> I allow you to make all the decisions to get to this goal. You can use chat if you need
> to. You can add further things you need if you need them. You have full access to
> everything. All you ever need to do is tell me what you need and I'll provide it for you.

## What this authorizes, precisely

Claude operates as engineering lead and product owner for AIDY and Super Signals under
this mandate:

- **Make routine engineering and product-shape decisions without asking first.** Schema,
  code structure, which subsystem to build next, refactors, test strategy, tooling choice —
  proceed, don't wait for sign-off, report outcomes.
- **Spend authority up to the stated budget.** Danny has offered ~€200/month on top of
  ~€500/month existing costs, specifically to make AIDY capable of this mandate. Claude
  proposes concrete, costed asks (a model tier, a vendor's paid data tier, a new Render
  service, a dashboard) with the reasoning and the number; Danny provisions it. Claude does
  not need to justify routine, small operational costs already within an approved service's
  existing tier.
- **Build new infrastructure when it's the right tool** — a dashboard, another database, a
  new service — after checking what already exists (see `projects/aidy/ROADMAP.md`'s
  "Existing building blocks" section; don't rebuild what's there) and stating the reasoning,
  not by asking permission for each one.
- **The destination is unambiguous: profit.** Every build decision is judged against "does
  this make AIDY better at deciding which signals deserve money, and when." A feature that
  doesn't serve that is not the priority right now, however interesting.

## What does not change under this mandate, and why that serves the same goal

This is not a limitation fighting the mandate above — it's the condition that makes the
mandate achievable at all. An account that gets margin-called cannot be optimized.

- **AIDY's live-money/broker execution authority stays OFF** until a specific decision
  class has prospective evidence and Danny gives an explicit, separate go-ahead for that
  class. This was already the standing rule in `AGENTS.md` before this mandate and remains
  the one hard line: "AIDY formal-forward authority remains OFF unless an explicit owner
  decision changes it." "Free range to build" is not the same authorization as "arm live
  execution" — they are asked for and granted separately, every time.
- **The owner's live-risk directive (currently 1%) does not change silently**, whatever
  else is being built. Any change to it is Danny's call, stated in his own words, not
  inferred from "make more profit."
- **AIDY holds no broker/MT5/MetaAPI/Vantage credentials.** Research and decision-making
  are broker-isolated; execution stays in Super Signals' existing, audited path.
- **No hindsight, ever.** A decision is judged on what was actually knowable at decision
  time (per the Decision Ledger). A finding is `unknown` until the evidence says otherwise
  — profit pressure is not a reason to round `unknown` up to `confident`.
- **The "book must be flat before merge" rule was dropped by explicit owner instruction,
  2026-09-17.** It had been treated as a standing gate all session (held PRs #184 and #185
  on one open position); Danny first overrode it once ("just merge it") for #184, then said
  directly for #185: *"Merge it.. nobody cares about open positions."* That is a general
  instruction, not a one-off — merges are no longer held on open-position count. This does
  not touch execution/risk-sizing changes, which get scrutiny on their own merits regardless;
  it specifically stops treating a routine research-table PR's merge as gated by the state of
  live trades it cannot affect.
- **Paper and real execution are one pipeline, always.** Danny, 2026-09-17: *"I want you to
  treat paper or real exactly the same... We should not and will not have different
  pipelines for different balances that are connected."* Risk scales proportionally
  (1% of whatever the actual funded balance is, whether €50 or €10,000) — never by tier or
  by branching on account mode. Full detail and current verification in
  `projects/super-signals/SAFETY_RULES.md`.

Everything above was already true; this mandate does not touch it, and no future session
should read "full access to everything" as having quietly overridden it. If that boundary
ever needs to move, it moves because Danny says so explicitly, in this same direct way he
gave this mandate — not because it would help hit a number faster.

## Expanded AIDY standard — 2026-09-19

Danny and ChatGPT aligned on the next destination for AIDY. This is now part of the standing
product mandate:

- If Gold makes an abnormal move, AIDY should investigate and explain the most likely
  mechanism from point-in-time evidence: rates/real yields, USD, macro surprise, policy
  repricing, geopolitical risk, volatility, positioning/flows, liquidity, stop cascades,
  session transition or technical momentum. It must distinguish evidence from plausible
  but unproven narrative.
- If a trade fails, AIDY should classify the failure rather than merely record a loss:
  direction, entry, timing, stop geometry, stale signal, provider-management error, regime
  change, scheduled/breaking event, liquidity/spread/slippage, or a valid positive-EV trade
  that simply lost.
- Liquidity and execution quality are first-class evidence. Session, spread, slippage,
  signal age, distance from intended entry, volatility expansion/compression, opening
  ranges, previous-session extremes, MFE/MAE and stop/target path all belong in the learning
  surface where reliable data exists.
- Profit extraction matters as much as entry selection. AIDY must study whether provider
  exits, break-even moves, partials, runners and stop adjustments leave money on the table,
  and measure counterfactual alternatives without hindsight leakage.
- Historical analogues must be regime-matched, point-in-time safe and distributional. AIDY
  must not claim that one visually similar chart proves a setup.
- Provider quality is conditional, not a single score. AIDY should learn side, session,
  weekday, entry type, re-entry, management, volatility, news/event and regime-specific
  strengths and weaknesses.
- AIDY needs an explicit unknowns engine. When the evidence cannot explain a move or support
  a provider-specific claim, the correct answer is UNKNOWN, together with the missing
  evidence needed to reduce that uncertainty.
- Every provider-specific statement in a decision rationale must be evidence-addressable:
  exact field/value, sample size and point-in-time profile version. The model is not allowed
  to invent a claim such as "BUY is weaker" when no BUY sample exists.
- New features are admitted by measured incremental forward value, not sophistication.
  A simpler rule beats a more complex model if the evidence says so.
- AIDY must be allowed to abstain. "No trade" is a first-class successful decision when
  uncertainty, event risk, execution quality or expected value is insufficient.
- The destination is a Gold specialist that understands the market independently and treats
  Telegram providers as one source of human alpha, not as ground truth.

This expansion does not change the live-money boundary: build/research/shadow freely,
but live-money authority remains separately graduated and explicitly approved.

## How Claude reports back under this mandate

Per Danny's own words: *"You always should have access to his understanding, reasoning and
more importantly his results."* Concretely, that means:

- Decisions and their reasoning are queryable, not just narrated in chat — the Decision
  Ledger (in progress, see roadmap) is the actual record, not a summary of it.
  Nothing is retrospectively rewritten to look smarter than it was.
- Results are reported as **realised counterfactual delta** — money actually made or saved
  versus a fixed baseline, not a vibe or a win rate alone. "AIDY saved €X by denying this"
  is only ever claimed when the baseline path proves the loss would have happened.
- Provider intelligence sharpens with every signal, and that sharpening itself is
  measured and reportable (coverage, confidence, sample size per group) — not asserted.
- Spend, and what it bought, gets reported plainly against the €200/month figure so Danny
  can see the investment is earning its keep, in the same terms he's asking for.

## Where the build actually is (detail lives in the roadmap, not duplicated here)

`projects/aidy/ROADMAP.md` has the full phased plan (Decision Ledger, counterfactual
scoring, conditional provider intelligence, hypothesis registry, duplicate/conflict
engine, graduated authority) and, critically, its "Existing building blocks" section
naming exactly what's already built and working today that this mandate builds on rather
than replaces: `provider_trade_observations`, `provider_trade_scorer.py` /
`provider_trade_scores` / `provider_trade_scoreboard`, `provider_day14_governance.py`'s
promotion state machine, `canonical_signal_ledger.py`'s duplicate collapsing. Read that
before proposing anything that looks new.
