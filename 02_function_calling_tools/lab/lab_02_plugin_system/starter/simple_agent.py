"""
MCP Client Demo — Connect to the MCP Server
=============================================
This file is given — read it to understand how an MCP client works.

Run this in a second terminal while server.py is NOT running.
The client spawns server.py as a subprocess automatically.

Usage:
    Terminal 1: (nothing — the client starts the server)
    Terminal 2: python simple_agent.py
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run_agent():
    """Connect to the MCP server and interact with tools."""

    # Define how to spawn the server as a subprocess
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Initialize the MCP connection
            await session.initialize()

            # Discover available tools
            tools = await session.list_tools()
            print(f"Connected! Server exposes {len(tools.tools)} tool(s):")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Call the calculate tool
            print("\nExecuting 'calculate': 10 + 5")
            result = await session.call_tool(
                "calculate",
                arguments={"operation": "add", "operand_a": 10, "operand_b": 5}
            )
            print(f"Result: {result.content[0].text}")

            # Another calculation
            print("\nExecuting 'calculate': 500 * 0.15")
            result2 = await session.call_tool(
                "calculate",
                arguments={"operation": "multiply", "operand_a": 500, "operand_b": 0.15}
            )
            print(f"Result: {result2.content[0].text}")

            # List files
            print("\nExecuting 'list_files': '.'")
            result3 = await session.call_tool("list_files", arguments={"path": "."})
            print(f"Result: {result3.content[0].text}")


if __name__ == "__main__":
    asyncio.run(run_agent())
