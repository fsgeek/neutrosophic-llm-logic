# Directional asymmetry in S4 declared losses: one robust number, two falsified theories, one failed control (v0.1)

**Current status (2026-10-08):** the direction survived a size match (post hoc),
a stimulus swap and a register split (both pre-registered); see the addenda
below, which supersede the body where they differ. Standing: a near-categorical
register split, a composition effect explaining most of the direction, and a
within-register residual with no theory. Dispersion matching (pre-registered,
2026-10-08): the target survives wherever matching is possible; the pooled data
cannot be matched by the registered design. Still open: dispersion for the
pooled and within-register cells, prompt variation, an encoder from outside the
sentence-transformers family.

**Original status (2026-09-13), kept as written:** exploratory measured note
(experiments 2026-06-04/05; re-run verbatim 2026-09-13).
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

## Addendum 2026-09-24: the two-way register test, pre-registered and run

Pre-registration: `register2_prereg.md` (priors on P(vanishes): Claude 0.45,
Tony 0.10). Labels: `data/register2_labels.csv`, 633 loss items, judge
gpt-4o-mini at temperature 0 seeing only `what` and `why`; 0 unparsed.
Analysis: `register2_analyze.py`. Judge/anchor-rule agreement 0.85 to 0.88.

**P1, the premise, holds and is near-categorical.** Share of world-directed
losses: ignorance 0.71 (original), 0.76 (swap); paradox 0.04 in both. The
register split is real and much sharper than expected.

**F-W is inconclusive by rule:** paradox has 4 world-directed losses of its
100 (pooled; the target pair has 236 items in all), below the pre-registered
minimum of 10. *(Corrected 2026-10-08: this line originally read "4
world-directed losses in 236 items," which reads as paradox's total; the
counts in `data/register2_labels.csv` are 48 + 52 = 100 paradox losses.)* The world register cannot be
tested within itself because paradox almost never produces it.

**F-S, within the sentence register, pooled data (the gating cell):**

| classifier | MiniLM | mpnet |
|---|---|---|
| judge | +0.079 [+0.013, +0.127] | +0.086 [+0.038, +0.126] |
| anchor rule | +0.079 [+0.024, +0.119] | +0.113 [+0.069, +0.150] |

Full (unsplit) asymmetry on the pooled data: +0.204 (MiniLM), +0.214 (mpnet).

**Verdict under the fixed rule: survives.** An evaluable within-register cell is
positive with CIs excluding zero on both encoders. Register does not explain
the asymmetry away. Tony's prior was right for the second time.

**Honest reading, past the binary.** Register explains a large part of it:
within the sentence register the asymmetry is about 40% of the full value, and
the cross-register cell X (ign_W→par_S) is large (+0.16 to +0.19, judge,
pooled). So the composition story is true as far as it goes: most of the
direction comes from ignorance losses being about the world and paradox losses
being about the sentence. But a residual remains among sentence-directed losses
alone: even when both phenomena's losses are about the statement, ignorance's
are covered worse by paradox's than the reverse. On the separate datasets that
residual is smaller and its CI touches zero in three of eight cells, so it is
real in the pool and thin in the parts.

Standing: the direction is now three-layered. (1) A near-categorical register
split, which is itself a clean finding about declared losses. (2) A composition
effect from that split, which accounts for most of the asymmetry. (3) A residual
within-register asymmetry with no theory. Layer 3 is the open problem; layers 1
and 2 are what to hand over.

### Post hoc (2026-09-24): Jev as a third classifier

Not pre-registered; added after the judge result to test whether the register
split is an artefact of the judge model. `register2_jev.py` casts the same
question as a TypeSafe System One Choice (model pinned to jev-1.13.0, one call
per loss, seeing only `what` and `why`); `register2_jev_analyze.py` reports.
Labels with probabilities and request ids: `data/register2_jev_labels.csv`.

- Judge/Jev agreement 0.897 overall (ignorance 0.86, paradox 0.99). Jev calls
  ignorance losses 62% world-directed (judge 74%), paradox 3% (judge 4%).
- Jev's median confidence is 0.99; on the items where it disagrees with the
  judge it is 0.64. The disagreements sit where the instrument itself is unsure.
- Within the sentence register under Jev's labels, pooled: +0.091 [+0.046,
  +0.127] (MiniLM), +0.101 [+0.062, +0.133] (mpnet). Same verdict as the judge:
  the residual survives.

Three classifiers (LLM judge, embedding anchors, Jev) now agree on the split
and on the within-register residual.

## Addendum 2026-10-08: dispersion, computed in September and not reported

`asymmetry_breadth_check.py` (the 2026-09-14 breadth check) prints three
breadth correlations across the 10 pairs; the addendum above reported only
set size. Re-run today, unchanged script, same data:

| breadth measure (A minus B) | MiniLM ρ (p) | mpnet ρ (p) |
|---|---|---|
| n (set size) | +0.67 (0.03) | +0.52 (0.13) |
| n distinct `what` strings | +0.42 (0.23) | +0.25 (0.50) |
| dispersion (1 − mean pairwise cos) | −0.42 (0.23) | **−0.69 (0.03)** |

Dispersion tracks asymmetry across pairs on mpnet: the less dispersed set of
a pair tends to be the one covered worse. For the target pair the dispersion
gap is small (ignorance minus paradox: −0.018 MiniLM, −0.023 mpnet), so it is
unlikely to carry the target, but no dispersion-matched test has been run and
this omission is of the same kind as the June memory's missing control,
smaller. Ten pairs, two encoders from one family, no correction for the three
correlations tested; read as a lead, not a result.

A related caution about the estimator itself: max-cos coverage between two
differently shaped point clouds is generically nonzero in one direction, so
"c is asymmetric" is close to guaranteed for any two loss sets that differ.
What carries information is which pairs, which direction, and whether it
survives controls; that is the standard the tests above were held to.

## Addendum 2026-10-08 (later): the dispersion-matched test, pre-registered and run

Pre-registration: `dispersion_prereg.md`, committed and stamped with its
script before it ran (8146a96). Priors: Claude P(target survives) = 0.75 and
P(mpnet cross-pair |rho| < 0.4 after matching) = 0.55; Tony declined a number
("I'll wait and see what we actually learn"). Script `dispersion_matched.py`;
full output `dispersion_matched_output.txt`. No new data.

**Target, primary estimator** (size-k subsets accepted when dispersions differ
by ≤ 0.005; mean [2.5%, 97.5%] over 1000 accepted draws):

| data | MiniLM | mpnet | size-matched only (for comparison) |
|---|---|---|---|
| original | +0.120 [+0.053, +0.149] | +0.109 [+0.053, +0.132] | +0.113 / +0.104 |
| swap | +0.195 [+0.116, +0.210] | +0.229 [+0.222, +0.236] | +0.186 / +0.222 |
| pooled | **unmatchable** (0 of 200,000) | **unmatchable** (0 of 200,000) | |

**Verdict by the letter of the rule: the gate is not met, because half of it
cannot be evaluated.** The rule required survival on both the original and the
pooled data; the pooled data are unmatchable on both encoders, which the rule
says makes that dataset not evaluable, and the rule did not say how the gate
resolves then. I am not resolving that ambiguity in my favour: the 0.75 prior
is scored as unresolved, not won. "Explained by dispersion" is not met either.

**What the evaluable data say.** On the original and the swap data, matching
dispersion changes almost nothing: the matched values are within 0.01 of the
size-matched ones and slightly larger, all intervals exclude zero. Within these
pairs the slope of asymmetry on dispersion gap is positive (+0.25 to +0.44),
the opposite sign to the cross-pair correlation, and ignorance is the *less*
dispersed set, so in these data dispersion, if anything, slightly suppresses
the target. It does not produce it.

**Why the pooled data could not be matched, and what that changes.** Pooling
reverses the dispersion gap: ignorance minus paradox is −0.02 within each
dataset but +0.12 (MiniLM) / +0.10 (mpnet) pooled. Ignorance's two sentences
(stars, Caesar's hair) produce losses in different places, while paradox's two
liar-type sentences produce losses in the same place, so pooling spreads
ignorance and not paradox. Random subsets cannot bridge a gap that size. The
secondary estimator (regression intercept at zero gap, reported not gated)
gives +0.126 [+0.110, +0.141] (MiniLM) and +0.110 [+0.096, +0.125] (mpnet),
but it extrapolates from gaps clustered near +0.11 to zero, and its intervals
resample draws of the same items, so they are far too narrow. Read it as
"positive", nothing more precise.

**Consequence for earlier numbers:** the register test (addendum 2026-09-24)
and the note to Maikel use pooled data. The pooled unsplit asymmetry (+0.20)
carries a dispersion difference created by pooling two stimuli, which the
per-dataset values do not; per-dataset values (+0.13 to +0.24) are the cleaner
comparison. The within-register residual has not been dispersion-checked.

**Secondary, cross-pair (descriptive):** only 5 of 10 pairs could be matched
on each encoder (pairs with gaps above about 0.03 fail). Over those 5,
Spearman(matched asym, full gap) = −0.30 (MiniLM, p = 0.62), −0.90 (mpnet,
p = 0.04). By the letter the 0.55 prior lost (|rho| did not fall below 0.4);
with five pairs, half the set unmatchable, and a different subset per encoder,
it says little either way.

**Design lesson:** rejection matching on random subsets only works when the
sets are already close; the pooled gap was not known when the rule was
written, and should have been computed first. A matching design that can bridge
large gaps (e.g., choosing subsets to target a dispersion) would be the next
step if the pooled question matters.

Standing after this: the target survives dispersion matching wherever matching
is possible; the pooled data need a different design; the cross-pair dispersion
pattern is unresolved.
