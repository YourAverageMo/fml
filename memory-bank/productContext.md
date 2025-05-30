# Product Context: `fml` - AI-Powered CLI Command Helper

## 1. Why this project exists

`fml` aims to solve the common problem faced by technical users: remembering and correctly crafting CLI commands for various tools. It streamlines the workflow by providing quick, accurate suggestions and automatically copying the command to the clipboard, reducing the need to search documentation or recall complex syntax.

## 2. Problems it solves

- **Command Recall:** Users often forget specific CLI commands or their exact syntax.
- **Flag/Option Confusion:** Difficulty remembering the correct flags and their purposes for a given command.
- **Workflow Interruption:** The need to switch context to search for commands, breaking the flow of work in the terminal.
- **Cross-Platform Consistency:** Ensuring commands work similarly across different operating systems.

## 3. How it should work

Users will invoke `fml` from their terminal with a natural language query. The application will send this query to an AI model (initially Google Gemini), which will return a structured response containing the command, an explanation, and a breakdown of flags. This information will be displayed clearly in the terminal, and the command will be automatically copied to the clipboard.

## 4. User experience goals

- **Efficiency:** Users should get the command they need quickly and with minimal effort.
- **Clarity:** The explanation and flag breakdown should be easy to understand, even for complex commands.
- **Seamless Integration:** The tool should feel like a natural extension of the terminal environment.
- **Reliability:** The AI should consistently provide accurate and relevant commands.
