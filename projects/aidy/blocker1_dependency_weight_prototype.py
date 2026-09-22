# Verified prototype of the v6 order-independent dependency weight d_i (§3.4.3).
# Pure arithmetic, no AIDY imports. Run: python3 <this file>
"""Prototype of the v6 order-independent dependency weight d_i.
Uses Build-20 STRUCTURAL facts (correlation_group, evidence_identity, high_dependency pairs)
but NOT its sequential per-signal multipliers or parent cap.
Verifies rename-invariance including the tied-reliability case."""
from decimal import Decimal as D
from itertools import permutations

def cluster_ids(contribs, high_dep_pairs):
    """Union-find over correlation_groups, merged by (a) shared evidence_identity and
    (b) empirical high-dependency pairs. Identical evidence is one cluster by definition."""
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[max(ra, rb)] = min(ra, rb)   # deterministic, value-based
    for c in contribs: find(c["correlation_group"])
    by_ev = {}
    for c in contribs:
        by_ev.setdefault(c["evidence_identity"], []).append(c["correlation_group"])
    for _, groups in by_ev.items():
        for g in groups[1:]:
            union(groups[0], g)
    for a, b in high_dep_pairs: union(a, b)
    return {c["signal_id"]: find(c["correlation_group"]) for c in contribs}

def compute_p(contribs, high_dep_pairs):
    # STEP 1: collapse exact duplicates ACROSS THE WHOLE FAMILY, by (evidence_identity, vote).
    dup = {}
    for m in contribs:
        dup.setdefault((m["evidence_identity"], m["vote"]), []).append(m)
    survivors = []   # (contributor, within-duplicate share)
    for _, grp in dup.items():
        best = max(D(g["r"]) for g in grp)
        tied = [g for g in grp if D(g["r"]) == best]          # ties -> symmetric split
        for g in tied:
            survivors.append((g, D(1) / D(len(tied))))
    # STEP 2: cluster the survivors (union-find over correlation groups + high-dependency pairs)
    surv_c = [g for g, _ in survivors]
    cl = cluster_ids(surv_c, high_dep_pairs)
    clusters = {}
    for g, share in survivors:
        clusters.setdefault(cl[g["signal_id"]], []).append((g, share))
    # STEP 3: each cluster contributes ONE unit, split among its surviving slots
    d = {}
    for _, members in clusters.items():
        slots = sum(share for _, share in members)
        for g, share in members:
            d[g["signal_id"]] = (D(1) / D(len(clusters))) * (share / slots)
    tot = sum(d.values())
    return {k: (v / tot) for k, v in d.items()}

def C(sid, grp, vote, ev, r):
    return {"signal_id": sid, "correlation_group": grp, "vote": vote,
            "evidence_identity": ev, "r": r}

def mass(contribs, high=()):
    p = compute_p(contribs, high)
    bull = sum(p[c["signal_id"]] * D(c["r"]) for c in contribs if c["vote"] == "bullish")
    bear = sum(p[c["signal_id"]] * D(c["r"]) for c in contribs if c["vote"] == "bearish")
    return bull - bear

BASE = [C("m5s","cg_a","bullish","ev1","0.60"), C("m15s","cg_a","bullish","ev2","0.55"),
        C("h1s","cg_b","bullish","ev3","0.45"), C("momi","cg_c","neutral","ev4","0.50")]
print("signed evidence, base names      :", f"{mass(BASE):.9f}")

# rename every signal_id, keep everything else identical
REN = [dict(c, signal_id=f"zz_{c['signal_id']}") for c in BASE]
print("signed evidence, all renamed     :", f"{mass(REN):.9f}")

# TIED reliability, opposing votes, different ids -- the case that broke v5
TIE = [C("aaa","cg_x","bullish","evA","0.50"), C("zzz","cg_x","bearish","evB","0.50"),
       C("mmm","cg_y","bullish","evC","0.40")]
print("tied reliability, base names     :", f"{mass(TIE):.9f}")
TIE2 = [C("yyy","cg_x","bullish","evA","0.50"), C("bbb","cg_x","bearish","evB","0.50"),
        C("nnn","cg_y","bullish","evC","0.40")]
print("tied reliability, renamed        :", f"{mass(TIE2):.9f}")

# exact duplicates with TIED reliability -> symmetric split, must be rename-proof
DUP  = [C("aaa","cg_x","bullish","SAME","0.50"), C("zzz","cg_y","bullish","SAME","0.50"),
        C("mmm","cg_z","bearish","evD","0.30")]
DUP2 = [C("yyy","cg_x","bullish","SAME","0.50"), C("bbb","cg_y","bullish","SAME","0.50"),
        C("nnn","cg_z","bearish","evD","0.30")]
print("tied exact duplicates, base      :", f"{mass(DUP):.9f}")
print("tied exact duplicates, renamed   :", f"{mass(DUP2):.9f}")

# input ORDER invariance (not just names)
vals = {f"{mass(list(perm)):.9f}" for perm in permutations(BASE)}
print("distinct results over all 24 input orderings:", len(vals), "->", vals)
