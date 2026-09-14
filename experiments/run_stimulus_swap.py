"""Stimulus-swap collection: S4 protocol, five models, five NEW statements, 5 reps.
Pre-registered in experiments/stimulus_swap_prereg.md. Writes data/s4_stimulus_swap.csv."""
from __future__ import annotations
import csv, os, sys, time
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from openai import OpenAI
from src.experiment import MODELS, run_single

SWAP = (
    {"type": "Paradox (Logical)", "phrase": "The next sentence is true. The previous sentence is false."},
    {"type": "Ignorance (Epistemic)", "phrase": "Julius Caesar had an even number of hairs on his head at the moment he died."},
    {"type": "Vagueness (Fuzzy)", "phrase": "Maria has 3,000 hairs on her head, therefore Maria is bald."},
    {"type": "Contradiction (Ethical)", "phrase": "Breaking a promise to prevent serious harm to a stranger is both morally required and morally forbidden."},
    {"type": "Contingency (Future)", "phrase": "The Frankfurt stock exchange will close higher next Monday than it closes this Friday."},
)
REPS, TEMP, OUT = 5, 0.7, Path("data/s4_stimulus_swap.csv")

def main():
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY not set")
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key,
                    default_headers={"HTTP-Referer": "https://github.com/fsgeek/neutrosophic-llm-logic",
                                     "X-Title": "Neutrosophic stimulus swap"})
    fields = ["Timestamp","Phenomenon_Type","Phrase_English","Provider","Model","Model_ID","Strategy","Rep",
              "T","I","F","Sum_TIF","Num_Losses","Mean_Severity","Losses_JSON","Temperature",
              "Prompt_Tokens","Completion_Tokens","Total_Tokens","Status","Raw_Response"]
    total = len(SWAP) * len(MODELS) * REPS; done = 0
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for ph in SWAP:
            for mid, info in MODELS.items():
                for rep in range(1, REPS + 1):
                    done += 1
                    print(f"[{done}/{total}] {info['short_name']} '{ph['phrase'][:30]}' rep={rep}", flush=True)
                    r = run_single(client, mid, 4, ph["phrase"], temperature=TEMP)
                    s = None if None in (r["T"], r["I"], r["F"]) else round(r["T"] + r["I"] + r["F"], 4)
                    w.writerow({"Timestamp": datetime.now(timezone.utc).isoformat(), "Phenomenon_Type": ph["type"],
                                "Phrase_English": ph["phrase"], "Provider": info["provider"], "Model": info["short_name"],
                                "Model_ID": mid, "Strategy": "S4", "Rep": rep, "T": r["T"], "I": r["I"], "F": r["F"],
                                "Sum_TIF": s, "Num_Losses": r.get("num_losses", ""), "Mean_Severity": r.get("mean_severity", ""),
                                "Losses_JSON": r.get("losses", ""), "Temperature": TEMP,
                                "Prompt_Tokens": r.get("prompt_tokens", ""), "Completion_Tokens": r.get("completion_tokens", ""),
                                "Total_Tokens": r.get("total_tokens", ""), "Status": r["status"], "Raw_Response": r.get("raw_response", "")})
                    f.flush(); time.sleep(0.5)
    print(f"Done: {done} calls -> {OUT}")

if __name__ == "__main__":
    main()
