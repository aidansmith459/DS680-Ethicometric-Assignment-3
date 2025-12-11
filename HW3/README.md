# Prompt Generation & Model Evaluation Pipeline

This repository contains a full pipeline for generating prompts, running model tests, evaluating outputs, normalizing metrics, and validating final results.
It is designed for experimentation, benchmarking, or dataset generation using LLMs.

---
## Citation / Attribution

The base code used in this repo was created by Peng Wang: https://github.com/ClAy140/DS680-BU-Fall2025/tree/main/HW3

If you use this code in your research, please acknowledge it in your paper (e.g., in the Appendix or Methods section) to ensure proper attribution. Example:

“This work uses the prompt generation and evaluation pipeline developed by <Peng Wang> (2025).”

## 🚀 **Features**

* **Automatic prompt generation** (`1generate_prompt.py`)
* **Prompt merging & preprocessing** (`2prompt.py`)
* **Model inference & output collection** (`3test.py`)
* **Scoring & evaluation** (`4evaluation.py`)
* **Statistical analysis utilities** (`analysis.py`)

* **Final output validation** (`validation.py`)

---

## 📦 **Project Structure**

```
repo
│
├── 1generate_prompt.py     # Generate prompt sets
├── 2prompt.py              # Merge & format prompts
├── 3test.py                # Run model inference
├── 4evaluation.py          # Score model outputs
├── analysis.py             # Aggregate & compute stats
├── norm.py                 # Normalize evaluation scores
├── validation.py           # Check empty/invalid outputs
└── output/                 # (Created during runtime)
```



---

## 🔑 **API Keys**

The scripts reference environment variables for model access.
Set them before running:

```bash
export OPENAI_API_KEY="your_key_here"
export HF_API_KEY="your_key_here"
```

Or on Windows:

```powershell
setx OPENAI_API_KEY "your_key_here"
setx HF_API_KEY "your_key_here"
```

> **Note:** The uploaded version contains empty placeholders, so keys are *not* included in the repo.

---

## 📘 **Usage Guide**

### **Step 1 — Generate Prompts**

```bash
python 1generate_prompt.py
```

Outputs files inside `output/prompts/`.

---

### **Step 2 — Merge & Format Prompts**

```bash
python 2prompt.py
```

Creates:

```
output/merged_prompts.json
```

---

### **Step 3 — Run Model Tests**

```bash
python 3test.py
```

This script sends prompts to the model and saves raw outputs to:

```
output/model_outputs.json
```

---

### **Step 4 — Evaluate the Model**

```bash
python 4evaluation.py
```

Produces:

```
output/evaluation_scores.json
```

---

### **Step 5 — Statistical Analysis**

```bash
python analysis.py
```

Generates aggregated results + summary stats.

---

Checks:

* missing outputs
* empty strings
* evaluation mismatches


---

## 📁 Output Directory

All generated artifacts are stored in:

```
output/
    prompts/
    merged_prompts.json
    model_outputs.json
    evaluation_scores.json
    norms.json         (or similar)
    validation_report.txt
```

---

## 🤝 Contributing

Feel free to submit issues or PRs for:

* new evaluation metrics
* additional normalization methods
* expanded prompt sets

---

## 📜 License

MIT License (optional — change if needed)

---
