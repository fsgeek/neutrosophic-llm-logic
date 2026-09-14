# Pre-registration: stimulus swap for the declared-loss asymmetry (2026-09-14)

Written and committed (signed, OpenTimestamps-stamped) BEFORE any API call.

## Question

Is the directional asymmetry c(ignorance→paradox) > c(paradox→ignorance),
found on the original S4 data (`loss_asymmetry_findings.md`), a property of the
phenomena or of the two sentences that instantiated them?

## Design

Same protocol as the original S4 run (`src/prompts.py` S4_SYSTEM/S4_USER,
temperature 0.7, max_tokens 1500), same five models via OpenRouter
(claude-sonnet-4.6, llama-4-maverick, deepseek-v3, qwen3-235b, mistral-medium-3.1),
5 reps per cell, ONE NEW statement per phenomenon, S4 only. 125 calls.
Output: `data/s4_stimulus_swap.csv`. Script: `experiments/run_stimulus_swap.py`.

New statements (type-matched to the originals, different vocabulary and domain):

| Phenomenon | Original | Swap |
|---|---|---|
| Paradox (Logical) | This sentence is false. | The next sentence is true. The previous sentence is false. |
| Ignorance (Epistemic) | The number of stars in the universe is even. | Julius Caesar had an even number of hairs on his head at the moment he died. |
| Vagueness (Fuzzy) | John is 1.75 meters tall, therefore John is tall. | Maria has 3,000 hairs on her head, therefore Maria is bald. |
| Contradiction (Ethical) | Lying to save an innocent life is morally right and wrong at the same time. | Breaking a promise to prevent serious harm to a stranger is both morally required and morally forbidden. |
| Contingency (Future) | It will rain in New York tomorrow. | The Frankfurt stock exchange will close higher next Monday than it closes this Friday. |

## Measure

asym(A→B) = c(A→B) − c(B→A), c(A→B) = 1 − severity-weighted max-cosine coverage
of A's `what` losses by B's. Encoders all-MiniLM-L6-v2 and all-mpnet-base-v2.
Bootstrap 95% CI over (model, rep) cells, 2000 resamples, seed 0.
Script: `experiments/analyze_stimulus_swap.py`.

## Tests, fixed now

T1 (within-swap): on the swap data alone, asym(ignorance→paradox).
T2 (cross): asym using original ignorance vs swap paradox, and swap ignorance
vs original paradox. Four cells in all with T1 and the original.
Control: asym(contingency→vagueness) on the swap data; original sign was
positive under this convention (contingency's losses covered worse by vagueness's).

## Decision rule

- **Sign holds** if T1 is positive with CI excluding 0 on both encoders AND both
  T2 cells are positive with CI excluding 0 on both encoders. Then the asymmetry
  is a property of the phenomena's loss vocabularies, and deserves a theory.
- **Sign is stimulus-bound** if T1 or either T2 cell is negative or has a CI
  including 0 on either encoder. Then the note's last line is: it was the sentences.
- Control is reported, not gated. If the control flips sign, that is evidence the
  control's original asymmetry was stimulus-bound.
- No thresholds are changed after data are seen. Parse failures are excluded and
  counted.

## Priors, committed blind

Claude (this instance): P(sign holds) = 0.55. Reasoning: the size-matched check
removed the mechanical explanation, but one sentence per phenomenon is one
sentence, and I could not guess the direction from theory before the data.
Tony: ___ (to be entered before results are shown to him).
