# Read-only derivation script used to produce the frozen T1 Scenario A fixture in
# BLOCKER1_AGGREGATION_PREREGISTRATION.md. Run from the Aidy-Gold-Signals repo root
# with: uv run python <this file>. Touches nothing; prints engine output only.
"""T1 Scenario A: derive REAL u_i with raw_weights = reliability_i, then Stage B/C."""
from decimal import Decimal as D
from aidy.gold_evidence_dependency import build_evidence_dependency_engine
AS_OF = "2026-09-22T12:00:00+00:00"

# (signal_id, family, correlation_group, vote, reliability)
SPEC = [
    ("h1s:trend",  "structure", "cg_h1",  "bullish", "0.45"),
    ("m15s:break", "structure", "cg_m15", "bullish", "0.55"),
    ("m5s:accept", "structure", "cg_m5",  "bullish", "0.60"),
    ("h4s:swing",  "structure", "cg_h4",  "bullish", "0.45"),
    ("momi:eff",   "momentum",  "cg_mom", "neutral", "0.50"),
    ("locr:conf",  "location",  "cg_loc", "neutral", "0.45"),
    ("liqp:depth", "liquidity", "cg_lq1", "bullish", "0.50"),
    ("liqr:speed", "liquidity", "cg_lq2", "bullish", "0.40"),
]
REL = {s[0]: D(s[4]) for s in SPEC}

signals, raw_weights = [], {}
for sid, fam, grp, vote, rel in SPEC:
    signals.append({"signal_id": sid, "gate_id": sid.split(":")[0], "calculator_id": sid,
                    "dependency_family": fam, "correlation_group": grp,
                    "role": "directional", "state": "known", "vote": vote,
                    "raw_weight": rel, "evidence_identity": f"ev_{sid}"})
    raw_weights[sid] = rel

eng = build_evidence_dependency_engine(signals=signals, historical_rows=[], as_of_utc=AS_OF)
rows = eng["adjustments"]["adjusted_signals"]

roots = {}
for r in rows:
    roots.setdefault(r["parent_family"], []).append(r)

S = W = D(0); qual = 0
print(f"{'root':<22} {'signal':<12} {'vote':<8} {'u':>9} {'p':>9} {'r':>6}")
for root, items in sorted(roots.items()):
    tot = sum(D(r["effective_weight"]) for r in items)
    bull = bear = D(0)
    for r in sorted(items, key=lambda x: -D(x["effective_weight"])):
        u = D(r["effective_weight"]); p = u/tot if tot else D(0); rel = REL[r["signal_id"]]
        if r["vote"] == "bullish": bull += p*rel
        elif r["vote"] == "bearish": bear += p*rel
        print(f"{root:<22} {r['signal_id']:<12} {r['vote']:<8} {u:>9} {p:>9.6f} {rel:>6}")
    signed = bull - bear; strength = abs(signed)
    fam_rel = bull + bear
    bal = (signed/fam_rel) if fam_rel else D(0)
    ok = strength >= D("0.20")
    qual += 1 if ok else 0
    S += signed; W += strength
    print(f"  -> {root}: bull={bull:.6f} bear={bear:.6f} signed={signed:.6f} "
          f"strength={strength:.6f} balance={bal:.6f} qualifying={ok}\n")

print(f"S={S:.6f}  W={W:.6f}  meta_balance={(S/W):.6f}  qualifying_families={qual}")
print("decision:", "BULLISH" if qual>=2 and abs(S/W)>=D("0.20") and S>0 else "see rules")
