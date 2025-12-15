"""Base class for all skill agents with LLM integration."""

from abc import ABC, abstractmethod
from typing import Dict
import os

from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI


class BaseSkillAgent(ABC):
    """Abstract base class for all skill agents.

    Provides shared Gemini model configuration via OpenAI-Agents-SDK.
    All sub-agents must inherit and define name, description, instructions.
    """

    name: str = "base"
    description: str = "Base skill agent"
    instructions: str = "You are a helpful assistant."

    def __init__(self):
        """Initialize the agent with Gemini model via OpenAI-compatible API."""
        self.provider = AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url=os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
        )
        self.model = OpenAIChatCompletionsModel(
            model="gemini-2.5-flash",
            openai_client=self.provider
        )
        self.agent = Agent(
            name=self.name,
            instructions=self.instructions,
            model=self.model
        )

    def run(self, query: str) -> Dict[str, str]:
        """Execute the agent's skill with LLM.

        Args:
            query: The user's input query

        Returns:
            Dict with 'response' key containing the generated output.

        Raises:
            ValueError: If query is empty.
        """
        query = self.validate_input(query, "query")
        result = Runner.run_sync(self.agent, input=query)
        return {"response": result.final_output}

    def validate_input(self, value: str, field_name: str) -> str:
        """Validate and sanitize input.

        - Strips whitespace
        - Raises ValueError if empty
        - Truncates to 2000 chars with notice

        Args:
            value: The input value to validate
            field_name: Name of the field for error messages

        Returns:
            Sanitized input string

        Raises:
            ValueError: If input is empty or None
        """
        if not value or not value.strip():
            raise ValueError(f"{field_name} cannot be empty")

        value = value.strip()
        if len(value) > 2000:
            value = value[:2000] + "... [truncated]"

        return value
