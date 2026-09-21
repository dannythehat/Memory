# AIDY Expert-Gate Programme — Build 22 Meta Direction Aggregator & Explanation

**Date:** 2026-09-21  
**Status:** ENGINEERING PROVEN / COMPLETE  
**Next:** Build 23 — Chronological Replay, Ablation & Untouched Holdout

Build 22 adds `aidy_gold_meta_direction_aggregator_v1`.

It produces one research-only 15-minute view:
- bullish;
- bearish;
- neutral;
- abstain.

Every directional contribution is traceable to the exact Build-21 selector row and verified Build-2 packet digest.

Strong high-trust contradiction can force abstention. Context-only gates remain visible but cannot cast directional votes.

Numerical confidence is not invented. It remains null unless a sufficient historical meta-calibration record existed before the current cycle. Small-N and future calibration records cannot create confidence.

Acceptance:
- tested head `5eb5a20f7aa5003aec38ccf6a5714f7adf8b559f`;
- implementation merge `25be25ddb973e9c419002630a481e2b6c4cb5d05`;
- AIDY handoff `73b7668806ed35d4d223a8f5e79b6cf8636ee8d8`;
- acceptance run `35615805313`: PASS;
- semantic gate `35615805343`: PASS;
- 74 focused tests;
- 6 dedicated aggregator tests;
- 1637 full regression tests.

Boundaries: research-only, formal-forward OFF, live-money authority OFF, no Super Signals execution/provider/risk changes.
