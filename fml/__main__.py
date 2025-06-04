import argparse
import os
import sys
import pyperclip
from fml.ai_providers.gemini_service import GeminiService, GeminiModels
from fml.output_formatter import OutputFormatter
from fml.ai_service import AIService, AIServiceError
from fml.schemas import AIContext, SystemInfo
from fml.gather_system_info import get_system_info


def _initialize_ai_service(model_name: str) -> AIService:
    """
    Initializes and returns the appropriate AI service based on the model name.
    """
    available_ai_services = [GeminiService]  # Extend this list for other AI providers

    selected_ai_service: AIService | None = None
    api_key: str | None = None
    system_prompt_path: str | None = None

    for service_class in available_ai_services:
        if model_name in service_class.get_supported_models():
            # Determine API key and system prompt path based on service
            if service_class == GeminiService:
                api_key = os.getenv("GEMINI_API_KEY")
                system_prompt_path = os.path.join(os.path.dirname(__file__),
                                                  "prompts",
                                                  "gemini_system_prompt.txt")
            # Add elif for other services here in the future

            if not api_key:
                raise RuntimeError(
                    f"API key environment variable not set for {service_class.__name__}."
                )

            selected_ai_service = service_class(
                api_key=api_key,
                system_instruction_path=system_prompt_path,
                model=model_name,
            )
            break

    if not selected_ai_service:
        supported_models_list = []
        for service_class in available_ai_services:
            supported_models_list.extend(service_class.get_supported_models())
        raise ValueError(
            f"Unsupported model '{model_name}'. Supported models are: {', '.join(supported_models_list)}"
        )

    return selected_ai_service


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered CLI Command Helper",
        epilog=
        "Example: fml 'how do i view the git diff for my current branch compared to main?'",
    )
    parser.add_argument(
        "query",
        nargs=argparse.REMAINDER,
        help="Your natural language query for a CLI command.",
    )
    parser.add_argument(
        "-m",
        "--model",
        default=GeminiModels.GEMINI_1_5_FLASH.value,
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
