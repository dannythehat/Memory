# AIDY — Current Roadmap

This is the current September continuation roadmap. Older Day-numbered milestones exist in the source repo; resolve ambiguity by date and evidence file.

## Current hardening sequence

- Day 3 — D1 usage/resilience monitoring — GREEN.
- Day 4 — capture freshness watchdog — GREEN.
- Day 5 — archive-outbox durability watchdog — GREEN.
- **Day 6 — bounded archive retry/backoff + explicit dead-letter state — NEXT.**

## Intelligence sequence after hardening

- **Day 7 — provider identity + behavioural profiles.** Learn how each provider communicates/trades without allowing historical prices to contaminate current decisions.
- **Day 8 — forward-only learning boundary.** Enforce what was actually knowable at the time.
- **Day 9 — canonical AIDY context join.** Match provider setups to the market/session/regime context AIDY knew then.
- **Day 10 — immutable context attached to each signal.** Make provider outcome research conditional on contemporaneous context.
- **Day 11 — execution-cost calibration.** Compare theoretical/paper outcomes against realistic spread/slippage/broker effects.
- **Day 12 — hierarchical provider fingerprints.** Build statistically shrunk provider identities rather than naive leaderboards.
- **Day 13 — conditional fingerprints.** Discover where a provider is strong/weak by side/session/regime with preregistration/FDR controls.
- **Day 14 — correlation/relay clusters + drift.** Detect copied/correlated sources and behaviour/performance change.
- **Day 15 — governance harness.** Evidence-backed promotion/demotion/shadow decisions.
- **Day 16 — veto/filter counterfactual.** Test whether AIDY can improve provider results by rejecting bad contexts.
- **Day 17 — confidence calibration + dormant sizing.** Test whether calibrated confidence deserves different paper exposure.
- **Day 18 — combined-book intelligence.** Account for correlated providers and total XAUUSD heat.
- **Day 19 — explainability.** Explain accepted trades without exposing providers/internal secrets.
- **Day 20 — active management intelligence.** Research exits, SL/BE, runners and management interventions.
- **Day 21 — full audit.** Separate BUILT vs ENGINEERING PROVEN vs STATISTICALLY VALIDATED vs any future real-money authority.

## Statistical discipline

No provider intelligence should graduate on tiny-N winner picking. Use minimum sample gates, effect sizes, uncertainty/credible intervals, hierarchical shrinkage, multiple-testing control and forward-only evidence.
