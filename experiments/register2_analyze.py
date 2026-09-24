"""Pre-registered analysis for register2 (see register2_prereg.md). Reads data/register2_labels.csv."""
from __future__ import annotations
import csv, numpy as np
from collections import defaultdict
from sentence_transformers import SentenceTransformer
LAB = "data/register2_labels.csv"; ENCODERS = ["all-MiniLM-L6-v2", "all-mpnet-base-v2"]; N_BOOT, SEED, MIN_N = 2000, 0, 10
IGN, PAR = "Ignorance (Epistemic)", "Paradox (Logical)"
W_ANCHORS = ["I lack access to the relevant facts or data", "the outcome depends on future events not yet known",
             "no empirical evidence is available to me", "I cannot verify this against real-world records",
             "the true state of the world is unknown to me"]
S_ANCHORS = ["the statement refers to itself", "the logical form of the sentence is self-undermining",
             "the term in the statement is vague and has no sharp boundary", "the wording is ambiguous",
             "the semantics of assigning a truth value to this sentence are unclear"]

def cov(EA, EB, sA):
    if len(EA) == 0 or len(EB) == 0: return 0.0
    m = (EA @ EB.T).max(axis=1); w = sA/sA.sum() if sA.sum() else np.ones(len(sA))/len(sA); return float((w*m).sum())
def asym(A, B): return (1-cov(A["E"], B["E"], A["S"])) - (1-cov(B["E"], A["E"], B["S"]))
def sub(P, idx): return {"E": P["E"][idx], "S": P["S"][idx], "cells": [P["cells"][i] for i in idx]}
def boot(A, B, rng):
    ca, cb = sorted(set(A["cells"])), sorted(set(B["cells"])); out = []
    for _ in range(N_BOOT):
        sa = set(rng.choice(ca, len(ca), replace=True)); sb = set(rng.choice(cb, len(cb), replace=True))
        ia = [i for i, c in enumerate(A["cells"]) if c in sa]; ib = [i for i, c in enumerate(B["cells"]) if c in sb]
        out.append(asym(sub(A, ia), sub(B, ib)))
    d = np.array(out); return d.mean(), np.percentile(d, 2.5), np.percentile(d, 97.5)

def main():
    rows = [r for r in csv.DictReader(open(LAB))]
    unp = sum(r["label"] == "UNPARSED" for r in rows); print(f"{len(rows)} items, {unp} unparsed (excluded)")
    rows = [r for r in rows if r["label"] in ("WORLD", "SENTENCE")]
    print("\n== P1 premise: share WORLD by phenomenon and dataset")
    for src in ["orig", "swap", "pooled"]:
        for ph in [IGN, PAR]:
            rs = [r for r in rows if r["phenomenon"] == ph and (src == "pooled" or r["source"] == src)]
            print(f"  {src:6s} {ph:24s} n={len(rs):3d}  W={sum(r['label']=='WORLD' for r in rs)/max(1,len(rs)):.2f}")
    for enc in ENCODERS:
        model = SentenceTransformer(enc, device="cuda")
        # secondary classifier (robustness)
        AW = model.encode(W_ANCHORS, normalize_embeddings=True); AS = model.encode(S_ANCHORS, normalize_embeddings=True)
        def pack(rs):
            E = model.encode([f"{r['what']}. {r['why']}" for r in rs], normalize_embeddings=True, convert_to_numpy=True, batch_size=128, show_progress_bar=False)
            return {"E": E, "S": np.array([float(r["severity"] or 0) for r in rs], dtype=np.float32), "cells": [f"{r['source']}|{r['model']}|{r['rep']}" for r in rs],
                    "judge": np.array([r["label"] == "WORLD" for r in rs]), "anchor": (E @ AW.T).max(axis=1) > (E @ AS.T).max(axis=1)}
        rng = np.random.default_rng(SEED)
        print(f"\n=== {enc}")
        for src in ["pooled", "orig", "swap"]:
            sel = lambda ph: [r for r in rows if r["phenomenon"] == ph and (src == "pooled" or r["source"] == src)]
            I, P = pack(sel(IGN)), pack(sel(PAR))
            agree = np.mean(np.concatenate([I["judge"] == I["anchor"], P["judge"] == P["anchor"]]))
            print(f"-- {src}  (judge/anchor agreement {agree:.2f})   full asym ign->par = {asym(I,P):+.3f}")
            for clf in ["judge", "anchor"]:
                iW = np.where(I[clf])[0]; iS = np.where(~I[clf])[0]; pW = np.where(P[clf])[0]; pS = np.where(~P[clf])[0]
                for name, a, b in [("F-W ign_W->par_W", iW, pW), ("F-S ign_S->par_S", iS, pS), ("X   ign_W->par_S", iW, pS), ("X'  ign_S->par_W", iS, pW)]:
                    if len(a) < MIN_N or len(b) < MIN_N:
                        print(f"   [{clf:6s}] {name}: inconclusive (n={len(a)},{len(b)})"); continue
                    m, lo, hi = boot(sub(I, a), sub(P, b), rng); flag = "excludes 0" if (lo > 0 or hi < 0) else "INCLUDES 0"
                    print(f"   [{clf:6s}] {name}: n=({len(a)},{len(b)})  {m:+.3f} [{lo:+.3f}, {hi:+.3f}]  {flag}")

if __name__ == "__main__":
    main()
