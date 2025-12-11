import os
import json

# ============================================================
# 1. Load L4 definitions
# ============================================================
with open("l4_norms.json", "r", encoding="utf-8") as f:
    L4_NORMS = json.load(f)

PROMPT_DIR = "prompt"
OUTPUT_FILE = "prompts.json"

# ============================================================
# 2. Merge prompt files
# ============================================================
merged = {"prompts": []}
global_id = 1

for filename in sorted(os.listdir(PROMPT_DIR)):
    if not filename.endswith(".json"):
        continue

    path = os.path.join(PROMPT_DIR, filename)
    print(f"Loading {path}...")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    l4_id = data.get("l4_id")

    if l4_id not in L4_NORMS:
        raise ValueError(f"Error: l4_id '{l4_id}' in file {filename} is not found in l4_norms.json")

    for p in data["prompts"]:
        merged["prompts"].append({
            "prompt_id": global_id,
            "l4_id": l4_id,
            "full_prompt": p["full_prompt"].strip()
        })
        global_id += 1

print(f"\nMerged {global_id - 1} prompts from {PROMPT_DIR}/")

# ============================================================
# 3. Save merged file
# ============================================================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)

print(f"Saved merged prompts to {OUTPUT_FILE}")
