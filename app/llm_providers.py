"""LLM provider implementations for OpenAI, Anthropic, and DeepSeek."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx
from openai import OpenAI
from anthropic import Anthropic
from app.config import settings


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def generate_completion(self, prompt: str, system_prompt: Optional[str] = None,
                                 temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Generate a completion from the LLM."""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the name of the provider."""
        pass


class DeepSeekProvider(LLMProvider):
    """DeepSeek LLM provider implementation."""

    def __init__(self, api_key: str, api_base: str, model: str):
        self.api_key = api_key
        self.api_base = api_base
        self.model = model
        self.client = OpenAI(
            api_key=api_key,
            base_url=api_base
        )

    async def generate_completion(self, prompt: str, system_prompt: Optional[str] = None,
                                 temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Generate completion using DeepSeek API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"DeepSeek API error: {str(e)}")

    def get_provider_name(self) -> str:
        return "DeepSeek"


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)

    async def generate_completion(self, prompt: str, system_prompt: Optional[str] = None,
                                 temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Generate completion using OpenAI API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def get_provider_name(self) -> str:
        return "OpenAI"


class AnthropicProvider(LLMProvider):
    """Anthropic LLM provider implementation."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = Anthropic(api_key=api_key)

    async def generate_completion(self, prompt: str, system_prompt: Optional[str] = None,
                                 temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Generate completion using Anthropic API."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt if system_prompt else "",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")

    def get_provider_name(self) -> str:
        return "Anthropic"


class LLMFactory:
    """Factory class to create LLM provider instances."""

    @staticmethod
    def create_provider(provider_name: str) -> LLMProvider:
        """Create and return an LLM provider instance."""
        provider_name = provider_name.lower()

        if provider_name == "deepseek":
            if not settings.deepseek_api_key:
                raise ValueError("DeepSeek API key not configured")
            return DeepSeekProvider(
                api_key=settings.deepseek_api_key,
                api_base=settings.deepseek_api_base,
                model=settings.deepseek_model
            )

        elif provider_name == "openai":
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            return OpenAIProvider(
                api_key=settings.openai_api_key,
                model=settings.openai_model
            )

        elif provider_name == "anthropic":
            if not settings.anthropic_api_key:
                raise ValueError("Anthropic API key not configured")
            return AnthropicProvider(
                api_key=settings.anthropic_api_key,
                model=settings.anthropic_model
            )

        else:
            raise ValueError(f"Unknown LLM provider: {provider_name}")

    @staticmethod
    def get_available_providers() -> Dict[str, bool]:
        """Return a dictionary of available providers and their status."""
        return {
            "deepseek": bool(settings.deepseek_api_key),
            "openai": bool(settings.openai_api_key),
            "anthropic": bool(settings.anthropic_api_key)
        }
