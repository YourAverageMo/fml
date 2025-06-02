import argparse
import os
import sys
from fml.ai_providers.gemini_service import GeminiService, GeminiModels
from fml.output_formatter import OutputFormatter
from fml.ai_service import AIService


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

    # List of available AI services
    available_ai_services = [GeminiService]

    selected_ai_service: AIService | None = None
    api_key: str | None = None
    system_prompt_path: str | None = None

    for service_class in available_ai_services:
        if args.model in service_class.get_supported_models():
            # Determine API key based on service
            if service_class == GeminiService:
                api_key = os.getenv("GEMINI_API_KEY")
                system_prompt_path = os.path.join(
                    os.path.dirname(__file__), "prompts", "gemini_system_prompt.txt"
                )
            # Add elif for other services here in the future

            if not api_key:
                print(
                    f"Error: API key environment variable not set for {service_class.__name__}."
                )
                sys.exit(1)

            selected_ai_service = service_class(
                api_key=api_key,
                system_instruction_path=system_prompt_path,
                model=args.model,
            )
            break

    if not selected_ai_service:
        print(f"Error: Unsupported model '{args.model}'.")
        print("Supported models are:")
        for service_class in available_ai_services:
            for model_name in service_class.get_supported_models():
                print(f"- {model_name}")
        sys.exit(1)

    # Generate command
    try:
        ai_command_response = selected_ai_service.generate_command(full_query)
    except RuntimeError as e:
        print(f"Error generating command: {e}")
        sys.exit(1)

    # Format and display response
    formatter = OutputFormatter()
    formatted_output = formatter.format_response(ai_command_response)
    print(formatted_output)



if __name__ == "__main__":
    main()
