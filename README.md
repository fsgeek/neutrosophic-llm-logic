# neutrosophic-llm-logic (fork)

This is a fork of [mleyvaz/neutrosophic-llm-logic](https://github.com/mleyvaz/neutrosophic-llm-logic),
the reproducibility package for Leyva-Vázquez & Smarandache, *Breaking the
Chains of Probability* (`paper/FINAL_PAPER.md`). Their original README is kept
unchanged in [`README-original.md`](README-original.md); for their current
work, including v2.0 of this study (Zenodo DOI 10.5281/zenodo.19911845), see
their repository, which this fork has not merged.

The fork became the empirical home for a conversation with them about
declared losses and whether contradiction between them has a direction.

## What is here, in the order it happened

1. **Cross-vendor replication** (Feb 2026, `experiments/README.md`, `src/`,
   `data/cross_vendor_results.csv`): their T/I/F protocol, published prompts,
   five vendors, five repetitions.
2. **S4, declared losses** (Feb–Mar 2026, `paper/TENSOR_EXTENSION_PAPER.md`,
   `paper/latex/`, arXiv:2604.09602): models declare what a scalar verdict
   loses. Two of that paper's claims were corrected by the authors' response
   manuscript and we accept both: "scalars cannot express" overreaches (scalar
   neutrosophic logic can write the distinction; these models did not, under
   this protocol), and "the model has the distinction" is a latent-state claim
   the text cannot license. See `paper/correspondence/2026-09-13-their-response-and-ours.md`.
3. **Directional contradiction** (June and Sept–Oct 2026, `experiments/`):
   does an estimator of the plithogenic contradiction function c that is
   *allowed* to be asymmetric come out asymmetric on the declared losses?
   Start with **[`experiments/loss_asymmetry_findings.md`](experiments/loss_asymmetry_findings.md)**.
   In short: one pair (ignorance→paradox) is directional; the direction
   survived a size match, a pre-registered stimulus swap, and a pre-registered
   register split; most of it is explained by a near-categorical split between
   world-directed and sentence-directed losses; a residual inside one register
   has no theory. Failed controls, falsified theories and lost priors are in
   the note, not removed from it.
4. **Correspondence** (`paper/correspondence/`): the memo on their response,
   a superseded draft, and the note actually sent.
5. **The turn-local defense construction** (`paper/impossibility_construction.md`):
   a June 2026 working draft, unreviewed by an adversary; not a result.

## How to check us

Since 2026-09-13 every commit is signed (research@wamason.com) and followed
by an OpenTimestamps proof in `timestamps/` (anchored proofs in
`timestamps/anchored/`; `scripts/ots-upgrade.sh` moves them). Pre-registrations
(`experiments/*_prereg.md`) were committed and stamped before their first API
call, with blind priors recorded; work before that date is not timestamped and
the findings note says which tests were post hoc. If a summary here disagrees
with the scripts and data, believe the scripts and data.

## Who did the work

Tony Mason with Claude instances (Opus 4.6 in Feb–Mar; a Claude instance in
June; Kutichiq, a Claude Fable 5.1 instance, in September; Claude Opus 5.5 in
October). Original study, data and protocol: Maikel Leyva-Vázquez and
Florentin Smarandache.

License: MIT, as upstream (`LICENSE`).
