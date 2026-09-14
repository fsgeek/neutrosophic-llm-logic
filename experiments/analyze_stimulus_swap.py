"""Analysis fixed by experiments/stimulus_swap_prereg.md. Reads the original S4 data and the
swap data; reports T1 (within-swap), T2 (cross), the original, and the control, per encoder."""
from __future__ import annotations
import csv, json, sys, numpy as np
from collections import defaultdict
from sentence_transformers import SentenceTransformer
ORIG, SWAP = "data/s4_tensor_results.csv", "data/s4_stimulus_swap.csv"
ENCODERS = ["all-MiniLM-L6-v2", "all-mpnet-base-v2"]; N_BOOT, SEED = 2000, 0
IGN, PAR, CON, VAG = "Ignorance (Epistemic)", "Paradox (Logical)", "Contingency (Future)", "Vagueness (Fuzzy)"

def load(path):
    by, fails = defaultdict(list), 0
    for row in csv.DictReader(open(path)):
        if row["Status"] != "Success": fails += 1; continue
        try: L = json.loads(row["Losses_JSON"])
        except Exception: fails += 1; continue
        for it in L:
            w = (it.get("what") or "").strip()
            if not w: continue
            try: s = float(it.get("severity", 0))
            except Exception: s = 0.0
            by[row["Phenomenon_Type"]].append((w, s, row["Model"], row["Rep"]))
    return by, fails

def cov(EA, EB, sA):
    if len(EA) == 0 or len(EB) == 0: return 0.0
    m = (EA @ EB.T).max(axis=1); w = sA/sA.sum() if sA.sum() else np.ones(len(sA))/len(sA); return float((w*m).sum())

def asym(A, B):  # A,B: dict with E, S, cells (cell id per item)
    return (1-cov(A["E"], B["E"], A["S"])) - (1-cov(B["E"], A["E"], B["S"]))

def boot(A, B, rng):
    cellsA, cellsB = sorted(set(A["cells"])), sorted(set(B["cells"]))
    out = []
    for _ in range(N_BOOT):
        ca = set(rng.choice(cellsA, len(cellsA), replace=True)); cb = set(rng.choice(cellsB, len(cellsB), replace=True))
        ia = [i for i, c in enumerate(A["cells"]) if c in ca]; ib = [i for i, c in enumerate(B["cells"]) if c in cb]
        out.append(asym({"E": A["E"][ia], "S": A["S"][ia]}, {"E": B["E"][ib], "S": B["S"][ib]}))
    d = np.array(out); return d.mean(), np.percentile(d, 2.5), np.percentile(d, 97.5), float((d <= 0).mean())

def main():
    orig, f1 = load(ORIG); swap, f2 = load(SWAP)
    print(f"parse failures: original {f1}, swap {f2}")
    for ph in sorted(swap): print(f"  swap {ph:26s} {len(swap[ph]):4d} losses")
    for enc in ENCODERS:
        model = SentenceTransformer(enc, device="cuda")
        def pack(items):
            return {"E": model.encode([w for w,_,_,_ in items], normalize_embeddings=True, convert_to_numpy=True, batch_size=128, show_progress_bar=False),
                    "S": np.array([s for _,s,_,_ in items], dtype=np.float32), "cells": [f"{m}|{r}" for _,_,m,r in items]}
        O = {k: pack(v) for k, v in orig.items()}; W = {k: pack(v) for k, v in swap.items()}
        rng = np.random.default_rng(SEED)
        print(f"\n=== {enc}   asym(A->B) = c(A->B) - c(B->A); + means A's losses are covered WORSE by B's")
        tests = [("ORIGINAL  ign(orig)->par(orig)", O[IGN], O[PAR]),
                 ("T1 within ign(swap)->par(swap)", W[IGN], W[PAR]),
                 ("T2 cross  ign(orig)->par(swap)", O[IGN], W[PAR]),
                 ("T2 cross  ign(swap)->par(orig)", W[IGN], O[PAR]),
                 ("CONTROL   con(orig)->vag(orig)", O[CON], O[VAG]),
                 ("CONTROL   con(swap)->vag(swap)", W[CON], W[VAG])]
        for name, A, B in tests:
            pt = asym(A, B); m, lo, hi, p = boot(A, B, rng)
            flag = "excludes 0" if (lo > 0 or hi < 0) else "INCLUDES 0"
            print(f"{name}: {pt:+.3f}  boot {m:+.3f} [{lo:+.3f}, {hi:+.3f}]  P(<=0)={p:.4f}  {flag}")

if __name__ == "__main__":
    main()
