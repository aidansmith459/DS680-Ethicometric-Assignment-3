import os
HF_API_KEY = os.environ.get("HF_API_KEY", "YOUR_API_KEY_HERE")

import json
import time
from datetime import datetime
from tqdm import tqdm
from openai import OpenAI

# ----------------------------------------
# API Client (Hugging Face router)
# ----------------------------------------

hf_client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=HF_API_KEY)

MODELS = {
    "kimi_k2": {"client": hf_client, "model": "moonshotai/Kimi-K2-Instruct", "is_openai": False},
    "deepseek_v3_2": {"client": hf_client, "model": "deepseek-ai/DeepSeek-V3.2", "is_openai": False},
    "llama_3_1_8b": {"client": hf_client, "model": "meta-llama/Llama-3.1-8B-Instruct", "is_openai": False}
}

# ----------------------------------------
# Load prompts.json
# ----------------------------------------
with open("prompts.json", "r", encoding="utf-8") as f:
    PROMPTS = json.load(f)["prompts"]

print(f"Loaded {len(PROMPTS)} prompts.\n")

# ----------------------------------------
# Output structure (nested)
# ----------------------------------------
OUTPUT_FILE = "output/model_outputs.json"
ERROR_FILE = "output/errors.log"

# If output exists, resume
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        output_data = json.load(f)
else:
    output_data = {"results": {}}

# ----------------------------------------
# Run experiments
# ----------------------------------------
for model_name, info in tqdm(MODELS.items(), desc="Models", unit="model"):

    # Ensure model layer exists
    if model_name not in output_data["results"]:
        output_data["results"][model_name] = {}

    client = info["client"]
    model_id = info["model"]
    is_openai = info["is_openai"]

    for prompt_item in tqdm(PROMPTS, desc=f"{model_name} prompts", leave=False):

        prompt_id = prompt_item["prompt_id"]
        l4_id = prompt_item["l4_id"]
        full_prompt = prompt_item["full_prompt"]

        # Create L4 subfolder if missing
        if l4_id not in output_data["results"][model_name]:
            output_data["results"][model_name][l4_id] = []

        # Skip if already done
        already_done = any(p["prompt_id"] == prompt_id 
                           for p in output_data["results"][model_name][l4_id])
        #if already_done:
        #    continue

        try:
            # Model call
            if is_openai:
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[{"role": "user", "content": full_prompt}],
                    max_completion_tokens=200
                )
            else:
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[{"role": "user", "content": full_prompt}],
                    max_tokens=200
                )

            output_text = response.choices[0].message.content or ""

            # Save nested result
            # Save nested result (more complete structure)
            output_data["results"][model_name][l4_id].append({
                "model": model_name,
                "model_id": model_id,
                "prompt_id": prompt_id,
                "l4_id": l4_id,
                "full_prompt": full_prompt,
                "output": output_text,
                "timestamp": datetime.now().isoformat()
            })


            # Save continuously
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            with open(ERROR_FILE, "a", encoding="utf-8") as ef:
                ef.write(f"{datetime.now()} | {model_name} | prompt {prompt_id} | {e}\n")

        time.sleep(0.2)  # avoid rate limits

print("\n✔ DONE — Nested results saved to model_outputs.json\n")
