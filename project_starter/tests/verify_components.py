import sys
import os
import json
import logging
from dataclasses import dataclass

# Add project_starter root to path so "from src.X import Y" works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tools.registry import registry, Tool
from src.observability.loop_detector import AdvancedLoopDetector
from src.observability.tracer import tracer, AgentStep, ToolCallRecord

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_registry():
    logger.info("Testing Registry...")

    @registry.register("test_tool", "A test tool")
    def my_tool(x: int, y: str = "default"):
        return f"{x}-{y}"

    tool = registry.get_tool("test_tool")
    assert tool is not None, "Tool not registered"

    schema = tool.to_openai_schema()
    print(json.dumps(schema, indent=2))

    assert schema["function"]["name"] == "test_tool"
    assert "x" in schema["function"]["parameters"]["properties"]
    assert "y" in schema["function"]["parameters"]["properties"]

    result = tool.execute(x=10, y="tested")
    assert result == "10-tested"
    logger.info("Registry Test Passed!")

def test_loop_detector():
    logger.info("Testing Loop Detector...")
    detector = AdvancedLoopDetector(exact_threshold=2, fuzzy_threshold=0.8)

    # Test Exact Match
    r1 = detector.check_tool_call("search", "python agents")
    assert not r1.is_looping
    r2 = detector.check_tool_call("search", "python agents")
    assert r2.is_looping and r2.strategy == "exact"

    # Test Fuzzy Match
    detector.reset()
    detector.check_tool_call("search", "python agents var 1")
    detector.check_tool_call("search", "python agents var 2") # Not looping yet (threshold 2)
    r3 = detector.check_tool_call("search", "python agents var 3") # Should trigger fuzzy

    # Verify Jaccard works (logic check)
    sim = detector._jaccard_similarity("a b c", "a b c")
    assert sim == 1.0
    sim = detector._jaccard_similarity("a b c", "x y z")
    assert sim == 0.0

    logger.info("Loop Detector Test Passed!")

def test_tracer():
    logger.info("Testing Tracer...")
    trace_id = tracer.start_trace("VerificationAgent", "Test Query")
    assert trace_id

    step = AgentStep(
        step_number=1,
        reasoning="Testing",
        tool_calls=[],
        duration_ms=100
    )
    tracer.log_step(trace_id, step)

    tracer.end_trace(trace_id, "Final Answer")

    trace_json = tracer.get_trace_json(trace_id)
    trace_data = json.loads(trace_json)

    assert trace_data["trace_id"] == trace_id
    assert trace_data["status"] == "completed"
    assert len(trace_data["steps"]) == 1

    logger.info("Tracer Test Passed!")

if __name__ == "__main__":
    test_registry()
    test_loop_detector()
    test_tracer()
