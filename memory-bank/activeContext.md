# Active Context: `fml` - AI-Powered CLI Command Helper

## 1. Current Work Focus

The current focus is on enhancing the LLM context with system information and ensuring all new additions are thoroughly tested, aiming for 100% or near 100% test coverage, including edge cases.

## 2. Recent Changes

- Initial memory bank files (`projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `activeContext.md`, `progress.md`) have been created based on the `prd.md`.
- The Python project environment has been initialized using `uv init`.
- The main application entry point (`fml.py`) has been created with basic CLI argument parsing implemented (Task 001 completed).
- All MVP development tasks (Task 001-007) have been created and added to the task queue.
- The project changes have been committed and merged to `main`.
- A new branch `add/tests` has been created for testing efforts.
- **Refactoring & Modularization:**
  - An `AIService` abstract base class (`fml/ai_service.py`) has been introduced for AI provider abstraction, now including `model` in `__init__`.
  - `GeminiService` has been moved to `fml/ai_providers/gemini_service.py` and now inherits from `AIService`, accepting a `model` parameter.
  - A new `fml/schemas.py` module defines the AI response structure using Pydantic models for robust validation.
  - A new `fml/output_formatter.py` module handles the formatting and display of AI responses.
- **Dynamic AI Service and Model Selection (Task 017 & 026):**
  - Implemented CLI argument `-m` or `--model` in `fml/__main__.py` for dynamic model selection.
  - A `MODELS` dictionary in `fml/ai_providers/models.py` now serves as the central registry for model metadata (provider module, service class, env var, prompt details).
  - Logic in `fml/__main__.py` dynamically imports AI service classes and retrieves prompt content based on this metadata, preventing unnecessary imports at startup.
  - `get_supported_models()` method has been removed from `AIService` and `GeminiService`.
- **Refactor `main()` function (Task 018 - Part 1):**
  - Extracted AI service initialization logic into a new `_initialize_ai_service` helper function in `fml/__main__.py`.
- **Clipboard Integration (Task 005):**
  - The `pyperclip` library has been added as a dependency.
  - Logic has been implemented in `fml/__main__.py` to copy the generated command to the system clipboard and display a confirmation message.
- **Test Clipboard Integration (Task 015):**
  - A new test file `tests/test_clipboard.py` has been created.
  - Tests have been implemented using `pytest`'s `monkeypatch` and `capsys` fixtures to mock `pyperclip.copy()` and verify the confirmation message.
- **Error Handling & Refinement (Task 006):**
  - Centralized common error handling for AI service interactions in the `AIService` abstract base class (`fml/ai_service.py`), catching `requests.exceptions.ConnectionError` and `pydantic.ValidationError`.
  - Introduced `AIServiceError` custom exception for consistent error reporting.
  - Modified `GeminiService` (`fml/ai_providers/gemini_service.py`) to implement `_generate_command_internal` and specifically handle `google.genai.errors.APIError`, relying on the base class for common error handling.
  - Updated `fml/__main__.py` to catch `AIServiceError` for user-friendly error messages.
- **Enhanced LLM Context with System Information (Task 025 & 028):**
  - Defined `SystemInfo` and `AIContext` Pydantic models in `fml/schemas.py`.
  - Created `fml/gather_system_info.py` with `get_system_info()` to collect system details.
  - **Improved Windows Shell Detection (Task 028):** The `get_system_info()` function in `fml/gather_system_info.py` has been refined to accurately identify the active shell on Windows. It now prioritizes the `SHELL` environment variable, then checks for PowerShell via `PSModulePath`, and defaults to `unknown_shell` if neither is found, aligning with the project's requirements to not support `cmd.exe`.
  - Modified `fml/ai_service.py` and `fml/ai_providers/gemini_service.py` to accept and pass `AIContext` to the AI model.
  - Updated `fml/__main__.py` to gather system info, create `AIContext`, and pass it to `generate_command()`.
  - Modified `fml/prompts/gemini_system_prompt.txt` to instruct the AI on using system context.
  - Created `tests/test_gather_system_info.py` with `pytest` unit tests for `get_system_info()`, including mocking `platform` and `os` calls for various environments.
- **Prompt Loading from Modules:**
  - Renamed `fml/prompts/gemini_system_prompt.txt` to `fml/prompts/gemini_system_prompt.py`.
  - Converted the content of `fml/prompts/gemini_system_prompt.py` into a multiline string variable `GEMINI_SYSTEM_PROMPT`.
  - Updated `fml/ai_providers/models.py` to include `prompt_module` and `prompt_variable` fields in `ModelProviderDetails` and updated the `MODELS` dictionary accordingly.
  - Modified `fml/__main__.py` to dynamically import the prompt module and retrieve the prompt string, passing it directly to the AI service.
  - Updated `fml/ai_service.py` and `fml/ai_providers/gemini_service.py` to accept `system_instruction_content` instead of `system_instruction_path`.

## 3. Next Steps

The immediate next steps involve:

- Cross-platform testing (Task 007).
- Integration tests (Task 016).

## 4. Active Decisions and Considerations

- **AI Output Structure:** Strict adherence to the defined JSON structure for AI responses is critical for reliable parsing, now enforced by Pydantic schemas. Robust error handling for malformed responses remains a priority.
- **Cross-Platform Compatibility:** All features, especially clipboard integration, must be tested and verified across macOS, Windows, and Linux.
- **Modularity:** The successful implementation of dynamic AI service and model selection further reinforces the commitment to a modular architecture, facilitating future enhancements and alternative AI providers.
- **Prompt Engineering:** The initial system prompt for Gemini remains crucial for consistent and accurate command generation. This will continue to be an iterative process.

## 5. Important Patterns and Preferences

- **Environment Variables for API Keys:** API keys (e.g., `GEMINI_API_KEY`) are now dynamically determined based on the selected AI service.
- **Python Standard Libraries:** Prioritizing `argparse` for CLI parsing.
- **External Libraries:** `google.genai` (the new SDK), `pyperclip` (pending re-integration), and `pydantic` are the primary external dependencies for MVP.

## 6. Learnings and Project Insights

- The project's success heavily relies on the AI's ability to consistently provide structured and accurate command information, now significantly improved by Pydantic schema enforcement.
- Cross-platform compatibility, particularly for clipboard operations, requires careful attention to potential system-level dependencies.
- A clear, modular architecture, now largely implemented for the core AI interaction and dynamic selection, is key to future extensibility, especially for adding new AI providers or a TUI.
- The iterative process of refactoring and testing is crucial for maintaining code health and addressing issues promptly.
- **Google Gemini SDK (`google-generativeai`) Learnings:**
  - The `APIError` exception is found in `google.genai.errors`, not `google.genai.types`.
  - When mocking `APIError` for testing, its constructor expects the error message as a positional argument and `response_json` as a keyword argument (e.g., `APIError("message", response_json={...})`).
  - When mocking `google.genai.Client` using `unittest.mock.patch` in `pytest` fixtures, the fixture should yield the patched class (`mock_client_class`). Test functions should then access the mock instance via `mock_client_class.return_value` to interact with its methods (e.g., `mock_client_instance.models.generate_content`).
