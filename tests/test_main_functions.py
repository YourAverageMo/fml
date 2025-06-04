import pytest
import os
from unittest.mock import patch, MagicMock
from fml.__main__ import _initialize_ai_service
from fml.ai_providers.gemini_service import GeminiService
from fml.ai_providers.models import MODELS
from fml.ai_service import AIService


@pytest.fixture
def mock_gemini_service_class():
    """
    Fixture to mock the GeminiService class.
    """
    MockGeminiService = MagicMock(spec=GeminiService)
    MockGeminiService.__name__ = "GeminiService"
    MockGeminiService.return_value = MagicMock(spec=AIService)
    yield MockGeminiService


@pytest.fixture
def mock_importlib_import_module(mock_gemini_service_class):
    """
    Fixture to mock importlib.import_module for dynamic imports.
    """
    with patch("importlib.import_module") as mock_import_module:

        def side_effect_import_module(name, *args, **kwargs):
            if name == MODELS["gemini-1.5-flash"].provider:
                mock_gemini_module = MagicMock()
                mock_gemini_module.GeminiService = mock_gemini_service_class
                return mock_gemini_module
            elif name == MODELS["gemini-1.5-flash"].prompt_module:
                mock_prompt_module = MagicMock()
                setattr(
                    mock_prompt_module,
                    MODELS["gemini-1.5-flash"].prompt_variable,
                    "mock system prompt content",
                )
                return mock_prompt_module
            else:
                return MagicMock()

        mock_import_module.side_effect = side_effect_import_module
        yield mock_import_module


@pytest.fixture
def mock_os_getenv():
    """
    Fixture to mock os.getenv.
    """
    with patch("os.getenv") as mock_getenv:
        yield mock_getenv


def test_initialize_ai_service_valid_gemini_model(
    mock_gemini_service_class, mock_os_getenv, mock_importlib_import_module
):
    """
    Test that _initialize_ai_service correctly instantiates GeminiService for a valid Gemini model.
    """
    mock_os_getenv.return_value = "dummy_gemini_api_key"
    model_name = "gemini-1.5-flash"
    mock_prompt_content = "mock system prompt content"

    service = _initialize_ai_service(model_name)

    mock_importlib_import_module.assert_any_call(
        MODELS[model_name].prompt_module
    )  # Check that the prompt module was imported
    mock_gemini_service_class.assert_called_once_with(
        api_key="dummy_gemini_api_key",
        system_instruction_content=mock_prompt_content,
        model=model_name,
    )
    assert (
        service is mock_gemini_service_class.return_value
    )  # Ensure the returned service is the mocked instance


def test_initialize_ai_service_unsupported_model(
    mock_gemini_service_class, mock_os_getenv, mock_importlib_import_module
):
    """
    Test that a ValueError is raised for an unsupported model name.
    """
    mock_os_getenv.return_value = "dummy_gemini_api_key"
    model_name = "unsupported-model"

    with pytest.raises(ValueError) as exc_info:
        _initialize_ai_service(model_name)

    assert f"Unsupported model '{model_name}'." in str(exc_info.value)
    assert f"Supported models are: {', '.join(MODELS.keys())}" in str(
        exc_info.value
    )  # Ensure supported models are listed dynamically


def test_initialize_ai_service_missing_gemini_api_key(
    mock_gemini_service_class, mock_os_getenv, mock_importlib_import_module
):
    """
    Test that a RuntimeError is raised when GEMINI_API_KEY is not set.
    """
    mock_os_getenv.return_value = None  # Simulate missing API key
    model_name = "gemini-1.5-flash"

    with pytest.raises(RuntimeError) as exc_info:
        _initialize_ai_service(model_name)

    assert (
        "API key environment variable 'GEMINI_API_KEY' not set for model 'gemini-1.5-flash'."
        in str(exc_info.value)
    )
    mock_gemini_service_class.assert_not_called()  # Ensure service is not instantiated


def test_initialize_ai_service_returns_ai_service_instance(
    mock_gemini_service_class, mock_os_getenv, mock_importlib_import_module
):
    """
    Test that the function returns an instance that behaves like an AIService.
    """
    mock_os_getenv.return_value = "dummy_gemini_api_key"
    model_name = "gemini-1.5-flash"
    mock_prompt_content = "mock system prompt content"

    service = _initialize_ai_service(model_name)
    assert isinstance(
        service, AIService
    )  # Check against the abstract base class. This will pass if the mock instance correctly implements the AIService interface.
