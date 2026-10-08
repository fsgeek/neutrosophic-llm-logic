"""Within-register (sentence) residual, stratified by stimulus set and dispersion-matched.
Fixed by experiments/residual_stratified_prereg.md."""
from __future__ import annotations
import csv, numpy as np
from sentence_transformers import SentenceTransformer
JUDGE, JEV = "data/register2_labels.csv", "data/register2_jev_labels.csv"
ENCODERS = ["all-MiniLM-L6-v2", "all-mpnet-base-v2"]
SEED, TOL, N_B, MAX_TRIES, N_BOOT, FAIL_MAX = 0, 0.005, 1000, 20_000, 2000, 0.05
IGN, PAR, STRATA = "Ignorance (Epistemic)", "Paradox (Logical)", ["orig", "swap"]

def cov(EA, EB, sA):
    if len(EA) == 0 or len(EB) == 0: return 0.0
    m = (EA @ EB.T).max(axis=1); w = sA/sA.sum() if sA.sum() else np.ones(len(sA))/len(sA); return float((w*m).sum())
def asym(EA, SA, EB, SB): return (1-cov(EA, EB, SA)) - (1-cov(EB, EA, SB))
def disp(E):
    G = E @ E.T; iu = np.triu_indices(len(E), 1); return 1 - float(G[iu].mean())

def jev_labels():
    rows = list(csv.DictReader(open(JEV)))
    keyf = [c for c in ("source", "row", "item") if c in rows[0]]
    lab = "jev_label" if "jev_label" in rows[0] else "label"
    return {tuple(r[c] for c in keyf): r[lab] for r in rows}, keyf

def cells_of(items):  # items: list of (E, S, cell)
    by = {}
    for i, (_, _, c) in enumerate(items): by.setdefault(c, []).append(i)
    return by

def resample(items, rng):
    by = cells_of(items); keys = sorted(by)
    pick = rng.choice(len(keys), len(keys), replace=True)
    return [i for p in pick for i in by[keys[p]]]

def stratum_matched(I, P, rng):
    ia_all, ip_all = resample(I, rng), resample(P, rng)
    EI = np.array([I[i][0] for i in ia_all]); SI = np.array([I[i][1] for i in ia_all], dtype=np.float32)
    EP = np.array([P[i][0] for i in ip_all]); SP = np.array([P[i][1] for i in ip_all], dtype=np.float32)
    k = min(len(EI), len(EP))
    for _ in range(MAX_TRIES):
        a = rng.choice(len(EI), k, replace=False); b = rng.choice(len(EP), k, replace=False)
        if abs(disp(EI[a]) - disp(EP[b])) <= TOL:
            return asym(EI[a], SI[a], EP[b], SP[b])
    return None

def stratum_plain(I, P, rng):
    ia, ip = resample(I, rng), resample(P, rng)
    return asym(np.array([I[i][0] for i in ia]), np.array([I[i][1] for i in ia], dtype=np.float32),
                np.array([P[i][0] for i in ip]), np.array([P[i][1] for i in ip], dtype=np.float32))

def run(rows, label_of, model, tag):
    def items(ph, src, sentence_only=True):
        rs = [r for r in rows if r["phenomenon"] == ph and r["source"] == src and (not sentence_only or label_of(r) == "SENTENCE")]
        E = model.encode([f"{r['what']}. {r['why']}" for r in rs], normalize_embeddings=True, convert_to_numpy=True, batch_size=128, show_progress_bar=False)
        return [(E[i], float(rs[i]["severity"] or 0), f"{rs[i]['model']}|{rs[i]['rep']}") for i in range(len(rs))]
    S = {s: (items(IGN, s), items(PAR, s)) for s in STRATA}
    F = {s: (items(IGN, s, False), items(PAR, s, False)) for s in STRATA}
    print(f"  [{tag}] F-S n: " + ", ".join(f"{s} ({len(S[s][0])},{len(S[s][1])})" for s in STRATA))
    rng = np.random.default_rng(SEED)
    vals, fails = [], {s: 0 for s in STRATA}
    for _ in range(N_B):
        per = {}
        for s in STRATA:
            v = stratum_matched(*S[s], rng)
            if v is None: fails[s] += 1
            per[s] = v
        if all(per[s] is not None for s in STRATA): vals.append(np.mean([per[s] for s in STRATA]))
    evaluable = all(fails[s] <= FAIL_MAX * N_B for s in STRATA)
    v = np.array(vals); lo, hi = np.percentile(v, [2.5, 97.5]) if len(v) else (np.nan, np.nan)
    print(f"  [{tag}] PRIMARY stratified+matched: {v.mean():+.3f} [{lo:+.3f}, {hi:+.3f}]  "
          f"failures {fails}  evaluable={evaluable}")
    rng = np.random.default_rng(SEED)
    for name, D in [("stratified F-S, no matching", S), ("stratified FULL (unsplit)", F)]:
        b = np.array([np.mean([stratum_plain(*D[s], rng) for s in STRATA]) for _ in range(N_BOOT)])
        l2, h2 = np.percentile(b, [2.5, 97.5])
        print(f"  [{tag}] {name}: {b.mean():+.3f} [{l2:+.3f}, {h2:+.3f}]")
    return evaluable, (v.mean() if len(v) else np.nan), lo

def main():
    rows = [r for r in csv.DictReader(open(JUDGE)) if r["label"] in ("WORLD", "SENTENCE")]
    jmap, keyf = jev_labels()
    verdict_inputs = {}
    for enc in ENCODERS:
        model = SentenceTransformer(enc, device="cuda")
        print(f"\n=== {enc}   asym(ign_S -> par_S); + means ignorance covered WORSE")
        verdict_inputs[enc] = run(rows, lambda r: r["label"], model, "judge")
        run(rows, lambda r: jmap.get(tuple(r[c] for c in keyf), "NA"), model, "jev  ")
    ev = [verdict_inputs[e][0] for e in ENCODERS]; m = [verdict_inputs[e][1] for e in ENCODERS]; lo = [verdict_inputs[e][2] for e in ENCODERS]
    if not any(ev): v = "UNRESOLVED"
    elif all(ev) and all(x > 0 for x in m) and all(x > 0 for x in lo): v = "SURVIVES"
    elif all(ev) and all(x <= 0 for x in m): v = "EXPLAINED BY POOLING/DISPERSION"
    elif all(ev): v = "WEAKENED"
    else: v = "UNRESOLVED (evaluable on one encoder only; rule requires both)"
    print(f"\nVERDICT (judge, primary, by rule): {v}")

if __name__ == "__main__":
    main()
