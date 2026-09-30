# Hub counter vectors

How the hub's counters must behave (D-022/D-023/D-025). **Canonical counters** (`shapes`, `base_formed`) are stored ONCE per pattern × side × timeframe × version; **variant counters** (`qualified`, `signals`, `trades`, skips, open/closed, P&L) per pattern × side × timeframe × variant × version. P&L is in R, dollars (1R = $100 on the fixed $10,000 reference, non-compounding) and percent (1R = 1.00%).

#### `GV-HUB-01`
> Four H1 occurrences of the same candle pair (a: all three variants trade and win; b: BASE only, stopped; c: UPTREND so shape only; d: CB skipped for RR, BASE and SH still open). Formation counters are stored ONCE per pattern x TF (shapes 4, base_formed 3), not once per variant; qualified/signals/trades/skips/P&L are per variant. BASE: 3 trades (2 closed +2R and -1R = +1R = +$100 = +1.00% of the $10,000 reference; 1 open). CB: qualified 2, trades 1, one SKIPPED_SRC_RR. SH: qualified 2, trades 2 (1 closed +2R, 1 open).

**Occurrence 1** (H1) — context: atr=4 · trend=DOWN · rsi=25 · zones_pre=[4202.50-4202.60] · zones_entry=[4231.00-4232.00]
bars: 4210.00/4211.00/4203.00/4204.00 ; 4203.50/4212.50/4203.00/4212.00
ticks (bid/ask): 09-16 12:00:02 4212.00/4212.20; 09-16 12:01:40 4231.00/4231.20

**Occurrence 2** (H1) — context: atr=4 · trend=DOWN · rsi=40 · zones_entry=[4231.00-4232.00]
bars: 4210.00/4211.00/4203.00/4204.00 ; 4203.50/4212.50/4203.00/4212.00
ticks (bid/ask): 09-16 12:00:02 4212.00/4212.20; 09-16 12:01:40 4202.80/4203.00

**Occurrence 3** (H1) — context: atr=4 · trend=UP · rsi=25 · zones_pre=[4202.50-4202.60] · zones_entry=[4231.00-4232.00]
bars: 4210.00/4211.00/4203.00/4204.00 ; 4203.50/4212.50/4203.00/4212.00
ticks (bid/ask): 09-16 12:00:02 4212.00/4212.20

**Occurrence 4** (H1) — context: atr=4 · trend=DOWN · rsi=25 · zones_pre=[4202.50-4202.60] · zones_entry=[4230.99-4232.00]
bars: 4210.00/4211.00/4203.00/4204.00 ; 4203.50/4212.50/4203.00/4212.00
ticks (bid/ask): 09-16 12:00:02 4212.00/4212.20

Strategies: `GT-ENGULF-BULL-v1.0/BASE`, `GT-ENGULF-BULL-v1.0/SRC-CB`, `GT-ENGULF-BULL-v1.0/SRC-SH`

Expected counters:
```json
{
 "canonical": {
  "GT-ENGULF-BULL-v1.0|H1": {
   "shapes": 4,
   "base_formed": 3
  }
 },
 "variants": {
  "GT-ENGULF-BULL-v1.0|H1|BASE": {
   "status": "ACTIVE",
   "qualified": 3,
   "signals": 3,
   "trades": 3,
   "open": 1,
   "closed": 2,
   "pnl_r": "1.00",
   "pnl_usd": "100.00",
   "pnl_pct": "1.00",
   "skips": {}
  },
  "GT-ENGULF-BULL-v1.0|H1|SRC-CB": {
   "status": "ACTIVE",
   "qualified": 2,
   "signals": 2,
   "trades": 1,
   "open": 0,
   "closed": 1,
   "pnl_r": "2.00",
   "pnl_usd": "200.00",
   "pnl_pct": "2.00",
   "skips": {
    "SKIPPED_SRC_RR": 1
   }
  },
  "GT-ENGULF-BULL-v1.0|H1|SRC-SH": {
   "status": "ACTIVE",
   "qualified": 2,
   "signals": 2,
   "trades": 2,
   "open": 1,
   "closed": 1,
   "pnl_r": "2.00",
   "pnl_usd": "200.00",
   "pnl_pct": "2.00",
   "skips": {}
  }
 }
}
```

#### `GV-HUB-02`
> Hammer, two M15 occurrences: #1 trend DOWN (BASE trades and wins +2R); #2 trend RANGE at support (shape only for BASE; the SRC-PS variant would qualify but it is DISABLED_PENDING_PIP_CONFIRMATION). Canonical: shapes 2, base_formed 1. BASE: qualified 1, trades 1, closed 1, +2.00R. SRC-PS: status disabled, every counter 0.

**Occurrence 1** (M15) — context: atr=4 · trend=DOWN
bars: 4200.00/4200.50/4194.00/4200.20
ticks (bid/ask): 09-16 10:15:02 4200.20/4200.40; 09-16 10:16:40 4213.60/4213.80

**Occurrence 2** (M15) — context: atr=4 · trend=RANGE · zones_pre=[4193.50-4193.90]
bars: 4200.00/4200.50/4194.00/4200.20
ticks (bid/ask): 09-16 10:15:02 4200.20/4200.40

Strategies: `GT-HAMMER-BULL-v1.0/BASE`, `GT-HAMMER-BULL-v1.0/SRC-PS`

Expected counters:
```json
{
 "canonical": {
  "GT-HAMMER-BULL-v1.0|M15": {
   "shapes": 2,
   "base_formed": 1
  }
 },
 "variants": {
  "GT-HAMMER-BULL-v1.0|M15|BASE": {
   "status": "ACTIVE",
   "qualified": 1,
   "signals": 1,
   "trades": 1,
   "open": 0,
   "closed": 1,
   "pnl_r": "2.00",
   "pnl_usd": "200.00",
   "pnl_pct": "2.00"
  },
  "GT-HAMMER-BULL-v1.0|M15|SRC-PS": {
   "status": "DISABLED_PENDING_PIP_CONFIRMATION",
   "qualified": 0,
   "signals": 0,
   "trades": 0,
   "open": 0,
   "closed": 0,
   "pnl_r": "0.00"
  }
 }
}
```

#### `GV-HUB-03`
> The same Hammer candle on M15 (wins +2R) and on H1 (stopped -1R): two SEPARATE ledgers, never pooled (D-011). The card for an all-timeframe total would be a label 'sum of separate ledgers', not a strategy result.

**Occurrence 1** (M15) — context: atr=4 · trend=DOWN
bars: 4200.00/4200.50/4194.00/4200.20
ticks (bid/ask): 09-16 10:15:02 4200.20/4200.40; 09-16 10:16:40 4213.60/4213.80

**Occurrence 2** (H1) — context: atr=4 · trend=DOWN
bars: 4200.00/4200.50/4194.00/4200.20
ticks (bid/ask): 09-16 11:00:02 4200.20/4200.40; 09-16 11:01:40 4193.80/4194.00

Strategies: `GT-HAMMER-BULL-v1.0/BASE`

Expected counters:
```json
{
 "canonical": {
  "GT-HAMMER-BULL-v1.0|M15": {
   "shapes": 1,
   "base_formed": 1
  },
  "GT-HAMMER-BULL-v1.0|H1": {
   "shapes": 1,
   "base_formed": 1
  }
 },
 "variants": {
  "GT-HAMMER-BULL-v1.0|M15|BASE": {
   "trades": 1,
   "closed": 1,
   "pnl_r": "2.00",
   "pnl_usd": "200.00"
  },
  "GT-HAMMER-BULL-v1.0|H1|BASE": {
   "trades": 1,
   "closed": 1,
   "pnl_r": "-1.00",
   "pnl_usd": "-100.00",
   "pnl_pct": "-1.00"
  }
 }
}
```

#### `GV-HUB-04`
> Kicker Early (trigger at the open tick after C1) and Kicker (completed, needs C2) are separate pattern identities with separate counters. One early trigger occurrence: entry ask 4210.20, stop 4203.30, target 4224.00 hit = +2R. The completed Kicker on the same two candles is HUB-05; each identity keeps its own shapes/base_formed.

**Occurrence 1** (M15) — context: atr=4 · trend=DOWN
bars: 4210.00/4210.50/4203.50/4204.00
ticks (bid/ask): 09-16 10:15:00 4210.00/4210.20; 09-16 10:16:40 4224.00/4224.20

Strategies: `GT-KICKEREARLY-BULL-v1.0/BASE-EARLY`

Expected counters:
```json
{
 "canonical": {
  "GT-KICKEREARLY-BULL-v1.0|M15": {
   "shapes": 1,
   "base_formed": 1
  }
 },
 "variants": {
  "GT-KICKEREARLY-BULL-v1.0|M15|BASE-EARLY": {
   "qualified": 1,
   "signals": 1,
   "trades": 1,
   "closed": 1,
   "pnl_r": "2.00"
  }
 }
}
```

#### `GV-HUB-05`
> The same two candles seen by the completed Kicker: its own counters are separate (shapes 1, base_formed 1, trades 1, still open).

**Occurrence 1** (M15) — context: atr=4 · trend=DOWN
bars: 4210.00/4210.50/4203.50/4204.00 ; 4211.00/4218.00/4210.50/4217.80
ticks (bid/ask): 09-16 10:30:02 4217.80/4218.00

Strategies: `GT-KICKER-BULL-v1.0/BASE`

Expected counters:
```json
{
 "canonical": {
  "GT-KICKER-BULL-v1.0|M15": {
   "shapes": 1,
   "base_formed": 1
  }
 },
 "variants": {
  "GT-KICKER-BULL-v1.0|M15|BASE": {
   "qualified": 1,
   "signals": 1,
   "trades": 1,
   "open": 1,
   "closed": 0
  }
 }
}
```

