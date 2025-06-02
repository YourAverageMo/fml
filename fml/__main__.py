import argparse
import os
import sys
from fml.ai_providers.gemini_service import GeminiService
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

    args = parser.parse_args()

    # If no query arguments are provided, print help and exit.
    # argparse handles -h/--help automatically when nargs=REMAINDER is used.
    if not args.query:
        parser.print_help()
        sys.exit(0)  # Exit with 0 for successful help display

    # Join the list of query parts into a single string
    full_query = " ".join(args.query)

    # API Key Management
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print(
            "Please set the GEMINI_API_KEY environment variable to your Google Gemini API key."
        )
        sys.exit(1)

    # Initialize AI Service
    system_prompt_path = os.path.join(os.path.dirname(__file__), "prompts",
                                      "gemini_system_prompt.txt")
    ai_service: AIService = GeminiService(api_key=api_key,
                                          system_instruction_path=system_prompt_path)

    # Generate command
    try:
        ai_command_response = ai_service.generate_command(full_query)
    except RuntimeError as e:
        print(f"Error generating command: {e}")
        sys.exit(1)

    # Format and display response
    formatter = OutputFormatter()
    formatted_output = formatter.format_response(ai_command_response)
    print(formatted_output)



if __name__ == "__main__":
    main()
