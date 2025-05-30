# System Patterns: `fml` - AI-Powered CLI Command Helper

## 1. System Architecture

The `fml` application will follow a modular architecture, separating concerns to allow for flexibility and future enhancements.

```mermaid
graph TD
    A[User Input (CLI)] --> B{CLI Parser (argparse)}
    B --> C[Core Logic]
    C --> D{AI Service Abstraction}
    D --> E[Google Gemini Implementation]
    E --> F[Gemini API]
    F --> D
    D --> G[Response Parser]
    G --> H[Presentation Layer (Terminal Display)]
    G --> I[Clipboard Integration (pyperclip)]
```

## 2. Key Technical Decisions

- **Modularity for AI Services:** AI interaction logic will be wrapped in an abstraction layer (e.g., an `AIService` class or interface). This design choice simplifies switching to other AI providers (OpenAI, Ollama) in the future without significant refactoring of the core application logic.
- **Structured AI Response:** The AI will be prompted to return a structured JSON response. This ensures reliable parsing and extraction of command, explanation, and flag details. Robust error handling will be implemented for malformed or missing AI responses.
- **Separation of Core Logic and Presentation:** The core logic (AI interaction, command processing, business rules) will be distinct from the presentation layer (terminal output). This facilitates future integration with a Terminal User Interface (TUI) without rewriting the core functionality.

## 3. Design Patterns in Use

- **Abstraction Layer:** For AI service integration, allowing different AI providers to be plugged in without changing the core application.
- **Command Pattern (Implicit):** The application essentially acts as a command generator based on user input.
- **Parser Pattern:** For interpreting the structured JSON response from the AI.

## 4. Component Relationships

- **CLI Parser (`argparse`):** Responsible for capturing user queries from the command line.
- **Core Logic:** Orchestrates the flow, calling the AI service, parsing its response, and directing output to the presentation and clipboard layers.
- **AI Service Abstraction:** Defines the interface for interacting with AI models.
- **Google Gemini Implementation:** Concrete implementation of the `AIService` interface for Google Gemini.
- **Response Parser:** Extracts and validates data from the AI's structured output.
- **Presentation Layer:** Formats and displays the command information to the user in the terminal.
- **Clipboard Integration (`pyperclip`):** Handles copying the generated command to the system clipboard.

## 5. Critical Implementation Paths

- **End-to-End Flow:** User query -> CLI parsing -> AI request -> AI response -> Response parsing -> Terminal display & Clipboard copy. This path must be robust and error-tolerant.
- **API Key Management:** Secure and reliable access to the `GEMINI_API_KEY` environment variable is crucial for application functionality. Clear error messages for missing keys are essential.
- **Cross-Platform Compatibility:** Ensuring `pyperclip` and general Python execution work seamlessly across macOS, Windows, and Linux.
