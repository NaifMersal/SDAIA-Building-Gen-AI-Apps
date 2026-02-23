# Homework: The Great Model Bake-off

## Objective
Use your `HuggingFaceClient` (from Lab 2) to send the **same 3 prompts** to **3 different models**, then compare their responses on quality and latency.

## Instructions

### 1. Choose Your Models
Pick 3 models from Hugging Face (suggested defaults in the template):

| Model | Type | Why |
|-------|------|-----|
| `mistralai/Mistral-7B-Instruct-v0.3` | Instruction-tuned | Strong general-purpose |
| `HuggingFaceH4/zephyr-7b-beta` | Chat-optimized | Fine-tuned for dialogue |
| `google/flan-t5-large` | Instruction-tuned | Smaller, different architecture |

### 2. Choose Your Prompts
Design 3 prompts that test different capabilities:

1. **Factual question** — e.g., "Explain the difference between TCP and UDP in 3 sentences."
2. **Creative task** — e.g., "Write a short poem about machine learning."
3. **Reasoning task** — e.g., "A company has 100 employees. 60% use Python, 40% use Java, and 20% use both. How many use at least one?"

### 3. Run the Bake-off
```bash
cd 01_architecture_fundamentals/homework
uv pip install requests python-dotenv
python bakeoff_template.py
```

### 4. Write Your Report
Fill in `report_template.md` with:
- Results table (quality rating 1-5, latency)
- Analysis of which model performed best and why
- Lessons learned about model selection

## Deliverables
1. Completed `bakeoff_template.py` with your prompts and ratings
2. Completed `report_template.md` with analysis

## Grading Rubric
| Criteria | Points |
|----------|--------|
| All 3 prompts tested on all 3 models | 30 |
| Quality ratings with justification | 25 |
| Latency measurements recorded | 15 |
| Thoughtful analysis in report | 20 |
| Code runs without errors | 10 |
