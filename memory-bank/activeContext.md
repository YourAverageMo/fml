# Active Context: `fml` - AI-Powered CLI Command Helper

## 1. Current Work Focus

The current focus has shifted to refactoring and modularizing the core application logic, specifically the AI service integration and response handling, to improve extensibility and maintainability. The next immediate step is to re-integrate clipboard functionality and then proceed with testing.

## 2. Recent Changes

- Initial memory bank files (`projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `activeContext.md`, `progress.md`) have been created based on the `prd.md`.
- The Python project environment has been initialized using `uv init`.
- The main application entry point (`fml.py`) has been created with basic CLI argument parsing implemented (Task 001 completed).
- All MVP development tasks (Task 001-007) have been created and added to the task queue.
- The project changes have been committed and merged to `main`.
- A new branch `add/tests` has been created for testing efforts.
- **Refactoring & Modularization:**
  - An `AIService` abstract base class (`fml/ai_service.py`) has been introduced for AI provider abstraction.
  - `GeminiService` has been moved to `fml/ai_providers/gemini_service.py` and now inherits from `AIService`.
  - A new `fml/schemas.py` module defines the AI response structure using Pydantic models for robust validation.
  - A new `fml/output_formatter.py` module handles the formatting and display of AI responses.

## 3. Next Steps

The immediate next steps involve:

- Planning out the testing tasks for the project.
- Creating individual task files for testing.
- Updating `progress.md` with the new testing tasks.
- Implementing tests for existing functionalities, starting with CLI parsing and API key management.

## 4. Active Decisions and Considerations

- **AI Output Structure:** Strict adherence to the defined JSON structure for AI responses is critical for reliable parsing, now enforced by Pydantic schemas. Robust error handling for malformed responses remains a priority.
- **Cross-Platform Compatibility:** All features, especially clipboard integration, must be tested and verified across macOS, Windows, and Linux.
- **Modularity:** The successful implementation of AI service abstraction and separate output formatting reinforces the commitment to a modular architecture, facilitating future enhancements and alternative AI providers.
- **Prompt Engineering:** The initial system prompt for Gemini remains crucial for consistent and accurate command generation. This will continue to be an iterative process.

## 5. Important Patterns and Preferences

- **Environment Variables for API Keys:** `GEMINI_API_KEY` will be used for secure API key management.
- **Python Standard Libraries:** Prioritizing `argparse` for CLI parsing.
- **External Libraries:** `google.genai` (the new SDK), `pyperclip` (to be re-added), and `pydantic` are the primary external dependencies for MVP.

## 6. Learnings and Project Insights

- The project's success heavily relies on the AI's ability to consistently provide structured and accurate command information, now significantly improved by Pydantic schema enforcement.
- Cross-platform compatibility, particularly for clipboard operations, requires careful attention to potential system-level dependencies.
- A clear, modular architecture, now largely implemented for the core AI interaction, is key to future extensibility, especially for adding new AI providers or a TUI.
- The iterative process of refactoring and testing is crucial for maintaining code health and addressing issues promptly.
