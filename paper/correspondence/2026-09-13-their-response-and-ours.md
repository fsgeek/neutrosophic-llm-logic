# What Leyva-Vázquez and Smarandache say about our work, and what we say back

Memo, 2026-09-13. Sources: their reproducibility package
(github.com/mleyvaz/plithogenic-declared-loss-evaluation, manuscript v22 dated
2026-09-11, "Declared-Loss Evaluation of Language Models as Plithogenic
Neutrosophic Structure: Formal Embedding, Auditor Effects, and the Limits of
Verbalised Triplets", prepared for *AI* (MDPI); earlier for *Entropy*), plus
arXiv:2605.24053 v2 §5.4, the April plithogenic-tensor note, and the Spanish
Type-K note. Their "Is the Ladder Measurable?" preprint (Aug 2026, cites us)
could not be fetched (preprints.org returns 403); not read.

## Their claims about our paper, sorted

**They concede, in writing, with pre-registered gates:**
- The verbalised (T, I, F) triplet is *not* a reading of internal state.
  Verbalised I moves with framing (interaction F = 68.9); hyper-truth appears
  in 0 of 60 items under a neutral frame and only when the protocol invites it.
  Two evidence-side probes failed their gates. They use Mason & Anand
  (arXiv:2603.20531) as the reason. This is the "auditor effect": the report
  is a property of the interface, not the model.
- Their own earlier draft's injectivity claim, lattice-homomorphism claim, and
  metric were wrong and are withdrawn (found by adversarial review of the
  released package).

**They push back on us, correctly:**
1. *Absorption is not a limitation of neutrosophic logic.* Scalar NL can
   already write paradox as (0.5, 1, 0.5) and ignorance as (0, 1, 0); Claude
   does exactly that in our data. Absorption is what certain models emit under
   certain prompts. Our paper's framing ("scalars cannot express") overreaches;
   the defensible claim is "these models did not express it under S1, and
   did under S4."
2. *"The model has the distinction" is unsupported.* Our sentence "the model
   has the distinction; the scalar cannot express it; the tensor can" asserts a
   latent state from text. By our own (Mason & Anand) theorem, that inference is
   not licensed. The declared losses discriminate *stimuli*; whether they read
   a state is exactly what cannot be shown from text.
3. *S4 is not a new representational structure.* Declared-loss outputs embed
   injectively into single-valued plithogenic neutrosophic structures
   (Smarandache 2018); for a fixed spectrum the scalar is a factor projection of
   a product lattice, and the Absorption Problem is that projection's
   non-injectivity. Fine. Our Prop-2-shaped point is now their Theorem 1.
4. *Our Jaccard numbers are not their c.* Word-level Jaccard on `what` fields is
   a statistic on words, not a similarity of spectra as label sets; they decline
   to evaluate their index on our summaries.
5. *Intervals don't fix it.* Injective recoding of degrees into intervals does
   not make the projection lossless; their registered interval pilot separates
   paradox from ignorance only under cross-vendor transfer (AUROC 0.66 vs 0.41),
   not within vendors (0.70 vs 0.68), and the interval tautology control fails.

**Their new empirical finding that matters to us most:**
- The 4 × 3 auditor crossover: the rate of extended-range (S4-O.C) usage depends
  on *which model audits which*. Pooled: Claude-as-auditor 0.49, Llama 0.515,
  GPT-4o 0.12; χ² = 83.5, p = 7e-19. The evaluation is a relation between
  auditor and audited, not a property of the audited output.

## What we say back

**Concede 1 and 2 outright**, in whatever we write next. The overclaim was
"scalars cannot express"; the truth is "these models did not, under this
protocol." And "the model has the distinction" is the latent-variable sentence
our own theorem forbids. Say so plainly and cite them for catching it. This is
the same discipline they credit us with in v2 §1; return it.

**Accept 3 as a gift.** Their formal embedding is what our paper invited. The
open items they list as Limitation 2 are exactly the shape of the next thing:
"alignment of spectra across statements... not established"; "the contradiction
function is Jaccard on justifications; no other estimator was compared."

**Push on one thing, and only one.** Their contradiction function is symmetric
by axiom and symmetric by estimator. Their own auditor crossover shows the
evaluation relation is *directional*: c(Claude reads Llama) is not
c(Llama reads Claude). Our findings note (`experiments/loss_asymmetry_findings.md`)
shows a coverage estimator of c is measurably non-symmetric on the S4 data, and
that no structural theory of the direction survived pre-registration. Together:
symmetry is an axiom their data already strain, and a non-commutative
c(v_i → v_j) is a well-posed open problem *in their formalism*. Hand it to them
as an open problem, not as a result. That is the chair pulled out.

**Do not send** the asymmetry finding as a positive result. The control failed.

**The two-path consensus demonstration** (their AIHealthProject case: Cx rises
0.57 → 0.94 under mutual adjustment *and* under capitulation, same number) is
the instrument for the same point one paper over (the Ayni method's Cx is
symmetric and memoryless). It still belongs in the gift basket; `commune.py`
in hamutay is where it runs. Not urgent for the JEPR reply.

## Shape of a reply note (if we write one)

Title (working): *Declared losses read the interface, not the model: a
concession, and one open problem for the contradiction function.*
Short. Four parts: (i) what we withdraw and why (their probes + our own
theorem); (ii) what survives (protocol-level discrimination of stimuli, which
is what an audit interface needs); (iii) the auditor crossover read as a
directional relation; (iv) the non-commutative c as an open problem, with the
negative result attached. Their journal's negative-results section is the
natural home, and a board member's submission goes to an independent editor.
