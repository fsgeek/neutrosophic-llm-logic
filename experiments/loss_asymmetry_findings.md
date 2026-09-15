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

## Addendum 2026-09-14: the size confound, tested

Two checks run after the note above (`asymmetry_breadth_check.py`,
`asymmetry_equal_n_check.py`, seed 0, same encoders).

**Breadth.** Loss-set sizes differ (ignorance 70 items, paradox 48; contingency
61, vagueness 53). Across the 10 pairs, asymmetry correlates with the size
difference: Spearman ρ = +0.67 (p = 0.03, MiniLM), +0.52 (p = 0.13, mpnet). A
larger set covers a smaller one better by chance alone, so size is a real
confound, and the target pair has the largest size gap (+22) of any pair.

**Size-matched.** Subsampling both sets to equal n (1000 draws):

| pair | full n | matched mean [2.5%, 97.5%] |
|---|---|---|
| ignorance→paradox (MiniLM) | +0.151 | +0.113 [+0.039, +0.151] |
| ignorance→paradox (mpnet) | +0.134 | +0.104 [+0.051, +0.132] |
| contingency→vagueness (MiniLM) | +0.048 | +0.045 [+0.039, +0.051] |
| contingency→vagueness (mpnet) | +0.085 | +0.081 [+0.072, +0.089] |

Set size accounts for roughly a quarter of the target's magnitude and none of
its sign. The control pair is unaffected by matching, so its failure is not a
size artefact either. Standing: the direction is not explained by how many
losses each phenomenon produced. Still unexplained, still not stimulus-swapped.
(Sign convention here: asym(A→B) = c(A→B) − c(B→A); the battery script prints
the coverage difference, which has the opposite sign for the control pair.)

## Addendum 2026-09-14 (later): the stimulus swap, pre-registered and run

Pre-registration: `stimulus_swap_prereg.md` (committed and stamped before the
first call; priors: Claude 0.55, Tony 0.85). Data: `data/s4_stimulus_swap.csv`,
125 calls, 125 parsed, 0 errors. Analysis: `analyze_stimulus_swap.py`.

| cell | MiniLM | mpnet |
|---|---|---|
| original ign→par | +0.151 [+0.043, +0.189] | +0.134 [+0.050, +0.174] |
| T1 swap ign→swap par | +0.207 [+0.055, +0.230] | +0.237 [+0.082, +0.281] |
| T2 orig ign→swap par | +0.171 [+0.032, +0.210] | +0.107 [+0.040, +0.155] |
| T2 swap ign→orig par | +0.210 [+0.061, +0.230] | +0.250 [+0.077, +0.292] |
| control orig con→vag | +0.048 [+0.029, +0.083] | +0.085 [+0.060, +0.094] |
| control swap con→vag | +0.019 [−0.012, +0.041] | +0.017 [−0.033, +0.049] |

**Verdict under the fixed rule: the sign holds.** All four target cells are
positive with 95% intervals excluding zero on both encoders, and the swap
magnitudes are larger than the original, not smaller. The asymmetry is a
property of the phenomena's loss vocabularies, not of the two sentences.

**The control resolved the other way.** On the swap sentences the
contingency→vagueness asymmetry collapses to zero on both encoders. Its
original sign-stability was stimulus-bound. So the June battery's control did
what a control should, one run late: the target survives a stimulus change and
the control does not.

Post hoc (not pre-registered, labelled as such): size-matched target on the swap
data, n = 52 per set, 1000 draws: +0.186 [+0.093, +0.211] (MiniLM),
+0.222 [+0.152, +0.242] (mpnet).

Also noted while checking: the original S4 file has 23 excluded rows (18
Mistral, 5 Llama, API errors), so Mistral is thin in the original asymmetry
cells. `data/s4_mistral_rerun.csv` exists and was not used by these scripts.
The swap run had no exclusions.

Standing now: the direction is real, survives a change of sentences and a size
match, and has no theory. Tony's prior (0.85) was the better one.
