# Lab 2: Plugin System

**Module 02 — Function Calling & Tool Systems**

## Objectives

By the end of this lab you will be able to:

1. **Implement** the plugin pattern — convert standalone functions into `BaseTool` subclasses
2. **Build** a `ToolRegistry` that manages execution, rate limiting, and permissions
3. **Expose** your tool registry as an MCP server so any client can discover and use your tools

## What You're Building

```
BaseTool (abstract contract)
    ↓
CalculatorTool, ListFilesTool  (concrete tools)
    ↓
ToolRegistry  (central dispatch + security + rate limiting)
    ↓
FastMCP server  (standardized protocol exposure)
    ↓
MCP client (simple_agent.py — given demo)
```

## Setup

```bash
uv pip install -r requirements.txt
```

## Files

| File | Your Task |
|------|-----------|
| `base.py` | **Given** — read the contract carefully |
| `calculator_tool.py` | Implement `name`, `description`, `parameters`, `execute()` |
| `filesystem.py` | Implement `execute()` only |
| `security.py` | Implement `validate_safe_path()` |
| `manager.py` | Implement `is_allowed()` |
| `registry.py` | Implement `register()`, `get_schemas()`, `execute()`, `execute_secure()` |
| `server.py` | Add `@mcp.tool()` and `@mcp.resource()` decorators |
| `simple_agent.py` | **Given** — run it to test your server |

## Recommended Order

1. `calculator_tool.py` — implement and test with its `__main__` block
2. `security.py` + `manager.py` — test each independently
3. `filesystem.py` — test with its `__main__` block
4. `registry.py` — test with its `__main__` block (should exercise everything)
5. `server.py` — add the MCP decorators
6. Run `python simple_agent.py` in one terminal to test end-to-end

## Running the MCP Demo

The client (`simple_agent.py`) spawns `server.py` as a subprocess automatically:

```bash
# Just run the client — it starts the server for you
python simple_agent.py
```
