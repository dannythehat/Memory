# Read-only probe proving identity-order dependence is NOT confined to the parent cap (§3.4.1).
# Run from the Aidy-Gold-Signals repo root: uv run python <this file>
"""Is Build-20's PRE-parent-cap dependency multiplier also identity-order dependent?"""
from decimal import Decimal as D
from aidy.gold_evidence_dependency import build_evidence_dependency_engine
AS_OF = "2026-09-22T12:00:00+00:00"

def sig(sid, fam, grp, vote, ev, raw="1"):
    return {"signal_id": sid, "gate_id": sid.split(":")[0], "calculator_id": sid,
            "dependency_family": fam, "correlation_group": grp,
            "role": "directional", "state": "known", "vote": vote,
            "raw_weight": raw, "evidence_identity": ev}

def show(label, sigs):
    eng = build_evidence_dependency_engine(signals=sigs, historical_rows=[], as_of_utc=AS_OF)
    print(f"--- {label}")
    for r in sorted(eng["adjustments"]["adjusted_signals"], key=lambda x: x["signal_id"]):
        print(f"    {r['signal_id']:<10} pre_cap={r['dependency_multiplier_pre_parent_cap']:>9} "
              f"eff={r['effective_weight']:>9}  {','.join(r['adjustment_reasons']) or '-'}")

# CASE 1: two signals, SAME correlation group, SAME vote (same-family damping applies)
show("same correlation_group, same vote: ids aaa/zzz",
     [sig("aaa:p","structure","cg_shared","bullish","ev1"),
      sig("zzz:q","structure","cg_shared","bullish","ev2")])
show("same set RENAMED to yyy/bbb",
     [sig("yyy:p","structure","cg_shared","bullish","ev1"),
      sig("bbb:q","structure","cg_shared","bullish","ev2")])

# CASE 2: exact duplicates (same evidence_identity AND vote)
show("exact duplicates: ids aaa/zzz",
     [sig("aaa:p","structure","cg_a","bullish","EVSAME"),
      sig("zzz:q","structure","cg_b","bullish","EVSAME")])
show("exact duplicates RENAMED to yyy/bbb",
     [sig("yyy:p","structure","cg_a","bullish","EVSAME"),
      sig("bbb:q","structure","cg_b","bullish","EVSAME")])
