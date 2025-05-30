# Active Context: `fml` - AI-Powered CLI Command Helper

## 1. Current Work Focus

The current focus is on initializing the project and setting up the foundational components as outlined in the MVP (Minimum Viable Product) phase of the PRD. This includes establishing the project structure, implementing CLI argument parsing, integrating with the Google Gemini API, handling API key management, parsing AI responses, displaying output, and integrating with the system clipboard.

## 2. Recent Changes

- Initial memory bank files (`projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`) have been created based on the `prd.md`.

## 3. Next Steps

The immediate next steps involve:
- Creating the `progress.md` file to track task progress.
- Generating individual task files (`tasks/task_XXX.txt`) based on the MVP milestones defined in the PRD.
- Setting up the Python project environment (e.g., `uv init`).
- Implementing CLI argument parsing.
- Implementing API key management.
- Integrating with the Google Gemini API.
- Developing response parsing and terminal display logic.
- Integrating clipboard functionality.

## 4. Active Decisions and Considerations

- **AI Output Structure:** Strict adherence to the defined JSON structure for AI responses is critical for reliable parsing. Robust error handling for malformed responses is a priority.
- **Cross-Platform Compatibility:** All features, especially clipboard integration, must be tested and verified across macOS, Windows, and Linux.
- **Modularity:** Maintaining the separation of concerns (core logic vs. presentation, AI abstraction) from the outset to facilitate future enhancements.
- **Prompt Engineering:** The initial system prompt for Gemini will be crucial for consistent and accurate command generation. This will be an iterative process.

## 5. Important Patterns and Preferences

- **Environment Variables for API Keys:** `GEMINI_API_KEY` will be used for secure API key management.
- **Python Standard Libraries:** Prioritizing `argparse` for CLI parsing.
- **External Libraries:** `google-generativeai` and `pyperclip` are the primary external dependencies for MVP.

## 6. Learnings and Project Insights

- The project's success heavily relies on the AI's ability to consistently provide structured and accurate command information.
- Cross-platform compatibility, particularly for clipboard operations, requires careful attention to potential system-level dependencies.
- A clear, modular architecture will be key to future extensibility, especially for adding new AI providers or a TUI.
