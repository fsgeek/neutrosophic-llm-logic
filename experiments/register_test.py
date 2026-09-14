"""Pre-registered REGISTER test. Tony's blind classification (before seeing matrix):

  outward (world/data withholds): ignorance, contingency
  inward  (proposition/concept self-undermines): paradox, vagueness, contradiction

Hypothesis: CROSS-register pairs (one outward, one inward) show LARGE directional
asymmetry; SAME-register pairs (out-out or in-in) show SMALL asymmetry. Binary cut,
no tuning. Tests whether |asym| separates by register class.
"""
from __future__ import annotations
import csv, json, itertools
from collections import defaultdict
import numpy as np
from scipy.stats import mannwhitneyu
from sentence_transformers import SentenceTransformer

DATA = "data/s4_tensor_results.csv"
ENCODERS = ["all-MiniLM-L6-v2", "all-mpnet-base-v2"]
SEED = 0

REGISTER = {
    "Ignorance (Epistemic)": "outward",
    "Contingency (Future)": "outward",
    "Paradox (Logical)": "inward",
    "Vagueness (Fuzzy)": "inward",
    "Contradiction (Ethical)": "inward",
}

def load():
    by = defaultdict(list)
    with open(DATA) as f:
        for row in csv.DictReader(f):
            if row["Status"] != "Success":
                continue
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
    if len(EA) == 0 or len(EB) == 0: return 0.0
    m = (EA @ EB.T).max(axis=1)
    w = sA / sA.sum() if sA.sum() else np.ones(len(sA)) / len(sA)
    return float((w * m).sum())

def main():
    by = load()
    for enc in ENCODERS:
        model = SentenceTransformer(enc, device="cuda")
        emb, sev = {}, {}
        for ph, items in by.items():
            emb[ph] = model.encode([w for w, _ in items], normalize_embeddings=True,
                                   convert_to_numpy=True, batch_size=128, show_progress_bar=False)
            sev[ph] = np.array([s for _, s in items], dtype=np.float32)

        phens = sorted(by)
        rows = []
        for a, b in itertools.combinations(phens, 2):
            c_ab = 1 - cov(emb[a], emb[b], sev[a])
            c_ba = 1 - cov(emb[b], emb[a], sev[b])
            d = abs(c_ab - c_ba)
            cls = "CROSS" if REGISTER[a] != REGISTER[b] else "same "
            rows.append((d, cls, a, b))
        rows.sort(reverse=True)

        cross = [r[0] for r in rows if r[1] == "CROSS"]
        same = [r[0] for r in rows if r[1] == "same "]

        print(f"\n{'='*64}\nENCODER: {enc}\n{'='*64}")
        print(f"{'|asym|':>7} {'class':>6}  pair")
        for d, cls, a, b in rows:
            print(f"{d:>7.3f} {cls:>6}  {a.split()[0]:>13} <-> {b.split()[0]:<13}")
        print(f"\nCROSS-register (n={len(cross)}): mean |asym| = {np.mean(cross):.3f}  "
              f"range [{min(cross):.3f}, {max(cross):.3f}]")
        print(f"SAME-register  (n={len(same)}): mean |asym| = {np.mean(same):.3f}  "
              f"range [{min(same):.3f}, {max(same):.3f}]")
        # Is every CROSS > every SAME? (clean separation)
        sep = min(cross) > max(same)
        print(f"clean separation (min CROSS > max SAME)? {sep}")
        # Mann-Whitney one-sided: CROSS > SAME
        try:
            u, p = mannwhitneyu(cross, same, alternative="greater")
            print(f"Mann-Whitney U one-sided (CROSS>SAME): U={u:.1f}, p={p:.4f}")
        except Exception as e:
            print("MWU failed:", e)

if __name__ == "__main__":
    main()
