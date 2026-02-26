# Student Project Evaluation Criteria: AI Agentic Systems

This rubric is used to evaluate student projects building AI Agent systems.
**You need at least 80 points to pass.**

---

## Summary of Weighting

| Category | Points | Key Focus |
| :--- | :---: | :--- |
| **1. Agent Architecture** | 50 | ReAct loop, tool integration, specialized agents (Multi-Agent, Plan-Execute) |
| **2. Observability & Reliability** | 40 | Tracing, loop detection, cost tracking, error handling |
| **3. Engineering Excellence** | 10 | Dependency management, project structure, documentation |
| **Total** | **100** | |
| **Bonus** | +15 | Full RAG system integration |

---

## Detailed Rubric

### 1. Agent Architecture (50 Points + 15 Bonus)

*How well is the agent's logic and reasoning implemented?*

| Band | Points | Description |
| :--- | :---: | :--- |
| **Excellent** | 40–50 | Implements advanced patterns such as Multi-Agent Orchestration (e.g., Researcher → Analyst → Writer) or Plan-and-Execute. Tool calling is precise and handles complex inputs gracefully. |
| **Good** | 30–39 | Solid ReAct loop implementation. Uses a diverse set of tools correctly. Logic is clear but lacks complex orchestration. |
| **Satisfactory** | 20–29 | Basic ReAct loop. Limited tool set. Reasoning is often brittle or fails on edge cases. |
| **Poor** | 0–19 | Agent is a simple prompt wrapper. No iterative reasoning or tool usage. |

**Bonus (+15):** Implement a full RAG (Retrieval-Augmented Generation) system.

---

### 2. Observability & Reliability (40 Points)

*Is the system transparent and production-ready?*

| Band | Points | Description |
| :--- | :---: | :--- |
| **Excellent** | 35–40 | Full structured tracing of every step. Implements advanced loop detection (repetition and stagnation). Real-time cost and token tracking per query. |
| **Good** | 25–34 | Basic logging of tool calls. Simple step-limiting loop prevention. Tracks total tokens. |
| **Satisfactory** | 15–24 | Minimal logging. No robust mechanism to stop infinite loops or track costs. |
| **Poor** | 0–14 | System is a black box. No visibility into the agent's internal state or tool execution. |

---

### 3. Engineering Excellence (10 Points)

*Is the codebase maintainable and professionally structured?*

| Band | Points | Description |
| :--- | :---: | :--- |
| **Excellent** | 9–10 | Uses `uv` for dependency management. Modular `src` layout with clear separation of concerns. Clean `README` with setup and usage instructions. |
| **Good** | 6–8 | Standard `pip`/`poetry` setup. Follows basic Python package structure. Decent documentation. |
| **Satisfactory** | 3–5 | Bloated files. Lacks modularity. Setup instructions are vague. |
| **Poor** | 0–2 | Chaotic structure. Hard-coded paths. No README or setup instructions. |
