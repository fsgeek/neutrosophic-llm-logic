# Pre-registration: two-way register test for the ignorance→paradox asymmetry (2026-09-24)

Committed (signed, stamped) BEFORE any classification call or analysis.

## Hypothesis (from the swap result, 2026-09-14)

The losses a model declares about ignorance name things in the world it cannot
reach (world-directed, W); the losses it declares about paradox name things about
the statement itself (sentence-directed, S); and W vocabulary covers S vocabulary
better than the reverse. If so, the asymmetry c(ign→par) > c(par→ign) is a
composition effect of register, and should VANISH within a single register.

## Data

`data/s4_tensor_results.csv` (original) and `data/s4_stimulus_swap.csv` (swap),
Success rows, every loss item with a non-empty `what`. Analysed separately and pooled.

## Classifier (primary), fixed now

openai/gpt-4o-mini via OpenRouter, temperature 0, one call per loss item. The
judge sees ONLY the loss's `what` and `why` text. It does not see the statement,
the phenomenon label, the model, or the T/I/F values. Prompt
(`experiments/register2_classify.py`):

> A language model was asked to evaluate a statement and to declare what it
> could not evaluate. Below is one such declared limitation. Classify what the
> limitation is ABOUT: **WORLD** if it concerns facts, evidence, data, events,
> future states, or knowledge about the world that the model lacks or cannot
> access; **SENTENCE** if it concerns the statement itself: its wording,
> self-reference, logical form, vagueness of its terms, ambiguity, or the
> semantics of evaluating it. Answer with exactly one word: WORLD or SENTENCE.

Secondary (robustness, no API): nearest-anchor cosine under all-mpnet-base-v2
against two fixed anchor sets of five phrases each, listed in the script.
Reported; not gating.

## Tests

P1 (premise): share of W among ignorance losses exceeds share of W among
paradox losses, in the original and in the swap data. If P1 fails, the
hypothesis is dead before the falsifier and the result is reported as such.

F (falsifier): coverage asymmetry computed WITHIN register:
- F-W: asym(ign_W → par_W)
- F-S: asym(ign_S → par_S)
Same measure as before (severity-weighted max-cosine coverage, asym = c(A→B) −
c(B→A)), both encoders, bootstrap over (model, rep) cells, 2000 resamples, seed 0.
A cell is evaluable only if both subsets have ≥ 10 items; otherwise inconclusive.

X (composition prediction): asym(ign_W → par_S) should be large and positive
if register drives the effect. Reported, not gating.

## Decision rule

- **Vanishes** (register explains it): every evaluable F cell has a 95% CI
  including 0 on both encoders, on the pooled data.
- **Survives** (register does not explain it): any evaluable F cell is positive
  with a CI excluding 0 on both encoders, on the pooled data.
- Otherwise **inconclusive**, reported as such. No thresholds change after data.

## Priors, committed blind: P(vanishes)

Claude (this instance): 0.45. "The ranking test already inverted a theory that
felt this good."
Tony: 0.10. "Not because I have any deep knowledge, only because I think
sometimes we are surprised."
