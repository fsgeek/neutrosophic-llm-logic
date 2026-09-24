"""POST HOC: agreement between the pre-registered judge and Jev, and the register cells under Jev's labels.
Reuses the measure from register2_analyze.py. Reported, not gating."""
from __future__ import annotations
import csv, sys, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from register2_analyze import cov, asym, sub, boot, ENCODERS, SEED, MIN_N, IGN, PAR
from sentence_transformers import SentenceTransformer
J = "data/register2_labels.csv"; V = "data/register2_jev_labels.csv"

def main():
    judge = {(r["source"], r["row"], r["item"]): r for r in csv.DictReader(open(J))}
    jev = [r for r in csv.DictReader(open(V))]
    err = sum(r["jev_label"] == "ERROR" for r in jev); jev = [r for r in jev if r["jev_label"] != "ERROR"]
    print(f"{len(jev)} Jev labels ({err} errors); model {jev[0]['jev_model']}")
    agree = np.mean([r["jev_label"] == r["judge_label"] for r in jev]); print(f"judge/Jev agreement overall: {agree:.3f}")
    for ph in [IGN, PAR]:
        rs = [r for r in jev if r["phenomenon"] == ph]
        print(f"  {ph:24s} n={len(rs):3d}  Jev W={np.mean([r['jev_label']=='WORLD' for r in rs]):.2f}  judge W={np.mean([r['judge_label']=='WORLD' for r in rs]):.2f}  agree={np.mean([r['jev_label']==r['judge_label'] for r in rs]):.2f}")
    conf = np.array([float(r["confidence"] or 0) for r in jev]); dis = np.array([r["jev_label"] != r["judge_label"] for r in jev])
    print(f"Jev confidence: median {np.median(conf):.3f}; on disagreements median {np.median(conf[dis]) if dis.any() else float('nan'):.3f}")
    for enc in ENCODERS:
        model = SentenceTransformer(enc, device="cuda")
        def pack(rs):
            E = model.encode([f"{judge[(r['source'],r['row'],r['item'])]['what']}. {judge[(r['source'],r['row'],r['item'])]['why']}" for r in rs],
                             normalize_embeddings=True, convert_to_numpy=True, batch_size=128, show_progress_bar=False)
            return {"E": E, "S": np.array([float(r["severity"] or 0) for r in rs], dtype=np.float32),
                    "cells": [f"{r['source']}|{r['model']}|{r['rep']}" for r in rs], "W": np.array([r["jev_label"] == "WORLD" for r in rs])}
        rng = np.random.default_rng(SEED); print(f"\n=== {enc}  (Jev labels, pooled)")
        I = pack([r for r in jev if r["phenomenon"] == IGN]); P = pack([r for r in jev if r["phenomenon"] == PAR])
        iW, iS, pW, pS = np.where(I["W"])[0], np.where(~I["W"])[0], np.where(P["W"])[0], np.where(~P["W"])[0]
        print(f"   full asym ign->par = {asym(I,P):+.3f}")
        for name, a, b in [("F-W ign_W->par_W", iW, pW), ("F-S ign_S->par_S", iS, pS), ("X   ign_W->par_S", iW, pS)]:
            if len(a) < MIN_N or len(b) < MIN_N: print(f"   {name}: inconclusive (n={len(a)},{len(b)})"); continue
            m, lo, hi = boot(sub(I, a), sub(P, b), rng); print(f"   {name}: n=({len(a)},{len(b)})  {m:+.3f} [{lo:+.3f}, {hi:+.3f}]  {'excludes 0' if (lo>0 or hi<0) else 'INCLUDES 0'}")

if __name__ == "__main__":
    main()
