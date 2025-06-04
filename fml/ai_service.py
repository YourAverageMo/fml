from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import ValidationError
from requests.exceptions import ConnectionError
from fml.schemas import AICommandResponse, AIContext


class AIServiceError(Exception):
    """Custom exception for AI service-related errors."""

    pass


class AIService(ABC):
    """
    Abstract base class for AI services.
    Defines the interface for generating CLI commands.
    """

    def __init__(self, api_key: str, system_instruction_content: str, model: str):
        self.api_key = api_key
        self.system_instruction_content = system_instruction_content
        self.model = model

    @abstractmethod
    def _generate_command_internal(
        self, query: str, ai_context: AIContext
    ) -> AICommandResponse:
        """
        Internal method to generate a CLI command based on a natural language query.
        Concrete implementations should implement their specific API calls here.

        Args:
            query: The natural language query.
            ai_context: An AIContext object containing additional context for the AI.

        Returns:
            An instance of AICommandResponse containing the generated command, explanation, and flags.
        """
        pass

    def generate_command(self, query: str, ai_context: AIContext) -> AICommandResponse:
        """
        Generates a CLI command based on a natural language query, with common error handling.

        Args:
            query: The natural language query.
            ai_context: An AIContext object containing additional context for the AI.

        Returns:
            An instance of AICommandResponse containing the generated command, explanation, and flags.
        """
        try:
            return self._generate_command_internal(query, ai_context)
        except ConnectionError as e:
            # Catch network-related errors
            raise AIServiceError(
                f"Network Error: Could not connect to the AI service. Please check your internet connection. Details: {e}"
            ) from e
        except ValidationError as e:
            # Catch Pydantic validation errors if AI response is malformed
            raise AIServiceError(
                f"AI Response Format Error: The AI returned an unexpected response format. Details: {e}"
            ) from e
        except Exception as e:
            # Catch any other unexpected errors
            raise AIServiceError(
                f"An unexpected error occurred during AI interaction: {e}"
            ) from e
