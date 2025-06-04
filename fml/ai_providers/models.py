from pydantic import BaseModel


class ModelProviderDetails(BaseModel):
    provider: str
    service: str
    env_var: str
    prompt_module: str
    prompt_variable: str


MODELS = {
    "gemini-1.5-flash": ModelProviderDetails(
        provider="fml.ai_providers.gemini_service",
        service="GeminiService",
        env_var="GEMINI_API_KEY",
        prompt_module="fml.prompts.gemini_system_prompt",
        prompt_variable="GEMINI_SYSTEM_PROMPT",
    ),
    # future models here
}
