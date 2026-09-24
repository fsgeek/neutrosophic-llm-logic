"""POST HOC robustness classifier for the register test: Jev (TypeSafe System One) as a third labeller.
Not pre-registered (added 2026-09-24 after the judge result); reported, not gating.
Same WORLD/SENTENCE question as the judge, cast as a Jev Choice with criteria. One call per loss item,
each seeing only `what` and `why`. Writes data/register2_jev_labels.csv with probabilities and request ids."""
from __future__ import annotations
import csv, json, sys, time
from pathlib import Path
from typesafe_sdk import Choice, TypeSafeClient
IN, OUT = Path("data/register2_labels.csv"), Path("data/register2_jev_labels.csv")
LENS_VERSION = "1"
INSTRUCTIONS = ("A language model was asked to evaluate a statement and to declare what it could not evaluate. "
                "The text is one such declared limitation, followed by the reason the model gave for it. "
                "Classify what the limitation is ABOUT. Judge only the limitation text shown.")
CRITERIA = {
    "world": {"what": ("The limitation concerns facts, evidence, data, events, future states, or knowledge about the "
                       "world that the model lacks or cannot access. Examples: 'no information about the number of stars'; "
                       "'cannot know what will happen tomorrow'; 'no historical record of this'; 'lacks empirical data'."),
              "not_for": "A limitation about the wording, logical form, vagueness, self-reference or semantics of the statement itself."},
    "sentence": {"what": ("The limitation concerns the statement itself: its wording, self-reference, logical form, "
                          "vagueness of its terms, ambiguity, or the semantics of assigning it a truth value. Examples: "
                          "'the sentence refers to itself'; 'the term tall has no sharp threshold'; 'the statement is "
                          "internally contradictory'; 'truth value cannot be assigned without a paradox'."),
                 "not_for": "A limitation about missing facts, evidence, data or knowledge of the world."},
}
QUESTION = Choice(instructions=INSTRUCTIONS, criteria=CRITERIA)
LENS_TEXT = json.dumps(QUESTION.model_dump(mode="json"))

def pick_model(client):
    """Pin the versioned id the levadura_salvaje lenses use; the listing exposes only aliases."""
    try:
        client.system_one(state={"loss": "probe"}, questions={"register": QUESTION}, model="jev-1.13.0")
        return "jev-1.13.0"
    except Exception as e:
        print(f"jev-1.13.0 unavailable ({e}); falling back to jev-latest (alias; resp.model recorded per row)", flush=True)
        return "jev-latest"

def main():
    rows = list(csv.DictReader(open(IN))); client = TypeSafeClient(timeout=60)
    model = pick_model(client); print(f"{len(rows)} items; model {model}; lens sha not stored, lens text stored per row", flush=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["source", "row", "item", "phenomenon", "model", "rep", "severity", "judge_label",
                                       "jev_label", "p_world", "p_sentence", "confidence", "jev_model", "request_id", "lens_version"])
        for n, r in enumerate(rows, 1):
            text = f"Limitation: {r['what']}\nReason given: {r['why']}"
            for attempt in range(3):
                try:
                    resp = client.system_one(state={"loss": text}, questions={"register": QUESTION}, model=model); break
                except Exception as e:
                    resp = None; err = e; time.sleep(2)
            if resp is None:
                w.writerow([r["source"], r["row"], r["item"], r["phenomenon"], r["model"], r["rep"], r["severity"], r["label"],
                            "ERROR", "", "", "", model, "", LENS_VERSION]); continue
            a = resp.choices["register"]; p = dict(a.probabilities)
            w.writerow([r["source"], r["row"], r["item"], r["phenomenon"], r["model"], r["rep"], r["severity"], r["label"],
                        a.choice.upper(), p.get("world", ""), p.get("sentence", ""), a.confidence, resp.model, resp.request_id, LENS_VERSION])
            f.flush()
            if n % 100 == 0: print(f"  {n}/{len(rows)}", flush=True)
    client.close(); print("done ->", OUT)

if __name__ == "__main__":
    main()
