"""Directional contradiction asymmetry in S4 declared losses.

Answers Leyva-Vazquez & Smarandache (2026) Sec 5.4: their plithogenic
contradiction function c(v_i, v_j) is defined SYMMETRIC (c(v_i,v_j)=c(v_j,v_i),
their line 833). We test whether declared-loss data violate that symmetry.

Contradiction c(A->B) = 1 - coverage(A by B), where coverage measures how well
B's declared losses semantically cover A's. Asymmetric whenever one phenomenon's
epistemic predicament is *contained in* another's.

Hardening over the exploratory run:
  - bootstrap CI over (model, rep) resampling -> is the asymmetry significant?
  - two independent encoders -> is the sign an artifact of one embedding geometry?

Prediction (pre-registered, prior session): paradox<->ignorance is the largest
asymmetry, with c(ignorance->paradox) > c(paradox->ignorance), because ignorance's
predicament ("can't determine the value") is a subset of paradox's
("can't determine AND can't even be bivalent"). Severity-mass confound controlled
by reporting the UNWEIGHTED measure alongside the weighted one.
"""
from __future__ import annotations
import csv, json, argparse
from collections import defaultdict
import numpy as np
from sentence_transformers import SentenceTransformer

DATA = "data/s4_tensor_results.csv"
ENCODERS = ["all-MiniLM-L6-v2", "all-mpnet-base-v2"]
N_BOOT = 2000
SEED = 0  # determinism; no Date.now/random nondeterminism in the claim

def load():
    """phen -> list of (what, severity, model, rep) so we can resample by cell."""
    by_phen = defaultdict(list)
    with open(DATA) as f:
        for row in csv.DictReader(f):
            if row["Status"] != "Success":
                continue
            try:
                L = json.loads(row["Losses_JSON"])
            except Exception:
                continue
            for item in L:
                what = (item.get("what") or "").strip()
                if not what:
                    continue
                try:
                    sev = float(item.get("severity", 0))
                except Exception:
                    sev = 0.0
                by_phen[row["Phenomenon_Type"]].append(
                    (what, sev, row["Model"], row["Rep"])
                )
    return by_phen

def coverage(EA, sA, EB, weighted):
    """weighted/unweighted mean over a in A of max_b cos(a,b). E* are L2-normalized."""
    if len(EA) == 0 or len(EB) == 0:
        return 0.0
    maxsim = (EA @ EB.T).max(axis=1)
    if weighted:
        w = sA / sA.sum() if sA.sum() else np.ones(len(sA)) / len(sA)
        return float((w * maxsim).sum())
    return float(maxsim.mean())

def contradiction_matrix(emb, sev, phens, weighted):
    return {
        (a, b): 1 - coverage(emb[a], sev[a], emb[b], weighted)
        for a in phens for b in phens if a != b
    }

def run_encoder(name, by_phen, phens):
    print(f"\n{'='*70}\nENCODER: {name}\n{'='*70}")
    model = SentenceTransformer(name, device="cuda")
    emb, sev, cells = {}, {}, {}
    for p in phens:
        whats = [w for w, _, _, _ in by_phen[p]]
        s = np.array([sv for _, sv, _, _ in by_phen[p]], dtype=np.float32)
        E = model.encode(whats, normalize_embeddings=True, convert_to_numpy=True,
                         batch_size=128, show_progress_bar=False)
        emb[p], sev[p], cells[p] = E, s, [(m, r) for _, _, m, r in by_phen[p]]

    for weighted in (True, False):
        tag = "weighted" if weighted else "unweighted"
        mat = contradiction_matrix(emb, sev, phens, weighted)
        ip = ("Ignorance (Epistemic)", "Paradox (Logical)")
        c_ip = mat[ip]                       # ignorance -> paradox
        c_pi = mat[(ip[1], ip[0])]           # paradox -> ignorance
        asym = c_ip - c_pi

        # bootstrap: resample (model,rep) cells with replacement, per phenomenon
        rng = np.random.default_rng(SEED)
        cell_groups = {}  # phen -> list of idx-groups, one per (model,rep) cell
        for p in phens:
            grouped = defaultdict(list)
            for i, mr in enumerate(cells[p]):
                grouped[mr].append(i)
            cell_groups[p] = [np.array(g) for g in grouped.values()]

        boots = []
        for _ in range(N_BOOT):
            bemb, bsev = {}, {}
            for p in phens:
                groups = cell_groups[p]
                pick = rng.integers(0, len(groups), size=len(groups))
                idx = np.concatenate([groups[k] for k in pick])
                bemb[p], bsev[p] = emb[p][idx], sev[p][idx]
            c1 = 1 - coverage(bemb[ip[0]], bsev[ip[0]], bemb[ip[1]], weighted)
            c2 = 1 - coverage(bemb[ip[1]], bsev[ip[1]], bemb[ip[0]], weighted)
            boots.append(c1 - c2)
        boots = np.array(boots)
        lo, hi = np.percentile(boots, [2.5, 97.5])
        p_le0 = float((boots <= 0).mean())

        # rank paradox<->ignorance |asym| among all pairs
        seen, mags = set(), []
        for a in phens:
            for b in phens:
                if a == b or (b, a) in seen:
                    continue
                seen.add((a, b))
                mags.append((abs(mat[(a, b)] - mat[(b, a)]), a, b))
        mags.sort(reverse=True)
        rank = 1 + next(i for i, (_, a, b) in enumerate(mags) if {a, b} == set(ip))

        print(f"\n[{tag}] ignorance->paradox c = {c_ip:.3f}")
        print(f"[{tag}] paradox->ignorance c = {c_pi:.3f}")
        print(f"[{tag}] asymmetry (ign->par - par->ign) = {asym:+.3f}")
        print(f"[{tag}] bootstrap 95% CI = [{lo:+.3f}, {hi:+.3f}]  (n={N_BOOT})")
        print(f"[{tag}] P(asym <= 0) = {p_le0:.4f}   "
              f"{'>>> excludes zero, predicted sign' if lo > 0 else 'CI crosses zero'}")
        print(f"[{tag}] paradox<->ignorance is rank #{rank} of {len(mags)} "
              f"pairs by |asymmetry|  (largest={mags[0][0]:.3f})")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--encoders", nargs="*", default=ENCODERS)
    args = ap.parse_args()
    by_phen = load()
    phens = sorted(by_phen)
    print("Phenomena and loss counts:")
    for p in phens:
        print(f"  {p}: {len(by_phen[p])} losses")
    for name in args.encoders:
        run_encoder(name, by_phen, phens)

if __name__ == "__main__":
    main()
