# Lab 1: The Plan-and-Execute Newsroom

Welcome to your first lab on AI Agents! You will implement a **Plan-and-Execute** agent that produces high-quality research reports — without any hardcoded pipeline.

## Core Concept: Plan-and-Execute

Traditional multi-agent systems hardcode a fixed sequence of steps (research → analyze → write). The **Plan-and-Execute** pattern separates two concerns:

1. **Plan:** Ask the LLM to decompose the query into an ordered list of sub-tasks, each assigned to a specialist.
2. **Execute:** Run each sub-task in order, feeding dependency results as context into the next step.

This means the agent decides *which* specialists to call and *in what order* — the orchestrator just drives the loop.

```
Query → Planner → [Step 1, Step 2, Step 3, ...] → Execute each → Synthesize
```

---

## Project: The Newsroom

You will build a newsroom agent with three specialists:

1. **Researcher** — Finds raw information and cites sources.
2. **Analyst** — Cross-references findings, rates confidence, flags gaps.
3. **Writer** — Synthesizes analysis into a polished executive briefing.

### Learning Objectives
- Write focused **system prompts** that constrain agent behaviour.
- Model a plan as **structured output** using Pydantic (`PlanStep`, `Plan`).
- Implement the **execute loop**: dispatch each step to the right specialist and pass dependency context forward.
- Understand why a **SharedWorkspace is no longer needed** — a plain `dict` of step results is sufficient.

---

## Step-by-Step Instructions

### Step 1: Specialist Prompts (`specialists.py`)
Fill in `SPECIALIST_PROMPTS` for each of the three specialists and implement `call_specialist()`.
**Key constraint:** each specialist should refuse to do work outside its role.

### Step 2: The Planner (`orchestrator.py`)
Write `PLANNER_PROMPT` — it must tell the LLM to output steps with `step`, `task`, `specialist`, and `depends_on` fields.
Then implement `TaskPlanner.create_plan()` to call the LLM with `response_format=Plan` and return a list of step dicts.

### Step 3: The Execute Loop (`orchestrator.py`)
Inside `NewsroomAgent.run()`:
- Call `_get_context()` to retrieve dependency results.
- Append context to the task string and call `call_specialist()`.
- Store each result in `results[step_num]`.

### Step 4: Synthesize (`orchestrator.py`)
Implement `_synthesize()` — format all step results and call the LLM to produce the final cited report.

---

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Configure your `.env` file with `MODEL_NAME` and your API key.
3. Start with `specialists.py`, then open `orchestrator.py`.
4. Run: `python orchestrator.py`
