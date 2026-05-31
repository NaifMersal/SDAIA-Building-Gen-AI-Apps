"""
Simple observability layer that mirrors the Langfuse v4 decorator API.

Usage (identical to production Langfuse):
    from src.observability.observe import observe, propagate_attributes

    @observe
    async def run(self, query):
        with propagate_attributes(metadata={"env": "dev"}):
            ...

Swapping to real Langfuse later requires only changing the import:
    from langfuse import observe, propagate_attributes
"""

import asyncio
import functools
import time
import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class Span:
    id: str
    name: str
    start_time: float
    level: int
    type: str = "span"
    parent: Optional["Span"] = None
    children: List["Span"] = field(default_factory=list)
    end_time: Optional[float] = None
    input: Any = None
    output: Any = None
    metadata: dict = field(default_factory=dict)
    usage: dict = field(default_factory=dict)
    model: Optional[str] = None


_current_span: ContextVar[Optional[Span]] = ContextVar("current_span", default=None)
_propagated_attrs: ContextVar[dict] = ContextVar("propagated_attrs", default={})


class SimpleObserver:
    @staticmethod
    def print_tree(span: Span):
        duration = (span.end_time - span.start_time) * 1000
        indent = "  " * span.level

        if span.level == 0:
            prefix, suffix = "=== TRACE: ", " ==="
        else:
            prefix, suffix = "|-- ", ""

        meta_parts = []
        # Show model if present
        if span.model:
            meta_parts.append(f"model={span.model}")

        # Usage tracking
        if span.usage:
            u = span.usage
            # Support both flat and nested usage dicts
            in_t = u.get("input_tokens") or u.get("input", 0)
            out_t = u.get("output_tokens") or u.get("output", 0)
            if in_t or out_t:
                meta_parts.append(f"tokens={in_t}+{out_t}")

        # Cost and other metadata
        if "cost_usd" in span.metadata:
            meta_parts.append(f"${span.metadata['cost_usd']:.4f}")
        elif "cost" in span.metadata:
            meta_parts.append(f"${span.metadata['cost']:.4f}")

        meta_str = f" [{', '.join(meta_parts)}]" if meta_parts else ""

        # Include type in the display if it's not a generic span
        type_str = f" [{span.type}]" if span.type != "span" else ""
        print(f"{indent}{prefix}{span.name}{type_str}{suffix} ({duration:.2f}ms){meta_str}")
        
        for child in span.children:
            SimpleObserver.print_tree(child)


def _make_span(span_name: str, span_type: str, func, args, kwargs) -> Span:
    parent = _current_span.get()
    level = parent.level + 1 if parent else 0
    captured_args = (
        args[1:]
        if args and hasattr(args[0], "__class__") and func.__name__ in dir(args[0].__class__)
        else args
    )
    span = Span(
        id=str(uuid.uuid4())[:8],
        name=span_name,
        type=span_type,
        start_time=time.time(),
        level=level,
        parent=parent,
        input={"args": captured_args, "kwargs": kwargs},
    )
    # Inherit propagated attributes
    span.metadata.update(_propagated_attrs.get())
    
    if parent:
        parent.children.append(span)
    return span


def _finish_span(span: Span):
    span.end_time = time.time()
    if span.level == 0:
        print("\n" + "-" * 60)
        SimpleObserver.print_tree(span)
        print("-" * 60 + "\n")


def observe(name=None, as_type=None, type=None):
    def decorator(func):
        span_name = name if isinstance(name, str) else func.__name__
        # Support both 'as_type' (Langfuse) and 'type' (DeepEval)
        span_type = as_type or type or "span"

        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                span = _make_span(span_name, span_type, func, args, kwargs)
                token = _current_span.set(span)
                try:
                    result = await func(*args, **kwargs)
                    if span.output is None:
                        span.output = result
                    return result
                except Exception as e:
                    span.output = f"Error: {e}"
                    raise
                finally:
                    _finish_span(span)
                    _current_span.reset(token)
        else:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                span = _make_span(span_name, span_type, func, args, kwargs)
                token = _current_span.set(span)
                try:
                    result = func(*args, **kwargs)
                    if span.output is None:
                        span.output = result
                    return result
                except Exception as e:
                    span.output = f"Error: {e}"
                    raise
                finally:
                    _finish_span(span)
                    _current_span.reset(token)

        return wrapper

    # Support both @observe and @observe() and @observe(name="foo", type="bar")
    if callable(name):
        f = name
        name = None
        return decorator(f)
    return decorator


@contextmanager
def propagate_attributes(user_id=None, session_id=None, metadata=None, tags=None):
    """
    Stub for Langfuse v4 propagate_attributes.
    Sets attributes for the current span and all child spans created within the context.
    """
    new_attrs = _propagated_attrs.get().copy()
    if user_id: new_attrs["user_id"] = user_id
    if session_id: new_attrs["session_id"] = session_id
    if tags: new_attrs["tags"] = tags
    if metadata: new_attrs.update(metadata)
    
    token = _propagated_attrs.set(new_attrs)
    
    # Also update current span if it exists
    span = _current_span.get()
    if span:
        span.metadata.update(new_attrs)
        
    try:
        yield
    finally:
        _propagated_attrs.reset(token)


class LangfuseContext:
    """
    Legacy wrapper for backward compatibility with v2/v3 patterns.
    New code should use propagate_attributes.
    """

    def update_current_observation(self, **kwargs):
        span = _current_span.get()
        if not span:
            return
        
        # Extract special fields
        if "input" in kwargs:
            span.input = kwargs.pop("input")
        if "output" in kwargs:
            span.output = kwargs.pop("output")
        if "usage" in kwargs:
            new_usage = kwargs.pop("usage")
            if isinstance(new_usage, dict):
                if not isinstance(span.usage, dict):
                    span.usage = {}
                span.usage.update(new_usage)
            else:
                span.usage = new_usage
        if "model" in kwargs:
            span.model = kwargs.pop("model")
            
        # Everything else goes to metadata
        span.metadata.update(kwargs)


langfuse_context = LangfuseContext()
