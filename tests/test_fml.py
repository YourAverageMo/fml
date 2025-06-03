import pytest
import subprocess
import sys
import os

# Helper function to run fml.py using uv run
def run_fml_command(args):
    # Construct the command to run fml.py using uv run
    # We need to ensure the fml.py script is found relative to the current working directory
    # which is /Users/mo/Repos/Professional/fml
    # The command should now be 'uv run python -m fml [args]'
    # This runs the 'fml' package's __main__.py
    command = ['uv', 'run', 'python', '-m', 'fml'] + args
    
    # Execute the command and capture output
    # check=False allows us to inspect the returncode even if it's non-zero
    return subprocess.run(command, capture_output=True, text=True, check=False)

def test_cli_parsing_with_quotes():
    """
    Test that a query provided with quotes is correctly captured.
    Simulates: fml "how do i view the git diff"
    """
    # subprocess.run will handle the quotes correctly if passed as a single argument
    result = run_fml_command(['how do i view the git diff'])
    assert result.returncode == 0
    assert "Query received: how do i view the git diff" in result.stdout
    assert not result.stderr

def test_cli_parsing_without_quotes():
    """
    Test that a query provided without quotes is correctly captured as a single string.
    Simulates: fml how do i view the git diff
    argparse with nargs='?' will combine these into a single string.
    """
    result = run_fml_command(['how', 'do', 'i', 'view', 'the', 'git', 'diff'])
    assert result.returncode == 0
    assert "Query received: how do i view the git diff" in result.stdout
    assert not result.stderr

def test_cli_parsing_help_flag():
    """
    Test that the -h/--help flag displays the help message and exits with code 0.
    Simulates: fml -h
    """
    result = run_fml_command(['-h'])
    assert result.returncode == 0
    assert "usage: fml" in result.stdout
    assert not result.stderr

def test_cli_parsing_help_long_flag():
    """
    Test that the --help flag displays the help message and exits with code 0.
    Simulates: fml --help
    """
    result = run_fml_command(['--help'])
    assert result.returncode == 0
    assert "usage: fml" in result.stdout
    assert not result.stderr

def test_api_key_set():
    """
    Test that the application proceeds if GEMINI_API_KEY is set.
    """
    # Temporarily set a dummy API key for this test
    original_gemini_api_key = os.getenv("GEMINI_API_KEY")
    os.environ["GEMINI_API_KEY"] = "dummy_api_key_123"

    result = run_fml_command(['another query'])
    
    # Restore the environment variable
    if original_gemini_api_key:
        os.environ["GEMINI_API_KEY"] = original_gemini_api_key
    else:
        del os.environ["GEMINI_API_KEY"] # Clean up if it wasn't set originally

    assert result.returncode == 0
    assert "Query received: another query" in result.stdout
    assert "AI interaction and command generation will go here." in result.stdout
    assert not "Error: GEMINI_API_KEY environment variable not set." in result.stdout
    assert not result.stderr
