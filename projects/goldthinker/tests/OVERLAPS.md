# Overlap (multi-strategy) vectors

Several strategies read the SAME candles. Each strategy still produces its own detection/counters; detections completing on the same bar, same TF and same direction share one `cluster_id` (spec G11). `formed` detections only.

#### `GV-OV-01` · M15
> One candle (O 4199.80, H 4200.00, L 4194.00, C 4199.90) is legitimately a Hammer, a Dragonfly Doji and a bullish Pin Bar. All three form on the same bar in the same direction: three detections, ONE cluster (G11). Each is traded/counted separately by its own strategy.

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4199.80 | 4200.00 | 4194.00 | 4199.90 |

| strategy | expected |
|---|---|
| `GT-HAMMER-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |
| `GT-DRAGONFLY-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |
| `GT-PINBAR-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-HAMMER-BULL-v1.0`, `GT-DRAGONFLY-BULL-v1.0`, `GT-PINBAR-BULL-v1.0`}

#### `GV-OV-01m` · M15
*Mirror of `GV-OV-01`.*
> One candle (O 4199.80, H 4200.00, L 4194.00, C 4199.90) is legitimately a Hammer, a Dragonfly Doji and a bullish Pin Bar. All three form on the same bar in the same direction: three detections, ONE cluster (G11). Each is traded/counted separately by its own strategy.

Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.20 | 4206.00 | 4200.00 | 4200.10 |

| strategy | expected |
|---|---|
| `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |
| `GT-GRAVESTONE-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |
| `GT-PINBAR-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-SHOOTINGSTAR-BEAR-v1.0`, `GT-GRAVESTONE-BEAR-v1.0`, `GT-PINBAR-BEAR-v1.0`}

#### `GV-OV-02` · M15
> Same candle after an UPTREND: Hammer and Dragonfly are shapes only (Hanging Man candidate logged for the hammer); only the Pin Bar (no prior-state rule) forms. Only formed detections cluster.

Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4199.80 | 4200.00 | 4194.00 | 4199.90 |

| strategy | expected |
|---|---|
| `GT-HAMMER-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED; candidate: HANGING_MAN |
| `GT-DRAGONFLY-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED; candidate: None |
| `GT-PINBAR-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-PINBAR-BULL-v1.0`}

#### `GV-OV-02m` · M15
*Mirror of `GV-OV-02`.*
> Same candle after an UPTREND: Hammer and Dragonfly are shapes only (Hanging Man candidate logged for the hammer); only the Pin Bar (no prior-state rule) forms. Only formed detections cluster.

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4200.20 | 4206.00 | 4200.00 | 4200.10 |

| strategy | expected |
|---|---|
| `GT-SHOOTINGSTAR-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED; candidate: INVERTED_HAMMER |
| `GT-GRAVESTONE-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED; candidate: None |
| `GT-PINBAR-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-PINBAR-BEAR-v1.0`}

#### `GV-OV-03` · M15
> C2 engulfs C1's body AND its wicks: Bullish Engulfing and (bullish) Outside Bar both form on the same bar: one cluster.

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:15 | 4203.50 | 4212.50 | 4202.50 | 4212.00 |

| strategy | expected |
|---|---|
| `GT-ENGULF-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; flags: wicks_engulfed=True |
| `GT-OUTSIDE-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-ENGULF-BULL-v1.0`, `GT-OUTSIDE-BULL-v1.0`}

#### `GV-OV-03m` · M15
*Mirror of `GV-OV-03`.*
> C2 engulfs C1's body AND its wicks: Bullish Engulfing and (bullish) Outside Bar both form on the same bar: one cluster.

Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.00 | 4196.00 |
| 2 | 09-16 10:15 | 4196.50 | 4197.50 | 4187.50 | 4188.00 |

| strategy | expected |
|---|---|
| `GT-ENGULF-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; flags: wicks_engulfed=True |
| `GT-OUTSIDE-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-ENGULF-BEAR-v1.0`, `GT-OUTSIDE-BEAR-v1.0`}

#### `GV-OV-04` · M15
> Same bars in an UPTREND: the engulfing is only logged as an ENGULF_CONTINUATION candidate; the Outside Bar (no prior state) still forms.

Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4211.00 | 4203.00 | 4204.00 |
| 2 | 09-16 10:15 | 4203.50 | 4212.50 | 4202.50 | 4212.00 |

| strategy | expected |
|---|---|
| `GT-ENGULF-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED; candidate: ENGULF_CONTINUATION |
| `GT-OUTSIDE-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-OUTSIDE-BULL-v1.0`}

#### `GV-OV-04m` · M15
*Mirror of `GV-OV-04`.*
> Same bars in an UPTREND: the engulfing is only logged as an ENGULF_CONTINUATION candidate; the Outside Bar (no prior state) still forms.

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4197.00 | 4189.00 | 4196.00 |
| 2 | 09-16 10:15 | 4196.50 | 4197.50 | 4187.50 | 4188.00 |

| strategy | expected |
|---|---|
| `GT-ENGULF-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED; candidate: ENGULF_CONTINUATION |
| `GT-OUTSIDE-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-OUTSIDE-BEAR-v1.0`}

#### `GV-OV-05` · M15
> Tweezer Bottom (lows 0.10 apart) that is also a Bullish Engulfing (O2 <= C1, C2 = O1, B2 5.5 > B1 5.0): both form, one cluster.

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4205.00 | 4206.00 | 4199.00 | 4200.00 |
| 2 | 09-16 10:15 | 4199.50 | 4205.50 | 4199.10 | 4205.00 |

| strategy | expected |
|---|---|
| `GT-ENGULF-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |
| `GT-TWEEZERBOTTOM-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-ENGULF-BULL-v1.0`, `GT-TWEEZERBOTTOM-BULL-v1.0`}

#### `GV-OV-05m` · M15
*Mirror of `GV-OV-05`.*
> Tweezer Bottom (lows 0.10 apart) that is also a Bullish Engulfing (O2 <= C1, C2 = O1, B2 5.5 > B1 5.0): both form, one cluster.

Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4195.00 | 4201.00 | 4194.00 | 4200.00 |
| 2 | 09-16 10:15 | 4200.50 | 4200.90 | 4194.50 | 4195.00 |

| strategy | expected |
|---|---|
| `GT-ENGULF-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |
| `GT-TWEEZERTOP-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-ENGULF-BEAR-v1.0`, `GT-TWEEZERTOP-BEAR-v1.0`}

#### `GV-OV-06` · M15
> C2 closes 4209.99, 0.01 below O1 4210.00: Piercing Line forms, Bullish Engulfing does not (C2>=O1 fails). The equality boundary splits the two.

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4203.00 | 4209.99 | 4202.50 | 4209.99 |

| strategy | expected |
|---|---|
| `GT-PIERCING-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |
| `GT-ENGULF-BULL-v1.0/BASE` | canonical: no event; failing clause(s): C2>=O1 |

Clusters (formed detections sharing a bar/direction): {`GT-PIERCING-BULL-v1.0`}

#### `GV-OV-06m` · M15
*Mirror of `GV-OV-06`.*
> C2 closes 4209.99, 0.01 below O1 4210.00: Piercing Line forms, Bullish Engulfing does not (C2>=O1 fails). The equality boundary splits the two.

Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4197.00 | 4197.50 | 4190.01 | 4190.01 |

| strategy | expected |
|---|---|
| `GT-DARKCLOUD-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |
| `GT-ENGULF-BEAR-v1.0/BASE` | canonical: no event; failing clauses: 1 |

Clusters (formed detections sharing a bar/direction): {`GT-DARKCLOUD-BEAR-v1.0`}

#### `GV-OV-07` · M15
> C2 closes exactly at O1 (4210.00): Bullish Engulfing forms, Piercing Line does not (C2<O1 is strict). No bar can be both.

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4203.00 | 4210.50 | 4202.50 | 4210.00 |

| strategy | expected |
|---|---|
| `GT-PIERCING-BULL-v1.0/BASE` | canonical: no event; failing clause(s): C2<O1 |
| `GT-ENGULF-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-ENGULF-BULL-v1.0`}

#### `GV-OV-07m` · M15
*Mirror of `GV-OV-07`.*
> C2 closes exactly at O1 (4210.00): Bullish Engulfing forms, Piercing Line does not (C2<O1 is strict). No bar can be both.

Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4197.00 | 4197.50 | 4189.50 | 4190.00 |

| strategy | expected |
|---|---|
| `GT-DARKCLOUD-BEAR-v1.0/BASE` | canonical: no event; failing clauses: 1 |
| `GT-ENGULF-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-ENGULF-BEAR-v1.0`}

#### `GV-OV-08` · M15
> A true Abandoned Baby (gaps on both sides of the doji) is also a valid Morning Star (P19 field 21: subset). Both form on the C3 bar: one cluster.

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4202.80 | 4203.20 | 4201.80 | 4202.85 |
| 3 | 09-16 10:30 | 4204.00 | 4209.50 | 4203.50 | 4209.20 |

| strategy | expected |
|---|---|
| `GT-MORNINGSTAR-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |
| `GT-ABABY-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-MORNINGSTAR-BULL-v1.0`, `GT-ABABY-BULL-v1.0`}

#### `GV-OV-08m` · M15
*Mirror of `GV-OV-08`.*
> A true Abandoned Baby (gaps on both sides of the doji) is also a valid Morning Star (P19 field 21: subset). Both form on the C3 bar: one cluster.

Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4190.00 | 4196.50 | 4189.50 | 4196.00 |
| 2 | 09-16 10:15 | 4197.20 | 4198.20 | 4196.80 | 4197.15 |
| 3 | 09-16 10:30 | 4196.00 | 4196.50 | 4190.50 | 4190.80 |

| strategy | expected |
|---|---|
| `GT-EVENINGSTAR-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |
| `GT-ABABY-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-EVENINGSTAR-BEAR-v1.0`, `GT-ABABY-BEAR-v1.0`}

#### `GV-OV-09` · M15
> Inside bar followed by a bar that pierces the mother low and closes back inside: P22 (Sweep & Reclaim) signals on bar 3. The Inside-Bar-Breakout (P09) is formed at bar 2 but has NO breakout close and is still waiting (window bars 3-5). The two are different detections completing on different bars, so they do not share a cluster.

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4212.00 | 4215.00 | 4200.00 | 4204.00 |
| 2 | 09-16 10:15 | 4206.00 | 4210.00 | 4203.00 | 4209.00 |
| 3 | 09-16 10:30 | 4207.00 | 4209.00 | 4199.50 | 4206.00 |

| strategy | expected |
|---|---|
| `GT-INSIDE-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED; disposition: PENDING_BREAKOUT |
| `GT-IBSR-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL |

Clusters (formed detections sharing a bar/direction): {`GT-INSIDE-BULL-v1.0`} ; {`GT-IBSR-BULL-v1.0`}

#### `GV-OV-09m` · M15
*Mirror of `GV-OV-09`.*
> Inside bar followed by a bar that pierces the mother low and closes back inside: P22 (Sweep & Reclaim) signals on bar 3. The Inside-Bar-Breakout (P09) is formed at bar 2 but has NO breakout close and is still waiting (window bars 3-5). The two are different detections completing on different bars, so they do not share a cluster.

Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4188.00 | 4200.00 | 4185.00 | 4196.00 |
| 2 | 09-16 10:15 | 4194.00 | 4197.00 | 4190.00 | 4191.00 |
| 3 | 09-16 10:30 | 4193.00 | 4200.50 | 4191.00 | 4194.00 |

| strategy | expected |
|---|---|
| `GT-INSIDE-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED; disposition: PENDING_BREAKOUT |
| `GT-IBSR-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL |

Clusters (formed detections sharing a bar/direction): {`GT-INSIDE-BEAR-v1.0`} ; {`GT-IBSR-BEAR-v1.0`}

#### `GV-OV-10` · M15
> The same idea with the full 5-bar window: the sweep bar never closed outside, so P09 expires (EXPIRED_NO_CONFIRMATION) while P22 remains a valid signal on bar 3.

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4212.00 | 4215.00 | 4200.00 | 4204.00 |
| 2 | 09-16 10:15 | 4206.00 | 4210.00 | 4203.00 | 4209.00 |
| 3 | 09-16 10:30 | 4207.00 | 4209.00 | 4199.50 | 4206.00 |
| 4 | 09-16 10:45 | 4206.00 | 4209.00 | 4203.50 | 4207.00 |
| 5 | 09-16 11:00 | 4207.00 | 4209.50 | 4203.60 | 4208.00 |

| strategy | expected |
|---|---|
| `GT-INSIDE-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED; disposition: EXPIRED_NO_CONFIRMATION |
| `GT-IBSR-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL |

Clusters (formed detections sharing a bar/direction): {`GT-INSIDE-BULL-v1.0`} ; {`GT-IBSR-BULL-v1.0`}

#### `GV-OV-10m` · M15
*Mirror of `GV-OV-10`.*
> The same idea with the full 5-bar window: the sweep bar never closed outside, so P09 expires (EXPIRED_NO_CONFIRMATION) while P22 remains a valid signal on bar 3.

Context: atr=4 · trend=UP

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4188.00 | 4200.00 | 4185.00 | 4196.00 |
| 2 | 09-16 10:15 | 4194.00 | 4197.00 | 4190.00 | 4191.00 |
| 3 | 09-16 10:30 | 4193.00 | 4200.50 | 4191.00 | 4194.00 |
| 4 | 09-16 10:45 | 4194.00 | 4196.50 | 4191.00 | 4193.00 |
| 5 | 09-16 11:00 | 4193.00 | 4196.40 | 4190.50 | 4192.00 |

| strategy | expected |
|---|---|
| `GT-INSIDE-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED; disposition: EXPIRED_NO_CONFIRMATION |
| `GT-IBSR-BEAR-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED; variant: VARIANT_QUALIFIED, SIGNAL |

Clusters (formed detections sharing a bar/direction): {`GT-INSIDE-BEAR-v1.0`} ; {`GT-IBSR-BEAR-v1.0`}

#### `GV-OV-11` · M15
> Early Kicker (fires at K2's opening tick; formation_end = K1) and the completed Kicker (K2 closes; formation_end = K2) exist for the same two candles. Ruling A-21: they have DIFFERENT formation clusters (formation_end_bar differs) but the SAME signal cluster (both signal on K2 in the same direction), which is exactly what the two ids are for.

Context: atr=4 · trend=DOWN

| # | open (UTC) | O | H | L | C |
|---|---|---|---|---|---|
| 1 | 09-16 10:00 | 4210.00 | 4210.50 | 4203.50 | 4204.00 |
| 2 | 09-16 10:15 | 4211.00 | 4218.00 | 4210.50 | 4217.80 |

Ticks (bid/ask): 09-16 10:15:00 4210.00/4210.20

| strategy | expected |
|---|---|
| `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |
| `GT-KICKER-BULL-v1.0/BASE` | canonical: SHAPE_DETECTED, BASE_PATTERN_FORMED |

Clusters (formed detections sharing a bar/direction): {`GT-KICKEREARLY-BULL-v1.0`} ; {`GT-KICKER-BULL-v1.0`}

