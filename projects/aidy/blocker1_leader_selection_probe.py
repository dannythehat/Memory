# Read-only probe demonstrating the §3.4.1 alphabetical-leader defect.
# Run from the Aidy-Gold-Signals repo root with: uv run python <this file>.
"""Is the family leader chosen by evidence quality, or by alphabetical signal_id?"""
from decimal import Decimal
from aidy.gold_evidence_dependency import build_evidence_dependency_engine
AS_OF = "2026-09-22T12:00:00+00:00"

def sig(sid, family, group, vote, raw="1"):
    return {"signal_id": sid, "gate_id": sid.split(":")[0], "calculator_id": sid,
            "dependency_family": family, "correlation_group": group,
            "role": "directional", "state": "known", "vote": vote,
            "raw_weight": raw, "evidence_identity": f"ev_{sid}"}

def leader_of(sigs):
    eng = build_evidence_dependency_engine(signals=sigs, historical_rows=[], as_of_utc=AS_OF)
    rows = [r for r in eng["adjustments"]["adjusted_signals"] if r["parent_family"]=="price_action"]
    return max(rows, key=lambda r: Decimal(r["effective_weight"]))["signal_id"]

# Case 1: all raw weights equal -> who leads?
A = [sig("aaa:x","structure","cg1","bullish"), sig("zzz:y","structure","cg2","bullish"),
     sig("mmm:z","momentum","cg3","bearish")]
print("equal raw weights, leader =", leader_of(A))

# Case 2: identical set, but rename so a different id sorts first
B = [sig("bbb:x","structure","cg1","bullish"), sig("aab:y","structure","cg2","bullish"),
     sig("mmm:z","momentum","cg3","bearish")]
print("equal raw weights, renamed,  leader =", leader_of(B))

# Case 3: give the LAST-sorting signal a higher raw weight (i.e. reliability-informed)
C = [sig("aaa:x","structure","cg1","bullish","0.30"), sig("zzz:y","structure","cg2","bullish","0.90"),
     sig("mmm:z","momentum","cg3","bearish","0.20")]
print("raw weights differ,          leader =", leader_of(C))
