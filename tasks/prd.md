# Product Requirements Document: `fml` - AI-Powered CLI Command Helper

## 1. Introduction & App Overview

**App Name:** `fml`

**Concept:** `fml` is a lightweight, terminal-based Python application designed to help users remember and craft command-line interface (CLI) commands for various tools (e.g., Docker, FFmpeg, Git). Users will input a natural language query, and `fml` will leverage an AI model (initially Google Gemini) to provide the relevant command, an explanation, a breakdown of flags, and automatically copy the command to the clipboard.

**Objectives:**

- Provide quick and accurate CLI command suggestions based on natural language queries.
- Explain the generated command and its components (flags/options) clearly.
- Streamline the user's workflow by copying the command directly to the clipboard.
- Be easily invokable from the terminal.
- Maintain a modular architecture to allow for future AI provider flexibility and feature enhancements (like a TUI).

## 2. Target Audience

- **Primary:** Technical users who frequently interact with CLIs (e.g., software developers, DevOps engineers, system administrators, data scientists).
- **Context:** This is initially a hobby project, so the primary user and tester will be the developer themself.

## 3. Core Features & Functionality (Minimum Viable Product - MVP)

The MVP will focus on delivering the core command generation and explanation capabilities.

### 3.1. User Input via CLI Argument

- **Description:** Users will invoke the application from their terminal using the command `fml` followed by their natural language query in quotes.
- **Example:** `fml how do i view the git diff for my current branch compared to main?`
- **Acceptance Criteria:**
  - The application correctly captures the full query string provided as an argument.
  - Quotes should not be required for the query
  - If no query is provided, a helpful usage message is displayed.

### 3.2. AI Interaction (Google Gemini)

- **Description:** The application will send the user's query to the Google Gemini API to generate the command and explanation.
- **Acceptance Criteria:**
  - The application successfully authenticates and communicates with the Gemini API.
  - The user's query is correctly transmitted to the AI.
  - The application handles potential API errors (e.g., network issues, authentication failure, rate limits) gracefully by informing the user.

### 3.3. Structured AI Response Generation & Parsing

- **Description:** The AI (Gemini) will be prompted to return a structured response (ideally JSON) containing the command, a brief explanation, and a breakdown of flags. The application will parse this response.
- **Desired AI Output Structure (conceptual JSON):**
  ```json
  {
    "explanation": "A 2-3 sentence explanation of what the command does.",
    "flags": [
      {
        "flag": "--flag1",
        "description": "Short definition of what flag1 does."
      },
      { "flag": "-f2", "description": "Short definition of what f2 does." }
    ],
    "command": "the full complete_command --flag1 -f2"
  }
  ```
- **Acceptance Criteria:**
  - The application can parse the structured response from the AI.
  - If the AI response is not in the expected format or is missing key information, the application informs the user of the issue.

### 3.4. Terminal Display

- **Description:** The parsed information from the AI will be displayed in a clean, readable format in the terminal.
- **Format:**
  1.  Brief 2-3 sentence explanation.
  2.  Line break.
  3.  Each flag and its description on a new line.
  4.  The full, complete command on its own line.
- **Acceptance Criteria:**
  - Output matches the specified format.
  - Text is easily readable in standard terminal emulators.

### 3.5. Clipboard Integration

- **Description:** The generated full command string will be automatically copied to the user's system clipboard.
- **Acceptance Criteria:**
  - The command is successfully copied to the clipboard on macOS, Windows, and Linux.
  - A confirmation message (e.g., "(command copied to clipboard)") is displayed after the command.

### 3.6. API Key Management

- **Description:** The Google Gemini API key will be accessed via an environment variable.
- **Acceptance Criteria:**
  - The application looks for a predefined environment variable (e.g., `GEMINI_API_KEY`).
  - If the environment variable is not set, the application displays a clear error message instructing the user on how to set it.

### 3.7. Cross-Platform Support

- **Description:** The application should function correctly on macOS, Windows.
- **Acceptance Criteria:**
  - All core features work as expected on these platforms.
  - Installation and execution are straightforward on each platform.

## 4. Technical Stack & Architecture Recommendations

- **Programming Language:** Python (version 3.8+)
- **AI Service Integration:**
  - **Initial:** Google Gemini, using the official `google-generativeai` Python SDK.
  - **Modularity:** Wrap AI interaction logic in an abstraction layer (e.g., an `AIService` class or interface) to simplify switching to other providers (OpenAI, Ollama) in the future. The Gemini implementation would be the first concrete class.
- **Command-Line Argument Parsing:** Python's built-in `argparse` module.
- **Clipboard Access:** `pyperclip` library (cross-platform).
- **API Key Management:** Read from environment variables (e.g., using Python's `os.environ`).
- **Code Structure for Future TUI:**
  - Separate core logic (AI interaction, command processing, business rules) from the presentation layer.
  - Initially, the presentation layer will be simple `print()` statements. This should be easily replaceable with a TUI library component later.
- **Potential TUI Libraries (for future consideration):** `Textual` or `prompt_toolkit`.

## 5. Prompt Engineering Guidance for LLM (Gemini)

This section is to guide an LLM (or a developer working with an LLM) in crafting the system prompt for Google Gemini to elicit the desired structured output.

- **Overall Goal:** Obtain a JSON object containing an explanation, a list of flags with their descriptions, and the complete command string.
- **Key Instructions for the System Prompt:**
  1.  **Role Definition:** "You are a helpful and concise AI assistant specializing in generating and explaining command-line interface (CLI) commands for various tools like git, docker, ffmpeg, etc."
  2.  **Task Specification:** "Based on the user's query, generate the most relevant CLI command. Provide a brief explanation of what the command does, a breakdown of each flag or option used, and the complete command itself."
  3.  **Output Format Mandate:** "Your response MUST be a single, valid JSON object. Do NOT include any text outside of this JSON object, including backticks or markdown formatting around the JSON."
  4.  **JSON Structure Definition:**
      - "The JSON object must have the following top-level keys: `explanation` (string), `flags` (array of objects), and `command` (string)."
      - "`explanation`: A clear, concise explanation of the command's purpose, limited to 2-3 sentences."
      - "`flags`: An array where each object represents a flag or option used in the command. Each object in this array must have two keys: `flag` (string, e.g., '--verbose' or '-v') and `description` (string, a brief definition of what the flag does)."
      - "`command`: The full, complete command string that the user can copy and paste."
  5.  **Content Guidelines:**
      - "Prioritize accuracy and common usage for the CLI tool mentioned or inferred from the query."
      - "Be concise in explanations and flag descriptions."
      - "If a command doesn't typically use flags for the described action, the `flags` array can be empty."
      - "If the user's query is ambiguous or a command cannot be reasonably constructed, the `explanation` should state this, and the `command` can be an empty string or a relevant help command (e.g., `git --help`)."
- **Example of desired JSON output (to be included in prompt if helpful, or as a reference):**
  ```json
  {
    "explanation": "This command shows the differences between your current branch and the 'main' branch in git.",
    "flags": [
      {
        "flag": "diff",
        "description": "The git subcommand to show changes between commits, commit and working tree, etc."
      },
      {
        "flag": "main",
        "description": "The branch to compare against the current branch."
      }
    ],
    "command": "git diff main"
  }
  ```
- **Iteration Note:** Prompt engineering is iterative. Test the prompt with various queries and refine it to improve consistency and accuracy of the JSON output.

## 6. Conceptual Data Model (for AI Output)

This refers to the structure of the data expected from the AI and used within the application. It mirrors the JSON structure defined in section 5.

- **Main Object:**
  - `explanation`: String
  - `flags`: List of Flag Objects
    - `flag`: String
    - `description`: String
  - `command`: String

## 7. UI/UX Design Principles (MVP)

- **Interaction Model:** Command-line driven (`fml "query"`).
- **Output:** Clear, legible, and structured text output directly in the terminal.
- **Feedback:** Provide essential feedback like "Command copied to clipboard" or clear error messages.
- **Simplicity:** Avoid unnecessary complexity in the terminal output for V1.

## 8. Security Considerations

- **API Keys:** The Google Gemini API key must be handled securely. Storing it in an environment variable is the recommended approach for this local application. The application code should not log or expose the API key.
- **No Sensitive Data:** The application itself will not store any user data or history in the MVP.
- **Command Execution (Future):** If direct command execution in a subshell is implemented later, extreme care must be taken to prevent command injection vulnerabilities. This is not part of the MVP.

## 9. Development Phases/Milestones (Conceptual)

### Phase 1: MVP - Core Functionality

1.  **Setup & CLI Parsing:**
    - Initialize Python project (`uv init` or `python -m venv`).
    - Implement CLI argument parsing for `fml "query"` using `argparse`.
2.  **API Key & Basic Config:**
    - Implement logic to read `GEMINI_API_KEY` from environment variables.
    - Add error handling for missing API key.
3.  **Gemini API Integration:**
    - Install `google-generativeai` SDK.
    - Implement function to send a query to Gemini and retrieve the response.
    - Develop initial system prompt (see Section 5).
4.  **Response Parsing & Display:**
    - Implement logic to parse the expected JSON response from Gemini.
    - Implement logic to format and print the explanation, flags, and command to the terminal as specified.
5.  **Clipboard Integration:**
    - Install `pyperclip`.
    - Implement logic to copy the generated command to the clipboard.
    - Add "command copied" confirmation message.
6.  **Error Handling & Refinement:**
    - Implement basic error handling for API calls (e.g., network, authentication).
    - Test with various queries and refine prompt/parsing as needed.
7.  **Cross-Platform Testing:**
    - Test basic functionality on macOS, Windows, and Linux.

### Phase 2: Post-MVP Enhancements (Future Considerations)

- **Multi-turn Chat for Revisions:**
  - Allow follow-up prompts to refine the last generated command.
  - Manage conversation history for context.
- **Subshell Command Execution:**
  - Add an option to directly execute the generated command in a subshell (with appropriate security warnings).
- **Packaging & Distribution:**
  - Package the tool using `uv` or standard Python packaging tools (setuptools, build) for easier distribution/installation (e.g., via PyPI).
- **Terminal User Interface (TUI):**
  - Explore and implement a TUI using libraries like `Textual` for a richer interactive experience (e.g., navigable history, better layout for complex commands, interactive refinement).
- **Support for Other AI Providers:**
  - Refactor AI service interaction to use the abstraction layer.
  - Implement support for other models/providers (e.g., OpenAI API, local Ollama models).

## 10. Potential Challenges & Solutions

- **Prompt Engineering Consistency:**
  - **Challenge:** Ensuring Gemini consistently returns valid, structured JSON.
  - **Solution:** Iterative refinement of the system prompt. Explicitly requesting JSON. Robust parsing with error handling for unexpected formats.
- **Cross-Platform Clipboard Issues:**
  - **Challenge:** `pyperclip` might have dependencies (e.g., `xclip`/`xsel` on Linux) that need to be installed.
  - **Solution:** Document dependencies clearly. Test thoroughly on all target platforms.
- **API Rate Limits/Costs:**
  - **Challenge:** Exceeding free tier limits or incurring unexpected costs with the Gemini API.
  - **Solution:** Monitor usage. Implement retries with backoff for rate limit errors. Inform users about potential API key requirements and associated costs.
- **Handling Diverse CLI Tools:**
  - **Challenge:** The AI might not be equally proficient with all CLI tools or complex/niche scenarios.
  - **Solution:** Focus prompt on common tools. Acknowledge limitations. The iterative nature of multi-turn chat (future) could help refine commands for less common tools.

## 11. Future Expansion Possibilities

- User-configurable AI provider and model choice.
- Saving frequently used or favorited commands (would require local storage).
- Integration with shell history for context.
- Ability to define custom command templates or snippets.
- Community sharing of useful `fml` prompts or generated commands.
