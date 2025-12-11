import json

with open("output/model_outputs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

results = data["results"]

EXPECTED_PROMPTS = set(range(1, 73))
MISSING = {}
EMPTY = {}
COUNT_BY_MODEL = {}

for model_name, model_data in results.items():
    print(f"\n=== Checking {model_name} ===")
    COUNT_BY_MODEL[model_name] = {}

    for l4_id, entries in model_data.items():
        # count prompts
        COUNT_BY_MODEL[model_name][l4_id] = len(entries)

        # collect prompt IDs
        prompt_ids = [e["prompt_id"] for e in entries]

        # missing prompts for this L4
        missing = EXPECTED_PROMPTS - set(prompt_ids)
        if missing:
            MISSING[(model_name, l4_id)] = missing

        # empty outputs
        empty_outputs = [e["prompt_id"] for e in entries if not e["output"].strip()]
        if empty_outputs:
            EMPTY[(model_name, l4_id)] = empty_outputs

print("\n\n=== SUMMARY ===")

print("\nPrompt count per model/L4:")
for model, l4_data in COUNT_BY_MODEL.items():
    print(f"\n{model}:")
    for l4, count in l4_data.items():
        print(f"  {l4}: {count}")

if not MISSING:
    print("\n✅ No missing prompts!")
else:
    print("\n❌ Missing prompts detected:")
    for k, v in MISSING.items():
        print(k, sorted(v))

if not EMPTY:
    print("\n✅ No empty outputs!")
else:
    print("\n❌ Empty outputs found:")
    for k, v in EMPTY.items():
        print(k, v)
