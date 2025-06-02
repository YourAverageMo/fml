# System Patterns: `fml` - AI-Powered CLI Command Helper

## 1. System Architecture

The `fml` application will follow a modular architecture, separating concerns to allow for flexibility and future enhancements.

```mermaid
graph TD
    A[User Input (CLI)] --> B{CLI Parser (argparse)}
    B --> C[Core Logic]
    C --> D{AI Service Abstraction (fml/ai_service.py)}
    D --> E[AI Provider Implementations (fml/ai_providers/)]
    E --> F[Google Gemini Implementation (fml/ai_providers/gemini_service.py)]
    F --> G[Gemini API]
    G --> E
    E --> D
    D --> H[AI Command Response (fml/schemas.py)]
    H --> I[Output Formatter (fml/output_formatter.py)]
    I --> J[Presentation Layer (Terminal Display)]
    I --> K[Clipboard Integration (pyperclip)]
```

## 2. Key Technical Decisions

- **Modularity for AI Services:** AI interaction logic is wrapped in an `AIService` abstract base class. Concrete implementations (e.g., `GeminiService`) reside in `fml/ai_providers/`, simplifying switching to other AI providers (OpenAI, Ollama) without significant refactoring of the core application logic.
- **Structured AI Response with Pydantic:** The AI is prompted to return a structured JSON response, now strictly enforced and validated using `pydantic` models defined in `fml/schemas.py`. This ensures reliable parsing and extraction of command, explanation, and flag details. Robust error handling is implemented for malformed or missing AI responses.
- **Separation of Core Logic and Presentation:** The core logic (AI interaction, command processing, business rules) is distinct from the presentation layer (terminal output), now handled by `fml/output_formatter.py`. This facilitates future integration with a Terminal User Interface (TUI) without rewriting the core functionality.

## 3. Design Patterns in Use

- **Abstraction Layer:** For AI service integration, allowing different AI providers to be plugged in without changing the core application.
- **Command Pattern (Implicit):** The application essentially acts as a command generator based on user input.
- **Parser Pattern:** For interpreting the structured JSON response from the AI.

## 4. Component Relationships

- **CLI Parser (`argparse`):** Responsible for capturing user queries from the command line.
- **Core Logic:** Orchestrates the flow, calling the AI service, parsing its response, and directing output to the presentation and clipboard layers.
- **AI Service Abstraction (`fml/ai_service.py`):** Defines the abstract interface for interacting with AI models.
- **AI Provider Implementations (`fml/ai_providers/`):** Contains concrete implementations of `AIService` for specific AI providers (e.g., `GeminiService`).
- **AI Command Response (`fml/schemas.py`):** Defines the `pydantic` data model for the structured AI output, ensuring type safety and validation.
- **Output Formatter (`fml/output_formatter.py`):** Formats the `AICommandResponse` object into a human-readable string for terminal display.
- **Presentation Layer:** Formats and displays the command information to the user in the terminal.
- **Clipboard Integration (`pyperclip`):** Handles copying the generated command to the system clipboard (to be re-added in a future task).

## 5. Critical Implementation Paths

- **End-to-End Flow:** User query -> CLI parsing -> AI request -> AI response -> Response parsing -> Terminal display & Clipboard copy. This path must be robust and error-tolerant.
- **API Key Management:** Secure and reliable access to the `GEMINI_API_KEY` environment variable is crucial for application functionality. Clear error messages for missing keys are essential.
- **Cross-Platform Compatibility:** Ensuring `pyperclip` and general Python execution work seamlessly across macOS, Windows, and Linux.
