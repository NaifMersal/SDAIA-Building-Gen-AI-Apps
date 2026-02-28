# Lab 2: Routing & Resilience

In this lab, you will build an agent system that is both **efficient** and **resilient**. You will solve the problem of "tool overload" using semantic routing and the problem of "infinite loops" using observability and circuit breakers.

## 🎯 Learning Objectives
1. **Dynamic Tool Routing:** Select only the most relevant tools for a query to keep context windows lean.
2. **Observability (Tracing):** Instrument your agent to capture a detailed trace of reasoning and actions.
3. **Resilience (Loop Detection):** Implement a "circuit breaker" that detects repetitive behaviors and stops loops before they burn tokens.

---

## 🏗️ The Architecture
We are building a **Routed Agent** that follows this flow:
1. **Perception:** User query enters.
2. **Routing:** 
   - A cheap classifier routes to a domain (financial, academic, general).
   - An embedding-based selector finds the top-K most relevant tools.
3. **Execution:** The agent loop runs with ONLY the selected tools.
4. **Monitoring:** A Tracer logs every step.
5. **Circuit Breaker:** A Loop Detector checks for stagnation or repetition.

---

## 🛠️ Step-by-Step Instructions

### Step 1: Semantic Tool Selection
Open `routing/semantic_router.py`. Your task is to implement the embedding-based selection logic:
- Implement `cosine_similarity`.
- Implement `build_index` to embed all tool descriptions.
- Implement `select_tools` to find the best matches for a query.

### Step 2: Agent Tracing
Open `agent/tracer.py`. Implement the `AgentTracer` class to capture:
- Agent name, model, and status.
- Every step's reasoning, tool calls, and duration.
- Final summary of tokens and cost.

### Step 3: Loop Detection
Open `agent/loop_detector.py`. Implement three detection strategies:
- **Exact Match:** Same tool + same args repeated.
- **Fuzzy Match:** High Jaccard similarity between tool inputs.
- **Stagnation:** Agent produces nearly identical reasoning outputs N times in a row.

### Step 4: The Final Agent
Open `agent/broken_agent.py`. Wire everything together!
- Instrument the loop with your `AgentTracer`.
- Add a check to `AdvancedLoopDetector` before each tool call.
- If a loop is detected, inject a warning instead of executing the tool.

---

## 🚀 Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Configure your `.env`.
3. Start with `routing/semantic_router.py`.
