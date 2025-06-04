import pytest
import pyperclip
from unittest.mock import MagicMock, patch
from fml.__main__ import main
from fml.schemas import AICommandResponse


@pytest.fixture
def mock_ai_service_success():
    """
    Mocks the AI service to return a successful AICommandResponse.
    """
    with patch("fml.__main__._initialize_ai_service") as mock_init_service:
        mock_service_instance = MagicMock()
        mock_service_instance.generate_command.return_value = AICommandResponse(
            explanation="This is a test explanation.",
            flags=[{"flag": "--test", "description": "A test flag."}],
            command="test command --test",
        )
        mock_init_service.return_value = mock_service_instance
        yield mock_init_service


def test_clipboard_copy_success(mock_ai_service_success, monkeypatch, capsys):
    """
    Tests that the command is copied to the clipboard and a confirmation message is displayed.
    """
    mock_pyperclip_copy = MagicMock()
    monkeypatch.setattr("pyperclip.copy", mock_pyperclip_copy)

    # Simulate command-line arguments
    monkeypatch.setattr("sys.argv", ["fml", "test query"])

    main()

    # Verify pyperclip.copy was called with the correct command
    mock_pyperclip_copy.assert_called_once_with("test command --test")

    # Verify the confirmation message is printed
    captured = capsys.readouterr()
    assert "(command copied to clipboard)" in captured.out


def test_clipboard_copy_failure(mock_ai_service_success, monkeypatch, capsys):
    """
    Tests that a warning is displayed if clipboard copying fails.
    """

    def mock_copy_fail(text):
        raise pyperclip.PyperclipException("Clipboard not available")

    monkeypatch.setattr("pyperclip.copy", mock_copy_fail)

    # Simulate command-line arguments
    monkeypatch.setattr("sys.argv", ["fml", "test query"])

    main()

    # Verify the warning message is printed to stderr
    captured = capsys.readouterr()
    assert (
        "Warning: Could not copy to clipboard: Clipboard not available" in captured.err
    )
