import argparse
import os
import sys
import pyperclip
import importlib
from fml.ai_providers.models import MODELS
from fml.output_formatter import OutputFormatter
from fml.ai_service import AIService, AIServiceError
from fml.schemas import AIContext, SystemInfo
from fml.gather_system_info import get_system_info


def _initialize_ai_service(model_name: str) -> AIService:
    """
    Initializes and returns the appropriate AI service based on the model name.
    """
    model_provider_details = MODELS.get(model_name)

    if not model_provider_details:
        supported_models_list = list(MODELS.keys())
        raise ValueError(
            f"Unsupported model '{model_name}'. Supported models are: {', '.join(supported_models_list)}"
        )

    provider_module_name = model_provider_details.provider
    service = model_provider_details.service
    env_var = model_provider_details.env_var
    prompt_module_name = model_provider_details.prompt_module
    prompt_name = model_provider_details.prompt_variable

    api_key = os.getenv(env_var)
    if not api_key:
        raise RuntimeError(
            f"API key environment variable '{env_var}' not set for model '{model_name}'."
        )

    # Dynamically import the provider module and class
    try:
        provider_module = importlib.import_module(provider_module_name)
        service_class = getattr(provider_module, service)
    except (ImportError, AttributeError) as e:
        raise RuntimeError(
            f"Failed to dynamically load AI service for model '{model_name}': {e}"
        ) from e

    try:
        prompt_module = importlib.import_module(prompt_module_name)
        system_instruction_content = getattr(prompt_module, prompt_name)
    except (ImportError, AttributeError) as e:
        raise RuntimeError(
            f"Failed to load system prompt for model '{model_name}': {e}"
        ) from e

    selected_ai_service = service_class(
        api_key=api_key,
        system_instruction_content=system_instruction_content,
        model=model_name,
    )

    return selected_ai_service


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered CLI Command Helper",
        epilog="Example: fml 'how do i view the git diff for my current branch compared to main?'",
    )
    parser.add_argument(
        "query",
        nargs=argparse.REMAINDER,
        help="Your natural language query for a CLI command.",
    )
    parser.add_argument(
        "-m",
        "--model",
        default=list(MODELS.keys())[
            0
        ],  # Use the first model in the MODELS dictionary as default
        help="Specify the AI model to use (e.g., 'gemini-1.5-flash').",
    )

    args = parser.parse_args()

    # If no query arguments are provided, print help and exit.
    # argparse handles -h/--help automatically when nargs=REMAINDER is used.
    if not args.query:
        parser.print_help()
        sys.exit(0)  # Exit with 0 for successful help display

    # Join the list of query parts into a single string
    full_query = " ".join(args.query)

    # Gather system information
    system_info = get_system_info()
    ai_context = AIContext(system_info=system_info)

    # Initialize AI service and generate command
    try:
        ai_service = _initialize_ai_service(args.model)
        ai_command_response = ai_service.generate_command(full_query, ai_context)
    except (AIServiceError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Format and display response
    formatter = OutputFormatter()
    formatted_output = formatter.format_response(ai_command_response)
    print(formatted_output)

    # Copy command to clipboard
    try:
        pyperclip.copy(ai_command_response.command)
        print("(command copied to clipboard)")
    except pyperclip.PyperclipException as e:
        print(f"Warning: Could not copy to clipboard: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
