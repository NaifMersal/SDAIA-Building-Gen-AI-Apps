# Lab 04: Routing & Semantic Agents

## Overview

Build intelligent routing systems that select the right tools for each query. You'll implement two approaches: a **classifier-based router** that categorizes queries into domains, and a **semantic router** that uses embeddings for dynamic tool matching.

## Learning Goals

1. Build a `ClassifierRouter` using a small LLM to categorize queries
2. Implement a `SemanticToolSelector` using embeddings and cosine similarity
3. Create a `RoutedAgent` that filters tools before execution
4. Compare context window usage between standard and routed agents

## Prerequisites

- `uv pip install -r requirements.txt`
- A valid API key in `.env` (e.g., `OPENAI_API_KEY=sk-...`)

## Files

```
routing/
  router.py              # Classifier-based routing (provided)
  semantic_router.py     # TODO: Build the SemanticToolSelector

agent/
  routed_agent.py        # Classifier-routed agent (provided)
  semantic_agent.py      # TODO: Build the SemanticAgent

tools/
  registry.py            # Tool registry (provided)

starter/
  semantic_router.py     # TODO template
  semantic_agent.py      # TODO template

solutions/
  semantic_router.py     # Complete SemanticToolSelector
  semantic_agent.py      # Complete SemanticAgent
```

## Steps

### Step 1: Explore the Classifier Router (`routing/router.py`)

Run the existing classifier router to understand how it works:

```bash
python -c "from routing.router import ToolRouter; r = ToolRouter(); print(r.route('What is Apple stock price?'))"
```

The classifier:
- Uses GPT-4o-mini for fast, cheap classification
- Maps queries to domains: financial, academic, general
- Returns filtered tool sets

### Step 2: Build the Semantic Router (`starter/semantic_router.py`)

Implement `SemanticToolSelector` with:
- `build_index()` — embed all tool descriptions at startup
- `select_tools(query, top_k)` — return top-K most relevant tools
- `get_tool_schemas(query, top_k)` — return OpenAI-format schemas

Key concepts:
- Use `text-embedding-3-small` for embeddings
- Compute cosine similarity between query and tool embeddings
- Return tools sorted by relevance score

### Step 3: Build the Semantic Agent (`starter/semantic_agent.py`)

Implement `SemanticAgent` that:
- Calls `select_tools()` before each query
- Passes only the top-K tools to the agent loop
- Logs which tools were selected (for debugging)

### Step 4: Compare Approaches

Test both routing methods:

```bash
# Classifier routing
python -c "from agent.routed_agent import RoutedAgent; a = RoutedAgent(); print(a.run('What is Apple stock price?'))"

# Semantic routing (your implementation)
python -c "from agent.semantic_agent import SemanticAgent; a = SemanticAgent(); print(a.run('What is Apple stock price?'))"
```

Compare:
- Tools selected for each query
- Context window size (tokens in tools schema)
- Latency (classifier call vs embedding call)

## Time

75 minutes

## Reference

The `solutions/` directory contains complete implementations. Compare your work after completing the TODO sections.

## Quick Reference: Cosine Similarity

Formula: similarity = (A · B) / (‖A‖ · ‖B‖)

Ranges from 0.0 (unrelated) to 1.0 (identical meaning).
For the implementation, see the TODO in `starter/semantic_router.py`.

## Quick Reference: LiteLLM Embeddings

```python
from litellm import embedding

response = embedding(model="text-embedding-3-small", input=["your text here"])
vector = response.data[0]["embedding"]  # List of floats
```
