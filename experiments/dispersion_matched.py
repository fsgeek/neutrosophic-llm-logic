"""Dispersion-matched asymmetry, fixed by experiments/dispersion_prereg.md.
For each pair: size-k subsets (k = min n), accepted only when the subsets' dispersions
(1 - mean pairwise cos) differ by <= TOL. Primary: mean/percentiles over accepted draws.
Secondary: regression of asym on dispersion gap over unconditioned draws; intercept at gap 0."""
from __future__ import annotations
import csv, json, itertools, numpy as np
from collections import defaultdict
from sentence_transformers import SentenceTransformer
from scipy.stats import spearmanr
ORIG, SWAP = "data/s4_tensor_results.csv", "data/s4_stimulus_swap.csv"
ENCODERS = ["all-MiniLM-L6-v2", "all-mpnet-base-v2"]
SEED, TOL, N_ACCEPT, MAX_TRIES, N_FREE, N_BOOT = 0, 0.005, 1000, 200_000, 2000, 2000
IGN, PAR = "Ignorance (Epistemic)", "Paradox (Logical)"

def load(path):
    by = defaultdict(list)
    for row in csv.DictReader(open(path)):
        if row["Status"] != "Success": continue
        try: L = json.loads(row["Losses_JSON"])
        except Exception: continue
        for it in L:
            w = (it.get("what") or "").strip()
            if not w: continue
            try: s = float(it.get("severity", 0))
            except Exception: s = 0.0
            by[row["Phenomenon_Type"]].append((w, s))
    return by

def cov(EA, EB, sA):
    m = (EA @ EB.T).max(axis=1); w = sA/sA.sum() if sA.sum() else np.ones(len(sA))/len(sA); return float((w*m).sum())

def asym(EA, SA, EB, SB):
    return (1-cov(EA, EB, SA)) - (1-cov(EB, EA, SB))

def disp(G, idx):
    sub = G[np.ix_(idx, idx)]; iu = np.triu_indices(len(idx), 1); return 1 - float(sub[iu].mean())

def matched(P, A, B, rng):
    EA, SA, GA = P[A]; EB, SB, GB = P[B]; k = min(len(EA), len(EB))
    acc, gaps, tries = [], [], 0
    while len(acc) < N_ACCEPT and tries < MAX_TRIES:
        tries += 1
        ia = rng.choice(len(EA), k, replace=False); ib = rng.choice(len(EB), k, replace=False)
        g = disp(GA, ia) - disp(GB, ib)
        if abs(g) <= TOL:
            acc.append(asym(EA[ia], SA[ia], EB[ib], SB[ib])); gaps.append(g)
    return np.array(acc), np.array(gaps), tries, k

def free_regression(P, A, B, rng):
    EA, SA, GA = P[A]; EB, SB, GB = P[B]; k = min(len(EA), len(EB)); xs, ys = [], []
    for _ in range(N_FREE):
        ia = rng.choice(len(EA), k, replace=False); ib = rng.choice(len(EB), k, replace=False)
        xs.append(disp(GA, ia) - disp(GB, ib)); ys.append(asym(EA[ia], SA[ia], EB[ib], SB[ib]))
    x, y = np.array(xs), np.array(ys)
    slope, icpt = np.polyfit(x, y, 1); boots = []
    for _ in range(N_BOOT):
        j = rng.integers(0, len(x), len(x)); boots.append(np.polyfit(x[j], y[j], 1)[1])
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return icpt, lo, hi, slope, float(x.mean())

def main():
    orig, swap = load(ORIG), load(SWAP)
    pooled = {ph: orig[ph] + swap.get(ph, []) for ph in orig}
    data = {"original": orig, "swap": swap, "pooled": pooled}
    for name, by in data.items():
        print(f"{name}: " + ", ".join(f"{ph.split()[0]} {len(v)}" for ph, v in sorted(by.items())))
    for enc in ENCODERS:
        model = SentenceTransformer(enc, device="cuda")
        print(f"\n=== {enc}   asym(A->B) = c(A->B) - c(B->A); + means A covered WORSE by B")
        packs = {}
        for name, by in data.items():
            P = {}
            for ph, items in by.items():
                E = model.encode([w for w,_ in items], normalize_embeddings=True, convert_to_numpy=True, batch_size=128, show_progress_bar=False)
                P[ph] = (E, np.array([s for _,s in items], dtype=np.float32), E @ E.T)
            packs[name] = P
        print("\n-- TARGET ignorance->paradox")
        for name, P in packs.items():
            rng = np.random.default_rng(SEED)
            full = asym(P[IGN][0], P[IGN][1], P[PAR][0], P[PAR][1])
            fd = disp(P[IGN][2], np.arange(len(P[IGN][0]))) - disp(P[PAR][2], np.arange(len(P[PAR][0])))
            acc, gaps, tries, k = matched(P, IGN, PAR, rng)
            if len(acc) < N_ACCEPT:
                prim = f"UNMATCHABLE ({len(acc)} accepted in {tries} tries)"
            else:
                lo, hi = np.percentile(acc, [2.5, 97.5])
                prim = f"matched {acc.mean():+.3f} [{lo:+.3f}, {hi:+.3f}]  accept {len(acc)}/{tries}  mean gap {gaps.mean():+.4f}"
            icpt, ilo, ihi, slope, mx = free_regression(P, IGN, PAR, rng)
            print(f"{name:9s} k={k:3d} full {full:+.3f} (full disp gap {fd:+.3f}) | {prim}")
            print(f"{'':9s} secondary: intercept {icpt:+.3f} [{ilo:+.3f}, {ihi:+.3f}], slope {slope:+.2f}, mean free gap {mx:+.4f}")
        print("\n-- SECONDARY, original data, all 10 pairs (descriptive)")
        P = packs["original"]; rows = []
        for A, B in itertools.combinations(sorted(P), 2):
            rng = np.random.default_rng(SEED)
            fd = disp(P[A][2], np.arange(len(P[A][0]))) - disp(P[B][2], np.arange(len(P[B][0])))
            acc, _, tries, _ = matched(P, A, B, rng)
            m = acc.mean() if len(acc) == N_ACCEPT else float("nan")
            rows.append((A, B, m, fd))
            print(f"{A[:14]:14s} -> {B[:14]:14s} matched {m:+.3f}  accept {len(acc)}/{tries}  full disp gap {fd:+.3f}")
        ok = [(m, fd) for _,_,m,fd in rows if not np.isnan(m)]
        rho, p = spearmanr([fd for _,fd in ok], [m for m,_ in ok])
        print(f"Spearman(matched asym, full disp gap) over {len(ok)} pairs: rho={rho:+.3f} p={p:.3f}")

if __name__ == "__main__":
    main()
