# Rulings log — how each GV-0.1 ambiguity was settled

Every ambiguity found by the GV-0.1 vectors was ruled (reviewer rulings A-01..A-30, applied by Claude in `CANDLE_SPEC_V1.md` Draft 0.3). The spec was changed only through these rulings, never to make a test pass. The table below points at the vectors that now test each ruling.

**Two items differ from a literal reading of the reviewer's text**, both flagged for the reviewer to challenge: **A-01** (zone death: Claude replaced 'either edge' with a role-based rule because the literal rule kills every support zone on an upward bounce; GV-E2E-02 demonstrates it) and **A-03** (the rollover filter is applied to intraday timeframes only, since every D1/W1/MN1 bar contains the pause). A-09 also gained the code NOT_TRIGGERED_OTHER_SIDE.

| ID | severity | where | status | ruling | vectors |
|---|---|---|---|---|---|
| A-01 | HIGH | G4 zone death | RULED - Claude differs from the reviewer | Reviewer ruled 'dead after a close beyond EITHER edge'. Claude replaced it: zone ROLE = type of the latest contributing pivot (low -> SUPPORT, high -> RESISTANCE); a SUPPORT zone dies on a close > 0.10 ATR BELOW its bottom, a RESISTANCE zone on a close > 0.10 ATR ABOVE its top; only bars after that pivot are scanned, so a later re-joining pivot revives it. Reason: 'either edge' kills every support zone the instant price bounces upward from it (GV-E2E-02 demonstrates it). Flagged back to the reviewer. | GV-G-ZN-11, GV-G-ZN-12, GV-E2E-02, GV-P12-V05 |
| A-02 | LOW | Notation | RULED (reviewer) | Candles are K1..K5; O1,H1,L1,C1 are numeric fields; clause names in vectors use K (e.g. `K1 bear`, `LARGE(K1)`). | all pattern packs |
| A-03 | MEDIUM | P08 SRC-PS filters | RULED (reviewer + Claude refinement) | News and rollover filters apply to K2 only. Refinement: the rollover test applies to intraday TFs (M1-H4) only, because every D1/W1/MN1 bar contains the pause by construction. New code SKIPPED_ROLLOVER. | GV-P08-V11, GV-P08-V14, GV-P08-V15, GV-P08-V16, GV-P08-V17 |
| A-04 | MEDIUM | T_SR straddling zone | RULED (reviewer) | The straddling zone is the nearest obstacle; near edge at/behind entry -> SKIPPED_TARGET_ALREADY_PASSED. | GV-P08-V09 |
| A-05 | MEDIUM | SRC-SH prior state | RULED (reviewer) | Base prior state inherited unless a variant replaces it. | GV-P06-H07, GV-P06-QF1 |
| A-06 | MEDIUM | Session boundaries | RULED (reviewer) | Half-open [start, end). | GV-G-SS-03, GV-P12-S03, GV-P12-S05 |
| A-07 | MEDIUM | News boundaries | RULED (reviewer) | Inclusive endpoints. | GV-G-NW-03, GV-DORM-P04-04, GV-DORM-P04-06 |
| A-08 | LOW | Outside Bar events | RULED (reviewer) | Neutral OUTSIDE_BAR_SHAPE when H2>H1 and L2<L1; directional pattern only if K2 has a direction. | GV-P08-B05, GV-P08-B06, GV-P08-QF1, GV-HUB-07 |
| A-09 | MEDIUM | Inside Bar side | RULED (reviewer + Claude addition) | Neutral INSIDE_BAR formation at K2, counted once even if expired; PENDING_BREAKOUT while the window is open. Addition: NOT_TRIGGERED_OTHER_SIDE when the close breaks the other way. | GV-P09-S07, GV-OV-09, GV-HUB-06 |
| A-10 | LOW | Tweezer flags | RULED (reviewer) | Mirrored 25% flags on both tweezers. | GV-P11-F01, GV-P11-F02, GV-P10-F01, GV-P10-F02 |
| A-11 | MEDIUM | R_TOO_SMALL | RULED (reviewer) | Baseline only. | GV-EX-B05, GV-EX-B05b, GV-EX-B03c |
| A-12 | MEDIUM | Non-qualification | RULED (reviewer) | qualification_failures[] keeps every failed static gate; disposition NOT_QUALIFIED; SKIPPED_TF_NOT_ALLOWED retired into failure code TF_NOT_ALLOWED. Codes: PRIOR_STATE, DIRECTION, TF_NOT_ALLOWED, WITH_TREND, AT_LEVEL, IDENTITY_DELTA, RSI, SIZE_FILTER, WICKS_ENGULFED, BODY_CLOSE_FLAG, TRIGGER_NOT_MET. | GV-P03-QF1, GV-P01-QF1, GV-P08-QF1, GV-P06-QF1, GV-P14-QF1, GV-P14E-QF1, GV-P21-V05, GV-P08-V10, GV-P14-V01-M15 |
| A-13 | HIGH | MAX_HOLD | RULED (reviewer) | Entry bar = bar 0 (not counted); next 50 existing completed bars; exit at first tick after bar 50 completes; first tick after reopening (exit_across_break) if a closure follows. | GV-EX-B01, GV-EX-B01b |
| A-14 | HIGH | Swap | RULED (reviewer) | Account-spec fields; charge at every rollover crossed (x multiplier on the triple day); PENDING_COST_SPEC when a rollover was crossed and the spec is missing. Tests use an explicit fixture (swap_long -5.00, swap_short +2.00 per lot per night, rollover 22:00 UTC, triple Wednesday). | GV-EX-B02, GV-EX-B02b, GV-EX-B02c, GV-EX-B02d |
| A-15 | MEDIUM | Inside Bar CB level | RULED (reviewer) | Bull: mother low at support; bear: mother high at resistance. | GV-P09-V01 |
| A-16 | LOW | T_SWING | RULED (reviewer) | BUY: swing highs above entry; SELL: swing lows below. | GV-P14-V05 |
| A-17 | MEDIUM | Morning/Evening Star SRC-PS | RULED (reviewer) | Symmetric stop max(H1,H2)+buffer for the Evening Star; TP2 source wordings kept (Morning: swing high; Evening: zone), because the two sources differ. | GV-P16-V07, GV-P16-V01 |
| A-18 | LOW | STOP_ENTRY window | RULED (reviewer) | Bar membership; a tick belonging to bar 4 is too late (a tick stamped exactly at bar 3's completion instant belongs to bar 4). | GV-P17-V04, GV-P17-V04b |
| A-19 | LOW | Target precedence | RULED (reviewer) | SKIPPED_TARGET_ALREADY_PASSED before SKIPPED_SRC_RR. | GV-P20-V04 |
| A-20 | MEDIUM | Piercing vs Dark Cloud | RULED (reviewer) | Asymmetry kept (the Pro-Scalper pages differ). | GV-P13-V20, GV-P13-V21 |
| A-21 | LOW | Clusters | RULED (reviewer) | formation_cluster_id and signal_cluster_id. | GV-OV-01, GV-OV-09, GV-OV-11 |
| A-22 | MEDIUM | Numerics | RULED (reviewer) | Integer ticks; exact rationals; no rounding before comparisons. | GV-G-ATR-03 |
| A-23 | LOW | Even median | RULED (reviewer) | Mean of the two middle prices. | GV-G-ZN-04 |
| A-24 | LOW | 200-bar window | RULED (reviewer) | Pivot centre inside the window; left neighbours may lie outside. | GV-G-SW-04 |
| A-25 | HIGH | Entry beyond stop | RULED (reviewer) | SKIPPED_ENTRY_AT_OR_BEYOND_STOP for every variant. | GV-EX-B03, GV-EX-B03b, GV-EX-B03c |
| A-26 | MEDIUM | Bars-only fallback | RULED (reviewer) | BID and ASK bars stored from ticks; shorts use ASK bars; else NEEDS_ASK_BARS; both proven -> STOP FIRST. | GV-EX-B04, GV-EX-B04b, GV-EX-B04c, GV-P01-L06, GV-P02-L06 |
| A-27 | LOW | RAW MAE | RULED (reviewer) | MFE and MAE are non-negative magnitudes; mfe_before_mae_h defined on BID ticks. | GV-EX-B06, GV-EX-B06b, GV-P01-M01, GV-P01-M02, GV-P01-M03, GV-P01-M04, GV-P01-M05, GV-P02-M01 |
| A-28 | LOW | Rising/Falling | RULED (reviewer) | Asymmetry kept (source text differs). | GV-P20-V05, GV-P21-V05 |
| A-29 | LOW | P22 code | RULED (reviewer) | NO_SIGNAL_AMBIGUOUS_BOTH_SIDES added to the code list. | GV-P22-B05 |
| A-30 | MEDIUM | Executable-price quantisation | RULED (reviewer, new) | Exact internally; stops away from entry, fixed-R/Fibonacci/measured targets in the profit direction, structural targets toward entry, stop-entry triggers in the trigger direction; virtual trade and Vantage mirror share the levels. | GV-G-QT-01, GV-P01-Q01, GV-P08-Q01, GV-P08-Q02, GV-P08-Q03, GV-P16-Q01, GV-P20-V01, GV-E2E-02 |

## Observations (not ambiguities)

- **O-1** No ACTIVE variant can qualify without its BASE pattern: every variant with a relaxed prior state or wider tolerance is a pip-dependent SRC-PS variant, disabled by D-032. The `base_formed=false` path appears only in DORMANT vectors (GV-DORM-*).
- **O-2** The early setups test the BID in both directions, so the bear side is not the price mirror of the bull side (a mirror of a bid test is an ask test). Their bear vectors are hand-written.
- **O-3** The Dragonfly/Gravestone clause `LW >= 0.80*R` is implied by `DOJI` and `UW <= 0.05*R` and can never fail alone (GV-P04-N04).
- **O-4** For Abandoned Baby (completed and early) the SRC-PS stop equals the BASE stop by construction.
- **O-5** G2 size-class boundaries are tested once globally (GV-G-CLS-01..03) and again as single-clause probes inside the patterns that use them.
- **O-6** End-to-end wiring exists for ATR (three cases), the trend/zone/entry-snapshot/target pipeline (GV-E2E-02) and RSI (GV-E2E-03); more can be added once a detector exists.
