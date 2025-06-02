from abc import ABC, abstractmethod


class AIService(ABC):
    """
    Abstract base class for AI services.
    Defines the interface for generating CLI commands.
    """

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
