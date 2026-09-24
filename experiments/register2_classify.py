"""Classify every declared loss as WORLD or SENTENCE, blind to phenomenon. Pre-registered in register2_prereg.md.
Writes data/register2_labels.csv with one row per loss item (source file, row index, item index, what, why, label)."""
from __future__ import annotations
import csv, json, os, sys, time
from pathlib import Path
from openai import OpenAI
SOURCES = {"orig": "data/s4_tensor_results.csv", "swap": "data/s4_stimulus_swap.csv"}
OUT = Path("data/register2_labels.csv")
PROMPT = ("A language model was asked to evaluate a statement and to declare what it could not evaluate. "
          "Below is one such declared limitation. Classify what the limitation is ABOUT: "
          "WORLD if it concerns facts, evidence, data, events, future states, or knowledge about the world "
          "that the model lacks or cannot access; SENTENCE if it concerns the statement itself: its wording, "
          "self-reference, logical form, vagueness of its terms, ambiguity, or the semantics of evaluating it. "
          "Answer with exactly one word: WORLD or SENTENCE.\n\nLimitation: {what}\nReason given: {why}")

def items():
    for src, path in SOURCES.items():
        for ri, row in enumerate(csv.DictReader(open(path))):
            if row["Status"] != "Success": continue
            try: L = json.loads(row["Losses_JSON"])
            except Exception: continue
            for ii, it in enumerate(L):
                what = (it.get("what") or "").strip()
                if not what: continue
                yield src, ri, ii, what, (it.get("why") or "").strip(), row["Phenomenon_Type"], row["Model"], row["Rep"], it.get("severity", 0)

def main():
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
    rows = list(items()); print(f"{len(rows)} loss items to classify", flush=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["source", "row", "item", "what", "why", "phenomenon", "model", "rep", "severity", "label", "raw"])
        for n, (src, ri, ii, what, why, ph, model, rep, sev) in enumerate(rows, 1):
            raw = ""
            for attempt in range(3):
                try:
                    r = client.chat.completions.create(model="openai/gpt-4o-mini", temperature=0, max_tokens=3,
                        messages=[{"role": "user", "content": PROMPT.format(what=what, why=why)}])
                    raw = (r.choices[0].message.content or "").strip(); break
                except Exception as e:
                    raw = f"ERR {e}"; time.sleep(2)
            u = raw.upper(); label = "WORLD" if u.startswith("WORLD") else ("SENTENCE" if u.startswith("SENTENCE") else "UNPARSED")
            w.writerow([src, ri, ii, what, why, ph, model, rep, sev, label, raw]); f.flush()
            if n % 50 == 0: print(f"  {n}/{len(rows)}", flush=True)
            time.sleep(0.2)
    print("done ->", OUT)

if __name__ == "__main__":
    main()
