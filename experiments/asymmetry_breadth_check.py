"""Does directional asymmetry track loss-set BREADTH (size / diversity) rather than epistemics?
For each ordered pair (A,B): asym(A->B) = c(A->B) - c(B->A) with c = 1 - severity-weighted max-cos coverage.
Breadth of a set: n distinct 'what' strings, and dispersion = 1 - mean pairwise cosine.
Prediction if breadth explains it: asym(A->B) correlates with breadth(A) - breadth(B) across the 10 pairs
(the broader set covers the other better, so is 'contradicted' less in the direction toward it).
"""
import csv, json, itertools, numpy as np
from collections import defaultdict
from sentence_transformers import SentenceTransformer
from scipy.stats import spearmanr
by = defaultdict(list)
for row in csv.DictReader(open("data/s4_tensor_results.csv")):
    if row["Status"] != "Success": continue
    try: L = json.loads(row["Losses_JSON"])
    except Exception: continue
    for it in L:
        w = (it.get("what") or "").strip()
        if not w: continue
        try: s = float(it.get("severity", 0))
        except Exception: s = 0.0
        by[row["Phenomenon_Type"]].append((w, s))
def cov(EA, EB, sA):
    m = (EA @ EB.T).max(axis=1); w = sA/sA.sum() if sA.sum() else np.ones(len(sA))/len(sA); return float((w*m).sum())
for enc in ["all-MiniLM-L6-v2", "all-mpnet-base-v2"]:
    model = SentenceTransformer(enc, device="cuda")
    E, S, n, disp, ndist = {}, {}, {}, {}, {}
    for ph, items in by.items():
        E[ph] = model.encode([w for w,_ in items], normalize_embeddings=True, convert_to_numpy=True, batch_size=128, show_progress_bar=False)
        S[ph] = np.array([s for _,s in items], dtype=np.float32)
        n[ph] = len(items); ndist[ph] = len(set(w.lower() for w,_ in items))
        G = E[ph] @ E[ph].T; iu = np.triu_indices(len(G), 1); disp[ph] = 1 - float(G[iu].mean())
    print(f"\n=== {enc}")
    print(f"{'phenomenon':28s} {'n':>4s} {'ndistinct':>9s} {'dispersion':>10s}")
    for ph in sorted(by): print(f"{ph:28s} {n[ph]:4d} {ndist[ph]:9d} {disp[ph]:10.3f}")
    rows = []
    for A, B in itertools.combinations(sorted(by), 2):
        asym = (1-cov(E[A],E[B],S[A])) - (1-cov(E[B],E[A],S[B]))
        rows.append((A, B, asym, n[A]-n[B], ndist[A]-ndist[B], disp[A]-disp[B]))
    print(f"\n{'A':26s} {'B':26s} {'asym(A->B)':>10s} {'dn':>5s} {'ddist':>6s} {'ddisp':>7s}")
    for A,B,a,dn,dd,dp in rows: print(f"{A:26s} {B:26s} {a:+10.3f} {dn:+5d} {dd:+6d} {dp:+7.3f}")
    a = [r[2] for r in rows]
    for lab, idx in [("n", 3), ("ndistinct", 4), ("dispersion", 5)]:
        x = [r[idx] for r in rows]; rho, p = spearmanr(x, a)
        print(f"Spearman(asym, d{lab}) over 10 pairs: rho={rho:+.3f} p={p:.3f}")
