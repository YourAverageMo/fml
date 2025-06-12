<!-- omit in toc -->
# fml: AI-Powered CLI Command Helper

- [Introduction](#introduction)
- [Usage](#usage)
- [Features](#features)
- [Installation](#installation)
- [Supported AI Models](#supported-ai-models)
- [Contribute](#contribute)

## Introduction

FML (forgot my line) terminal AI to help you remember cli commands and flags.

Addresses the common challenges faced by technical users, such as remembering complex CLI commands, understanding their flags and options, and the constant interruption of searching documentation. By leveraging an AI model, `fml` provides quick, accurate command suggestions, explains their purpose, breaks down their components, and automatically copies the command to your clipboard, allowing you to stay focused in your terminal environment.

## Usage

Here are some examples of how to use `fml`:

```bash
$ fml 'how do I list all running docker containers, dont truncated, and show total file size?'
```

```bash
$ fml 'how do i rename the previous commit message'
```

> [!NOTE] It is recommended to wrap query in single quotes to prevent shell expansion (unless thats what you want).

`fml` is a simple tool to help you remember computer commands. You ask it a question, and it gives you the command you need, along with what it does and what its parts mean. _think tldr but with AI_

**What `fml` IS:**

- A quick way to get a command you forgot.
- A helper to understand command parts (like flags).
- A tool to copy commands right to your clipboard.

**What `fml` IS NOT:**

- A chatbot for talking.
- A tool to run commands for you.

## Features

- **Automatic Clipboard Integration:** The generated command is automatically copied to your system clipboard, ready for immediate pasting and execution.
  > [!NOTE] Note for Linux users: This feature requires `xclip` or `xsel` to be installed on your system.
- **AI Model Selection:** While currently supporting Google Gemini, `fml` is built with a modular architecture that allows for easy integration of future AI providers.
- **User-Friendly Terminal Output:** Commands and explanations are displayed in a clean, readable format directly in your terminal, with with optional color output for enhanced clarity.
- **System Context Awareness:** `fml` gathers essential system information (operating system, current working directory, architecture, python version, and shell. see @gather_system_info.py) and provides it to the AI. This helps the AI generate more accurate and contextually relevant commands tailored to your specific environment.

## Installation

**Requirements**

- Python 3.8+
- `uv` (recommended for installation and dependency management)
- An API key for your chosen AI model (e.g., `GEMINI_API_KEY` for Google Gemini), set as an environment variable.
- For Linux users, `xclip` or `xsel` is required for clipboard functionality.

`fml` is designed for easy installation using `uv`, the recommended and officially supported method. If you don't have [uv](https://github.com/astral-sh/uv) get it... seriously. While other tools like `pipx` might function, they are not officially supported. For reference, `fml` is registered on PyPI as 'fml-ai'.

To install `fml`, use the following command:

```bash
uv tool install fml-ai
```

You can also try out `fml` temporarily via uv without installing:

```bash
uv tool fml-ai
```

## Supported AI Models

`fml` currently supports the following Google Gemini models:

- `gemini-2.5-flash-preview-05-20` (default)
- `gemini-2.0-flash`
- `gemini-2.0-flash-lite`
- `gemini-1.5-flash`

**Important:** You need to provide your own API key for the selected AI model as an environment variable (e.g., `GEMINI_API_KEY` for Google Gemini).

The application's modular architecture is designed for extensibility, allowing for seamless integration of other AI providers (such as OpenAI or local Ollama models) in future enhancements.

## Contribute

If you got a fix in mind or feel like you could improve upon this project feel free to make a fork of this repo, create a new branch, and submit a pull request. As long as the code is well documented and readable, I'd love to see it through!
