"""
Lab 2 - Step 4: The Broken Agent
==================================
Your job: instrument this agent with the tracer, add loop detection, and fix it.
"""

import json
import time
import logging
from litellm import completion
from config import MODEL_NAME
from tools.mock_tools import TOOLS_DICT, TOOLS_SCHEMA
from agent.tracer import AgentTracer, AgentStep, ToolCallRecord
from agent.loop_detector import AdvancedLoopDetector
from routing.semantic_router import SemanticToolSelector

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

def run_agent(query: str, max_steps: int = 10) -> dict:
    """Standard agent loop. Needs instrumentation."""
    messages = [
        {"role": "system", "content": "You are a research assistant. Use tools to answer questions."},
        {"role": "user", "content": query},
    ]
    
    # TODO: Initialize tracer and loop detector (Step 4)
    # --- YOUR CODE HERE ---
    
    # Optional: Use SemanticToolSelector to filter tools for efficiency (Step 1)
    # selector = SemanticToolSelector()
    # tools_schema = selector.get_tool_schemas(query, top_k=5)
    
    # --- END YOUR CODE ---

    for step in range(max_steps):
        step_start = time.time()
        
        response = completion(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS_SCHEMA, # Or your filtered tools
            tool_choice="auto",
        )

        message = response.choices[0].message
        content = message.content
        tool_calls = message.tool_calls
        messages.append(message)

        if content: logger.info(f"[Step {step + 1}] {content[:100]}...")

        if tool_calls:
            for tc in tool_calls:
                fn_name = tc.function.name
                fn_args = json.loads(tc.function.arguments)
                args_str = json.dumps(fn_args)

                # TODO: Check for loops BEFORE executing (Step 4)
                # --- YOUR CODE HERE ---
                
                # Execute tool
                tool_start = time.time()
                result = TOOLS_DICT.get(fn_name, lambda **_: "Unknown tool")(**fn_args)
                tool_duration = (time.time() - tool_start) * 1000
                
                logger.info(f"[Step {step + 1}] Tool: {fn_name}({args_str}) -> {result[:50]}...")

                messages.append({"tool_call_id": tc.id, "role": "tool", "name": fn_name, "content": result})
                
                # --- END YOUR CODE ---

        # TODO: Log step to tracer (Step 4)
        
        if not tool_calls and content:
            # TODO: End trace and return
            return {"answer": content, "total_steps": step + 1}

    return {"answer": "[Max steps reached]", "total_steps": max_steps}

if __name__ == "__main__":
    print("Test 1: Normal Query")
    run_agent("What is the capital of France?")
    
    print("\nTest 2: Looping Query (BUG!)")
    run_agent("What are the latest trends in quantum computing?")
