from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_name: str = Field(default="gpt-4o", description="The LLM model to use")
    max_steps: int = Field(default=10, description="Max steps for agent execution")
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="console", description="Logging format (json or console)")

    model_config = ConfigDict(env_file=".env", extra="ignore")


settings = Settings()
