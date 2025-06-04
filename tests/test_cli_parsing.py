import argparse
import pytest
import sys
from unittest.mock import patch, MagicMock

# Import the main function and the helper function from the application
from fml.__main__ import main, _initialize_ai_service
from fml.ai_providers.models import MODELS
from fml.schemas import AIContext, SystemInfo
from fml.ai_service import AIServiceError


@pytest.fixture
def mock_sys_argv():
    """Fixture to temporarily modify sys.argv for CLI argument testing."""
    original_argv = sys.argv
    try:
        yield
    finally:
        sys.argv = original_argv


@pytest.fixture
def mock_sys_exit():
    """Fixture to mock sys.exit to prevent actual program exit during tests."""
    with patch('sys.exit') as mock_exit:
        def side_effect(code=None):
            raise SystemExit(code)
        mock_exit.side_effect = side_effect
        yield mock_exit


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


@pytest.fixture
def mock_initialize_ai_service(mock_ai_context):
    """Fixture to mock _initialize_ai_service to isolate CLI parsing tests."""
    with patch('fml.__main__._initialize_ai_service') as mock_init:
        mock_service = MagicMock()
        mock_service.generate_command.return_value = MagicMock(
            explanation="Test explanation.",
            flags=[],
            command="test command"
        )
        mock_init.return_value = mock_service
        yield mock_init


@pytest.fixture
def mock_output_formatter():
    """Fixture to mock OutputFormatter to prevent actual printing during tests."""
    with patch('fml.__main__.OutputFormatter') as mock_formatter_class:
        mock_formatter_instance = MagicMock()
        mock_formatter_instance.format_response.return_value = "Formatted Output"
        mock_formatter_class.return_value = mock_formatter_instance
        yield mock_formatter_class


def test_main_no_query_prints_help_and_exits(mock_sys_argv, mock_sys_exit, capsys):
    """
    Test that main() prints help message and exits when no query is provided.
    """
    sys.argv = ['fml']
    with pytest.raises(SystemExit) as excinfo:
        main()
    mock_sys_exit.assert_called_once_with(0)
    assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert "usage: fml" in captured.out
    assert "Your natural language query for a CLI command." in captured.out


def test_main_with_query_and_default_model(mock_sys_argv, mock_sys_exit,
                                           mock_initialize_ai_service,
                                           mock_output_formatter, capsys,
                                           mock_ai_context):
    """
    Test main() with a query and verifies default model is used.
    """
    sys.argv = ['fml', 'how do I list files?']
    # Mock get_system_info to return a consistent SystemInfo object
    with patch('fml.__main__.get_system_info', return_value=mock_ai_context.system_info):
        main()
    mock_sys_exit.assert_not_called()  # Should not exit on valid query
    mock_initialize_ai_service.assert_called_once_with(
        "gemini-1.5-flash")
    mock_initialize_ai_service.return_value.generate_command.assert_called_once_with(
        "how do I list files?", mock_ai_context)
    mock_output_formatter.return_value.format_response.assert_called_once()
    captured = capsys.readouterr()
    assert "Formatted Output" in captured.out


def test_main_with_query_and_specified_model(mock_sys_argv, mock_sys_exit,
                                             mock_initialize_ai_service,
                                             mock_output_formatter, capsys,
                                             mock_ai_context):
    """
    Test main() with a query and a specified model.
    """
    sys.argv = ['fml', '--model', 'gemini-1.0-pro', 'show docker images']
    with patch('fml.__main__.get_system_info', return_value=mock_ai_context.system_info):
        main()
    mock_sys_exit.assert_not_called()
    mock_initialize_ai_service.assert_called_once_with('gemini-1.0-pro')
    mock_initialize_ai_service.return_value.generate_command.assert_called_once_with(
        "show docker images", mock_ai_context)
    mock_output_formatter.return_value.format_response.assert_called_once()
    captured = capsys.readouterr()
    assert "Formatted Output" in captured.out


def test_main_with_multi_word_query(mock_sys_argv, mock_sys_exit,
                                    mock_initialize_ai_service,
                                    mock_output_formatter, capsys,
                                    mock_ai_context):
    """
    Test main() with a multi-word query that argparse should join.
    """
    sys.argv = ['fml', 'git', 'commit', '-m', 'initial commit']
    with patch('fml.__main__.get_system_info', return_value=mock_ai_context.system_info):
        main()
    mock_sys_exit.assert_not_called()
    mock_initialize_ai_service.assert_called_once_with(
        "gemini-1.5-flash")
    mock_initialize_ai_service.return_value.generate_command.assert_called_once_with(
        "git commit -m initial commit", mock_ai_context)
    captured = capsys.readouterr()
    assert "Formatted Output" in captured.out


def test_main_handles_ai_service_runtime_error(mock_sys_argv, mock_sys_exit,
                                                mock_initialize_ai_service,
                                                capsys):
    """
    Test main() handles AIServiceError from _initialize_ai_service.
    """
    sys.argv = ['fml', 'some query']
    mock_initialize_ai_service.side_effect = AIServiceError("API key not set.")
    with pytest.raises(SystemExit) as excinfo:
        main()
    mock_sys_exit.assert_called_once_with(1)
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error: API key not set." in captured.err


def test_main_handles_ai_service_value_error(mock_sys_argv, mock_sys_exit,
                                              mock_initialize_ai_service,
                                              capsys):
    """
    Test main() handles ValueError from _initialize_ai_service (unsupported model).
    """
    sys.argv = ['fml', '--model', 'unsupported-model', 'some query']
    mock_initialize_ai_service.side_effect = ValueError(
        "Unsupported model 'unsupported-model'.")
    with pytest.raises(SystemExit) as excinfo:
        main()
    mock_sys_exit.assert_called_once_with(1)
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Unsupported model 'unsupported-model'." in captured.err
