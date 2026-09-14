"""Pre-registered ranking test: does measured directional-asymmetry magnitude
track Tony's BLIND containment-strength ranking (committed before seeing data)?

Tony's ranking, most-directional (strongest containment) -> least:
"""
from __future__ import annotations
import csv, json, itertools
from collections import defaultdict
import numpy as np
from scipy.stats import spearmanr
from sentence_transformers import SentenceTransformer

DATA = "data/s4_tensor_results.csv"
ENCODERS = ["all-MiniLM-L6-v2", "all-mpnet-base-v2"]
SEED = 0

P = {"contradiction": "Contradiction (Ethical)", "paradox": "Paradox (Logical)",
     "ignorance": "Ignorance (Epistemic)", "contingency": "Contingency (Future)",
     "vagueness": "Vagueness (Fuzzy)"}

# Tony's blind prior: rank 1 = MOST directional ... rank 10 = LEAST directional
PRIOR = [
    ("contradiction", "paradox"),    # 1
    ("ignorance", "contingency"),    # 2
    ("vagueness", "ignorance"),      # 3
    ("vagueness", "contingency"),    # 4
    ("vagueness", "paradox"),        # 5
    ("contingency", "contradiction"),# 6
    ("vagueness", "contradiction"),  # 7
    ("contingency", "paradox"),      # 8
    ("ignorance", "contradiction"),  # 9
    ("ignorance", "paradox"),        # 10
]

def load():
    by = defaultdict(list)
    with open(DATA) as f:
        for row in csv.DictReader(f):
            if row["Status"] != "Success":
                continue
            try:
                L = json.loads(row["Losses_JSON"])
            except Exception:
                continue
            for it in L:
                w = (it.get("what") or "").strip()
                if not w:
                    continue
                try: s = float(it.get("severity", 0))
                except Exception: s = 0.0
                by[row["Phenomenon_Type"]].append((w, s))
    return by

def cov_maxcos(EA, EB, sA):
    if len(EA) == 0 or len(EB) == 0: return 0.0
    m = (EA @ EB.T).max(axis=1)
    w = sA / sA.sum() if sA.sum() else np.ones(len(sA)) / len(sA)
    return float((w * m).sum())

def main():
    by = load()
    prior_pairs = [(P[a], P[b]) for a, b in PRIOR]
    prior_rank = {frozenset(p): i + 1 for i, p in enumerate(prior_pairs)}  # 1=most

    for enc in ENCODERS:
        model = SentenceTransformer(enc, device="cuda")
        emb, sev = {}, {}
        for ph, items in by.items():
            emb[ph] = model.encode([w for w, _ in items], normalize_embeddings=True,
                                    convert_to_numpy=True, batch_size=128, show_progress_bar=False)
            sev[ph] = np.array([s for _, s in items], dtype=np.float32)

        # measured |asymmetry| for all 10 unordered pairs
        phens = sorted(by)
        measured = {}
        for a, b in itertools.combinations(phens, 2):
            c_ab = 1 - cov_maxcos(emb[a], emb[b], sev[a])
            c_ba = 1 - cov_maxcos(emb[b], emb[a], sev[b])
            measured[frozenset((a, b))] = abs(c_ab - c_ba)

        # align by Tony's pairs
        rows = []
        for p in prior_pairs:
            key = frozenset(p)
            rows.append((prior_rank[key], measured[key], p))
        rows.sort()  # by prior rank 1..10

        pr = [r[0] for r in rows]            # prior rank 1..10 (1=most directional)
        meas = [r[1] for r in rows]          # measured |asym|
        # data rank: 1 = largest measured asymmetry
        order = sorted(range(len(meas)), key=lambda i: -meas[i])
        data_rank = [0] * len(meas)
        for dr, i in enumerate(order):
            data_rank[i] = dr + 1

        rho, p_param = spearmanr(pr, meas)   # prior 1=most vs measured magnitude
        # so we expect NEGATIVE rho (low prior-number == high magnitude) if prior is right
        # report as +correlation between (11-prior) and magnitude for readability
        rho_aligned, _ = spearmanr([11 - x for x in pr], meas)

        # permutation p on rho_aligned
        rng = np.random.default_rng(SEED)
        obs = rho_aligned
        perm = []
        base = [11 - x for x in pr]
        for _ in range(20000):
            perm.append(spearmanr(rng.permutation(base), meas)[0])
        perm = np.array(perm)
        p_perm = float((perm >= obs).mean())  # one-sided: prior predicts magnitude

        print(f"\n{'='*64}\nENCODER: {enc}\n{'='*64}")
        print(f"{'prior#':>6} {'|asym|':>7} {'dataRank':>9}  pair")
        for (prk, m, pair), drk in zip(rows, [data_rank[i] for i in range(len(rows))]):
            flag = "  <-- TARGET" if frozenset(pair) == frozenset((P['ignorance'], P['paradox'])) else ""
            print(f"{prk:>6} {m:>7.3f} {drk:>9}  {pair[0].split()[0]:>13} <-> {pair[1].split()[0]:<13}{flag}")
        print(f"\nSpearman rho (prior-strength vs measured |asym|) = {rho_aligned:+.3f}")
        print(f"permutation one-sided p = {p_perm:.4f}  (n=20000)")
        print("  rho>0 => prior predicts magnitude; rho<0 => prior INVERTED by data")

if __name__ == "__main__":
    main()
