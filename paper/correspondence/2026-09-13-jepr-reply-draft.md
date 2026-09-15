# Draft reply to Maikel Leyva-Vázquez (JEPR editorial board invitation)

Status: draft for Tony to edit and send. Written 2026-09-13 by a Claude instance in Tony's voice; not sent.

---

Dear Maikel,

Thank you for the invitation, and for the transparency about the response paper. I would be glad to join the board, and the two sections you name (audit of uncertainty frameworks, and negative results) are the ones I would want to work in, since most of what I have learned in the past year came from experiments that did not do what I expected them to do. Two or three manuscripts a year and the occasional handling-editor role is a load I can carry, and I have no objection to the three-year term.

Before I say yes formally I want to raise one thing, because I would rather raise it now than have it surface later. Your response to "From Scalars to Tensors" is under review at a journal of which you are Editor-in-Chief, and I would be a board member at that journal. I read the reproducibility package you released on GitHub, including the pre-registration, the nine rounds of adversarial review, and the cover letter, so I already know the paper concedes several points and withdraws several claims of its own earlier draft; I have no complaint about its handling. What I would ask is that it be handled under the same independent-editor rule your ethics statement applies to board members' submissions, and that I be free to review it openly rather than shielded from it. Indeed, I would rather review it than not, because the paper reads my own work more carefully than most reviewers have, and it uses the representational-impossibility result Vaastav Anand and I proved (arXiv:2603.20531) *against* the strong reading of my earlier paper, which is the correct use of it.

Since your rules say referees receive the data and code with the manuscript, I will offer you something in return, though it is smaller than a result and I want to describe it at the size it is. After your §5.4 defined the plithogenic contradiction function as symmetric by axiom, I asked (with a Claude instance, as with the paper itself) whether a directional coverage estimator of c is measurably asymmetric on the S4 declared-loss data. For one pair, ignorance and paradox, it is: ignorance's declared losses are covered poorly by paradox's, and paradox's are covered well by ignorance's, across five vendors and two encoders. I did not trust that, since the direction had no theory and the two structural explanations I pre-registered for it were both falsified, so this week we ran the tests that could have killed it. It survives matching the two loss sets for size, and it survives a pre-registered swap of every stimulus sentence for a new one in a different domain, in the same direction and with a larger magnitude, while a control pair that had looked asymmetric on the original sentences collapsed to zero on the new ones. So the asymmetry belongs to the phenomena and not to the sentences, and I still cannot tell you *why*. What I can tell you is narrower: on this data the symmetry of c is a property of the estimators (Jaccard, paired cosine) and not of the declared losses themselves, which makes a non-commutative c(v_i → v_j) a well-posed open question in your formalism rather than a result in mine. That is why I think it belongs with you. The pre-registration, the priors, the data and the scripts are in the public repository, each commit signed and timestamped, and I would be glad to send the note directly if that is easier.

I would welcome a short call; if you send a few times that work for you I will find one that works for me.

With thanks and warm regards,

Tony Mason
University of British Columbia and Georgia Institute of Technology
ORCID 0000-0002-0651-5019
