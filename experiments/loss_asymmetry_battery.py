"""Robustness battery for directional-contradiction asymmetry in S4 declared losses.

Tests the answer to Leyva-Vazquez & Smarandache (2026) Sec 5.4: their plithogenic
contradiction c(v_i,v_j) is symmetric by axiom. We claim declared-loss data violate
that symmetry for ignorance/paradox, in the predicted direction.

Three robustness axes, because the skeptic (Smarandache) will probe all three:
  A. Multiple directional MEASURES (not just max-cosine) -> sign must survive.
  B. Per-MODEL breakdown -> is the sign driven by all vendors or one outlier?
  C. Discriminant CONTROL pair (vagueness<->contingency) -> mutual overlap, not
     containment, so it should be LOW magnitude and SIGN-UNSTABLE. If our measure
     paints THAT asymmetric too, the instrument is noise. Pre-registered prediction.

All across two encoders (different geometry). Bootstrap over (model,rep) cells.
"""
from __future__ import annotations
import csv, json
from collections import defaultdict
import numpy as np
from sentence_transformers import SentenceTransformer

DATA = "data/s4_tensor_results.csv"
ENCODERS = ["all-MiniLM-L6-v2", "all-mpnet-base-v2"]
N_BOOT = 2000
SEED = 0
TOPK = 3

TARGET = ("Ignorance (Epistemic)", "Paradox (Logical)")          # predicted: large, sign-stable
CONTROL = ("Vagueness (Fuzzy)", "Contingency (Future)")          # predicted: small, sign-unstable

def load():
    by_phen = defaultdict(list)  # phen -> (what, sev, model, rep)
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
                    (what, sev, row["Model"], row["Rep"]))
    return by_phen

# ---- directional coverage measures: coverage(A by B) in [0,1]; contradiction = 1-coverage ----
def cov_maxcos(EA, EB, sA):
    """A's losses each matched to best B-loss (max cosine), severity-weighted mean."""
    if len(EA) == 0 or len(EB) == 0: return 0.0
    m = (EA @ EB.T).max(axis=1)
    w = sA / sA.sum() if sA.sum() else np.ones(len(sA)) / len(sA)
    return float((w * m).sum())

def cov_topk(EA, EB, sA, k=TOPK):
    """Mean of top-k B-similarities per A-loss (softer than max), severity-weighted."""
    if len(EA) == 0 or len(EB) == 0: return 0.0
    S = EA @ EB.T
    kk = min(k, S.shape[1])
    topk = np.sort(S, axis=1)[:, -kk:].mean(axis=1)
    w = sA / sA.sum() if sA.sum() else np.ones(len(sA)) / len(sA)
    return float((w * topk).sum())

def cov_softmax(EA, EB, sA, temp=0.1):
    """Soft-assignment coverage: softmax over B per A-loss, weighted by similarity."""
    if len(EA) == 0 or len(EB) == 0: return 0.0
    S = EA @ EB.T
    P = np.exp(S / temp); P /= P.sum(axis=1, keepdims=True)
    soft = (P * S).sum(axis=1)
    w = sA / sA.sum() if sA.sum() else np.ones(len(sA)) / len(sA)
    return float((w * soft).sum())

MEASURES = {"max-cosine": cov_maxcos, "top-k-mean": cov_topk, "softmax": cov_softmax}

def asym(emb, sev, pair, covfn):
    a, b = pair
    c_ab = 1 - covfn(emb[a], emb[b], sev[a])   # a -> b
    c_ba = 1 - covfn(emb[b], emb[a], sev[b])   # b -> a
    return c_ab - c_ba, c_ab, c_ba

def bootstrap_asym(emb, sev, cells, pair, covfn):
    rng = np.random.default_rng(SEED)
    groups = {}
    for p in pair:
        g = defaultdict(list)
        for i, mr in enumerate(cells[p]):
            g[mr].append(i)
        groups[p] = [np.array(v) for v in g.values()]
    out = []
    for _ in range(N_BOOT):
        be, bs = {}, {}
        for p in pair:
            gs = groups[p]
            pick = rng.integers(0, len(gs), size=len(gs))
            idx = np.concatenate([gs[k] for k in pick])
            be[p], bs[p] = emb[p][idx], sev[p][idx]
        d, _, _ = asym(be, bs, pair, covfn)
        out.append(d)
    return np.array(out)

def run(name, by_phen):
    print(f"\n{'='*72}\nENCODER: {name}\n{'='*72}")
    model = SentenceTransformer(name, device="cuda")
    phens = sorted(by_phen)
    emb, sev, cells = {}, {}, {}
    for p in phens:
        whats = [w for w, _, _, _ in by_phen[p]]
        emb[p] = model.encode(whats, normalize_embeddings=True, convert_to_numpy=True,
                              batch_size=128, show_progress_bar=False)
        sev[p] = np.array([s for _, s, _, _ in by_phen[p]], dtype=np.float32)
        cells[p] = [(m, r) for _, _, m, r in by_phen[p]]

    for label, pair, pred in [("TARGET (ignorance<->paradox)", TARGET, "large, sign-stable +"),
                              ("CONTROL (vagueness<->contingency)", CONTROL, "small, sign-unstable")]:
        print(f"\n--- {label}   [pre-registered: {pred}] ---")
        for mname, covfn in MEASURES.items():
            d, c_ab, c_ba = asym(emb, sev, pair, covfn)
            boots = bootstrap_asym(emb, sev, cells, pair, covfn)
            lo, hi = np.percentile(boots, [2.5, 97.5])
            verdict = "excludes 0" if (lo > 0 or hi < 0) else "CROSSES 0"
            print(f"  {mname:>10}: asym={d:+.3f}  ({pair[0].split()[0][:4]}->{pair[1].split()[0][:4]}={c_ab:.3f}, "
                  f"rev={c_ba:.3f})  95%CI=[{lo:+.3f},{hi:+.3f}]  {verdict}")

    # Per-model breakdown on TARGET, max-cosine
    print(f"\n--- PER-MODEL: {TARGET[0].split()[0]}->{TARGET[1].split()[0]} asymmetry (max-cosine) ---")
    models = sorted({m for _, _, m, _ in by_phen[TARGET[0]]})
    for mdl in models:
        e2, s2 = {}, {}
        ok = True
        for p in TARGET:
            idx = [i for i, (_, _, mm, _) in enumerate(by_phen[p]) if mm == mdl]
            if not idx: ok = False; break
            e2[p] = emb[p][idx]; s2[p] = sev[p][idx]
        if not ok:
            print(f"  {mdl:>20}: (no data)"); continue
        d, c_ab, c_ba = asym(e2, s2, TARGET, cov_maxcos)
        sign = "+" if d > 0 else "-"
        print(f"  {mdl:>20}: asym={d:+.3f}  [{sign} = predicted]" if d > 0
              else f"  {mdl:>20}: asym={d:+.3f}  [SIGN FLIP]")

def main():
    by_phen = load()
    for name in ENCODERS:
        run(name, by_phen)

if __name__ == "__main__":
    main()
