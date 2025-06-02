from abc import ABC, abstractmethod
from typing import List


class AIService(ABC):
    """
    Abstract base class for AI services.
    Defines the interface for generating CLI commands.
    """

    def __init__(self, api_key: str, system_instruction_path: str, model: str):
        self.api_key = api_key
        self.system_instruction_path = system_instruction_path
        self.model = model

    @abstractmethod
    def generate_command(self, query: str):
        """
        Generates a CLI command based on a natural language query.

        Args:
            query: The natural language query.

        Returns:
            An instance of AICommandResponse containing the generated command, explanation, and flags.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_supported_models() -> List[str]:
        """
        Returns a list of user-facing model names supported by this AI service.
        """
        pass
