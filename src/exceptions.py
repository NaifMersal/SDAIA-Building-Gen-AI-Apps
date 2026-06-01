class ProjectError(Exception):
    """Base exception for the project."""
    pass

class ConfigurationError(ProjectError):
    """Raised when there is a configuration error."""
    pass

class AgentError(ProjectError):
    """Base exception for agent-related errors."""
    pass

class AgentExecutionError(AgentError):
    """Raised when an agent fails to execute a task."""
    pass

class ToolError(AgentError):
    """Raised when a tool execution fails."""
    pass

class MaxStepsError(AgentError):
    """Raised when an agent exceeds the maximum number of steps."""
    pass

class TokenBudgetExceeded(AgentError):
    """Raised when the agent exceeds its token budget."""
    pass
