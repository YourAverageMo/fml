import os
from enum import Enum
from fml.ai_service import AIService
from fml.schemas import AICommandResponse, AIContext
from google import genai
from google.genai.types import GenerateContentResponse


class GeminiModels(Enum):
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_1_5_PRO = "gemini-1.5-pro"


class GeminiService(AIService):
    """
    Concrete implementation of AIService for Google Gemini.
    """

    def __init__(self, api_key: str, system_instruction_path: str, model: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model

        # Read system instruction from file
        with open(system_instruction_path, "r") as f:
            self.system_instruction = f.read()

    @staticmethod
    def get_supported_models() -> list[str]:
        return [model.value for model in GeminiModels]

    def _generate_command_internal(self, query: str, ai_context: AIContext) -> AICommandResponse:
        contents_parts = [query]

        if ai_context.system_info:
            system_info_json = ai_context.system_info.model_dump_json(indent=2)
            contents_parts.append(f"\n\nUser's System Information:\n```json\n{system_info_json}\n```")

        response: GenerateContentResponse = self.client.models.generate_content(
            model=self.model_name,
            contents=contents_parts,
            config=genai.types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                response_mime_type="application/json",
                response_schema=AICommandResponse.model_json_schema(),
            ),
        )
        # Parse the JSON string into the Pydantic model
        return AICommandResponse.model_validate_json(response.text)
