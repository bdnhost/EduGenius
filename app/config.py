"""Configuration management for EduGenius application."""
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # LLM API Keys
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    deepseek_api_key: str = ""

    # Default LLM Provider
    default_llm_provider: Literal["openai", "anthropic", "deepseek"] = "deepseek"

    # DeepSeek Configuration
    deepseek_api_base: str = "https://api.deepseek.com/v1"
    deepseek_model: str = "deepseek-chat"

    # OpenAI Configuration
    openai_model: str = "gpt-4o-mini"

    # Anthropic Configuration
    anthropic_model: str = "claude-3-5-sonnet-20241022"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
