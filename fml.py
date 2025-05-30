import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered CLI Command Helper",
        epilog="Example: fml 'how do i view the git diff for my current branch compared to main?'"
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Your natural language query for a CLI command."
    )

    args = parser.parse_args()

    if not args.query:
        parser.print_help()
        sys.exit(1)

    print(f"Query received: {args.query}")
    # Placeholder for AI interaction and further logic
    print("AI interaction and command generation will go here.")

if __name__ == "__main__":
    main()
