import pytest
from unittest.mock import MagicMock, patch, mock_open
from fml.ai_providers.gemini_service import GeminiService
from fml.ai_providers.models import MODELS
from fml.schemas import AICommandResponse, AIContext, SystemInfo
from fml.ai_service import AIServiceError
from google import genai
from google.genai.types import GenerateContentResponse
from google.genai.errors import APIError


@pytest.fixture
def mock_genai_client():
    """Fixture to mock the genai.Client and its generate_content method."""
    with patch("google.genai.Client") as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance
        # Mock the models attribute of the client instance
        mock_client_instance.models = MagicMock()
        yield mock_client_class


@pytest.fixture
def mock_ai_context():
    """Fixture to provide a mock AIContext object."""
    return AIContext(
        system_info=SystemInfo(
            os_name="test_os",
            shell="test_shell",
            cwd="/test/cwd",
            architecture="test_arch",
            python_version="3.9.0",
        )
    )


def test_gemini_service_initialization(mock_genai_client):
    """Verify that GeminiService initializes correctly."""
    api_key = "test_gemini_api_key"
    system_instruction_content = "mock system instruction"
    model = "gemini-1.5-flash"

    service = GeminiService(api_key, system_instruction_content, model)

    # Assert that genai.Client was called with the correct api_key
    mock_genai_client.assert_called_once_with(api_key=api_key)
    assert service.model_name == model
    assert service.system_instruction == "mock system instruction"


def test_gemini_service_generate_command_success(mock_genai_client, mock_ai_context):
    """Verify generate_command successfully calls API and parses response."""
    api_key = "test_gemini_api_key"
    system_instruction_content = "mock system instruction"
    model = "gemini-1.5-pro"
    query = "how to list docker containers"

    mock_response_text = '{"explanation": "Lists all Docker containers.", "flags": [], "command": "docker ps -a"}'
    mock_api_response = MagicMock(spec=GenerateContentResponse)
    mock_api_response.text = mock_response_text

    # Get the mock client instance from the mock_genai_client (which is the class)
    mock_client_instance = mock_genai_client.return_value
    mock_client_instance.models.generate_content.return_value = mock_api_response

    service = GeminiService(api_key, system_instruction_content, model)
    response = service.generate_command(query, mock_ai_context)

    expected_system_info_json = mock_ai_context.system_info.model_dump_json(indent=2)
    expected_contents = [
        query,
        f"\n\nUser's System Information:\n```json\n{expected_system_info_json}\n```",
    ]

    mock_client_instance.models.generate_content.assert_called_once_with(
        model=model,
        contents=expected_contents,
        config=genai.types.GenerateContentConfig(
            system_instruction="mock system instruction",
            response_mime_type="application/json",
            response_schema=AICommandResponse.model_json_schema(),
        ),
    )
    assert isinstance(response, AICommandResponse)
    assert response.command == "docker ps -a"
    assert response.explanation == "Lists all Docker containers."
    assert response.flags == []


def test_gemini_service_generate_command_api_error(mock_genai_client, mock_ai_context):
    """Verify generate_command handles APIError."""
    api_key = "test_gemini_api_key"
    system_instruction_content = "mock system instruction"
    model = "gemini-1.5-flash"
    query = "some query"

    mock_client_instance = mock_genai_client.return_value
    mock_client_instance.models.generate_content.side_effect = APIError(
        "Rate limit exceeded",
        response_json={"error": {"message": "Rate limit exceeded", "code": 429}},
    )

    service = GeminiService(api_key, system_instruction_content, model)
    with pytest.raises(
        AIServiceError,
        match="API Error: Rate limit exceeded \\(Code: Rate limit exceeded\\)",
    ):
        service.generate_command(query, mock_ai_context)


def test_gemini_service_generate_command_unexpected_error(
    mock_genai_client, mock_ai_context
):
    """Verify generate_command handles unexpected errors."""
    api_key = "test_gemini_api_key"
    system_instruction_content = "mock system instruction"
    model = "gemini-1.5-pro"
    query = "another query"

    mock_client_instance = mock_genai_client.return_value
    mock_client_instance.models.generate_content.side_effect = Exception(
        "Network connection lost"
    )

    service = GeminiService(api_key, system_instruction_content, model)
    with pytest.raises(
        AIServiceError,
        match="An unexpected error occurred during AI interaction: Network connection lost",
    ):
        service.generate_command(query, mock_ai_context)


def test_gemini_service_generate_command_invalid_json_response(
    mock_genai_client, mock_ai_context
):
    """Verify generate_command handles invalid JSON response."""
    api_key = "test_gemini_api_key"
    system_instruction_content = "mock system instruction"
    model = "gemini-1.5-flash"
    query = "invalid json test"

    mock_api_response = MagicMock(spec=GenerateContentResponse)
    mock_api_response.text = '{"explanation": "invalid json", "flags": "not a list", "command": "invalid"}'  # Invalid flags type

    mock_client_instance = mock_genai_client.return_value
    mock_client_instance.models.generate_content.return_value = mock_api_response

    service = GeminiService(api_key, system_instruction_content, model)
    with pytest.raises(
        AIServiceError,
        match="AI Response Format Error: The AI returned an unexpected response format. Details: 1 validation error for AICommandResponse",
    ):
        service.generate_command(query, mock_ai_context)
