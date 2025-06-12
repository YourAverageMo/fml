# Project Title
<!-- Note for LLM: Use "fml: AI-Powered CLI Command Helper" as the main title. -->

## Tagline
<!-- Note for LLM: Use "AI-Powered CLI Command Helper" as the tagline. -->

## Introduction
<!-- Note for LLM: Emphasize why fml exists, the problems it solves (command recall, flag confusion, workflow interruption), and how it works (natural language query -> AI -> structured response -> terminal display + clipboard). Maintain a formal, technical tone. -->

## Features
<!-- Note for LLM: List core MVP features from PRD. Group them logically if possible (e.g., Core Functionality, User Experience). Highlight:
- AI-powered command generation (explanation, flags, command)
- Automatic clipboard integration (mention Linux dependency: requires xclip or xsel)
- AI model selection
- User-friendly terminal output (with optional color)
-->

## Installation
<!-- Note for LLM:
- Recommended and only officially supported method is `uv`.
- Provide commands:
  - `uv tool install fml-ai` for installation.
  - `uv tool fml-ai` to try it out without full installation.
- Mention that other methods like `pipx` might function but are not officially supported.
-->

## Usage
<!-- Note for LLM:
- Provide 2 real-world Docker examples that showcase flags being broken down.
- Example structure:
  ```bash
  $ fml "your query"
  ```
  Followed by the expected output format (explanation, flags, command).
- Do not include `--no-color` argument in examples.
- Consider adding a GIF demonstrating usage.
-->

## Supported AI Models
<!-- Note for LLM:
- Explicitly state that only Google Gemini is currently supported.
- Mention that the modular architecture allows for easy integration of future AI providers (e.g., OpenAI, Ollama).
-->
