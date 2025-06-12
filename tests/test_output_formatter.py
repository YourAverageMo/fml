import pytest
from fml.schemas import AICommandResponse, Flag
from fml.output_formatter import OutputFormatter


@pytest.fixture
def output_formatter():
    return OutputFormatter()


def test_format_response_standard_output(output_formatter):
    """
    Test that format_response produces the expected string output for a typical AICommandResponse.
    """
    flags = [
        Flag(flag="-a", description="All files"),
        Flag(flag="-l", description="Long listing format"),
    ]
    ai_response = AICommandResponse(
        explanation="Lists directory contents.", flags=flags, command="ls -al"
    )
    expected_output = (
        "Lists directory contents.\n\n-a: All files\n-l: Long listing format\n\nls -al"
    )
    assert output_formatter.format_response(ai_response, enable_color=False) == expected_output


def test_format_response_no_flags(output_formatter):
    """
    Test a scenario where the flags list is empty.
    """
    ai_response = AICommandResponse(
        explanation="Displays current working directory.", flags=[], command="pwd"
    )
    expected_output = "Displays current working directory.\n\npwd"
    assert output_formatter.format_response(ai_response, enable_color=False) == expected_output


def test_format_response_empty_command(output_formatter):
    """
    Test a scenario where the command field is an empty string.
    """
    flags = [Flag(flag="--version", description="Show version information")]
    ai_response = AICommandResponse(
        explanation="This command shows the version of the tool.",
        flags=flags,
        command="",
    )
    expected_output = (
        "This command shows the version of the tool.\n"
        "\n"
        "--version: Show version information\n"
        "\n"
        ""
    )
    assert output_formatter.format_response(ai_response, enable_color=False) == expected_output


def test_format_response_long_explanation(output_formatter):
    """
    Test with a longer explanation to ensure it's handled correctly.
    """
    ai_response = AICommandResponse(
        explanation="This is a very long explanation that spans multiple sentences to describe the complex nature of the command. It should still be formatted correctly and appear as a single block of text before the flags and command.",
        flags=[],
        command="complex_command --option",
    )
    expected_output = (
        "This is a very long explanation that spans multiple sentences to describe the complex nature of the command. It should still be formatted correctly and appear as a single block of text before the flags and command.\n"
        "\n"
        "complex_command --option"
    )
    assert output_formatter.format_response(ai_response, enable_color=False) == expected_output


def test_format_response_special_characters(output_formatter):
    """
    Test with special characters in explanation, flags, and command.
    """
    flags = [
        Flag(flag="-f", description="File with spaces & symbols: file_name (1).txt"),
        Flag(flag="--path", description="Path to directory /usr/local/bin/*"),
    ]
    ai_response = AICommandResponse(
        explanation="This command handles files with tricky names and paths! Use it carefully.",
        flags=flags,
        command="cp 'file name (1).txt' /tmp/new_dir",
    )
    expected_output = (
        "This command handles files with tricky names and paths! Use it carefully.\n"
        "\n"
        "-f: File with spaces & symbols: file_name (1).txt\n"
        "--path: Path to directory /usr/local/bin/*\n"
        "\n"
        "cp 'file name (1).txt' /tmp/new_dir"
    )
    assert output_formatter.format_response(ai_response, enable_color=False) == expected_output


def test_format_response_empty_explanation(output_formatter):
    """
    Test a scenario where the explanation field is an empty string.
    """
    flags = [Flag(flag="-v", description="Verbose output")]
    ai_response = AICommandResponse(explanation="", flags=flags, command="echo hello")
    expected_output = "\n\n-v: Verbose output\n\necho hello"
    assert output_formatter.format_response(ai_response, enable_color=False) == expected_output


def test_format_response_empty_flags_and_explanation(output_formatter):
    """
    Test a scenario where both flags and explanation are empty.
    """
    ai_response = AICommandResponse(explanation="", flags=[], command="just_a_command")
    expected_output = "\n\njust_a_command"
    assert output_formatter.format_response(ai_response, enable_color=False) == expected_output
