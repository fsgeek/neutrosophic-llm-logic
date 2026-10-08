# Pre-registration: the within-register residual, stratified and dispersion-matched (2026-10-08)

Committed (signed, OpenTimestamps-stamped) with its script BEFORE the script is
run. No new API calls. Data: `data/register2_labels.csv` (judge labels,
primary), `data/register2_jev_labels.csv` (Jev labels, reported only).

## Why this test

The register test (2026-09-24) found the ignorance→paradox asymmetry survives
within the sentence register (F-S) on POOLED data (+0.079 MiniLM, +0.086
mpnet, judge). The dispersion test earlier today showed pooling two stimuli
creates a dispersion gap the per-dataset data do not have. Computed before
writing this (dispersion only, no asymmetry), F-S cell, judge labels,
embedding `what. why` as in `register2_analyze.py`:

| F-S cell | n (ign, par) | gap MiniLM | gap mpnet |
|---|---|---|---|
| original | 20, 46 | −0.014 | +0.008 |
| swap | 16, 50 | +0.041 | −0.008 |
| pooled | 36, 96 | +0.132 | +0.128 |

Within each pair the slope of asymmetry on dispersion gap was positive in
today's test, so a +0.13 gap could inflate the pooled residual. Also already
known: per-dataset F-S values from 2026-09-24 are smaller and their CIs touch
zero in three of eight (dataset × encoder × classifier) cells.

## Design: stratify by stimulus set, do not pool items

Strata: original, swap. Each stratum's estimate uses only its own items; the
combined estimate is the equal-weight mean of the two strata.

**Primary (gated), stratified and dispersion-matched,** `experiments/residual_stratified.py`:
for b = 1..1000 (seed 0), in each stratum independently:
1. resample (model, rep) cells with replacement, separately for ignorance-S
   and paradox-S items (as in `register2_analyze.py`);
2. from the resampled items, draw size-k subsets, k = min(n_ign, n_par) of the
   resample, accepting the first draw whose dispersions differ by ≤ 0.005,
   up to 20,000 tries;
3. compute asym on the accepted subsets.
The combined value for b is the mean of the two strata's values. Report mean
and 2.5th/97.5th percentiles over b. A resample that fails to match in either
stratum is recorded as a failure.

**Reported, not gated:**
- Stratified without matching (cell bootstrap, 2000 resamples, seed 0).
- The full (unsplit) stratified asymmetry with the same `what. why`
  embedding, so the residual can be stated as a fraction of it.
- The same primary computation under Jev labels.

## Decision rule (fixed now, including the unevaluable case)

- **Evaluable** on an encoder if failures are ≤ 5% of the 1000 resamples in
  each stratum. Failures are dropped and counted.
- **Survives** if, on both encoders, evaluable and the combined mean > 0 with
  2.5th percentile > 0.
- **Explained by pooling/dispersion** if, on both encoders, evaluable and the
  combined mean ≤ 0.
- **Weakened** if evaluable on both encoders and neither of the above (e.g.
  positive mean, interval including 0, or the encoders disagree).
- **Unresolved** if not evaluable on at least one of the two encoders (one
  failing is enough). No other reading is substituted for the gate in that case.

## Prior, committed before running

Claude (Opus 5.5): P(Survives) = 0.40. Reasoning: the pooled residual was
+0.08 with a dispersion gap of +0.13 and a positive within-pair slope, which
could account for much of it; the per-dataset cells were already thin; and
matching small cells (k = 16 to 20) adds variance. Against that, the residual
appeared under three classifiers, and dispersion slightly suppressed the
unsplit target in today's test rather than producing it.

Tony: none requested this time; his stated stance on the previous test was to
wait and see.
