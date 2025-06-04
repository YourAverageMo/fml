import pytest
from abc import ABC, abstractmethod
from typing import List

from fml.ai_service import AIService
from fml.schemas import AICommandResponse, AIContext, SystemInfo


class ConcreteAIService(AIService):
    """A concrete implementation for testing purposes."""

    def __init__(self, api_key: str, system_instruction_path: str, model: str):
        super().__init__(api_key, system_instruction_path, model)

    def _generate_command_internal(self, query: str, ai_context: AIContext) -> AICommandResponse:
        return AICommandResponse(
            explanation="mocked explanation",
            flags=[],
            command="mocked command"
        )



@pytest.fixture
def mock_ai_context():
    """Provides a mock AIContext object for testing."""
    return AIContext(
        query="test query",
        system_info=SystemInfo(
            os_name="test_os",
            shell="test_shell",
            cwd="/test/cwd",
            architecture="test_arch",
            python_version="test_python_version"
        )
    )


def test_ai_service_is_abstract():
    """Verify that AIService is an abstract base class."""
    assert issubclass(AIService, ABC)
    with pytest.raises(
            TypeError,
            match=
            "Can't instantiate abstract class AIService without an implementation for abstract method '_generate_command_internal'"
    ):
        AIService("key", "path", "model")


def test_ai_service_abstract_methods():
    """Verify that abstract methods are defined."""
    assert '_generate_command_internal' in AIService.__abstractmethods__


def test_ai_service_initialization():
    """Verify that AIService initializes attributes correctly."""
    service = ConcreteAIService("test_api_key", "test system instruction content",
                                "test-model")
    assert service.api_key == "test_api_key"
    assert service.system_instruction_content == "test system instruction content"
    assert service.model == "test-model"


def test_concrete_ai_service_implements_abstract_methods(mock_ai_context):
    """Verify that a concrete subclass can be instantiated and implements abstract methods."""
    service = ConcreteAIService("key", "path", "model")
    response = service.generate_command("test query", mock_ai_context)
    assert response.command == "mocked command"
