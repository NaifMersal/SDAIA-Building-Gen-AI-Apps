"""
MCP Server — Expose Tools via Model Context Protocol
=====================================================
Wrap the ToolRegistry in a FastMCP server so any MCP-compliant
client can discover and use your tools.

Prerequisites: Copy your completed Lab 2 files into this directory,
or use them directly if they're in the same folder.

Steps:
  1. Registry is initialized for you (see below)
  2. TODO: Add @mcp.tool() for the calculate function
  3. TODO: Add @mcp.tool() for list_files
  4. TODO: Add @mcp.resource() for system logs
"""

from mcp.server.fastmcp import FastMCP

from base import BaseTool
from calculator_tool import CalculatorTool
from filesystem import ListFilesTool
from registry import ToolRegistry

# Step 1: Initialize the Registry (given)
registry = ToolRegistry()
registry.register(CalculatorTool())
registry.register(ListFilesTool())

# Step 2: Create the MCP Server (given)
mcp = FastMCP("Research Assistant Tools")


# TODO: Step 3 — expose the calculate tool via MCP
# @mcp.tool()
# def calculate(...) -> dict:
#     """..."""
#     ...


# TODO: Step 4 — expose list_files via MCP
# @mcp.tool()
# def list_files(...) -> dict:
#     ...


# TODO: Step 5 — add a resource for system logs
# Decorator: @mcp.resource("system://logs/recent")
# Read last 10 lines from "app.log", return "No logs available." if missing


if __name__ == "__main__":
    mcp.run()
