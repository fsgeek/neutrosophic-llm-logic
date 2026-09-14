"""Size-matched asymmetry: subsample both sets to min(nA,nB) items, 1000 draws, seed 0.
If the target asymmetry survives at equal n, set size is not the explanation."""
import csv, json, itertools, numpy as np
from collections import defaultdict
from sentence_transformers import SentenceTransformer
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
rng = np.random.default_rng(0)
for enc in ["all-MiniLM-L6-v2", "all-mpnet-base-v2"]:
    model = SentenceTransformer(enc, device="cuda")
    E, S = {}, {}
    for ph, items in by.items():
        E[ph] = model.encode([w for w,_ in items], normalize_embeddings=True, convert_to_numpy=True, batch_size=128, show_progress_bar=False)
        S[ph] = np.array([s for _,s in items], dtype=np.float32)
    print(f"\n=== {enc}   (asym(A->B) at full n  |  size-matched mean [2.5%, 97.5%] over 1000 draws)")
    for A, B in itertools.combinations(sorted(by), 2):
        full = (1-cov(E[A],E[B],S[A])) - (1-cov(E[B],E[A],S[B]))
        k = min(len(E[A]), len(E[B])); draws = []
        for _ in range(1000):
            ia = rng.choice(len(E[A]), k, replace=False); ib = rng.choice(len(E[B]), k, replace=False)
            draws.append((1-cov(E[A][ia],E[B][ib],S[A][ia])) - (1-cov(E[B][ib],E[A][ia],S[B][ib])))
        d = np.array(draws); lo, hi = np.percentile(d, [2.5, 97.5])
        flag = "  <-- TARGET" if (A,B)==("Ignorance (Epistemic)","Paradox (Logical)") else ("  <-- CONTROL" if (A,B)==("Contingency (Future)","Vagueness (Fuzzy)") else "")
        print(f"{A[:14]:14s} -> {B[:14]:14s}  full {full:+.3f} | matched {d.mean():+.3f} [{lo:+.3f}, {hi:+.3f}]{flag}")
