from abc import ABC, abstractmethod
from google import genai
import os


class AIService(ABC):
    """
    Abstract base class for AI services.
    Defines the interface for generating CLI commands.
    """

    @abstractmethod
    def generate_command(self, query: str) -> str:
        """
        Generates a CLI command based on a natural language query.

        Args:
            query: The natural language query.

        Returns:
            A JSON string containing the generated command, explanation, and flags.
        """
        pass


class GeminiService(AIService):
    """
    Concrete implementation of AIService for Google Gemini.
    """

    def __init__(self, api_key: str, system_instruction_path: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-1.5-flash-latest'

        # Read system instruction from file
        with open(system_instruction_path, 'r') as f:
            self.system_instruction = f.read()

    def generate_command(self, query: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=query,
                config=genai.types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    response_mime_type='application/json',
                    response_schema={
                        "type": "object",
                        "properties": {
                            "explanation": {
                                "type": "string"
                            },
                            "flags": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "flag": {
                                            "type": "string"
                                        },
                                        "description": {
                                            "type": "string"
                                        }
                                    },
                                    "required": ["flag", "description"]
                                }
                            },
                            "command": {
                                "type": "string"
                            }
                        },
                        "required": ["explanation", "flags", "command"]
                    }))
            return response.text
        except genai.errors.APIError as e:
            return f"API Error: {e.message} (Code: {e.code})"
        except Exception as e:
            return f"An unexpected error occurred: {e}"
