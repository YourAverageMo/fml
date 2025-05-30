# Project Brief: `fml` - AI-Powered CLI Command Helper

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
