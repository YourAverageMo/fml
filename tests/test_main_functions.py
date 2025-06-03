import pytest
import os
from unittest.mock import patch, MagicMock
from fml.__main__ import _initialize_ai_service
from fml.ai_providers.gemini_service import GeminiService, GeminiModels
from fml.ai_service import AIService

@pytest.fixture
def mock_gemini_service_class():
    """
    Fixture to mock the GeminiService class.
    """
    with patch('fml.__main__.GeminiService', spec=True) as MockGeminiService:
        MockGeminiService.get_supported_models.return_value = [model.value for model in GeminiModels]
        MockGeminiService.__name__ = "GeminiService" # Explicitly set __name__ for the mock class
        yield MockGeminiService

@pytest.fixture
def mock_os_getenv():
    """
    Fixture to mock os.getenv.
    """
    with patch('os.getenv') as mock_getenv:
        yield mock_getenv

def test_initialize_ai_service_valid_gemini_model(mock_gemini_service_class, mock_os_getenv):
    """
    Test that _initialize_ai_service correctly instantiates GeminiService for a valid Gemini model.
    """
    mock_os_getenv.return_value = "dummy_gemini_api_key"
    model_name = GeminiModels.GEMINI_1_5_FLASH.value

    service = _initialize_ai_service(model_name)

    expected_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "fml", "prompts", "gemini_system_prompt.txt"))
    mock_gemini_service_class.assert_called_once_with(
        api_key="dummy_gemini_api_key",
        system_instruction_path=expected_path,
        model=model_name
    )
    assert service is mock_gemini_service_class.return_value

def test_initialize_ai_service_unsupported_model(mock_gemini_service_class, mock_os_getenv):
    """
    Test that a ValueError is raised for an unsupported model name.
    """
    mock_os_getenv.return_value = "dummy_gemini_api_key"
    model_name = "unsupported-model"

    with pytest.raises(ValueError) as exc_info:
        _initialize_ai_service(model_name)

    assert f"Unsupported model '{model_name}'." in str(exc_info.value)
    assert "Supported models are: gemini-1.5-flash, gemini-1.5-pro" in str(exc_info.value) # Ensure supported models are listed

def test_initialize_ai_service_missing_gemini_api_key(mock_gemini_service_class, mock_os_getenv):
    """
    Test that a RuntimeError is raised when GEMINI_API_KEY is not set.
    """
    mock_os_getenv.return_value = None  # Simulate missing API key
    model_name = GeminiModels.GEMINI_1_5_FLASH.value

    with pytest.raises(RuntimeError) as exc_info:
        _initialize_ai_service(model_name)

    assert "API key environment variable not set for GeminiService." in str(exc_info.value)
    mock_gemini_service_class.assert_not_called() # Ensure service is not instantiated

def test_initialize_ai_service_correct_system_prompt_path(mock_gemini_service_class, mock_os_getenv):
    """
    Test that the correct system prompt path is determined for GeminiService.
    """
    mock_os_getenv.return_value = "dummy_gemini_api_key"
    model_name = GeminiModels.GEMINI_1_5_FLASH.value

    _initialize_ai_service(model_name)

    expected_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "fml", "prompts", "gemini_system_prompt.txt"))
    mock_gemini_service_class.assert_called_once()
    assert mock_gemini_service_class.call_args.kwargs['system_instruction_path'] == expected_path

def test_initialize_ai_service_returns_ai_service_instance(mock_gemini_service_class, mock_os_getenv):
    """
    Test that the function returns an instance that behaves like an AIService.
    """
    mock_os_getenv.return_value = "dummy_gemini_api_key"
    model_name = GeminiModels.GEMINI_1_5_FLASH.value

    service = _initialize_ai_service(model_name)
    assert isinstance(service, AIService) # Check against the abstract base class. This will pass if the mock instance correctly implements the AIService interface.
