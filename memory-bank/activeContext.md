# Active Context: `fml` - AI-Powered CLI Command Helper

## 1. Current Work Focus

The current focus is on refactoring the `main()` function in `fml/__main__.py` by extracting the AI service initialization logic into a dedicated helper function `_initialize_ai_service` (Task 018). This builds upon the dynamic AI service and model selection implemented in Task 017. The next immediate step after this is to re-integrate clipboard functionality and then proceed with testing.

## 2. Recent Changes

- Initial memory bank files (`projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `activeContext.md`, `progress.md`) have been created based on the `prd.md`.
- The Python project environment has been initialized using `uv init`.
- The main application entry point (`fml.py`) has been created with basic CLI argument parsing implemented (Task 001 completed).
- All MVP development tasks (Task 001-007) have been created and added to the task queue.
- The project changes have been committed and merged to `main`.
- A new branch `add/tests` has been created for testing efforts.
- **Refactoring & Modularization:**
  - An `AIService` abstract base class (`fml/ai_service.py`) has been introduced for AI provider abstraction, now including `model` in `__init__` and an abstract `get_supported_models()` method.
  - `GeminiService` has been moved to `fml/ai_providers/gemini_service.py` and now inherits from `AIService`, accepting a `model` parameter and defining supported models via `GeminiModels` enum.
  - A new `fml/schemas.py` module defines the AI response structure using Pydantic models for robust validation.
  - A new `fml/output_formatter.py` module handles the formatting and display of AI responses.
- **Dynamic AI Service and Model Selection (Task 017):**
  - Implemented CLI argument `-m` or `--model` in `fml/__main__.py` for dynamic model selection.
  - Logic added to `fml/__main__.py` to dynamically select and instantiate the correct AI service based on the provided model name, and to determine the appropriate API key and system prompt path.
- **Refactor `main()` function (Task 018 - Part 1):**
  - Extracted AI service initialization logic into a new `_initialize_ai_service` helper function in `fml/__main__.py`.

## 3. Next Steps

The immediate next steps involve:

- Completing the refactoring of the `main()` function (Task 018 - remaining parts).
- Re-integrating clipboard functionality (Task 005).
- Planning out the remaining testing tasks for the project.
- Creating individual task files for testing.
- Updating `progress.md` with the new testing tasks.
- Implementing tests for existing functionalities, starting with CLI parsing and API key management.

## 4. Active Decisions and Considerations

- **AI Output Structure:** Strict adherence to the defined JSON structure for AI responses is critical for reliable parsing, now enforced by Pydantic schemas. Robust error handling for malformed responses remains a priority.
- **Cross-Platform Compatibility:** All features, especially clipboard integration, must be tested and verified across macOS, Windows, and Linux.
- **Modularity:** The successful implementation of dynamic AI service and model selection further reinforces the commitment to a modular architecture, facilitating future enhancements and alternative AI providers.
- **Prompt Engineering:** The initial system prompt for Gemini remains crucial for consistent and accurate command generation. This will continue to be an iterative process.

## 5. Important Patterns and Preferences

- **Environment Variables for API Keys:** API keys (e.g., `GEMINI_API_KEY`) are now dynamically determined based on the selected AI service.
- **Python Standard Libraries:** Prioritizing `argparse` for CLI parsing.
- **External Libraries:** `google.genai` (the new SDK), `pyperclip` (to be re-added), and `pydantic` are the primary external dependencies for MVP.

## 6. Learnings and Project Insights

- The project's success heavily relies on the AI's ability to consistently provide structured and accurate command information, now significantly improved by Pydantic schema enforcement.
- Cross-platform compatibility, particularly for clipboard operations, requires careful attention to potential system-level dependencies.
- A clear, modular architecture, now largely implemented for the core AI interaction and dynamic selection, is key to future extensibility, especially for adding new AI providers or a TUI.
- The iterative process of refactoring and testing is crucial for maintaining code health and addressing issues promptly.
