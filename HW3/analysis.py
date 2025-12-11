import json
import numpy as np
from collections import defaultdict, Counter

# Load data
with open("score/evaluation_scores.json", "r", encoding="utf-8") as f:
    data = json.load(f)["scores"]

models = list(data.keys())
l4_categories = list(next(iter(data.values())).keys())

# ---------------------------------------------
# 1. Compute average score per model and per L4
# ---------------------------------------------
model_avg = {}
l4_avg = defaultdict(list)
heatmap = defaultdict(dict)

for model, l4_dict in data.items():
    scores_all = []
    for l4, entries in l4_dict.items():
        scores = [int(e["score"]) for e in entries]
        avg_l4 = np.mean(scores)
        heatmap[model][l4] = avg_l4

        scores_all.extend(scores)
        l4_avg[l4].extend(scores)

    model_avg[model] = np.mean(scores_all)

# ---------------------------------------------
# 2. Score distribution (1–5)
# ---------------------------------------------
score_dist = Counter()

for model, l4_dict in data.items():
    for l4, entries in l4_dict.items():
        for e in entries:
            score_dist[int(e["score"])] += 1

# ---------------------------------------------
# 3. Hardest prompts (lowest average across models)
# ---------------------------------------------
prompt_scores = defaultdict(list)

for model, l4_dict in data.items():
    for l4, entries in l4_dict.items():
        for e in entries:
            pid = e["prompt_id"]
            prompt_scores[pid].append(int(e["score"]))

hardest_prompts = sorted(
    prompt_scores.items(),
    key=lambda kv: np.mean(kv[1])
)[:10]  # 10 lowest mean-score prompts

# Aidan's Scoring
#Every models score within each L4 category is the average of it's lowest 5 scores
# Risk is not communicated by it sometimes turning out to be correct, but by it ALWAYS
# avoiding bad behavior

final_scores = {}

for model, l4_dict in data.items():
    final_scores[model] = {}
    for l4, entries in l4_dict.items():
        scores = sorted([int(e["score"]) for e in entries])
        final_scores[model][l4] = np.mean(scores[:5])  # average of lowest 5 scores


# ---------------------------------------------
# 4. Printout
# ---------------------------------------------
print("\n========================")
print("AVERAGE SCORE PER MODEL")
print("========================")
for model, avg in model_avg.items():
    print(f"{model:20s} → {avg:.2f}")

print("\n=======================")
print("AVERAGE SCORE PER L4")
print("=======================")
for l4, scores in l4_avg.items():
    print(f"{l4:35s} → {np.mean(scores):.2f}")

print("\n==============================================")
print("MODEL × L4 HEATMAP (higher = more aligned)")
print("==============================================")
for model in models:
    print(f"\n▶ {model}")
    for l4 in l4_categories:
        print(f"  {l4:35s} : {heatmap[model][l4]:.2f}")

print("\n===========================")
print("SCORE DISTRIBUTION (1–5)")
print("===========================")
for s in range(1, 6):
    print(f"Score {s}: {score_dist[s]} samples")

print("\n=================================")
print("HARDEST PROMPTS (lowest mean score)")
print("=================================")
for prompt_id, scores in hardest_prompts:
    print(f"Prompt {prompt_id}: mean={np.mean(scores):.2f}, scores={scores}")




print("\n===========================")
print("FINAL SCORES (Aidan's method)")
print("===========================")
for model, l4_dict in final_scores.items():
    print(f"\n▶ {model}")
    for l4, avg in l4_dict.items():
        print(f"  {l4:35s} : {avg:.2f}")


print("\n============================")
print("Aidan's method, scaled output")
print("============================")
for model, l4_dict in final_scores.items():
    # scale final_scores from 0.0-1.0 instead of 1.0-5.0
    scaled = {l4: (score - 1) / 4 for l4, score in l4_dict.items()}
    overall = np.mean(list(scaled.values()))
    print(f"\n▶ {model} (overall avg: {overall:.2f})")
    for l4, avg in scaled.items():
        print(f"  {l4:35s} : {avg:.2f}")
