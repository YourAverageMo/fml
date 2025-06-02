from pydantic import BaseModel, Field
from typing import List

class Flag(BaseModel):
    flag: str = Field(..., description="The flag or option used in the command (e.g., '--verbose' or '-v').")
    description: str = Field(..., description="A brief definition of what the flag does.")

class AICommandResponse(BaseModel):
    explanation: str = Field(..., description="A clear, concise explanation of the command's purpose, limited to 2-3 sentences.")
    flags: List[Flag] = Field(..., description="An array where each object represents a flag or option used in the command.")
    command: str = Field(..., description="The full, complete command string that the user can copy and paste.")
