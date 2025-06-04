import pytest
import subprocess
import os
from unittest.mock import patch, MagicMock, ANY

from fml.schemas import AICommandResponse, AIContext, SystemInfo
from fml.ai_service import AIServiceError


# Helper function to run fml.py using uv run
def run_fml_command(
    args, env=None, mock_stdout=None, mock_stderr=None, mock_returncode=0
):
    """Helper to run the fml command with given arguments and capture output."""
    command = ["uv", "run", "python", "-m", "fml"] + args
    current_env = os.environ.copy()
    if env:
        current_env.update(env)

    # Mock subprocess.run if mock_stdout or mock_stderr are provided
    if mock_stdout is not None or mock_stderr is not None:
        mock_completed_process = MagicMock(spec=subprocess.CompletedProcess)
        mock_completed_process.returncode = mock_returncode
        mock_completed_process.stdout = mock_stdout if mock_stdout is not None else ""
        mock_completed_process.stderr = mock_stderr if mock_stderr is not None else ""
        with patch("subprocess.run", return_value=mock_completed_process) as mock_run:
            return subprocess.run(
                command, capture_output=True, text=True, check=False, env=current_env
            )
    else:
        return subprocess.run(
            command, capture_output=True, text=True, check=False, env=current_env
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
            python_version="test_python_version",
        ),
    )


@pytest.fixture
def mock_initialize_ai_service_fixture(mock_ai_context):
    """Fixture to mock _initialize_ai_service and its generate_command method."""
    with patch("fml.__main__._initialize_ai_service") as mock_init:
        mock_service = MagicMock()
        mock_service.generate_command.return_value = AICommandResponse(
            explanation="Test explanation.", flags=[], command="test command"
        )
        mock_init.return_value = mock_service
        yield mock_init


@pytest.fixture
def mock_get_system_info_fixture(mock_ai_context):
    """Fixture to mock get_system_info."""
    with patch(
        "fml.__main__.get_system_info", return_value=mock_ai_context.system_info
    ) as mock_get_info:
        yield mock_get_info


@pytest.fixture
def mock_successful_fml_run():
    """Mocks subprocess.run for a successful fml command execution."""
    mock_completed_process = MagicMock(spec=subprocess.CompletedProcess)
    mock_completed_process.returncode = 0
    mock_completed_process.stdout = (
        "Test explanation.\n\ntest command\n(command copied to clipboard)\n"
    )
    mock_completed_process.stderr = ""
    with patch("subprocess.run", return_value=mock_completed_process) as mock_run:
        yield mock_run


@pytest.fixture
def mock_help_fml_run():
    """Mocks subprocess.run for fml --help command execution."""
    mock_completed_process = MagicMock(spec=subprocess.CompletedProcess)
    mock_completed_process.returncode = 0
    mock_completed_process.stdout = "usage: __main__.py [-h] [-m {gemini-1.5-flash,gemini-1.5-pro}] query\n\nAI-Powered CLI Command Helper\n\npositional arguments:\n  query       The natural language query for the CLI command.\n\noptions:\n  -h, --help  show this help message and exit\n  -m {gemini-1.5-flash,gemini-1.5-pro}, --model {gemini-1.5-flash,gemini-1.5-pro}\n              Specify the AI model to use (e.g., gemini-1.5-flash).\n"
    mock_completed_process.stderr = ""
    with patch("subprocess.run", return_value=mock_completed_process) as mock_run:
        yield mock_run


@pytest.fixture
def mock_api_key_set_fml_run():
    """Mocks subprocess.run for fml command when API key is set."""
    mock_completed_process = MagicMock(spec=subprocess.CompletedProcess)
    mock_completed_process.returncode = 0
    mock_completed_process.stdout = (
        "Test explanation.\n\ntest command\n(command copied to clipboard)\n"
    )
    mock_completed_process.stderr = ""
    with patch("subprocess.run", return_value=mock_completed_process) as mock_run:
        yield mock_run


@pytest.fixture
def mock_api_key_not_set_fml_run():
    """Mocks subprocess.run for fml command when API key is not set."""
    mock_completed_process = MagicMock(spec=subprocess.CompletedProcess)
    mock_completed_process.returncode = 1
    mock_completed_process.stdout = ""
    mock_completed_process.stderr = (
        "Error: API key environment variable not set for GeminiService.\n"
    )
    with patch("subprocess.run", return_value=mock_completed_process) as mock_run:
        yield mock_run


def test_cli_parsing_with_quotes(mock_successful_fml_run):
    """
    Test that a query provided with quotes is correctly captured and processed.
    Simulates: fml "how do i view the git diff"
    """
    result = run_fml_command(["how do i view the git diff"])
    assert result.returncode == 0
    assert "Test explanation." in result.stdout
    assert "test command" in result.stdout
    assert "(command copied to clipboard)" in result.stdout
    assert not result.stderr
    mock_successful_fml_run.assert_called_once_with(
        ["uv", "run", "python", "-m", "fml", "how do i view the git diff"],
        capture_output=True,
        text=True,
        check=False,
        env=ANY,
    )


def test_cli_parsing_without_quotes(mock_successful_fml_run):
    """
    Test that a query provided without quotes is correctly captured as a single string and processed.
    Simulates: fml how do i view the git diff
    """
    result = run_fml_command(["how", "do", "i", "view", "the", "git", "diff"])
    assert result.returncode == 0
    assert "Test explanation." in result.stdout
    assert "test command" in result.stdout
    assert "(command copied to clipboard)" in result.stdout
    assert not result.stderr
    mock_successful_fml_run.assert_called_once_with(
        [
            "uv",
            "run",
            "python",
            "-m",
            "fml",
            "how",
            "do",
            "i",
            "view",
            "the",
            "git",
            "diff",
        ],
        capture_output=True,
        text=True,
        check=False,
        env=ANY,
    )


def test_cli_parsing_help_flag(mock_help_fml_run):
    """
    Test that the -h flag displays the help message and exits with code 0.
    Simulates: fml -h
    """
    result = run_fml_command(["-h"])
    assert result.returncode == 0
    assert "usage: __main__.py [-h]" in result.stdout
    assert "AI-Powered CLI Command Helper" in result.stdout
    assert not result.stderr
    mock_help_fml_run.assert_called_once_with(
        ["uv", "run", "python", "-m", "fml", "-h"],
        capture_output=True,
        text=True,
        check=False,
        env=ANY,
    )


def test_cli_parsing_help_long_flag(mock_help_fml_run):
    """
    Test that the --help flag displays the help message and exits with code 0.
    Simulates: fml --help
    """
    result = run_fml_command(["--help"])
    assert result.returncode == 0
    assert "usage: __main__.py [-h]" in result.stdout
    assert "AI-Powered CLI Command Helper" in result.stdout
    assert not result.stderr
    mock_help_fml_run.assert_called_once_with(
        ["uv", "run", "python", "-m", "fml", "--help"],
        capture_output=True,
        text=True,
        check=False,
        env=ANY,
    )


def test_api_key_set(mock_api_key_set_fml_run):
    """
    Test that the application proceeds if GEMINI_API_KEY is set.
    """
    env_with_key = os.environ.copy()
    env_with_key["GEMINI_API_KEY"] = (
        "dummy_api_key_123"  # This key is only used to satisfy the check in _initialize_ai_service
    )

    result = run_fml_command(["another query"], env=env_with_key)

    assert result.returncode == 0
    assert "Test explanation." in result.stdout
    assert "test command" in result.stdout
    assert "(command copied to clipboard)" in result.stdout
    assert (
        "Error: API key environment variable not set for GeminiService."
        not in result.stderr
    )
    assert not result.stderr
    mock_api_key_set_fml_run.assert_called_once_with(
        ["uv", "run", "python", "-m", "fml", "another query"],
        capture_output=True,
        text=True,
        check=False,
        env=ANY,
    )


def test_api_key_not_set(mock_api_key_not_set_fml_run):
    """
    Test that the application exits with an error if GEMINI_API_KEY is not set.
    """
    original_gemini_api_key = os.getenv("GEMINI_API_KEY")
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]

    result = run_fml_command(["some query"])

    if original_gemini_api_key:
        os.environ["GEMINI_API_KEY"] = original_gemini_api_key

    assert result.returncode == 1
    assert (
        "Error: API key environment variable not set for GeminiService."
        in result.stderr
    )
    assert not result.stdout
    mock_api_key_not_set_fml_run.assert_called_once_with(
        ["uv", "run", "python", "-m", "fml", "some query"],
        capture_output=True,
        text=True,
        check=False,
        env=ANY,
    )
