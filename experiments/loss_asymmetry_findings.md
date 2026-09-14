# Directional asymmetry in S4 declared losses: one robust number, two falsified theories, one failed control (v0.1)

**Status: exploratory measured note (experiments 2026-06-04/05; re-run verbatim 2026-09-13).**
Not a result to send. Not stimulus-swap tested. No validated generative model.
Producers: `loss_asymmetry.py`, `loss_asymmetry_battery.py`, `ranking_test.py`,
`register_test.py`, all over `data/s4_tensor_results.csv`, encoders
`all-MiniLM-L6-v2` and `all-mpnet-base-v2`, seed 0, 2000 bootstrap resamples over
(model, rep) cells. Re-run log: session scratchpad, 2026-09-13; numbers below are
from that run and match the June run to the third decimal.

## What was asked

Leyva-Vázquez & Smarandache (2026, arXiv:2605.24053 §5.4) define the plithogenic
contradiction function symmetric by axiom, c(v_i, v_j) = c(v_j, v_i). Their
declared-loss manuscript (Sept 2026) operationalises c as Jaccard on
justifications and lists "no other estimator was compared" as a limitation.
We asked whether a *directional* coverage estimator, c(A→B) = 1 − coverage of
A's losses by B's, is measurably asymmetric on the S4 data, and whether the
asymmetry has a structural explanation.

## Pre-registered predictions (Tony's, blind, June 2026)

1. Ignorance↔paradox is the largest asymmetry, with c(ignorance→paradox) >
   c(paradox→ignorance), because ignorance's predicament is contained in paradox's.
2. Control pair vagueness↔contingency: mutual overlap, not containment, so
   **small magnitude and sign-unstable** across encoders and measures.
3. Ranking: a blind 10-pair ordering by containment strength predicts measured
   magnitude (`ranking_test.py`).
4. Register: cross-register pairs (outward: ignorance, contingency; inward:
   paradox, vagueness, contradiction) show larger asymmetry than same-register
   pairs (`register_test.py`).

## What the data said

| Test | Prediction | Measured | Verdict |
|---|---|---|---|
| Target sign and magnitude | large, + | max-cos asym +0.151 (MiniLM), +0.134 (mpnet); 95% CI excludes 0 on both; rank 1 of 10 on both; positive in all 5 vendors on both encoders (0.011 to 0.108) | **held** |
| Three measures | sign survives | max-cos, top-k, softmax all +, CIs exclude 0 | held |
| **Control pair** | small, sign-unstable | −0.048 (MiniLM), −0.085 (mpnet); **CI excludes 0 on both; sign-stable negative** on all three measures | **failed** |
| Ranking (Spearman, prior vs measured) | ρ > 0 | ρ = −0.78 (MiniLM), −0.53 (mpnet); one-sided p = 0.996, 0.943 | **inverted** |
| Register (Mann-Whitney cross > same) | cross larger | means 0.073 vs 0.063 and 0.079 vs 0.085; p = 0.46, 0.76 | **null** |

## Honest reading

The target number is robust: same sign in ten of ten (vendor × encoder) cells,
three measures, two encoders, weighted and unweighted. That is all it is.

The control failed its own pre-registration. The script's docstring said: "If
our measure paints THAT asymmetric too, the instrument is noise." It did, at
about half the target's magnitude but with equal sign stability. The
pre-registered criterion was sign instability, not magnitude, so the honest
verdict is that the instrument registers directional structure on a pair where
the containment story predicts none. The containment theory (ranking test) is
inverted by the data, and the register theory is null. We therefore have a
correspondence-table number with no generative model that survived contact.

Candidate confounds not excluded: vocabulary breadth of the loss descriptions
(a phenomenon whose losses are described in more diverse language covers more
and is covered less), severity mass, encoder geometry shared by both encoders,
and stimulus identity (one statement per phenomenon; a swap was never run).

## What survives, and is small

The only claim this supports is about estimators, not epistemics: any
coverage-based estimator of c is non-symmetric on this data, so symmetry of c
is a property imposed by the choice of a symmetric estimator (Jaccard, cosine
on paired justifications), not a property found in the declared losses. That is
enough to make "c(v_i→v_j) ≠ c(v_j→v_i)" a well-posed open question in their
formalism. It is not enough to say what the direction means.

## Next, if this is pursued

1. Stimulus swap: a second statement per phenomenon; does the target sign
   survive a change of stimulus with the phenomenon held fixed?
2. Vocabulary-breadth control: match A and B on number of distinct loss
   descriptions and on mean pairwise within-set cosine before computing coverage.
3. Only then a theory.

If this note has drifted from the scripts and the data file, believe the scripts
and the data file.
