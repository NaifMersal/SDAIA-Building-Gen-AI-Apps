import json
import logging
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.observability.detectors import LoopDetector
from src.observability.observe import langfuse_context, observe, propagate_attributes
from src.tools.registry import registry

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
    detector = LoopDetector(exact_threshold=2, fuzzy_threshold=0.8)

    # Exact match detection — threshold=2 means 3rd identical call triggers it
    r1 = detector.check_tool_call("search", "python agents")
    assert not r1.is_looping
    r2 = detector.check_tool_call("search", "python agents")
    assert not r2.is_looping
    r3 = detector.check_tool_call("search", "python agents")
    assert r3.is_looping and r3.strategy == "exact"

    # Fuzzy match detection
    detector.reset()
    detector.check_tool_call("search", "python agents var 1")
    detector.check_tool_call("search", "python agents var 2")
    detector.check_tool_call("search", "python agents var 3")

    # Jaccard similarity sanity checks
    assert detector._jaccard_similarity("a b c", "a b c") == 1.0
    assert detector._jaccard_similarity("a b c", "x y z") == 0.0

    logger.info("Loop Detector Test Passed!")


def test_observe():
    logger.info("Testing @observe decorator...")

    @observe
    def greet(name: str) -> str:
        langfuse_context.update_current_observation(input=name, output=f"Hello, {name}!")
        return f"Hello, {name}!"

    result = greet("World")
    assert result == "Hello, World!"

    # Child span
    @observe("outer")
    def outer():
        @observe("inner")
        def inner():
            return 42
        return inner()

    assert outer() == 42
    logger.info("@observe Test Passed!")


def test_observe_langfuse_format():
    logger.info("Testing @observe langfuse format...")
    
    from src.observability.observe import _current_span

    captured_span = None

    @observe(name="mock_agent", as_type="agent")
    def mock_run(query: str):
        nonlocal captured_span
        langfuse_context.update_current_observation(
            input=query,
            model="gpt-4o",
        )

        @observe(name="search_tool", as_type="tool")
        def mock_tool():
            langfuse_context.update_current_observation(
                input={"tool": "search", "args": {"q": "test"}},
                output="Search results"
            )


        mock_tool()
        mock_tool()

        langfuse_context.update_current_observation(
            output="Final answer",
            usage={"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
            cost_usd=0.015
        )
        captured_span = _current_span.get()
        return "Final answer"

    result = mock_run("What is AI?")
    assert result == "Final answer"
    assert captured_span is not None
    assert captured_span.name == "mock_agent"
    assert captured_span.type == "agent"
    assert captured_span.model == "gpt-4o"
    assert captured_span.input == "What is AI?"
    assert captured_span.output == "Final answer"
    assert captured_span.usage["total_tokens"] == 30
    assert captured_span.metadata["cost_usd"] == 0.015

    assert len(captured_span.children) == 2
    child = captured_span.children[0]
    assert child.name == "search_tool"
    assert child.type == "tool"
    assert child.output == "Search results"

    logger.info("@observe langfuse format Test Passed!")
    
    # Test propagate_attributes (New v4 Pattern)
    logger.info("Testing propagate_attributes (v4 Pattern)...")
    @observe(name="parent")
    def parent_func():
        with propagate_attributes(user_id="user_v4", metadata={"v": "4"}):
            @observe(name="child")
            def child_func():
                return _current_span.get()
            return child_func()
    
    child_span = parent_func()
    assert child_span.metadata["user_id"] == "user_v4"
    assert child_span.metadata["v"] == "4"
    logger.info("propagate_attributes Test Passed!")


if __name__ == "__main__":
    test_registry()
    test_loop_detector()
    test_observe()
    test_observe_langfuse_format()
    print("\nAll checks passed!")
