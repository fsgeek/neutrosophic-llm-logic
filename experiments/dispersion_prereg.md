# Pre-registration: dispersion-matched asymmetry (2026-10-08)

Written and committed (signed, OpenTimestamps-stamped) together with its
analysis script BEFORE the script is run. No new API calls: the data are the
existing `data/s4_tensor_results.csv` (original) and `data/s4_stimulus_swap.csv`
(swap). What this pre-registration fixes is the analysis, not the collection.

**Already seen before writing this:** the full-n dispersions and the cross-pair
correlations printed by `asymmetry_breadth_check.py` (findings note, addendum
2026-10-08): rho(asym, ddispersion) = −0.69 (mpnet), −0.42 (MiniLM) on the
original data; target pair dispersion gap ignorance minus paradox = −0.018
(MiniLM), −0.023 (mpnet). Not seen: any dispersion on the swap or pooled data,
any matched quantity.

## Question

Does the ignorance→paradox asymmetry survive when the two loss sets are
matched on dispersion (1 − mean pairwise cosine) as well as on size?

## Measure

As before: asym(A→B) = c(A→B) − c(B→A), c(A→B) = 1 − severity-weighted
max-cosine coverage of A's `what` losses by B's; + means A's losses are
covered worse by B's. Encoders all-MiniLM-L6-v2 and all-mpnet-base-v2,
normalized embeddings. Seed 0.

## Procedure (`experiments/dispersion_matched.py`)

For a pair (A, B), with k = min(nA, nB):
1. Draw a size-k subset of A and of B without replacement.
2. Compute each subset's dispersion. Accept the draw if
   |disp(A_sub) − disp(B_sub)| ≤ 0.005.
3. Repeat until 1000 accepted draws or 200,000 attempts.
4. **Primary estimator:** mean asym over accepted draws, with the 2.5th and
   97.5th percentiles of the accepted draws.
5. **Secondary estimator (no rejection):** over 2000 unconditioned size-k draws,
   regress asym on (disp_A − disp_B) by least squares; report the intercept
   (asym predicted at zero dispersion gap) and slope, with a 2000-resample
   bootstrap over draws for the intercept's 95% interval.

Datasets: original, swap, pooled (original + swap items per phenomenon).

Limitation, stated now: the percentile interval reflects which items are
drawn, not resampling of (model, rep) cells; it matches the size-matched check
for comparability and is narrower than a cell bootstrap would be.

## Decision rule for the target, fixed now

- **Survives** if the primary estimator is positive with its 2.5th percentile
  > 0 on both encoders for BOTH the original and the pooled data.
- **Explained by dispersion** if the primary mean is ≤ 0 on both encoders for
  the pooled data.
- **Weakened** otherwise; reported with the fraction of the size-matched
  magnitude retained.
- **Unmatchable** for a dataset if fewer than 1000 draws are accepted within
  200,000 attempts on either encoder; that dataset is then not evaluable and the
  secondary estimator is reported in its place, labelled as such.
- Swap data reported, not gated. The secondary estimator is reported, not gated.

## Secondary question, descriptive, not gated

Across all 10 pairs on the original data, recompute the dispersion-matched
asymmetry and its Spearman correlation with the full-n dispersion gap. If the
cross-pair correlation on mpnet falls below |0.4|, the cross-pair dispersion
pattern was carried by dispersion differences rather than by something the
matching leaves in place.

## Priors, committed before running

Claude (Opus 5.5, this instance): P(target survives) = 0.75. Reasoning: the
target's dispersion gap is small, and its size-matched value kept about three
quarters of its magnitude; but my last two priors on this pair priced the
mechanism I had just been thinking about and lost both, so I am not going higher.

Claude: P(mpnet cross-pair |rho| falls below 0.4 after matching) = 0.55.

Tony (2026-10-08): declined to give a number: "I don't have any strong sense so
my prediction would be a random guess. I'll wait and see what we actually learn."
