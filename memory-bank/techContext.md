# Tech Context: `fml` - AI-Powered CLI Command Helper

## 1. Technologies Used

- **Programming Language:** Python (version 3.8+)
- **AI Service Integration:**
  - **Initial:** Google Gemini, using the official `google-generativeai` Python SDK.
  - **Modularity:** AI interaction logic will be wrapped in an abstraction layer to allow for future integration with other providers (OpenAI, Ollama).
- **Command-Line Argument Parsing:** Python's built-in `argparse` module.
- **Clipboard Access:** `pyperclip` library (cross-platform).
- **API Key Management:** Python's `os.environ` for reading environment variables.
- **Potential TUI Libraries (for future consideration):** `Textual` or `prompt_toolkit`.

## 2. Development Setup

- **Python Environment:** Use `uv init` or `python -m venv` for project initialization and dependency management.
- **Dependencies:**
  - `google-generativeai`
  - `pyperclip`
- **API Key:** `GEMINI_API_KEY` environment variable must be set for Google Gemini API access.

## 3. Technical Constraints

- **Python Version:** Minimum Python 3.8.
- **AI Output Format:** Strict requirement for AI to return a structured JSON object.
- **Cross-Platform Compatibility:** Must function on macOS, Windows, and Linux.
- **API Rate Limits:** Awareness and potential handling of Google Gemini API rate limits.

## 4. Dependencies

- **External Libraries:**
  - `google-generativeai`: For interacting with the Google Gemini API.
  - `pyperclip`: For cross-platform clipboard operations.
- **System Dependencies for `pyperclip` (Linux):** May require `xclip` or `xsel` to be installed on Linux systems.

## 5. Tool Usage Patterns

- **`argparse`:** Used for robust and standard CLI argument parsing.
- **`os.environ`:** Standard Python approach for secure environment variable access.
- **`google-generativeai` SDK:** Direct interaction with the Gemini API via its official SDK.
- **`pyperclip`:** Utilized for its cross-platform capabilities in clipboard management.
