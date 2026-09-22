#!/usr/bin/env python3
"""Deterministic generator for the frozen Blocker-1 T1 source state.

Pre-registration artefact. Every parameter below is FIXED. Output is byte-identical
on any machine (pure stdlib, no floats in the emitted JSON, sorted keys, fixed seed).
The SHA-256 of the emitted file is recorded in BLOCKER1_AGGREGATION_PREREGISTRATION.md
and must not change after approval.

Run:  python3 blocker1_t1_fixture_generator.py            # writes + prints digest
      python3 blocker1_t1_fixture_generator.py --verify    # verifies digest only
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from datetime import UTC, datetime, timedelta
from decimal import Decimal as D
from pathlib import Path

# ---------------------------------------------------------------- FROZEN PARAMETERS
SEED = 20260922
AS_OF = "2026-06-01T12:00:00+00:00"          # frozen decision time
HORIZON_MIN = 15
OUTCOME_N = 5000                              # resolved outcomes before AS_OF
CLASS_MIX = (("bearish", 2000), ("bullish", 2000), ("neutral", 1000))   # 40/40/20
NEUTRAL_BAND_BPS = D("2")
START_PRICE = D("3650.00")
M1_MINUTES = 2880                             # 2 days of M1, per _decision_candles window
TICK_BPS = D("0.8")                           # per-minute step scale

# Contributors: (signal_id, dependency_family, correlation_group, evidence_identity,
#                current_vote, target_N, target_excess)
# Reliability is DERIVED from the emitted history, never stated in the spec.
CONTRIBUTORS = (
    ("m5s:accept",  "structure", "cg_m5",  "ev_m5",  "bullish", 168, D("0.090")),
    ("m15s:break",  "structure", "cg_m15", "ev_m15", "bullish", 156, D("0.075")),
    ("h1s:trend",   "structure", "cg_h1",  "ev_h1",  "bullish", 144, D("0.060")),
    ("h4s:swing",   "structure", "cg_h4",  "ev_h4",  "bullish", 132, D("0.045")),
    ("momi:eff",    "momentum",  "cg_mom", "ev_mom", "neutral", 150, D("0.060")),
    ("locr:conf",   "location",  "cg_loc", "ev_loc", "neutral", 138, D("0.045")),
    ("liqp:depth",  "liquidity", "cg_lq1", "ev_lq1", "bullish", 162, D("0.075")),
    ("liqr:speed",  "liquidity", "cg_lq2", "ev_lq2", "bullish", 126, D("0.030")),
)
EXPECTED_GATE_N = 15
EXPECTED_ELIGIBLE_CONTRIBUTORS = 8
OUT = Path(__file__).with_name("blocker1_t1_full_fixture.json")


def _iso(dt: datetime) -> str:
    return dt.astimezone(UTC).isoformat()


def build() -> dict:
    rng = random.Random(SEED)
    as_of = datetime.fromisoformat(AS_OF)

    # ---- resolved outcome history (drives the PIT baseline estimator) ----
    classes: list[str] = []
    for label, count in CLASS_MIX:
        classes.extend([label] * count)
    rng.shuffle(classes)
    outcomes = []
    for i, label in enumerate(classes):
        resolved = as_of - timedelta(minutes=HORIZON_MIN * (OUTCOME_N - i))
        bps = {"bullish": D("7.5"), "bearish": D("-7.5"), "neutral": D("0.5")}[label]
        outcomes.append({
            "outcome_id": f"oc_{i:05d}",
            "resolved_at_utc": _iso(resolved),
            "realised_direction": label,
            "realised_return_bps": str(bps),
        })

    # ---- per-contributor commitment history, engineered to hit target_excess ----
    baseline = {c: D(n + 10) / D(OUTCOME_N + 30) for c, n in CLASS_MIX}
    histories = []
    for sid, fam, grp, ev, vote, n, target in CONTRIBUTORS:
        # a contributor's record is on DIRECTIONAL commitments only
        commit_class = "bullish" if vote != "bearish" else "bearish"
        base = baseline[commit_class]
        # correct_n chosen so (correct_n/n - base) is as close to target as integers allow
        correct_n = int((target + base) * D(n) + D("0.5"))
        correct_n = max(0, min(n, correct_n))
        rows = []
        for j in range(n):
            resolved = as_of - timedelta(minutes=HORIZON_MIN * (n - j) * 3)
            rows.append({
                "commitment_id": f"{sid}#{j:04d}",
                "resolved_at_utc": _iso(resolved),
                "predicted_class": commit_class,
                "correct": 1 if j < correct_n else 0,
            })
        histories.append({
            "signal_id": sid, "dependency_family": fam, "correlation_group": grp,
            "evidence_identity": ev, "current_vote": vote,
            "commitment_n": n, "correct_n": correct_n,
            "target_shrunk_excess": str(target), "commitments": rows,
        })

    # ---- deterministic M1 series (source for every timeframe aggregate) ----
    price = START_PRICE
    m1 = []
    for k in range(M1_MINUTES):
        step = D(rng.randint(-100, 100)) / D(100) * TICK_BPS * price / D(10000)
        o = price
        price = (price + step).quantize(D("0.01"))
        hi = max(o, price) + (D(rng.randint(0, 40)) / D(100))
        lo = min(o, price) - (D(rng.randint(0, 40)) / D(100))
        m1.append({
            "open_time_utc": _iso(as_of - timedelta(minutes=M1_MINUTES - k)),
            "open": str(o), "high": str(hi.quantize(D("0.01"))),
            "low": str(lo.quantize(D("0.01"))), "close": str(price),
            "first_observed_at": _iso(as_of - timedelta(minutes=M1_MINUTES - k)),
            "revision_index": 0,
        })

    return {
        "fixture_version": "blocker1_t1_full_fixture_v1",
        "generator_seed": SEED,
        "as_of_utc": AS_OF,
        "target_horizon_minutes": HORIZON_MIN,
        "neutral_band_bps": str(NEUTRAL_BAND_BPS),
        "expected_gate_n": EXPECTED_GATE_N,
        "expected_eligible_contributors": EXPECTED_ELIGIBLE_CONTRIBUTORS,
        "pit_baselines_at_as_of": {c: str(v) for c, v in baseline.items()},
        "resolved_outcome_history": outcomes,
        "contributor_histories": histories,
        "m1_series": m1,
        "research_only": True,
        "live_money_execution_allowed": False,
    }


def main() -> int:
    payload = json.dumps(build(), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    digest = hashlib.sha256(payload.encode()).hexdigest()
    if "--verify" in sys.argv:
        current = hashlib.sha256(OUT.read_bytes()).hexdigest() if OUT.exists() else None
        print(f"regenerated sha256 : {digest}")
        print(f"on-disk     sha256 : {current}")
        print("MATCH" if current == digest else "MISMATCH")
        return 0 if current == digest else 1
    OUT.write_text(payload, encoding="utf-8")
    print(f"wrote {OUT.name}  bytes={len(payload)}  sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
