# Draft reply to Maikel Leyva-Vázquez (JEPR editorial board invitation)

Status: draft for Tony to edit and send. Written 2026-09-13 by a Claude instance in Tony's voice; not sent.

---

Dear Maikel,

Thank you for the invitation, and for the transparency about the response paper. I would be glad to join the board, and the two sections you name (audit of uncertainty frameworks, and negative results) are the ones I would want to work in, since most of what I have learned in the past year came from experiments that did not do what I expected them to do. Two or three manuscripts a year and the occasional handling-editor role is a load I can carry, and I have no objection to the three-year term.

Before I say yes formally I want to raise one thing, because I would rather raise it now than have it surface later. Your response to "From Scalars to Tensors" is under review at a journal of which you are Editor-in-Chief, and I would be a board member at that journal. I read the reproducibility package you released on GitHub, including the pre-registration, the nine rounds of adversarial review, and the cover letter, so I already know the paper concedes several points and withdraws several claims of its own earlier draft; I have no complaint about its handling. What I would ask is that it be handled under the same independent-editor rule your ethics statement applies to board members' submissions, and that I be free to review it openly rather than shielded from it. Indeed, I would rather review it than not, because the paper reads my own work more carefully than most reviewers have, and it uses Vaastav Anand's and my non-identifiability result *against* the strong reading of my earlier paper, which is the correct use of it.

Since your rules say referees receive the data and code with the manuscript, and negative results are a standing section, I will offer you one in return. After your §5.4 defined the plithogenic contradiction function as symmetric by axiom, I ran a small battery (with a Claude instance, as with the paper itself) on the S4 declared-loss data asking whether a directional coverage estimator of c is measurably asymmetric. One pair (ignorance and paradox) shows a stable asymmetry across five vendors and two encoders, and every structural explanation I pre-registered for *why* was falsified by the data, including a control pair that was supposed to come out symmetric and did not. The honest conclusion is narrow: symmetry of c is imposed by choosing a symmetric estimator (Jaccard, paired cosine), and is not something the declared losses themselves exhibit. That leaves a non-commutative c(v_i → v_j) as an open question in your formalism rather than a result in mine, which is why I think it belongs in your negative-results section and not in a paper of mine. The scripts, data and the note are in the public repository, each commit signed and timestamped, and I would be happy to send the note directly if that is easier.

I would welcome a short call; if you send a few times that work for you I will find one that works for me.

With thanks and warm regards,

Tony Mason
University of British Columbia and Georgia Institute of Technology
ORCID 0000-0002-0651-5019
