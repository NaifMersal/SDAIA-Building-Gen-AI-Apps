# Student Project Evaluation Criteria: AI Agentic Systems

This rubric is designed to evaluate student projects building AI Agent systems. You need at least 80% to pass.

## 📊 Summary of Weighting

| Category | Weight | Key Focus |
| :--- | :---: | :--- |
| **1. Agent Architecture** | 50% | ReAct loop, tool integration, specialized agents (Multi-Agent, Plan-Execute). |
| **2. Observability & Reliability** | 40% | Tracing, loop detection, cost tracking, error handling. |
| **3. Evaluation Framework** | 5% | Metric implementation (DeepEval), testing against ground truth. |
| **4. Engineering Excellence** | 5% | Dependency management (`uv`), project structure, documentation. |


---

## 🔍 Detailed Rubric

### 1. Agent Architecture (50 Points + 15 Bonus Points)
*How well is the agent's logic and reasoning implemented?*

*   **Excellent (40-50):** Implements advanced patterns like Multi-Agent Orchestration (e.g., Researcher/Writer) or Plan-and-Execute. Tool calling is precise and handles complex inputs. (If the use case require complex pattren like research)
*   **Good (30-39):** Solid ReAct loop implementation. Uses a diverse set of tools correctly. Logic is clear but lacks complex orchestration.
*   **Satisfactory (20-29):** Basic ReAct loop. Limited tool set. Reasoning is often brittle or fails on edge cases.
*   **Poor (0-19):** Agent is a simple prompt wrapper. No iterative reasoning or tool usage.

*   **Bonus (0-15):** Implement a full RAG system.

### 2. Observability & Reliability (40 Points)
*Is the system transparent and "production-ready"?*

*   **Excellent (35-40):** Full structured tracing of every step. Implements advanced loop detection (e.g., repetition and stagnation). Real-time cost and token tracking per query.
*   **Good (25-34):** Basic logging of tool calls. Simple step-limiting loop prevention. Tracks total tokens.
*   **Satisfactory (15-24):** Minimal logging. No robust way to stop infinite loops or track costs.
*   **Poor (0-14):** System is a "black box". No visibility into the agent's internal state or tool execution.

### 3. Evaluation Framework (5 Points)
*How do we know the agent is actually performing well?*

*   **Excellent (4-5):** DeepEval integration (or similar) with multiple metrics (Relevancy, Recall, Precision). Automated evaluation runs against a diverse test dataset.
*   **Good (3):** Basic evaluation scripts. Uses at least one automated metric. Test cases cover happy paths.
*   **Satisfactory (2):** Manual evaluation only. No formal metrics or automated testing.
*   **Poor (0-1):** No evaluation strategy. Accuracy is assumed rather than measured.

### 4. Engineering Excellence (5 Points)
*Is the codebase maintainable and professionally structured?*

*   **Excellent (5):** Uses `uv` for lightning-fast dependency management. Modular code (concise `src` structure). Clean `README` with clear setup and usage instructions. deterministic doc IDs.
*   **Good (3-4):** Standard `pip`/`poetry` setup. Follows basic Python package structure. Decent documentation.
*   **Satisfactory (2):** Bloated files. Lacks modularity. High-level instructions are vague.
*   **Poor (0-1):** Chaotic structure. Hard-coded paths. No README or setup instructions.

