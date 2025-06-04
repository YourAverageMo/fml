from pydantic import BaseModel, Field
from typing import List, Optional


class Flag(BaseModel):
    flag: str = Field(
        ...,
        description="The flag or option used in the command (e.g., '--verbose' or '-v').",
    )
    description: str = Field(
        ..., description="A brief definition of what the flag does."
    )


class AICommandResponse(BaseModel):
    explanation: str = Field(
        ...,
        description="A clear, concise explanation of the command's purpose, limited to 2-3 sentences.",
    )
    flags: List[Flag] = Field(
        ...,
        description="An array where each object represents a flag or option used in the command.",
    )
    command: str = Field(
        ...,
        description="The full, complete command string that the user can copy and paste.",
    )


class SystemInfo(BaseModel):
    os_name: str = Field(
        ...,
        description="The name of the operating system (e.g., 'Linux', 'Windows', 'Darwin').",
    )
    shell: str = Field(
        ...,
        description="The default shell being used (e.g., 'bash', 'zsh', 'cmd.exe').",
    )
    cwd: str = Field(..., description="The current working directory.")
    architecture: str = Field(
        ..., description="The system architecture (e.g., 'x86_64', 'arm64')."
    )
    python_version: Optional[str] = Field(
        None, description="The Python version being used."
    )


class AIContext(BaseModel):
    system_info: Optional[SystemInfo] = Field(
        None, description="Information about the user's system environment."
    )
    # Future context types can be added here (e.g., git_context, file_context)
