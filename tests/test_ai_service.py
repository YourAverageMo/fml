import pytest
from abc import ABC, abstractmethod
from typing import List

from fml.ai_service import AIService


class ConcreteAIService(AIService):
    """A concrete implementation for testing purposes."""

    def __init__(self, api_key: str, system_instruction_path: str, model: str):
        super().__init__(api_key, system_instruction_path, model)

    def generate_command(self, query: str):
        return "mocked command"

    @staticmethod
    def get_supported_models() -> List[str]:
        return ["mock-model-1", "mock-model-2"]


def test_ai_service_is_abstract():
    """Verify that AIService is an abstract base class."""
    assert issubclass(AIService, ABC)
    with pytest.raises(TypeError, match="Can't instantiate abstract class AIService without an implementation for abstract methods 'generate_command', 'get_supported_models'"):
        AIService("key", "path", "model")


def test_ai_service_abstract_methods():
    """Verify that abstract methods are defined."""
    assert 'generate_command' in AIService.__abstractmethods__
    assert 'get_supported_models' in AIService.__abstractmethods__


def test_ai_service_initialization():
    """Verify that AIService initializes attributes correctly."""
    service = ConcreteAIService("test_api_key", "/path/to/prompt.txt", "test-model")
    assert service.api_key == "test_api_key"
    assert service.system_instruction_path == "/path/to/prompt.txt"
    assert service.model == "test-model"


def test_concrete_ai_service_implements_abstract_methods():
    """Verify that a concrete subclass can be instantiated and implements abstract methods."""
    service = ConcreteAIService("key", "path", "model")
    assert service.generate_command("test query") == "mocked command"
    assert service.get_supported_models() == ["mock-model-1", "mock-model-2"]
